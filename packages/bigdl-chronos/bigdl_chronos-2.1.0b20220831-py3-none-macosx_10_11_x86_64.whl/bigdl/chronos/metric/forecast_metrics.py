#
# Copyright 2016 The BigDL Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import torch
import numpy as np
from torch import Tensor
from numpy import ndarray
from functools import partial
from torchmetrics.functional import mean_squared_error, mean_absolute_error,\
    mean_absolute_percentage_error, r2_score
from bigdl.nano.utils.log4Error import invalidInputError
from timeit import repeat


EPSILON = 1e-10


# implemented this metric to keep up with orca.automl
def symmetric_mean_absolute_percentage_error(preds: Tensor, target: Tensor) -> Tensor:
    abs_diff = torch.abs(preds - target)
    abs_per_error = abs_diff / (torch.abs(preds) + torch.abs(target) + EPSILON)
    sum_abs_per_error = 100 * torch.sum(abs_per_error)
    num_obs = target.numel()
    return sum_abs_per_error / num_obs


TORCHMETRICS_REGRESSION_MAP = {
    'mae': mean_absolute_error,
    'mse': mean_squared_error,
    'rmse': partial(mean_squared_error, squared=False),
    'mape': mean_absolute_percentage_error,
    'smape': symmetric_mean_absolute_percentage_error,
    'r2': r2_score,
}


def _standard_input(metrics, y_true, y_pred):
    """
    Standardize input functions. Format metrics,
    check the ndim of y_pred and y_true,
    converting 1-3 dim y_true and y_pred to 2 dim.
    """
    if not isinstance(metrics, list):
        metrics = [metrics]
    if isinstance(metrics[0], str):
        metrics = list(map(lambda x: x.lower(), metrics))
        invalidInputError(all(metric in TORCHMETRICS_REGRESSION_MAP.keys() for metric in metrics),
                          f"metric should be one of {TORCHMETRICS_REGRESSION_MAP.keys()},"
                          f" but get {metrics}.")
        invalidInputError(type(y_true) is type(y_pred) and isinstance(y_pred, ndarray),
                          "y_pred and y_true type must be numpy.ndarray,"
                          f" but found {type(y_pred)} and {type(y_true)}.")
        y_true, y_pred = torch.from_numpy(y_true), torch.from_numpy(y_pred)

    invalidInputError(y_true.shape == y_pred.shape,
                      "y_true and y_pred should have the same shape, "
                      f"but get {y_true.shape} and {y_pred.shape}.")

    if y_true.ndim == 1:
        y_true = y_true.reshape(-1, 1)
        y_pred = y_pred.reshape(-1, 1)
        original_shape = y_true.shape
    elif y_true.ndim == 3:
        original_shape = y_true.shape
        y_true = y_true.reshape(y_true.shape[0], y_true.shape[1]*y_true.shape[2])
        y_pred = y_pred.reshape(y_pred.shape[0], y_pred.shape[1]*y_pred.shape[2])
    else:
        original_shape = y_true.shape
    return metrics, y_true, y_pred, original_shape


class Evaluator(object):
    """
    Evaluate metrics for y_true and y_pred.
    """

    @staticmethod
    def evaluate(metrics, y_true, y_pred, aggregate='mean'):
        """
        Evaluate a specific metrics for y_true and y_pred.

        :param metrics: String or list in ['mae', 'mse', 'rmse', 'r2', 'mape', 'smape'] for built-in
               metrics. If callable function, it signature should be func(y_true, y_pred), where
               y_true and y_pred are numpy ndarray.
        :param y_true: Array-like of shape = (n_samples, \*). Ground truth (correct) target values.
        :param y_pred: Array-like of shape = (n_samples, \*). Estimated target values.
        :param aggregate: aggregation method. Currently, "mean" and None are supported,
               'mean' represents aggregating by mean, while None will return the element-wise
               result. The value defaults to 'mean'.

        :return: Float or ndarray of floats.
                 A floating point value, or an
                 array of floating point values, one for each individual target.
        """
        metrics, y_true, y_pred, original_shape = _standard_input(metrics, y_true, y_pred)

        res_list = []
        for metric in metrics:
            if callable(metric):
                metric_func = metric
            else:
                metric_func = TORCHMETRICS_REGRESSION_MAP[metric]
            if len(original_shape) in [2, 3] and aggregate is None:
                res = torch.zeros(y_true.shape[-1])
                for i in range(y_true.shape[-1]):
                    if callable(metric):
                        res[i] = torch.from_numpy(metric_func(y_true[..., i], y_pred[..., i]))
                    else:
                        res[i] = metric_func(y_pred[..., i], y_true[..., i])
                res = res.reshape(original_shape[1:])
                res_list.append(res.numpy())
            else:
                if callable(metric):
                    res = metric_func(y_true, y_pred)
                    res_list.append(res)
                else:
                    res = metric_func(y_pred, y_true)
                    res_list.append(res.numpy())
        return res_list

    def get_latency(func, *args, num_running=100, **kwargs):
        """
        Return the time cost in milliseconds of a specific function by running multiple times.

        :param func: The function to be tested for latency.
        :param args: arguments for the tested function.
        :param num_running: Int and the value is positive. Specify the running number of
               the function and the value defaults to 100.
        :param kwargs: other arguments for the tested function.

        :return: Dictionary of str:float.
                 Show the information of the time cost in milliseconds.

        Example:
            >>> # to get the inferencing performance of a trained TCNForecaster
            >>> x = next(iter(test_loader))[0]
            >>> # run forecaster.predict(x.numpy()) for len(tsdata_test.df) times
            >>> # to evaluate the time cost
            >>> latency = Evaluator.get_latency(forecaster.predict, x.numpy(),\
                          num_running = len(tsdata_test.df))
            >>> # an example output:
            >>> # {"p50": 3.853, "p90": 3.881, "p95": 3.933, "p99": 4.107}
        """
        invalidInputError(isinstance(num_running, int), "num_running type must be int, "
                          f"but found {type(num_running)}.")
        if num_running < 0:
            invalidInputError(False, "num_running value must be positive, "
                              f"but found {num_running}.")

        time_list = repeat(lambda: func(*args, **kwargs), number=1, repeat=num_running)
        sorted_time = np.sort(time_list)

        latency_list = {"p50": round(1000 * np.median(time_list), 3),
                        "p90": round(1000 * sorted_time[int(0.90 * num_running)], 3),
                        "p95": round(1000 * sorted_time[int(0.95 * num_running)], 3),
                        "p99": round(1000 * sorted_time[int(0.99 * num_running)], 3)}

        return latency_list
