# This file is part of QLKNN-develop.
# You should have received QLKNN-develop LICENSE file with this project.
import runpy

import pexpect
from pexpect import spawn as Spawn
import pytest
from IPython import embed  # pylint: disable=unused-import # noqa: F401
import pandas as pd


def test_help_message(running_command):
    running_command.shell_cmd = "quickslicer --help"
    running_command.spawn()
    assert running_command.process.expect("usage: quickslicer") == 0


def test_slice_quick_summary(tmpdir, running_command, qlk_h5_gen5_4D_dataset):
    """Test if we can produce slices from a pure dataset (no networks)"""
    store = qlk_h5_gen5_4D_dataset.store
    assert isinstance(store, pd.HDFStore)
    assert isinstance(store.filename, str)
    store_path = store.filename

    cmd = f"quickslicer {store_path} " "--slice-target=efiITG_GB --mode=quick --summary-to-disk"
    meta = tmpdir.join("slicestat_metadata.csv")
    res = tmpdir.join("slicestat_results.csv")
    running_command.shell_cmd = cmd
    with tmpdir.as_cwd():
        running_command.spawn()

        # Block until command finishes
        running_command.block_wait_finish()

        # Check output
        assert meta.exists()
        assert res.exists()
        # Meta used to be a pandas Series, check if we can read it
        meta_se = pd.read_csv(meta, index_col=[0])
        # TODO: Try to read res
        pd.read_csv(res)


def test_slice_quick_nn_summary(
    request,
    running_command,
    tmpdir,
    qlk_h5_gen5_4D_dataset,
    nn_efi_path,
):
    store = qlk_h5_gen5_4D_dataset.store
    store_path = store.filename

    nn_json_path = nn_efi_path / "nn.json"
    assert nn_json_path.exists()
    scriptname = "nn_mega.py"

    nn_script_file = f"""# Dummy file to test quickslicer scripting interface
from qlknn.models.ffnn import QuaLiKizNDNN

nns = {{}}
nn = QuaLiKizNDNN.from_json("{nn_json_path}")
nn.label = "pretty_label"
nns[nn.label] = nn
slicedim = "Ati"
style = "mono"
"""
    run_args = [
        "quickslicer",
        f"{store_path}",
        f"{scriptname}",
        "--mode=quick",
        "--summary-to-disk",
    ]
    with tmpdir.as_cwd():
        mega_script_path = tmpdir.join(scriptname)
        with mega_script_path.open("w") as f_:
            f_.write(nn_script_file)

        # Test if generated script runs, needed for quickslicing
        toplevel_namespace = runpy.run_path(str(mega_script_path))
        assert "nns" in toplevel_namespace
        assert "slicedim" in toplevel_namespace
        assert "style" in toplevel_namespace
        running_command.shell_cmd = " ".join(run_args)
        child: Spawn = running_command.spawn()

        # Wait for slicing to start
        index = child.expect(["Starting \d+ slices"])
        assert index == 0

        # Wait for child to finish
        #running_command.block_wait_finish()
