import itertools
import os
import re
from typing import Any, Dict, List, Tuple

OKGREEN = "\033[92m"
OKRED = "\033[0;31m"
ENDC = "\033[0m"


class Suggestion:
    """
    Suggestion for rewriting Ansible task
    """

    def __init__(self, task: Any, suggestion: Dict[str, Any]):
        """
        Instantiate Suggestion object
        :param task: Ansible task content (usually a dict)
        :param suggestion: Suggestion as dict with action to do and data to use for update
        """
        self.args = args = task["task_args"]

        self.file = args["__meta__"]["__file__"]
        self.start_mark = args["__meta__"]["__start_mark_index__"]
        self.end_mark = args["__meta__"]["__end_mark_index__"]
        self.suggestion = suggestion


def _update_content(content: str, suggestion: Suggestion, colorize: bool) -> Tuple[str, int]:
    """
    Update task content
    :param content: Old task content
    :param suggestion: Suggestion object for a specific task
    :param colorize: If True color things that will be changed
    :return: Tuple with updated content and content length difference
    """
    suggestion_dict = suggestion.suggestion
    if suggestion_dict.get("action") != "FIX_FQCN":
        return content, 0

    part = content[suggestion.start_mark:suggestion.end_mark]
    before = suggestion_dict["data"]["before"]
    after = suggestion_dict["data"]["after"]
    regex = rf"([\t ]*)({before})(\s*:\s*)"

    replacement = f"{OKGREEN}{after}{ENDC}" if colorize else after
    match = re.search(regex, part, re.MULTILINE)
    s_index, e_index = match.span(2)
    end_content = content[:suggestion.start_mark + s_index] + replacement + content[suggestion.start_mark + e_index:]
    return end_content, len(replacement) - len(before)


def update_files(suggestions: List[Suggestion]):
    """
    Update files by following suggestions
    :param suggestions: List of suggestions as Suggestion objects
    """
    get_file_func = lambda x: x.file  # pylint: disable=unnecessary-lambda-assignment
    files = [(file, list(tasks)) for file, tasks in itertools.groupby(suggestions, get_file_func)]

    get_inode_func = lambda x: os.stat(x[0]).st_ino  # pylint: disable=unnecessary-lambda-assignment
    inodes = [next(group) for _, group in itertools.groupby(sorted(files, key=get_inode_func), get_inode_func)]

    for file, tasks in inodes:
        tasks_reversed = list(reversed(tasks))
        with open(file, "r", encoding="utf-8") as f:
            content = f.read()

        end_content = content
        try:
            for task in tasks_reversed:
                end_content, _ = _update_content(end_content, task, False)
        except Exception:  # pylint: disable=broad-except
            print(file)

        if end_content != content:
            with open(file, "w", encoding="utf-8") as f:
                f.write(end_content)
