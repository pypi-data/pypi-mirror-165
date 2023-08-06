from typing import Dict, Union

import numpy as np
import pandas as pd
from sklearn.metrics import r2_score


def paritydata(Y_actual: np.ndarray, Y_predicted: np.ndarray) -> pd.DataFrame:
    """

    Creates a pd.DataFrame that contains the actual and predicted values

    """
    if Y_actual.ndim == 1:
        Y_actual = Y_actual.reshape(-1, 1)

    if len(Y_predicted.shape) == 1:
        Y_predicted = Y_predicted.reshape(-1, 1)

    return pd.DataFrame(np.hstack((Y_actual, Y_predicted)), columns=["Actual", "Predicted"])


def rmse(Y_actual: np.ndarray, Y_predicted: np.ndarray) -> np.ndarray:
    """

    Determines the root mean square error (RMSE) between the actual and predicted values

    """
    if Y_actual.ndim > 1:
        Y_actual = Y_actual.flatten()

    if len(Y_predicted.shape) > 1:
        Y_predicted = Y_predicted.flatten()

    return np.sqrt(np.mean((Y_actual - Y_predicted) ** 2))


def r2(Y_actual: np.ndarray, Y_predicted: np.ndarray) -> np.ndarray:
    """

    Determines the coefficient of determination (r^2) between the actual and predicted values

    """
    if Y_actual.ndim > 1:
        Y_actual = Y_actual.flatten()

    if len(Y_predicted.shape) > 1:
        Y_predicted = Y_predicted.flatten()

    return r2_score(Y_actual, Y_predicted)


def all_performance_metrics(Y: np.ndarray, Y_predicted: np.ndarray) -> Dict[str, Union[np.ndarray, pd.DataFrame]]:
    """

    Creates a dictionary containing the root mean square error (RMSE), coefficient of determination (r^2), and
    pd.DataFrame of the actual and predicted values

    """
    return {
        "RMSE": rmse(Y, Y_predicted),
        "r2": r2(Y, Y_predicted),
        "Parity Data": paritydata(Y, Y_predicted),
    }


def all_performance_metrics_train_val(
    Y_train: np.ndarray, Y_train_predicted: np.ndarray, Y_val: np.ndarray, Y_val_predicted: np.ndarray
) -> Dict[str, Union[np.ndarray, pd.DataFrame]]:
    """

    Creates a dictionary containing the root mean square error (RMSE), coefficient of determination (r^2), and
    pd.DataFrame of the actual and predicted values for training and validation data

    Parameters
    ----------
    Y_train: np.ndarray
        Actual values for training data
    Y_train_predicted: np.ndarray
        Predicted values for training data
    Y_val: np.ndarray
        Actual values for validation data
    Y_val_predicted: np.ndarray
        Predicted values for validation data

    """
    return {
        "Train RMSE": rmse(Y_train, Y_train_predicted),
        "Validation RMSE": rmse(Y_val, Y_val_predicted),
        "Train r2": r2(Y_train, Y_train_predicted),
        "Validation r2": r2(Y_val, Y_val_predicted),
        "Train Parity Data": paritydata(Y_train, Y_train_predicted),
        "Validation Parity Data": paritydata(Y_val, Y_val_predicted),
    }


def all_performance_metrics_train_val_test(
    Y_train: np.ndarray,
    Y_train_predicted: np.ndarray,
    Y_val: np.ndarray,
    Y_val_predicted: np.ndarray,
    Y_test: np.ndarray,
    Y_test_predicted: np.ndarray,
) -> Dict[str, Union[np.ndarray, pd.DataFrame]]:
    """

    Creates a dictionary containing the root mean square error (RMSE), coefficient of determination (r^2), and
    pd.DataFrame of the actual and predicted values for training, validation, and test data

    Parameters
    ----------
    Y_train: np.ndarray
        Actual values for training data
    Y_train_predicted: np.ndarray
        Predicted values for training data
    Y_val: np.ndarray
        Actual values for validation data
    Y_val_predicted: np.ndarray
        Predicted values for validation data
    Y_test: np.ndarray
        Actual values for test data
    Y_test_predicted: np.ndarray
        Predicted values for test data

    """
    return {
        "Train RMSE": rmse(Y_train, Y_train_predicted),
        "Validation RMSE": rmse(Y_val, Y_val_predicted),
        "Test RMSE": rmse(Y_test, Y_test_predicted),
        "Train r2": r2(Y_train, Y_train_predicted),
        "Validation r2": r2(Y_val, Y_val_predicted),
        "Test r2": r2(Y_test, Y_test_predicted),
        "Train Parity Data": paritydata(Y_train, Y_train_predicted),
        "Validation Parity Data": paritydata(Y_val, Y_val_predicted),
        "Test Parity Data": paritydata(Y_test, Y_test_predicted),
    }
