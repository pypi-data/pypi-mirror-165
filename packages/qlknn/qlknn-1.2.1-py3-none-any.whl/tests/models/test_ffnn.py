import os
import json

from IPython import embed  # pylint: disable=unused-import # noqa: F401
import numpy as np
import pandas as pd
import pytest

from qlknn.models.ffnn import *


class TestQuaLiKizNDNN:
    def test_get_output(self, nn_efi, inp_gen2_7D_df):
        output = nn_efi.get_output(inp_gen2_7D_df)


class TestQuaLiKizComboNN:
    def test_create(self, nn_efi, nn_efi_div_efe):
        QuaLiKizComboNN(
            ["efeITG_GB"],
            [nn_efi, nn_efi_div_efe],
            lambda nn0, nn1: nn0 * nn1,
        )

    def test_get_output(self, inp_gen2_7D_df, nn_efi, nn_efi_div_efe):
        net = QuaLiKizComboNN(
            ["efeITG_GB"],
            [nn_efi, nn_efi_div_efe],
            lambda nn0, nn1: nn0 * nn1,
        )
        out_combo = net.get_output(inp_gen2_7D_df, clip_low=False, clip_high=False)
        out_sep = pd.DataFrame(
            nn_efi.get_output(inp_gen2_7D_df, clip_low=False, clip_high=False).values
            * nn_efi_div_efe.get_output(inp_gen2_7D_df, clip_low=False, clip_high=False).values,
            columns=["efeITG_GB"],
        )
        assert out_combo.equals(out_sep)

    def test_multi_output(self, inp_gen2_7D_df, nn_efi, nn_efi_div_efe):
        net = QuaLiKizComboNN(
            ["efiITG_GB", "efeITG_GB_div_efiITG_GB"],
            [nn_efi, nn_efi_div_efe],
            lambda *args: np.hstack(args),
        )
        efi_nn_out = nn_efi.get_output(inp_gen2_7D_df, clip_low=False, clip_high=False)
        efi_div_efe_nn_out = nn_efi_div_efe.get_output(
            inp_gen2_7D_df, clip_low=False, clip_high=False
        )
        out_sep = efi_nn_out.join(efi_div_efe_nn_out)

        out_combo = net.get_output(inp_gen2_7D_df, clip_low=False, clip_high=False)
        assert out_combo.equals(out_sep)

    def test_pandas_index_passing(self, inp_gen2_7D_df: pd.DataFrame, nn_efi: QuaLiKizNDNN):
        # make sure original index is not default (does not start at 0)
        inp_gen2_7D_df.set_index(np.arange(10, len(inp_gen2_7D_df) + 10, 1), inplace=True)

        nn_out = nn_efi.get_output(inp_gen2_7D_df, pandas=True)
        null_w_index = pd.DataFrame(
            np.zeros_like(nn_out.values), columns=nn_out.columns, index=inp_gen2_7D_df.index
        )

        # pandas will automatically associate matching indices
        diff = nn_out - null_w_index

        assert (nn_out.sum().sum() == diff.sum().sum()) and (diff.isnull().sum().sum() == 0)
