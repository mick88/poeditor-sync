import warnings
from pathlib import Path
from typing import Tuple, Iterator

import yaml
from poeditor.client import POEditorAPI


def get_config(config_file: Path) -> dict:
    with open(config_file) as yaml_file:
        return yaml.safe_load(yaml_file)


def get_client(token=None) -> POEditorAPI:
    return POEditorAPI(token)


def get_project_languages(project: dict, client: POEditorAPI) -> Iterator[Tuple[str, str]]:
    for language in client.list_project_languages(project_id=project['id']):
        language_code = language['code']
        translation_path: str
        terms = project.get('terms')
        if terms and language_code in terms:
            translation_path = project['terms'][language_code]
        elif project.get('terms_path'):
            translation_path = project.get('terms_path').format(language_code=language_code)
        else:
            msg = f"Project {project['id']} does not define path for {language['name']} ({language_code}). Add translation path to the 'terms' dictionary or define a generic path in 'terms_path'"
            warnings.warn(msg)
            continue
        yield language_code, translation_path
