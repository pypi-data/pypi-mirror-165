import runpy
import shutil
import copy
from pathlib import Path

import pytest
from IPython import embed
import pandas as pd

from qlknn.models.ffnn import QuaLiKizNDNN
from qlknn.training.train_NDNN import *


@pytest.fixture
def default_rundir(request, tmpdir):
    test_file = request.fspath
    repo_root = test_file.join("../../../")
    assert repo_root.exists()
    train_script = repo_root.join("qlknn/training/train_NDNN.py")
    assert train_script.exists()
    with tmpdir.as_cwd():
        shutil.copy(str(train_script), str(tmpdir))
    return tmpdir


def pytest_exception_interact(node, call, report):
    excinfo = call.excinfo
    if "script" in node.funcargs:
        excinfo.traceback = excinfo.traceback.cut(path=node.funcargs["script"])
    report.longrepr = node.repr_failure(excinfo)


class TestTrainNDNN:
    def test_default_train(self, request, default_rundir, default_settings):
        settings = copy.deepcopy(default_settings)
        with default_rundir.as_cwd():
            with open("settings.json", "w") as file_:
                json.dump(settings, file_)
            glo = runpy.run_path("train_NDNN.py")
            glo["main"]()

    def test_function_train(self, request, default_rundir, default_settings):
        settings = copy.deepcopy(default_settings)
        with default_rundir.as_cwd():
            train(settings)
            final_nn_file = Path("nn.json")
            assert final_nn_file.exists()
            history_file = Path("history.csv")
            assert history_file.exists()

            assert ["efiITG_GB"] == settings["train_dims"]
            assert 3 == settings["max_epoch"]

            history = pd.read_csv(history_file, index_col=0)
            nn = QuaLiKizNDNN.from_json(final_nn_file)
            # The epochs from history is 1-off from max_epoch
            assert settings["max_epoch"] - 1 == history.epoch.max()

    def test_divnet_live(self, request, default_rundir, default_settings):
        settings = copy.deepcopy(default_settings)
        # Modify dataset to drop efe
        ds_path = Path(settings["dataset_path"])
        store = pd.HDFStore(ds_path)

        ds_new_name = "reduced_set" + "".join(ds_path.suffixes)

        store["/output/efeITG_GB"].to_hdf(default_rundir / ds_new_name, "/output/efeITG_GB")
        store["/output/efiITG_GB"].to_hdf(default_rundir / ds_new_name, "/output/efiITG_GB")
        store["/input"].to_hdf(default_rundir / ds_new_name, "/input")
        store["/constants"].to_hdf(default_rundir / ds_new_name, "/constants")
        store.close()

        settings["dataset_path"] = ds_new_name
        settings["train_dims"] = ["efeITG_GB_div_efiITG_GB"]
        with default_rundir.as_cwd():
            with open("settings.json", "w") as file_:
                json.dump(settings, file_)
            glo = runpy.run_path("train_NDNN.py")
            glo["main"]()
            assert Path("nn.json").is_file()


@pytest.mark.skip("Underlying function does not work")
class TestTrainNDNNEdgeRun:
    def test_function_train(self, request, default_rundir, default_settings):
        settings = copy.deepcopy(default_settings)
        with default_rundir.as_cwd():
            train_edgerun(settings)
            final_nn_file = Path("nn.json")
            assert final_nn_file.exists()
            history_file = Path("history.csv")
            assert history_file.exists()

            assert ["efiITG_GB"] == settings["train_dims"]
            assert 3 == settings["max_epoch"]

            history = pd.read_csv(history_file, index_col=0)
            nn = QuaLiKizNDNN.from_json(final_nn_file)
            # The epochs from history is 1-off from max_epoch
            assert settings["max_epoch"] - 1 == history.epoch.max()
