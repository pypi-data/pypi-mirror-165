import sys
import pandas as pd
from qlknn.dataset.data_io import save_to_store
from IPython import embed


def seperate_7D_from_9D_data(store_9D, store_7D):
    """Extract 7D data from a 9D HDF file by fixing Zeff=1 and logNustar=-3 and write it to another HDF file

    Args:
      - store_9D: Path to 9D HDF trainig data
      - store_7D: Path where to save 7D HDF training data
    """
    store = pd.HDFStore(store_9D, "r")
    const = store["/constants"]
    const["Zeff"] = 1
    const["Nustar"] = 0.000999324

    print("Loading input")
    inp = store["/input"]

    print("Filtering input")
    if "Zeff" in inp:
        inp = inp[(inp.Zeff - 1.0).abs() < 0.1]
        inp = inp.drop("Zeff", axis=1)
    if "logNustar" in inp:
        inp = inp[(inp.logNustar + 3.0).abs() < 0.1]
        inp = inp.drop("logNustar", axis=1)

    output_keys = [x for x in store.keys() if "output" in x]
    print("Number of outputs to filter: " + str(len(output_keys)))
    output = []
    for i, key in enumerate(output_keys, start=1):
        print("Starting with output: " + str(i))
        var = store[key]
        var = var[inp.index]
        output.append(var)
    data = pd.concat(output, axis=1)
    store.close()

    print("Now saving to disk")
    save_to_store(inp, data, const, store_7D)


if __name__ == "__main__":
    store_9D = sys.argv[1]
    store_7D = sys.argv[2]
    seperate_7D_from_9D_data(store_9D, store_7D)
