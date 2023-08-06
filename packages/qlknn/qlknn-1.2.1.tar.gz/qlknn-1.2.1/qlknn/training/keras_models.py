import math
import os
import time
import logging
import json
import sys
import copy

import numpy as np
import pandas as pd
import tensorflow as tf
import tensorflow.keras as ke
from tensorflow.keras import backend as K
from tensorboard.plugins.hparams.api import KerasCallback
from IPython import embed

from qlknn.training.keras_helpers import (
    parse_activation,
    parse_init_string,
    convert_to_generator_like,
    RestoreBest,
    StablePositiveLoss,
    UnstableAwareGoodness,
    TotalLoss,
)
from qlknn.training.nn_primitives import model_to_json_dict
from qlknn.misc.analyse_names import determine_special_input
import abc

root_logger = logging.getLogger("qlknn")
logger = root_logger
logger.setLevel(logging.INFO)


class QLKNet(abc.ABC):
    _layer_save_keywords = ["hidden", "output"]

    def __init__(
        self,
        settings,
        feature_names,
        scale_factor=None,
        scale_bias=None,
        feature_prescale_bias=None,
        feature_prescale_factor=None,
        target_prescale_bias=None,
        target_prescale_factor=None,
        debug=False,
        warm_start_nn=None,
        train_set=None,
    ):
        """Create a FFNN Keras-style model.

        args:
            x:               The input of the FFNN (directly to the input layer)
            num_target_dims: The dimensionality of the output vector
            settings:        The settings dict

        kwargs:
            debug:           Create the network in debug mode. Enables extra
                             debugging options in TensorBoard, but slows down
                             training a lot. [default: False]
            warn_start_nn:   A QuaLiKizNDNN to use the weights and biases from
                             to initialize this FFNN
        """
        # super().__init__(name='QLKNN', dynamic=False)
        self.settings = copy.deepcopy(settings)
        self.debug = debug
        self.warm_start_nn = warm_start_nn

        self._feature_names = feature_names
        self._feature_prescale_bias = feature_prescale_bias
        self._feature_prescale_factor = feature_prescale_factor
        self._target_prescale_bias = target_prescale_bias
        self._target_prescale_factor = target_prescale_factor
        self._train_set = train_set
        for attr in [
            "_feature_prescale_bias",
            "_feature_prescale_factor",
            "_target_prescale_bias",
            "_target_prescale_factor",
            "_train_set",
        ]:
            if getattr(self, attr) is None:
                logger.warning(
                    "{!s} not defined, cannot write this model to QLKNN structure!".format(attr)
                )

        if settings["drop_chance"] != 0:
            raise NotImplementedError("Drop chance != 0")

        self.model_from_settings()
        self.train_style = None
        if self.model.layers[0].name != "input":
            logger.warning(
                "First layer is not input. The first layer will not be written to nn.json!"
            )
        for ii, layer in enumerate(self.model.layers[1:]):
            if not self._serializable_layer(layer.name):
                logger.warning(
                    "Layer {:d}: {!s} will not be written to nn.json!".format(ii, layer.name)
                )

    def echo(self, msg: str):
        """Test function that just echo's the string back"""
        return str(msg)

    def _serializable_layer(self, layer_name):
        return any(word in layer_name for word in self._layer_save_keywords)

    @abc.abstractmethod
    def model_from_settings(self):
        pass

    @property
    def _target_names(self):
        return self.settings["train_dims"]

    def to_json(self):
        trainable = {}
        for ii, layer in enumerate(self.model.layers[1:], start=1):
            # Some metrics generate artificial layers. Ignore those.
            if not self._serializable_layer(layer.name):
                continue
            name = "layer" + str(ii) + "/"
            weight_name = name + "weights/Variable:0"
            bias_name = name + "biases/Variable:0"
            weights = layer.get_weights()
            trainable[weight_name] = weights[0].tolist()
            trainable[bias_name] = weights[1].tolist()

        nn_dict = model_to_json_dict(
            "dummy_name",
            trainable=trainable,
            feature_names=self._feature_names,
            target_names=self._target_names,
            scale_factor=pd.concat([self._feature_prescale_factor, self._target_prescale_factor]),
            scale_bias=pd.concat([self._feature_prescale_bias, self._target_prescale_bias]),
            train_set=self._train_set,
            settings=self.settings,
        )
        return nn_dict

    @staticmethod
    def save_pretty_json(path, dct):
        with open(path, "w") as file_:
            json.dump(dct, file_, indent=4, separators=(",", ": "))

    def save_qlknn(self, path):
        nn_dict = self.to_json()
        self.save_pretty_json(path, nn_dict)

    def _check_general_train_sanity(self):
        settings = self.settings
        if settings["goodness"] != "mse":
            raise NotImplementedError("Using {!s} as goodness".format(settings["goodness"]))
        for field in [
            "steps_per_report",
            "epochs_per_report",
            "save_checkpoint_networks",
            "save_best_networks",
            "track_training_time",
        ]:
            if settings.get(field, None) is not None:
                raise NotImplementedError("Training with field {!s}".format(field))

    def _pandas_to_numpy(self, settings, datasets):
        """Convert a dict of pandas DataFrame to sets of numpy arrays"""
        target_names = settings["train_dims"]
        for name in ["validation", "test"]:
            if not datasets[name].columns.equals(datasets["train"].columns):
                raise Exception("Passed datasets have different columns!")
        feature_names = self._feature_names

        if settings.get("nn_type", "FFNN") == "HornNet":
            # Determine the 'special dimensions' for CMGnets
            special_input = determine_special_input(target_names[0])
            if any(determine_special_input(var) != special_input for var in target_names[1:]):
                logger.warning(
                    "Target {!s} needs a different special input than one of the others targets. Might give weird results".format(
                        target_names[0]
                    )
                )
            if special_input[0] not in feature_names:
                raise Exception("Special input not in dataset")

            # Everything that is not special, is normal
            normal_input = feature_names.copy()
            for dim in special_input:
                normal_input.remove(dim)
            inp_train = [
                datasets["train"].loc[:, normal_input].values,
                datasets["train"].loc[:, special_input].values,
            ]
            inp_val = [
                datasets["validation"].loc[:, normal_input].values,
                datasets["validation"].loc[:, special_input].values,
            ]

            labels_train = datasets["train"].loc[:, target_names].values
            labels_val = datasets["validation"].loc[:, target_names].values

            labels_val = labels_val.T
            labels_val = [train for train in labels_val]
            labels_train = labels_train.T
            labels_train = [train for train in labels_train]
        else:
            inp_train = datasets["train"].loc[:, feature_names].values
            inp_val = datasets["validation"].loc[:, feature_names].values
            labels_train = datasets["train"].loc[:, target_names].values
            labels_val = datasets["validation"].loc[:, target_names].values

        if "weights" in datasets["train"].columns:
            weights_train = datasets["train"].loc[:, "weights"].values
            if settings.get("validation_instance_weighting", False):
                weights_val = datasets["validation"].loc[:, "weights"].values
            else:
                weights_val = None
        else:
            weights_train = None
            weights_val = None

        return (inp_train, labels_train, weights_train), (
            inp_val,
            labels_val,
            weights_val,
        )

    def _pandas_to_generator(self, settings, datasets):
        """Convert a dict of pandas DataFrame to Keras API-style generators"""
        (inp_train, labels_train, weights_train), (
            inp_val,
            labels_val,
            weights_val,
        ) = self._pandas_to_numpy(settings, datasets)

        batch_size = int(math.ceil(len(datasets["train"]) / settings["minibatches"]))
        max_epoch = settings.get("max_epoch") or sys.maxsize
        # Backwards compatibility default
        epochs_per_shuffle = settings.get("epochs_per_shuffle", 1)
        if epochs_per_shuffle == 0:
            shuffle = False
        elif epochs_per_shuffle == 1:
            shuffle = True
        else:
            raise NotImplementedError("Shuffling every {!s} epochs".format(epochs_per_shuffle))

        train_gen, steps_per_epoch = convert_to_generator_like(
            (inp_train, labels_train, weights_train),
            batch_size=batch_size,
            steps_per_epoch=None,
            epochs=max_epoch,
            shuffle=shuffle,
        )

        validation_batches = settings.get("validation_batches", 1)
        if validation_batches == "same_as_training_batch_size":
            validation_batch_size = batch_size
        else:
            validation_batch_size = int(
                math.ceil(len(datasets["validation"]) / validation_batches)
            )

        return (
            train_gen,
            (inp_val, labels_val, weights_val),
            steps_per_epoch,
            validation_batch_size,
        )

    def _prepare_data_for_keras(
        self, settings, datasets, feature_names, goodness_only_on_unstable=True
    ):
        """Convert dataset from old TF1 dataset API to new Keras API"""
        logger.warning("Old TF1 Dataset API no longer supported!")
        # Grab the whole training set batch
        # TODO: Do not load whole set in memory?
        train_data = inp_train, labels_train = datasets.train.next_batch(-1, shuffle=False)
        # Old goodness_only_on_unstable based on weights
        # Might be buggy in Keras! Gave up. See e.g.
        # https://github.com/keras-team/keras/issues/13641
        # if goodness_only_on_unstable:
        #    scale = self._target_prescale_factor[self._target_names].to_numpy()
        #    bias = self._target_prescale_bias[self._target_names].to_numpy()
        #    labels_train_descale = (labels_train - bias) / scale
        #    is_unstab = is_unstable_label(labels_train_descale)
        #    if is_unstab.shape[1] > 1:
        #        logger.warning('Multi-D targets with goodness_only_on_unstable on. Not sure what will and should happen here!')

        #    train_weights = K.switch(is_unstab, K.ones_like(is_unstab, dtype=K.floatx()), K.zeros_like(is_unstab, dtype=K.floatx())).numpy()
        # else:
        train_weights = None

        # Convert train set to generator-like. This seems to happen inside of Keras regardless
        batch_size = int(math.floor(datasets.train.num_examples / settings["minibatches"]))
        max_epoch = settings.get("max_epoch") or sys.maxsize
        # Backwards compatibility default
        epochs_per_shuffle = settings.get("epochs_per_shuffle", 1)
        if epochs_per_shuffle == 0:
            shuffle = False
        elif epochs_per_shuffle == 1:
            shuffle = True
        else:
            raise NotImplementedError("Shuffling every {!s} epochs".format(epochs_per_shuffle))

        inp_train = [
            inp_train.take(normal_inp, axis=1),
            inp_train.take(special_inp, axis=1),
        ]

        train_gen, steps_per_epoch = convert_to_generator_like(
            (inp_train, labels_train, train_weights),
            batch_size=batch_size,
            steps_per_epoch=None,
            epochs=max_epoch,
            shuffle=shuffle,
        )

        # Grab the whole validation batch
        # TODO: Do not load whole set in memory?
        validation_data = inp_val, labels_val = datasets.validation.next_batch(-1, shuffle=False)

        # if goodness_only_on_unstable:
        #    scale = self._target_prescale_factor[self._target_names].to_numpy()
        #    bias = self._target_prescale_bias[self._target_names].to_numpy()
        #    labels_val_descale = (labels_val - bias) / scale
        #    is_unstab = is_unstable_label(labels_val_descale)
        #    if is_unstab.shape[1] > 1:
        #        logger.warning('Multi-D targets with goodness_only_on_unstable on. Not sure what will and should happen here!')

        #    val_weights = K.switch(is_unstab, K.ones_like(is_unstab, dtype=K.floatx()), K.zeros_like(is_unstab, dtype=K.floatx())).numpy()
        # else:
        val_weights = None

        return train_gen, (inp_val, labels_val, val_weights), steps_per_epoch

    def train(
        self,
        train_data,
        validation_data,
        steps_per_epoch=None,
        batch_size=None,
        validation_batch_size=None,
        workers=1,
        verbosity=0,
        final_json_name="nn.json",
    ):
        settings = self.settings
        self._check_general_train_sanity()
        self.train_style = "keras"
        # First have to 'compile' the model
        # See tensorflow_core/python/keras/engine/training.py
        # or https://keras.io/models/model/#compile
        # Set up the optimizer
        if settings["optimizer"] == "adam":
            optimizer = ke.optimizers.Adam(
                learning_rate=settings["learning_rate"],
                beta_1=settings["adam_beta1"],
                beta_2=settings["adam_beta2"],
            )
        elif settings["optimizer"] == "rmsprop":
            optimizer = ke.optimizers.RMSprop(
                learning_rate=settings["learning_rate"],
                rho=settings["rmsprop_decay"],
                momentum=settings["rmsprop_decay"],
            )
        elif settings["optimizer"] == "grad":
            optimizer = ke.optimizers.SGD(
                learning_rate=settings["learning_rate"],
            )
        else:
            raise NotImplementedError("Optimizer {!s}".format(settings["optimizer"]))
        # Compile the model
        # compile(optimizer, loss=None, metrics=None, loss_weights=None, sample_weight_mode=None, weighted_metrics=None, target_tensors=None)
        # Adding stable_positive_loss as both a loss _and_ a metric, somehow borks Keras
        from tensorflow.keras.losses import MeanSquaredError

        if settings["goodness_only_on_unstable"]:
            goodness = UnstableAwareGoodness(
                "mse",
                self._target_prescale_factor,
                self._target_prescale_bias,
            )
        else:
            goodness = MeanSquaredError()

        losses = [goodness]
        loss_weights = [1.0]
        stable_positive_loss = None
        if settings["cost_stable_positive_scale"] != 0:
            stable_positive_loss = StablePositiveLoss(
                settings["cost_stable_positive_scale"],
                settings["cost_stable_positive_offset"],
                settings["cost_stable_positive_function"],
                self._target_prescale_factor,
                self._target_prescale_bias,
            )
            losses.append(stable_positive_loss)
            loss_weights.append(1.0)

        def model_losses(y_true, y_pred):
            return K.sum(self.model.losses)

        total_loss = TotalLoss(losses, loss_weights)
        self.model.compile(
            optimizer=optimizer,
            loss=total_loss,
            metrics=[goodness],
            # metrics = [total_loss, goodness, stable_positive_loss],
            # metrics=[goodness, stable_positive_loss])
            # metrics=[goodness, model_losses, stable_positive_loss],
        )

        path_logs = os.path.join("tf_logs")
        path_model = os.path.join("checkpoints", "{epoch:05d}.ckpt")

        # Save logs for plotting with TensorBoard. See https://www.tensorflow.org/api_docs/python/tf/keras/callbacks/TensorBoard
        write_graph = settings.get("write_graph", False)
        histogram_freq = settings.get("histogram_freq", 0)
        callbacks = [
            ke.callbacks.TensorBoard(
                log_dir=path_logs,
                write_graph=write_graph,
                histogram_freq=histogram_freq,
                profile_batch=2,
            )
        ]
        # ke.callbacks.ModelCheckpoint(path_model, save_freq=num_samples*settings['checkpoint_period'], save_weights_only=True),
        early_stop_measure = "val_" + settings["early_stop_measure"]
        if settings["early_stop_measure"] != "none":
            es = ke.callbacks.EarlyStopping(
                monitor=early_stop_measure,
                min_delta=0.0,
                restore_best_weights=True,
                patience=settings["early_stop_after"],
                verbose=1,
            )
            callbacks.append(es)
        # Still save best model, even after early stopping
        restore_best_measure = "val_" + settings.pop("monitor", "loss")
        rb = RestoreBest(monitor=restore_best_measure, verbose=0)
        callbacks.append(rb)

        if settings.get("track_hyperparams", []) != []:
            hyperparams = {
                hyperparam: settings.get(hyperparam, "")
                for hyperparam in settings["track_hyperparams"]
            }
            for elem in hyperparams:
                if not isinstance(hyperparams[elem], (bool, int, float, str)):
                    hyperparams[elem] = str(hyperparams[elem])
            callbacks.append(KerasCallback(os.path.join(path_logs, "validation"), hyperparams))

        max_epoch = settings.get("max_epoch") or sys.maxsize
        train_start = time.time()
        stop_reason = "undefined"
        print("Start training")
        # Backwards compatibility default
        epochs_per_shuffle = settings.get("epochs_per_shuffle", 1)
        if epochs_per_shuffle == 0:
            shuffle = False
        elif epochs_per_shuffle == 1:
            shuffle = True
        else:
            raise NotImplementedError("Shuffling every {!s} epochs".format(epochs_per_shuffle))

        if settings.get("use_generator", True):
            # As data passed should a generator, do not pass batch_size!
            # If steps_per_epoch is not passed to fit, it gets confused..
            if steps_per_epoch != settings["minibatches"]:
                logger.warning(
                    "Using {:d} steps per epoch instead of the requested {!s} minibatches".format(
                        steps_per_epoch, settings["minibatches"]
                    )
                )

            hist = self.model.fit(
                train_data,
                validation_data=validation_data,
                epochs=max_epoch,
                initial_epoch=0,
                shuffle=shuffle,
                callbacks=callbacks,
                batch_size=batch_size,
                validation_batch_size=validation_batch_size,
                steps_per_epoch=steps_per_epoch,
                verbose=verbosity,
                workers=workers,
                use_multiprocessing=(workers != 1),
            )

        else:
            hist = self.model.fit(
                train_data[0],
                train_data[1],
                sample_weight=train_data[2],
                validation_data=validation_data,
                epochs=max_epoch,
                initial_epoch=0,
                shuffle=shuffle,
                callbacks=callbacks,
                batch_size=batch_size,
                validation_batch_size=validation_batch_size,
                steps_per_epoch=steps_per_epoch,
                verbose=verbosity,
            )

        # Get validation loss again like this, without batch_size will not be identical!!
        # self.model.evaluate(x=inp_val, y=labels_val, batch_size=len(inp_val))

        # Merge history with epochs, and dump to disk
        try:
            df = pd.DataFrame(data={"epoch": hist.epoch})
        except:
            print("Could not initialize history dataframe! Weeeird!")
        else:
            for key, val in hist.history.items():
                try:
                    df[key] = val
                except ValueError:
                    print("Could not add {!s} to history log".format(key))
            df.to_csv("history.csv")

        # Collect some metadata about the training
        # We use the 'first epoch == epoch 0' here, the stats are from _after_ the train step, so after model update
        if hist.epoch[-1] < max_epoch - 1:
            best_epoch = hist.epoch[-1] - self.settings["early_stop_after"]
            stop_reason = "early_stopping"
        else:
            best_epoch = rb.best_epoch - 1  # First epoch == epoch 1 according to RestoreBest
            stop_reason = "max epochs"

        metadata = {
            "epoch": hist.epoch[-1],
            "best_epoch": best_epoch,
            #'l2_loss_validation'     : l2_loss_val,
            #'rms_validation_descaled': rms_val_descale,
            "walltime [s]": time.time() - train_start,
            #'shuffle_time [s]'       : shuffle_time,
            #'shuffle_percentage'     : shuffle_time/cur_train_time.eval(session=sess)*100,
            "stop_reason": stop_reason,
        }

        try:
            if isinstance(goodness, MeanSquaredError) or (
                isinstance(goodness, UnstableAwareGoodness) and goodness.measure == "mse"
            ):
                val_mse = hist.history["val_goodness"][best_epoch]
            else:
                raise Exception("Unknown goodness {!s}".format(goodness))
        except Exception as ee:
            logger.warning(
                'Could not grab val_stable_positive_loss, raised Exception "{!s}"'.format(ee)
            )
        else:
            rms_val = np.sqrt(val_mse)
            metadata["rms_validation"] = rms_val

        try:
            loss_val = hist.history["val_loss"][best_epoch]
        except:
            print("Could not grab val_loss from history! History is:")
            print(hist.history)
        else:
            metadata["loss_validation"] = loss_val

        try:
            if "val_stable_positive_loss" in hist.history:
                y_pred = self.model.predict(validation_data[0])
                y_real = validation_data[1]
                stable_positive_loss_val = hist.history["val_stable_positive_loss"][best_epoch]
            elif stable_positive_loss is not None:
                y_pred = self.model.predict(validation_data[0])
                y_true = validation_data[1]
                stable_positive_loss_val = float(stable_positive_loss(y_true, y_pred).numpy())
            else:
                stable_positive_loss_val = 0
        except Exception as ee:
            logger.warning(
                'Could not grab val_stable_positive_loss, raised Exception "{!s}"'.format(ee)
            )
        else:
            metadata["stable_positive_loss_validation"] = stable_positive_loss_val

        try:
            import socket

            metadata["hostname"] = socket.gethostname()
        except:
            pass

        fmt = "{:" + str(max(len(key) for key in metadata) + 1) + "s}: {!s}"
        for key, val in metadata.items():
            print(fmt.format(key, val))

        dct = {"_metadata": metadata}
        nn_dict = self.to_json()
        dct.update(nn_dict)
        dct["_parsed_settings"] = self.settings
        self.save_pretty_json(final_json_name, dct)

    def get_metric(self, name):
        """Get a metric by name

        Uniqueness of names is not guaranteed. Raise a warning and return the last
        defined metric if a duplicate is found
        """
        if self.train_style is None:
            raise Exception("train_style undefined. Metrics only defined during training")
        elif self.train_style == "tf2":
            returned_metric = None
            for metric in self.metrics:
                if metric.name == name:
                    if returned_metric != None:
                        logger.warning("Multiple metrics with name {!s}".format(name))
                    returned_metric = metric
            if returned_metric is None:
                available = [metric.name for metric in self.metrics]
                raise Exception(
                    'Could not find metric "{!s}", available metrics: {!s}'.format(
                        name, available
                    )
                )
        else:
            raise NotImplementedError(
                "Getting metrics for train style {!s}".format(self.train_style)
            )
        return returned_metric

    def own_train(self, datasets, verbosity=1):
        """Train the TensorFlow 2.0 way"""
        logger.warning(
            "This training loop is experimental, largely untested, and not under development"
        )
        self.train_style = "tf2"
        settings = self.settings
        self._check_general_train_sanity()
        for field in ["histogram_freq", "write_graph"]:
            if settings.get(field, None) is not None:
                logger.warning("{!s} not used".format(field))
        if settings["early_stop_measure"] != "none":
            raise NotImplementedError("Early stopping")

        logdir = "tf_logs"
        train_writer = tf.summary.create_file_writer(os.path.join(logdir, "train"))
        validation_writer = tf.summary.create_file_writer(os.path.join(logdir, "validation"))

        train_loss = tf.keras.metrics.Mean(name="train_loss")
        train_mse = tf.keras.metrics.MeanSquaredError(name="train_mse")

        validation_loss = tf.keras.metrics.Mean(name="validation_loss")
        validation_mse = tf.keras.metrics.MeanSquaredError(name="validation_mse")

        # Copy the Keras Model API kinda
        self.metrics = [train_loss, train_mse, validation_loss, validation_mse]

        self.loss_object = tf.keras.losses.MeanSquaredError()

        self.optimizer = ke.optimizers.Adam(
            lr=settings["learning_rate"],
            beta_1=settings["adam_beta1"],
            beta_2=settings["adam_beta2"],
        )

        max_epoch = settings.get("max_epoch") or sys.maxsize

        # Split dataset in minibatches
        minibatches = settings["minibatches"]
        batch_size = int(math.floor(datasets.train.num_examples / minibatches))

        print("Start training")
        train_start = time.time()
        for epoch in range(max_epoch):
            # Reset the metrics at the start of the next epoch
            for metric in self.metrics:
                metric.reset_states()

            # for images, labels in zip(*datasets.train.next_batch(-1)):
            #    train_step(images, labels)
            for step in range(minibatches):
                xs, ys = datasets.train.next_batch(batch_size, shuffle=True)
                with train_writer.as_default():
                    self.train_step(xs, ys)

            xs, ys = datasets.validation.next_batch(-1, shuffle=False)
            with validation_writer.as_default():
                self.validation_step(xs, ys)

            # for images, labels in zip(*datasets.test.next_batch(-1)):
            #    test_step(test_images, test_labels)

            if verbosity >= 1:
                template = "Epoch {}, Loss: {}, MSE: {}, Validation Loss: {}, Validation MSE: {}"
                print(
                    template.format(
                        epoch + 1,
                        train_loss.result(),
                        train_mse.result(),
                        validation_loss.result(),
                        validation_mse.result(),
                    )
                )

            validation_writer.flush()
            train_writer.flush()
        metadata = {}
        metadata["rms_validation"] = float(math.sqrt(validation_mse.result()))
        metadata["loss_validation"] = float(validation_loss.result())
        dct = {"_metadata": metadata}
        nn_dict = self.to_json()
        dct.update(nn_dict)
        dct["_parsed_settings"] = self.settings
        self.save_pretty_json("nn.json", dct)

    @tf.function
    def train_step(self, images, labels):
        train_loss = self.get_metric("train_loss")
        train_mse = self.get_metric("train_mse")
        model = self.model
        loss_object = self.loss_object
        optimizer = self.optimizer
        with tf.GradientTape() as tape:
            # training=True is only needed if there are layers with different
            # behavior during training versus inference (e.g. Dropout).
            predictions = model(images, training=True)
            loss = loss_object(labels, predictions)
        gradients = tape.gradient(loss, model.trainable_variables)
        optimizer.apply_gradients(zip(gradients, model.trainable_variables))

        train_loss(loss)
        train_mse(labels, predictions)
        tf.summary.scalar("loss", train_loss.result(), step=optimizer.iterations)
        tf.summary.scalar("mse", train_mse.result(), step=optimizer.iterations)

    @tf.function
    def validation_step(self, images, labels):
        model = self.model
        loss_object = self.loss_object
        validation_loss = self.get_metric("validation_loss")
        validation_mse = self.get_metric("validation_mse")
        optimizer = self.optimizer
        # training=False is only needed if there are layers with different
        # behavior during training versus inference (e.g. Dropout).
        predictions = model(images, training=False)
        t_loss = loss_object(labels, predictions)

        validation_loss(t_loss)
        validation_mse(labels, predictions)
        tf.summary.scalar("loss", validation_loss.result(), step=optimizer.iterations)
        tf.summary.scalar("mse", validation_mse.result(), step=optimizer.iterations)


class FFNN(QLKNet):
    def model_from_settings(self):
        settings = self.settings
        feature_names = self._feature_names
        warm_start_nn = self.warm_start_nn
        inputs = ke.Input(shape=(len(feature_names),), name="input")

        # "layer1" in TF is n_inputs x n_hidden_neurons
        # In 3-hidden layer network it is followed by layer2, layer3
        # The "output layer" is layer4 (n_hidden_neurons x n_outputs)
        hidden_layer = inputs
        self._layers = []
        for ii, (activation, neurons) in enumerate(
            zip(settings["hidden_activation"], settings["hidden_neurons"]), start=1
        ):
            if warm_start_nn is None:
                weight_init = settings["weight_init"]
                bias_init = settings["bias_init"]
                weight_mask_init = "const_1"
            else:
                raise NotImplementedError("Warm starting of NN training")

            # Get the activation function for this layer from the settings dict
            # Initialize the network layer. It is autoconnected to the previous one.
            # TODO: Check setting of dtype
            # TODO: Check setting of name
            # TODO: Check setting of weight_mask_init
            # There is a factor 2 between TF1 definition (output = sum(t ** 2) / 2) and
            # Keras definition (K.sum(K.square(x))) of L2 loss
            if settings["cost_l2_scale"] != 0 and settings["cost_l1_scale"] != 0:
                k_reg = ke.regularizers.l1_l2(
                    settings["cost_l1_scale"], 0.5 * settings["cost_l2_scale"]
                )
            elif settings["cost_l2_scale"] != 0:
                k_reg = ke.regularizers.l2(0.5 * settings["cost_l2_scale"])
            elif settings["cost_l1_scale"] != 0:
                k_reg = ke.regularizers.l1(settings["cost_l1_scale"])
            else:
                k_reg = None
            hidden_layer = ke.layers.Dense(
                neurons,
                activation=parse_activation(activation),
                kernel_initializer=parse_init_string(weight_init),
                bias_initializer=parse_init_string(bias_init),
                kernel_regularizer=k_reg,
                name="hidden" + str(ii),
            )(hidden_layer)
            self._layers.append(hidden_layer)
            # setattr(self, 'hidden_layer' + str(ii), hidden_layer)
            # self.num_layers += 1
        # Initialize output layer with normal distribution. Might be worse than not initializing at all
        output_layer = ke.layers.Dense(
            1,
            activation=parse_activation(settings["output_activation"]),
            kernel_initializer=parse_init_string(weight_init),
            bias_initializer=parse_init_string(bias_init),
            kernel_regularizer=k_reg,
            name="output",
        )(hidden_layer)
        self._layers.append(output_layer)

        # Do not subclass model directly, as that has a reduced functionality
        # Instead, initialize a regular Keras model. See
        #
        # compile(optimizer, loss=None, metrics=None, loss_weights=None, sample_weight_mode=None, weighted_metrics=None, target_tensors=None)
        self.model = ke.Model(inputs=inputs, outputs=output_layer)


class HornNet(QLKNet):
    def __init__(
        self,
        settings=None,
        feature_names=None,
        path=None,
        scale_factor=None,
        scale_bias=None,
        feature_prescale_bias=None,
        feature_prescale_factor=None,
        target_prescale_bias=None,
        target_prescale_factor=None,
        debug=False,
        warm_start_nn=None,
        train_set=None,
    ):
        self.debug = debug
        self.warm_start_nn = warm_start_nn

        self._train_set = train_set

        if path:
            self.model_from_json(path)
        elif settings and feature_names:
            self.settings = settings
            self._feature_names = feature_names
            self._feature_prescale_bias = feature_prescale_bias
            self._feature_prescale_factor = feature_prescale_factor
            self._target_prescale_bias = target_prescale_bias
            self._target_prescale_factor = target_prescale_factor
            self.model_from_settings()
        else:
            raise Exception(
                "You have to give either a path from which the NN has to be loaded or settings and feature_names"
            )

        target_names = self.settings["train_dims"]
        self._special_feature = determine_special_input(target_names[0])
        if any(determine_special_input(var) != self._special_feature for var in target_names[1:]):
            logger.warning(
                "Target {!s} needs a different special input than one of the others targets. Might give weird results".format(
                    target_names[0]
                )
            )

        for attr in [
            "_feature_prescale_bias",
            "_feature_prescale_factor",
            "_target_prescale_bias",
            "_target_prescale_factor",
            "_train_set",
        ]:
            if getattr(self, attr) is None:
                logger.warning(
                    "{!s} not defined, cannot write this model to QLKNN structure!".format(attr)
                )

        if self.settings["drop_chance"] != 0:
            raise NotImplementedError("Drop chance != 0")

        self.train_style = None

    def model_from_settings(self):
        settings = self.settings
        feature_names = self._feature_names
        train_dims = settings["train_dims"]
        warm_start_nn = self.warm_start_nn
        if warm_start_nn is None:
            weight_init = settings["weight_init"]
            bias_init = settings["bias_init"]
            weight_mask_init = "const_1"
        else:
            raise NotImplementedError("Warm starting of NN training")

        if settings["cost_l2_scale"] != 0 and settings["cost_l1_scale"] != 0:
            k_reg = ke.regularizers.l1_l2(
                settings["cost_l1_scale"], 0.5 * settings["cost_l2_scale"]
            )
        elif settings["cost_l2_scale"] != 0:
            k_reg = ke.regularizers.l2(0.5 * settings["cost_l2_scale"])
        elif settings["cost_l1_scale"] != 0:
            k_reg = ke.regularizers.l1(settings["cost_l1_scale"])
        else:
            k_reg = None

        if settings["cost_l2_scale_CGM"] != 0 and settings["cost_l1_scale_CGM"] != 0:
            CGM_k_reg = ke.regularizers.l1_l2(
                settings["cost_l1_scale_CGM"], 0.5 * settings["cost_l2_scale_CGM"]
            )
        elif settings["cost_l2_scale_CGM"] != 0:
            CGM_k_reg = ke.regularizers.l2(0.5 * settings["cost_l2_scale_CGM"])
        elif settings["cost_l1_scale_CGM"] != 0:
            CGM_k_reg = ke.regularizers.l1(settings["cost_l1_scale_CGM"])
        else:
            CGM_k_reg = None

        # Inputlayer
        normal_inputs = ke.Input(shape=(len(feature_names) - 1,), name="general_input")
        special_input = ke.Input(shape=(1,), name="seperated_input")

        # Neural network for all constants
        hidden_layer = normal_inputs
        for ii, (activation, neurons) in enumerate(
            zip(settings["common_layers_activation"], settings["common_layers"]),
            start=1,
        ):
            hidden_layer = ke.layers.Dense(
                neurons,
                activation=parse_activation(activation),
                kernel_initializer=parse_init_string(weight_init),
                bias_initializer=parse_init_string(bias_init),
                kernel_regularizer=CGM_k_reg,
                name=str(ii) + ".common_hidden_layer",
            )(hidden_layer)

        # Neural network for single constants
        constant1 = hidden_layer
        constant2 = []
        constant3 = []
        for dimension in train_dims:
            constant2.append(hidden_layer)
            if "pf" in dimension:
                constant3.append(
                    ke.layers.Concatenate(name="concat_layer_" + dimension)(
                        [hidden_layer, special_input]
                    )
                )
            else:
                constant3.append(hidden_layer)
        for ii, (activation, neurons) in enumerate(
            zip(settings["individual_layers_activation"], settings["individual_layers"]),
            start=1,
        ):
            constant1 = ke.layers.Dense(
                neurons,
                activation=parse_activation(activation),
                kernel_initializer=parse_init_string(weight_init),
                bias_initializer=parse_init_string(bias_init),
                kernel_regularizer=CGM_k_reg,
                name=str(ii) + ".hidden_layer_c1_",
            )(constant1)
            for j, dimension in enumerate(train_dims):
                if "pf" in dimension:
                    constant3[j] = ke.layers.Dense(
                        neurons,
                        activation=parse_activation(activation),
                        kernel_initializer=parse_init_string(weight_init),
                        bias_initializer=parse_init_string(bias_init),
                        kernel_regularizer=k_reg,
                        name=str(ii) + ".hidden_layer_" + dimension,
                    )(constant3[j])
                else:
                    constant2[j] = ke.layers.Dense(
                        neurons,
                        activation=parse_activation(activation),
                        kernel_initializer=parse_init_string(weight_init),
                        bias_initializer=parse_init_string(bias_init),
                        kernel_regularizer=CGM_k_reg,
                        name=str(ii) + ".hidden_layer_c2_" + dimension,
                    )(constant2[j])
                    constant3[j] = ke.layers.Dense(
                        neurons,
                        activation=parse_activation(activation),
                        kernel_initializer=parse_init_string(weight_init),
                        bias_initializer=parse_init_string(bias_init),
                        kernel_regularizer=CGM_k_reg,
                        name=str(ii) + ".hidden_layer_c3_" + dimension,
                    )(constant3[j])

        # All the constants
        constant1 = ke.layers.Dense(
            1, activation="linear", kernel_regularizer=CGM_k_reg, name="c1_output"
        )(constant1)
        for i, dimension in enumerate(train_dims):
            if "pf" in dimension:
                constant3[i] = ke.layers.Dense(
                    1,
                    activation="linear",
                    kernel_regularizer=k_reg,
                    name="output_" + dimension,
                )(constant3[i])
            else:
                constant2[i] = ke.layers.Dense(
                    1,
                    activation="relu",
                    kernel_regularizer=CGM_k_reg,
                    name="c2_output_" + dimension,
                )(constant2[i])
                constant3[i] = ke.layers.Dense(
                    1,
                    activation="linear",
                    kernel_regularizer=CGM_k_reg,
                    name="c3_output_" + dimension,
                )(constant3[i])

        # Final layers
        difference = ke.layers.Subtract(name="difference")([special_input, constant1])
        relu = ke.layers.ReLU(name="heaviside_function_times_x")(difference)

        # Outputlayer
        outputs = []
        for i, dimension in enumerate(train_dims):
            if "pf" in dimension:
                outputs.append(
                    ke.layers.Multiply(name="final_product_" + dimension)([constant3[i], relu])
                )
            else:
                outputs.append(
                    ke.layers.Multiply(name="final_product_" + dimension)(
                        [
                            constant3[i],
                            relu,
                            tf.pow(
                                tf.clip_by_value(tf.abs(difference), 0.0000000001, 1000),
                                constant2[i],
                            ),
                        ]
                    )
                )

        # Initialazing the model
        self.model = ke.Model(inputs=[normal_inputs, special_input], outputs=outputs)

    def to_json(self):
        nn_dict = model_to_json_dict(
            "dummy_name",
            feature_names=self._feature_names,
            target_names=self._target_names,
            scale_factor=pd.concat([self._feature_prescale_factor, self._target_prescale_factor]),
            scale_bias=pd.concat([self._feature_prescale_bias, self._target_prescale_bias]),
            train_set=self._train_set,
            settings=self.settings,
        )
        model_dict = json.loads(self.model.to_json())
        weights_list = self.model.get_weights()
        weight_dict = {}
        for layer in self.model.layers:
            weight_dict[layer.name] = [arr.tolist() for arr in layer.get_weights()]
            nn_dict.update(
                {
                    "special_feature": self._special_feature,
                    "model": model_dict,
                    "weights": weight_dict,
                }
            )
        return nn_dict

    def model_from_json(self, path="nn.json"):
        with open(path, "r") as file_:
            nn_dict = json.load(file_)
        self.settings = nn_dict["_parsed_settings"]
        self._feature_names = nn_dict["feature_names"]
        self._feature_prescale_bias = dict(
            (k, nn_dict["prescale_bias"][k])
            for k in self._feature_names
            if k in nn_dict["prescale_bias"]
        )
        self._feature_prescale_factor = dict(
            (k, nn_dict["prescale_factor"][k])
            for k in self._feature_names
            if k in nn_dict["prescale_factor"]
        )
        self._target_prescale_bias = dict(
            (k, nn_dict["prescale_bias"][k])
            for k in self._target_names
            if k in nn_dict["prescale_bias"]
        )
        self._target_prescale_factor = dict(
            (k, nn_dict["prescale_factor"][k])
            for k in self._target_names
            if k in nn_dict["prescale_factor"]
        )
        self.model = ke.models.model_from_json(json.dumps(nn_dict["model"]))
        weight_dict = nn_dict["weights"]
        for layer in self.model.layers:
            layer.set_weights([np.array(el) for el in weight_dict[layer.name]])
