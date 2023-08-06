import copy
import unittest
from pathlib import Path
import json

import tensorflow.keras as ke
import pytest
from IPython import embed

from qlknn.training.keras_models import *


def simple_model_from_settings(self):
    # Initialization of local vars
    _feature_names = self._feature_names
    settings = self.settings

    # Use example from FFNN, create a 1-hidden-layer NN
    input_layer = ke.Input(shape=(len(_feature_names),), name="input")

    _layers = [input_layer]

    weight_mask_init = "const_1"
    k_reg = ke.regularizers.l2(0.5 * settings["cost_l2_scale"])
    hidden_layer = ke.layers.Dense(
        settings["hidden_neurons"][0],
        activation=parse_activation(settings["hidden_activation"][0]),
        kernel_initializer=parse_init_string(settings["weight_init"]),
        bias_initializer=parse_init_string(settings["bias_init"]),
        kernel_regularizer=k_reg,
        name="hidden" + str(0),
    )(input_layer)
    _layers.append(hidden_layer)

    # Initialize output layer with normal distribution. Might be worse than not initializing at all
    output_layer = ke.layers.Dense(
        1,
        activation=parse_activation(settings["output_activation"]),
        kernel_initializer=parse_init_string(settings["weight_init"]),
        bias_initializer=parse_init_string(settings["bias_init"]),
        kernel_regularizer=k_reg,
        name="output",
    )(hidden_layer)
    _layers.append(output_layer)

    # Do not subclass model directly, as that has a reduced functionality
    # Instead, initialize a regular Keras model. See
    #
    # compile(optimizer, loss=None, metrics=None, loss_weights=None, sample_weight_mode=None, weighted_metrics=None, target_tensors=None)
    model = ke.Model(inputs=input_layer, outputs=output_layer)
    assert isinstance(model, ke.models.Model)
    self.model = model


class TestQLKNet:
    @pytest.fixture(scope="function")
    def default_qlknet(self, default_settings, qlk_h5_gen5_4D_dataset):
        feature_names = ["Ati", "q", "smag", "Ti_Te"]
        target_names = default_settings["train_dims"]
        ds_path = qlk_h5_gen5_4D_dataset
        with unittest.mock.patch.multiple(
            QLKNet, model_from_settings=simple_model_from_settings, __abstractmethods__=set()
        ):
            nn = QLKNet(
                default_settings,
                feature_names,
                feature_prescale_bias=pd.Series([0, 0, 0, 0], index=feature_names),
                feature_prescale_factor=pd.Series([1, 1, 1, 1], index=feature_names),
                target_prescale_bias=pd.Series([0], index=target_names),
                target_prescale_factor=pd.Series([1], index=target_names),
                train_set=[],
            )
        yield nn

    def test_default_init(self, default_settings):
        target_names = pd.Series(["efiITG_GB"])
        feature_names = ["Ati", "q", "smag", "Ti_Te"]
        settings = copy.deepcopy(default_settings)

        with unittest.mock.patch.multiple(
            QLKNet, model_from_settings=simple_model_from_settings, __abstractmethods__=set()
        ):
            nn = QLKNet(settings, feature_names)

        assert nn._feature_names == feature_names
        echo = nn.echo("Hello world!")
        assert echo == "Hello world!"

    def test__serializable_layer(self, default_qlknet):
        assert default_qlknet._serializable_layer("hidden") is True
        assert default_qlknet._serializable_layer("output") is True
        assert default_qlknet._serializable_layer("anything else") is False

    def test_to_json(self, default_qlknet):
        json_dict = default_qlknet.to_json()
        # Check a few fields
        layer1 = default_qlknet.model.layers[1]
        hidden_activation = layer1.get_config()["activation"]
        assert json_dict["target_names"] == default_qlknet._target_names
        assert json_dict["hidden_activation"][0] == hidden_activation

    def test_save_pretty_json(path, tmpdir, default_qlknet):
        json_name = "nn_test.json"
        json_dict = default_qlknet.to_json()
        with tmpdir.as_cwd():
            default_qlknet.save_pretty_json(json_name, json_dict)
            assert Path(json_name).exists()
            # TODO: Implement model from json and test roundtrip
            with open(json_name) as f_:
                read_json = json.load(f_)
            assert read_json == json_dict

    def test_save_qlknave_pretty_json(self, tmpdir, default_qlknet):
        json_name = "nn_test.json"
        json_dict = default_qlknet.to_json()
        with tmpdir.as_cwd():
            default_qlknet.save_qlknn(json_name)
            assert Path(json_name).exists()
            # TODO: Implement model from json and test roundtrip
            with open(json_name) as f_:
                read_json = json.load(f_)
            assert read_json == json_dict

    def test__check_general_train_sanity(self, default_qlknet):
        default_qlknet._check_general_train_sanity()

    def test__check_general_train_sanity_no_mse(self, default_qlknet):
        default_qlknet.settings["goodness"] = "not mse"
        with pytest.raises(NotImplementedError) as excinfo:
            default_qlknet._check_general_train_sanity()
        assert "Using not mse as goodness" in str(excinfo.value)

    def test__check_general_train_sanity_other_fields(self, default_qlknet):
        default_qlknet.settings["steps_per_report"] = "smth"
        with pytest.raises(NotImplementedError) as excinfo:
            default_qlknet._check_general_train_sanity()
        assert "Training with field steps_per_report" in str(excinfo.value)

        default_qlknet.settings["steps_per_report"] = None
        default_qlknet.settings["epochs_per_report"] = "smth"
        with pytest.raises(NotImplementedError) as excinfo:
            default_qlknet._check_general_train_sanity()
        assert "Training with field epochs_per_report" in str(excinfo.value)

        default_qlknet.settings["epochs_per_report"] = None
        default_qlknet.settings["save_checkpoint_networks"] = "smth"
        with pytest.raises(NotImplementedError) as excinfo:
            default_qlknet._check_general_train_sanity()
        assert "Training with field save_checkpoint_networks" in str(excinfo.value)

        default_qlknet.settings["save_checkpoint_networks"] = None
        default_qlknet.settings["save_best_networks"] = "smth"
        with pytest.raises(NotImplementedError) as excinfo:
            default_qlknet._check_general_train_sanity()
        assert "Training with field save_best_networks" in str(excinfo.value)

        default_qlknet.settings["save_best_networks"] = None
        default_qlknet.settings["track_training_time"] = "smth"
        with pytest.raises(NotImplementedError) as excinfo:
            default_qlknet._check_general_train_sanity()
        assert "Training with field track_training_time" in str(excinfo.value)

    @pytest.fixture
    def datasets(self, qlk_h5_gen5_4D_dataset):
        i_split = int(len(qlk_h5_gen5_4D_dataset.data) * 0.6)
        i_split2 = int(len(qlk_h5_gen5_4D_dataset.data) * 0.8)
        all_data = pd.concat(
            [qlk_h5_gen5_4D_dataset.input, qlk_h5_gen5_4D_dataset.data], axis="columns"
        )
        datasets = {
            "train": all_data.iloc[:i_split, :],
            "validation": all_data.iloc[i_split:i_split2, :],
            "test": all_data.iloc[i_split2:, :],
        }
        yield datasets

    def test__pandas_to_numpy(self, default_qlknet, datasets):
        (inp_train, labels_train, weights_train), (
            inp_val,
            labels_val,
            weights_val,
        ) = default_qlknet._pandas_to_numpy(default_qlknet.settings, datasets)

    def test__pandas_to_generator(self, default_qlknet, datasets):
        (
            train_gen,
            (inp_val, labels_val, weights_val),
            steps_per_epoch,
            validation_batch_size,
        ) = default_qlknet._pandas_to_generator(default_qlknet.settings, datasets)

    def test_train_generator(self, tmpdir, default_qlknet, datasets):
        (
            train_gen,
            validation_data,
            steps_per_epoch,
            validation_batch_size,
        ) = default_qlknet._pandas_to_generator(default_qlknet.settings, datasets)
        with tmpdir.as_cwd():
            default_qlknet.train(
                train_gen,
                validation_data,
                steps_per_epoch=steps_per_epoch,
            )
            assert Path("history.csv").exists()
            assert Path("nn.json").exists()
            assert Path("tf_logs").exists()

    def test_train_generator_labeled(self, tmpdir, default_qlknet, datasets):
        (
            train_gen,
            validation_data,
            steps_per_epoch,
            validation_batch_size,
        ) = default_qlknet._pandas_to_generator(default_qlknet.settings, datasets)
        with tmpdir.as_cwd():
            default_qlknet.train(
                train_gen,
                validation_data,
                steps_per_epoch=steps_per_epoch,
                final_json_name="other_nn.json",
            )
            assert Path("history.csv").exists()
            assert Path("other_nn.json").exists()
            assert Path("tf_logs").exists()


class TestFFNN:
    pass


class TestHornNet:
    pass
