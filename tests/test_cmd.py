from unittest import TestCase

from click.testing import CliRunner, Result

from poeditor_sync.cmd import poeditor


class CmdReadOnlyTokenTest(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.runner = CliRunner(env={
            'POEDITOR_CONFIG_FILE': 'test.yml',
        })

    def test_poeditor(self):
        result: Result = self.runner.invoke(poeditor)
        self.assertEqual(result.exit_code, 0)
        self.assertTrue(result.stdout.startswith('Usage: poeditor'))

    def test_poeditor_pull(self):
        result: Result = self.runner.invoke(poeditor, ['pull'])
        self.assertEqual(result.exit_code, 0, result.stdout)

    def test_poeditor_push(self):
        result: Result = self.runner.invoke(poeditor, 'push')
        self.assertEqual(result.exit_code, 1)

    def test_poeditor_push_terms(self):
        result: Result = self.runner.invoke(poeditor, 'push')
        self.assertEqual(result.exit_code, 1)
