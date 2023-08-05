"""
service.py

Prediction service.
"""
import ast
import json
import uuid
import traceback
from importlib import import_module

from cognite.client.exceptions import CogniteNotFoundError

import akerbp.mlops.cdf.helpers as mlops_helpers
from akerbp.mlops.core import config, logger
from akerbp.mlops.core.helpers import input_data_validation
from typing import Dict

c = config.read_service_settings()
model_module = import_module(c.model_import_path)
predict = model_module.predict
_initialization = model_module.initialization
ModelException = model_module.ModelException

logging = logger.get_logger("mlops_services")


def initialization(secrets: Dict) -> None:
    """
    Read initialization object required by `predict`
    """
    # This check adds a little overhead to each prediction
    if "init_object" not in globals():
        global init_object
        artifact_folder = c.artifact_folder
        init_object = _initialization(artifact_folder, secrets)  # type: ignore


def service(data: Dict, secrets: Dict) -> Dict:
    """
    Generate prediction for an input
    If the input dictionary (data) contains a key-value pair "return_file" = True,
    the resulting predictions are uploaded to Files in CDF.
    The response will now contain a field 'prediction_file' with a reference to a binary file
    containing the predictions. Otherwise, i.e. if "return_file" = False or the input dictionary does
    not contain a "return_file" key, the predictions are passed to the 'prediction' field of the response,
    and the field 'prediction_file' is set to False.

    Inputs:
        data: input to the model (sent by a user through the API)
        secrets: api keys that the model may need during initialization
    Output:
        Dictionary containing the function call response with a status field ('ok' or 'error').
        If status is 'ok' the response will have fields for 'prediction' and 'prediction_file'
        Otherwise, the response contains a field 'message' with the corresponding error message
    """
    try:
        logging.info("Initializing model")
        initialization(secrets)
        logging.info("Model initialized")
        logging.info("Performing input data validation")
        required_input = ast.literal_eval(
            c.info["prediction"]["metadata"]["required_input"]
        )
        is_input_data_valid = input_data_validation(
            required_input=required_input, input=data
        )
        if is_input_data_valid:
            logging.info("Input data successfully validated")
        else:
            raise KeyError(
                f"Payload is missing at least one of the required curves: {required_input}"
            )
        logging.info("Call predict on the initialized model using the provided payload")
        y = predict(data, init_object, secrets)  # type: ignore
        logging.info("Predictions obtained")
        write_predictions_to_file = data.get("return_file", False)
        if write_predictions_to_file:
            logging.info("Writing predictions to file")
            mlops_helpers.api_keys = secrets
            mlops_helpers.set_up_cdf_client()
            cdf_client = mlops_helpers.global_client
            external_file_id = f"{c.model_name}_predictions_{uuid.uuid4().hex}.binary"
            try:
                cdf_client["files"].files.delete(external_id=external_file_id)
            except CogniteNotFoundError:
                pass
            cdf_client["files"].files.upload_bytes(
                content=str(json.dumps(y)),
                name=f"{c.model_name}_predictions",
                external_id=external_file_id,
            )
            logging.info(f"Prediction file uploaded to {external_file_id}")
            return dict(
                status="ok",
                prediction={},
                prediction_file=external_file_id,
                model_id=c.model_id,
            )
        else:
            logging.info("Writing predictions to the response")
            return dict(
                status="ok", prediction=y, prediction_file="", model_id=c.model_id
            )
    except KeyError:
        error_message = f"Unable to obtain a prediction with the provided payload. See the traceback for more details: {traceback.format_exc()}"
        logging.error(error_message)
        return dict(status="error", message=error_message, model_id=c.model_id)
    except ModelException as error:
        error_message = f"Could not get a prediction. Message: {error}"
        logging.error(error_message)
        return dict(status="error", message=error_message, model_id=c.model_id)
