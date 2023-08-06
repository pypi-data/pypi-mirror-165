import os

import pytest
from IPython import embed

from qlknn.models.kerasmodel import *

test_files_dir = os.path.abspath(os.path.join(__file__, "../../keras_test_files"))
phillip_net_json_model_path = os.path.join(test_files_dir, "philippstyle_CGNN_model.json")
phillip_net_json_weights_path = os.path.join(test_files_dir, "philippstyle_CGNN_weights.json")
standardization_path = os.path.join(test_files_dir, "training_gen3_7D_nions0_flat_filter8.csv")
inp_path = os.path.join(test_files_dir, "philippstyle_CGNN_inp.csv")
outp_path = os.path.join(test_files_dir, "philippstyle_CGNN_outp.csv")

inp = pd.DataFrame()
scann = 100
inp["Ati"] = np.array(np.linspace(2, 13, scann))
inp["Ate"] = np.full_like(inp["Ati"], 5.0)
inp["An"] = np.full_like(inp["Ati"], 2.0)
inp["q"] = np.full_like(inp["Ati"], 0.660156)
inp["smag"] = np.full_like(inp["Ati"], 0.399902)
inp["x"] = np.full_like(inp["Ati"], 0.449951)
inp["Ti_Te"] = np.full_like(inp["Ati"], 1.0)
inp["logNustar"] = np.full_like(inp["Ati"], -1)
inp["Zeff"] = np.full_like(inp["Ati"], 1.2)


@pytest.fixture()
def philipp9DNN_json():
    net = Philipp9DNN.from_json(
        phillip_net_json_model_path,
        phillip_net_json_weights_path,
        standardization_path,
        "ITG",
        GB_scale_length=3.0,
        debias_output=False,
        descale_output_together=False,
    )
    return net


@pytest.fixture()
def test_outp():
    return pd.read_csv(outp_path, index_col=0)


@pytest.fixture()
def test_inp():
    return pd.read_csv(inp_path, index_col=0)


# TODO: Fix by Karel
@pytest.mark.skip("Known failing, to be fixed")
class TestPhilipp9DNN:
    def test_from_json(self, philipp9DNN_json):
        assert isinstance(philipp9DNN_json, Philipp9DNN)

    def test_evaluate_json(self, philipp9DNN_json, test_inp, test_outp):
        outp = philipp9DNN_json.get_output(
            test_inp,
            clip_low=False,
            clip_high=False,
            low_bound=None,
            high_bound=None,
            safe=True,
            output_pandas=True,
            shift_output_by=0,
        )
        # assert np.all(np.isclose(outp, test_outp, atol=1e-5))
        assert isinstance(outp, pd.DataFrame)
        assert all(outp.columns == ["efeITG_GB", "efiITG_GB", "pfeITG_GB"])
