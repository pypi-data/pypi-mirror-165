# [Target Core](https://gitlab.com/singer-core/target-core)

[![GitLab - License](https://img.shields.io/gitlab/license/singer-core/target-core?color=blue)](https://gitlab.com/singer-core/target-core/-/blob/main/LICENSE)
[![Python package builder](https://gitlab.com/singer-core/target-core/badges/main/pipeline.svg)](https://gitlab.com/singer-core/target-core/pipelines)
[![Coverage](https://codecov.io/gl/singer-core/target-core/branch/main/graph/badge.svg?token=CM6FJI0P5D)](https://codecov.io/gl/singer-core/target-core)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/target-core.svg)](https://pypi.org/project/target-core)
[![PyPI version](https://badge.fury.io/py/target-core.svg)](https://badge.fury.io/py/target-core)
[![PyPi project installs](https://img.shields.io/pypi/dm/target-core.svg?maxAge=2592000&label=installs&color=%2327B1FF)](https://pypistats.org/packages/target-core)

<!-- [![Pypi - License](https://img.shields.io/pypi/l/target-core?color=yellow)](https://opensource.org/licenses/Apache-2.0) -->
<!-- [![Coverage](https://gitlab.com/singer-core/target-core/badges/main/coverage.svg)](https://gitlab.com/singer-core/target-core/-/graphs/main/charts) -->
<!-- [![Documentation Status](https://readthedocs.org/projects/target-core/badge/?version=latest)](https://singer-core.gitlab.io/target-core/en/latest/?badge=latest) -->
<!-- [![Latest Release](https://gitlab.com/singer-core/target-core/-/badges/release.svg)](https://gitlab.com/singer-core/target-core/-/releases) -->

[**Singer**](https://www.singer.io/) [`target-core`](https://gitlab.com/singer-core/target-core) provide safe tools to easily build new `targets` following the [*Singer spec*](https://github.com/singer-io/getting-started/blob/master/docs/SPEC.md) *convention* and *protocol*.

## How to use it

[`target-core`](https://singer-core.gitlab.io/target-core) is a [Singer](https://singer.io) Target which intend to work with regular [Singer](https://singer.io) Tap.

The Goal is to use this package as a foundation to build other taps focusing on the core tools, reducing the energy spent on maintaining the common parts.

## Packages extending the `target-core`
- [`target-s3-jsonl`](https://github.com/ome9ax/target-s3-jsonl)

## Install

First, make sure Python 3 is installed on your system or follow these
installation instructions for [Mac](http://docs.python-guide.org/en/latest/starting/install3/osx/) or
[Ubuntu](https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-local-programming-environment-on-ubuntu-16-04).

It's recommended to use a `venv`:

### Defaults
```bash
python -m venv venv
. venv/bin/activate
pip install --upgrade target-core
```

### Head
```bash
python -m venv venv
. venv/bin/activate
pip install --upgrade https+git@gitlab.com:omegax/target-core.git
```

### Isolated virtual environment
```bash
python -m venv ~/.virtualenvs/target-core
~/.virtualenvs/target-core/bin/pip install target-core
```

Alternative
```bash
python -m venv ~/.virtualenvs/target-core
source ~/.virtualenvs/target-core/bin/activate
pip install target-core
deactivate
```

### To run

Like any other target that's following the singer specificiation:

`some-singer-tap | target-core --config [config.json]`

It's reading incoming messages from STDIN and using the properites in `config.json` to upload the data.

**Note**: To avoid version conflicts run `tap` and `targets` in separate virtual environments.

### Configuration settings

Running the the target connector requires a `config.json` file. An example with the minimal settings:

```json
{
    "path_template": "{stream}_{date_time:%Y%m%d_%H%M%S}_part_{part:0>3}.json"
}
```

### Profile based authentication

Profile based authentication used by default using the `default` profile. To use another profile set `aws_profile` parameter in `config.json` or set the `AWS_PROFILE` environment variable.

### Non-Profile based authentication

For non-profile based authentication set `aws_access_key_id` , `aws_secret_access_key` and optionally the `aws_session_token` parameter in the `config.json`. Alternatively you can define them out of `config.json` by setting `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` and `AWS_SESSION_TOKEN` environment variables.


Full list of options in `config.json`:

| Property                            | Type    | Mandatory? | Description                                                   |
|-------------------------------------|---------|------------|---------------------------------------------------------------|
| path_template                   | String  |            | (Default: None) Custom naming convention of the s3 key. Replaces tokens `date`, `stream`, and `date_time` with the appropriate values.<br><br>Supports datetime and other python advanced string formatting e.g. `{stream}_{date_time:%FT%T.%f}.jsonl` or `{stream:_>8}/{date_time:%Y}/{date_time:%m}/{date_time:%d}/{date_time:%Y%m%d_%H%M%S_%f}.json`.<br><br>Supports "folders" in s3 keys e.g. `my_folder/my_sub_folder/{stream}/export_date={date}/{date_time}.json`.<br><br>Honors the `s3_key_prefix`,  if set, by prepending the "filename". E.g. path_template = `folder1/my_file.json` and s3_key_prefix = `prefix_` results in `folder1/prefix_my_file.json`. |
| timezone_offset                     | Integer |            | Offset value in hour. Use offset `0` hours is you want the `path_template` to use `utc` time zone. The `null` values is used by default. |
| memory_buffer                       | Integer |            | Memory buffer's size used before storing the data into the temporary file. 64Mb used by default if unspecified. This value is used to partition the files by size. |
| work_dir                            | String  |            | (Default: platform-dependent) Directory of temporary JSONL files with RECORD messages. |
| compression                         | String  |            | The type of compression to apply before uploading. Supported options are `none` (default), `gzip`, and `lzma`. For gzipped files, the file extension will automatically be changed to `.json.gz` for all files. For `lzma` compression, the file extension will automatically be changed to `.json.xz` for all files. |

## Test
Install the tools
```bash
pip install .[test,lint]
```

Run pytest
```bash
pytest -p no:cacheprovider
```

## Lint
```bash
flake8 --show-source --statistics --count --extend-exclude .virtualenvs
```

## Release
1. Update the version number at the beginning of `target-core/target_core/__init__.py`
2. Merge the changes PR into `main`
3. Create a tag `git tag -a 1.0.0 -m 'Release version 1.0.0'`
4. Release the new version in github

## License

Apache License Version 2.0

<!---

# Utils
## Getting started

To make it easy for you to get started with GitLab, here's a list of recommended next steps.

Already a pro? Just edit this README.md and make it your own. Want to make it easy? [Use the template at the bottom](#editing-this-readme)!

## Add your files

- [ ] [Create](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#create-a-file) or [upload](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#upload-a-file) files
- [ ] [Add files using the command line](https://docs.gitlab.com/ee/gitlab-basics/add-file.html#add-a-file-using-the-command-line) or push an existing Git repository with the following command:

```
cd existing_repo
git remote add origin https://gitlab.com/singer-core/target-core.git
git branch -M main
git push -uf origin main
```

## Integrate with your tools

- [ ] [Set up project integrations](https://gitlab.com/singer-core/target-core/-/settings/integrations)

## Collaborate with your team

- [ ] [Invite team members and collaborators](https://docs.gitlab.com/ee/user/project/members/)
- [ ] [Create a new merge request](https://docs.gitlab.com/ee/user/project/merge_requests/creating_merge_requests.html)
- [ ] [Automatically close issues from merge requests](https://docs.gitlab.com/ee/user/project/issues/managing_issues.html#closing-issues-automatically)
- [ ] [Enable merge request approvals](https://docs.gitlab.com/ee/user/project/merge_requests/approvals/)
- [ ] [Automatically merge when pipeline succeeds](https://docs.gitlab.com/ee/user/project/merge_requests/merge_when_pipeline_succeeds.html)

## Test and Deploy

Use the built-in continuous integration in GitLab.

- [ ] [Get started with GitLab CI/CD](https://docs.gitlab.com/ee/ci/quick_start/index.html)
- [ ] [Analyze your code for known vulnerabilities with Static Application Security Testing(SAST)](https://docs.gitlab.com/ee/user/application_security/sast/)
- [ ] [Deploy to Kubernetes, Amazon EC2, or Amazon ECS using Auto Deploy](https://docs.gitlab.com/ee/topics/autodevops/requirements.html)
- [ ] [Use pull-based deployments for improved Kubernetes management](https://docs.gitlab.com/ee/user/clusters/agent/)
- [ ] [Set up protected environments](https://docs.gitlab.com/ee/ci/environments/protected_environments.html)

***

# Editing this README

When you're ready to make this README your own, just edit this file and use the handy template below (or feel free to structure it however you want - this is just a starting point!).  Thank you to [makeareadme.com](https://www.makeareadme.com/) for this template.

## Suggestions for a good README
Every project is different, so consider which of these sections apply to yours. The sections used in the template are suggestions for most open source projects. Also keep in mind that while a README can be too long and detailed, too long is better than too short. If you think your README is too long, consider utilizing another form of documentation rather than cutting out information.

## Name
Choose a self-explaining name for your project.

## Description
Let people know what your project can do specifically. Provide context and add a link to any reference visitors might be unfamiliar with. A list of Features or a Background subsection can also be added here. If there are alternatives to your project, this is a good place to list differentiating factors.

## Badges
On some READMEs, you may see small images that convey metadata, such as whether or not all the tests are passing for the project. You can use Shields to add some to your README. Many services also have instructions for adding a badge.

## Visuals
Depending on what you are making, it can be a good idea to include screenshots or even a video (you'll frequently see GIFs rather than actual videos). Tools like ttygif can help, but check out Asciinema for a more sophisticated method.

## Installation
Within a particular ecosystem, there may be a common way of installing things, such as using Yarn, NuGet, or Homebrew. However, consider the possibility that whoever is reading your README is a novice and would like more guidance. Listing specific steps helps remove ambiguity and gets people to using your project as quickly as possible. If it only runs in a specific context like a particular programming language version or operating system or has dependencies that have to be installed manually, also add a Requirements subsection.

## Usage
Use examples liberally, and show the expected output if you can. It's helpful to have inline the smallest example of usage that you can demonstrate, while providing links to more sophisticated examples if they are too long to reasonably include in the README.

## Support
Tell people where they can go to for help. It can be any combination of an issue tracker, a chat room, an email address, etc.

## Roadmap
If you have ideas for releases in the future, it is a good idea to list them in the README.

## Contributing
State if you are open to contributions and what your requirements are for accepting them.

For people who want to make changes to your project, it's helpful to have some documentation on how to get started. Perhaps there is a script that they should run or some environment variables that they need to set. Make these steps explicit. These instructions could also be useful to your future self.

You can also document commands to lint the code or run tests. These steps help to ensure high code quality and reduce the likelihood that the changes inadvertently break something. Having instructions for running tests is especially helpful if it requires external setup, such as starting a Selenium server for testing in a browser.

## Authors and acknowledgment
Show your appreciation to those who have contributed to the project.

## License
For open source projects, say how it is licensed.

## Project status
If you have run out of energy or time for your project, put a note at the top of the README saying that development has slowed down or stopped completely. Someone may choose to fork your project or volunteer to step in as a maintainer or owner, allowing your project to keep going. You can also make an explicit request for maintainers.

-->
