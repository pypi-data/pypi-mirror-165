import numpy as np
import pandas as pd
from typing import Tuple, Union

from nemo_bo.opt.objectives import CalculableObjective, RegressionObjective, ObjectivesList
from nemo_bo.opt.variables import (
    CategoricalVariableWithDescriptors,
    CategoricalVariableDiscreteValues,
    ContinuousVariable,
    VariablesList,
)


def extract_input_template(input_template_xlsx: str) -> Tuple[np.ndarray, np.ndarray, VariablesList, ObjectivesList]:
    """
    Function that can extract user-inputted variables and objectives information and data from the input template provided

    Parameters
    ----------
    input_template_xlsx: str
        Excel file for the input template containing the variables, objectives, and data

    Returns
    -------
    X: np.ndarry
        Data for the variables
    Y: np.ndarray
        Data for the objectives
    var_list: VariablesList
        Object that contains all of the variables information
    obj_list: VariablesList
        Object that contains all of the objectives information
    """
    input_template = pd.read_excel(input_template_xlsx, sheet_name=None, index_col=0)

    var_list = []
    for var_index, var_type in enumerate(input_template["Variables"].columns):
        if "ContinuousVariable" in var_type:
            var_list.append(
                ContinuousVariable(
                    name=input_template["Variables"].loc["name"][var_index],
                    lower_bound=input_template["Variables"].loc["lower_bound"][var_index],
                    upper_bound=input_template["Variables"].loc["upper_bound"][var_index],
                    transformation_type=input_template["Variables"].loc["transformation_type"][var_index]
                    if not pd.isnull(input_template["Variables"].loc["transformation_type"][var_index])
                    else None,
                    units=input_template["Variables"].loc["units"][var_index]
                    if not pd.isnull(input_template["Variables"].loc["units"][var_index])
                    else None,
                )
            )
        elif "CategoricalVariableDiscreteValues" in var_type:
            name = input_template["Variables"].loc["name"][var_index]
            var_list.append(
                CategoricalVariableDiscreteValues(
                    name=name,
                    categorical_levels=list(input_template[name].index),
                    lower_bound=input_template["Variables"].loc["lower_bound"][var_index]
                    if not pd.isnull(input_template["Variables"].loc["lower_bound"][var_index])
                    else None,
                    upper_bound=input_template["Variables"].loc["upper_bound"][var_index]
                    if not pd.isnull(input_template["Variables"].loc["upper_bound"][var_index])
                    else None,
                    transformation_type=input_template["Variables"].loc["transformation_type"][var_index]
                    if not pd.isnull(input_template["Variables"].loc["transformation_type"][var_index])
                    else None,
                    units=input_template["Variables"].loc["units"][var_index]
                    if not pd.isnull(input_template["Variables"].loc["units"][var_index])
                    else None,
                )
            )
        elif "CategoricalVariableWithDescriptors" in var_type:
            name = input_template["Variables"].loc["name"][var_index]
            var_list.append(
                CategoricalVariableWithDescriptors(
                    name=name,
                    categorical_levels=list(input_template[name].index),
                    descriptor_names=list(input_template[name].columns),
                    categorical_descriptors=input_template[name].values,
                    lower_bound=input_template["Variables"].loc["lower_bound"][var_index]
                    if not pd.isnull(input_template["Variables"].loc["lower_bound"][var_index])
                    else None,
                    upper_bound=input_template["Variables"].loc["upper_bound"][var_index]
                    if not pd.isnull(input_template["Variables"].loc["upper_bound"][var_index])
                    else None,
                    transformation_type=input_template["Variables"].loc["transformation_type"][var_index]
                    if not pd.isnull(input_template["Variables"].loc["transformation_type"][var_index])
                    else None,
                    units=input_template["Variables"].loc["units"][var_index]
                    if not pd.isnull(input_template["Variables"].loc["units"][var_index])
                    else None,
                )
            )

    obj_list = []
    for obj_index, obj_type in enumerate(input_template["Objectives"].columns):
        if "RegressionObjective" in obj_type:
            obj_list.append(
                RegressionObjective(
                    name=input_template["Objectives"].loc["name"][obj_index],
                    obj_max_bool=input_template["Objectives"].loc["obj_max_bool"][obj_index],
                    lower_bound=input_template["Objectives"].loc["lower_bound"][obj_index],
                    upper_bound=input_template["Objectives"].loc["upper_bound"][obj_index],
                    transformation_type=input_template["Objectives"].loc["transformation_type"][obj_index]
                    if not pd.isnull(input_template["Objectives"].loc["transformation_type"][obj_index])
                    else None,
                    units=input_template["Objectives"].loc["units"][obj_index]
                    if not pd.isnull(input_template["Objectives"].loc["units"][obj_index])
                    else None,
                    predictor_type=[input_template["Objectives"].loc["predictor_type"][obj_index]]
                    if not pd.isnull(input_template["Objectives"].loc["predictor_type"][obj_index])
                    else None,
                )
            )
        elif "CalculableObjective" in obj_type:
            obj_list.append(
                CalculableObjective(
                    name=input_template["Objectives"].loc["name"][obj_index],
                    obj_max_bool=input_template["Objectives"].loc["obj_max_bool"][obj_index],
                    lower_bound=input_template["Objectives"].loc["lower_bound"][obj_index],
                    upper_bound=input_template["Objectives"].loc["upper_bound"][obj_index],
                    units=input_template["Objectives"].loc["units"][obj_index]
                    if not pd.isnull(input_template["Objectives"].loc["units"][obj_index])
                    else None,
                )
            )

    X = input_template["Variables"].iloc[5:, :].values
    Y = input_template["Objectives"].iloc[7:, :].values.astype(float)
    var_list = VariablesList(var_list)
    obj_list = ObjectivesList(obj_list)

    return X, Y, var_list, obj_list
