# pylint: disable=no-self-use,missing-function-docstring,missing-class-docstring,missing-module-docstring,invalid-name # noqa
from pathlib import Path

import pytest  # pylint: disable=unused-import # noqa: F401
from IPython import embed  # pylint: disable=unused-import # noqa: F401
import pandas as pd
from pandas.testing import assert_series_equal

from qlknn.dataset.data_io import *


def test_load_from_store_default(store_path):
    """Test default use case of loading from store

    Most common use-case is passing a string,
    and having it load input, data and constants
    """
    inp, data, const = load_from_store(store_path)

    assert isinstance(inp, pd.DataFrame)
    assert isinstance(data, pd.DataFrame)
    assert isinstance(const, pd.Series)

    assert inp["Ati"].iloc[0] == pytest.approx(1e-14)
    assert inp["q"].iloc[0] == pytest.approx(0.66)
    assert inp["smag"].iloc[0] == pytest.approx(-1)
    assert inp["Ti_Te"].iloc[0] == pytest.approx(0.25)

    # To be clearer, use == False (not is False, it's a numpy bool!)
    assert data["ETG"].iloc[0] == False
    assert data["vti_GB"].iloc[0] == pytest.approx(0)

    assert const["gammaE"] == pytest.approx(1e-14)
    assert const["x"] == pytest.approx(0.45)


def test_combine_vars_missing_key(store_path):
    _, data, _ = load_from_store(store_path)
    with pytest.raises(KeyError, match="fakey"):
        combine_vars(data, "efeITG_GB_div_fakey_GB")


def test_combine_vars_undefined_op(store_path):
    _, data, _ = load_from_store(store_path)
    with pytest.raises(NotImplementedError, match="magic"):
        combine_vars(data, "efeITG_GB_magic_efiITG_GB")


def test_combine_vars_triplet(store_path):
    _, data, _ = load_from_store(store_path)
    new_df = combine_vars(data, "efeITG_GB_div_efiITG_GB_plus_efeITG_GB")
    assert new_df is None
    assert "efeITG_GB_div_efiITG_GB_plus_efeITG_GB" in data


def test_combine_vars_triplet_copy(store_path):
    _, data, _ = load_from_store(store_path)
    new_df = combine_vars(data, "efeITG_GB_div_efiITG_GB_plus_efeITG_GB", inplace=False)
    assert new_df is not None
    assert "efeITG_GB_div_efiITG_GB_plus_efeITG_GB" not in data


def test_combine_vars(store_path):
    _, data, _ = load_from_store(store_path)
    new_df = combine_vars(data, "efeITG_GB_div_efiITG_GB")
    assert new_df is None
    assert "efeITG_GB_div_efiITG_GB" in data


def test_combine_vars_copy_correctness(store_path):
    _, data, _ = load_from_store(store_path)
    new_df = combine_vars(data, "efeITG_GB_div_efiITG_GB", inplace=False)
    assert new_df is not None
    assert "efeITG_GB_div_efiITG_GB" in data
    assert "efeITG_GB_div_efiITG_GB" in new_df

    # ID tests
    assert new_df is not data
    assert_series_equal(data["efeITG_GB_div_efiITG_GB"], new_df["efeITG_GB_div_efiITG_GB"])
