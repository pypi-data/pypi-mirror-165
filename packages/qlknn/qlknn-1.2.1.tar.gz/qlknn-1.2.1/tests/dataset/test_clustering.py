# pylint: disable=no-self-use,missing-function-docstring,missing-class-docstring,missing-module-docstring # noqa
# This file is part of QLKNN-develop.
# You should have received QLKNN-develop LICENSE file with this project.
import json
from pathlib import Path

import pytest  # pylint: disable=unused-import # noqa: F401
from IPython import embed  # pylint: disable=unused-import # noqa: F401

from qlknn.dataset.clustering import *  # pylint: disable=wildcard-import, unused-wildcard-import # noqa: F403, E50


@pytest.fixture
def cluster_datadir(datadir):
    return datadir / "clustering/"


@pytest.fixture
def settings_base_path(cluster_datadir):
    assert cluster_datadir.is_dir()
    return cluster_datadir / "settings_DBMSND.json"


@pytest.fixture
def settings(settings_base_path):
    assert settings_base_path.is_file()
    settings_base = json.load(settings_base_path.open())
    return settings_base


def test_run_clustering(tmpdir, settings, store_path):
    # Modify the settings file with path to testdata
    settings["dataset_path"] = str(store_path)
    settings_path = tmpdir / "testSettings.json"
    with tmpdir.as_cwd():
        # Dump modified settings file to tmpdir
        json.dump(settings, settings_path.open("w"))
        run_clustering(settings_path, verbose=0, fdebug=False)


def test_run_wrapper(running_command, tmpdir, settings, store_path):
    # Modify the settings file with path to testdata
    settings["dataset_path"] = str(store_path)
    settings_path = tmpdir / "testSettings.json"
    cmd = f"clustering --settings {settings_path}"
    with tmpdir.as_cwd():
        # Dump modified settings file to tmpdir
        json.dump(settings, settings_path.open("w"))

        running_command.shell_cmd = cmd
        running_command.spawn()
        running_command.block_wait_finish()
