from pathlib import Path
import sys
import argparse
from typing import Any, Callable, Dict, TextIO, Tuple, Optional
from decimal import Decimal
import json
import datetime
from asyncio import run

from jsonschema import Draft4Validator, FormatChecker

from .file import set_schema, save_json, config_file, config_compression
from ._logger import get_logger
LOGGER = get_logger()


def _add_metadata_columns_to_schema(schema_message: Dict) -> Dict:
    '''Metadata _sdc columns according to the stitch documentation at
    https://www.stitchdata.com/docs/data-structure/integration-schemas#sdc-columns

    Metadata columns gives information about data injections
    '''
    schema_message['schema']['properties'].update(
        _sdc_batched_at={'type': ['null', 'string'], 'format': 'date-time'},
        _sdc_deleted_at={'type': ['null', 'string']},
        _sdc_extracted_at={'type': ['null', 'string'], 'format': 'date-time'},
        _sdc_primary_key={'type': ['null', 'string']},
        _sdc_received_at={'type': ['null', 'string'], 'format': 'date-time'},
        _sdc_sequence={'type': ['integer']},
        _sdc_table_version={'type': ['null', 'string']})

    return schema_message


def _add_metadata_values_to_record(record_message: Dict, schema_message: Dict, timestamp: datetime.datetime) -> Dict:
    '''Populate metadata _sdc columns from incoming record message
    The location of the required attributes are fixed in the stream
    '''
    utcnow = timestamp.astimezone(datetime.timezone.utc).replace(tzinfo=None).isoformat()
    # utcnow = timestamp.replace(tzinfo=None).isoformat()
    record_message['record'].update(
        _sdc_batched_at=utcnow,
        _sdc_deleted_at=record_message.get('record', {}).get('_sdc_deleted_at'),
        _sdc_extracted_at=record_message.get('time_extracted'),
        _sdc_primary_key=schema_message.get('key_properties'),
        _sdc_received_at=utcnow,
        _sdc_sequence=int(timestamp.timestamp() * 1000),
        _sdc_table_version=record_message.get('version'))

    return record_message['record']


def _remove_metadata_values_from_record(record_message: Dict) -> Dict:
    '''Removes every metadata _sdc column from a given record message
    '''
    for key in {
        '_sdc_batched_at',
        '_sdc_deleted_at',
        '_sdc_extracted_at',
        '_sdc_primary_key',
        '_sdc_received_at',
        '_sdc_sequence',
        '_sdc_table_version'
    }:

        record_message['record'].pop(key, None)

    return record_message['record']


def _float_to_decimal(value: Any) -> Any:
    '''Walk the given data structure and turn all instances of float into
    double.'''
    if isinstance(value, float):
        return Decimal(str(value))
    if isinstance(value, list):
        return [_float_to_decimal(child) for child in value]
    if isinstance(value, dict):
        return {k: _float_to_decimal(v) for k, v in value.items()}
    return value


def emit_state(state: Optional[Any]) -> None:
    if state is not None:
        line = json.dumps(state)
        LOGGER.debug(f'Emitting state {line}')
        sys.stdout.write(f'{line}\n')
        sys.stdout.flush()


class Loader():

    def __init__(self,
                 config: Dict,
                 set_schemas: Callable = set_schema,
                 writeline: Callable = save_json) -> None:
        self.config: Dict = config
        self.set_schemas: Callable = set_schemas
        self.writeline: Callable = writeline

    async def writelines(self, lines: TextIO = sys.stdin) -> Tuple[Optional[Any], Dict[Any, Any]]:
        '''Process the lines received from the Singer Tap.

        This is the core of the lines processing.
        Each line is processed function of its type, and the *RECORD* lines are saved using and functions provided as an argument.
        By default they are written as a *jsonl* in the *work_dir* working directory provided in the default `config` file.

        Parameters
        ----------
        lines: TextIO
            Input IO stream of lines
        config : dict
            configuration dictionary.
        set_schemas : Callable
            function used to process the schemas
        writeline : Callable
            function used to save the records

        Raises
        ------
        json.decoder.JSONDecodeError
            If the line structure is inconsistent or cnotains errors.

        Returns
        -------
        out : list[dict, dict]
            A `state` closure info.

        See Also
        --------
        `Singer spec <https://github.com/singer-io/getting-started/blob/master/docs/SPEC.md>`_ *convention* and *protocol*.
        '''

        state = None
        schemas = {}
        key_properties = {}
        validators: Dict = {}
        stream_data: Dict = {}

        for raw_line in lines:
            try:
                line = json.loads(raw_line)
            except json.decoder.JSONDecodeError:
                LOGGER.error(f'Unable to parse:\n{raw_line}')
                raise

            message_type = line['type']
            if message_type == 'SCHEMA':
                if 'stream' not in line:
                    raise Exception("Line is missing required key 'stream': {}".format(raw_line))
                stream = line['stream']

                schemas[stream] = _add_metadata_columns_to_schema(line) if self.config.get('add_metadata_columns') else _float_to_decimal(line['schema'])

                # NOTE: prevent exception *** jsonschema.exceptions.UnknownType: Unknown type 'SCHEMA' for validator.
                #       'type' is a key word for jsonschema validator which is different from `{'type': 'SCHEMA'}` as the message type.
                schemas[stream].pop('type')
                validators[stream] = Draft4Validator(schemas[stream], format_checker=FormatChecker())

                if 'key_properties' not in line:
                    raise Exception('key_properties field is required')
                key_properties[stream] = line['key_properties']
                LOGGER.debug('Setting schema for {}'.format(stream))

                self.set_schemas(stream, self.config, stream_data, schemas[stream])

            elif message_type == 'ACTIVATE_VERSION':
                LOGGER.debug('ACTIVATE_VERSION {}'.format(raw_line))

                # if version not in line:
                #     raise Exception(f'An ACTIVATE_VERSION value is expected for stream {stream}')

                # active_version = line['version']

            elif message_type == 'RECORD':
                if 'stream' not in line:
                    raise Exception(f"Line is missing required key 'stream': {raw_line}")
                stream = line['stream']

                if stream not in schemas:
                    raise Exception(f'A record for stream {stream} was encountered before a corresponding schema')

                record_to_load = line['record']

                # NOTE: Validate record
                validators[stream].validate(_float_to_decimal(record_to_load))

                record_to_load = _add_metadata_values_to_record(line, {}, self.config['date_time']) \
                    if self.config.get('add_metadata_columns') \
                    else _remove_metadata_values_from_record(line)

                await self.writeline(stream, stream_data, self.config, record_to_load)

                state = None

            elif message_type == 'STATE':
                LOGGER.debug('Setting state to %s', line['value'])
                state = line['value']

            else:
                LOGGER.warning('Unknown line type "{}" in line "{}"'.format(line['type'], line))

        for stream in stream_data:
            await self.writeline(stream, stream_data, self.config)

        self.state, self.stream_data = state, stream_data
        return self.state, self.stream_data

    async def sync(self, lines: TextIO = sys.stdin) -> None:

        await self.writelines(lines)

    def run(self, lines: TextIO = sys.stdin) -> None:

        run(self.sync(lines))

        emit_state(self.state)
        LOGGER.debug('Completed successfully')


def main(loader: type[Loader] = Loader, lines: TextIO = sys.stdin) -> None:
    '''Main'''
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', help='Config file', required=True)
    args = parser.parse_args()
    config = config_compression(config_file(json.loads(Path(args.config).read_text(encoding='utf-8'))))

    loader(config).run(lines)
