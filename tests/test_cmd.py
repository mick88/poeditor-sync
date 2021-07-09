from unittest import TestCase

from click.testing import CliRunner

from poeditor_sync.cmd import poeditor


class CmdTest(TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.runner = CliRunner()

    def test_poeditor(self):
        self.runner.invoke(poeditor)

    def test_poeditor_pull(self):
        self.runner.invoke(poeditor, 'pull')
