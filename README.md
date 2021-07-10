# POEditor sync
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
Create a config file `poeditor.yml` to link your project with a POEditor project and define paths to translation files. For example.
```yml
api_token: ABC123...
projects:
  - id: 12345
    format: po
    default_language: en
    terms:
      en: locale/en/LC_MESSAGES/django.js
      pl: locale/pl/LC_MESSAGES/django.js

```
The API token in your config file can be a read-only token. You can use a separate token for uploads and pass it using `--token` option or `POEDITOR_TOKEN` environment variable.
