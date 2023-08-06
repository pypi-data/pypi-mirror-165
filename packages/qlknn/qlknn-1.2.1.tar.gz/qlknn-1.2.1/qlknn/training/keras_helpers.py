import numpy as np
import tensorflow as tf
import tensorflow.keras as ke
from tensorflow.keras import backend as K
from tensorflow.python.ops import math_ops
from tensorflow.python.ops.losses import util as tf_losses_utils
from tensorflow.python.framework import ops
from tensorflow.python.ops import init_ops
from tensorflow.python.ops import array_ops
from IPython import embed
import logging

# Enable fancy logging before anything else
root_logger = logging.getLogger("qlknn")
logger = root_logger
logger.setLevel(logging.INFO)

# For grabbing the training generator
import math
from tensorflow.python.util import nest
from tensorflow.python.keras.utils import data_utils
from tensorflow.python.keras.utils import generic_utils
from tensorflow.python.keras.engine import training_utils
from tensorflow.python.keras.callbacks import Callback
from tensorflow.python.data.ops import iterator_ops
from tensorflow.python.data.ops import dataset_ops


@tf.function
def is_stable_label(y):
    return K.all([K.less_equal(y, 1.0e-4), K.greater_equal(y, -1.0e-4)], axis=0)


class TotalLoss(ke.losses.Loss):
    def __init__(
        self,
        losses,
        loss_weights,
        reduction=ke.losses.Reduction.AUTO,
        name="total_loss",
    ):
        assert len(losses) == len(loss_weights)
        ke.losses.Loss.__init__(self, reduction=reduction, name=name)
        self.losses = losses
        self.loss_weights = loss_weights

    @tf.function
    def call(self, y_true, y_pred):
        total_loss = 0
        for weight, loss in zip(self.loss_weights, self.losses):
            total_loss += weight * loss.call(y_true, y_pred)
        return total_loss


class UnstableAwareGoodness(ke.losses.Loss, ke.metrics.Metric):
    def __init__(
        self,
        measure,
        target_prescale_factor,
        target_prescale_bias,
        reduction=ke.losses.Reduction.AUTO,
        name="goodness",
        dtype=None,
    ):
        ke.losses.Loss.__init__(self, reduction=reduction, name=name)
        ke.metrics.Metric.__init__(self, name=name, dtype=dtype)

        # This assumes the passed prescales are ordered!
        self.target_prescale_factor = np.array(target_prescale_bias)
        self.target_prescale_bias = np.array(target_prescale_bias)
        if measure not in ["mse"]:
            raise NotImplementedError("Measure of goodness {!s}".format(measure))
        self.measure = measure
        self.goodness_metric = self.add_weight(name="goodness_metric", initializer="zeros")
        with ops.init_scope():
            self.total = self.add_weight("total", initializer=init_ops.zeros_initializer)
            self.count = self.add_weight("count", initializer=init_ops.zeros_initializer)

    @tf.function
    def call(self, y_true, y_pred):
        y_true_descale = (y_true - self.target_prescale_bias) / self.target_prescale_factor
        orig_is_stable = is_stable_label(y_true_descale)
        if self.measure == "mse":
            goodness = math_ops.squared_difference
        good = goodness(y_true, y_pred)
        weights = array_ops.where(
            orig_is_stable, array_ops.zeros_like(y_pred), array_ops.ones_like(y_pred)
        )
        # Not needed, as our weights are just 0 and 1
        # present = array_ops.where(
        #    math_ops.equal(weights, 0.0),
        #    array_ops.zeros_like(weights),
        #    array_ops.ones_like(weights))
        present = weights

        loss = math_ops.div_no_nan(
            math_ops.reduce_sum(good * weights), math_ops.reduce_sum(present)
        )
        # Original way. Kept for reference
        # val_weights = K.switch(orig_is_stable,
        #                       K.zeros_like(y_true),
        #                       K.ones_like(y_true))
        # loss = K.mean(tf_losses_utils.scale_losses_by_sample_weight(good, val_weights))
        return loss

    def update_state(self, y_true, y_pred, sample_weight=None):
        if sample_weight is not None:
            logger.warning("Updating state with sample weights not implemented, using unweighted")
        loss = self.call(y_true, y_pred)
        self.total.assign_add(loss)
        num_values = math_ops.cast(1.0, self._dtype)
        self.count.assign_add(num_values)

    def result(self):
        return math_ops.div_no_nan(self.total, self.count)

    def reset_states(self):
        self.total.assign(0.0)
        self.count.assign(0.0)

    # Overwrite 'name' property, or ke.metrics.Metric.__init__ will complain
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value


class StablePositiveLoss(ke.losses.Loss, ke.metrics.Metric):
    def __init__(
        self,
        weight,
        offset,
        function,
        target_prescale_factor,
        target_prescale_bias,
        reduction=ke.losses.Reduction.AUTO,
        name="stable_positive_loss",
        dtype=None,
    ):
        ke.losses.Loss.__init__(self, reduction=reduction, name=name)
        ke.metrics.Metric.__init__(self, name=name, dtype=dtype)
        # super(StablePositiveLoss, self).__init__(reduction=reduction, name=name)
        self.weight = weight
        self.offset = offset
        # This assumes the passed prescales are ordered!
        self.target_prescale_factor = np.array(target_prescale_bias)
        self.target_prescale_bias = np.array(target_prescale_bias)
        if function == "block":
            pass
        elif function == "barrier":
            raise NotImplementedError(
                "cost_stable_positive_function {!s}".format(
                    settings["cost_stable_positive_function"]
                )
            )
            # def loss(y_true, y_pred):
            #    punish_unstable_pred = tf.logical_and(orig_is_stable, nn_pred_above_offset)
            #    stable_positive_loss = tf.reduce_mean(tf.cast(orig_is_stable, x.dtype) * tf.exp(stable_positive_scale * (y - stable_positive_offset)))
        else:
            raise NotImplementedError(
                "cost_stable_positive_function {!s}".format(
                    settings["cost_stable_positive_function"]
                )
            )
        with ops.init_scope():
            self.total = self.add_weight("total", initializer=init_ops.zeros_initializer)
            self.count = self.add_weight("count", initializer=init_ops.zeros_initializer)

    def call(self, y_true, y_pred):
        y_true_descale = (y_true - self.target_prescale_bias) / self.target_prescale_factor
        orig_is_stable = is_stable_label(y_true_descale)
        nn_pred_above_offset = K.greater(y_pred, self.offset)
        punish_unstable_pred = K.all([orig_is_stable, nn_pred_above_offset], axis=0)
        loss = K.mean(
            self.weight * (y_pred - self.offset) * K.cast(punish_unstable_pred, y_pred.dtype)
        )
        return loss

    def update_state(self, y_true, y_pred, sample_weight=None):
        if sample_weight is not None:
            logger.warning("Updating state with sample weights not implemented, using unweighted")
        loss = self.call(y_true, y_pred)
        self.total.assign_add(loss)
        num_values = math_ops.cast(1.0, self._dtype)
        self.count.assign_add(num_values)

    def result(self):
        return math_ops.div_no_nan(self.total, self.count)

    def reset_states(self):
        self.total.assign(0.0)
        self.count.assign(0.0)

    # Overwrite 'name' property, or ke.metrics.Metric.__init__ will complain
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value


def parse_init_string(init):
    if isinstance(init, str):
        if init.startswith("normsm"):
            __, s, m = init.split("_")
            initial = tf.random_normal_initializer(mean=float(m), stddev=float(s))
        elif init == "glorot_normal":
            initial = ke.initializers.GlorotNormal()
        elif init == "glorot_uniform":
            initial = ke.initializers.GlorotUniform()
        elif init.startswith("const"):
            __, c = init.split("_")
            initial = ke.initializers.Constant(float(c))

    elif isinstance(init, np.ndarray):
        initial = tf.constant(init, dtype=dtype)
    try:
        initial
    except:
        raise Exception("Could not parse init {!s}".format(init))
    return initial


def parse_activation(activation):
    if activation == "tanh":
        act = tf.tanh
    elif activation == "relu":
        act = tf.nn.relu
    elif activation == "none":
        act = None
    else:
        raise Exception("Unknown activation function '{!s}'".format(activation_func))
    return act


def convert_to_generator_like(
    data, batch_size=None, steps_per_epoch=None, epochs=1, shuffle=False
):
    """Make a generator out of NumPy or EagerTensor inputs.

    Taken from tensorflow_core/python/keras/engine/training_generator.py

    Arguments:
      data: Either a generator or `keras.utils.data_utils.Sequence` object or
        `Dataset`, `Iterator`, or a {1,2,3}-tuple of NumPy arrays or EagerTensors.

        If a tuple, the elements represent `(x, y, sample_weights)` and may be
        `None` or `[None]`.
      batch_size: Used when creating a generator out of tuples of NumPy arrays or
        EagerTensors.
      steps_per_epoch: Steps of the generator to run each epoch. If `None` the
        number of steps will be read from the data (for
        `keras.utils.data_utils.Sequence` types).
      epochs: Total number of epochs to run.
      shuffle: Whether the data should be shuffled.

    Returns:
      - Generator, `keras.utils.data_utils.Sequence`, or `Iterator`.

    Raises:
      - ValueError: If `batch_size` is not provided for NumPy or EagerTensor
        inputs.
    """
    if isinstance(data, tuple):
        # Scrub `Nones` that might have been passed for `targets`, `sample_weights`.
        data = tuple(ele for ele in data if not all(e is None for e in nest.flatten(ele)))

    if data_utils.is_generator_or_sequence(data) or isinstance(data, iterator_ops.OwnedIterator):
        if isinstance(data, data_utils.Sequence):
            if steps_per_epoch is None:
                steps_per_epoch = len(data)
        return data, steps_per_epoch
    if isinstance(data, dataset_ops.DatasetV2):
        return dataset_ops.make_one_shot_iterator(data), steps_per_epoch

    # Create generator from NumPy or EagerTensor Input.
    num_samples = int(nest.flatten(data)[0].shape[0])
    if batch_size is None:
        raise ValueError(
            "When passing input data as arrays, do not specify "
            "`steps_per_epoch`/`steps` argument. Please use `batch_size` instead."
        )
    logger.info(f"found {num_samples} samples with batch size of {batch_size}"
                f" for input data shape {data[0].shape} and output data shape"
                f" {data[1].shape}")
    steps_per_epoch = int(math.ceil(num_samples / batch_size))

    def _gen(data):
        """Makes a generator out of a structure of NumPy/EagerTensors."""
        index_array = np.arange(num_samples)
        for _ in range(epochs):
            if shuffle:
                np.random.shuffle(index_array)
            batches = generic_utils.make_batches(num_samples, batch_size)
            for (batch_start, batch_end) in batches:
                batch_ids = index_array[batch_start:batch_end]
                flat_batch_data = training_utils.slice_arrays(
                    nest.flatten(data), batch_ids, contiguous=(not shuffle)
                )
                yield nest.pack_sequence_as(data, flat_batch_data)

    return _gen(data), steps_per_epoch


class RestoreBest(ke.callbacks.Callback):
    def __init__(self, monitor="val_loss", verbose=0, mode="auto", baseline=None):
        super(RestoreBest, self).__init__()

        self.monitor = monitor
        self.verbose = verbose
        self.baseline = baseline
        self.best_epoch = 0

        if mode not in ["auto", "min", "max"]:
            logging.warning("RestoreBest mode %s is unknown, " "fallback to auto mode.", mode)
            mode = "auto"

        if mode == "min":
            self.monitor_op = np.less
        elif mode == "max":
            self.monitor_op = np.greater
        else:
            if "acc" in self.monitor:
                self.monitor_op = np.greater
            else:
                self.monitor_op = np.less

    def on_train_begin(self, logs=None):
        # Allow instances to be re-used
        self.wait = 0
        self.best_epoch = 0
        # Do not overwrite best of previous trainings
        if not hasattr(self, "best"):
            if self.baseline is not None:
                self.best = self.baseline
            else:
                self.best = np.Inf if self.monitor_op == np.less else -np.Inf
        if not hasattr(self, "best_weights"):
            self.best_weights = None

    def on_epoch_end(self, epoch, logs=None):
        current = self.get_monitor_value(logs)
        if current is None:
            logging.warning(
                "Can save best model only with %s available, " "skipping.", self.monitor
            )
            return
        else:
            if self.monitor_op(current, self.best):
                if self.verbose > 0:
                    print(
                        "\nEpoch %05d: %s improved from %0.5f to %0.5f."
                        % (epoch + 1, self.monitor, self.best, current)
                    )
                self.best_epoch = epoch + 1
                self.best_weights = self.model.get_weights()
                self.best = current
            else:
                if self.verbose > 0:
                    print(
                        "\nEpoch %05d: %s did not improve from %0.5f"
                        % (epoch + 1, self.monitor, self.best)
                    )

    def on_train_end(self, logs=None):
        if self.best_epoch == 1:
            logging.warning(
                "Best epoch is epoch 1. Restore weights _after_ model update. "
                "Model before starting training might have been better"
            )
        if self.best_weights:
            self.model.set_weights(self.best_weights)
            if self.verbose > 0:
                print("Epoch %05d with loss %0.5f restored." % (self.best_epoch, self.best))

    def get_monitor_value(self, logs):
        logs = logs or {}
        monitor_value = logs.get(self.monitor)
        if monitor_value is None:
            logging.warning(
                "Early stopping conditioned on metric `%s` "
                "which is not available. Available metrics are: %s",
                self.monitor,
                ",".join(list(logs.keys())),
            )
        return monitor_value
