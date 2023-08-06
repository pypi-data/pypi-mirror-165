import time
from itertools import product
import gc
import os
import copy
import shutil
import logging

import numpy as np
import xarray as xr
import pandas as pd

# from dask.distributed import Client, get_client
parquet_engine = "pyarrow"

root_logger = logging.getLogger("qlknn")
logger = root_logger
logger.setLevel(logging.INFO)

try:
    ModuleNotFoundError
except NameError:
    ModuleNotFoundError = ImportError
try:
    from dask.diagnostics import visualize, ProgressBar
    from dask.diagnostics import Profiler, ResourceProfiler, CacheProfiler
    import dask.dataframe as dd
except ModuleNotFoundError:
    logger.warning("No dask installed, falling back to xarray")
from IPython import embed


from qlknn.dataset.data_io import store_format, sep_prefix
from qlknn.misc.analyse_names import is_transport
from qlknn.dataset.filtering import is_mode_scale

try:
    profile
except NameError:
    from qlknn.misc.tools import profile

from qualikiz_tools.qualikiz_io.outputfiles import xarray_to_pandas
from qlknn.misc.tools import notify_task_done

GAM_LEQ_GB_TMP_PATH = "gam_cache.nc"
dummy_var = "efe_GB"


@profile
def metadatize(ds):
    """Move all non-axis dims to metadata"""
    scan_dims = [dim for dim in ds.dims if dim not in ["kthetarhos", "nions", "numsols"]]
    metadata = {}
    for name in ds.coords:
        if all([dim not in scan_dims for dim in ds[name].dims]) and name not in [
            "kthetarhos",
            "nions",
            "numsols",
        ]:
            metadata[name] = ds[name].values
            ds = ds.drop(name)
    ds.attrs.update(metadata)
    return ds


@profile
def absambi(ds):
    """Calculate absambi; ambipolairity check (d(charge)/dt ~ 0)

    Args:
        ds:    Dataset containing pf[i|e]_GB, normni and Zi

    Returns:
        ds:    ds with absambi: sum(pfi * normni * Zi) / pfe
    """
    ds["absambi"] = (ds["pfi_GB"] * ds["normni"] * ds["Zi"]).sum("nions") / ds["pfe_GB"]
    ds["absambi"] = xr.where(ds["pfe_GB"] == 0, 1, ds["absambi"])
    return ds


@profile
def calculate_normni(ds):
    """Calculate ninorm from Zeff and Nex. Assumes two ions"""
    Z0, Z1 = ds["Zi"]
    Zeff = ds["Zeff"]
    ninorm1 = (Zeff - Z0) / (Z1**2 - Z1 * Z0)
    ninorm0 = (1 - Z1 * ninorm1) / Z0
    ds["normni"] = xr.concat([ninorm0, ninorm1], dim="nions")
    return ds


@profile
def calculate_rotdivs(ds, rotdim="Machtor"):
    """Calculate the rotdiv vars

    Rotdiv vars are variables of the form flux_without_rotation
    divided by flux_with_rotation, for example efe_GB_rot0_div_efe_GB
    This is used the train the rotdiv networks.
    """
    for var_name in [col for col in ds.data_vars if is_transport(col)]:
        rotdiv_name = var_name + "_rot0_div_" + var_name
        var = ds[var_name]
        rotdiv = var.sel({rotdim: 0}) / var
        rotdiv = xr.where(var == 0, 0, rotdiv)
        ds[rotdiv_name] = rotdiv
    return ds


@profile
def determine_stability(ds):
    """Determine if a point is TEM or ITG unstable. True if unstable"""
    kthetarhos = ds["kthetarhos"]
    bound_idx = len(kthetarhos[kthetarhos <= 2])
    ome = ds["ome_GB"]

    ome_i = ome.isel(kthetarhos=slice(None, bound_idx))
    ome_e = ome.isel(kthetarhos=slice(bound_idx, None))

    ds["TEM"] = (ome_i > 0).any(dim=["kthetarhos", "numsols"])
    ds["ITG"] = (ome_i < 0).any(dim=["kthetarhos", "numsols"])
    ds["ETG"] = (ome_e > 0).any(dim=["kthetarhos", "numsols"])
    return ds


@profile
def sum_pf(df=None, vt=None, vr=0, vc=None, An=None, R0=None, a=None):
    """Calculate particle flux from diffusivity and pinch"""
    pf = a / R0 * df * An + vt + vr + vc
    return pf


@profile
def sum_pinch(ds):
    """Sum all pinch terms together to va[i|e]_GB"""
    for mode in ["", "ITG", "TEM"]:
        ds["vae" + mode + "_GB"] = ds["vte" + mode + "_GB"] + ds["vce" + mode + "_GB"]
        ds["vai" + mode + "_GB"] = ds["vti" + mode + "_GB"] + ds["vci" + mode + "_GB"]
        if "vri" + mode + "_GB" in ds:
            ds["vai" + mode + "_GB"] += ds["vri" + mode + "_GB"]
        else:
            logger.warning("vri{!s}_GB not found!".format(mode))
    return ds


@profile
def calculate_particle_sepfluxes(ds):
    """Calculate pf[i|e][ITG|TEM] from diffusivity and pinch

    This is needed because of a bug in QuaLiKiz 2.4.0 in which
    pf[i|e][ITG|TEM] was not written to file. Fortunately,
    this can be re-calculated from the saved diffusivity
    and pinch files: df,vt,vc, and vr. Will not do anything
    if already contained in ds.
    """
    for spec, mode in product(["e", "i"], ["ITG", "TEM"]):
        pf_name = "pf" + spec + mode + "_GB"
        if pf_name not in ds:
            fluxes = ["df", "vt", "vc"]
            if spec == "i":
                fluxes.append("vr")
            parts = {flux: flux + spec + mode + "_GB" for flux in fluxes}
            parts = {flux: ds[part] for flux, part in parts.items()}
            if not "R0" in ds.coords:
                logger.warning("R0 not in coords, assuming R0=Ro")
                R0 = ds["Ro"]
            a = ds["Rmin"]
            pf = sum_pf(**parts, An=ds["An"], R0=R0, a=a)
            pf.name = pf_name
            ds[pf.name] = pf
    return ds


@profile
def remove_rotation(ds):
    """Drop the rotation-related variables from dataset"""
    for value in ["vfiTEM_GB", "vfiITG_GB", "vriTEM_GB", "vriITG_GB"]:
        try:
            ds = ds.drop(value)
        except ValueError:
            logger.warning("{!s} already removed".format(value))
    return ds


@profile
def calc_tite(ds):
    """Calculates ion temperature to electron temperature ratio"""
    ds.coords["Ti_Te"] = ds["Ti"] / ds["Te"]
    return ds


@profile
def expand_nions(ds):
    """Expands input variables which are dependent on number of ions"""
    for key in list(ds.coords):
        for item in ds[key].dims:
            if item == "nions":
                for ii in list(ds["nions"].values):
                    nkey = key + "%d" % (ii)
                    ds.coords[nkey] = xr.DataArray(ds[key].values[:, ii], dims=("dimx"))
                ds = ds.drop(key)
    return ds


def open_with_disk_chunks(path, dask=True, one_chunk=False, base_chunk_var="efe_GB"):
    """Determine the on-disk chunk sizes and open dataset

    Best performance in Dask is achieved if the on-disk chunks
    (as saved by xarray) are aligned with the Dask chunks.
    This function assumes all variables are chunked have the
    same on-disk chunks (the xarray default)
    """
    ds = xr.open_dataset(path)
    if dask:
        if base_chunk_var in ds.data_vars:
            chunk_sizes = ds[base_chunk_var]._variable._encoding["chunksizes"]
            dims = ds[base_chunk_var]._variable.dims
        else:
            raise Exception(
                "Could not figure out base chunk sizes, no {!s}".format(base_chunk_var)
            )
        for dim in ds.dims:
            if dim not in dims:
                for var in ds.data_vars.values():
                    if dim in var.dims:
                        idx = var._variable.dims.index(dim)
                        dims += (dim,)
                        chunk_sizes += (var._variable._encoding["chunksizes"][idx],)
                        break
        not_in_dims = set(ds.dims) - set(dims)
        if len(not_in_dims) != 0:
            logger.warning("{!s} not in chunk dims, but are dims of dataset".format(not_in_dims))
        ds.close()

        # Re-open dataset with on-disk chunksizes
        if one_chunk:
            chunks = {dim: length for dim, length in ds.dims.items()}
        else:
            chunks = dict(zip(dims, chunk_sizes))
        ds_kwargs = {
            "chunks": chunks,
            #'cache': True
            #'lock': lock
        }
        ds = xr.open_dataset(path, **ds_kwargs)
    else:
        ds_kwargs = {}
    return ds, ds_kwargs


def gcd(x, y):
    """Euclidian algorithm to find Greatest Common Devisor of two numbers"""
    while y:
        x, y = y, x % y
    return x


def get_dims_chunks(var):
    """Get the current dask chunks of a given variable"""
    if var.chunks is not None:
        if isinstance(var.chunks, dict):
            # xarray-style
            sizes = var.chunks
            chunksizes = [
                sizes[dim][0] if sizes[dim][:-1] == sizes[dim][1:] else None for dim in var.dims
            ]
        if isinstance(var.chunks, tuple):
            # dask-style
            chunksizes = []
            for sizes in var.chunks:
                if sizes[1:] == sizes[:-1]:  # If all are equal
                    chunksizes.append(sizes[0])
                elif np.unique(sizes).size == 2:
                    chunksizes.append(gcd(np.unique(sizes)[0], np.unique(sizes)[1]))
                else:
                    chunksizes.append(reduce(lambda x, y: gcd([x, y]), np.unique(sizes)))
        if None in chunksizes:
            raise Exception("Unequal size for one of the chunks in {!s}".format(var.chunks))
    else:
        logger.warning("No chunks for {!s}".format(var.name))
        chunksizes = None
    return chunksizes


@profile
def calculate_grow_vars(ds):
    """Calculate maxiumum growth-rate based variables"""

    kthetarhos = ds["kthetarhos"]
    bound_idx = len(kthetarhos[kthetarhos <= 2])

    gam = ds["gam_GB"]
    gam = gam.max("numsols")

    gam_leq = gam.isel(kthetarhos=slice(None, bound_idx))
    gam_leq = gam_leq.max("kthetarhos")
    gam_leq.name = "gam_leq_GB"

    if kthetarhos.size > bound_idx:
        gam_great = gam.isel(kthetarhos=slice(bound_idx + 1, None))
        gam_great = gam_great.max("kthetarhos")
        gam_great.name = "gam_great_GB"
    else:
        gam_great = None

    return gam_leq, gam_great


@profile
def merge_gam_leq_great(ds, ds_kwargs=None, rootdir=".", use_disk_cache=False, starttime=None):
    """Calculate and cache (or load from cache) gam_leq and gam_great

    As advised by xarray http://xarray.pydata.org/en/stable/dask.html#optimization-tips
    save gam_leq (which is an intermediate result) to disk.

    Args:
        ds:             xarray.Dataset containing gam_GB

    Kwargs:
        ds_kwargs:      xarray.Dataset kwargs passed to xr.open_dataset. [Default: None]
        rootdir:        Directory where the cache will be saved/is saved
        use_disk_cache: Just load an already cached dataset [Default: False]
        starttime:      Time the script was started. All debug timetraces will be
                        relative to this point. [Default: current time]

    Returns:
        ds:             The xarray.Dataset with gam_leq and gam_great merged in
    """
    if ds_kwargs is None:
        ds_kwargs = {}

    if starttime is None:
        starttime = time.time()

    gam_cache_path = os.path.join(rootdir, GAM_LEQ_GB_TMP_PATH)
    if use_disk_cache and not os.path.isfile(gam_cache_path):
        logger.warning(
            "Use of disk cache requested, but {!s} does not exist. Creating cache!".format(
                gam_cache_path
            )
        )
        use_disk_cache = False
    if not use_disk_cache:
        gam_leq, gam_great = calculate_grow_vars(ds)
        chunksizes = get_dims_chunks(gam_leq)

        # Perserve chunks/encoding from gam_GB
        encoding = {}
        for key in [
            "zlib",
            "shuffle",
            "complevel",
            "dtype",
        ]:
            encoding[key] = ds["gam_GB"].encoding[key]
        if chunksizes is not None:
            encoding["chunksizes"] = chunksizes

        # We assume this fits in RAM, so load before writing to get some extra speed
        gam_leq.load()
        gam_leq.to_netcdf(gam_cache_path, encoding={gam_leq.name: encoding})
        if gam_great is not None:
            gam_great.load()
            gam_great.to_netcdf(gam_cache_path, encoding={gam_great.name: encoding}, mode="a")

    # Now open the cache with the same args as the original dataset, as we
    # aggregated over kthetarhos and numsols, remove them from the chunk list
    kwargs = copy.deepcopy(ds_kwargs)
    if "chunks" in kwargs:
        chunks = kwargs.pop("chunks")
    else:
        chunks = None
    if chunks is not None:
        for key in list(chunks.keys()):
            if key not in gam_leq.dims:
                chunks.pop(key)
    else:
        logger.info("Loading gam cache from disk")
        chunks = None

    # Finally, open and merge the cache
    ds_gam = xr.open_dataset(os.path.join(rootdir, GAM_LEQ_GB_TMP_PATH), chunks=chunks, **kwargs)
    ds = ds.merge(ds_gam.data_vars)
    return ds


def compute_and_save_var(ds, new_ds_path, varname, chunks=None, starttime=None, compress=True):
    """Save a variable from the given dataset in a new dataset
    Args:
        ds:             xarray.Dataset containing gam_GB
        new_ds_path:    The path of the target new dataset (string)
        varname:        Name of the variable to save. Should be in ds.
        chunks:         A dict with the on-disk chunkage per dimention.

    Kwargs:
        starttime:      Time the script was started. All debug timetraces will be
                        relative to this point. [Default: current time]
    """
    if starttime is None:
        starttime = time.time()
    encoding = {}
    if compress:
        encoding = {varname: {"zlib": True}}

    # var = ds[varname]
    if chunks is not None:
        encoding[varname]["chunksizes"] = [chunks[dim] for dim in ds[varname].dims]
    # var.load()
    ds[varname].to_netcdf(new_ds_path, "a", encoding=encoding)
    notify_task_done(varname + " saved", starttime)


@profile
def compute_and_save(ds, new_ds_path, chunks=None, starttime=None):
    """Sequentially load all data_vars in RAM and write to new dataset
    This function forcibly loads variables in RAM, also triggering any
    lazy-loaded dask computations. We thus assume the result of each of
    these calculations fits in RAM. This is done because as of xarray
    '0.10.4', aligning on-disk chunks and dask chunks is still work in
    progress.

    Args:
        ds:          Dataset to write to new dataset
        new_ds_path: Absolute path to of the netCDF4 file that will
                     be generated

    Kwargs:
        chunks:      Dict with the dimension: chunksize for the new ds file
        starttime:   Time the script was started. All debug timetraces will be
                     relative to this point. [Default: current time]
    """
    if starttime is None:
        starttime = time.time()

    new_ds = xr.Dataset()
    new_ds.attrs = ds.attrs
    for coord in ds.coords:
        new_ds.coords[coord] = ds[coord]
    new_ds.to_netcdf(new_ds_path)
    notify_task_done("Coords saving", starttime)

    data_vars = list(ds.data_vars)
    calced_dims = ["gam_leq_GB", "gam_great_GB", "TEM", "ITG", "ETG", "absambi"]
    for spec, mode in product(["e", "i"], ["ITG", "TEM"]):
        flux = "pf"
        calced_dims.append(flux + spec + mode + "_GB")

    for calced_dim in reversed(calced_dims):
        if calced_dim in ds:
            data_vars.insert(0, data_vars.pop(data_vars.index(calced_dim)))

    for ii, varname in enumerate(data_vars):
        logger.info("starting {:2d}/{:2d}: {!s}".format(ii + 1, len(data_vars), varname))
        compute_and_save_var(ds, new_ds_path, varname, chunks, starttime=starttime)


@profile
def save_prepared_ds(ds, prepared_ds_path, starttime=None, ds_kwargs=None):
    """Save a prepared dataset to disk

    Will use dask to write if dataset had 'chuncks', and will do some
    profiling as well. Otherwise, just write with xarray.
    """
    if starttime is None:
        starttime = time.time()

    if ds_kwargs is None:
        ds_kwargs = {}

    if "chunks" in ds_kwargs:
        with Profiler() as prof, ResourceProfiler(dt=0.25) as rprof, CacheProfiler() as cprof:
            compute_and_save(
                ds, prepared_ds_path, chunks=ds_kwargs["chunks"], starttime=starttime
            )
        notify_task_done("prep_megarun", starttime)
        visualize([prof, rprof, cprof], file_path="profile_prep.html", show=False)
    else:
        compute_and_save(ds, prepared_ds_path, starttime=starttime)


@profile
def create_input_cache(ds, cachedir, use_dask=False, overwrite=False):
    """Create on-disk cache of the unfolded hypercube dims

    This function uses the native `xarray.Dataset.to_dataframe()` function
    to unfold the dims in (2D) table format, the classical `pandas.DataFrame`.
    As this operation uses a lot of RAM, we cache the index one-by-one to
    disk, and later glue it together using `input_hdf5_from_cache`. The
    on-disk format is parquet.


    Attrs:
        ds:       The dataset of which the dims/indices will be unfolded
        cachedir: Path where the cache folder should be made. WARNING!
                  OVERRIDES EXISTING FOLDERS!


    """
    # Convert to MultiIndexed DataFrame. Use efe_GB as dummy variable to get the right index
    input_names = list(ds[dummy_var].dims)
    dtype = ds[dummy_var].dtype
    input_df = ds["dimx"].to_dataframe()
    # input_df.drop(input_df.columns[0], axis=1, inplace=True)

    # Create empty cache dir
    if not overwrite and os.path.isdir(cachedir):
        if not all(
            os.path.exists(os.path.join(cachedir, varname + ".parquet"))
            for varname in input_df.index.names
        ):
            logger.info("Input cache dir exists, but cache files missing. Recreating..")
        else:
            logger.info("Input cache already exists, using..")
            return
    if os.path.exists(cachedir):
        shutil.rmtree(cachedir)
    os.mkdir(cachedir)

    # Now unfold the MultiIndex one-by-one
    num_levels = len(input_df.index.levels)
    for ii in range(num_levels):
        input_df.reset_index(level=0, inplace=True)
        varname = input_df.columns[0]
        logger.info(
            "starting to parquet for {:2d}/{:2d}: {!s}".format(ii + 1, num_levels, varname)
        )
        df = input_df[["dimx", varname]].copy(True)
        del input_df[varname]
        df.set_index("dimx", inplace=True)
        df = df.astype({varname: dtype}, copy=False)
        cachefile = os.path.join(cachedir, varname)
        if use_dask:
            ddf = dd.from_pandas(df, npartitions=10)
            ddf.to_parquet(cachefile + ".parquet", write_index=True, engine=parquet_engine)
            del ddf
        else:
            df.to_parquet(cachefile + ".parquet", engine=parquet_engine)
        del df
        gc.collect()


@profile
def input_hdf5_from_cache(
    store_name,
    cachedir,
    columns=None,
    mode="w",
    compress=True,
    store_format="fixed",
    use_dask=False,
):
    """Create HDF5 file using cache from `create_input_cache`

    The contents of cachedir are read into memory, then they are
    concatenated and saved to a single HDF5 file

    Attrs:
        store_name: Name of the HDF5 store/file that will be written to
        cachdir:    Path that will be scanned for cache files

    Kwargs:
        columns:    List of column names to write, pass None for all [Default: None]
        mode:       Mode to be passed to `to_hdf`. Overwrite by
                    default [Default: 'w']
        compress:   Compress the on-disk HDF5 [Default: True]
        store_format: Storage format passed to pandas. Can be 'fixed' or 'table' [Default:'fixed']
        use_dask:   Use dask instead of xarray to write to disk [Default: False]
    """
    panda_kwargs = {}
    if compress:
        panda_kwargs["complib"] = "zlib"
        panda_kwargs["complevel"] = 1
        if not store_name.endswith(".1"):
            logger.warning(
                "Applying compression level 1, but store_name does not end with .1 as is convention"
            )

    files = [os.path.join(cachedir, name) for name in os.listdir(cachedir)]
    ddfs = []
    for name in files:
        logger.info("Reading {!s}".format(name))
        if use_dask:
            ddf = dd.read_parquet(name, engine=parquet_engine)
        else:
            ddf = pd.read_parquet(name, engine=parquet_engine)
        ddfs.append(ddf)
    logger.info("Concatenating files")
    if use_dask:
        input_ddf = dd.concat(ddfs, axis=1)
    else:
        input_ddf = pd.concat(ddfs, axis=1)
    # input_ddf['dimx'] = 1
    # input_ddf['dimx'] = input_ddf['dimx'].cumsum() - 1
    # input_ddf = input_ddf.set_index('dimx', drop=True)
    input_ddf = input_ddf.loc[:, columns]
    logger.info("Writing input to {!s}".format(store_name))
    input_ddf.to_hdf(store_name, "input", format=store_format, mode=mode, **panda_kwargs)


@profile
def data_hdf5_from_ds(ds, store_name, compress=True, store_format="fixed"):
    """Add data_vars from ds to HDF5 file one-by-one

    Attrs:
        ds:         The dataset from which to write the data_vars
        store_name: Name of the HDF5 store/file that will be written to

    Kwargs:
        compress:   Compress the on-disk HDF5 [Default: True]
        store_format: Storage format passed to pandas. Can be 'fixed' or 'table' [Default:'fixed']
    """
    panda_kwargs = {}
    if compress:
        panda_kwargs["complib"] = "zlib"
        panda_kwargs["complevel"] = 1
        if not store_name.endswith(".1"):
            logger.warning(
                "Applying compression level 1, but store_name does not end with .1 as is convention"
            )

    for ii, varname in enumerate(ds.data_vars):
        logger.info(
            "starting to_hdf for {:2d}/{:2d}: {!s}".format(ii + 1, len(ds.data_vars), varname)
        )
        # ddf = ds[[varname]].to_dask_dataframe()
        # da = ds.variables[varname].data
        df = ds[["dimx", varname]].to_dataframe()
        df.reset_index(inplace=True, drop=True)
        df = df.set_index("dimx")
        df.sort_index(inplace=True)
        df.to_hdf(store_name, sep_prefix + varname, format=store_format, **panda_kwargs)
        # da.to_hdf5(store_name, '/output/' + varname, compression=compress)


def save_attrs(attrs, store_name):
    """Save a dictionary to the 'constants' field in the speciefied HDF5 store"""
    store = pd.HDFStore(store_name)
    store["constants"] = pd.Series(attrs)
    store.close()
