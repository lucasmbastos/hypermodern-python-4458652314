from unittest.mock import Mock

import click.testing
from click.testing import CliRunner
import pytest
from pytest_mock import MockFixture
import requests

from hypermodern_python_lucasmbastos import console


@pytest.fixture
def runner() -> CliRunner:
    return click.testing.CliRunner()


@pytest.fixture
def mock_wikipedia_random_page(mocker: Mock) -> MockFixture:
    return mocker.patch("hypermodern_python_lucasmbastos.wikipedia.random_page")


def test_main_succeeds(runner: CliRunner, mock_requests_get: MockFixture) -> None:
    result = runner.invoke(console.main)
    assert result.exit_code == 0


def test_main_prints_title(runner: CliRunner, mock_requests_get: MockFixture) -> None:
    result = runner.invoke(console.main)
    assert "Lorem Ipsum" in result.output


def test_main_invokes_request_get(
    runner: CliRunner, mock_requests_get: MockFixture
) -> None:
    runner.invoke(console.main)
    assert mock_requests_get.called


def test_main_uses_en_wikipedia_org(
    runner: CliRunner, mock_requests_get: MockFixture
) -> None:
    runner.invoke(console.main)
    args, _ = mock_requests_get.call_args
    assert "en.wikipedia.org" in args[0]


def test_main_fails_on_request_error(
    runner: CliRunner, mock_requests_get: MockFixture
) -> None:
    mock_requests_get.side_effect = Exception("Boom")
    result = runner.invoke(console.main)
    assert result.exit_code == 1


def test_main_prints_message_on_request_error(
    runner: CliRunner, mock_requests_get: MockFixture
) -> None:
    mock_requests_get.side_effect = requests.RequestException
    result = runner.invoke(console.main)
    assert "Error" in result.output


def test_main_uses_specified_language(
    runner: CliRunner, mock_wikipedia_random_page: MockFixture
) -> None:
    runner.invoke(console.main, ["--language=pl"])
    mock_wikipedia_random_page.assert_called_with(language="pl")


# Tutorial has a little tougths on Fakes. It will not implements any fakes, but
# it has a recommendation of installing the https://factoryboy.readthedocs.io/
# package. Futhermore it has some advices on tests that uses teardown.


@pytest.mark.e2e
def test_main_succeeds_in_production_env(runner: CliRunner) -> None:
    result = runner.invoke(console.main)
    assert result.exit_code == 0
