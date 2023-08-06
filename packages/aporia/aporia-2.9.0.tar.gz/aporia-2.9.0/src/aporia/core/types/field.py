from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Union

FieldValue = Union[float, int, str, bool, datetime, List[int]]

FieldSchema = Dict[str, Any]


class FieldType(Enum):
    """Field types."""

    NUMERIC = "numeric"
    CATEGORICAL = "categorical"
    STRING = "string"
    BOOLEAN = "boolean"
    DATETIME = "datetime"
    VECTOR = "vector"
    TEXT = "text"
    DICT = "dict"
    TENSOR = "tensor"


class FieldCategory(Enum):
    """Field categories."""

    FEATURES = "features"
    PREDICTIONS = "predictions"
    METRICS = "metrics"
    RAW_INPUTS = "raw_inputs"

    @staticmethod
    def from_camel_case(value: str) -> "FieldCategory":
        """Builds a field cateogry from a camelCase string.

        Args:
            value: Category value

        Returns:
            Category that matches the given value
        """
        if value == "rawInputs":
            return FieldCategory.RAW_INPUTS

        return FieldCategory(value)
