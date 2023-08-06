from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path, PurePath
from typing import Optional


class Storage:
    """A storage class for saving data to local storage"""

    DEFAULT_PATH = Path.home() / ".config/steampunk-spotter"

    @classmethod
    def create(cls, path: Optional[str] = None) -> Storage:
        """
        Create Storage object
        :param path: Storage path
        :return: Storage object
        """
        return Storage(Path(path or cls.DEFAULT_PATH))

    def __init__(self, path: Path):
        """
        Construct Storage object
        :param path: Storage path
        """
        try:
            self.path = path.absolute()
            path.mkdir(exist_ok=True, parents=True)
        except OSError as e:
            print(f"Error: could not create directory: {str(e)}")
            sys.exit(1)

    def write(self, content: str, *path: str):
        """
        Write content to storage
        :param content: Content
        :param path: Path inside storage to save the content to
        """
        try:
            *subpath, name = path
            dir_path = self.path / PurePath(*subpath)
            dir_path.mkdir(exist_ok=True, parents=True)
            (dir_path / name).write_text(content)
        except OSError as e:
            print(f"Error: unable to write content to storage: {str(e)}")
            sys.exit(1)

    def write_json(self, data: dict, *path: str):
        """
        Write JSON data to storage
        :param data: JSON data as dict
        :param path: Path inside storage to save the data to
        """
        try:
            self.write(json.dumps(data, indent=2), *path)
        except TypeError as e:
            print(f"Error: unable to serialize the object to JSON: {str(e)}")
            sys.exit(1)

    def read(self, *path: str) -> str:
        """
        Read content from storage
        :param path: Path inside storage to read the content from
        :return: Content as string
        """
        try:
            return (self.path / PurePath(*path)).read_text()
        except OSError as e:
            print(f"Error: unable to read content from storage: {str(e)}")
            sys.exit(1)

    def read_json(self, *path) -> dict:
        """
        Read JSON data from storage
        :param path: Path inside storage to read the data from
        :return: JSON object as dict
        """
        try:
            return json.loads(self.read(*path))
        except json.decoder.JSONDecodeError as e:
            print(f"Error: could not read JSON data from storage: {str(e)}")
            sys.exit(1)

    def exists(self, *path: str) -> bool:
        """
        Check if path inside storage exists
        :param path: Path inside storage to check existence for
        :return: True if exists, else False
        """
        try:
            return (self.path / PurePath(*path)).exists()
        except (OSError, ValueError) as e:
            print(f"Error: could check if file exists: {str(e)}")
            sys.exit(1)

    def remove(self, *path: str):
        """
        Remove file from storage
        :param path: Path inside storage to be removed
        """
        try:
            (self.path / PurePath(*path)).unlink(missing_ok=True)
        except OSError as e:
            print(f"Error: could not remove file from storage: {str(e)}")
            sys.exit(1)

    def remove_all(self):
        """
        Remove all files from storage (the storage dir will still exist after the content gets deleted)
        """
        try:
            shutil.rmtree(self.path)
            Path(self.path).mkdir(exist_ok=True)
        except OSError as e:
            print(f"Error: could not remove all files from storage: {str(e)}")
            sys.exit(1)
