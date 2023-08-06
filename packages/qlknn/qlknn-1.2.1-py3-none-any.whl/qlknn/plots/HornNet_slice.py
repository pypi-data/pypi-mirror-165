# All the imports
import os
import logging
import json
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from qlknn.models.kerasmodel import NDHornNet
from qlknn.dataset.data_io import load_from_store
from qlknn.dataset.mapping import all_inputs, get_ID
from qlknn.misc.analyse_names import determine_mode_scale

from IPython import embed

root_logger = logging.getLogger("qlknn")
logger = root_logger
logger.setLevel(logging.INFO)


def filter_data(data, inputs, x_axis=None):
    if x_axis:
        inputs[x_axis] = all_inputs[x_axis]
    inputs_df = pd.DataFrame(inputs)
    IDs = get_ID(inputs_df)
    return data.loc[data.index.intersection(IDs), :]


if __name__ == "__main__":
    # Loading/Defining all the parameters
    with open("settings_HornNet_slice.json") as file:
        settings = json.load(file)

    path_data = settings["path_data"]
    path_weights = settings["path_weights"]
    path_plot = settings["path_plot"]
    plot_weights = settings["plot_weights"]
    names = settings["names"]
    plot_dims = settings["plot_dims"]
    nn_evaluations = settings["nn_evaluations"]
    x_axis = settings["x_axis"]

    # Loading the data
    if path_data != "/":
        features, labels, _ = load_from_store(path_data, columns=plot_dims)
    else:
        features = pd.DataFrame([], columns=feature_names)
        labels = pd.DataFrame([], columns=plot_dims)
    if plot_weights:
        _, weights, _ = load_from_store(
            path_weights,
            columns=[determine_mode_scale(plot_dims[0]) + "weights"],
            load_input=False,
            load_const=False,
        )

    keep_plotting = True
    data_warning = True
    while keep_plotting:
        if settings["random_inputs"]:
            inputs = {name: random.choice(all_inputs[name]) for name in all_inputs.keys()}
            if "Zeff" not in features and "logNustar" not in features:
                inputs["Zeff"] = 1
                inputs["logNustar"] = -3
                if data_warning:
                    logger.warning(
                        "Data looks like 7D dataset. Fixing Zeff at 1 and logNustar at -3"
                    )
                    data_warning = False
        else:
            inputs = settings["inputs"]
            keep_plotting = False

        prediction_list = []
        targets_list = []
        for i, name in enumerate(names):
            # Load neural network
            path_NN = os.path.join(settings["path_NNs"], name)
            my_NN = NDHornNet(path_NN, GB_scale_length=settings["GB_scale_length_NNs"][i])
            targets_list.append(my_NN._target_names.values)
            feature_names = my_NN._feature_names
            inp = pd.DataFrame(
                np.zeros((settings["nn_evaluations"], len(feature_names))),
                columns=feature_names,
            )
            for feature_name in feature_names:
                if feature_name == x_axis:
                    inp[feature_name] = np.linspace(
                        all_inputs[feature_name][0],
                        all_inputs[feature_name][-1],
                        settings["nn_evaluations"],
                    )
                    x_inputs = inp[feature_name]
                else:
                    inp[feature_name] = inputs[feature_name]

            # Calculating neural network output
            predictions = my_NN.get_output(inp)
            prediction_list.append(predictions)

        # Filtering the data and weights
        features_filtered = filter_data(features, inputs, x_axis)
        features_filtered = features_filtered[x_axis]
        labels_filtered = labels.loc[features_filtered.index]
        weights_filtered = weights.loc[features_filtered.index]

        # Plotting
        fig, ax1 = plt.subplots()
        # plt.rcParams.update({'text.usetex': True})
        colors = ["r", "g", "b", "k", "m", "c"]
        data_symbols = ["x", "+", "*"]
        nn_symbols = ["-", "--", ":", "-."]
        data_labels = settings["data_labels"]
        nn_labels = settings["nn_labels"]

        ax1.spines["top"].set_visible(False)
        ax1.spines["right"].set_visible(False)

        ax1.set_xlabel(settings["xlabel"], fontsize=15)
        ax1.set_ylabel(settings["ylabel"], fontsize=15)

        if settings["xlim"] != []:
            ax1.set_xlim((settings["xlim"][0], settings["xlim"][1]))
        if settings["ylim"] != []:
            ax1.set_ylim((settings["ylim"][0], settings["ylim"][1]))
        if settings["yticks"] != []:
            yticks = np.arange(
                settings["yticks"][0], settings["yticks"][1], settings["yticks"][2]
            )
            ax1.set_yticks(yticks)
            for y in yticks:
                ax1.plot(
                    np.linspace(plt.xlim()[0], plt.xlim()[1], 2),
                    [y] * 2,
                    "--",
                    lw=0.5,
                    color="black",
                    alpha=0.3,
                )

        ax1.tick_params(labelsize=10)

        lns = []

        for i, dim in enumerate(plot_dims):
            lns.append(
                ax1.plot(
                    features_filtered,
                    labels_filtered[dim] / settings["GB_scale_length_data"],
                    data_symbols[i] + colors[i],
                    label="Data: " + data_labels[i],
                )[0]
            )
            for j, predictions in enumerate(prediction_list):
                if dim in targets_list[j]:
                    lns.append(
                        ax1.plot(
                            x_inputs,
                            predictions[dim],
                            nn_symbols[j] + colors[i],
                            label=nn_labels[j] + ": " + data_labels[i],
                        )[0]
                    )
        if plot_weights:
            ax2 = ax1.twinx()
            ax2.set_ylabel("Weights", fontsize=15)
            ax2.tick_params(labelsize=10)
            lns.append(ax2.plot(features_filtered, weights_filtered, "oy", label="Weights")[0])
            ratio = ax1.get_ylim()[0] / ax1.get_ylim()[1]
            ax2.set_ylim((ratio * ax2.get_ylim()[1], ax2.get_ylim()[1]))

        ax1.legend(lns, [l.get_label() for l in lns], fontsize=12)

        del inputs[x_axis]
        ax1.set_title(str(inputs)[1:-1], fontsize=8)

        if settings["save"]:
            plt.savefig(path_plot)
            plt.close()
        else:
            plt.show()
