from pathlib import Path
from typing import NamedTuple, Tuple, Optional

from poeditor.client import POEditorAPI


class State(NamedTuple):
    client: POEditorAPI
    config: dict
    config_path: Path
    languages: Tuple[str]

    @property
    def language(self) -> Optional[str]:
        """ Returns single language """
        if self.languages:
            return self.languages[0]
