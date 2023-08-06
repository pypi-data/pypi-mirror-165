import time
import gc
import os
import logging
import warnings
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import xarray as xr
from IPython import embed
from qualikiz_tools.qualikiz_io.outputfiles import xarray_to_pandas, qualikiz_folder_to_xarray

from qlknn.misc.tools import dump_package_versions
from qlknn.dataset.data_io import save_to_store, load_from_store
from qlknn.dataset.filtering import (
    create_divsum,
    sanity_filter,
    generate_test_train_index,
    split_test_train,
    stability_filter,
    div_filter,
    temperature_gradient_breakdown_filter,
)
from qlknn.dataset.hypercube_to_pandas import (
    open_with_disk_chunks,
    save_prepared_ds,
    remove_rotation,
    dummy_var,
    absambi,
    determine_stability,
)
from qlknn.dataset.filter_archive.megarun_one_to_pandas import prep_megarun_ds

root_logger = logging.getLogger("qlknn")
logger = root_logger
logger.setLevel(logging.INFO)

qlk_logger = logging.getLogger("qualikiz_tools")
qlk_logger.setLevel(logging.INFO)

try:
    import dask.dataframe as dd

    has_dask = True
except ModuleNotFoundError:
    logger.warning("No dask installed, falling back to xarray")

if __name__ == "__main__":
    dump_package_versions()
    # div_bounds = {
    #     "efeITG_GB_div_efiITG_GB": (0.05, 2.5),
    #     "pfeITG_GB_div_efiITG_GB": (0.02, 0.6),
    #     "efiTEM_GB_div_efeTEM_GB": (0.05, 2.0),
    #     "pfeTEM_GB_div_efeTEM_GB": (0.03, 0.8),
    # }

    dim = 7
    gen = 5
    # filter_num==0: Camille project final version
    # filter_num==1: Camille project final version without gradient breakdown
    filter_num = 1
    apply_breakdown_filter = False

    iden = "pedformreg8"
    rootdir = Path(".").absolute()
    try_use_cache = True
    basename = f"gen{gen}_{dim}D_{iden}_filter{filter_num}"
    suffix = ".h5.1"
    store_name = f"{basename}{suffix}"
    main_store_path = Path(f"{rootdir}{store_name}")

    pre_prepared_ds_name = Path("folded_netcdf.nc")
    prepared_ds_name = Path("prepared_netcdf.nc")
    pre_prepared_ds_path = rootdir / pre_prepared_ds_name
    prepared_ds_path = rootdir / prepared_ds_name

    starttime = time.time()

    # Determine where in the pipeline we need to start
    use_cache = False
    if try_use_cache:
        logger.info("User requested to use cache, finding files")
        if prepared_ds_path.exists():
            logger.info(
                f"Prepared dataset '{prepared_ds_path}' exists, opening with disk chunks as cache"
            )
            ds, ds_kwargs = open_with_disk_chunks(prepared_ds_path, dask=False)
            use_cache = True
        elif Path(main_store_path).exists():
            logger.info(
                f"Pandaized main_store_path='{main_store_path}' exists, skipping pandaization"
            )
            use_cache = True
        else:
            logger.info(
                f"Using cache requested, but '{main_store_path}' and '{prepared_ds_path} do not exist. Not using cache!"
            )
            use_cache = False

    if not use_cache or not prepared_ds_path.exists():
        # Do some prep in front
        logger.info("Preparing dataset '%s' from '%s'", prepared_ds_path, pre_prepared_ds_path)

        def load_folded_ds(rootdir=".", dask=False):
            """tmp function to load the dataset with extra parameters if needed"""
            ds, ds_kwargs = open_with_disk_chunks(pre_prepared_ds_path, dask=dask)
            return ds, ds_kwargs

        # This does many functions automagically
        ds, ds_kwargs = prep_megarun_ds(
            str(prepared_ds_name),
            starttime=starttime,
            rootdir=rootdir,
            ds_loader=load_folded_ds,
            save_grow_ds=True,
            sep_grow_ds=False,
        )
        # Dims are now (Ate, Nustar, q, smag, Ati, An, dilution)

        # We are not using rotation
        ds = remove_rotation(ds)

        # Create new "dimx" variable to keep track of what's what
        # This dimx will be used for all HDF5 files and further derived files
        ds["dimx"] = (
            ds[dummy_var].dims,
            np.arange(0, ds[dummy_var].size).reshape(ds[dummy_var].shape),
        )

        logger.info("Saving prepared dataset to '%s'", prepared_ds_path)
        save_prepared_ds(ds, prepared_ds_path, starttime=starttime, ds_kwargs=ds_kwargs)
        logger.info("Saving prepared dataset done")

    if not main_store_path.exists():
        logger.info("Preparing dataset '%s' from '%s'", main_store_path, prepared_ds_path)
        _ndims_vars = ["gam_GB", "ome_GB"]
        # _not_needed_vars = list(set(ds.data_vars) - set(["efiITG_GB", "efeITG_GB", "dimx"]))
        _not_needed_vars = []
        ds = ds.drop_vars(_ndims_vars + _not_needed_vars)

        logger.info("Loading xr.Dataset('%s') in memory", prepared_ds_path)
        ds.load()
        logger.info("Converting to pandas")
        pandas_all: dict = xarray_to_pandas(ds)

        # The QLKNN-hyper-PoP2020 order is:
        # Zeff, Ati, Ate, An, q, smag, x, Ti_Te, logNustar, gammaE, Te
        # More or less copy that here
        _as_folded = ("Ati", "Ate", "An", "q", "smag", "dilution", "Nustar")
        _features = ["dilution", "Ati", "Ate", "An", "q", "smag", "Nustar"]
        data: pd.DataFrame = pandas_all[_as_folded]
        assert set(data.index.names) == set(
            _features
        ), "Features not equal to prepared dataset index"

        # Make everthing very column-y to make it easier to understand
        # Both the input set and output set are now inside "data"
        data.reset_index(inplace=True)
        data.set_index("dimx", inplace=True)
        # Split into input variables and output variables
        # This makes a copy of the data!
        inp = data.loc[:, _features]
        _non_features = [col for col in data.columns if col not in _features]
        outp = data.loc[:, _non_features]

        # Here we save our "master" pandas file. All easier from here on out!
        logger.info("Saving training data to store '%s'", main_store_path)
        save_to_store(inp, outp, pandas_all["constants"], str(main_store_path), style="sep")
        # Remove all temp variables. Hacky workaround for ugly scoping
        del data, inp, outp, pandas_all
        gc.collect()

    #####################################
    # Preparation done; start filtering #
    #####################################
    # Reload from disk to prevent memory leaks
    logger.info(f"(Re)loading %s from disk", main_store_path)
    input, data, const = load_from_store(main_store_path)

    # Create divsum early to save us some duplication later
    logger.info("Creating divsum")
    create_divsum(data)
    with warnings.catch_warnings():
        data = sanity_filter(
            data,
            septot_factor=1.5,
            ambi_bound=1.5,
            femto_bound=1e-4,  # (everything under this value will be clipped to 0)
            startlen=len(data),
        )

    data.reset_index(inplace=True)  # Check if we need this
    data_columns = list(data)
    for col in data_columns:
        if isinstance(data[col][0], np.float64):
            data[col] = data[col].astype("float32")

    if apply_breakdown_filter:
        # Add At to the input for the temperature gradient breakdown filter
        logger.info("Creating tgb_filter_input")

        # Split the data into smaller datasets to avoid memory error when filtering with temperature gradient breakdown
        logger.info("Creating data_split")
        data_split = [
            data.iloc[:1000000, :],
            data.iloc[1000001:2000000, :],
            data.iloc[2000001:3000000, :],
            data.iloc[3000001:4000000, :],
            data.iloc[4000001:5000000, :],
            data.iloc[5000001:6000000, :],
            data.iloc[6000001:7000000, :],
            data.iloc[7000001:8000000, :],
            data.iloc[8000001:9000000, :],
            data.iloc[10000001:11000000, :],
            data.iloc[11000001:12000000, :],
            data.iloc[12000001:13000000, :],
            data.iloc[13000001:14000000, :],
            data.iloc[14000001:15000000, :],
            data.iloc[15000001:16000000, :],
            data.iloc[16000001:17000000, :],
            data.iloc[17000001:18000000, :],
            data.iloc[18000001:, :],
        ]

        logger.info("Creating tgb_filter_input_split")
        tgb_filter_input_split = [
            tgb_filter_input.iloc[:1000000, :],
            tgb_filter_input.iloc[1000001:2000000, :],
            tgb_filter_input.iloc[2000001:3000000, :],
            tgb_filter_input.iloc[3000001:4000000, :],
            tgb_filter_input.iloc[4000001:5000000, :],
            tgb_filter_input.iloc[5000001:6000000, :],
            tgb_filter_input.iloc[6000001:7000000, :],
            tgb_filter_input.iloc[7000001:8000000, :],
            tgb_filter_input.iloc[8000001:9000000, :],
            tgb_filter_input.iloc[10000001:11000000, :],
            tgb_filter_input.iloc[11000001:12000000, :],
            tgb_filter_input.iloc[12000001:13000000, :],
            tgb_filter_input.iloc[13000001:14000000, :],
            tgb_filter_input.iloc[14000001:15000000, :],
            tgb_filter_input.iloc[15000001:16000000, :],
            tgb_filter_input.iloc[16000001:17000000, :],
            tgb_filter_input.iloc[17000001:18000000, :],
            tgb_filter_input.iloc[18000001:, :],
        ]

        for i in range(len(data_split)):
            logger.info(f"temperature_gradient_breakdown_filter {i+1}/{len(data_split)}")
            # Determine indexes of fluxes to drop because QuaLiKiz breaks down at high gradients.)
            data_split[i] = temperature_gradient_breakdown_filter(
                tgb_filter_input_split[i], data_split[i], "ITG", patience=6
            )
            data_split[i] = temperature_gradient_breakdown_filter(
                tgb_filter_input_split[i], data_split[i], "TEM", patience=6
            )
            data_split[i] = temperature_gradient_breakdown_filter(
                tgb_filter_input_split[i], data_split[i], "ETG", patience=6
            )

        data = pd.concat(data_split)

    # # Calculate At and add it to an input used for tgb_filter
    # tgb_filter_input = input
    # tgb_filter_input = determine_At(data, tgb_filter_input)
    #
    # # Determine indexes of fluxes to drop because QuaLiKiz breaks down at high gradients.
    # data = temperature_gradient_breakdown_filter(tgb_filter_input, data, "ITG", patience=6)
    # data = temperature_gradient_breakdown_filter(tgb_filter_input, data, "TEM", patience=6)
    # data = temperature_gradient_breakdown_filter(tgb_filter_input, data, "ETG", patience=6)

    logger.info("Filtering done, garbage collecting and saving to disk")
    gc.collect()
    input = input.loc[data.index]
    filter_name = basename
    sane_store_name = rootdir / f"sane_{basename}.h5.1"
    save_to_store(input, data, const, str(sane_store_name))
    logger.info("Filtering dataset done. Moving onto sub-datasets")

    stable_pts = 0
    for index, row in data.iterrows():
        if not (row["ETG"]) and not (row["ITG"]) and not (row["TEM"]):
            stable_pts += 1
    logger.info("Stable points: %s%%", 100 * stable_pts / len(data))

    logger.info("Splitting dataset in test-train")
    generate_test_train_index(input, data, const)
    split_test_train(input, data, const, filter_name, rootdir=rootdir)
    del data, input, const
    gc.collect()

    for set in ["test", "training"]:
        logger.info("Working on dim=%s, set=%s", dim, set)
        basename = "".join(
            [
                set,
                "_gen",
                str(gen),
                "_",
                str(dim),
                "D_",
                iden,
                "_filter",
                str(filter_num),
                ".h5.1",
            ]
        )
        input, data, const = load_from_store(os.path.join(rootdir, basename))

        stable_pts = 0
        itg_pts = 0
        tem_pts = 0
        etg_pts = 0
        etg_itg_pts = 0
        etg_tem_pts = 0
        itg_tem_pts = 0
        itg_tem_etg_pts = 0
        for index, row in data.iterrows():
            if not (row["ETG"]) and not (row["ITG"]) and not (row["TEM"]):
                stable_pts += 1
            elif not (row["ETG"]) and (row["ITG"]) and not (row["TEM"]):
                itg_pts += 1
            elif not (row["ETG"]) and not (row["ITG"]) and (row["TEM"]):
                tem_pts += 1
            elif (row["ETG"]) and not (row["ITG"]) and not (row["TEM"]):
                etg_pts += 1
            elif (row["ETG"]) and (row["ITG"]) and not (row["TEM"]):
                etg_itg_pts += 1
            elif (row["ETG"]) and not (row["ITG"]) and (row["TEM"]):
                etg_tem_pts += 1
            elif not (row["ETG"]) and (row["ITG"]) and (row["TEM"]):
                itg_tem_pts += 1
            else:
                itg_tem_etg_pts += 1

        logger.info("Total rows: %s", len(data))
        logger.info("Stable points: %s%%", 100 * stable_pts / len(data))
        logger.info("ITG unstable points: %s%%", 100 * itg_pts / len(data))
        logger.info("ETG unstable points: %s%%", 100 * etg_pts / len(data))
        logger.info("TEM unstable points: %s%%", 100 * tem_pts / len(data))
        logger.info("ITG-ETG unstable points: %s%%", 100 * etg_itg_pts / len(data))
        logger.info("ETG-TEM unstable points: %s%%", 100 * etg_tem_pts / len(data))
        logger.info("ITG-TEM unstable points: %s%%", 100 * itg_tem_pts / len(data))
        logger.info("Completely unstable points: %s%%", 100 * itg_tem_etg_pts / len(data))

        data = stability_filter(data)
        # data = div_filter(data, div_bounds)
        save_to_store(input, data, const, os.path.join(rootdir, "unstable_" + basename))

    logger.info("Filter script done")
