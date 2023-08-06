from collections import abc, OrderedDict
from typing import Any, Dict, Iterable, Optional, Union

import numpy as np
import pandas as pd

from aporia.core.context import get_context
from aporia.core.errors import AporiaError, handle_error
from aporia.core.types.field import FieldSchema, FieldType, FieldValue


def _dtype_to_field_type(dtype: str) -> Optional[FieldSchema]:
    # This is based on https://numpy.org/doc/stable/reference/generated/numpy.dtype.kind.html#numpy.dtype.kind
    DTYPE_TO_FIELD_TYPE = {
        "b": FieldType.BOOLEAN,
        "i": FieldType.NUMERIC,
        "u": FieldType.NUMERIC,
        "f": FieldType.NUMERIC,
        "M": FieldType.DATETIME,
        "O": FieldType.STRING,
        "S": FieldType.STRING,
        "U": FieldType.STRING,
    }
    field_type = DTYPE_TO_FIELD_TYPE.get(dtype)
    if field_type is None:
        return None
    return {"type": field_type.value}


NUMERIC_DTYPES = ["i", "u", "f"]
STRING_DTYPES = ["O", "S", "U"]
STRING_UNIQUE_RATIO = 0.25
MIN_UNIQUE_VALUES_FOR_TEXT = 50


def _infer_string_data_for_text_or_string(data: pd.Series) -> FieldSchema:
    """Convert a numpy/pandas of series contains only strings to a FieldType.

    Args:
        data: pandas data series

    Returns:
        FieldType that matches the dtype
    """
    # We need to decided if a string type is str or text
    # We check if there are more than 50 unique values
    # which are more than 25% of the total values
    _, unique_counts = np.unique(data.values, return_counts=True)
    uniques = len(unique_counts)
    if uniques > MIN_UNIQUE_VALUES_FOR_TEXT and uniques > data.shape[0] * STRING_UNIQUE_RATIO:
        return {"type": FieldType.TEXT.value}

    return {"type": FieldType.STRING.value}


def _replace_na_type(data: pd.Series) -> pd.Series:
    """Replace NAType with NA (since they are not removed by dropna).

    Args:
        data: pandas data series

    Returns:
        The data series where the NAType objects are replaced with NA
    """
    result = data
    if data.apply(lambda x: x == pd._libs.missing.NAType).any():
        result = data.copy()
        for i, value in result.iteritems():
            if value == pd._libs.missing.NAType:
                result.at[i] = pd.NA
    return result


def _infer_object_dtype_column(data: pd.Series) -> Optional[FieldSchema]:
    """Attempts to convert a numpy/pandas series of object dtype to a FieldType.

    Args:
        data: pandas data series

    Returns:
        FieldType that matches the dtype, or None if conversion is impossible
    """
    if data.size == 0:
        return None
    elif data.apply(lambda x: isinstance(x, dict)).all():
        return {"type": FieldType.DICT.value}
    elif data.apply(lambda x: isinstance(x, str)).all():
        return _infer_string_data_for_text_or_string(data=data)
    elif data.apply(lambda x: isinstance(x, abc.Iterable)).all():
        return {"type": FieldType.TENSOR.value, "dimensions": [len(data.values[0])]}
    return None


def infer_field_schema_from_dtype_and_data(
    dtype: np.dtype, data: Optional[pd.Series]
) -> Optional[FieldSchema]:
    """Attempts to convert a numpy/pandas dtype to a FieldType.

    Args:
        dtype: Dtype to convert
        data: pandas data series

    Returns:
        FieldType that matches the dtype, or None if conversion is impossible
    """
    if isinstance(dtype, pd.api.types.CategoricalDtype):
        category_type = _dtype_to_field_type(dtype.categories.dtype.kind)
        # We only support categorical fields with numeric categories
        if category_type is None:
            return None
        if category_type["type"] == FieldType.NUMERIC.value:
            return {"type": FieldType.CATEGORICAL.value}

        return category_type

    if dtype.kind == "O":
        return _infer_object_dtype_column(data=data)

    if data is not None and not data.empty:
        if dtype.kind in NUMERIC_DTYPES and isinstance(data.values[0], abc.Iterable):
            arr: Any = data.values[0]
            return {"type": FieldType.TENSOR.value, "dimensions": [len(arr)]}

        # We need to decided if a string type is str or text
        # We check if there are more than 50 unique values
        # which are more than 25% of the total values
        if dtype.kind in STRING_DTYPES and len(data.shape) > 0:

            return _infer_string_data_for_text_or_string(data=data)

    return _dtype_to_field_type(dtype.kind)  # type: ignore


def pandas_to_dict(data: Union[pd.DataFrame, pd.Series]) -> Optional[Dict[str, FieldValue]]:
    """Converts a pandas DataFrame or Series to a dict for log_* functions.

    Args:
        data: DataFrame or Series to convert.

    Returns:
        The data converted to a dict, mapping field names to their values

    Notes:
        * data must contain column names that match the fields defined in create_model_version
        * If data is a DataFrame, it must contain exactly one row
    """
    context = None
    try:
        context = get_context()

        if isinstance(data, pd.Series):
            return data.fillna(np.nan).to_dict()  # type: ignore
        elif isinstance(data, pd.DataFrame):
            num_rows, _ = data.shape
            if num_rows > 1:
                raise AporiaError("cannot convert DataFrame with more than 1 row")

            return data.iloc[0].fillna(np.nan).to_dict()
        else:
            raise AporiaError("data must be a pandas DataFrame or Series")

    except Exception as err:
        handle_error(
            message_format="Converting pandas data to dict failed, {}",
            verbose=False if context is None else context.config.verbose,
            throw_errors=False if context is None else context.config.throw_errors,
            debug=False if context is None else context.config.debug,
            original_exception=err,
        )

    return None


def infer_schema_from_dataframe(data: pd.DataFrame) -> Optional[Dict[str, Dict]]:
    """Infers model version schema from a pandas DataFrame or Series.

    Field names and types are inferred from column names and types.

    Args:
        data: pandas DataFrame or Series

    Returns:
        A schema describing the data, as required by the create_model_version function.

    Notes:
        * The field types are inferred using the following logic, based on the column dtypes:
            * dtype="category" with numeric (integer of float) categories -> categorical field
            * dtype="category" with non-numeric categories -> See rules below
            * Array of numeric values (integer or float) -> vector field
            * dtype="bool" -> boolean field
            * dtypes that represent signed/unsigned integers and floating point numbers -> numeric field
            * dtype is "string", "unicode", "object" -> string field
            * dtype is "string", "unicode", "object", more than 50 values which more than
                25% of them are unique -> text field
            * dtype is any datetime type (with or without timezone) -> datetime field
        * If data contains a column with a type that doesn't match any of the rules
          described above, an error will be raised.
    """
    if not isinstance(data, pd.DataFrame):
        raise AporiaError(f"cannot infer schema from {type(data)}, data must be a pandas DataFrame")

    schema = OrderedDict()
    not_inferable_columns = []
    for column_name, values in data.items():
        column_name = str(column_name)

        values_without_nulls = _replace_na_type(values)
        values_without_nulls = values_without_nulls.dropna().infer_objects()

        column_type = infer_field_schema_from_dtype_and_data(
            values_without_nulls.dtype, values_without_nulls
        )
        if column_type is None:
            not_inferable_columns.append(column_name)
        else:
            schema[column_name] = column_type

    if len(not_inferable_columns) > 0:
        raise AporiaError(
            f"Could not infer the type of columns {not_inferable_columns}. "
            "To fix, make sure to set column dtype. For example "
            f"df['{not_inferable_columns[0]}'] = df['{not_inferable_columns[0]}'].astype(np.int32)"
        )

    return schema


def create_null_dataframe(size: int, columns: Iterable[str]) -> pd.DataFrame:
    """Creates a dataframe with nulls for each column.

    Args:
        size: Number of rows to create.
        columns: Iterable of column names.

    Returns:
        Dataframe with nulls for each column.
    """
    return pd.DataFrame({column: [None for _ in range(size)] for column in columns})
