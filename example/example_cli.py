"""Create configured argparse's CLI example."""

import argparse
from typing import Callable, Dict

from cli import colors, config, utils
from example import __version__
from example.command1 import command1

cli_config = {
    "name": "Script name",
    "description": "Script description.",
    "epilog": "Script epilog.",
    "version": __version__,
}

COMMANDS: Dict[str, Callable[..., None]] = {
    command1.__name__: command1,
}

CLI = config.ConfiguredParser(cli_config)
CLI.parser.add_argument(
    "-o",
    "--optional",
    action="store_true",
    help="Description of the optional flag.",
)

command = CLI.create_command(command1.__name__, "Description of the command1.")
group = command.add_mutually_exclusive_group(required=True)
group.add_argument(
    "-t",
    "--text",
    metavar="str",
    type=str,
    help="Example of argument that receives a string.",
)
group.add_argument(
    "-n",
    "--number",
    metavar="int",
    type=int,
    help="Example of argument that receives a integer.",
)
command.add_argument(
    dest="arguments",
    nargs=argparse.REMAINDER,
    help="Arbitrary arguments for a command.",
)


def main() -> None:
    """Run script on user call."""
    arguments = CLI.get_arguments()
    if arguments.optional:
        colors.print_flashy("Optional flag called.")
        utils.run_command("ls -1a")
    if arguments.command:
        COMMANDS[arguments.command](**dict(arguments._get_kwargs()))
