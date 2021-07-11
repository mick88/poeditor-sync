from unittest import TestCase

from click.testing import CliRunner, Result

from poeditor_sync.cmd import poeditor


class CmdReadOnlyTokenTest(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.runner = CliRunner(env={
            'POEDITOR_CONFIG_FILE': 'tests/test.yml',
            'POEDITOR_TOKEN': 'e1fc095d70eba2395fec56c6ad9e61c3',
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

    def test_poeditor_init_blank(self):
        result: Result = self.runner.invoke(poeditor, args=['--config-file', 'test_blank_init.yml', 'init'])
        self.assertEqual(result.exit_code, 0, result.stdout)

    def test_poeditor_init_project_id(self):
        result: Result = self.runner.invoke(poeditor, args=['--config-file', 'test_init_projectid.yml', 'init', '458528'])
        self.assertEqual(result.exit_code, 0, result.stdout)
