import os
from pathlib import Path
from time import sleep
from typing import Sequence

import click
import yaml
from poeditor.client import POEditorAPI

from poeditor_sync.models import State
from poeditor_sync.sync import get_client, get_config, get_project_languages


@click.group()
@click.option('--config-file', '-f', envvar='POEDITOR_CONFIG_FILE', default='poeditor.yml', type=click.Path(path_type=Path), help='Path to the project config file. You can also set environment variable POEDITOR_CONFIG_FILE')
@click.option('--token', '-t', envvar='POEDITOR_TOKEN', type=click.STRING, help="API token for POEditor. You can generate it at https://poeditor.com/account/api. You can also set environment variable POEDITOR_TOKEN.")
@click.option('--language', '-l', envvar='POEDITOR_LANGUAGE', type=click.STRING, help="Only push/pull this language", multiple=True)
@click.pass_context
def poeditor(context: click.Context, config_file: Path, token: str, language: Sequence[str]):
    if config_file.exists():
        config = get_config(config_file)
        token = token or config['api_token']
    else:
        # Create blank config if it does not exist
        config = {'projects': ()}
    client = get_client(token or config.get('api_token'))
    context.obj = State(client, config, config_file, tuple(language))


@poeditor.command('push-terms')
@click.option('--overwrite', '-o', default=False, is_flag=True, help='Whether translations should be overwritten')
@click.option('--sync-terms', '-s', default=False, is_flag=True, help='Whether to delete terms that are not present in pushed language')
@click.pass_obj
def push_terms(obj: State, overwrite: bool, sync_terms: bool):
    """
    Uploads list of terms in your local project to POEditor.
    """
    if not obj.config_path.exists():
        raise click.FileError(obj.config_path.name, 'Config file does not exist')

    config = obj.config
    client = obj.client
    reference_language = obj.language

    for n, project in enumerate(config['projects']):
        if not reference_language:
            project_details = client.view_project_details(project['id'])
            reference_language = project_details.get('reference_language')
            if not reference_language:
                raise click.ClickException(f"project {project_details['name']} does not define reference language. Please pass --reference-language option to select which language to use.")
        name = client.view_project_details(project_id=project['id']).get('name')
        click.echo(f"Pushing terms to {name} using '{reference_language}'...", nl=False)
        try:
            translation_file = project['terms'][reference_language]
        except KeyError:
            translation_file = project['terms_path'].format(language_code=reference_language)
        if n:
            sleep(30)
        client.update_terms(
            project_id=project['id'],
            file_path=translation_file,
            sync_terms=sync_terms,
            overwrite=overwrite,
        )
        click.echo('done!')


@poeditor.command('push')
@click.option('--overwrite', '-o', default=False, is_flag=True, help='Whether translations should be overwritten')
@click.option('--sync-terms', '-s', default=False, is_flag=True, help='Whether to delete terms that are not present in pushed language')
@click.pass_obj
def push_translations(obj: State, overwrite: bool, sync_terms: bool):
    """
    Upload local translations to POEditor
    """
    if not obj.config_path.exists():
        raise click.FileError(obj.config_path.name, 'Config file does not exist')
    config = obj.config
    client = obj.client
    for np, project in enumerate(config['projects']):
        name = client.view_project_details(project_id=project['id']).get('name')
        click.echo(f"Pushing {name} translations...", nl=False)
        for nl, (language, path) in enumerate(get_project_languages(project, client, obj.languages)):
            if nl or np:
                sleep(31)
            click.echo(f' {language}', nl=False)
            client.update_terms_translations(
                project['id'],
                path,
                language,
                overwrite=overwrite,
                sync_terms=sync_terms,
            )
        click.echo('')


@poeditor.command('pull')
@click.argument('filters', type=click.Choice(POEditorAPI.FILTER_BY), required=False, nargs=-1)
@click.pass_obj
def pull_translations(obj: State, filters: Sequence[str]):
    """
    Download translated strings from POEditor
    """
    if not obj.config_path.exists():
        raise click.FileError(obj.config_path.name, 'Config file does not exist')
    config = obj.config
    client = obj.client
    for project in config['projects']:
        name = client.view_project_details(project_id=project['id']).get('name')
        click.echo(f"Pulling {name} translations...", nl=False)
        file_type = project['format']
        for language, path in get_project_languages(project, client, obj.languages):
            click.echo(f' {language}', nl=False)
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
        click.echo('')


@poeditor.command('project-details')
@click.pass_obj
def project_details(obj: State):
    """
    Shows details of POEditor projects defined in config
    """
    if not obj.config_path.exists():
        raise click.FileError(obj.config_path.name, 'Config file does not exist')
    config = obj.config
    client = obj.client
    for project in config['projects']:
        project_id = project['id']
        click.echo(f"- Project: {project_id}")
        details = client.view_project_details(project_id=project_id)
        for key, value in details.items():
            click.echo(f"  {key}: {value}")
        click.echo(f"  Languages:")
        for language in client.list_project_languages(project_id=project_id):
            name = language.pop('name')
            lang_details = ', '.join(f"{k}={v}" for k, v in language.items())
            click.echo(f"  - {name}: {lang_details}")


@poeditor.command('init')
@click.argument('project_ids', nargs=-1, type=click.INT)
@click.pass_obj
def init(obj: State, project_ids: Sequence[int]):
    """
    Creates a config file for given project ids
    """
    if obj.config_path.exists() and not click.confirm(f"Config file {obj.config_path} already exists. Overwrite?"):
        return
    config = {
        'api_token': obj.client.api_token or '',
        'projects': [],
    }
    for project_id in project_ids:
        config['projects'].append({
            'id': project_id,
            'format': 'po',
            'terms_path': "Example: locales/{language_code}.po",
            'terms': {
                language['code']: ''
                for language in obj.client.list_project_languages(project_id)
            },
        })
    if not project_ids:
        languages = obj.languages or ('en', 'es')
        config['projects'].append({
            'id': '',
            'format': 'po',
            'terms_path': '',
            'terms': {code: '' for code in languages},
        })

    with open(obj.config_path, 'w') as yaml_file:
        yaml.dump(config, yaml_file)
    click.echo(f"""Created file '{obj.config_path}' initialized with project config.
Please edit the file and fill in correct file format and translation paths:
- format: The following formats are supported: {', '.join(POEditorAPI.FILE_TYPES)}
- terms_path: file path template for translation files
- terms: optionally, specify a separate path for each language (overrides terms_path)
For more information about configuration visit https://github.com/mick88/poeditor-sync/blob/master/README.md#configuration""")


if __name__ == '__main__':
    poeditor()
