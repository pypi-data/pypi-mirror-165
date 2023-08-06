import argparse
import inspect
import sys
from pathlib import Path
from typing import Union, Sequence, Optional

import colorama
import pkg_resources

from spotter import commands
from spotter.storage import Storage


class ArgParser(argparse.ArgumentParser):
    """An argument parser that displays help on error"""

    def error(self, message: str):
        """
        Overridden the original error method
        :param message: Error message
        """
        sys.stderr.write(f"error: {message}\n")
        self.print_help()
        sys.exit(1)

    def add_subparsers(self, **kwargs) -> argparse._SubParsersAction:
        """
        Overridden the original add_subparsers method (workaround for http://bugs.python.org/issue9253)
        """
        subparsers = super().add_subparsers()
        subparsers.required = True
        subparsers.dest = "command"
        return subparsers


def create_parser() -> ArgParser:
    """
    Create argument parser for CLI
    :return: Parser as argparse.ArgumentParser object
    """
    parser = ArgParser(description="Steampunk Spotter - a quality scanner for Ansible Playbooks")

    parser.add_argument(
        "--version", "-v", action=PrintCurrentVersionAction, nargs=0,
        help="Display the version of Steampunk Spotter CLI"
    )
    parser.add_argument(
        "--storage-path", "-s", type=lambda p: Path(p).absolute(),
        help=f"Storage folder location (instead of default {Storage.DEFAULT_PATH})"
    )
    parser.add_argument(
        "--username", "-u", type=str, help="Username"
    )
    parser.add_argument(
        "--password", "-p", type=str, help="Password"
    )
    parser.add_argument(
        "--no-colors", action="store_true", help="Disable output colors"
    )

    subparsers = parser.add_subparsers()
    cmds = inspect.getmembers(commands, inspect.ismodule)
    for _, module in sorted(cmds, key=lambda x: x[0]):
        module.add_parser(subparsers)
    return parser


class PrintCurrentVersionAction(argparse.Action):
    """An argument parser action for displaying current Python package version"""

    def __call__(self, parser: argparse.ArgumentParser, namespace: argparse.Namespace,
                 values: Union[str, Sequence, None], option_string: Optional[str] = None):
        """
        Overridden the original __call__ method for argparse.Action
        :param parser: ArgumentParser object
        :param namespace: Namespace object
        :param values: Command-line arguments
        :param option_string: Option string used to invoke this action.
        """
        try:
            print(pkg_resources.get_distribution("steampunk-spotter").version)
            sys.exit(0)
        except pkg_resources.DistributionNotFound as e:
            print(f"Error when retrieving current steampunk-spotter version: {e}")
            sys.exit(1)


def main() -> ArgParser:
    """
    Main CLI method to be called
    """
    colorama.init(autoreset=True)
    parser = create_parser()
    args = parser.parse_args()
    return args.func(args)
