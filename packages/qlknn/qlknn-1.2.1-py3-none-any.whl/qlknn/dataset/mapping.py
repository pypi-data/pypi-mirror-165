import numpy as np
import pandas as pd
from IPython import embed

all_inputs = {
    "logNustar": [-5.000294, -3.000294, -2.000294, -1.155196, -0.456226, -0.000294],
    "Ti_Te": [0.25, 0.5, 0.75, 1.0, 1.33, 1.66, 2.5],
    "x": [0.09, 0.21, 0.33, 0.45, 0.57, 0.69, 0.84, 0.99],
    "smag": [-1.0, 0.1, 0.4, 0.7, 1.0, 1.5, 2.0, 2.75, 3.5, 5.0],
    "q": [0.66, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 10.0, 15.0],
    "An": [-5.0, -3.0, -1.0, 1.0e-14, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 6.0],
    "Ate": [1.00e-14, 2.00, 2.75, 3.50, 4.25, 5.00, 5.75, 6.50, 7.25, 8.00, 10.0, 14.0],
    "Ati": [1.00e-14, 2.00, 2.75, 3.50, 4.25, 5.00, 5.75, 6.50, 7.25, 8.00, 10.0, 14.0],
    "Zeff": [1.0, 1.3, 1.7, 2.2, 3.0],
}


def get_ID(inputs):
    """Calculate a Sequence of global IDs from a DataFrame of inputs

    Args:
      - inputs: DataFrame of inputs from 7D or 9D datasets.
          If no Zeff is given it is fixed at 1.0
          If no logNustar and no Nustar are given logNustar is fixed at -3.000294
    """
    if "Zeff" not in inputs:
        inputs["Zeff"] = 1.0
    if "logNustar" not in inputs and "Nustar" not in inputs:
        inputs["logNustar"] = -3.000294
    elif "Nustar" in inputs:
        inputs["logNustar"] = np.log10(inputs["Nustar"])
        inputs = inputs.drop("Nustar", axis=1)

    i = 1
    mul = pd.Series(np.zeros(len(all_inputs)), index=all_inputs.keys())
    all_inputs_df = pd.DataFrame([])
    for inp in all_inputs:
        all_inputs_df = pd.concat([all_inputs_df, pd.DataFrame({inp: all_inputs[inp]})], axis=1)
        mul[inp] = i
        i *= len(all_inputs[inp])

    IDs = pd.DataFrame([], columns=inputs.columns, index=inputs.index)

    for i in all_inputs_df.index:
        IDs[(inputs - all_inputs_df.loc[i, :]).abs() < 0.05] = i

    IDs = (IDs * mul).sum(axis=1).astype(int)

    return IDs
