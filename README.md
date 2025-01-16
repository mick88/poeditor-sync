# POEditor sync
[![Tests](https://github.com/mick88/poeditor-sync/actions/workflows/python-test.yml/badge.svg?branch=master)](https://github.com/mick88/poeditor-sync/actions)
[![poeditor-sync](https://badge.fury.io/py/poeditor-sync.svg)](https://badge.fury.io/py/poeditor-sync)

A commandline tool for synchronizing your project's translation with [POEditor](https://poeditor.com/).

The script uses [Click](https://pypi.org/project/click/) library to wrap [POEditor API client](https://pypi.org/project/poeditor/) into a commandline tool that can be used manually or inside shell scripts.

## Installation
```shell
pip install poeditor-sync
```

## Usage

### Configuration
Create a config file `poeditor.yml` to link your project with a POEditor project and define paths to translation files. Multiple projects are supported.
```yml
api_token: ABC123...
projects:
  - id: 12345
    format: po
    # set it to terms to order results by 'terms' alphabetically.
    order: terms
    # generic path to translation file
    terms_path: locale/{language_code}/LC_MESSAGES/django.po
    # alternatively, specify per-language path
    terms:
      en: locale/en/LC_MESSAGES/django.po
      pl: locale/pl/LC_MESSAGES/django.po
  - id: 54321
    format: po
    terms_path: locale/{language_code}/LC_MESSAGES/djangojs.po
    terms:
      en: locale/en/LC_MESSAGES/djangojs.po
      pl: locale/pl/LC_MESSAGES/djangojs.po

```
If you're planning to commit the config file into your repository or share it with someone, it is recommend that the API token in your config file be a read-only token.
You can use a separate token for uploads and pass it using `--token` option or `POEDITOR_TOKEN` environment variable.

### Commands:
```shell
# View usage instructions
poeditor --help
# generate config file
poeditor init {project-id}
# List projects and their translation languages
poeditor project-details
# download translations
poeditor pull
# Upload local translations to poeditor
poeditur push
# Upload only one language and user a different API token:
poeditur --language pl --token=123ABCD push
# Upload only terms (after adding new strings to the project)
poeditor push-terms --sync-terms --overwrite
```

### Options
| Option          | environment variable   | default value                | description                                                          |
|-----------------|------------------------|------------------------------|----------------------------------------------------------------------|
| `--token`       | `POEDITOR_TOKEN`       | _api_token from config file_ | Authentication token for POEditor. Overrides value from config file. 
| `--config-file` | `POEDITOR_CONFIG_FILE` | poeditor.yml                 | Path to the project config file in yaml format                       
| `--language`    | `POEDITOR_LANGUAGE`    |                              | Operate only on this language                    
