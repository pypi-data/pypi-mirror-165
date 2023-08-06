import logging
from collections import OrderedDict
import gc

import pandas as pd
import numpy as np

from qlknn.dataset.data_io import load_from_store, determine_column_map, combine_vars
from qlknn.misc.tools import profile, dataframe_okay
from qlknn.misc.analyse_names import split_parts, extract_part_names

try:
    profile
except NameError:
    from qlknn.misc.tools import profile

root_logger = logging.getLogger("qlknn")
logger = root_logger
logger.setLevel(logging.INFO)


class Dataset:
    def __init__(self, features, target):
        if not isinstance(features, np.ndarray):
            features = np.array(features)
        if not isinstance(target, np.ndarray):
            target = np.array(target)
        self._epochs_completed = 0
        self._index_in_epoch = 0
        self._full_dataset_passed = False
        self._data = np.hstack([features, target])
        self._num_features = features.shape[1]
        self._num_examples = self._data.shape[0]

    @property
    def _features(self):
        return self._data[:, : self._num_features]

    @property
    def _target(self):
        return self._data[:, self._num_features :]

    @property
    def epochs_completed(self):
        return self._epochs_completed

    @property
    def num_examples(self):
        return self._num_examples

    def next_batch(self, batch_size, shuffle=True):
        start = self._index_in_epoch
        if batch_size == -1:
            batch_size = self._num_examples
        if self._full_dataset_passed:
            # Shuffle the data
            if shuffle:
                # from IPython import embed
                # embed()
                # print(self._data[:10, :])
                perm = np.arange(self._num_examples)
                # print('C', self._data.flags['C_CONTIGUOUS'])
                # print('F', self._data.flags['F_CONTIGUOUS'])
                np.random.shuffle(perm)
                # self._data = self._data[np.random.permutation(self._num_examples), :]
                self._data = np.take(self._data, perm, axis=0)
                # print(self._data[:10, :])
            # Start next epoch
            start = 0
            self._index_in_epoch = 0
            self._full_dataset_passed = False
        self._index_in_epoch += batch_size
        if self._index_in_epoch >= self._num_examples:
            # Finished epoch
            self._epochs_completed += 1
            self._full_dataset_passed = True
            end = self._num_examples
        else:
            end = self._index_in_epoch
        batch = (
            self._data[start:end, : self._num_features],
            self._data[start:end, self._num_features :],
        )
        return batch

    def to_hdf(self, file, key):
        with pd.HDFStore(file) as store:
            store.put(key + "/features", self._features)
            store.put(key + "/target", self._target)

    @classmethod
    def read_hdf(cls, file, key):
        with pd.HDFStore(file) as store:
            dataset = Dataset(store.get(key + "/features"), store.get(key + "/target"))
        return dataset

    def astype(self, dtype):
        self._features = self._features.astype(dtype)
        self._target = self._target.astype(dtype)
        return self


class Datasets:
    _fields = ["train", "validation", "test"]

    def __init__(self, **kwargs):
        for name in self._fields:
            setattr(self, name, kwargs.pop(name))
        assert len(kwargs) == 0, "kwarg dict not fully read"

    def to_hdf(self, file):
        for name in self._fields:
            getattr(self, name).to_hdf(file, name)

    @classmethod
    def read_hdf(cls, file):
        datasets = {}
        for name in cls._fields:
            datasets[name] = Dataset.read_hdf(file, name)
        return Datasets(**datasets)

    def astype(self, dtype):
        for name in self._fields:
            setattr(self, name, getattr(self, name).astype(dtype))
        return self


@profile
def convert_panda(data_df, feature_names, target_names, frac_validation, frac_test, shuffle=True):
    # data_df = pd.concat(input_df, target_df, axis=1)
    total_size = len(data_df)
    # Dataset might be ordered. Shuffle to be sure
    if shuffle:
        data_df = shuffle_panda(data_df)
    validation_size = int(frac_validation * total_size)
    test_size = int(frac_test * total_size)
    train_size = total_size - validation_size - test_size

    datasets = []
    for slice_ in [
        data_df.iloc[:train_size, :],
        data_df.iloc[train_size : train_size + validation_size, :],
        data_df.iloc[train_size + validation_size :, :],
    ]:
        datasets.append(
            Dataset(
                slice_.loc[:, feature_names],
                slice_.loc[:, target_names],
            )
        )

    return Datasets(
        train=datasets[0],
        validation=datasets[1],
        test=datasets[2],
    )


def split_panda(data_df, frac_validation, frac_test, shuffle=True):
    """Split panda dataset in train/validation/test

    Args:
      data_df:         Full data dataframe.
      frac_validation: Fraction of the dataset that should end up in validation
      frac_validation: Fraction of the dataset that should end up in test


    Kwargs:
      shuffle:         Shuffle the dataset before splitting

    Returns:
      datasets:        Dict of splitted datasets

    """
    total_size = len(data_df)
    # Dataset might be ordered. Shuffle to be sure
    if shuffle:
        data_df = shuffle_panda(data_df)
    validation_size = int(frac_validation * total_size)
    test_size = int(frac_test * total_size)
    train_size = total_size - validation_size - test_size

    datasets = {
        "train": data_df.iloc[:train_size, :],
        "validation": data_df.iloc[train_size : train_size + validation_size, :],
        "test": data_df.iloc[train_size + validation_size :, :],
    }

    return datasets


def shuffle_panda(panda):
    return panda.iloc[np.random.permutation(np.arange(len(panda)))]


@profile
def drop_nans(target_df):
    """Drop any row that has one or more NaNs inside"""
    target_df.dropna(axis=0, inplace=True)
    return target_df


@profile
def filter_input(input_df, target_df):
    """Merge input and target DataFrame. Inner join.

    Use only samples in the feature set that are in the target set. Because
    of filtering, not every feature has a target
    """
    if not input_df.index.is_unique:
        raise ValueError("Given input_df does not have a unique index!")
    if not target_df.index.is_unique:
        raise ValueError("Given target_df does not have a unique index!")

    logger.debug("Calculating intersection of input_df and target_df")
    # pandas==1.1.1 is very slow, use numpy==1.19.1 instead
    com_index = input_df.index[np.in1d(input_df.index, target_df.index)]
    if not com_index.is_monotonic_increasing:
        logger.warning("Common index not monotonic increasing!" " This might take a while")
    if not input_df.index.is_monotonic_increasing:
        logger.warning("input_df index not monotonic increasing!" " This might take a while")
    if not target_df.index.is_monotonic_increasing:
        logger.warning("target_df index not monotonic increasing!" " This might take a while")

    logger.debug("Grabbing rows specified by common index from input_df")
    input_df = input_df.loc[com_index, :]
    logger.debug("Grabbing rows specified by common index from target_df")
    target_df = target_df.loc[com_index, :]

    logger.debug("Merge input and output datasets")
    input_df[target_df.columns] = target_df
    return input_df


@profile
def convert_dtype(data_df, settings):
    """Convert to dtype in settings dicts.

    Covert the dtype of the supplied DataFrame. Usually anything smaller than
    float32 will lead to NaNs in the cost function.
    """
    data_df = data_df.astype(settings["dtype"])
    return data_df


@profile
def drop_outliers(target_df, settings):
    """Drop outliers of DataFrame on both ends based on 'settings'

    Used to drop the top and bottom fraction of the dataset.
    Use the settings 'drop_outlier_above' and 'drop_outlier_below'
    to specify the range.

    WARNING! SORTS THE DATAFRAME IN PLACE!
    """
    target_df.sort_values(list(target_df.columns), inplace=True)
    startlen = target_df.shape[0]
    drop_outlier_above = settings["drop_outlier_above"] if "drop_outlier_above" in settings else 1
    drop_outlier_below = settings["drop_outlier_below"] if "drop_outlier_below" in settings else 0
    if drop_outlier_above < 1:
        target_df = target_df.iloc[: int(np.floor(startlen * drop_outlier_above)), :]
    if drop_outlier_below > 0:
        target_df = target_df.iloc[int(np.floor(startlen * drop_outlier_below)) :, :]
    return target_df


def prep_dataset(settings, verbosity_level=None):
    """Prepare a DataFrame specified by the settings dict for training.

    Loads the dataset from disk, drops nans and outliers, converts dataset
    to the requested dtype and merge features and targets together

    Args:
      - settings: Dict with settings. Will probably crash if keys are missing
    Kwargs:
      - verbosity_level: Verbosity of this function. Uses python logger.
                         Passed to the lower levels
    """
    if verbosity_level is not None:
        logger.setLevel(verbosity_level)
    train_dims = settings["train_dims"]
    logger.debug("Train dims are {!s}".format(train_dims))
    if len(train_dims) == 0:
        raise Exception("No train dims passed in settings!")

    # Open HDF store
    # This is usually a Unix-style softlink to our filtered dataset
    # First check if all columns are available, if not, try to build
    store = pd.HDFStore(settings["dataset_path"], "r")
    name_map = determine_column_map(store, "")
    store.close()
    rev_name_map = OrderedDict((v, k) for k, v in name_map.items())
    load_cols = []
    for dim in train_dims:
        if dim in rev_name_map:
            load_cols.append(dim)
        else:
            # Check if we can make it.
            # Can be smarter for combining more than 2 vars
            parts = split_parts(dim)
            coefs = extract_part_names(parts)
            if all(coef in rev_name_map for coef in coefs):
                # We can build it from parts, load the separate columns
                load_cols.extend(coefs)

    input_df, target_df, const = load_from_store(
        settings["dataset_path"], columns=load_cols, verbosity_level=verbosity_level
    )

    # Now build the missing variables
    for dim in train_dims:
        if dim not in target_df:
            combine_vars(target_df, dim)

    # And remove leftover variables to save memory
    for col in target_df:
        if col not in train_dims:
            del target_df[col]
    gc.collect()

    try:
        del input_df["nions"]  # Delete leftover artifact from dataset split
    except KeyError:
        pass

    logger.info("Loaded full dataset from store")
    logger.debug("Dropping outliers")
    target_df = drop_outliers(target_df, settings)
    logger.debug("Dropping NaNs")
    target_df = drop_nans(target_df)

    logger.debug("Converting dtypes")
    target_df = convert_dtype(target_df, settings)
    input_df = convert_dtype(input_df, settings)

    logger.debug("Filter the input set")
    data_df = filter_input(input_df, target_df)
    del target_df, input_df
    logger.info("Dataset prepared")

    return data_df


@profile
def calc_standardization(data_df, settings, warm_start_nn=None):
    """Calculate the factor and bias needed to standardize

    For NN training, the features are usually scaled or 'standardized'
    around zero. In our case, we also scale the output, which gave
    better results empirically (feel free to not scale it and see what happens)
    This functions calculates the factor a and bias b needed to scale the dataset
    given by

    ```
    x_standardized = a * x + b
    ```

    Where the type of standardization is given by standardization. It can be:
    - minmax_l_u to scale such that x_standardized is between l (lower bound) and
      u (upper bound). Common choice is minmax_-1_1
    - normsm_s_m to scale such that x_standardized has a mean of m and standard
      deviation of s. Common choice is normsm_1_0
    """
    if warm_start_nn is None:
        if settings["standardization"].startswith("minmax"):
            min = float(settings["standardization"].split("_")[-2])
            max = float(settings["standardization"].split("_")[-1])
            scale_factor, scale_bias = normab(data_df, min, max)

        if settings["standardization"].startswith("normsm"):
            s_t = float(settings["standardization"].split("_")[-2])
            m_t = float(settings["standardization"].split("_")[-1])
            scale_factor, scale_bias = normsm(data_df, s_t, m_t)
    else:
        scale_factor = pd.concat(
            [
                warm_start_nn._feature_prescale_factor,
                warm_start_nn._target_prescale_factor,
            ]
        ).astype(data_df.dtypes[0])
        scale_bias = pd.concat(
            [warm_start_nn._feature_prescale_bias, warm_start_nn._target_prescale_bias]
        ).astype(data_df.dtypes[0])
    if not dataframe_okay(scale_bias) or not dataframe_okay(scale_factor):
        logger.warning(
            "Warning! Calculated standardization has infinites "
            "and/or nulls! This _will_ cause trouble later. "
            "Calculated values: scale_factor=%s, scale_bias=%s",
            scale_factor,
            scale_bias,
        )

    return scale_factor, scale_bias


def normab(panda, a, b):
    factor = (b - a) / (panda.max() - panda.min())
    bias = (b - a) * panda.min() / (panda.max() - panda.min()) + a
    return factor, bias


def normsm(panda, s_t, m_t):
    m_s = np.mean(panda)
    s_s = np.std(panda)
    factor = s_t / s_s
    bias = -m_s * s_t / s_s + m_t
    return factor, bias
