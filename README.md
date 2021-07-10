# POEditor sync
![Tests](https://github.com/mick88/poeditor-sync/actions/workflows/python-test.yml/badge.svg?branch=master)
[![poeditor-sync](https://badge.fury.io/py/poeditor-sync.svg)](https://badge.fury.io/py/poeditor-sync)

A commandline tool for synchronizing your project's translation with [POEditor](https://poeditor.com/)

## Installation
```shell
pip install poeditor-sync
```

## Usage
### Commands:
```shell
# download translations
poeditor pull
# Upload local translations to poeditor
poeditur push
# Upload only terms (after adding new strings to the project)
poeditor push-terms --sync-terms --overwrite
```

### Configuration
Create a config file `poeditor.yml` to link your project with a POEditor project and define paths to translation files. Multiple projects are supported.
```yml
api_token: ABC123...
projects:
  - id: 12345
    format: po
    default_language: en
    terms:
      en: locale/en/LC_MESSAGES/django.po
      pl: locale/pl/LC_MESSAGES/django.po
  - id: 54321
    format: po
    default_language: en
    terms:
      en: locale/en/LC_MESSAGES/djangojs.po
      pl: locale/pl/LC_MESSAGES/djangojs.po

```
If you're planning to check the file into your code repository or share it with someone the API token in your config file can be a read-only token. 
You can use a separate token for uploads and pass it using `--token` option or `POEDITOR_TOKEN` environment variable.

### Options

| Option          | environment variable   | default value                 | documentation |
|-----------------|------------------------|-------------------------------|---------------|
| `--token`       | `POEDITOR_TOKEN`       | _api_token from config file_  | Authentication token for POEditor. Overrides value from config file.
| `--config-file` | `POEDITOR_CONFIG_FILE` | poeditor.yml                  | Path to the project config file in yaml format
