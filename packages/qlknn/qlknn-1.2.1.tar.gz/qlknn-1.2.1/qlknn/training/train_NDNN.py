import sys
import json
import time
import os
import math
import logging
import site

# Enable fancy logging before anything else
root_logger = logging.getLogger("qlknn")
logger = root_logger
logger.setLevel(logging.INFO)

logger.debug("Python version is {!s}".format(sys.version_info))
if site.check_enableusersite():
    logger.debug(
        "According to your Python install, user site is enabled,"
        "giving it precedence to all other packages"
    )
    sys.path.insert(0, site.USER_SITE)

import numpy as np
import pandas as pd

from qlknn.training.datasets import split_panda, prep_dataset, calc_standardization
from qlknn.misc.tools import profile
from qlknn.training.nn_primitives import (
    scale_panda,
    descale_panda,
    model_to_json,
    model_to_json_dict,
)
from qlknn.training.keras_models import FFNN, HornNet
from qlknn.misc.tools import dump_package_versions


def train(settings, warm_start_nn=None, restore_old_checkpoint=False, workers=1, verbosity=0):
    if verbosity == 0:
        logger.setLevel(logging.INFO)
    elif verbosity >= 1:
        logger.setLevel(logging.DEBUG)
    dump_package_versions(log_func=logger.debug)
    start = time.time()

    data_df = prep_dataset(settings)
    logger.info("Basic preparation of dataset done")
    target_names = settings["train_dims"]
    # Everything that is not a target, is a feature
    feature_names = list(data_df.columns)
    for dim in target_names:
        feature_names.remove(dim)

    # To avoid skewing the distribution too much for mean std standardization,
    # we only use the non-zero part of the dataset to calculate mean/std
    # This probably doesn't make a lot of sense for minmax
    if settings["calc_standardization_on_nonzero"]:
        any_nonzero = (data_df[target_names] != 0).any(axis=1)
        data_df_nonzero = data_df.loc[any_nonzero, :]
        data_df_zero = data_df.loc[~any_nonzero, :]
        scale_factor, scale_bias = calc_standardization(
            data_df_nonzero, settings, warm_start_nn=warm_start_nn
        )
    else:
        scale_factor, scale_bias = calc_standardization(
            data_df, settings, warm_start_nn=warm_start_nn
        )

    logger.info("Standardization calculated")
    if settings.get("nn_type", "FFNN") == "HornNet":
        scale_bias[target_names] = 0
        if settings["goodness_only_on_unstable"]:
            settings["goodness_only_on_unstable"] = False
            logger.warning("Only MSE allowed when using CGMnets")
        if settings["cost_stable_positive_scale"] != 0:
            settings["cost_stable_positive_scale"] = 0
            logger.warning("Only MSE allowed when using CGMnets")

    if settings.get("scale_targets_together", False):
        scale_factor[target_names] = scale_factor[target_names].mean()

    logger.info("Standardizing dataset")
    data_df = scale_panda(data_df, scale_factor, scale_bias)

    if settings.get("instance_weighting", False):
        store = pd.HDFStore(settings["weights_path"], "r")
        data_df["weights"] = store[
            "/output/" + settings["train_dims"][0][3:6] + "weights"
        ].astype(settings["dtype"])
        store.close()

    # Set backwards compatibility default
    shuffle = settings.get("shuffle_before_split", True)
    # Split dataset in train/test/validate sets
    logger.info("Splitting dataset in train/test/validate")
    datasets = split_panda(
        data_df,
        settings["validation_fraction"],
        settings["test_fraction"],
        shuffle=shuffle,
    )

    logger.info("Initializing Keras network")
    if settings.get("nn_type", "FFNN") == "HornNet":
        net = HornNet(
            settings,
            feature_names,
            feature_prescale_bias=scale_bias[feature_names],
            feature_prescale_factor=scale_factor[feature_names],
            target_prescale_bias=scale_bias[target_names],
            target_prescale_factor=scale_factor[target_names],
            train_set=datasets["train"],
        )
    else:
        net = FFNN(
            settings,
            feature_names,
            feature_prescale_bias=scale_bias[feature_names],
            feature_prescale_factor=scale_factor[feature_names],
            target_prescale_bias=scale_bias[target_names],
            target_prescale_factor=scale_factor[target_names],
            train_set=datasets["train"],
        )

    logger.info("Kerasizing dataset")
    if settings.get("use_generator", True):
        (
            train_gen,
            validation_data,
            steps_per_epoch,
            validation_batch_size,
        ) = net._pandas_to_generator(settings, datasets)
        logger.info("Start training!")
        net.train(
            train_gen,
            validation_data,
            steps_per_epoch=steps_per_epoch,
            validation_batch_size=validation_batch_size,
            workers=workers,
            verbosity=verbosity,
        )
    else:
        train_data, validation_data = net._pandas_to_numpy(settings, datasets)
        batch_size = int(math.ceil(len(datasets["train"]) / settings["minibatches"]))
        logger.info("Start training!")
        net.train(train_data, validation_data, batch_size=batch_size, verbosity=verbosity)
    # net.own_train(datasets, verbosity=verbosity)


def train_NDNN_from_folder(warm_start_nn=None, restore_old_checkpoint=False, workers=1, **kwargs):
    with open("./settings.json") as file_:
        settings = json.load(file_)
    train(
        settings,
        warm_start_nn=warm_start_nn,
        restore_old_checkpoint=restore_old_checkpoint,
        workers=workers,
        **kwargs,
    )


def main(restore_old_checkpoint=False, **kwargs):
    nn = None
    # from qlknn.models.ffnn import QuaLiKizNDNN
    # nn = QuaLiKizNDNN.from_json('nn.json')
    train_NDNN_from_folder(
        warm_start_nn=nn, restore_old_checkpoint=restore_old_checkpoint, **kwargs
    )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Launch QLKNN training")
    parser.add_argument("--load-checkpoint", default=False, help="Start from saved checkpoint")
    parser.add_argument("--verbose", "-v", action="count", default=0)

    args = parser.parse_args()
    main(restore_old_checkpoint=args.load_checkpoint, verbosity=args.verbose)
