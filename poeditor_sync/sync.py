import yaml
from poeditor.client import POEditorAPI


def get_config(config_file) -> dict:
    config = yaml.safe_load(config_file)
    return config


def get_client(config: dict, token=None) -> POEditorAPI:
    if not token:
        token = config['api_token']
    return POEditorAPI(token)
