import pytest
import subprocess
from script_name.utils import (
    get_output, get_returncode, parse_arguments, run_command
)
from unittest.mock import patch


def test_parse_arguments():
    TEST_DATA = [
        {'input': ['the', 'dark', 'knight'], 'output': 'the dark knight'},
        {'input': ['-r', 'command', '-v', '1'], 'output': '-r command -v 1'},
        {'input': 'grep -Inr "batman" .', 'output': 'grep -Inr "batman" .'},
    ]
    for scenario in TEST_DATA:
        output = parse_arguments(scenario['input'])
        assert output == scenario['output']


@patch('subprocess.run')
def test_get_returncode(mock_subprocess):
    TEST_DATA = [
        {'input': ['joker', '--help'], 'mock': 0, 'output': True},
        {'input': 'batman --version', 'mock': 127, 'output': False},
    ]
    for scenario in TEST_DATA:
        mock_subprocess.return_value.returncode = scenario['mock']
        output = get_returncode(scenario['input'])
        assert output == scenario['output']


@patch('subprocess.run')
def test_get_output(mock_subprocess):
    TEST_DATA = [
        {
            'input': ['joker', '--help'],
            'mock': 'Why\nso\nserious\n?',
            'output': ['Why', 'so', 'serious', '?']
        },
        {
            'input': 'batman --version',
            'mock': '',
            'output': None
        },
    ]
    for scenario in TEST_DATA:
        mock_subprocess.return_value.stdout = scenario['mock']
        output = get_output(scenario['input'])
        assert output == scenario['output']


@patch('subprocess.run')
def test_run_command_success(mock_subprocess):
    TEST_DATA = [
        {
            'input': ['joker', '--help'],
            'output': 'Why\nso\nserious\n?\n',
        },
        {
            'input': 'batman --version',
            'output': 'Batman 1.2.3\n'
        },
    ]
    for scenario in TEST_DATA:
        mock_subprocess.return_value = scenario['output']
        output = run_command(scenario['input'])
        assert output == scenario['output']


@patch('subprocess.run')
def test_run_command_error(mock_subprocess, capsys):
    TEST_DATA = [
        {'input': ['riddler', '--help'], 'return_code': 127},
        {'input': 'batman --version', 'return_code': 1},
    ]
    for scenario in TEST_DATA:
        mock_subprocess.side_effect = subprocess.CalledProcessError(
            returncode=scenario['return_code'],
            cmd=scenario['input'],
        )
        formatted = (
            f"ERROR: Command '{scenario['input']}' returned non-zero exit "
            f"status {scenario['return_code']}.\n"
        )
        with pytest.raises(SystemExit) as sys_exit:
            run_command(scenario['input'])
        sys_output, sys_error = capsys.readouterr()
        assert not sys_error
        assert sys_output == formatted
        assert sys_exit.type == SystemExit
        assert sys_exit.value.code == scenario['return_code']
