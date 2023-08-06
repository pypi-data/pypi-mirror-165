from __future__ import annotations

import argparse
import dataclasses
import json
import os
import re
import sys
from enum import Enum
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional

from colorama import Fore, Style

from spotter.api import ApiClient
from spotter.environment import Environment
from spotter.parsing import parse_ansible_artifacts
from spotter.rewriting import Suggestion, update_files
from spotter.storage import Storage


@dataclasses.dataclass
class CheckResult:
    """A container for parsed check results originating from the backend"""
    level: DisplayLevel
    task_id: str
    original_task: dict
    message: str
    suggestion: Suggestion


class DisplayLevel(Enum):
    """Enum that holds different levels/statuses for check result"""
    HINT = 1
    WARN = 2
    ERROR = 3

    def __str__(self):
        """
        Convert DisplayLevel to lowercase string
        :return: String in lowercase
        """
        return self.name.lower()

    @staticmethod
    def from_string(level: str) -> DisplayLevel:
        """
        Convert string level to DisplayLevel object
        :param level: Check result level
        :return: DisplayLevel object
        """
        try:
            return DisplayLevel[level.upper()]
        except KeyError:
            print(f"Error: nonexistent check status display level: {level}, "
                  f"valid values are: {list(e for e in DisplayLevel)}.")
            sys.exit(1)


def add_parser(subparsers: argparse._SubParsersAction):
    """
    Adds a new parser to subparsers
    :param subparsers: Subparsers action
    """
    parser = subparsers.add_parser(
        "scan", help="Initiate Ansible scan", description="Initiate Ansible scan"
    )
    parser.add_argument(
        "--config", "-c", type=lambda p: Path(p).absolute(), help="Configuration file (as JSON/YAML)"
    )
    parser.add_argument(
        "--option", "-o", type=lambda s: s.strip().split("="), action="append", default=[],
        help="Additional config variable as key=value pair, for example ansible_version=2.13"
    )
    parser.add_argument(
        "--parse-values", "-p", action="store_true", help="Also parse values from Ansible task parameters",
    )
    parser.add_argument(
        "--rewrite", "-r", action="store_true", help="Rewrite files with fixes",
    )
    parser.add_argument(
        "--display-level", "-l", type=DisplayLevel.from_string,
        choices=list(DisplayLevel), default=DisplayLevel.HINT,
        help="Display only check results with specified level or greater "
             "(e.g., -l warn will show all warnings and errors, but suppress hints)"
    )
    import_export_group = parser.add_mutually_exclusive_group()
    import_export_group.add_argument(
        "--import-payload", "-i", type=lambda p: Path(p).absolute(),
        help="Path to the previously exported file to be sent for scanning"
    )
    import_export_group.add_argument(
        "--export-payload", "-e", type=lambda p: Path(p).absolute(),
        help="Output file path to export the locally scanned data without sending anything for scanning at the server"
    )
    parser.add_argument(
        "path", type=lambda p: Path(p).absolute(), nargs="*", help="Path to Ansible artifact or directory",
    )
    parser.set_defaults(func=_parser_callback)


def _parser_callback(args: argparse.Namespace):
    # pylint: disable=too-many-branches,too-many-locals, too-many-statements
    """
    Invoke the Ansible scanner and print/save the scan result (parser callback function)
    :param args: Argparse arguments
    """
    username = args.username or os.environ.get("SPOTTER_USERNAME")
    password = args.password or os.environ.get("SPOTTER_PASSWORD")
    storage = Storage.create(args.storage_path)
    client = ApiClient(ApiClient.ENDPOINT, storage, username, password)

    # create and set environment
    # the order that we read configuration is the following (in each step we overwrite what the previous one has):
    # 1. local discovery (from user's current workspace)
    # 2. config file (JSON/YAML file provided after --config flag)
    # 3. options provided as key=value pairs to the scan command
    environment = Environment()
    environment.set_from_local_discovery()
    if args.config:
        environment.set_from_config_file(args.config)
    if args.option:
        extra_vars = {}
        for key_value in args.option:
            if len(key_value) != 2:
                print(f"Error: '{'='.join(key_value)}' extra option is not specified as key=value.")
                sys.exit(1)
            else:
                extra_vars[key_value[0]] = key_value[1]

        environment.set_from_extra_vars(extra_vars)

    if args.import_payload and args.path:
        print("Error: the --import-payload is mutually exclusive with positional arguments.")
        sys.exit(1)

    if args.export_payload and not args.path or (not args.export_payload and not args.import_payload and not args.path):
        print("Error: no paths provided for scanning.")
        sys.exit(1)

    if args.import_payload:
        environment, input_tasks, input_playbooks = _import_scan_payload_from_json_file(args.import_payload)
    else:
        input_tasks = []
        input_playbooks = []
        if args.path:
            input_tasks, input_playbooks = parse_ansible_artifacts(args.path, parse_values=args.parse_values)

    cli_scan_args = {
        "parse_values": args.parse_values,
        "rewrite": args.rewrite,
        "display_level": str(args.display_level)
    }
    environment.cli_scan_args = cli_scan_args

    if args.export_payload:
        scan_payload = {
            "environment": environment.to_dict(),
            "tasks": input_tasks,
            "playbooks": input_playbooks
        }

        _export_scan_payload_to_json_file(scan_payload, args.export_payload)

        file_name = str(args.export_payload)
        try:
            # trim the part of the directory that is shared with CWD if this is possible
            file_name = str(Path(file_name).relative_to(Path.cwd()))
        except ValueError:
            pass

        print(f"Scan data saved to {file_name}.\nNote: this operation is fully offline. No actual scan was executed.")
    else:
        scan_payload = {"environment": environment.to_dict(),
                        "tasks": _remove_sensitive_data_from_tasks(input_tasks),
                        "playbooks": _remove_sensitive_data_from_playbooks(input_playbooks)
                        }
        response = client.post("/v2/scans/", payload=scan_payload)

        check_results_all = parse_check_results(input_tasks, response.json())
        check_results_filtered = filter_check_results(check_results_all, args.display_level)
        print_check_results(check_results_filtered, args.no_colors)

        if args.rewrite:
            apply_check_result_suggestions(check_results_filtered)

        if len(check_results_filtered) > 0:
            sys.exit(1)


def _import_scan_payload_from_json_file(import_path: Path) -> Tuple[Environment, List[Dict], List[Dict]]:
    """
    Imports scan input from JSON file
    :param import_path: File path to import from (must exist)
    :return: Scan input tuple (environment, tasks, playbooks)
    """
    try:
        if not import_path.exists():
            print(f"Error: import file at {import_path} does not exist.")
            sys.exit(1)

        with import_path.open("r") as import_file:
            scan_payload = json.load(import_file)
            environment_dict = scan_payload.get("environment", None)
            if environment_dict:
                environment = Environment.from_dict(environment_dict)
            else:
                environment = Environment()

            return environment, scan_payload.get("tasks", []), scan_payload.get("playbooks", [])
    except (json.JSONDecodeError, TypeError) as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


def _export_scan_payload_to_json_file(scan_payload: dict, export_path: Path):
    """
    Exports scan input to JSON file
    :param scan_payload: Scan input as dict
    :param export_path: File path to export to (will be overwritten if exists)
    """
    try:
        with export_path.open("w") as export_file:
            json.dump(scan_payload, export_file, indent=2)
    except TypeError as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


def _remove_sensitive_data_from_task(input_task: Any) -> Any:
    """
    Removes sensitive data from input task
    :param input_task: Input Ansible task
    :return: Cleaned input task
    """
    if not input_task:
        return input_task
    if isinstance(input_task, list):
        return [_remove_sensitive_data_from_task(x) for x in input_task if x != "__meta__"]
    if not isinstance(input_task, dict):
        return input_task

    tmp = dict(input_task)
    tmp.pop("__meta__", None)

    for k, v in tmp.items():
        tmp[k] = _remove_sensitive_data_from_task(v)

    return tmp


def _remove_sensitive_data_from_tasks(input_tasks: List[Dict]) -> List[Dict]:
    """
    Removes sensitive data from input tasks
    :param input_tasks: Input Ansible task list
    :return: Cleaned list of input tasks
    """
    return [
        {
            "task_id": t["task_id"],
            "task_args": _remove_sensitive_data_from_task(t["task_args"])
        } for t in input_tasks
    ]


def _remove_sensitive_data_from_playbooks(input_playbooks: List[Dict]) -> List[Dict]:
    """
    Removes sensitive data from input playbooks
    :param input_playbooks: Input Ansible playbooks list
    :return: Cleaned list of input playbooks
    """
    return [
        {
            "playbook_id": t["playbook_id"],
            "plays": [
                {
                    "play_id": x.get("play_id", None),
                    "play_args": _remove_sensitive_data_from_task(x["play_args"])
                }
                for x in t["plays"]
            ]
        } for t in input_playbooks
    ]


def parse_check_results(input_tasks: list, scan_output: dict) -> List[CheckResult]:
    """
    Parse result objects and map tasks with complete information
    :param input_tasks: The scanned tasks with no information removed
    :param scan_output: The backend API response
    :return: A list of check results
    """

    result: List[CheckResult] = []

    for element in scan_output.get("elements", []):
        level = element.get("level", "")
        task_id = element.get("task_id", "")
        message = element.get("message", "")
        suggestion = element.get("suggestion", "")

        # match the result task's ID to the original task (with complete information)
        original_task: Optional[dict] = None
        for task in input_tasks:
            if task.get("task_id", None) == task_id:
                original_task = task
                break

        # guard against incomplete results where we don't match a task
        if original_task is None:
            print("Could not map task ID to its original task.")
            continue

        # guard against missing task args and metadata
        task_args = original_task.get("task_args")
        task_meta = task_args.get("__meta__", None)
        if task_meta:
            suggestion_object: Optional[Suggestion] = None
            if suggestion:
                suggestion_object = Suggestion(original_task, suggestion)
            result.append(
                CheckResult(DisplayLevel.from_string(level), task_id, original_task, message, suggestion_object)
            )

    return result


def filter_check_results(results: List[CheckResult], threshold: DisplayLevel) -> List[CheckResult]:
    """
    Filter a list of results by only keeping tasks over a specified severity level
    :param results: The list of results to filter
    :param threshold: The threshold (inclusive) of what level messages (and above) to keep
    :return: A filtered list of results
    """
    return [cr for cr in results if cr.level.value >= threshold.value]


def print_check_results(results: List[CheckResult], disable_colors: bool = False) -> None:
    """
    Render a list of results into the console (assumes results are pre-filtered)
    :param disable_colors: Disable output colors and styling
    :param results: The results to display
    """
    for result in results:
        task_args = result.original_task.get("task_args")
        task_meta = task_args.get("__meta__", None)
        file_name = task_meta.get("__file__", None)
        task_line = task_meta.get("__line__", None)

        try:
            # trim the part of the directory that is shared with CWD if this is possible
            file_name = str(Path(file_name).relative_to(Path.cwd()))
        except ValueError:
            pass

        result_level = result.level.name.upper()
        result_prefix = f"{file_name}:{task_line}: {result_level}"
        result_message = result.message
        if not disable_colors:
            if result_level == DisplayLevel.ERROR.name:
                result_prefix = Fore.RED + result_prefix + Fore.RESET
                result_message = re.sub(r"'([^']*)'", Style.BRIGHT + Fore.RED + r"\1" + Fore.RESET + Style.NORMAL,
                                        result_message)
            elif result_level == DisplayLevel.WARN.name:
                result_prefix = Fore.YELLOW + result_prefix + Fore.RESET
                result_message = re.sub(r"'([^']*)'", Style.BRIGHT + Fore.YELLOW + r"\1" + Fore.RESET + Style.NORMAL,
                                        result_message)
            else:
                result_message = re.sub(r"'([^']*)'", Style.BRIGHT + r"\1" + Style.NORMAL, result_message)

        output = f"{result_prefix}: {result_message}"
        print(output)

    if len(results) > 0:
        worst_level = max((cr.level for cr in results), key=lambda level: level.value)

        print("------------------------------------------------------------------------")

        overall_status_message = f"Overall status: {worst_level.name.upper()}"
        if not disable_colors:
            overall_status_message = Style.BRIGHT + overall_status_message
        print(overall_status_message)


def apply_check_result_suggestions(results: List[CheckResult]) -> None:
    """
    Automatically apply suggestions
    :param results: A list of results, which may or may not contain suggestions, to apply suggestions from
    """
    all_suggestions = [cr.suggestion for cr in results if cr.suggestion is not None]
    update_files(all_suggestions)
