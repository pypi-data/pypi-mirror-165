# pylint: disable=no-self-use,missing-function-docstring,missing-class-docstring,missing-module-docstring # noqa
import pytest
from IPython import embed  # pylint: disable=unused-import # noqa: F401
import pandas as pd
from pathlib import Path
import shutil

from qlknn.dataset.filtering import *


class TestFilters:
    def test_ck_filter(self, qlk_h5_gen2_4D_dataset):
        cke_filter(qlk_h5_gen2_4D_dataset.data, 50)
        cki_filter(qlk_h5_gen2_4D_dataset.data, 50)

    def test_septot_filter(self, qlk_h5_gen2_4D_dataset):
        septot_filter(qlk_h5_gen2_4D_dataset.data, 1.5)

    def test_ambipolar_filter(self, qlk_h5_gen2_4D_dataset):
        ambipolar_filter(qlk_h5_gen2_4D_dataset.data, 1.5)

    def test_femtoflux_filter(self, qlk_h5_gen2_4D_dataset):
        femtoflux_filter(qlk_h5_gen2_4D_dataset.data, 1e-4)

    def test_sanity_filter(self, qlk_h5_gen2_4D_dataset):
        data = sanity_filter(
            qlk_h5_gen2_4D_dataset.data, 1.5, 1.5, 1e-4, cke_bound=50, cki_bound=50
        )

    def test_regime_filter(self, qlk_h5_gen2_4D_dataset):
        data = regime_filter(qlk_h5_gen2_4D_dataset.data, 0, 100)

    @pytest.mark.skip("Pending update to gen5 qlk_h5_gen2_4D_datasets")
    def test_stability_filter(self, qlk_h5_gen2_4D_dataset):
        stability_filter(qlk_h5_gen2_4D_dataset.data)

    def test_div_filter(self, qlk_h5_gen2_4D_dataset):
        div_filter(qlk_h5_gen2_4D_dataset.data)


# qlk_h5_gen2_4D_dataset is a special legacy test object
# qlk_h5_gen5_4D_dataset is just a path
def test_create_divsum(tmpdir, store_path):
    divlist = [
        "efiTEM_GB_div_efeTEM_GB",
        "efeITG_GB_div_efiITG_GB",
    ]
    with tmpdir.as_cwd():
        # Create divsum changes the file in place! So copy
        shutil.copy2(store_path, tmpdir / store_path.name)
        store = pd.HDFStore(tmpdir / store_path.name)
        create_divsum(store, divnames=divlist)
        for name in divlist:
            assert "/output/" + name in store
        store.close()
