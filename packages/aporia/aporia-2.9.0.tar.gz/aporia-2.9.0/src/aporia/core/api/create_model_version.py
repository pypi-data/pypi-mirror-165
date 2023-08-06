import logging
from typing import Any, Dict, List, Mapping, Optional, Union

from aporia.core.errors import AporiaError
from aporia.core.http_client import HttpClient
from aporia.core.logging_utils import LOGGER_NAME
from aporia.core.types.field import FieldSchema

logger = logging.getLogger(LOGGER_NAME)


async def run_create_model_version_query(
    http_client: HttpClient,
    model_id: str,
    model_version: str,
    model_type: str,
    features: Mapping[str, Union[FieldSchema, str]],
    predictions: Mapping[str, Union[FieldSchema, str]],
    raw_inputs: Optional[Mapping[str, Union[FieldSchema, str]]] = None,
    metrics: Optional[Dict[str, str]] = None,
    model_data_type: Optional[str] = None,
    labels: Optional[List[str]] = None,
    feature_importance: Optional[Dict[str, float]] = None,
    mapping: Optional[Dict[str, str]] = None,
):
    """Defines the schema for a specific model version.

    Args:
        http_client: Http client
        model_id: Model ID
        model_version: Model Version
        model_type: Model type
        features: Feature fields
        predictions: Prediction fields
        raw_inputs: Raw input fields.
        metrics: Prediction metric fields.
        model_data_type: Model data type.
        labels: Labels of multi-label, multiclass or binary model. Deprecated.
        feature_importance: Features' importance.
        mapping: General mapping. See Notes.

    Notes:
        Allowed mapping fields are:
            * batch_id_column_name: The name of the key in the `raw_inputs`
                dict that holds the value of the `batch_id`.
            * relevance_column_name: The name of the key in the `predictions`
                dict that holds the value of the `relevance` score of models of type `ranking`.
            * actual_relevance_column_name: The name of the key in the `actuals`
                dict that holds the value of the `relevance` score of models of type `ranking`.
    """
    await _validate_model_schema(
        http_client=http_client,
        model_schema={"features": features, "predictions": predictions, "raw_inputs": raw_inputs},
    )
    model_version_input = {
        "name": model_version,
        "model_type": model_type,
        "version_schema": {
            "features": features,
            "predictions": predictions,
            "raw_inputs": raw_inputs if raw_inputs is not None else None,
            "metrics": metrics,
            "feature_positions": generate_feature_positions(features),
        },
        "model_data_type": model_data_type,
        "labels": labels,
        "feature_importance": feature_importance,
        "mapping": mapping,
    }

    await http_client.post(
        url=f"/models/{model_id}/versions",
        data=model_version_input,
    )


async def _validate_model_schema(
    http_client: HttpClient,
    model_schema: Mapping[str, Optional[Mapping[str, Union[FieldSchema, str]]]],
):
    is_field_schema_as_dict_supported = await _is_field_schema_supported(http_client=http_client)
    for category_name, category_schema in model_schema.items():
        if category_schema is None:
            continue
        for field_name, field_schema in category_schema.items():
            if not is_field_schema_as_dict_supported and not isinstance(field_schema, str):
                raise AporiaError(
                    f"You backend doesn't support dicts in field schemas "
                    f"problematic field is '{field_name}' in '{category_name}'"
                )


async def _is_field_schema_supported(
    http_client: HttpClient,
) -> bool:
    try:
        result = await http_client.get("capabilities/", retry_on_failure=False)
        if isinstance(result, dict):
            return result["is_field_schema_supported"]
        else:
            raise AporiaError("unprocessable result")
    except Exception as e:  # noqa: F841
        logger.debug(
            "/capabilities call failed,returning false for _is_field_schema_supported",
            exc_info=True,
        )
        return False


def generate_feature_positions(features: Mapping[str, Any]) -> Dict[str, int]:
    """Generate features' position from a features dict.

    Args:
        features: features dict

    Returns:
        Features to positions dictionary.
    """
    return {field_name: index for index, field_name in enumerate(features.keys())}
