import click.testing

from hypermoden_python_lucasmbastos import console

def test_main_succeeds():
	runner = click.testing.CliRunner()
	result = runner.invoke(console.main)
	assert result.exit_code == 0
