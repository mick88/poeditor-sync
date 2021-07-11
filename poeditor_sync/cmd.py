import os
from time import sleep
from typing import Sequence

from click import option, echo, group, argument, File, Choice, STRING
from poeditor.client import POEditorAPI

from poeditor_sync.sync import get_client, get_config, get_project_languages


@group()
@option('--config-file', envvar='POEDITOR_CONFIG_FILE', default='poeditor.yml', type=File(), help='Path to the project config file. You can also set environment variable POEDITOR_CONFIG_FILE')
@option('--token', envvar='POEDITOR_TOKEN', type=STRING, help="API token for POEditor. You can generate it at https://poeditor.com/account/api. You can also set environment variable POEDITOR_TOKEN.")
def poeditor(config_file, token):
    global client, config
    config = get_config(config_file)
    client = get_client(config, token)


@poeditor.command('push-terms')
@option('--reference-language', default=None, help="Language that has the complete list of terms to update. Defaults to project's reference language")
@argument('overwrite', default=False)
@argument('sync-terms', default=False)
def push_terms(reference_language: str, overwrite: bool, sync_terms: bool):
    """
    Uploads list of terms in your local project to POEditor.
    overwrite - Whether translations should be overwritten
    sync-terms - Whether to delete terms that are not present in pushed language
    """
    for project in config['projects']:
        if not reference_language:
            project_details = client.view_project_details(project['id'])
            reference_language = project_details.get('reference_language')
            if not reference_language:
                raise ValueError(f"project {project_details['name']} does not define reference language. Please pass --reference-language option to select which language to use.")
        name = client.view_project_details(project_id=project['id']).get('name')
        echo(f"Pushing terms to {name} using '{reference_language}'...", nl=False)
        client.update_terms(
            project_id=project['id'],
            file_path=project['terms'][reference_language],
            sync_terms=sync_terms,
            overwrite=overwrite,
        )
        echo('done!')


@poeditor.command('push')
@argument('overwrite', default=False)
@argument('sync-terms', default=False)
def push_translations(overwrite: bool, sync_terms: bool):
    """
    Upload local translations to POEditor
    """
    for project in config['projects']:
        name = client.view_project_details(project_id=project['id']).get('name')
        echo(f"Pushing {name} translations...", nl=False)
        for n, (language, path) in enumerate(get_project_languages(project, client)):
            if n:
                sleep(30)
            echo(f' {language}', nl=False)
            client.update_terms_translations(
                project['id'],
                path,
                language,
                overwrite=overwrite,
                sync_terms=sync_terms,
            )
        echo('')


@poeditor.command('pull')
@argument('filters', type=Choice(POEditorAPI.FILTER_BY), required=False, nargs=-1)
def pull_translations(filters: Sequence[str]):
    """
    Download translated strings from POEditor
    """
    for project in config['projects']:
        name = client.view_project_details(project_id=project['id']).get('name')
        echo(f"Pulling {name} translations...", nl=False)
        file_type = project['format']
        for language, path in get_project_languages(project, client):
            echo(f' {language}', nl=False)
            directories = os.path.dirname(path)
            if directories and not os.path.exists(directories):
                os.makedirs(directories)
            client.export(
                project['id'],
                language_code=language,
                local_file=path,
                file_type=file_type,
                filters=filters or None,
            )
        echo('')


@poeditor.command('project-details')
def project_details():
    """
    Shows details of POEditor projects defined in config
    :return:
    """
    for project in config['projects']:
        project_id = project['id']
        echo(f"- Project: {project_id}")
        details = client.view_project_details(project_id=project_id)
        for key, value in details.items():
            echo(f"  {key}: {value}")
        echo(f"  Languages:")
        for language in client.list_project_languages(project_id=project_id):
            name = language.pop('name')
            lang_details = ', '.join(f"{k}={v}" for k, v in language.items())
            echo(f"  - {name}: {lang_details}")


if __name__ == '__main__':
    poeditor()
