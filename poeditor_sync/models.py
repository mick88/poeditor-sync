from pathlib import Path
from typing import NamedTuple

from poeditor.client import POEditorAPI


class State(NamedTuple):
    client: POEditorAPI
    config: dict
    config_path: Path
