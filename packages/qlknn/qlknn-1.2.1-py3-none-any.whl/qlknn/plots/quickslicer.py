import pickle
import os
import time
import re
import gc
import warnings
import sys
from itertools import product, chain
from functools import partial
from collections import OrderedDict
from multiprocessing import Pool, cpu_count
import json
import argparse
from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import Optional

import numpy as np
import scipy as sc
import scipy.stats as stats
import pandas as pd
from IPython import embed  # pylint: disable=unused-import # noqa: F401
import logging
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import gridspec, cycler


from qlknn.training.datasets import shuffle_panda
from qlknn.plots.load_data import nameconvert
from qlknn.dataset.data_io import load_from_store
from qlknn.misc.analyse_names import (
    split_parts,
    split_name,
    determine_driving_gradients,
)
from qlknn.misc.tools import parse_dataset_name

root_logger = logging.getLogger("qlknn")
logger = root_logger
logger.setLevel(logging.INFO)
pretty = False
have_nndb_functionality = False
try:
    from peewee import fn, OperationalError
except:
    logger.warning("Could not import peewee, cannot connect to NNDB")
    OperationalError = Exception
else:
    try:
        from qlknn.NNDB.model import (
            Network,
            NetworkJSON,
            PostprocessSlice,
            PostprocessSlice_9D,
            db,
        )
        from qlknn.NNDB.model import *

        have_nndb_functionality = True
    except:
        logger.warning("No NNDB access")

global nns, slicedim, df, style, col_names_loc, col_names  # Yes I use globals, deal with it
nns = None
slicedim = None
df = None
style = None
col_names_loc = None
col_names = None


def mode_to_settings(mode):
    settings = {}
    if mode == "debug":
        settings["plot"] = True
        settings["plot_pop"] = True
        settings["plot_nns"] = True
        settings["plot_slice"] = True
        settings["plot_poplines"] = True
        settings["plot_threshlines"] = True
        settings["plot_zerocolors"] = False
        settings["plot_thresh1line"] = False
        settings["calc_thresh1"] = False
        settings["calc_thresh2"] = True
        settings["calc_thresh3"] = False
        settings["hide_qualikiz"] = False
        settings["debug"] = True
        settings["parallel"] = False
        settings["plot_threshslope"] = False
    elif mode == "quick":
        settings["plot"] = False
        settings["plot_pop"] = False
        settings["plot_nns"] = False
        settings["plot_slice"] = False
        settings["plot_poplines"] = False
        settings["plot_threshlines"] = False
        settings["plot_zerocolors"] = False
        settings["plot_thresh1line"] = False
        settings["calc_thresh1"] = False
        settings["calc_thresh2"] = True
        settings["calc_thresh3"] = False
        settings["hide_qualikiz"] = False
        settings["debug"] = False
        settings["parallel"] = True
        settings["plot_threshslope"] = False
    elif mode == "pretty":
        settings["plot"] = True
        settings["plot_pop"] = False
        settings["plot_nns"] = True
        settings["plot_slice"] = False
        settings["plot_poplines"] = False
        settings["plot_threshlines"] = False
        settings["plot_zerocolors"] = False
        settings["plot_thresh1line"] = False
        settings["calc_thresh1"] = False
        settings["calc_thresh2"] = True
        settings["calc_thresh3"] = False
        settings["hide_qualikiz"] = False
        settings["debug"] = True
        settings["parallel"] = False
        settings["plot_threshslope"] = True
    return settings


def get_similar_not_in_table(
    table,
    max=20,
    only_dim=None,
    only_sep=False,
    no_particle=False,
    no_divsum=False,
    no_mixed=True,
    target_names=None,
    no_mixedmode=True,
    no_gam=True,
):
    non_sliced = Network.select().where(
        ~fn.EXISTS(table.select().where(getattr(table, "network") == Network.id))
    )
    if target_names is not None:
        non_sliced &= Network.select().where(Network.target_names == target_names)

    if only_dim is not None:
        non_sliced &= Network.select().where(
            fn.array_length(Network.feature_names, 1) == only_dim
        )

    if no_mixed:
        non_sliced &= Network.select().where(
            ~(
                fn.array_to_string(Network.target_names, ",") % "%pf%"
                & fn.array_to_string(Network.target_names, ",") % "%ef%"
            )
        )
    if no_mixedmode:
        non_sliced &= Network.select().where(
            ~(
                (
                    fn.array_to_string(Network.target_names, ",") % "%ITG%"
                    & fn.array_to_string(Network.target_names, ",") % "%TEM%"
                )
                | (
                    fn.array_to_string(Network.target_names, ",") % "%ITG%"
                    & fn.array_to_string(Network.target_names, ",") % "%ETG%"
                )
                | (
                    fn.array_to_string(Network.target_names, ",") % "%TEM%"
                    & fn.array_to_string(Network.target_names, ",") % "%ETG%"
                )
            )
        )

    if no_gam:
        non_sliced &= Network.select().where(
            ~(fn.array_to_string(Network.target_names, ",") % "%gam%")
        )
    tags = []
    if no_divsum:
        tags.extend(["div", "plus"])
    if no_particle:
        tags.append("pf")
    if len(tags) != 0:
        filter = ~fn.array_to_string(Network.target_names, ",") % ("%" + tags[0] + "%")
        for tag in tags[1:]:
            filter &= ~(fn.array_to_string(Network.target_names, ",") % ("%" + tag + "%"))
        non_sliced &= Network.select().where(filter)
    if only_sep:
        tags = ["TEM", "ITG", "ETG"]
        filter = fn.array_to_string(Network.target_names, ",") % ("%" + tags[0] + "%")
        for tag in tags[1:]:
            filter |= fn.array_to_string(Network.target_names, ",") % ("%" + tag + "%")

    if non_sliced.count() > 0:
        network = non_sliced.get()
    else:
        raise Exception("No candidates found for slicing!")

    non_sliced &= (
        Network.select()
        .where(Network.target_names == network.target_names)
        .where(Network.feature_names == network.feature_names)
    )
    non_sliced = non_sliced.limit(max)
    return non_sliced


def nns_from_NNDB(dim, max=20, only_dim=None):
    try:
        db.connect()
    except (OperationalError, NameError):
        logger.critical("ERROR! No access to NNDB, abort!")
        return
    if dim == 7:
        table = PostprocessSlice
    elif dim == 9:
        table = PostprocessSlice_9D
    non_sliced = get_similar_not_in_table(
        table,
        max=max,
        only_sep=True,
        no_particle=False,
        no_divsum=True,
        no_mixed=False,
        only_dim=only_dim,
    )
    network = non_sliced.get()
    style = "mono"
    if len(network.target_names) == 2:
        style = "duo"
    elif len(network.target_names) == 3:
        style = "triple"

    matches = []
    modes = []
    for target_name in network.target_names:
        matches.extend(re.compile("^.f.(ITG|ETG|TEM)_GB").findall(target_name))
        splitted = split_parts(target_name)
        if len(splitted) > 1:
            raise Exception(
                "Error! Can only quickslice pure networks, not {!s}".format(target_name)
            )
        __, __, mode, __ = split_name(splitted[0])
        modes.append(mode)
    if modes[1:] == modes[:-1]:
        mode = modes[0]
        if mode == "ITG":
            slicedim = "Ati"
        elif mode == "TEM" or mode == "ETG":
            slicedim = "Ate"
        else:
            raise Exception("Unknown mode {!s}".format(mode))
    else:
        raise Exception("Unequal stability regime. Cannot determine slicedim")
    nn_list = {network.id: str(network.id) for network in non_sliced}
    logger.info(
        "Found {:d} {!s} with target {!s}".format(
            len(non_sliced), network.__class__, network.target_names
        )
    )

    nns = OrderedDict()
    for dbnn in non_sliced:
        nn = dbnn.to_QuaLiKizNN()
        nn.label = "_".join([str(el) for el in [dbnn.__class__.__name__, dbnn.id]])
        nns[nn.label] = nn

    db.close()
    return slicedim, style, nns


def prep_df(
    store,
    feature_names,
    target_names,
    unstack,
    filter_less=np.inf,
    filter_geq=-np.inf,
    shuffle=True,
    sort=False,
    calc_maxgam=False,
    clip=False,
    myslice=None,
    frac=1,
    GB_scale=1,
):
    """Prepare a pd.HDFStore such that it can be safely used with QLKNN nets

    Returns a well-structured pd.DataFrame where the rows are samples
    and the columns are strictly ordered like
       feature_name_0 ... feature_name_n target_name_0 ... target_name_n

    So afterwards, we can use the underlying numpy blindly
    """

    input, data, const = load_from_store(
        store=store, columns=target_names, nustar_to_lognustar=False
    )
    data.dropna(axis="index", how="all", inplace=True)

    if "logNustar" in feature_names.to_list() and "logNustar" not in input.columns.to_list():
        print("Making logNustar")
        try:
            input["logNustar"] = np.log10(input["Nustar"])
            del input["Nustar"]
        except KeyError:
            logger.info("No Nustar in dataset, cannot create logNustar")
    if ("Zeff" == feature_names).any() and not ("Zeff" in input.columns):
        logger.warning("Creating Zeff. You should use a 9D dataset")
        if "Zeff" in const:
            input.insert(0, "Zeff", np.full_like(input["Ati"], float(const["Zeff"])))
        else:
            input["Zeff"] = 1
    if ("logNustar" == feature_names).any() and not ("logNustar" in input.columns):
        print("Making logNustar2")
        logger.warning("Creating logNustar. You should use a 9D dataset")
        if "Nustar" in const:
            input["logNustar"] = np.full_like(input["Ati"], np.log10(float(const["Nustar"])))
        else:
            input["logNustar"] = np.log10(0.009995)

    # Trying to apply a 7D QLKNN on a 4D dataset
    if (len(feature_names) == 7) and (len(input.columns) == 4):
        logger.warning("Slicing a 7D network with a 4D dataset. You should use a 7D dataset")
        missing_features = set(feature_names) - set(input.columns)
        if "x" in missing_features:
            logger.warning("Creating fake column x=.45")
            input["x"] = 0.45
        if "Ate" in missing_features:
            if "Ati" in input.columns:
                logger.warning("Creating fake column Ate=Ati")
                input["Ate"] = input["Ati"]
        if "An" in missing_features:
            logger.warning("Creating fake column An=3")
            input["An"] = 3

    if set(feature_names).issubset(input.columns):
        if any(input.columns != feature_names):
            logger.warning(
                "{!s} != {!s}, using 2* RAM to reorder.".format(input.columns, feature_names)
            )
            input = input[feature_names]
    else:
        raise RuntimeError(
            "Could not generate fake input with columns"
            f"{feature_names}, managed {input.columns}. Does your dataset match your network?"
        )

    # get_vars = target_names
    # data = pd.DataFrame()

    # dataset_vars = store.get_storer('/megarun1/flattened').non_index_axes[0][1]
    # for target_name in target_names:
    #    if target_name not in dataset_vars:
    #        print('WARNING! {!s} missing from dataset. Trying to reconstruct'.format(target_name))
    #        if target_name == 'efiTEM_GB_div_efeTEM_GB':
    #            parts = store.select('megarun1/flattened', columns=['efiTEM_GB', 'efeTEM_GB'])
    #        elif target_name == 'pfeTEM_GB_div_efeTEM_GB':
    #            parts = store.select('megarun1/flattened', columns=['pfeTEM_GB', 'efeTEM_GB'])
    #        elif target_name == 'efeITG_GB_div_efiITG_GB':
    #            parts = store.select('megarun1/flattened', columns=['efeITG_GB', 'efiITG_GB'])
    #        elif target_name == 'pfeITG_GB_div_efiITG_GB':
    #            parts = store.select('megarun1/flattened', columns=['pfeITG_GB', 'efiITG_GB'])
    #        else:
    #            raise Exception('Could not reconstruct {!s}'.format(target_name))
    #        se = parts.iloc[:,0] / parts.iloc[:,1]
    #        se.name = target_name
    #        data = data.append(se.to_frame())
    #        get_vars = get_vars[(get_vars != target_name)]

    input_cols = list(input.columns)
    logger.info("Merging target and features")
    df = data = input.merge(data, left_index=True, right_index=True, copy=False)
    del input
    gc.collect()
    # df = input.join(data[target_names], how='inner')

    if calc_maxgam is True:
        df_gam = store.select("/megarun1/flattened", columns=["gam_leq_GB", "gam_great_GB"])
        df_gam = df_gam.max(axis=1).to_frame("maxgam")
        df = df.join(df_gam)

    if myslice is not None:
        for name, val in myslice.items():
            if name in df:
                df = df[np.isclose(df[name], float(val), atol=1e-5, rtol=1e-3)]
                print("after", name, len(df))
            else:
                logging.warning(
                    "Requested {0!s}={1!s}, but {0!s} not in dataset".format(name, val)
                )

    if clip is True:
        logger.info("Clipping")
        df[target_names] = df[target_names].clip(filter_less, filter_geq, axis=1)
        # df = df[(df[target_names] < filter_less).all(axis=1)]
        # df = df[(df[target_names] >= filter_geq).all(axis=1)]

    logger.info("Setting index")
    df.set_index(input_cols, inplace=True)
    if sort:
        logger.info("Sorting")
        if sort and shuffle:
            logging.warning("Sorting and shuffeling. Sort will be useless")
        df = df.sort_index(level=unstack)

    if GB_scale != 1:
        scale_mask = [
            not any(prefix in name for prefix in ["df", "chie", "xaxis"]) and "GB" in name
            for name in df.columns
        ]
        logger.info(
            "Scaling {!s} by factor {!s}".format(df.columns[scale_mask].tolist(), GB_scale)
        )
        df.iloc[:, scale_mask] *= GB_scale

    logger.info("Unstacking slices")
    df = df.unstack(unstack)

    if shuffle:
        logger.info("Every day I'm shuffling")
        df = shuffle_panda(df)

    if frac < 1:
        logger.info("Taking {!s} fraction".format(frac))
        if not shuffle:
            logger.warning(
                "Taking fraction without shuffle. You will always get the same slices!"
            )
        idx = int(frac * len(df))
        if idx == 0:
            logger.warning(
                "Given fraction {!s} would result in no slices. Taking one slice instead".format(
                    frac
                )
            )
            idx = 1
        df = df.iloc[:idx, :]
    # df = df.iloc[1040:2040,:]

    logger.info("Converting to float64")
    df = df.astype("float64")
    logger.info("dataset loaded!")
    return df


def check_if_same_order(df, nns, slicedim):
    """ Check if feature_names of the nns match the df column order"""
    is_same_order = True
    for nn in nns.values():
        slicedim_idx = nn._feature_names[nn._feature_names == slicedim].index[0]
        varlist = list(df.index.names)
        varlist.insert(slicedim_idx, slicedim)
        try:
            if ~np.all(varlist == nn._feature_names):
                is_same_order = False
        except ValueError:
            raise Exception(
                "Dataset has features {!s} but dataset has features {!s}".format(
                    varlist, list(nn._feature_names)
                )
            )
    return is_same_order


def find_runs(x):
    """Find runs of consecutive items in an array.

    by https://gist.github.com/alimanfoo, see
    https://gist.github.com/alimanfoo/c5977e87111abe8127453b21204c1065
    """

    # ensure array
    x = np.asanyarray(x)
    if x.ndim != 1:
        raise ValueError("only 1D array supported")
    n = x.shape[0]

    # handle empty array
    if n == 0:
        return np.array([]), np.array([]), np.array([])
    else:
        # find run starts
        loc_run_start = np.empty(n, dtype=bool)
        loc_run_start[0] = True
        np.not_equal(x[:-1], x[1:], out=loc_run_start[1:])
        run_starts = np.nonzero(loc_run_start)[0]

        # find run values
        run_values = x[loc_run_start]

        # find run lengths
        run_lengths = np.diff(np.append(run_starts, n))

        return run_values, run_starts, run_lengths


def calculate_thresh1(x, feature, target, debug=False):
    try:
        idx = np.where(target == 0)[0][-1]  # Only works for 1D, index of last zero
        slope, intercept, r_value, p_value, std_err = stats.linregress(
            feature[idx:][~np.isnan(target[idx:])],
            target[idx:][~np.isnan(target[idx:])],
        )
        thresh_pred = x * slope + intercept
        thresh1 = x[thresh_pred < 0][-1]
    except (ValueError, IndexError):
        thresh1 = np.NaN
        if debug:
            logger.debug("No threshold1")
    return thresh1


def calculate_thresh2(feature, target, debug=False):
    if len(target.shape) > 1:
        raise NotImplementedError("2D threshold not implemented yet")
    try:
        idx = np.where(target == 0)[0][-1]  # Only works for 1D
        idx2 = np.where(~np.isnan(target[idx + 1 :]))[0][0] + idx + 1
        # idx = np.arange(target.shape[0]),target.shape[1] - 1 - (target[:,::-1]==0).argmax(1) #Works for 2D
        thresh2 = (feature[idx] + feature[idx2]) / 2
    except IndexError:
        thresh2 = np.NaN
        if debug:
            logger.debug("No threshold2")

    return thresh2


def calculate_thresh3(x, feature, target, debug=False, points=2):
    if len(target.shape) > 1:
        raise NotImplementedError("2D threshold not implemented yet")
    target = np.abs(target)
    feature = np.asanyarray(feature)[~np.isnan(target)]
    target = target[~np.isnan(target)]
    # run_values, run_starts, run_lengths = find_runs(np.diff(target) / np.diff(feature) > 0)
    grad = np.diff(target, prepend=np.nan) / np.diff(feature, prepend=np.nan)
    slope, intercept, r_value, p_value, std_err = stats.linregress(
        feature[grad > 0][:points], target[grad > 0][:points]
    )
    try:
        thresh_pred = x * slope + intercept
        thresh = x[thresh_pred < 0][-1]
    except (ValueError, IndexError):
        thresh = np.NaN
        if debug:
            logger.debug("No threshold3")

    return thresh


# 5.4 ms ± 115 µs per loop (mean ± std. dev. of 7 runs, 100 loops each) total
def process_chunk(
    target_names, chunck, thresh_method="2", settings=None, safe=True, column_map=None
):

    res = []
    for ii, row in enumerate(chunck.iterrows()):
        res.append(
            process_row(
                target_names,
                row,
                thresh_method=thresh_method,
                settings=settings,
                safe=safe,
                column_map=column_map,
            )
        )
    return res


def map_column_name_to_index_map(df, nns):
    """ Generate a map from QLKNN output names to numpy matrix indices"""
    column_map = []
    col_names = []
    if nns is not None:
        max_target_length = max(len(nn._target_names) for nn in nns.values())
        column = 0
        for ii, nn in enumerate(nns.values()):
            target_names = nn._target_names.to_list()
            # Do not map particle flux columns
            this_map = [column + jj for jj, name in enumerate(target_names)]
            # Pad with -1's
            this_map += [-1] * (max_target_length - len(target_names))
            column_map += this_map
            column += len(target_names)

        col_names_loc = list(
            str(nn_name) + "_" + str(col)
            for nn_name, nn in nns.items()
            for col in nn._target_names
        )
        col_names = [col_names_loc[colnum] if colnum >= 0 else "empty" for colnum in column_map]

        if len(column_map) != len(col_names):
            raise RuntimeError("Column names different length than produced map")
    return column_map, col_names


def process_row(
    target_names,
    row,
    thresh_method="2",
    ax1=None,
    safe=True,
    settings=None,
    column_map=None,
):
    """Process a single 'row' or 'slice'

    Args:
      - target_names: Target names to be analysed. Will only be
          used to determine shapes, as all data should be pre-
          formatted at this point
      - row: Tuple with el[0] the remaining dims of the slice
          and el[1] the pd.Series of the slice itself

    Kwargs:
      - thresh_method: String representing the threshold method
          used to calculate the QLK threshold
      - ax1: Axis to plot debugging plots on
      - safe: Run the NNs in safe mode; e.g. with DataFrames
      - settings: Additional slice settings
      - column_map: Length of map matches result array. Values
          match the column of NN res. Mandatory if nns are defined
    """
    calc_thresh_method = "calc_thresh" + thresh_method
    if calc_thresh_method not in settings or not settings[calc_thresh_method]:
        logger.warning(
            "{!s} was not True, but needed for thresh calculation. Forcing to true".format(
                calc_thresh_method
            )
        )
    if nns is not None and column_map is None:
        raise Exception("Provide a map from NN names to columns, or the rest will fail")
    if column_map is not None:
        column_map_clean = [el for el in column_map if el >= 0]
    index, slice_ = row
    feature = slice_.index.levels[1]
    target = slice_.values[: len(feature) * len(target_names)].reshape(
        len(target_names), len(feature)
    )

    target_idx = slice_.index.get_level_values(0)
    target_rownames = target_idx[target_idx.duplicated()].unique()
    logger.debug("Current slice:\n {!s}".format(slice_))
    logger.debug("Numpy style slice:\n {!s}".format(target))
    logger.debug("With rows: {!s}".format(target_rownames))
    if np.all(np.logical_or(target == 0, np.isnan(target))):
        logger.debug("Slice is all NaNs or zeros, skipping slice")
        return (1,)
    else:
        if nns is not None:
            # 156 µs ± 10.4 µs per loop (mean ± std. dev. of 7 runs, 10000 loops each) (no zerocolors)
            # Predict threshold statistics for each network and each
            # target it predicts. If a network does not predict a particular
            # ntarget, all stats are NaNs for that target
            max_target_length = max(len(nn._target_names) for nn in nns.values())
            thresh_nn = np.empty(max_target_length * len(nns))  # Threshold of NNs
            thresh_nn_i = np.empty_like(
                thresh_nn, dtype="int64"
            )  # Index in NN prediction array of the threshold
            popbacks = np.empty_like(thresh_nn)
            thresh1_misses = np.empty_like(thresh_nn)
            thresh2_misses = np.empty_like(thresh_nn)
            wobble_unstab = np.full_like(thresh_nn, np.nan)
            wobble_qlkunstab = np.full_like(thresh_nn, np.nan)
            wobble_tot = np.full_like(thresh_nn, np.nan)
        if settings["plot_zerocolors"]:
            maxgam = slice_["maxgam"]

        # Create slice, assume sorted
        # 14.8 µs ± 1.27 µs per loop (mean ± std. dev. of 7 runs, 100000 loops each)
        x = np.linspace(feature.values[0], feature.values[-1], 200)
        # if plot:
        if not ax1 and settings["plot"]:
            fig = plt.figure()
            if settings["plot_pop"] and settings["plot_slice"]:
                gs = gridspec.GridSpec(
                    2,
                    2,
                    height_ratios=[10, 1],
                    width_ratios=[5, 1],
                    left=0.05,
                    right=0.95,
                    wspace=0.05,
                    hspace=0.05,
                )
                ax2 = plt.subplot(gs[1, 0])
                ax3 = plt.subplot(gs[0, 1])
            if not settings["plot_pop"] and settings["plot_slice"]:
                gs = gridspec.GridSpec(
                    2,
                    1,
                    height_ratios=[10, 2],
                    width_ratios=[1],
                    left=0.05,
                    right=0.95,
                    wspace=0.05,
                    hspace=0.05,
                )
                ax2 = plt.subplot(gs[1, 0])
            if not settings["plot_pop"] and not settings["plot_slice"]:
                gs = gridspec.GridSpec(
                    1,
                    1,
                    height_ratios=[1],
                    width_ratios=[1],
                    left=0.05,
                    right=0.95,
                    wspace=0.05,
                    hspace=0.05,
                )
            ax1 = plt.subplot(gs[0, 0])
            # ax1.set_prop_cycle(cycler('color', ['#f1eef6','#d7b5d8','#df65b0','#dd1c77','#980043']))
            # http://tristen.ca/hcl-picker/#/clh/5/273/2A0A75/D59FEB
            # ax1.set_prop_cycle(cycler('color', ['#2A0A75','#6330B8','#9F63E2','#D59FEB']))
            if nns is not None:
                if len(nns) == 1:
                    color_range = np.array([0.7])
                else:
                    color_range = np.linspace(0, 0.9, len(nns))
                # Create a cycler so every nn has its own color, and every output has its own linestyle
                default_cycler = (
                    cycler(color=plt.cm.plasma(color_range)),
                    cycler(linestyle=["-", "--", "-."]),
                )

            if slicedim in nameconvert:
                xlabel = nameconvert[slicedim]
            else:
                logger.warn("No pretty name for {!s}".format(slicedim))
                xlabel = slicedim
            ax1.set_xlabel(xlabel)
            if len(target_names) == 1:
                ylabel = target_names[0]
            else:
                ylabel = " ".join(target_names)
            ax1.set_ylabel(ylabel)

        # All thresholds operate on the _first target only_
        if settings["calc_thresh1"]:
            thresh1 = calculate_thresh1(
                x, feature.values, np.abs(target[0, :]), debug=settings["debug"]
            )

        # 12.5 µs ± 970 ns per loop (mean ± std. dev. of 7 runs, 100000 loops each)
        # if all(['ef' in name for name in target_names]):
        #    thresh2 = calculate_thresh2(feature.values, target[0,:], debug=settings['debug'])
        # elif all(['pf' in name for name in target_names]):
        if settings["calc_thresh2"]:
            thresh2 = calculate_thresh2(
                feature.values, np.abs(target[0, :]), debug=settings["debug"]
            )

        if settings["calc_thresh3"]:
            thresh3 = calculate_thresh3(
                x, feature.values, np.abs(target[0, :]), debug=settings["debug"]
            )

        thresh = locals()["thresh" + thresh_method]
        # For now assume the thresholds for all dimensions are the same
        # For simpleness, just keep it as float

        if settings["plot"] and settings["plot_threshlines"]:
            thresh_color = "cyan"
            if settings["calc_thresh1"]:
                ax1.axvline(thresh1, c=thresh_color, linestyle="--", label="thresh1 (QLK)")
            if settings["calc_thresh2"]:
                ax1.axvline(thresh2, c=thresh_color, linestyle=":", label="thresh2 (QLK)")
            if settings["calc_thresh3"]:
                ax1.axvline(thresh3, c=thresh_color, linestyle="-.", label="thresh3 (QLK)")

        if settings["plot"] and settings["plot_threshslope"]:
            if ~np.isnan(thresh):
                pre_thresh = x[x <= thresh]
                ax1.plot(pre_thresh, np.zeros_like(pre_thresh), c="gray", linestyle="dashed")
                post_thresh = x[x > thresh]
                se = slice_.loc[target_names]
                se.index = se.index.droplevel()
                se = se.loc[se.index > thresh].dropna()
                a = sc.optimize.curve_fit(lambda x, a: a * x, se.index - thresh, se.values)[0][0]
                ax1.plot(
                    post_thresh,
                    a * (post_thresh - thresh),
                    c="gray",
                    linestyle="dashed",
                )

        # Insert the slice_dim into the NN input array
        if nns is not None:
            # 13.7 µs ± 1.1 µs per loop (mean ± std. dev. of 7 runs, 100000 loops each)
            if not safe:
                slice_list = [np.full_like(x, val) for val in index]
                slicedim_idx = np.nonzero(
                    list(nns.values())[0]._feature_names.values == slicedim
                )[0][0]
                slice_list.insert(slicedim_idx, x)
            else:
                logger.warning("Slicing in safe mode! Double check the debug logs!")
                slice_dict = {
                    name: np.full_like(x, val) for name, val in zip(df.index.names, index)
                }
                slice_dict[slicedim] = x

        # Plot target points
        if settings["plot"] and settings["plot_slice"]:
            table = ax2.table(
                cellText=[
                    [nameconvert[name] for name in df.index.names],
                    ["{:.2f}".format(xx) for xx in index],
                ],
                cellLoc="center",
            )
            table.auto_set_font_size(False)
            table.scale(1, 1.5)
            # table.set_fontsize(20)
            ax2.axis("tight")
            ax2.axis("off")
        # fig.subplots_adjust(bottom=0.2, transform=ax1.transAxes)

        # Make NN predictions
        if nns is not None:
            nn_preds = np.ndarray([x.shape[0], 0])
            # We loop over nns here, so we will get an array
            # nn_preds that is differently shaped from the
            # result array!
            for ii, (nn_index, nn) in enumerate(nns.items()):
                clip_low = True
                if not safe:
                    low_bound = np.array(
                        [
                            0 if ("ef" in name) and (not "div" in name) else -np.inf
                            for name in nn._target_names
                        ]
                    )
                else:
                    low_bound = pd.Series(
                        {
                            name: 0 if ("ef" in name) and (not "div" in name) else -np.inf
                            for name in nn._target_names
                        }
                    )
                clip_high = False
                high_bound = None
                # if all(['ef' in name for name in nn._target_names]):
                #    clip_low = True
                #    low_bound = np.zeros((len(nn._target_names), 1))

                #    #high_bound = np.full((len(nn._target_names), 1), np.inf)
                #    clip_high = False
                #    high_bound = None
                # elif all(['pf' in name for name in nn._target_names]):
                #    #raise NotImplementedError('Particle bounds')
                #    clip_low = False
                #    low_bound = np.full((len(nn._target_names), 1), -80)
                #    clip_high = False
                #    high_bound = np.full((len(nn._target_names), 1), 80)
                # else:
                #    clip_low = False
                #    low_bound = None
                #    clip_high = False
                #    high_bound = None
                #    print('Mixed target!')
                #    #embed()
                #    print('Weird stuff')
                if not safe:
                    nn_pred = nn.get_output(
                        np.array(slice_list).T,
                        clip_low=clip_low,
                        low_bound=low_bound,
                        clip_high=clip_high,
                        high_bound=high_bound,
                        safe=safe,
                        output_pandas=False,
                    )
                else:
                    nn_pred = nn.get_output(
                        pd.DataFrame(slice_dict),
                        clip_low=clip_low,
                        low_bound=low_bound,
                        clip_high=clip_high,
                        high_bound=high_bound,
                        safe=safe,
                        output_pandas=True,
                    ).values
                nn_preds = np.concatenate([nn_preds, nn_pred], axis=1)
                logger.trace("Prediction for nn={!s}: \n{!s}".format(nn.label, nn_pred))

        if nns is not None and settings["plot"] and settings["plot_nns"]:
            lines = []
            cc = None
            # for nn_name, nn in nns.keys():
            this_nn = -1
            for ii in range(len(thresh_nn)):
                ncol = column_map[ii]
                n_target_col = ii // len(nns)
                n_net = int(np.floor(ii / len(target_names)))
                if ncol < 0:
                    continue
                if this_nn != n_net:
                    this_nn = n_net
                cc = default_cycler[0].by_key()["color"][n_net]
                ls = default_cycler[1].by_key()["linestyle"][n_target_col]
                lines.append(
                    ax1.plot(x, nn_preds[:, ncol], label=col_names_loc[ncol], color=cc, ls=ls)[0]
                )

        if nns is not None:
            matrix_style = False
            if matrix_style:
                thresh_i = (
                    np.arange(nn_preds.shape[1]),
                    nn_preds.shape[0] - 1 - (nn_preds[::-1, :] == 0).argmax(0),
                )[1]
                thresh = x[thresh_i]
                thresh[thresh == x[-1]] = np.nan
            else:
                # Figure out with nn target matches which qlk threshold
                # Loop over each 'stat column', each column matches
                # a unique combinations of NN and target_name
                for ii, target_nn_combo in enumerate(column_map):
                    if target_nn_combo == -1:
                        thresh_nn[ii] = np.nan
                    else:
                        row = nn_preds[:, target_nn_combo]
                        try:
                            # If the last point is 0 or lower the next algorithm will fail
                            # Put NaN to be sure (this almost never happens)
                            if row[-1] <= 0:
                                thresh_nn[ii] = np.nan
                            else:
                                # Detect the index of the last zero crossing
                                # For example, take a prediction [-0.1, 0.01, -0.2, 0.1, 1, 5]
                                # np.sign(row) will be [-1, 1, -1, 1, 1, 1]
                                # np.diff(np.sign(row)) will be [ 2., -2.,  2.,  0., 0.]
                                # np.where will give us the indices where that array is non-zero
                                # Non-zero values are where a zero crossing occurred
                                # So the last index of _that_ array is the last point before the last
                                # zero crossing. In other words, the threshold!
                                thresh_i = thresh_nn_i[ii] = np.where(np.diff(np.sign(row)))[0][
                                    -1
                                ]
                                thresh_nn[ii] = x[thresh_i]
                        except IndexError:
                            thresh_nn[ii] = np.nan

            if settings["plot"] and settings["plot_threshlines"]:
                for ii in range(len(thresh_nn)):
                    ncol = column_map[ii]
                    n_target_col = ii // len(nns)
                    n_net = int(np.floor(ii / len(target_names)))
                    if ncol < 0:
                        continue
                    if this_nn != n_net:
                        this_nn = n_net
                    cc = default_cycler[0].by_key()["color"][n_net]
                    ls = default_cycler[1].by_key()["linestyle"][n_target_col]
                    ax1.axvline(thresh_nn[ii], c=cc, linestyle="dotted")

            if matrix_style:
                masked = np.ma.masked_where(x[:, np.newaxis] > thresh, nn_preds)
                # popback_i = (masked.shape[0] - 1 - (masked[::1,:]!=0)).argmax(0)
                popback_i = (
                    masked.shape[0] - 1 - (masked.shape[0] - 1 - (masked[::-1, :] != 0)).argmin(0)
                )
                popback = x[popback_i]
                popback[popback == x[-1]] = np.nan
            else:
                for ii, row in enumerate(nn_preds.T):
                    if not np.isnan(thresh_nn[ii]):
                        try:
                            popback_i = np.flatnonzero(row[: thresh_nn_i[ii]])
                            popbacks[ii] = x[popback_i[-1]]
                        except (IndexError):
                            popbacks[ii] = np.nan
                    else:
                        popbacks[ii] = np.nan

            # 5.16 µs ± 188 ns per loop (mean ± std. dev. of 7 runs, 100000 loops each)

            # Calculate wobbles of evaulated nets
            wobble_loc = np.abs(np.diff(nn_preds, n=2, axis=0))
            wobble_tot_loc = np.mean(wobble_loc, axis=0)
            with warnings.catch_warnings():  # col[ind:] is empty if no threshold
                warnings.simplefilter("ignore", category=RuntimeWarning)
                wobble_unstab_loc = np.array(
                    [np.mean(col[ind:]) for ind, col in zip(thresh_nn_i + 1, wobble_loc.T)]
                )
            try:

                with warnings.catch_warnings():  # col[ind:] is empty if no threshold
                    warnings.simplefilter("ignore", category=RuntimeWarning)
                    thresh_2_i = np.where(np.abs(x - thresh) == np.min(np.abs(x - thresh)))[0][0]
                with warnings.catch_warnings():  # col[thresh_2_i:] is empty if no threshold
                    warnings.simplefilter("ignore", category=RuntimeWarning)
                    wobble_qlkunstab_loc = np.array(
                        [np.mean(col[thresh_2_i:]) for col in wobble_loc.T]
                    )
            except IndexError:
                thresh_2_i = np.nan
                wobble_qlkunstab_loc = None
            # Cast wobbles to thresh shapes
            wobble_unstab[column_map_clean] = wobble_unstab_loc[column_map_clean]
            if wobble_qlkunstab_loc is not None:
                wobble_qlkunstab[column_map_clean] = wobble_qlkunstab_loc[column_map_clean]
            wobble_tot[column_map_clean] = wobble_tot_loc[column_map_clean]

            if settings["plot"] and settings["plot_pop"]:
                thresh_misses = thresh_nn - thresh
                thresh_popback = popbacks - thresh
                slice_stats = np.array([thresh_misses, thresh_popback, wobble_qlkunstab]).T
                slice_strings = np.array(
                    ["{:.1f}".format(xx) for xx in slice_stats.reshape(slice_stats.size)]
                )
                slice_strings = slice_strings.reshape(slice_stats.shape)
                slice_strings = np.insert(
                    slice_strings,
                    0,
                    ["thre_mis", "pop_mis", "wobble_qlkunstab"],
                    axis=0,
                )
                table = ax3.table(cellText=slice_strings, loc="center")
                table.auto_set_font_size(False)
                ax3.axis("tight")
                ax3.axis("off")
                logger.debug(
                    "Derived stats: \n{!s}".format(
                        pd.DataFrame(
                            slice_stats,
                            index=col_names,
                            columns=["thre_mis", "pop_mis", "wobble_qlkunstab"],
                        )
                    )
                )

        if settings["plot"]:
            if settings["plot_zerocolors"]:
                color = target.copy()
                color[(target == 0) & (maxgam == 0)] = "green"
                color[(target != 0) & (maxgam == 0)] = "red"
                color[(target == 0) & (maxgam != 0)] = "magenta"
                color[(target != 0) & (maxgam != 0)] = "blue"
            else:
                color = "blue"
            if settings["hide_qualikiz"]:
                color = "white"
                zorder = 1
                label = ""
            else:
                zorder = 1000
                # label = 'QuaLiKiz'
                # label = 'Turbulence model'
                # label=''
                labels = target_rownames
            markers = ["1", "2", "3"]
            for label, column, marker in zip(labels, target, markers):
                ax1.scatter(
                    feature[column != 0],
                    column[column != 0],
                    c=color,
                    label=label,
                    marker=marker,
                    zorder=zorder,
                )
            ax1.scatter(
                feature[column == 0],
                column[column == 0],
                edgecolors=color,
                marker="o",
                facecolors="none",
                zorder=zorder,
            )

        # Plot regression
        if settings["plot"] and settings["plot_thresh1line"] and not np.isnan(thresh1):
            # plot_min = ax1.get_ylim()[0]
            plot_min = -0.1
            x_plot = x[(thresh_pred > plot_min) & (thresh_pred < ax1.get_ylim()[1])]
            y_plot = thresh_pred[(thresh_pred > plot_min) & (thresh_pred < ax1.get_ylim()[1])]
            ax1.plot(x_plot, y_plot, c="gray", linestyle="dotted")
            ax1.plot(
                x[x < thresh1],
                np.zeros_like(x[x < thresh1]),
                c="gray",
                linestyle="dotted",
            )
            # ax1.axvline(thresh1, c='black', linestyle='dotted')

        if nns is None:
            slice_res = np.full((1, 5), np.nan)
        else:
            slice_res = np.array(
                [thresh_nn, popbacks, wobble_tot, wobble_unstab, wobble_qlkunstab]
            ).T
            logger.debug(
                "Calculated stats: \n{!s}".format(
                    pd.DataFrame(
                        slice_res,
                        columns=[
                            "thresh_nn",
                            "popbacks",
                            "wobble_tot",
                            "wobble_unstab",
                            "wobble_qlkunstab",
                        ],
                        index=col_names,
                    )
                )
            )
        if settings["plot"]:
            ax1.legend()
            ax1.set_ylim(bottom=min(ax1.get_ylim()[0], 0))
            plt.show()
            fig.savefig("slice.pdf", format="pdf", bbox_inches="tight")
            qlk_data = pd.DataFrame(target.T, columns=target_names, index=feature)
            if nns is not None:
                nn_data = pd.DataFrame(nn_preds, columns=col_names_loc)
                nn_data.index = x
                nn_data.index.name = feature.name
                slice_data = pd.Series(dict(zip(df.index.names, index)))
                slice_latex = (
                    ("  {!s} &" * len(df.index.names))
                    .format(*[nameconvert[name] for name in df.index.names])
                    .strip(" &")
                )
                slice_latex += ("\\\\\n" + " {:.2f} &" * len(index)).format(*index).strip(" &")
            # embed()
            plt.close(fig)
        if not isinstance(thresh, float):
            logger.warning("Threshold not a float, should look at this..")
        return (0, thresh, slice_res.flatten())
    # sliced += 1
    # if sliced % 1000 == 0:
    #    print(sliced, 'took ', time.time() - starttime, ' seconds')


def extract_stats(totstats, style):
    df = totstats.copy()
    lines = totstats.columns.get_level_values("line")
    stats = totstats.columns.get_level_values("stat")
    columns = []
    for ii, (line, stat) in enumerate(zip(lines, stats)):
        name = None
        if line != "empty":
            split = line.split("_")
            if len(split) < 3:
                logger.warning("Could not split NN name from target name for {!s}".format(line))
            else:
                name = ("_".join(split[:-2]), "_".join(split[-2:]), stat)
        if name is None:
            name = ("empty" + str(ii), "empty" + str(ii), stat)
        columns.append(name)
    df.columns = pd.MultiIndex.from_tuples(columns)
    df.columns.names = ("nn", "target", "measure")
    df = df.reorder_levels(["measure", "nn", "target"], axis=1)

    results = pd.DataFrame()

    for relabs, measure in product(["rel", "abs", "absabs"], ["thresh", "pop"]):
        df2 = df[measure]
        qlk_data = df2["QLK"]
        network_data = df2.drop("QLK", axis="columns", level="nn")
        if relabs == "rel":
            mis = network_data.subtract(qlk_data, level=1).divide(qlk_data, level=1)
        elif relabs == "abs":
            mis = network_data.subtract(qlk_data, level=1)
        elif relabs == "absabs":
            mis = network_data.subtract(qlk_data, level=1)
            mis = mis.abs()

        quant1 = 0.025
        quant2 = 1 - quant1
        quant = mis.quantile([quant1, quant2])
        results["_".join([measure, relabs, "mis", "median"])] = mis.median()
        results["_".join([measure, relabs, "mis", "mean"])] = mis.mean()
        results["_".join([measure, relabs, "mis", "95width"])] = (
            quant.loc[quant2] - quant.loc[quant1]
        )

        if relabs == "abs":
            results["_".join(["no", measure, "frac"])] = mis.isnull().sum() / len(mis)
    results["wobble_unstab"] = df["wobble_unstab"].mean()
    results["wobble_qlkunstab"] = df["wobble_qlkunstab"].mean()
    results["wobble_tot"] = df["wobble_tot"].mean()

    if style == "duo" or style == "triple":
        # This implementation only works with Karel-style networks in mind. For now, just ignore..
        try:
            duo_results = pd.DataFrame()
            measure = "thresh"
            df2 = df[measure]
            network_data = df2.drop("QLK", axis=1)
            network_data = network_data.reorder_levels([1, 0], axis=1)
            efelike_name = network_data.columns[0][0]
            efilike_name = network_data.columns[1][0]
            if not (efelike_name.startswith("efe") and efilike_name.startswith("efi")):
                raise Exception(
                    "{!s} does not start with efe or {!s} does not start with efi".format(
                        efelike_name, efilike_name
                    )
                )
            mis = network_data[efilike_name] - network_data[efelike_name]
            quant = mis.quantile([quant1, quant2])
            duo_results["dual_thresh_mismatch_median"] = mis.median()
            duo_results["dual_thresh_mismatch_95width"] = quant.loc[quant2] - quant.loc[quant1]
            duo_results["no_dual_thresh_frac"] = mis.isnull().sum() / len(mis)
        except:
            logger.warning("Style is {!s}, but dual-stat extraction failed".format(style))
            duo_results = pd.DataFrame()
    else:
        duo_results = pd.DataFrame()
    return results, duo_results


def extract_nn_stats(results, duo_results, nns, frac, store_name, submit_to_nndb=False):
    try:
        db.connect()
    except (OperationalError, NameError):
        logger.warning("No access to NNDB, aborting NNDB connection!")
        return
    for network_name, res in results.unstack().iterrows():
        network_class, network_number = network_name.split("_")
        nn = nns[network_name]
        res_dict = {"network": network_number}
        res_dict["frac"] = frac
        res_dict["store_name"] = store_name

        for stat, val in res.unstack(level=0).iteritems():
            res_dict[stat] = val.loc[nn._target_names].values

        try:
            duo_res = duo_results.loc[network_name]
            res_dict.update(duo_res)
        except KeyError:
            pass

        __, dim, __ = get_store_params(store_name)
        if dim == 7:
            postprocess_slice = PostprocessSlice(**res_dict)
        elif dim == 9:
            postprocess_slice = PostprocessSlice_9D(**res_dict)

        if submit_to_nndb is True:
            postprocess_slice.save()
    db.close()


def dump_results_to_disk(res, duo_res, frac, store_name, runname="slicestat"):
    res.to_csv(runname + "_results.csv")
    if len(duo_res) != 0:
        duo_res.to_csv(runname + "_duo_results.csv")
    meta = pd.Series({"frac": frac, "store_name": store_name})
    meta.to_csv(runname + "_metadata.csv")


def get_store_params(store_name):
    unstable, set, gen, dim, label, filter = parse_dataset_name(store_name)
    if filter is not None:
        filter = int(filter)
    gen, dim = int(gen), int(dim)
    return gen, dim, filter


def initialize_argument_parser(parser: ArgumentParser) -> ArgumentParser:
    parser.description = """
Slice  QLKNN datasets and collect stats of QLKNN-style
Neural Networks (NNs). These networks can be stored locally in a
file, or in the Neural Network DataBase (NNDB)
"""
    parser.add_argument(
        "dataset_path", type=Path, help="Path to the to-be sliced pandas HDF5 file"
    )

    parser.add_argument(
        "nn_source",
        type=Path,
        nargs="?",
        help="Source where the NNs will be pulled from. Can be a path to a file,"
        " or the special key 'NNDB' to pull unsliced networks from the NNDB",
    )

    # Add "general arguments"
    parser.add_argument("--verbosity", "-v", default=0, action="count")
    parser.add_argument("--quiet", "-q", action="store_true")

    # Add quickslicer specific arguments
    parser.add_argument(
        "--mode",
        default="debug",
        type=str,
        choices=["quick", "pretty", "debug"],
        help="Runmode. Can be 'debug' to generate plots every slice, 'quick' to"
        " slice everything and produce stats and 'pretty' to generate pretty plots",
    )
    parser.add_argument(
        "--summary-to-disk",
        action="store_true",
        help="Dump CSV with summary statistics to disk",
    )
    parser.add_argument(
        "--totstats-to-disk", action="store_true", help="Dump per-slice stats to disk"
    )
    parser.add_argument(
        "--disk-prefix",
        default="slicestat",
        type=str,
        metavar="name",
        help="Prefix given to on-disk dump files",
    )
    parser.add_argument("--submit-to-nndb", action="store_true", help="Submit statistics to NNDB")
    parser.add_argument(
        "--fraction",
        default=0.05,
        type=float,
        metavar="frac",
        help="Fraction of dataset to slice",
    )
    parser.add_argument(
        "--parallel",
        action="store_true",
        help="Slice networks in parallel, spreading the dataset over all cores."
        " Overwrites any smart 'thinking for you' KLP implemented",
    )
    parser.add_argument(
        "--gb-scale",
        default=1,
        type=float,
        metavar="scale",
        help="Rescale the length scale of GyroBohm fluxes in dataset",
    )
    parser.add_argument(
        "--slice-targets",
        nargs="+",
        metavar="targets",
        help="Space-separated list of slice target variables. Autogenerated"
        " from nns in nn_source if not given",
    )
    parser.add_argument(
        "--slice-dim",
        help="Dimension to be sliced osdver. Autogenerated if not given",
    )
    parser.add_argument(
        "--thresh-method",
        default=["2"],
        nargs="+",
        metavar="nums",
        help="Comma seperated list of method index used to determine threshold."
        " First one in the list is used for further calculations. Special value"
        " 'all' calculates all styles of thresholds, using 2 for further calculation",
    )
    parser.add_argument(
        "--myslice",
        type=str,
        default="{}",
        metavar="string",
        help="JSON string with {'input name': value}. Fill be used to constain"
        "the sliced space [default: unconstrained]",
    )
    parser.add_argument(
        "--force-safe", action="store_true", help="Force safe mode. Will be slow!"
    )
    parser.add_argument(
        "--dump-slice-input",
        action="store_true",
        help="Dump a HDF5 with the sliced inputs to disk",
    )
    parser.add_argument(
        "--dump-slice-output",
        action="store_true",
        help="Dump a HDF5 with the sliced outputs to disk",
    )
    parser.add_argument("--no-shuffle", action="store_true", help="Do not shuffle data")
    parser.set_defaults(func=main)
    return parser


def main(namespace: Optional[Namespace] = None):
    """ Main Quickslicer CLI entry point """
    # multiprocess parallelism uses globals to share state. Probably can be done safer, but this is simple and fast
    global slicedim, df, style, col_names_loc, col_names, nns  # Yes I use globals, deal with it

    if not namespace:
        parser = argparse.ArgumentParser()
        parser: ArgumentParser = initialize_argument_parser(parser)
        args: Namespace = parser.parse_args()
    else:
        args = namespace
    assert isinstance(args, Namespace)

    if args.verbosity >= 2:
        print("quickslicer received:")
        print(args)
        print()

    # Being quiet trumps all
    if args.quiet:
        logger.setLevel("WARNING")
    elif args.verbosity >= 1:
        logger.setLevel("DEBUG")
    elif args.verbosity >= 2:
        logger.setLevel("TRACE")

    # Parse CLI arguments
    frac = args.fraction
    parallel_forced = args.parallel
    submit_to_nndb = args.submit_to_nndb
    nn_source = args.nn_source  # (Possibly empty) list of strings
    dump_totstats_to_disk = args.totstats_to_disk
    dump_to_disk = args.summary_to_disk
    runname = args.disk_prefix
    GB_scale = args.gb_scale

    if args.thresh_method[0] == "all":
        thresh_methods = ["2", "1", "3"]
    else:
        thresh_methods = args.thresh_method

    slicedim = args.slice_dim

    target_names = args.slice_targets

    # Define a slice from CLI
    # Very simple JSON parser
    slicestr = args.myslice.replace("'", '"')
    myslice = json.loads(slicestr)

    # Define a slice from CLI
    force_safe = args.force_safe

    dump_slice_input_to_disk = args.dump_slice_input
    dump_slice_output_to_disk = args.dump_slice_output

    shuffle = not args.no_shuffle

    # Find on-disk dataset
    store = pd.HDFStore(args.dataset_path, "r")
    if len(store.groups()) < 1:
        raise TypeError(f"{args.dataset_path} is empty, are you sure this is a pd.HDFStore?")
    store_basename = args.dataset_path.name

    # Load to-be-sliced NNs
    if nn_source == "NNDB":
        try:
            __, dim, __ = get_store_params(store_basename)
        except:
            logger.critical(
                "When pulling from NNDB, dataset basename {!s} should be parsable by misc.get_store_params".format(
                    store_basename
                )
            )
            raise
        slicedim_nndb, style, nns = nns_from_NNDB(dim, max=100)
        if slicedim is None:
            slicedim = slicedim_nndb
    elif nn_source is None:
        style = "mono"
        nns = None
    else:
        if not nn_source.is_file():
            raise Exception("'{!s}' does not exist! Cannot load networks".format(nn_source))
        import importlib

        module_path, ext = os.path.splitext(nn_source)
        module_folder, module_name = os.path.split(module_path)
        if module_folder == "":
            module_folder = os.path.abspath(".")
        sys.path.insert(0, module_folder)
        logger.debug(
            "Temporarly added {!s} to path, trying to load module {!s}".format(
                sys.path[0], module_name
            )
        )
        nn_source_module = importlib.import_module(module_name)
        nns = nn_source_module.nns
        if slicedim is None:
            slicedim = nn_source_module.slicedim
        style = nn_source_module.style
        sys.path.remove(module_folder)

    if nns is not None:
        nn0 = list(nns.values())[0]
        feature_names = nn0._feature_names
        if target_names is None:
            target_names = nn0._target_names
    else:
        feature_names = pd.Series(
            name.decode("UTF-8") for name in store.get_node("input").axis0.read()
        )
        if target_names is None:
            raise Exception("Please pass --slice-targets when slicing without NNs")
        if slicedim is None:
            driving_gradient_list = determine_driving_gradients("_dummy_".join(target_names))
            if len(driving_gradient_list) >= 1:
                driving_gradient = driving_gradient_list[0]  # Just take the first gradient
                if driving_gradient == "Ate" and "Ate" in list(feature_names):
                    slicedim = "Ate"
                elif driving_gradient == "Ate" and "At" in list(feature_names):
                    slicedim = "At"
                elif driving_gradient == "Ati" and "Ati" in list(feature_names):
                    slicedim = "Ati"
                elif driving_gradient == "Ati" and "Ati" in list(feature_names):
                    slicedim = "At"
                else:
                    raise Exception(
                        "Could not auto-determine --slice-dim for {!s} with driving gradient {!s}. Please pass it explicitly".format(
                            target_names, driving_gradient
                        )
                    )
            else:
                raise Exception(
                    "{!s} is not pure ion or electron mode. Please pass --slice-dim explicitly".format(
                        target_names
                    )
                )
    logger.info(
        "Determined target_names={!s}, feature_names={!s}, slicedim={!s}".format(
            list(target_names), list(feature_names), slicedim
        )
    )

    # Set up some auto-generated options
    if style != "similar":
        labels = True
    else:
        labels = False

    if args.mode == "quick":
        clip = False
        filter_geq = None
        filter_less = None
    else:
        clip = True
        filter_geq = -120
        filter_less = 120

    # Prepare the dataset: fold into slices and re-order in NN order if necessary
    # Returns the folded dataset
    df = prep_df(
        store,
        feature_names,
        target_names,
        slicedim,
        filter_less=filter_less,
        filter_geq=filter_geq,
        myslice=myslice,
        frac=frac,
        GB_scale=GB_scale,
        shuffle=shuffle,
    )
    gc.collect()
    # Check if the dataset is indeed in the same order as _all_ the nns feature names.
    # If not, will need some special handling
    if nns is not None:
        is_same_order = check_if_same_order(df, nns, slicedim)
    else:
        is_same_order = True
    if not is_same_order:
        logger.warning(
            "Networks and dataset have features in a different order! Forcing safe mode!"
        )
        safe = True
    else:
        safe = False

    if force_safe:
        if safe:
            logger.warning("Networks seem to support unsafe mode, but safe forced. Will be slow!")
        safe = True

    # Slicing is usually done in 'unsafe' mode. e.g. the order of the input, and order of the
    # features are assumed to be aligned and assumed to be numpy arrays
    if safe:
        logger.warning(
            "Safe mode is experimental! Provide networks that can run in unsafe mode please"
        )

    settings = mode_to_settings(args.mode)

    thresh_method = thresh_methods[0]
    for method in thresh_methods:
        settings["calc_thresh" + method] = True

    if args.mode == "pretty":
        logger.info("Trying to load pretty names, fonts and styles")
        plt.style.use("./thesis.mplstyle")
        mpl.rcParams.update({"font.size": 16})
    else:
        if hasattr(target_names, "index") and hasattr(target_names.index, "names"):
            target_names_list = target_names.index.names
        else:
            target_names_list = list(target_names)
        nameconvert = {
            name: name for name in df.columns.names + df.index.names + target_names_list
        }

    # Thresholds only calculated on first target name
    if len(target_names) > 1 and len(thresh_methods) != 0:
        logger.warning("Thresholds are only calculated on the first target name")

    column_map, col_names = map_column_name_to_index_map(df, nns)
    col_names_loc = col_names

    # Try to determine if we want to run in parallel. Plotting in parallel is not a good idea
    # so 'debug' mode and 'pretty' mode try to run serially. quick mode tries to be parallel
    running_parallel = (settings["parallel"] and parallel_forced is None) or (
        parallel_forced is True
    )
    if running_parallel:
        num_processes = cpu_count()
        chunk_size = int(df.shape[0] / num_processes)
        if chunk_size == 0:
            print("Chunk size is smaller than one, clipping to one")
            chunk_size = 1
        chunks = [df.loc[df.index[i : i + chunk_size]] for i in range(0, df.shape[0], chunk_size)]
        pool = Pool(processes=num_processes)
        logger.info("Using {:d} processes".format(num_processes))
    else:
        logger.info("Running in serial mode")

    if nns is not None:
        logger.info("Starting {:d} slices for {:d} networks".format(len(df), len(nns)))
    else:
        logger.info("Starting {:d} slices without networks".format(len(df)))
    starttime = time.time()

    if not running_parallel:
        results = [
            process_chunk(target_names, df, settings=settings, safe=safe, column_map=column_map)
        ]
    else:
        results = pool.map(
            partial(
                process_chunk,
                target_names,
                settings=settings,
                safe=safe,
                column_map=column_map,
            ),
            chunks,
        )

    logger.info("{!s} took {!s} seconds".format(len(df), time.time() - starttime))

    zero_slices = 0
    totstats = []
    qlk_thresh = []
    index = []
    # This loops over each _row_
    for islice, result in enumerate(chain(*results)):
        if result[0] == 1:
            zero_slices += 1
        else:
            totstats.append(result[2])
            qlk_thresh.append(result[1])
            index.append(islice)

    stats = ["thresh", "pop", "wobble_tot", "wobble_unstab", "wobble_qlkunstab"]
    if nns is None:
        totstats = pd.DataFrame(
            totstats,
            index=index,
            columns=pd.MultiIndex.from_tuples(list(product(["dummy"], stats))),
        )
        totstats.columns.names = ("line", "stat")
    else:
        totstats = pd.DataFrame(
            totstats,
            index=index,
            columns=pd.MultiIndex.from_tuples(list(product(col_names, stats))),
        )
        totstats.columns.names = ("line", "stat")

    qlk_columns = list(one + "_" + two for one, two in product(["QLK"], target_names))
    qlk_data = np.full([len(totstats), len(qlk_columns) * len(stats)], np.nan)
    qlk_data[:, 0] = qlk_thresh  # Assume the first column is thresh;)
    qlk_data = pd.DataFrame(
        qlk_data, index=index, columns=pd.MultiIndex.from_product([qlk_columns, stats])
    )
    qlk_data.columns.names = ("line", "stat")

    totstats = totstats.join(qlk_data)

    totstats_filename = runname + "_totstats.h5.1"
    if dump_totstats_to_disk:
        print('Writing totstats to "{!s}"'.format(totstats_filename))
        totstats.to_hdf(totstats_filename, "stats", format="table", complevel=1)

    res, duo_res = extract_stats(totstats, style)
    res.index.names = ["network_label", "target_names"]
    if len(duo_res) != 0:
        duo_res.index.names = ["network_label", "target_names"]

    # dump to disk
    if dump_to_disk:
        dump_results_to_disk(res, duo_res, frac, store_basename, runname=runname)

    if nns is not None:
        try:
            extract_nn_stats(
                res, duo_res, nns, frac, store_basename, submit_to_nndb=submit_to_nndb
            )
        except:
            logger.warning("Could not extract NNDB stats")

    if dump_slice_input_to_disk:
        print('Writing slice inputs to "{!s}"'.format(totstats_filename))
        inp = df.index.to_frame(index=False)
        inp.to_hdf(totstats_filename, "input", format="table", complevel=1)

    if dump_slice_output_to_disk:
        # This will be numbered per slice, e.g. index 0 for 0th slice
        outp = df.reset_index(drop=True)
        outp = outp.stack().reset_index(-1)
        outp.to_hdf(totstats_filename, "output", format="table", complevel=1)


if __name__ == "__main__":
    main()
