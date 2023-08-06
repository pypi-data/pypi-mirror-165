"""Tensorflow model utility functions."""

import os
import tempfile
from types import SimpleNamespace
from typing import TYPE_CHECKING, Any, Dict, List, Tuple, Union

import numpy as np
import slideflow as sf
from pandas.core.frame import DataFrame
from slideflow.stats import df_from_pred
from slideflow.util import log
from rich.progress import Progress, TimeElapsedColumn, MofNCompleteColumn

import tensorflow as tf

if TYPE_CHECKING:
    import neptune.new as neptune


def log_summary(
    model: tf.keras.Model,
    neptune_run: "neptune.Run" = None
) -> None:
    """Log the model summary.

    Args:
        model (tf.keras.Model): Tensorflow/Keras model.
        neptune_run (neptune.Run, optional): Neptune run. Defaults to None.
    """
    if sf.getLoggingLevel() <= 20:
        print()
        model.summary()
    if neptune_run:
        summary_string = []
        model.summary(print_fn=lambda x: summary_string.append(x))
        neptune_run['summary'] = "\n".join(summary_string)


def get_layer_index_by_name(model: tf.keras.Model, name: str) -> int:
    for i, layer in enumerate(model.layers):
        if layer.name == name:
            return i
    raise IndexError(f"Layer {name} not found.")


def batch_loss_crossentropy(
    features: tf.Tensor,
    diff: float = 0.5,
    eps: float = 1e-5
) -> tf.Tensor:
    split = tf.split(features, 8, axis=0)

    def tstat(first, rest):
        first_mean = tf.math.reduce_mean(first, axis=0)
        rest_mean = tf.math.reduce_mean(rest, axis=0)

        # Variance
        A = tf.math.reduce_sum(tf.math.square(first - first_mean), axis=0) / (first_mean.shape[0] - 1)
        B = tf.math.reduce_sum(tf.math.square(rest - rest_mean), axis=0) / (rest_mean.shape[0] - 1)

        # Not performing square root of SE for computational reasons
        se = tf.math.sqrt((A / first_mean.shape[0]) + (B / rest_mean.shape[0]))
        t_square = tf.math.square((first_mean - rest_mean - diff) / se)
        return tf.math.reduce_mean(t_square)

    stats = [
        tstat(
            split[n],
            tf.concat([
                sp for i, sp in enumerate(split)
                if i != n
            ], axis=0))
        for n in range(len(split))
    ]
    return tf.math.reduce_mean(tf.stack(stats)) * eps


def negative_log_likelihood(y_true: tf.Tensor, y_pred: tf.Tensor) -> tf.Tensor:
    """Negative log likelihood loss.

    Implemented by Fred Howard, adapted from
    https://github.com/havakv/pycox/blob/master/pycox/models/loss.py

    Args:
        y_true (tf.Tensor): True labels.
        y_pred (tf.Tensor): Predictions.

    Returns:
        tf.Tensor: Loss.
    """
    events = tf.reshape(y_pred[:, -1], [-1])  # E
    pred_hr = tf.reshape(y_pred[:, 0], [-1])  # y_pred
    time = tf.reshape(y_true, [-1])           # y_true

    order = tf.argsort(time)  # direction='DESCENDING'
    sorted_events = tf.gather(events, order)            # pylint: disable=no-value-for-parameter
    sorted_predictions = tf.gather(pred_hr, order)      # pylint: disable=no-value-for-parameter

    # Finds maximum HR in predictions
    gamma = tf.math.reduce_max(sorted_predictions)

    # Small constant value
    eps = tf.constant(1e-7, dtype=tf.float32)

    log_cumsum_h = tf.math.add(
                    tf.math.log(
                        tf.math.add(
                            tf.math.cumsum(             # pylint: disable=no-value-for-parameter
                                tf.math.exp(
                                    tf.math.subtract(sorted_predictions, gamma))),
                            eps)),
                    gamma)

    neg_likelihood = -tf.math.divide(
                        tf.reduce_sum(
                            tf.math.multiply(
                                tf.subtract(sorted_predictions, log_cumsum_h),
                                sorted_events)),
                        tf.reduce_sum(sorted_events))

    return neg_likelihood


def negative_log_likelihood_breslow(
    y_true: tf.Tensor,
    y_pred: tf.Tensor
) -> tf.Tensor:
    """Negative log likelihood loss, Breslow approximation.

    Args:
        y_true (tf.Tensor): True labels.
        y_pred (tf.Tensor): Predictions.

    Returns:
        tf.Tensor: Breslow loss.
    """
    events = tf.reshape(y_pred[:, -1], [-1])
    pred = tf.reshape(y_pred[:, 0], [-1])
    time = tf.reshape(y_true, [-1])

    order = tf.argsort(time, direction='DESCENDING')
    sorted_time = tf.gather(time, order)                # pylint: disable=no-value-for-parameter
    sorted_events = tf.gather(events, order)            # pylint: disable=no-value-for-parameter
    sorted_pred = tf.gather(pred, order)                # pylint: disable=no-value-for-parameter

    Y_hat_c = sorted_pred
    Y_label_T = sorted_time
    Y_label_E = sorted_events
    Obs = tf.reduce_sum(Y_label_E)

    # numerical stability
    amax = tf.reduce_max(Y_hat_c)
    Y_hat_c_shift = tf.subtract(Y_hat_c, amax)
    # Y_hat_c_shift = tf.debugging.check_numerics(Y_hat_c_shift, message="checking y_hat_c_shift")
    Y_hat_hr = tf.exp(Y_hat_c_shift)
    Y_hat_cumsum = tf.math.log(tf.cumsum(Y_hat_hr)) + amax  # pylint: disable=no-value-for-parameter

    unique_values, segment_ids = tf.unique(Y_label_T)
    loss_s2_v = tf.math.segment_max(Y_hat_cumsum, segment_ids)
    loss_s2_count = tf.math.segment_sum(Y_label_E, segment_ids)

    loss_s2 = tf.reduce_sum(tf.multiply(loss_s2_v, loss_s2_count))
    loss_s1 = tf.reduce_sum(tf.multiply(Y_hat_c, Y_label_E))
    loss_breslow = tf.divide(tf.subtract(loss_s2, loss_s1), Obs)
    return loss_breslow


def concordance_index(y_true: tf.Tensor, y_pred: tf.Tensor) -> tf.Tensor:
    """Calculate concordance index (C-index).

    Args:
        y_true (tf.Tensor): True labels.
        y_pred (tf.Tensor): Predictions.

    Returns:
        tf.Tensor: Concordance index.
    """
    E = y_pred[:, -1]
    y_pred = y_pred[:, :-1]
    E = tf.reshape(E, [-1])
    y_pred = tf.reshape(y_pred, [-1])
    y_pred = -y_pred  # negative of log hazard ratio to have correct relationship with survival
    g = tf.subtract(tf.expand_dims(y_pred, -1), y_pred)
    g = tf.cast(g == 0.0, tf.float32) * 0.5 + tf.cast(g > 0.0, tf.float32)
    f = tf.subtract(tf.expand_dims(y_true, -1), y_true) > 0.0
    event = tf.multiply(tf.transpose(E), E)
    f = tf.multiply(tf.cast(f, tf.float32), event)
    f = tf.compat.v1.matrix_band_part(tf.cast(f, tf.float32), -1, 0)
    g = tf.reduce_sum(tf.multiply(g, f))
    f = tf.reduce_sum(f)
    return tf.where(tf.equal(f, 0), 0.0, g/f)


def add_regularization(
    model: tf.keras.Model,
    regularizer: tf.keras.layers.Layer
) -> tf.keras.Model:
    '''Adds regularization (e.g. L2) to all eligible layers of a model.
    This function is from "https://sthalles.github.io/keras-regularizer/" '''

    if not isinstance(regularizer, tf.keras.regularizers.Regularizer):
        print('Regularizer must be a subclass of tf.keras.regularizers.Regularizer')
        return model

    for layer in model.layers:
        for attr in ['kernel_regularizer']:
            if hasattr(layer, attr):
                setattr(layer, attr, regularizer)

    # When we change the layers attributes, the change only happens in the model config file
    model_json = model.to_json()

    # Save the weights before reloading the model.
    tmp_weights_path = os.path.join(tempfile.gettempdir(), 'tmp_weights.h5')
    model.save_weights(tmp_weights_path)

    # load the model from the config
    model = tf.keras.models.model_from_json(model_json)

    # Reload the model weights
    model.load_weights(tmp_weights_path, by_name=True)
    return model


def get_uq_predictions(
    img: tf.Tensor,
    pred_fn: tf.keras.Model,
    num_outcomes: int,
    uq_n: int = 30
) -> Tuple[tf.Tensor, tf.Tensor, int]:
    if not num_outcomes:
        yp_drop = {}  # type: Union[List[Any], Dict[int, List]]
    else:
        yp_drop = {n: [] for n in range(num_outcomes)}
    for _ in range(uq_n):
        yp = pred_fn(img, training=False)
        if not num_outcomes:
            num_outcomes = 1 if not isinstance(yp, list) else len(yp)
            yp_drop = {n: [] for n in range(num_outcomes)}
        if num_outcomes > 1:
            for o in range(num_outcomes):
                yp_drop[o] += [yp[o]]
        else:
            yp_drop[0] += [yp]
    if num_outcomes > 1:
        yp_drop = [tf.stack(yp_drop[n], axis=0) for n in range(num_outcomes)]
        yp_mean = [tf.math.reduce_mean(yp_drop[n], axis=0) for n in range(num_outcomes)]
        yp_std = [tf.math.reduce_std(yp_drop[n], axis=0) for n in range(num_outcomes)]
    else:
        yp_drop = tf.stack(yp_drop[0], axis=0)
        yp_mean = tf.math.reduce_mean(yp_drop, axis=0)
        yp_std = tf.math.reduce_std(yp_drop, axis=0)
    return yp_mean, yp_std, num_outcomes


def unwrap(
    model: tf.keras.models.Model
):
    """Unwraps a Tensorflow model built in Slideflow, returning the
    input tensor, post-convolutional output tensor, and final model output
    tensor.

    Args:
        model (tf.keras.models.Model): Model built with Slideflow.

    Returns:
        A tuple containing

            tf.Tensor:  Input tensor.

            tf.Tensor:  Post-convolutional layer output tensor.

            tf.Tensor:  Final model output tensor.
    """
    submodel = model.layers[1]
    x = submodel.outputs[0]
    postconv = x
    for layer_index in range(2, len(model.layers)):
        extracted_layer = model.layers[layer_index]
        x = extracted_layer(x)

    return submodel.inputs, postconv, x


def _eval_from_model(
    model: "tf.keras.Model",
    dataset: "tf.data.Dataset",
    model_type: str,
    pred_args: SimpleNamespace,
    num_tiles: int = 0,
    uq_n: int = 30,
    incl_loc: bool = False,
) -> Tuple[DataFrame, float, float]:
    """Generates predictions (y_true, y_pred, tile_to_slide) from a given
    Tensorflow model and dataset.

    Args:
        model (str): Path to Tensorflow model.
        dataset (tf.data.Dataset): Tensorflow dataset.
        model_type (str, optional): 'categorical', 'linear', or 'cph'.
            Will not attempt to calculate accuracy for non-categorical models.
            Defaults to 'categorical'.
        pred_args (namespace): Namespace containing the property `loss` (loss
            function used to calculate loss) and `uq` (bool, whether to use uq).
        num_tiles (int, optional): Used for progress bar. Defaults to 0.
        uq_n (int, optional): Number of per-tile inferences to perform is
            calculating uncertainty via dropout.

    Returns:
        pd.DataFrame, accuracy, loss
    """

    @tf.function
    def get_predictions(img, training=False):
        return model(img, training=training)

    y_true, y_pred, tile_to_slides = [], [], []
    locations = [] if incl_loc else None
    y_std = [] if pred_args.uq else None  # type: ignore
    num_vals, num_batches, num_outcomes, running_loss = 0, 0, 0, 0
    is_cat = (model_type == 'categorical')
    if not is_cat:
        acc = None

    pb = Progress(
        *Progress.get_default_columns(),
        TimeElapsedColumn(),
        MofNCompleteColumn(),
        transient=sf.getLoggingLevel()>20
    )
    task = pb.add_task("Evaluating...", total=num_tiles)
    pb.start()
    for batch in dataset:

        # Parse dataset batch
        if incl_loc:
            img, yt, slide, loc_x, loc_y = batch
            locations += [tf.stack([loc_x, loc_y], axis=-1).numpy()]
        else:
            img, yt, slide = batch

        pb.advance(task, slide.shape[0])
        tile_to_slides += [_byte.decode('utf-8') for _byte in slide.numpy()]
        num_vals += slide.shape[0]
        num_batches += 1

        if pred_args.uq:
            yp, yp_std, num_outcomes = get_uq_predictions(
                img, get_predictions, num_outcomes, uq_n
            )
            y_pred += [yp]
            y_std += [yp_std]  # type: ignore
        else:
            yp = get_predictions(img, training=False)
            y_pred += [yp]
        if type(yt) == dict:
            y_true += [[yt[f'out-{o}'].numpy() for o in range(len(yt))]]
            yt = [yt[f'out-{o}'] for o in range(len(yt))]
        else:
            y_true += [yt.numpy()]
        loss = pred_args.loss(yt, yp)
        running_loss += tf.math.reduce_sum(loss).numpy() * slide.shape[0]
    pb.stop()

    if type(y_pred[0]) == list:
        # Concatenate predictions for each outcome
        y_pred = [np.concatenate(yp) for yp in zip(*y_pred)]
        if pred_args.uq:
            y_std = [np.concatenate(ys) for ys in zip(*y_std)]  # type: ignore
    else:
        y_pred = [np.concatenate(y_pred)]
        if pred_args.uq:
            y_std = [np.concatenate(y_std)]

    if type(y_true[0]) == list:
        # Concatenate y_true for each outcome
        y_true = [np.concatenate(yt) for yt in zip(*y_true)]
        if is_cat:
            acc = [
                np.sum(y_true[i] == np.argmax(y_pred[i], axis=1)) / num_vals
                for i in range(len(y_true))
            ]
    else:
        y_true = [np.concatenate(y_true)]
        if is_cat:
            acc = np.sum(y_true[0] == np.argmax(y_pred[0], axis=1)) / num_vals

    if incl_loc:
        locations = np.concatenate(locations)

    # Create pandas DataFrame from arrays
    df = df_from_pred(y_true, y_pred, y_std, tile_to_slides, locations)

    # Note that Keras loss during training includes regularization losses,
    # so this loss will not match validation loss calculated during training
    loss = running_loss / num_vals
    log.debug("Evaluation complete.")
    return df, acc, loss  # type: ignore


def _predict_from_model(
    model: "tf.keras.Model",
    dataset: "tf.data.Dataset",
    model_type: str,
    pred_args: SimpleNamespace,
    num_tiles: int = 0,
    uq_n: int = 30,
    incl_loc: bool = False,
) -> DataFrame:
    """Generates predictions (y_true, y_pred, tile_to_slide) from a given
    Tensorflow model and dataset.

    Args:
        model (str): Path to Tensorflow model.
        dataset (tf.data.Dataset): Tensorflow dataset.
        model_type (str, optional): 'categorical', 'linear', or 'cph'.
            Will not attempt to calculate accuracy for non-categorical models.
            Defaults to 'categorical'.
        pred_args (namespace): Namespace containing the property `loss`, loss
            function used to calculate loss.
        num_tiles (int, optional): Used for progress bar. Defaults to 0.
        uq_n (int, optional): Number of per-tile inferences to perform is
            calculating uncertainty via dropout.

    Returns:
        pd.DataFrame, accuracy, loss
    """

    @tf.function
    def get_predictions(img, training=False):
        return model(img, training=training)

    y_pred, tile_to_slides = [], []
    locations = [] if incl_loc else None
    y_std = [] if pred_args.uq else None  # type: ignore
    num_vals, num_batches, num_outcomes = 0, 0, 0

    pb = Progress(
        *Progress.get_default_columns(),
        TimeElapsedColumn(),
        MofNCompleteColumn(),
        transient=sf.getLoggingLevel()>20
    )
    task = pb.add_task("Predicting...", total=num_tiles)
    pb.start()
    for batch in dataset:  # TODO: support not needing to supply yt
        if incl_loc:
            img, yt, slide, loc_x, loc_y = batch
            locations += [tf.stack([loc_x, loc_y], axis=-1).numpy()]
        else:
            img, yt, slide = batch
        pb.advance(task, slide.shape[0])
        tile_to_slides += [_bytes.decode('utf-8') for _bytes in slide.numpy()]
        num_vals += slide.shape[0]
        num_batches += 1
        if pred_args.uq:
            yp_mean, yp_std, num_outcomes = get_uq_predictions(
                img, get_predictions, num_outcomes, uq_n
            )
            y_pred += [yp_mean]
            y_std += [yp_std]  # type: ignore
        else:
            yp = get_predictions(img, training=False)
            y_pred += [yp]
    pb.stop()

    if type(y_pred[0]) == list:
        # Concatenate predictions for each outcome
        y_pred = [np.concatenate(yp) for yp in zip(*y_pred)]
        if pred_args.uq:
            y_std = [np.concatenate(ys) for ys in zip(*y_std)]  # type: ignore
    else:
        y_pred = [np.concatenate(y_pred)]
        if pred_args.uq:
            y_std = [np.concatenate(y_std)]

    if incl_loc:
        locations = np.concatenate(locations)

    # Create pandas DataFrame from arrays
    df = df_from_pred(None, y_pred, y_std, tile_to_slides, locations)

    log.debug("Prediction complete.")
    return df
