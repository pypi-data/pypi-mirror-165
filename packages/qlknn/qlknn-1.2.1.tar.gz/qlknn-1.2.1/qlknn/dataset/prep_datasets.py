from qlknn.misc.tools import profile

@profile
def prep_jet_onedpdb_ds(input_ds_name, rootdir=".", use_gam_cache=False):
    """Prepares a QuaLiKiz netCDF4 dataset for convertion to pandas
    This function was designed to use dask, but should work for
    pure xarray too. In this function it is assumed the chunks on disk,
    and the chunks for dask are the same (or at least aligned)

    Kwargs:
        rootdir:        Path where all un-prepared datasets reside [Default: '.']
        use_gam_cache:  Load the already prepared gam_leq/gam_great cache [Default: False]

    Returns:
        ds:             Prepared xarray.Dataset
        ds_kwargs:      Keyword arguments for prepared xarray.Dataset
    """

    starttime = time.time()
    #    prepared_ds_path = os.path.join(rootdir, prepared_ds_name)

    # Load the dataset
    ds, ds_kwargs = open_with_disk_chunks(os.path.join(rootdir, input_ds_name), dask=False)
    notify_task_done("Datasets merging", starttime)
    # Calculate gam_leq and gam_great and cache to disk
    #    ds = merge_gam_leq_great(ds,
    #                             ds_kwargs=ds_kwargs,
    #                             rootdir=rootdir,
    #                             use_disk_cache=use_gam_cache,
    #                             starttime=starttime)
    #    notify_task_done('gam_[leq,great]_GB cache creation', starttime)

    ds.swap_dims({"dimn": "kthetarhos"}, inplace=True)

    ds = determine_stability(ds)
    notify_task_done("[ITG|TEM] calculation", starttime)

    if "normni" not in ds:
        ds = calculate_normni(ds)
    ds = absambi(ds)
    notify_task_done("absambi calculation", starttime)

    #    ds = sum_pinch(ds)
    #    notify_task_done('Total pinch calculation', starttime)

    # Remove variables and coordinates we do not need for NN training
    ds = ds.drop(["gam_GB", "ome_GB"])

    scan_dims = [
        "Nustar",
        "smag",
        "Machtor",
        "Te",
        "q",
        "Zeff",
        "Autor",
        "rho",
        "alpha",
        "ne",
        "x",
        "Ate",
        "Ane",
        "Ani",
        "Ati",
        "normni",
        "Ti",
        "Bo",
        "Ro",
        "Rmin",
        "Aupar",
        "gammaE",
        "Machpar",
        "R0",
        "Ai",
        "Zi",
        "labels",
    ]
    metadata = {}
    for name in ds.coords:
        if all([dim not in scan_dims for dim in ds[name].dims]) and name not in scan_dims:
            metadata[name] = ds[name].values
            ds = ds.drop(name)
    del metadata["phi"]
    del metadata["typei"]
    del metadata["typee"]
    ds.attrs.update(metadata)
    if "labels" in ds.coords:
        ds.reset_coords(["labels"], inplace=True)
    notify_task_done("Bookkeeping", starttime)

    ds = calc_tite(ds)
    #    ds.assign_coords('Ti_Te')
    ds.reset_coords(["Ti", "Te"], inplace=True)
    notify_task_done("Temperature ratio calculation", starttime)

    ds = expand_nions(ds)
    notify_task_done("Ion depedency expansion", starttime)

    for name, var in ds.variables.items():
        if name.endswith("_SI"):
            ds = ds.drop(name)
    notify_task_done("SI data removal", starttime)

    accepted_dims = ["dimx", "nions"]
    for name, var in ds.data_vars.items():
        fdrop = False
        for item in var.dims:
            if item not in accepted_dims:
                fdrop = True
        if fdrop:
            ds = ds.drop(name)
    ds = ds.sel(nions=0)
    ds.reset_coords(["ne"], inplace=True)
    remove_vars = ["Ti_Te1", "Ti_Te2"]
    for var in remove_vars:
        if var in list(ds.variables):
            ds = ds.drop(var)
    notify_task_done("Extra data removal", starttime)

    ds.reset_coords(
        [
            "rho",
            "normni2",
            "Ani2",
            "Ati1",
            "Ati2",
            "Bo",
            "Ro",
            "Rmin",
            "Aupar",
            "Autor",
            "Machpar",
            "R0",
            "Ai0",
            "Ai1",
            "Ai2",
            "Zi0",
            "Zi1",
            "Zi2",
        ],
        inplace=True,
    )
    print(ds.data_vars)

    notify_task_done("Pre-disk write dataset preparation", starttime)
    return ds, ds_kwargs


@profile
def load_rot_three_ds(rootdir="."):
    ds, ds_kwargs = open_with_disk_chunks(os.path.join(rootdir, "rot_three.nc.1"), dask=False)
    return ds, ds_kwargs


def prepare_rot_three(rootdir, use_disk_cache=False):
    starttime = time.time()
    store_name = os.path.join(rootdir, "gen4_8D_rot_three.h5.1")
    prep_ds_name = "rot_three_prepared.nc.1"
    prepared_ds_path = os.path.join(rootdir, prep_ds_name)
    ds_loader = load_rot_three_ds
    if use_disk_cache:
        ds, ds_kwargs = open_with_disk_chunks(prepared_ds_path, dask=False)
    else:
        ds, ds_kwargs = prep_megarun_ds(
            prep_ds_name, starttime=starttime, rootdir=rootdir, ds_loader=ds_loader
        )

        # Drop SI variables
        for name, var in ds.variables.items():
            if name.endswith("_SI"):
                ds = ds.drop(name)

        # Remove ETG vars, rotation run is with kthetarhos <=2
        for name, var in ds.variables.items():
            if "ETG" in name:
                print("Dropping {!s}".format(name))
                ds = ds.drop(name)

        # ds = calculate_rotdivs(ds)
        save_prepared_ds(ds, prepared_ds_path, starttime=starttime, ds_kwargs=ds_kwargs)
    notify_task_done("Preparing dataset", starttime)
    return ds, store_name


if __name__ == "__main__":
    # client = Client(processes=False)
    # client = Client()
    rootdir = "../../../qlk_data"
    ds, store_name = prepare_edge_one(rootdir)
    # ds, store_name = prepare_rot_three(rootdir)
    # ds, store_name = prepare_megarun1(rootdir)

    # Convert to pandas
    # Remove all variables with more dims than our cube
    non_drop_dims = list(ds[dummy_var].dims)
    for name, var in ds.items():
        if len(set(var.dims) - set(non_drop_dims)) != 0:
            ds = ds.drop(name)

    # dummy_var = next(ds.data_vars.keys().__iter__())
    ds["dimx"] = (
        ds[dummy_var].dims,
        np.arange(0, ds[dummy_var].size).reshape(ds[dummy_var].shape),
    )
    use_disk_cache = False
    # use_disk_cache = True
    cachedir = os.path.join(rootdir, "cache")
    if not use_disk_cache:
        create_input_cache(ds, cachedir)

    input_hdf5_from_cache(store_name, cachedir, columns=non_drop_dims, mode="w")
    save_attrs(ds.attrs, store_name)

    data_hdf5_from_ds(ds, store_name)
