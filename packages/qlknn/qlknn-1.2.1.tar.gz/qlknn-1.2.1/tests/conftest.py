import os
import json
from pathlib import Path, PosixPath
from typing import Optional, List
from pexpect import spawn as Spawn
import pexpect
import subprocess as sp
import time
import contextlib
import sys
from datetime import datetime
import signal


import pytest
from _pytest.mark.structures import Mark, MarkDecorator
import numpy as np
import pandas as pd
from IPython import embed  # pylint: disable=unused-import # noqa: F401

from qlknn.models.ffnn import QuaLiKizNDNN

this_file = Path(__file__).resolve()


##########################
# Pytest global settings #
##########################
def pytest_addoption(parser):
    parser.addoption("--timeout", default=40, help="timeout for shell commands")


def pytest_runtest_setup(item):
    for marker in item.iter_markers(name="timeout"):
        print(marker)
        sys.stdout.flush()


# Hook to modify collected test "items"
# Can use e.g. pytest_collection_modifyitems(session, config, items)
def pytest_collection_modifyitems(config, items):
    for item in items:
        if item.get_closest_marker("cli_timeout") is None:
            # If unmarked by cli_timeout, set it
            timeout_val = float(config.getoption("timeout"))
            markdec: MarkDecorator = pytest.mark.cli_timeout(timeout_val)
            item.add_marker(markdec)

        if item.get_closest_marker("cli_command") is None:
            # If unmarked by cli_command, set it
            timeout_val = float(config.getoption("timeout"))
            default_cmd = (
                "echo 'set command with running_command.shell_cmd = `something`'; exit 1"
            )
            markdec: MarkDecorator = pytest.mark.cli_command(default_cmd)
            item.add_marker(markdec)


##################################
# Common useful pytest functions #
##################################
class PytestError(Exception):
    """Base class for all Pytest exceptions."""

    pass


class RunningCommandError(PytestError):
    """Exception raised for errors in the input.

    Attrs:
        expression: input expression in which the error occurred
        message: explanation of the error
    """

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


def postmortem_child(child: Spawn) -> List[str]:
    """Forcably terminate the child and do post-mortem analysis

    Arrange and act is _before_ this fixture
    We only assert and clean up. The child might still be running
    and maybe needs to be killed if timeout is reached.
    """
    assert isinstance(child, Spawn)
    # Wait for child to exit normally
    loglist = []
    if child.eof():
        print("EOF exception detected in this childs' history")
    else:
        print("EOF exception not detected in this childs' history")
        if child.isalive():
            strsignal = signal.strsignal(child.signalstatus) if child.signalstatus else None
            print(
                f"Child is still alive, but signalstatus={strsignal} and exitstatus={child.status}, wait for timeout"
            )
            print(f"Child timed out within expected timeout, closing connection")
            child.close(force=False)
        else:
            print("Child is dead, flush buffer and do post-mortem")
            child.flush()
    #    # This returns True if the EOF exception was ever raised.
    # print(f"EOF not reached within specified timeout of {child.timeout}s"
    #      ", starting forceful termination of child."
    #      )

    # We expect the command to finish (EOF) before timeout, so force close
    # if child.terminate(force=True):
    #    loglist.append("Child succesfully terminated.")
    # else:
    #    loglist.append("Could not terminate child, force closing connection.")
    #    child.close()

    # If the child exited normally then exitstatus will store the exit return
    # code and signalstatus will be None.
    test_passed = True
    if isinstance(child.exitstatus, int) and child.signalstatus is None:
        print("Child terminated correctly")
    else:
        test_passed = False
        # pytest.fail("Child did not terminate correctly")
        if os.WIFEXITED(child.status):
            print("Child exited via exit() system call")
        elif os.WIFSIGNALED(child.status):
            print("Child was terminated by a signal")
        print("\npexpect loglist information:")
        print(child)

    # Build a Karel-approved path with Pathlib
    logname = spawn_logpath(child)
    logfile = Path(logname).resolve()
    assert logfile.is_relative_to(
        Path.cwd()
    ), f"logfile location {logfile} is not relative to current working directory!"
    assert isinstance(logfile, PosixPath)

    # Append log to spawn logfile
    with logfile.open(mode="a") as f_:
        f_.writelines([f"{str(el)}\n" for el in loglist])

    raise RunningCommandError(
        not test_passed,
        f"Error in exit, exit status = '{child.exitstatus}' and"
        f" signal status = '{child.signalstatus}', should be an"
        " integer and None instead. Check logs",
    )
    return test_passed


class RunningCommand:
    """Run a command in a shell interperter using command_string operant mode

    e.g. bash -c or sh -c
    """

    shell = "sh"

    def __init__(self, shell_cmd: str, timeout: Optional[float] = 60) -> Spawn:
        """

        Args:
            shell_cmd
            timeout

        Returns:
            stuff

        """
        self.shell_cmd = shell_cmd
        self.timeout = timeout
        self.process = None

    def spawn(self):
        assert isinstance(self.shell, str)
        assert isinstance(self.shell_cmd, str)
        print(f"Spawning command '{self.shell_cmd}' in '{self.shell}' shell at {datetime.now()}")
        print(f"Will time out in {self.timeout}s")
        child: Spawn = pexpect.spawn(
            self.shell, ["-c", self.shell_cmd], encoding="utf-8", timeout=self.timeout
        )
        assert isinstance(child, Spawn)
        child.logfile = spawn_logpath(child).open("x")  # Log to file
        print(f"Spawned {child!r}")
        assert len(self.shell_cmd) != 0
        self.process = child
        return self.process

    def clean_kill(self):
        postmortem_child(self.process)

    def block_wait_finish(self):
        self.process.expect(pexpect.EOF)


@pytest.fixture
def running_command(request, cache, pytestconfig, record_property):
    timeout = float(request.node.get_closest_marker("cli_timeout").args[0])
    command = str(request.node.get_closest_marker("cli_command").args[0])
    child = RunningCommand(command, timeout=timeout)
    yield child
    # Always exit, no matter the errors
    try:
        child.clean_kill()
    except:
        print("Problem in closing process. Continuing anyway.")


def spawn_logpath(spawn: Spawn) -> PosixPath:
    """Generate path to log for spawn"""
    command = spawn.args[2].split()[0].decode("UTF-8")
    logpath = Path(f"{command}-{spawn.pid}.log")
    assert not logpath.is_absolute(), f"Logpath '{logpath}' is not a relative path!"
    return logpath


@pytest.fixture
def create_child_in_shell(request, running_child):
    """Create a child process that runs in a sub pseudo TTY"""

    def command_to_run(cmd: str) -> Spawn:
        """Runs a command given by a string. Not blocking."""
        # A child process that will live until it is killed/finished
        assert isinstance(cmd, str)
        return running_child()

    return command_to_run


################################
# Old quite specific functions #
################################
@pytest.fixture(scope="session")
def default_settings(request):
    test_root = request.node.fspath
    settings_json = test_root.join("qlknn/training/default_settings.json")
    with open(str(settings_json), "r") as f_:
        settings = json.load(f_)
    settings.update(
        {
            "dataset_path": str(
                test_root.join(
                    "testdata/gen3_test_files/unstable_training_gen3_4D_nions0_flat_filter8.h5.1"
                )
            ),
            "train_dims": ["efiITG_GB"],
            "max_epoch": 3,
        }
    )
    return settings


@pytest.fixture
def datadir():
    datadir = (this_file / "../../testdata").resolve()
    return datadir


class Dataset:
    pass


@pytest.fixture
def store_path(qlk_h5_gen5_4D_dataset):
    store = qlk_h5_gen5_4D_dataset.store
    return Path(store.filename)

@pytest.fixture
def qlk_h5_gen5_4D_dataset(datadir):
    gen = 5
    dim = 4
    iden = "nions0_flat"
    filter_num = 10
    suffix = ".h5.1"
    basename = f"gen{gen}_{dim}D_{iden}_filter{filter_num}"
    store_name = f"{basename}{suffix}"
    dirname = f"gen{gen}_test_files"
    store_path = (datadir / dirname / store_name).resolve()
    assert store_path.is_file()
    ds = Dataset()
    ds.store = pd.HDFStore(store_path, "r")
    ds.input = ds.store["/input"]
    ds.data = ds.store["/flattened"]
    ds.const = ds.store["/constants"]

    yield ds

    ds.store.close()


@pytest.fixture
def qlk_h5_gen2_4D_dataset(datadir):
    dim = 4
    store_name = "".join([str(dim), "D_nions0_flat"])
    store_path = (datadir / "gen2_test_files" / (store_name + ".h5")).resolve()
    assert store_path.is_file()
    ds = Dataset()
    ds.store = pd.HDFStore(store_path, "r")
    ds.input = ds.store["/megarun1/input"]
    ds.data = ds.store["/megarun1/flattened"]
    ds.const = ds.store["/megarun1/constants"]

    yield ds

    ds.store.close()


@pytest.fixture
def inp_7D_df():
    inp = pd.DataFrame()
    scann = 100
    inp["Ati"] = np.array(np.linspace(2, 13, scann))
    inp["Ate"] = 9
    inp["An"] = 3
    inp["q"] = 2
    inp["smag"] = 1
    inp["x"] = 0.45
    inp["Ti_Te"] = 1.2
    return inp


@pytest.fixture
def inp_gen2_7D_df(inp_7D_df):
    return inp_7D_df.rename(columns={"q": "qx"})


#################################
# FFNN related fixtures and tools
#################################
def ffnn(path):
    json_file = path / "nn.json"
    with open(json_file) as file_:
        dict_ = json.load(file_)
    nn = QuaLiKizNDNN(dict_, layer_mode="classic")
    return nn


@pytest.fixture
def nn_efi_path(datadir):
    return datadir / "committee_nets/Cmte_efiITG_GB/NN_0"


@pytest.fixture
def nn_efi(nn_gen2_efi_path):
    return ffnn(nn_gen2_efi_path)


@pytest.fixture
def nn_gen2_efi_path(datadir):
    return datadir / "gen2_test_files/network_1393"


@pytest.fixture
def nn_gen2_efi(nn_gen2_efi_path):
    return ffnn(nn_gen2_efi_path)


@pytest.fixture
def nn_gen2_efi_div_efe_path(datadir):
    return datadir / "gen2_test_files/network_1393"


@pytest.fixture
def nn_gen2_efi_div_efe(nn_gen2_efi_div_efe_path):
    return ffnn(nn_gen2_efi_div_efe_path)


@pytest.fixture
def nn_efi_div_efe(datadir):
    path = datadir / "gen2_test_files/network_1440"
    return ffnn(path)


######################################
# Committee related fixtures and tools
######################################


def grab_jsons(parent_dir):
    nns = {}
    for subdir in parent_dir.iterdir():
        nn_json = subdir / "nn.json"
        assert nn_json.is_file()
        nns[subdir.name] = nn_json
    return nns


@pytest.fixture
def efiITG_paths(datadir):
    path = datadir / "committee_nets/Cmte_efiITG_GB"
    return grab_jsons(path)


def grab_nets(json_paths):
    nns = []
    for path in json_paths.values():
        nn = QuaLiKizNDNN.from_json(path)
        nns.append(nn)
    return nns


@pytest.fixture
def efiITG_committee_nets(efiITG_paths):
    return grab_nets(efiITG_paths)


@pytest.fixture
def efeTEM_paths(datadir):
    path = datadir / "committee_nets/Cmte_efeTEM_GB"
    return grab_jsons(path)


@pytest.fixture
def efeTEM_committee_nets(efeTEM_paths):
    return grab_nets(efeTEM_paths)
