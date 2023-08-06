from typing import Tuple

import numpy as np
import sklearn


def remove_nan(arr1: np.ndarray, arr2: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """

    Removes slices in two arrays,arr1 and arr2, based on the indexes where there are NaN values in arr2. This method is
    useful to allow ML models to be fitted when you have an irregular number of Y-values for different objectives.
    Ignores any NaN values in arr1 that maybe in arr2.

    Parameters
    ----------
    arr1: np.ndarray
        Array that will be manipulated based on the values in arr2
    arr2: np.ndarray
        The array with shape (n, ) that is used to identify the indexes where NaN values are. These indexes are applied
        as a boolean mask to arr1 and arr2

    Returns
    -------
    arr1: np.ndarray
        Array with slices removed that corresponded with the indexes of any NaN in the arr2 array
    arr2: np.ndarray
        Array with all NaN values removed

    """
    if arr1.shape[0] != arr2.shape[0]:
        raise ValueError(
            f"The arr1 shape at index 0 (arr1.shape[0]) is not the same as the arr2 shape at index 0 (arr2.shape[0])"
        )

    nan_mask = ~np.isnan(arr2)
    return arr1[nan_mask], arr2[nan_mask]


def remove_all_nan_rows(Y: np.ndarray) -> np.ndarray:
    """

    Any rows that contain missing values (NaN) are removed. For example, useful for acquisition functions, which do not
    allow for irregular arrays of objective values.

    Parameters
    ----------
    Y: np.ndarray
        Y array to check for NaN values

    """
    if Y.ndim == 1:
        return Y[~np.isnan(Y)]
    else:
        return Y[~np.isnan(Y).any(axis=1)]


def sort(X: np.ndarray, Y: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """

    Re-orders X and Y arrays such that the Y-values are in ascending order

    """
    if len(Y.shape) == 1:
        Y = Y.reshape(-1, 1)

    XY = np.hstack((X, Y))
    XY_sorted = XY[XY[:, X.shape[1]].argsort()]
    X_sorted = XY_sorted[:, :-1]
    Y_sorted = XY_sorted[:, -1].reshape(-1, 1)

    return X_sorted, Y_sorted.flatten()


def train_test_split(array: np.ndarray, splitnum: int) -> Tuple[np.ndarray, np.ndarray]:
    """

    Splits the provided array by taking out a row every user-defined number (splitnum) for the test set. The remaining
    data in the array are used in the training set

    Parameters
    ----------
    array: np.ndarray

    splitnum: int
        e.g. splitnum = 5 will cause every 5th row in the provided array to be extracted for the test set.

    Returns
    -------
    array_train: np.ndarray
        Training set created from the provided array
    array_test: np.ndarray
        Test set created from the provided array

    """
    array_test_indexes = [x for x in range(0, array.shape[0], splitnum)]
    array_train_indexes = list(set(list(range(array.shape[0]))) - set(array_test_indexes))

    array_train = array[array_train_indexes]
    array_test = array[array_test_indexes]

    return array_train, array_test


def train_val_test_split(array: np.ndarray, splitnum: int) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """

    Splits the provided array by taking out a row every user-defined number (splitnum) for the test set and
    (splitnum/2) for the validation set. The remaining data in the array are used in the training set

    Parameters
    ----------
    array: np.ndarray

    splitnum: int
        e.g. splitnum = 5 will cause every 5th row in the provided array to be extracted for the test set. Every 5th row
        starting from the splitnum/2 row will be extracted for the validation set

    Returns
    -------
    array_train: np.ndarray
        Training set created from the provided array
    array_val: np.ndarray
        Validation set created from the provided array
    array_test: np.ndarray
        Test set created from the provided array

    """
    array_test_indexes = [x for x in range(0, array.shape[0], splitnum)]
    array_val_indexes = [x for x in range(int(splitnum / 2), array.shape[0], splitnum)]
    array_train_indexes = list(set(list(range(array.shape[0]))) - set(array_test_indexes) - set(array_val_indexes))

    array_train = array[array_train_indexes]
    array_val = array[array_val_indexes]
    array_test = array[array_test_indexes]

    return array_train, array_val, array_test


def train_val_test_split_blocks(array: np.ndarray, test_ratio: float) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """

    Splits the inputted array into three equally sized parts for training, validation, and test sets

    """
    array_train, array_val, array_test = np.split(
        array, [int((1 - (2 * test_ratio)) * array.shape[0]), int((1 - test_ratio) * array.shape[0]),],
    )

    return array_train, array_val, array_test


def shuffle(X: np.ndarray, Y: np.ndarray, seed: int) -> Tuple[np.ndarray, np.ndarray]:
    """

    Shuffles the X and Y arrays according to the seed integer provided

    """
    X, Y = sklearn.utils.shuffle(X, Y, random_state=seed)

    return X, Y


def sort_train_test_split_shuffle(
    X: np.ndarray, Y: np.ndarray, test_ratio: float = 0.2, seed: int = None
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """

    Sequentially (i) sorts the inputted X and Y arrays, (ii) splits into training and test sets, and then (iii) shuffles
    the training and test sets

    Parameters
    ----------
    X: np.ndarray
        X array containing variables data
    Y: np.ndarray
        Y array containing objectives data with shape (y, )
    test_ratio: float, Default = 0.2
        The proportion of inputted X and Y arrays to be split into the test set
    seed: int, Default = None
        The seed used for shuffling the data sets to ensure that it is consistent
    Returns
    -------
    X_train: np.ndarray
        X array to be used as training data
    X_test: np.ndarray
        x array to be used as test data
    Y_train: np.ndarray
        Y array to be used as training data
    Y_test: np.ndarray
        Y array to be used as test data

    """
    splitnum = int(1 / test_ratio)

    X_sorted, Y_sorted = sort(X, Y)

    X_train, X_test = train_test_split(X_sorted, splitnum)
    Y_train, Y_test = train_test_split(Y_sorted, splitnum)

    if seed == None:
        seed = 1
    # np.random.seed(seed)  # setting the random seed
    X_train, Y_train = shuffle(X_train, Y_train, seed)
    X_test, Y_test = shuffle(X_test, Y_test, seed)

    return X_train, X_test, Y_train, Y_test


def sort_train_val_test_split_shuffle(
    X: np.ndarray, Y: np.ndarray, test_ratio: float = 0.2, seed: int = None
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """

    Sequentially (i) sorts the inputted X and Y arrays, (ii) splits into training, validation, and test sets, and then
    (iii) shuffles the training, validation, and test sets

    Parameters
    ----------
    X: np.ndarray
        X array containing variables data
    Y: np.ndarray
        Y array containing objectives data with shape (y, )
    test_ratio: float, Default = 0.2
        The proportion of inputted X and Y arrays to be split into the test set
    seed: int, Default = None
        The seed used for shuffling the data sets to ensure that it is consistent
    Returns
    -------
    X_train: np.ndarray
        X array to be used as training data
    X_val: np.ndarray
        x array to be used as validation data
    X_test: np.ndarray
        x array to be used as test data
    Y_train: np.ndarray
        Y array to be used as training data
    Y_val: np.ndarray
        Y array to be used as validation data
    Y_test: np.ndarray
        Y array to be used as test data

    """
    splitnum = int(1 / test_ratio)

    X_sorted, Y_sorted = sort(X, Y)

    X_train, X_val, X_test = train_val_test_split(X_sorted, splitnum)
    Y_train, Y_val, Y_test = train_val_test_split(Y_sorted, splitnum)

    if seed == None:
        seed = 1
    # np.random.seed(seed)  # setting the random seed
    X_train, Y_train = shuffle(X_train, Y_train, seed)
    X_val, Y_val = shuffle(X_val, Y_val, seed)
    X_test, Y_test = shuffle(X_test, Y_test, seed)

    return X_train, X_val, X_test, Y_train, Y_val, Y_test
