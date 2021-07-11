from typing import Optional, NamedTuple

from poeditor.client import POEditorAPI


class State(NamedTuple):
    client: POEditorAPI
    config: Optional[dict] = None
