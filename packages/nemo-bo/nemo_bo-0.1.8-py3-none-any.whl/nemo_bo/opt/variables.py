import copy
import os
from attrs import define, field

# from dataclasses import dataclass
from typing import Any, List, Optional, Union

import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder, StandardScaler

import nemo_bo.utils.logger as logging_nemo
from nemo_bo.utils.transformations import Transformations

try:
    logging_nemo.logging_path
    logger = logging_nemo.logging_nemo_child(os.path.basename(__file__))
except AttributeError:
    logger = logging_nemo.logging_nemo_master(os.path.basename(__file__))


@define
class ContinuousVariable:
    """

    Class for a variable with continuous values

    Parameters
    ----------
    name: str
        Name of the variable
    lower_bound: int | float
        The lower bound of the variable
    upper_bound: int | float
        The upper bound of the variable
    transformation_type: str. Default = None
        The type of transformation that should be applied to the variable for modelling. When left as the default
        None, the modelling uses the default transformations specified by the model type. When specified, can be
        "normalisation", "standardisation", or "none" for min-max normalisation, standardisation to a mean of 0 and a
        standard deviation of 1, or no transformation respectively
    units: str, Default = ""
        The units for the variable

    """

    name: str
    lower_bound: Union[int, float]
    upper_bound: Union[int, float]
    transformation_type: Optional[str] = None
    units: str = ""
    transformations: Transformations = field(init=False)

    def __attrs_post_init__(self):
        self.transformations = None

    def transform(self, X: np.ndarray) -> np.ndarray:
        """

        Fit the transformation scalar to the inputted X array when self.transformation_type is "normalisation" or
        "standardisation". The X array is subsequently transformed according to the fit scalar. When
        self.transformation_type = "none", no transformation occurs

        Parameters
        ----------
        X: np.ndarray
            X array containing untransformed values for one variable

        """
        if self.transformation_type is None:
            raise AttributeError(
                "Please either: 1. Fit the model first, or 2. Set transformation_type = 'none', 'normalisation', or 'standarisation' when creating the variable instance"
            )

        if self.transformation_type == "none":
            return X
        self.transformations = Transformations()
        if self.transformation_type == "normalisation":
            return self.transformations.minmaxscaler(X)
        elif self.transformation_type == "standardisation":
            return self.transformations.standardscaler(X)

    def transform_only(self, X: np.ndarray) -> np.ndarray:
        """

        The X array is transformed according to the fit scalar in the self.transformations object. When
        self.transformation_type = "none", no transformation occurs

        Parameters
        ----------
        X: np.ndarray
            X array containing untransformed values for one variable

        """
        if self.transformation_type is None:
            raise AttributeError(
                "Please either: 1. Fit the model first, or 2. Set transformation_type = 'none', 'normalisation', or 'standarisation' when creating the variable instance"
            )

        if self.transformation_type == "none":
            return X
        if self.transformation_type == "normalisation":
            return self.transformations.minmaxscaler_transform_only(X)
        elif self.transformation_type == "standardisation":
            return self.transformations.standardscaler_transform_only(X)

    def inverse_transform(self, X_transform: np.ndarray) -> np.ndarray:
        """

        The X_transform array undergoes an inverse transform according to the fit scalar in the self.transformations
        object. When self.transformation_type = "none", no transformation occurs

        Parameters
        ----------
        X_transform: np.ndarray
            X array containing transformed values for one variable

        """
        if self.transformation_type == "none":
            return X_transform
        if isinstance(self.transformations.scaler, MinMaxScaler):
            return self.transformations.inverse_minmaxscaler(X_transform)
        elif isinstance(self.transformations.scaler, StandardScaler):
            return self.transformations.inverse_standardscaler(X_transform)


@define(kw_only=True)
class CategoricalVariable:
    """

    Base class for categorical variables

    Parameters
    ----------
    name: str
        Name of the variable
    categorical_levels: List[str | int | float]
        The categories/choices/levels for a given categorical variable
    units: str, Default = ""
        The units for the variable

    """

    name: str
    categorical_levels: List[Union[str, int, float]]
    units: str = ""
    transformations: Transformations = field(init=False)

    def enum_to_cat_level(self, X_array: np.ndarray) -> np.ndarray:
        """

        Converts the categorical level index to its respective name/value

        Parameters
        ----------
        X_array: np.ndarray
            Array of indexes that correspond to the categorical levels for a categorical variable

        Returns
        -------
        np.ndarray
            Array where the indexes that correspond to the categorical levels have been replaced by the name/value

        """
        return np.array([self.categorical_levels[int(x)] for x in X_array])


@define
class CategoricalVariableOneHot(CategoricalVariable):
    """

    Class for categorical variables that will be treated using one-hot encoding

    Parameters
    ----------
    name: str
        Name of the variable
    categorical_levels: List[str | int | float]
        The categories/choices/levels for a given categorical variable
    units: str, Default = ""
        The units for the variable

    """

    num_categorical_levels: int = field(init=False)

    def __attrs_post_init__(self):
        self.num_categorical_levels = len(self.categorical_levels)

    def one_hot_encode(self, X: np.ndarray) -> np.ndarray:
        """

        Converts the categorical levels in an X array to a one-hot-encoding array

        Parameters
        ----------
        X_array: np.ndarray
            Array containing categorical levels as names/values

        Returns
        -------
        np.ndarray
            Array where the categorical levels have been converted using one-hot encoding

        """
        return OneHotEncoder(handle_unknown="ignore", categories=self.categorical_levels).transform(X).toarray()


@define(kw_only=True)
class CategoricalVariableDiscreteValues(CategoricalVariable):
    """

    Class for categorical variables that have levels of discrete values

    Parameters
    ----------
    name: str
        Name of the variable
    categorical_levels: List[str | int | float]
        The categories/choices/levels for a given categorical variable
    units: str, Default = ""
        The units for the variable
    lower_bound: int | float, Default = None
        The lower bound of the variable
    upper_bound: int | float, Default = None
        The upper bound of the variable
    transformation_type: str. Default = None
        The type of transformation that should be applied to the variable for modelling. When left as the default
        None, the modelling uses the default transformations specified by the model type. When specified, can be
        "normalisation", "standardisation", or "none" for min-max normalisation, standardisation to a mean of 0 and a
        standard deviation of 1, or no transformation respectively

    """

    lower_bound: Optional[Union[int, float]] = None
    upper_bound: Optional[Union[int, float]] = None
    transformation_type: Optional[str] = None
    num_categorical_levels: int = field(init=False)

    def __attrs_post_init__(self):
        self.num_categorical_levels = len(self.categorical_levels)
        self.transformations = None
        if self.lower_bound is None:
            self.lower_bound = min(self.categorical_levels)

        if self.upper_bound is None:
            self.upper_bound = max(self.categorical_levels)

    def transform(self, X: np.ndarray) -> np.ndarray:
        """

        Fit the transformation scalar to the inputted X array when self.transformation_type is "normalisation" or
        "standardisation". The X array is subsequently transformed according to the fit scalar. When
        self.transformation_type = "none", no transformation occurs

        Parameters
        ----------
        X: np.ndarray
            X array containing untransformed values for one variable

        """
        if self.transformation_type is None:
            raise AttributeError(
                "Please either: 1. Fit the model first, or 2. Set transformation_type = 'none', 'normalisation', or 'standarisation' when creating the variable instance"
            )

        if self.transformation_type == "none":
            return X
        self.transformations = Transformations()
        if self.transformation_type == "normalisation":
            return self.transformations.minmaxscaler(X)
        elif self.transformation_type == "standardisation":
            return self.transformations.standardscaler(X)

    def transform_only(self, X: np.ndarray) -> np.ndarray:
        """

        The X array is transformed according to the fit scalar in the self.transformations object. When
        self.transformation_type = "none", no transformation occurs

        Parameters
        ----------
        X: np.ndarray
            X array containing untransformed values for one variable

        """
        if self.transformation_type is None:
            raise AttributeError(
                "Please either: 1. Fit the model first, or 2. Set transformation_type = 'none', 'normalisation', or 'standarisation' when creating the variable instance"
            )

        if self.transformation_type == "none":
            return X
        if self.transformation_type == "normalisation":
            return self.transformations.minmaxscaler_transform_only(X)
        elif self.transformation_type == "standardisation":
            return self.transformations.standardscaler_transform_only(X)

    def inverse_transform(self, X_transform: np.ndarray) -> np.ndarray:
        """

        The X_transform array undergoes an inverse transform according to the fit scalar in the self.transformations
        object. When self.transformation_type = "none", no transformation occurs

        Parameters
        ----------
        X_transform: np.ndarray
            X array containing transformed values for one variable

        """
        if self.transformation_type == "none":
            return X_transform
        if isinstance(self.transformations.scaler, MinMaxScaler):
            return self.transformations.inverse_minmaxscaler(X_transform)
        elif isinstance(self.transformations.scaler, StandardScaler):
            return self.transformations.inverse_standardscaler(X_transform)

    def value_to_discrete(self, X: np.ndarray) -> np.ndarray:
        """

        Converts the categorical level index to their closest discrete value

        Parameters
        ----------
        X_array: np.ndarray
            Array containing X values to be converted

        Returns
        -------
        np.ndarray
            Array where the X values have been converted to their closest discrete values

        """

        X_new = copy.copy(X)
        for index, value in enumerate(X):
            diff = ((self.categorical_levels - value) ** 2) ** 0.5
            diff_min_index = np.argmin(diff)
            X_new[index] = self.categorical_levels[diff_min_index]

        return X_new

    def enum_to_discrete(self, X: np.ndarray) -> np.ndarray:
        """

        Converts the categorical level indexes to the corresponding discrete values

        Parameters
        ----------
        X_array: np.ndarray
            Array containing categorical level indexes to be converted

        Returns
        -------
        np.ndarray
            Array where the categorical level indexes have been converted to their corresponding discrete values

        """
        return np.vstack([self.categorical_descriptors[int(x)] for x in X])


@define(kw_only=True)
class CategoricalVariableWithDescriptors(CategoricalVariable):
    """

    Class for categorical variables that have levels which are arrays of descriptor values

    Parameters
    ----------
    name: str
        Name of the variable
    categorical_levels: List[str | int | float]
        The categories/choices/levels for a given categorical variable
    units: str, Default = ""
        The units for the variable
    descriptor_names: List[str]
        The names for each type of descriptor in the descriptor arrays
    categorical_descriptors: List[Any] | np.ndarray
        The array of descriptor values where the shape is [{number of categorical levels}, {number of descriptor types}],
        where each row in the array are the descriptors for each categorical level
    transformation_type: str. Default = None
        The type of transformation that should be applied to the variable for modelling. When left as the default
        None, the modelling uses the default transformations specified by the model type. When specified, can be
        "normalisation", "standardisation", or "none" for min-max normalisation, standardisation to a mean of 0 and a
        standard deviation of 1, or no transformation respectively
    lower_bound: int | float, Default = None
        The lower bound of the variable
    upper_bound: int | float, Default = None
        The upper bound of the variable

    """

    descriptor_names: List[str]
    categorical_descriptors: Union[List[Any], np.ndarray]
    transformation_type: Optional[str] = None
    lower_bound: Optional[Union[int, float]] = None
    upper_bound: Optional[Union[int, float]] = None
    num_categorical_levels: int = field(init=False)
    num_descriptors: int = field(init=False)

    def __attrs_post_init__(self):
        self.num_categorical_levels = len(self.categorical_levels)
        self.transformations = None
        if self.lower_bound is None:
            self.lower_bound = []
            descriptor_range = np.ptp(self.categorical_descriptors, axis=0)
            for descriptor, range in zip(np.array(self.categorical_descriptors).T, descriptor_range):
                self.lower_bound.append(descriptor.min() - (range * 0.10))

        if self.upper_bound is None:
            self.upper_bound = []
            descriptor_range = np.ptp(self.categorical_descriptors, axis=0)
            for descriptor, range in zip(np.array(self.categorical_descriptors).T, descriptor_range):
                self.upper_bound.append(descriptor.max() + (range * 0.10))

        self.num_descriptors = (
            len(self.categorical_descriptors)
            if np.array(self.categorical_descriptors).ndim == 1
            else len(self.categorical_descriptors[0])
        )

    def name_to_descriptor(self, X: np.ndarray) -> np.ndarray:
        """

        Converts the categorical level names into an array of the corresponding descriptor values

        Parameters
        ----------
        X_array: np.ndarray
            Array containing categorical level names to be converted

        Returns
        -------
        np.ndarray
            Array where the categorical level names have been converted to their corresponding descriptor values

        """
        return self.categorical_descriptors[self.categorical_levels.index(X)]

    def name_to_enum(self, X: np.ndarray) -> np.ndarray:
        """

        Converts the categorical level names to the corresponding categorical level index

        Parameters
        ----------
        X_array: np.ndarray
            Array containing categorical level names to be converted

        Returns
        -------
        np.ndarray
            Array where the categorical level names have been converted to their corresponding categorical level index

        """
        return np.vstack([self.categorical_levels.index(x) for x in X])

    def enum_to_descriptor(self, X: np.ndarray) -> np.ndarray:
        """

        Converts the categorical level indexes to the corresponding descriptor values

        Parameters
        ----------
        X_array: np.ndarray
            Array containing categorical level indexes to be converted

        Returns
        -------
        np.ndarray
            Array where the categorical level indexes have been converted to their corresponding descriptor values

        """
        return np.vstack([self.categorical_descriptors[int(x)] for x in X])

    def transform(self, X: np.ndarray) -> np.ndarray:
        """

        Fit the transformation scalar to the inputted X array when self.transformation_type is "normalisation" or
        "standardisation". The X array is subsequently transformed according to the fit scalar. When
        self.transformation_type = "none", no transformation occurs

        Parameters
        ----------
        X: np.ndarray
            X array containing untransformed values for one variable

        """
        if self.transformation_type is None:
            raise AttributeError(
                "Please either: 1. Fit the model first, or 2. Set transformation_type = 'none', 'normalisation', or 'standarisation' when creating the variable instance"
            )

        if self.transformation_type == "none":
            return X
        self.transformations = Transformations()
        if self.transformation_type == "normalisation":
            return self.transformations.minmaxscaler(X)
        elif self.transformation_type == "standardisation":
            return self.transformations.standardscaler(X)

    def transform_only(self, X: np.ndarray) -> np.ndarray:
        """

        The X array is transformed according to the fit scalar in the self.transformations object. When
        self.transformation_type = "none", no transformation occurs

        Parameters
        ----------
        X: np.ndarray
            X array containing untransformed values for one variable

        """
        if self.transformation_type is None:
            raise AttributeError(
                "Please either: 1. Fit the model first, or 2. Set transformation_type = 'none', 'normalisation', or 'standarisation' when creating the variable instance"
            )

        if self.transformation_type == "none":
            return X
        if self.transformation_type == "normalisation":
            return self.transformations.minmaxscaler_transform_only(X)
        elif self.transformation_type == "standardisation":
            return self.transformations.standardscaler_transform_only(X)

    def inverse_transform(self, X_transform: np.ndarray) -> np.ndarray:
        """

        The X_transform array undergoes an inverse transform according to the fit scalar in the self.transformations
        object. When self.transformation_type = "none", no transformation occurs

        Parameters
        ----------
        X_transform: np.ndarray
            X array containing transformed values for one variable

        """
        if self.transformation_type == "none":
            return X_transform
        if isinstance(self.transformations.scaler, MinMaxScaler):
            return self.transformations.inverse_minmaxscaler(X_transform)
        elif isinstance(self.transformations.scaler, StandardScaler):
            return self.transformations.inverse_standardscaler(X_transform)


@define
class VariablesList:
    """

    Class that stores all variables and their respective properties

    Parameters
    ----------
    objectives: List[Objective]
        A list of ContinuousVariable and/or CategoricalVariable objects

    """

    variables: List[Union[ContinuousVariable, CategoricalVariable]]
    names: List[str] = field(init=False)
    units: List[str] = field(init=False)
    num_cat_onehot_var: int = field(init=False)
    num_cat_discrete_var: int = field(init=False)
    num_cat_descriptor_var: int = field(init=False)
    num_cat_var: int = field(init=False)
    categorical_levels: List[List[Union[str, int]]] = field(init=False)
    num_categorical_levels: int = field(init=False)
    descriptor_names: List[List[str]] = field(init=False)
    categorical_descriptors: List[List[str]] = field(init=False)
    num_descriptors: List[int] = field(init=False)
    lower_bounds: List[Union[int, float]] = field(init=False)
    upper_bounds: List[Union[int, float]] = field(init=False)
    var_splitter_indexes: List[int] = field(init=False)
    n_var: int = field(init=False)
    continuous_var_names: List[str] = field(init=False)

    def __attrs_post_init__(self):
        self.names = [var.name for var in self.variables]
        self.units = [var.units for var in self.variables]

        # Counts the number of each type of categorical variables, and the total number of categorical variables
        self.num_cat_onehot_var = sum(isinstance(var, CategoricalVariableOneHot) for var in self.variables)
        self.num_cat_discrete_var = sum(isinstance(var, CategoricalVariableDiscreteValues) for var in self.variables)
        self.num_cat_descriptor_var = sum(isinstance(var, CategoricalVariableWithDescriptors) for var in self.variables)
        self.num_cat_var = self.num_cat_onehot_var + self.num_cat_discrete_var + self.num_cat_descriptor_var

        # List of the categorical levels for every categorical variables
        self.categorical_levels = [
            var.categorical_levels if not isinstance(var, ContinuousVariable) else None for var in self.variables
        ]
        # List of the number of categorical levels for every categorical variables
        self.num_categorical_levels = [
            var.num_categorical_levels if not isinstance(var, ContinuousVariable) else 0 for var in self.variables
        ]
        # List of descriptor names for every categorical variable with descriptors
        self.descriptor_names = [
            var.descriptor_names if isinstance(var, CategoricalVariableWithDescriptors) else None
            for var in self.variables
        ]
        # List of descriptor value arrays for every categorical variable with descriptors
        self.categorical_descriptors = [
            var.categorical_descriptors if isinstance(var, CategoricalVariableWithDescriptors) else None
            for var in self.variables
        ]
        # List of the number of descriptors in every categorical variable with descriptors
        self.num_descriptors = [
            var.num_descriptors if isinstance(var, CategoricalVariableWithDescriptors) else 0 for var in self.variables
        ]

        # Creates lists of lower and upper bounds for all variables (where applicable), and a list that contains
        # indexes that indicate where to split the X array to separate each variable
        (self.lower_bounds, self.upper_bounds, self.var_splitter_indexes, categorical_descriptor_index_range,) = (
            [],
            [],
            [],
            [],
        )
        var_counter = 0
        for var_index, var in enumerate(self.variables):
            if isinstance(var, ContinuousVariable) or isinstance(var, CategoricalVariableDiscreteValues):
                self.lower_bounds.append(var.lower_bound)
                self.upper_bounds.append(var.upper_bound)
                var_counter += 1
            elif isinstance(var, CategoricalVariableOneHot):
                var_counter += var.num_categorical_levels
            elif isinstance(var, CategoricalVariableWithDescriptors):
                for lower_value, upper_value in zip(var.lower_bound, var.upper_bound):
                    self.lower_bounds.append(lower_value)
                    self.upper_bounds.append(upper_value)

                categorical_descriptor_index_range.append(
                    [var.name, var_index, var_counter, var_counter + var.num_descriptors,]
                )
                var_counter += var.num_descriptors
            if var_index + 1 < len(self.variables):
                self.var_splitter_indexes.append(var_counter)

        self.n_var = var_counter

        # List of variables names for all continuous variables, categorical variables with discrete values, and the
        # descriptor names in categorical variables with descriptors
        self.continuous_var_names = []
        for var in self.variables:
            if isinstance(var, ContinuousVariable) or isinstance(var, CategoricalVariableDiscreteValues):
                self.continuous_var_names.append(var.name)
            elif isinstance(var, CategoricalVariableWithDescriptors):
                for descriptor_name in var.descriptor_names:
                    self.continuous_var_names.append(descriptor_name)

    def transform(self, X: np.ndarray, transform_type: Optional[str] = None) -> np.ndarray:
        """

        Fits and transforms the X array containing data for multiple variables based on each variables'
        transformation_type attribute

        Parameters
        ----------
        X: np.ndarray
            X array containing untransformed values for all variables
        transform_type: str, Default = None
            Assigns the transformation type if one was not specified when the variable object was created

        Returns
        -------
        np.ndarray
            X array containing transformed values for all variables

        """
        X_split = self.split_var(X)
        for var_index, var in enumerate(self.variables):
            if not isinstance(var, CategoricalVariableOneHot):
                if var.transformation_type is None:
                    var.transformation_type = transform_type

                if X_split[var_index].shape[1] == 1:
                    X_split[var_index] = var.transform(X_split[var_index]).reshape(-1, 1)
                else:
                    X_split[var_index] = var.transform(X_split[var_index])

        return np.hstack(X_split)

    def transform_only(self, X: np.ndarray) -> np.ndarray:
        """

        Transforms the X array containing data for multiple variables based on each variables' transformation_type
        attribute using the previously fitted scalars

        Parameters
        ----------
        X: np.ndarray
            X array containing untransformed values for all variables

        Returns
        -------
        np.ndarray
            X array containing transformed values for all variables

        """
        X_split = self.split_var(X)
        for var_index, var in enumerate(self.variables):
            if not isinstance(var, CategoricalVariableOneHot):
                if X_split[var_index].shape[1] == 1:
                    X_split[var_index] = var.transform_only(X_split[var_index]).reshape(-1, 1)
                else:
                    X_split[var_index] = var.transform_only(X_split[var_index])

        return np.hstack(X_split)

    def inverse_transform(self, X: np.ndarray) -> np.ndarray:
        """

        The inputted X array containing data for multiple variables undergoes an inverse transformaion using the
        previously fitted scalars

        Parameters
        ----------
        X: np.ndarray
            X array containing transformed values for all variables

        Returns
        -------
        np.ndarray
            X array containing untransformed values for all variables

        """
        X_split = self.split_var(X)
        for var_index, var in enumerate(self.variables):
            if not isinstance(var, CategoricalVariableOneHot):
                if X_split[var_index].shape[1] == 1:
                    X_split[var_index] = var.inverse_transform(X_split[var_index]).reshape(-1, 1)
                else:
                    X_split[var_index] = var.inverse_transform(X_split[var_index])

        return np.hstack(X_split)

    def categorical_transform(self, X: np.ndarray) -> np.ndarray:
        """

        Transforms all categorical data in the X array according to their categorical variable type:
        - CategoricalVariableOneHot: Converts the categorical levels in an X array to a one-hot-encoding array
        - CategoricalVariableDiscreteValues: Converts the categorical level index to their closest discrete value
        - CategoricalVariableWithDescriptors: Converts the categorical level names into an array of the corresponding
        descriptor values

        Parameters
        ----------
        X: np.ndarray
            X array containing untransformed values for all categorical variables. Any continuous variable data in the
            array are unaffected

        Returns
        -------
        np.ndarray
            X array containing transformed values for all categorical variables. Any continuous variable data in the
            array are unaffected

        """
        X_transform = np.zeros_like(X, dtype=np.object)
        for var_index, var in enumerate(self.variables):
            if isinstance(var, CategoricalVariableOneHot):
                for index in range(X_transform[:, var_index].shape[0]):
                    X_transform[index, var_index] = var.one_hot_encode(X[index, var_index])
            elif isinstance(var, CategoricalVariableDiscreteValues):
                X_transform[:, var_index] = var.value_to_discrete(X[:, var_index])
            elif isinstance(var, CategoricalVariableWithDescriptors):
                for index in range(X_transform[:, var_index].shape[0]):
                    X_transform[index, var_index] = var.name_to_descriptor(X[index, var_index])
            elif isinstance(var, ContinuousVariable):
                X_transform[:, var_index] = X[:, var_index]

        return np.array([np.hstack(row) for row in X_transform]).astype(float)

    def descriptor_to_name(self, X: np.ndarray) -> np.ndarray:
        """

        Transforms all X values that correspond to descriptor values for categorical variables to their respective
        categorical level name according to the shortest normalised euclidean distance

        Parameters
        ----------
        X: np.ndarray
            X array containing untransformed values for all categorical variables. Any continuous variable data in the
            array are unaffected

        Returns
        -------
        np.ndarray
            X array containing transformed values for all categorical variables. Any continuous variable data in the
            array are unaffected

        """
        X_split = self.split_var(X)
        for var_index, var in enumerate(self.variables):
            if isinstance(var, CategoricalVariableWithDescriptors):
                cat_name_list = []
                for x in X_split[var_index]:
                    # Normalises the x array
                    x_norm = (x - np.array(var.lower_bound)) / (np.array(var.upper_bound) - np.array(var.lower_bound))
                    # Normalises this categorical variable's descriptor array
                    norm_categorical_descriptors = (var.categorical_descriptors - np.array(var.lower_bound)) / (
                        np.array(var.upper_bound) - np.array(var.lower_bound)
                    )
                    # Calculates the normalised euclidean distance for the normalised x array against every categorical
                    # level's normalised descriptor array
                    euc_dist = [np.linalg.norm(cat_level - x_norm) for cat_level in norm_categorical_descriptors]
                    # Identifies the categorical level index with the shortest normalised euclidean distance
                    euc_dist_min_index = np.argmin(euc_dist)
                    cat_name_list.append([var.categorical_levels[euc_dist_min_index]])
                X_split[var_index] = np.array(cat_name_list)

        return np.hstack(X_split)

    def categorical_values_euc(self, X: np.ndarray) -> np.ndarray:
        """

        Transforms all X values that correspond to descriptor
         values or discrete values for categorical variables to
        their categorical value(s) according to the shortest normalised euclidean distance

        Parameters
        ----------
        X: np.ndarray
            X array containing untransformed values for all categorical variables. Any continuous variable data in the
            array are unaffected

        Returns
        -------
        np.ndarray
            X array containing transformed values for all categorical variables. Any continuous variable data in the
            array are unaffected

        """
        X_split = self.split_var(X)
        for var_index, var in enumerate(self.variables):
            if isinstance(var, CategoricalVariableDiscreteValues):
                X_split[var_index] = var.value_to_discrete(X_split[var_index])
        X = np.hstack(X_split).astype(np.float)

        if any(isinstance(var, CategoricalVariableWithDescriptors) for var in self.variables):
            X = self.value_to_descriptor(X)

        return X

    def value_to_descriptor(self, X_array: np.ndarray) -> np.ndarray:
        """

        Transforms all X values that correspond to descriptors for categorical variables to descriptors values that are
        at the shortest normalised euclidean distance

        Parameters
        ----------
        X: np.ndarray
            X array containing untransformed values for all categorical variables. Any continuous variable data in the
            array are unaffected

        Returns
        -------
        np.ndarray
            X array containing transformed values for all categorical variables. Any continuous variable data in the
            array are unaffected

        """
        X_split = self.split_var(X_array)
        for var_index, var in enumerate(self.variables):
            if isinstance(var, CategoricalVariableWithDescriptors):
                cat_descriptor_list = []
                for x in X_split[var_index]:
                    x_norm = (x - np.array(var.lower_bound)) / (np.array(var.upper_bound) - np.array(var.lower_bound))
                    norm_categorical_descriptors = (var.categorical_descriptors - np.array(var.lower_bound)) / (
                        np.array(var.upper_bound) - np.array(var.lower_bound)
                    )
                    euc_dist = [np.linalg.norm(cat_level - x_norm) for cat_level in norm_categorical_descriptors]
                    # euc_dist = [np.linalg.norm(cat_level - x) for cat_level in np.array(var.categorical_descriptors)]
                    euc_dist_min_index = np.argmin(euc_dist)
                    cat_descriptor_list.append(var.categorical_descriptors[euc_dist_min_index])
                # X_split[var_index] = np.array(cat_descriptor_list).reshape(1, -1)
                X_split[var_index] = np.array(cat_descriptor_list)

        return np.hstack(X_split)

    def enum_to_values(self, X_array: np.ndarray) -> np.ndarray:
        """

        Converts the categorical level indexes in the X values for categorical variables with discrete or descriptor
        values to the corresponding discrete or descriptor values

        Parameters
        ----------
        X_array: np.ndarray
            Array containing categorical level indexes to be converted

        Returns
        -------
        np.ndarray
            Array where the categorical level indexes have been converted to their corresponding descriptor values

        """
        X_array_object = X_array.astype(np.object)
        for var_index, var in enumerate(self.variables):
            if isinstance(var, CategoricalVariableWithDescriptors):
                X_array_object[:, var_index] = var.enum_to_descriptor(X_array[:, var_index])
            elif isinstance(var, CategoricalVariableDiscreteValues):
                X_array_object[:, var_index] = var.enum_to_discrete(X_array[:, var_index])

        return X_array_object.astype("float64")

    def name_to_descriptor(self, X_array: np.ndarray) -> np.ndarray:
        """

        Converts the categorical level names in the X values for categorical variables with descriptor values to the
        corresponding descriptor arrays

        Parameters
        ----------
        X_array: np.ndarray
            Array containing categorical level indexes to be converted

        Returns
        -------
        np.ndarray
            Array where the categorical level indexes have been converted to their corresponding descriptor arrays

        """
        X_array_object = X_array.astype(np.object)
        for var_index, var in enumerate(self.variables):
            if isinstance(var, CategoricalVariableWithDescriptors):
                X_array_object[:, var_index] = var.name_to_descriptor(X_array[:, var_index])

        return X_array_object.astype("float64")

    # def reshape_to_2d(self, X_array: np.ndarray) -> np.ndarray:
    #     return np.hstack(X_array.ravel().tolist()).reshape(X_array.shape[0], self.n_var)

    def split_var(self, X_array: np.ndarray) -> List[np.ndarray]:
        """

        Splits an X-array that contains the continuous and categorical variables into a list of sub-arrays for each
        individual variable

        Parameters
        ----------
        X_array: np.ndarray
             X-array that contains the continuous and categorical variables, where the categorical variables are
             specified in their categorical levels (and not as descriptors for example)

        Returns
        -------
        List[np.ndarray]
            List of sub-arrays for each individual variable

        """
        return np.split(X_array, self.var_splitter_indexes, axis=1)

    def append(self, var: Union[ContinuousVariable, CategoricalVariable]):
        """

        Function for appending an additional variable to the current VariablesList object

        Parameters
        ----------
        var: ContinuousVariable | CategoricalVariable
            ContinuousVariable or CategoricalVariable variable

        """
        var_list = copy.copy(self.variables)
        var_list.append(var)

        return VariablesList(var_list)
