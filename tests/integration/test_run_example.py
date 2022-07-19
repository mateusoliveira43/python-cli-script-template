"""Integration tests of module scripts.run_example."""

import sys
from runpy import run_path
from typing import List
from unittest.mock import patch

import pytest

from example.example_cli import COMMANDS
from tests import ABSOLUTE_PATH

EXAMPLE_FILE = (ABSOLUTE_PATH / "run_example.py").as_posix()
ARGUMENTS = {
    "help": ["-h", "--help"],
    "version": ["-v", "--version"],
    "optional": ["-o", "--optional"],
}
INVALID_FLAGS = ["-k", "--invalid"]

USAGE = "Usage:\n  [python|python3] "
OPTIONS = ["[-h]", "[-v]", "[-o]", "[COMMAND]", "..."]
OPTIONS_COMMAND = ["[-h]", "(-t str | -n int)", "..."]

UNRECOGNIZED_ARGUMENTS = "error: unrecognized arguments"
INVALID_CHOICE = "invalid choice"
INVALID_INT_VALUE = "invalid int value"

INVALID_COMMANDS = ["riddler", "joker"]
TEXT_OPTION_TEST_DATA = ["1", "batman", "nightwing"]
NUMBER_OPTION_TEST_DATA = ["1", "37", "-4"]
ARGUMENTS_OPTION_TEST_DATA = [["1.9"], ["-0.7"], ["batman", "joker", "robin"]]
INVALID_NUMBER_OPTION_TEST_DATA = ["1.9", "joker", "-0.7", "1,7"]
INVALID_ARGUMENTS_OPTION_TEST_DATA = [["-k"], ["-v"], ["-batman", "joker"]]


def test_main_without_options(capsys: pytest.CaptureFixture[str]) -> None:
    """Test main without options."""
    sys_mock = ["file_name"]
    with patch.object(sys, "argv", sys_mock):
        with pytest.raises(SystemExit) as sys_exit:
            run_path(EXAMPLE_FILE, run_name="__main__")
    output, error = capsys.readouterr()
    assert not error
    assert USAGE in output
    assert all(option in output for option in OPTIONS)
    assert sys_exit.type == SystemExit
    assert sys_exit.value.code == 0


@pytest.mark.parametrize("option", ARGUMENTS["help"])
def test_main_with_option_help(
    option: str, capsys: pytest.CaptureFixture[str]
) -> None:
    """Test main with option help."""
    sys_mock = ["file_name", option]
    with patch.object(sys, "argv", sys_mock):
        with pytest.raises(SystemExit) as sys_exit:
            run_path(EXAMPLE_FILE, run_name="__main__")
    output, error = capsys.readouterr()
    assert not error
    assert USAGE in output
    assert all(option in output for option in OPTIONS)
    assert sys_exit.type == SystemExit
    assert sys_exit.value.code == 0


@pytest.mark.parametrize("option", ARGUMENTS["version"])
def test_main_with_option_version(
    option: str, capsys: pytest.CaptureFixture[str]
) -> None:
    """Test main with option version."""
    sys_mock = ["file_name", option]
    with patch.object(sys, "argv", sys_mock):
        with pytest.raises(SystemExit) as sys_exit:
            run_path(EXAMPLE_FILE, run_name="__main__")
    output, error = capsys.readouterr()
    assert not error
    assert all(
        word in output for word in ["Script", "name", "version", "1.0.0", "\n"]
    )
    assert sys_exit.type == SystemExit
    assert sys_exit.value.code == 0


@pytest.mark.parametrize("option", ARGUMENTS["optional"])
def test_main_with_option_optional(
    option: str, capfd: pytest.CaptureFixture[str]
) -> None:
    """Test main with option optional."""
    sys_mock = ["file_name", option]
    with patch.object(sys, "argv", sys_mock):
        run_path(EXAMPLE_FILE, run_name="__main__")
    output, error = capfd.readouterr()
    assert not error
    assert USAGE not in output
    assert not all(option in output for option in OPTIONS)
    assert "Optional flag called." in output
    assert "poetry.lock" in output


@pytest.mark.parametrize("option", INVALID_FLAGS)
def test_main_with_invalid_options(
    option: str, capsys: pytest.CaptureFixture[str]
) -> None:
    """Test main with invalid options."""
    sys_mock = ["file_name", option]
    with patch.object(sys, "argv", sys_mock):
        with pytest.raises(SystemExit) as sys_exit:
            run_path(EXAMPLE_FILE, run_name="__main__")
    output, error = capsys.readouterr()
    assert UNRECOGNIZED_ARGUMENTS in error
    assert not output
    assert sys_exit.type == SystemExit
    assert sys_exit.value.code == 2


@pytest.mark.parametrize("command", INVALID_COMMANDS)
def test_main_invalid_commands(
    command: str, capsys: pytest.CaptureFixture[str]
) -> None:
    """Test main invalid commands."""
    sys_mock = ["file_name", command]
    with patch.object(sys, "argv", sys_mock):
        with pytest.raises(SystemExit) as sys_exit:
            run_path(EXAMPLE_FILE, run_name="__main__")
    output, error = capsys.readouterr()
    assert INVALID_CHOICE in error
    assert not output
    assert sys_exit.type == SystemExit
    assert sys_exit.value.code == 2


@pytest.mark.parametrize("command", COMMANDS)
def test_main_commands_without_options(
    command: str, capsys: pytest.CaptureFixture[str]
) -> None:
    """Test main commands without options."""
    sys_mock = ["file_name", command]
    with patch.object(sys, "argv", sys_mock):
        with pytest.raises(SystemExit) as sys_exit:
            run_path(EXAMPLE_FILE, run_name="__main__")
    output, error = capsys.readouterr()
    assert not output
    assert "one of the arguments" in error
    assert "is required" in error
    assert sys_exit.type == SystemExit
    assert sys_exit.value.code == 2


@pytest.mark.parametrize("option", ARGUMENTS["help"])
@pytest.mark.parametrize("command", COMMANDS)
def test_main_commands_with_option_help(
    command: str, option: str, capsys: pytest.CaptureFixture[str]
) -> None:
    """Test main commands with option help."""
    sys_mock = ["file_name", command, option]
    with patch.object(sys, "argv", sys_mock):
        with pytest.raises(SystemExit) as sys_exit:
            run_path(EXAMPLE_FILE, run_name="__main__")
    output, error = capsys.readouterr()
    assert not error
    assert USAGE in output
    assert command in output
    assert all(option_command in output for option_command in OPTIONS_COMMAND)
    assert sys_exit.type == SystemExit
    assert sys_exit.value.code == 0


# @pytest.mark.parametrize('text_input', TEXT_OPTION_TEST_DATA)
# @pytest.mark.parametrize('command', COMMANDS)
# @patch('scripts.example.main.COMMANDS')
# def test_main_commands_with_option_text(
#     commands_mock, command, text_input, capsys
# ):
#     """Test main commands with option text."""
#     sys_mock = ['file_name', command, '-t', text_input]
#     with patch.object(sys, 'argv', sys_mock):
#         main()
#     output, error = capsys.readouterr()
#     assert not output
#     assert not error
#     commands_mock.get(command).assert_called_once_with(
#         optional=False,
#         command=command,
#         text=text_input,
#         number=None,
#         arguments=[],
#     )
#     commands_mock.reset_mock()


# @pytest.mark.parametrize('number_input', NUMBER_OPTION_TEST_DATA)
# @pytest.mark.parametrize('command', COMMANDS)
# @patch('scripts.example.main.COMMANDS')
# def test_main_commands_with_option_number(
#     commands_mock, command, number_input, capsys
# ):
#     """Test main commands with option number."""
#     sys_mock = ['file_name', command, '-n', number_input]
#     with patch.object(sys, 'argv', sys_mock):
#         main()
#     output, error = capsys.readouterr()
#     assert not output
#     assert not error
#     commands_mock.get(command).assert_called_once_with(
#         optional=False,
#         command=command,
#         text=None,
#         number=int(number_input),
#         arguments=[],
#     )
#     commands_mock.reset_mock()


# @pytest.mark.parametrize('args', ARGUMENTS_OPTION_TEST_DATA)
# @pytest.mark.parametrize('command', COMMANDS)
# @patch('scripts.example.main.COMMANDS')
# def test_main_commands_with_option_arguments(
#     commands_mock, command, args, capsys
# ):
#     """Test main commands with option arguments."""
#     sys_mock = ['file_name', command, '-t', 'text_input', *args]
#     with patch.object(sys, 'argv', sys_mock):
#         main()
#     output, error = capsys.readouterr()
#     assert not output
#     assert not error
#     commands_mock.get(command).assert_called_once_with(
#         optional=False,
#         command=command,
#         text='text_input',
#         number=None,
#         arguments=args,
#     )
#     commands_mock.reset_mock()


@pytest.mark.parametrize("number_input", INVALID_NUMBER_OPTION_TEST_DATA)
@pytest.mark.parametrize("command", COMMANDS)
def test_main_commands_with_invalid_option_number(
    command: str, number_input: str, capsys: pytest.CaptureFixture[str]
) -> None:
    """Test main commands with invalid option number."""
    sys_mock = ["file_name", command, "-n", number_input]
    with patch.object(sys, "argv", sys_mock):
        with pytest.raises(SystemExit) as sys_exit:
            run_path(EXAMPLE_FILE, run_name="__main__")
    output, error = capsys.readouterr()
    assert not output
    assert INVALID_INT_VALUE in error
    assert sys_exit.type == SystemExit
    assert sys_exit.value.code == 2


@pytest.mark.parametrize("args", INVALID_ARGUMENTS_OPTION_TEST_DATA)
@pytest.mark.parametrize("command", COMMANDS)
def test_main_commands_with_invalid_option_arguments(
    command: str, args: List[str], capsys: pytest.CaptureFixture[str]
) -> None:
    """Test main commands with invalid option arguments."""
    sys_mock = ["file_name", command, "-t", "text_input", *args]
    with patch.object(sys, "argv", sys_mock):
        with pytest.raises(SystemExit) as sys_exit:
            run_path(EXAMPLE_FILE, run_name="__main__")
    output, error = capsys.readouterr()
    assert not output
    assert UNRECOGNIZED_ARGUMENTS in error
    assert sys_exit.type == SystemExit
    assert sys_exit.value.code == 2
