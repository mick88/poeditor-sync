import os

from click import option, echo, group, argument, File, Choice, STRING
from poeditor.client import POEditorAPI

from poeditor_sync.sync import get_client, get_config


@group()
@option('--config-file', envvar='POEDITOR_CONFIG_FILE', default='poeditor.yml', type=File())
@option('--token', envvar='POEDITOR_TOKEN', type=STRING)
def poeditor(config_file, token):
    global client, config
    config = get_config(config_file)
    client = get_client(config, token)


@poeditor.command('push-terms')
@option('--language-code', default=None)
@argument('overwrite', default=False)
@argument('sync-terms', default=False)
def push_terms(language_code: str, overwrite: bool, sync_terms: bool):
    for project in config['projects']:
        language = language_code or project.get('default_language', 'en')
        name = client.view_project_details(project_id=project['id']).get('name')
        echo(f"Pushing terms to {name}")
        client.update_terms(
            project_id=project['id'],
            file_path=project['terms'][language],
            sync_terms=sync_terms,
            overwrite=overwrite,
        )


@poeditor.command('push')
@argument('overwrite', default=False)
@argument('sync-terms', default=False)
def push_translations(overwrite: bool, sync_terms: bool):
    for project in config['projects']:
        name = client.view_project_details(project_id=project['id']).get('name')
        echo(f"Pushing {name} translations...", nl=False)
        for language, path in project['terms'].items():
            client.update_terms_translations(
                project['id'],
                path,
                language,
                overwrite=overwrite,
                sync_terms=sync_terms,
            )


@poeditor.command('pull')
@argument('filters', type=Choice(POEditorAPI.FILTER_BY), required=False, nargs=-1)
def pull_translations(filters: tuple[str]):
    for project in config['projects']:
        name = client.view_project_details(project_id=project['id']).get('name')
        echo(f"Pulling {name} translations...", nl=False)
        file_type = project['format']
        for language, path in project['terms'].items():
            echo(f' {language}', nl=False)
            client.export(
                project['id'],
                language_code=language,
                local_file=path,
                file_type=file_type,
                filters=filters or None,
            )
        echo('')


if __name__ == '__main__':
    poeditor()