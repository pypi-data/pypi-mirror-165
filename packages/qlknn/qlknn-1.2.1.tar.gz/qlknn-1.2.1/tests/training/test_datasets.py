# pylint: disable=missing-module-docstring,missing-function-docstring
from IPython import embed
import pandas as pd
import pytest

from qlknn.training.datasets import *  # pylint: disable=unused-wildcard-import, wildcard-import # noqa: F403, F401, E501


class TestDataset:
    def test_stuff(self):
        pass


class TestDatasets:
    def test_stuff(self):
        pass


def test_prep_dataset(default_settings):
    settings = default_settings
    data_df = prep_dataset(settings)
    assert dataframe_okay(data_df)


@pytest.fixture
def prepped_dataset(default_settings):
    settings = default_settings
    data_df = prep_dataset(settings)
    return data_df


def test_calc_standardization(prepped_dataset, default_settings):
    settings = default_settings
    scale_factor, scale_bias = calc_standardization(prepped_dataset, settings)
    assert dataframe_okay(scale_bias)
    assert dataframe_okay(scale_factor)


def test_calc_standardization_zeroes(caplog, prepped_dataset, default_settings):
    settings = default_settings
    prepped_dataset["Ti_Te"] = 0
    scale_factor, scale_bias = calc_standardization(prepped_dataset, settings)
    for record in caplog.records:
        assert record.levelname == "WARNING"
    assert caplog.text.startswith("WARNING  qlknn:datasets.py")


# def test_convert_panda(data_df, feature_names, target_names, frac_validation, frac_test, shuffle=True):
# def test_split_panda(data_df, frac_validation, frac_test, shuffle=True):
# def test_shuffle_panda(panda):
# def test_drop_nans(target_df):
# def test_filter_input(input_df, target_df):
# def test_convert_dtype(data_df, settings):
# def test_drop_outliers(target_df, settings):
# def test_normab(panda, a, b):
# def test_normsm(panda, s_t, m_t):
