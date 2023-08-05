# handler.py
import traceback
import warnings
import time
from importlib import import_module
import akerbp.mlops.cdf.helpers as cdf
from akerbp.mlops.core import config, logger
from typing import Dict, Union, Any

warnings.simplefilter("ignore")


service_name = config.envs.service_name
logging = logger.get_logger("mlops_cdf")

service = import_module(f"akerbp.mlops.services.{service_name}").service


def handle(
    data: Dict, secrets: Dict, function_call_info: Dict
) -> Union[Any, Dict[Any, Any]]:
    """Handler function for deploying models to CDF

    Args:
        data (Dict): model payload
        secrets (Dict): API keys to be used by the service
        function_call_info (Dict): dictionary containing function id and whether the function call is scheduled

    Returns:
        Union[Any, Dict[Any, Any]]: Function call response
    """
    try:
        cdf.api_keys = secrets
        logging.info("Setting up CDF Client with access to Data, Files and Functions")
        cdf.set_up_cdf_client(context="deploy")
        logging.info("Set up complete")
        if data:
            logging.info("Calling model using provided payload")
            start = time.time()
            output = service(data, secrets)
            elapsed = time.time() - start
            logging.info(f"Model call complete. Duration: {elapsed:.2f} s")
        else:
            logging.info("Calling model with empty payload")
            output = dict(status="ok")
            logging.info("Model call complete")
        logging.info("Querying metadata from the function call")
        function_call_metadata = cdf.get_function_call_response_metadata(
            function_call_info["function_id"]
        )
        logging.info("Function call metadata obtained")
        logging.info("Writing function call metadata to response")
        output.update(dict(metadata=function_call_metadata))
        logging.info("Function call metadata successfully written to response")
        return output
    except Exception:
        trace = traceback.format_exc()
        error_message = f"{service_name} service failed.\n{trace}"
        logging.critical(error_message)
        return dict(status="error", error_message=error_message)
