from __future__ import annotations

import json
import os
import platform
import subprocess
import sys
from pathlib import Path
from typing import Optional

import pkg_resources
import yaml


class Environment:
    """User environment/workspace state discovery (retrieves system info and versions of installed packages)"""

    def __init__(self):
        """Construct Environment object"""
        self.python_version = None
        self.ansible_python_version = None
        self.ansible_core_python_version = None
        self.ansible_base_python_version = None
        self.ansible_version = None
        self.installed_ansible_collections = None
        self.ansible_config = None
        self.galaxy_yml = None
        self.collection_requirements = None
        self.cli_scan_args = None

    def _get_python_version(self) -> str:
        """
        Get python version
        :return: Version string
        """
        return platform.python_version()

    def _get_ansible_python_version(self) -> Optional[str]:
        """
        Get ansible python package version
        :return: Version string
        """
        try:
            return pkg_resources.get_distribution("ansible").version
        except pkg_resources.DistributionNotFound:
            return None

    def _get_ansible_core_python_version(self) -> Optional[str]:
        """
        Get ansible-core python package version
        :return: Version string
        """
        try:
            return pkg_resources.get_distribution("ansible-core").version
        except pkg_resources.DistributionNotFound:
            return None

    def _get_ansible_base_python_version(self) -> Optional[str]:
        """
        Get ansible-base python package version
        :return: Version string
        """
        try:
            return pkg_resources.get_distribution("ansible-base").version
        except pkg_resources.DistributionNotFound:
            return None

    def _get_ansible_version(self) -> Optional[str]:
        """
        Get Ansible version
        :return: Version string
        """
        try:
            output = subprocess.check_output(["ansible", "--version"], stderr=subprocess.DEVNULL).decode("utf-8")
            return output.splitlines()[0].lower().replace("ansible", "").strip()
        except (subprocess.CalledProcessError, FileNotFoundError):
            return None

    def _get_installed_ansible_collections(self) -> list:
        """
        Get installed Ansible collections
        :return: Dict with Ansible collection names and their versions
        """
        installed_collections = []
        try:
            output = subprocess.check_output(["ansible-galaxy", "collection", "list", "--format", "json"],
                                             stderr=subprocess.DEVNULL).decode(
                "utf-8")
            for location, value in json.loads(output).items():
                for fqcn, version in value.items():
                    installed_collections.append({"fqcn": fqcn,
                                                  "version": version.get("version", None),
                                                  "location": location})
            return installed_collections
        except (subprocess.CalledProcessError, FileNotFoundError):
            return installed_collections

    def _get_ansible_config(self) -> dict:
        """
        Get Ansible config current settings
        :return: Dict with Ansible config current settings specified as key-value pairs
        """
        ansible_config = {}
        try:
            output = subprocess.check_output(["ansible-config", "dump", "--only-changed"],
                                             stderr=subprocess.DEVNULL).decode("utf-8")
            for line in output.splitlines():
                if line:
                    key, value = line.split("=", maxsplit=1)
                    ansible_config[key.strip()] = value.strip()
            return ansible_config
        except (subprocess.CalledProcessError, FileNotFoundError):
            return ansible_config

    def _get_galaxy_yml(self) -> dict:
        """
        Get galaxy.yml contents
        :return: Contents of galaxy.yml file
        """
        try:
            with open("galaxy.yml", "r", encoding="utf-8") as stream:
                try:
                    return yaml.safe_load(stream)
                except yaml.YAMLError:
                    return {}
        except OSError:
            return {}

    def _get_collection_requirements(self) -> dict:
        """
        Get Ansible collection requirements from requirements.yml or collections/requirements.yml
        :return: Contents of requirements.yml or collections/requirements.yml file
        """
        try:
            requirements_yml_path = "requirements.yml"
            if not os.path.exists(requirements_yml_path):
                requirements_yml_path = "collections/requirements.yml"

            with open(requirements_yml_path, "r", encoding="utf-8") as stream:
                try:
                    return yaml.safe_load(stream)
                except yaml.YAMLError:
                    return {}
        except OSError:
            return {}

    def to_dict(self) -> dict:
        """
        Return workspace variables as dict
        :return: Dict with all variables from workspace
        """
        return {
            "ansible_version": {
                "ansible": self.ansible_version,
                "ansible_core": self.ansible_core_python_version,
                "ansible_base": self.ansible_base_python_version
            },
            "installed_collections": self.installed_ansible_collections,
            "python_version": self.python_version,
            "ansible_config": self.ansible_config,
            "galaxy_yml": self.galaxy_yml,
            "collection_requirements": self.collection_requirements,
            "cli_scan_args": self.cli_scan_args
        }

    @classmethod
    def from_dict(cls, environment_dict: dict) -> Environment:
        """
        Create Environment object from dict
        :param environment_dict: Dict to create Environment object from
        :return: Environment object
        """
        environment = cls()

        ansible_version = environment_dict.get("ansible_version", None)
        environment.ansible_version = ansible_version.get("ansible", None) if ansible_version else None
        environment.ansible_core_python_version = ansible_version.get("ansible_core", None) if ansible_version else None
        environment.ansible_base_python_version = ansible_version.get("ansible_base", None) if ansible_version else None
        environment.ansible_python_version = None
        environment.python_version = environment_dict.get("python_version", None)
        environment.installed_ansible_collections = environment_dict.get("installed_collections", None)
        environment.ansible_config = environment_dict.get("ansible_config", None)
        environment.galaxy_yml = environment_dict.get("galaxy_yml", None)
        environment.collection_requirements = environment_dict.get("collection_requirements", None)
        environment.cli_scan_args = environment_dict.get("cli_scan_args", None)
        return environment

    def set_from_local_discovery(self):
        """
        Set workspace variables discovered locally on user's system
        :return: Dict with all variables from workspace
        """
        self.python_version = self._get_python_version()
        self.ansible_python_version = self._get_ansible_python_version()
        self.ansible_core_python_version = self._get_ansible_core_python_version()
        self.ansible_base_python_version = self._get_ansible_base_python_version()
        self.ansible_version = self._get_ansible_version()
        self.installed_ansible_collections = self._get_installed_ansible_collections()
        self.ansible_config = self._get_ansible_config()
        self.galaxy_yml = self._get_galaxy_yml()
        self.collection_requirements = self._get_collection_requirements()

    def set_from_config_file(self, config_path: Path):
        """
        Set workspace variables from environment
        :param config_path: Configuration file path (must exist)
        """
        try:
            if not config_path.exists():
                print(f"Error: config file at {config_path} does not exist.")
                sys.exit(1)

            with config_path.open("r") as config_file:
                config = yaml.safe_load(config_file)
                self.ansible_core_python_version = config.get("ansible_version", self.ansible_core_python_version)
        except yaml.YAMLError as e:
            print(f"Invalid configuration file: {e}")
            sys.exit(1)

    def set_from_extra_vars(self, extra_vars: dict):
        """
        Set workspace variables from extra vars
        :param extra_vars: Dict of variables
        """
        self.ansible_core_python_version = extra_vars.get("ansible_version", self.ansible_core_python_version)
