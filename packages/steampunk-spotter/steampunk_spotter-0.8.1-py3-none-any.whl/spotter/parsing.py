import sys
import uuid
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Generator

import yaml


class SafeLineLoader(yaml.loader.SafeLoader):
    """YAML loader that adds line numbers"""

    def construct_mapping(self, node, deep=False) -> dict:
        """
        Overridden the original construct_mapping method
        :param node: YAML node object
        :param deep: Build objects recursively
        :return: A dict with loaded YAML
        """
        mapping = super().construct_mapping(node, deep=deep)

        meta = {}
        meta["__line__"] = node.start_mark.line + 1
        meta["__start_mark_index__"] = node.start_mark.index
        meta["__end_mark_index__"] = node.end_mark.index
        mapping["__meta__"] = meta

        return mapping


class AnsibleArtifact(Enum):
    """Enum that can distinct between different Ansible artifacts (i.e., types of Ansible files)"""
    TASK = 1
    PLAYBOOK = 2
    ROLE = 3
    COLLECTION = 4


class _PlaybookKeywords(set, Enum):
    """
    Enum that stores significant keywords for playbooks that help us automatically discover Ansible file types
    Keywords were gathered from: https://docs.ansible.com/ansible/latest/reference_appendices/playbooks_keywords.html
    """
    PLAY = {
        "any_errors_fatal", "become", "become_exe", "become_flags", "become_method", "become_user", "check_mode",
        "collections", "connection", "debugger", "diff", "environment", "fact_path", "force_handlers", "gather_facts",
        "gather_subset", "gather_timeout", "handlers", "hosts", "ignore_errors", "ignore_unreachable",
        "max_fail_percentage", "module_defaults", "name", "no_log", "order", "port", "post_tasks", "pre_tasks",
        "remote_user", "roles", "run_once", "serial", "strategy", "tags", "tasks", "throttle", "timeout", "vars",
        "vars_files", "vars_prompt"
    }
    ROLE = {
        "any_errors_fatal", "become", "become_exe", "become_flags", "become_method", "become_user", "check_mode",
        "collections", "connection", "debugger", "delegate_facts", "delegate_to", "diff", "environment",
        "ignore_errors", "ignore_unreachable", "module_defaults", "name", "no_log", "port", "remote_user", "run_once",
        "tags", "throttle", "timeout", "vars", "when"
    }
    BLOCK = {
        "always", "any_errors_fatal", "become", "become_exe", "become_flags", "become_method", "become_user", "block",
        "check_mode", "collections", "connection", "debugger", "delegate_facts", "delegate_to", "diff", "environment",
        "ignore_errors", "ignore_unreachable", "module_defaults", "name", "no_log", "notify", "port", "remote_user",
        "rescue", "run_once", "tags", "throttle", "timeout", "vars", "when"
    }
    TASK = {
        "action", "any_errors_fatal", "args", "async", "become", "become_exe", "become_flags", "become_method",
        "become_user", "changed_when", "check_mode", "collections", "connection", "debugger", "delay", "delegate_facts",
        "delegate_to", "diff", "environment", "failed_when", "ignore_errors", "ignore_unreachable", "local_action",
        "loop", "loop_control", "module_defaults", "name", "no_log", "notify", "poll", "port", "register",
        "remote_user", "retries", "run_once", "tags", "throttle", "timeout", "until", "vars", "when"
    }


def _clean_action_and_local_action(task, parse_values):
    # TODO: Remove this spaghetti when API will be able to parse action plugins
    if parse_values:
        # server handles that case already
        return

    if not isinstance(task, Dict):
        # probably inlined - we do not cover that case without parsde values
        return

    if not ("action" in task or "local_action" in task):
        # nothing to do
        return

    verb = "action" if "action" in task else "local_action"
    dict_with_module = next((d for d in list(task.values()) if isinstance(d, dict) and "module" in d), None)
    if dict_with_module is not None:
        module_name = dict_with_module.pop("module", None)
        action = task.pop(verb, None)
        task[module_name] = action
        if verb == "local_action":
            task["delegate_to"]: None


def _parse_tasks(tasks: list, file_name: str, parse_values: Optional[bool] = False) -> Generator:
    """
    Parse Ansible tasks and prepare them for scanning
    :param tasks: List of Ansible task dicts
    :param file_name: Name of the original file with tasks
    :param parse_values: True if also read values (apart from parameter names) from task parameters, False if not
    :return: Generator with parsed Ansible tasks
    """
    for task in tasks:  # pylint: disable=too-many-nested-blocks
        task_dict = {"task_id": str(uuid.uuid4()), "task_args": {}}
        task_meta = task.pop("__meta__", None)

        _clean_action_and_local_action(task, parse_values)
        if "block" in task:
            yield from _parse_tasks(task["block"], file_name, parse_values)
            continue

        for task_key in task:
            if isinstance(task[task_key], dict):
                if not parse_values:
                    for key in list(task[task_key]):
                        if key != "__meta__":
                            task[task_key][key] = None
            else:
                if not parse_values:
                    task[task_key] = None

        meta = {}
        meta["__file__"] = file_name
        meta["__line__"] = task_meta["__line__"]
        meta["__start_mark_index__"] = task_meta["__start_mark_index__"]
        meta["__end_mark_index__"] = task_meta["__end_mark_index__"]
        task["__meta__"] = meta

        task_dict["task_args"] = task

        yield task_dict


def _parse_play(play: dict, file_name: str, parse_values: Optional[bool] = False) -> dict:
    """
    Parse Ansible play and prepare it for scanning
    :param play: Ansible play dict
    :param file_name: Name of the original file with play
    :param parse_values: True if also read values (apart from parameter names) from play parameters, False if not
    :return: Dict with parsed Ansible play
    """
    play_dict = {"play_id": str(uuid.uuid4()), "play_args": {}}
    play_meta = play.pop("__meta__", None)

    for play_key in play:
        if isinstance(play[play_key], dict):
            if not parse_values:
                for key in list(play[play_key]):
                    if key != "__meta__":
                        play[play_key][key] = None
        else:
            if not parse_values:
                play[play_key] = None

    meta = {}
    meta["__file__"] = file_name
    meta["__line__"] = play_meta["__line__"]
    meta["__start_mark_index__"] = play_meta["__start_mark_index__"]
    meta["__end_mark_index__"] = play_meta["__end_mark_index__"]
    play["__meta__"] = meta

    play_dict["play_args"] = play

    return play_dict


def _parse_playbook(playbook: dict, file_name: str, parse_values: Optional[bool] = False) -> Tuple[list, list]:
    """
    Parse Ansible playbook and prepare it for scanning
    :param playbook: Ansible playbook as dict
    :param file_name: Name of the original file with playbook
    :param parse_values: True if also read values (apart from parameter names) from task parameters, False if not
    :return: Tuple containing list of parsed Ansible tasks and parsed playbook as dict
    """
    parsed_tasks = []
    parsed_plays = []
    for play in playbook:
        play.pop("__line__", None)
        tasks = play.pop("tasks", [])

        parsed_tasks += _parse_tasks(tasks, file_name, parse_values)
        parsed_plays.append(_parse_play(play, file_name, parse_values))

    parsed_playbook = {"playbook_id": str(uuid.uuid4()), "plays": parsed_plays}
    return parsed_tasks, [parsed_playbook]


def _parse_task_file(file: Path, parse_values: Optional[bool] = False) -> Tuple[list, list]:
    """
    Parse Ansible file
    :param file: Ansible task file
    :param parse_values: True if also read values (apart from parameter names) from task parameters, False if not
    :return: Tuple containing list of parsed Ansible tasks and parsed playbook as dict
    """
    with file.open() as stream:
        return list(_parse_tasks(yaml.load(stream, Loader=SafeLineLoader), str(file), parse_values)), []


def _parse_playbook_file(file: Path, parse_values: Optional[bool] = False) -> Tuple[list, list]:
    """
    Parse Ansible playbook file
    :param file: Ansible playbook file
    :param parse_values: True if also read values (apart from parameter names) from task parameters, False if not
    :return: Tuple containing list of parsed Ansible tasks and parsed playbook as dict
    """
    with file.open() as stream:
        return _parse_playbook(yaml.load(stream, Loader=SafeLineLoader), str(file), parse_values)


def _parse_role_dir(directory: Path, parse_values: Optional[bool] = False) -> Tuple[list, list]:
    """
    Parse Ansible role
    :param directory: Role directory
    :param parse_values: True if also read values (apart from parameter names) from task parameters, False if not
    :return: Tuple containing list of parsed Ansible tasks and parsed playbook as dict
    """
    parsed_role_tasks = []
    for file in (list((directory / "tasks").rglob("*")) + list((directory / "handlers").rglob("*"))):
        if file.is_file() and _is_task_file(file):
            parsed_tasks, _ = _parse_task_file(file, parse_values)
            parsed_role_tasks += parsed_tasks
    return parsed_role_tasks, []


def _parse_collection_dir(directory: Path, parse_values: Optional[bool] = False) -> Tuple[list, list]:
    """
    Parse Ansible collection
    :param directory: Collection directory
    :param parse_values: True if also read values (apart from parameter names) from task parameters, False if not
    :return: Tuple containing list of parsed Ansible tasks and parsed playbook as dict
    """
    parsed_collection_tasks = []
    parsed_collection_playbooks = []
    for role in (list((directory / "roles").rglob("*"))):
        if role.is_dir():
            parsed_tasks, _ = _parse_role_dir(role, parse_values)
            parsed_collection_tasks += parsed_tasks
    for playbook in (list((directory / "playbooks").rglob("*"))):
        if playbook.is_file() and _is_playbook(playbook):
            parsed_tasks, parsed_playbooks = _parse_playbook_file(playbook, parse_values)
            parsed_collection_tasks += parsed_tasks
            parsed_collection_playbooks += parsed_playbooks
    for path in (list(directory.glob("*.yml")) + list(directory.glob("*.yaml"))):
        if path.is_file():
            if _is_playbook(path):
                parsed_tasks, parsed_playbooks = _parse_playbook_file(path, parse_values)
                parsed_collection_tasks += parsed_tasks
                parsed_collection_playbooks += parsed_playbooks
            elif _is_task_file(path):
                parsed_tasks, parsed_playbooks = _parse_task_file(path, parse_values)
                parsed_collection_tasks += parsed_tasks
                parsed_collection_playbooks += parsed_playbooks
    return parsed_collection_tasks, parsed_collection_playbooks


def _is_task_file(file: Path) -> bool:
    """
    Check if file is a task file = a YAML file containing one or more tasks in a list, where at least one task uses
    keywords for tasks or blocks
    :param file: Path to file
    :return: True or False
    """
    # use keywords for tasks and blocks
    task_file_keywords = (_PlaybookKeywords.TASK.union(_PlaybookKeywords.BLOCK))

    with file.open() as f:
        try:
            loaded_yaml = yaml.safe_load(f)
            if isinstance(loaded_yaml, list):
                if any(len(task_file_keywords.intersection(e.keys())) > 0 for e in loaded_yaml):
                    return True
        except yaml.YAMLError:
            return False

    return False


def _is_playbook(file: Path) -> bool:
    """
    Check if file is a playbook = a YAML file containing one or more plays in an list
    :param file: Path to file
    :return: True or False
    """
    # use only keywords that are unique for play and do not intersect with other keywords
    playbook_keywords = _PlaybookKeywords.PLAY.difference(
        _PlaybookKeywords.TASK.union(_PlaybookKeywords.BLOCK).union(_PlaybookKeywords.ROLE))

    with file.open() as f:
        try:
            loaded_yaml = yaml.safe_load(f)
            if isinstance(loaded_yaml, list):
                if any(len(playbook_keywords.intersection(e.keys())) > 0 for e in loaded_yaml):
                    return True
        except yaml.YAMLError:
            return False

    return False


def _is_role(directory: Path) -> bool:
    """
    Check if directory is a role = a directory with at least one of eight main standard directories
    :param directory: Path to directory
    :return: True or False
    """
    standard_role_directories = ["tasks", "handlers", "library", "defaults", "vars", "files", "templates", "meta"]

    if any((directory / d).exists() for d in standard_role_directories):
        return True
    return False


def _is_collection(directory: Path) -> bool:
    """
    Check if directory is a collection = a directory with galaxy.yml or roles or playbooks
    :param directory: Path to directory
    :return: True or False
    """
    if (directory / "galaxy.yml").exists() or (directory / "roles").exists() or (directory / "playbooks").exists():
        return True
    return False


def parse_known_ansible_artifact(path: Path, ansible_artifact_type: AnsibleArtifact,
                                 parse_values: Optional[bool] = False) -> Tuple[list, list]:
    """
    Parse Ansible artifact (known by type)
    :param path: Path to Ansible artifact
    :param ansible_artifact_type: Type of Ansible files (task files, playbooks, roles or collections)
    :param parse_values: True if also read values (apart from parameter names) from task parameters, False if not
    :return: Tuple containing list of parsed Ansible tasks and parsed playbook as dict
    """
    if ansible_artifact_type == AnsibleArtifact.TASK:
        if not path.is_file():
            print(f"Task file {path.name} is not a valid file")
            sys.exit(1)
        return _parse_task_file(path, parse_values)
    if ansible_artifact_type == AnsibleArtifact.PLAYBOOK:
        if not path.is_file():
            print(f"Playbook {path.name} is not a valid file")
            sys.exit(1)
        return _parse_playbook_file(path, parse_values)
    if ansible_artifact_type == AnsibleArtifact.ROLE:
        if not path.is_dir():
            print(f"Role {path.name} is not a valid directory")
            sys.exit(1)
        return _parse_role_dir(path, parse_values)
    if ansible_artifact_type == AnsibleArtifact.COLLECTION:
        if not path.is_dir():
            print(f"Collection {path.name} is not a valid directory")
            sys.exit(1)
        return _parse_collection_dir(path, parse_values)

    print(f"Unknown Ansible artifact type {ansible_artifact_type}")
    sys.exit(1)


def parse_unknown_ansible_artifact(path: Path, parse_values: Optional[bool] = False) -> Tuple[list, list]:
    """
    Parse Ansible artifact (unknown by type) by applying automatic Ansible file type detection, where we can discover
    task files, playbooks, roles and collections at any level recursively
    :param path: Path to file or directory
    :param parse_values: True if also read values (apart from parameter names) from task parameters, False if not
    :return: Tuple containing list of parsed Ansible tasks and parsed playbook as dict
    """
    parsed_ansible_artifacts_tasks = []
    parsed_ansible_artifacts_playbooks = []
    yaml_suffixes = (".yml", ".yaml")
    if path.is_file() and path.suffix in yaml_suffixes:
        if _is_playbook(path):
            parsed_tasks, parsed_playbooks = parse_known_ansible_artifact(path, AnsibleArtifact.PLAYBOOK, parse_values)
            parsed_ansible_artifacts_tasks += parsed_tasks
            parsed_ansible_artifacts_playbooks += parsed_playbooks
        elif _is_task_file(path):
            parsed_tasks, parsed_playbooks = parse_known_ansible_artifact(path, AnsibleArtifact.TASK, parse_values)
            parsed_ansible_artifacts_tasks += parsed_tasks
            parsed_ansible_artifacts_playbooks += parsed_playbooks
    if path.is_dir():
        if _is_collection(path):
            parsed_tasks, parsed_playbooks = parse_known_ansible_artifact(path, AnsibleArtifact.COLLECTION,
                                                                          parse_values)
            parsed_ansible_artifacts_tasks += parsed_tasks
            parsed_ansible_artifacts_playbooks += parsed_playbooks
        elif _is_role(path):
            parsed_tasks, parsed_playbooks = parse_known_ansible_artifact(path, AnsibleArtifact.ROLE, parse_values)
            parsed_ansible_artifacts_tasks += parsed_tasks
            parsed_ansible_artifacts_playbooks += parsed_playbooks
        else:
            yaml_paths = [yml for gen in [path.rglob(f"*{suf}") for suf in yaml_suffixes] for yml in gen]
            for yaml_path in yaml_paths:
                parsed_tasks, parsed_playbooks = parse_unknown_ansible_artifact(yaml_path, parse_values)
                parsed_ansible_artifacts_tasks += parsed_tasks
                parsed_ansible_artifacts_playbooks += parsed_playbooks

    return parsed_ansible_artifacts_tasks, parsed_ansible_artifacts_playbooks


def parse_ansible_artifacts(paths: List[Path], ansible_artifact_type: Optional[AnsibleArtifact] = None,
                            parse_values: Optional[bool] = False) -> Tuple[list, list]:
    """
    Parse multiple Ansible artifacts
    :param paths: List of paths to Ansible artifacts
    :param ansible_artifact_type: Type of Ansible artifacts (task files, playbooks, roles or collections) or None
    :param parse_values: True if also read values (apart from parameter names) from task parameters, False if not
    :return: List of parsed Ansible tasks that are prepared for scanning
    """
    parsed_ansible_artifacts_tasks = []
    parsed_ansible_artifacts_playbooks = []
    if isinstance(paths, list):
        for path in paths:
            if not path.exists():
                print(f"Error: Ansible artifact file at {path} provided for scanning does not exist.")
                sys.exit(1)

            if ansible_artifact_type:
                parsed_tasks, parsed_playbooks = parse_known_ansible_artifact(path, ansible_artifact_type, parse_values)
                parsed_ansible_artifacts_tasks += parsed_tasks
                parsed_ansible_artifacts_playbooks += parsed_playbooks
            else:
                parsed_tasks, parsed_playbooks = parse_unknown_ansible_artifact(path, parse_values)
                parsed_ansible_artifacts_tasks += parsed_tasks
                parsed_ansible_artifacts_playbooks += parsed_playbooks

    return parsed_ansible_artifacts_tasks, parsed_ansible_artifacts_playbooks
