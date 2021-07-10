import warnings
from typing import Tuple, Iterator

import yaml
from poeditor.client import POEditorAPI


def get_config(config_file) -> dict:
    config = yaml.safe_load(config_file)
    return config


def get_client(config: dict, token=None) -> POEditorAPI:
    if not token:
        token = config['api_token']
    return POEditorAPI(token)


def get_project_languages(project: dict, client: POEditorAPI) -> Iterator[Tuple[str, str]]:
    for language in client.list_project_languages(project_id=project['id']):
        language_code = language['code']
        translation_path: str
        if language_code in project['terms']:
            translation_path = project['terms'][language_code]
        elif project.get('terms_path'):
            translation_path = project.get('terms_path').format(language_code=language_code)
        else:
            msg = f"Project {project['id']} does not define path for {language['name']} ({language_code}). Add translation path to the 'terms' dictionary or define a generic path in 'terms_path'"
            warnings.warn(msg)
            continue
        yield language_code, translation_path
