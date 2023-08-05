"""
service.py

Training service
"""
from importlib import import_module
from tempfile import TemporaryDirectory
from pathlib import Path
from typing import Dict, Callable

import akerbp.mlops.model_manager as mm
from akerbp.mlops.core import config, logger
from cognite.client.data_classes import FileMetadata

logging = logger.get_logger("mlops_services")
c = config.read_service_settings()
env = config.envs.env

model_module = import_module(c.model_import_path)
train = model_module.train
ModelException = model_module.ModelException


def _saver(path: Path, metadata: Dict, cdf_api_keys: Dict) -> FileMetadata:
    """
    Upload model folder to CDF Files
    """
    mm.setup(cdf_api_keys, c.dataset)
    model_info = mm.upload_new_model_version(c.model_name, env, path, metadata)
    return model_info


def service(data: Dict, secrets: Dict, saver: Callable = _saver) -> Dict:
    """
    Training service
    Inputs:
        - data: dictionary, data passed by the user through the API
        - secrets: dictionary with api keys
        - saver: an object that saves the model folder

    Output:
        - Dictionary with status 'ok' or 'error' as keys.
            status == 'ok'    -> there is a 'training' key as well
                                (data on the model file)
            status == 'error' -> there is a 'message' key as well
    """
    try:
        with TemporaryDirectory() as temp_dir:
            metadata = train(data=data, folder_path=temp_dir, secrets=secrets)
            logging.debug(f"{metadata=}")
            model_info = saver(temp_dir, metadata, secrets)
        return dict(status="ok", training=model_info)
    except ModelException as e:
        error_message = f"Training failed. Message: {e}"
        logging.error(error_message)
        return dict(status="error", message=error_message)
