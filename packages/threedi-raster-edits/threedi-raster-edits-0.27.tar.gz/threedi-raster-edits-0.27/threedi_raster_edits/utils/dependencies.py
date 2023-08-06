# -*- coding: utf-8 -*-
"""
Created on Tue May 31 10:50:44 2022

@author: chris.kerklaan
"""
import pathlib
import importlib
import logging
from collections import namedtuple


# Globals
logger = logging.getLogger(__name__)
Module = namedtuple(
    "package", "name installed_version installed minimum_required_version"
)
OUR_DIR = pathlib.Path(__file__)
REQUIREMENTS_PATH = str(OUR_DIR.parents[1] / "requirements.txt")


class Dependencies:
    def __init__(self, requirements_path=REQUIREMENTS_PATH):
        ogr_module = Module(
            "osgeo.ogr", _check_version("osgeo.ogr"), _check_installed("osgeo.ogr"), 3.4
        )
        self.modules = [ogr_module]
        self._load_requirement_modules(requirements_path)

    def _load_requirement_modules(self, path):
        with open(path, "r") as f:
            lines = f.readlines()

            for line in lines:
                data = line.replace("\n", "").split("==")
                if len(data) > 1:
                    version = version_to_tuple(data[1])
                else:
                    version = None
                module = Module(
                    data[0],
                    _check_version(data[0]),
                    _check_installed(data[0]),
                    version,
                )
                self.modules.append(module)
                setattr(self, module.name.replace("-", "_"), module)

        def __repr__(self):
            return self.modules

        def __str__(self):
            return str(self.modules)

    def missing(self):
        for module in self.modules:
            if module.name == "-e .[test]":
                continue

            if not module.installed:
                logger.debug(f"Dependency {module} not available!")
                continue

            if module.installed_version and module.minimum_required_version:
                if not module.installed_version >= module.minimum_required_version:
                    logger.debug(f"Dependency {module} version is incorrect!")
                    continue

            # logger.info(f"Dependency {module} correctly installed!")


def _check_installed(module_name):
    try:
        importlib.import_module(module_name)
    except Exception:
        return False
    else:
        return True


def _check_version(module_name):
    try:
        version = importlib.metadata.version(module_name)
        version = version_to_tuple(version)
    except Exception:
        return None
    else:
        return version


def version_to_tuple(version: str):
    return tuple([int(i) for i in version.split(".")])


# Adding a global
DEPENDENCIES = Dependencies()
