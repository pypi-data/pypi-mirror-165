"""Model Manager module for handling model artifacts in CDF.

This module deals with uploading, promoting and downloading of model artifacts
to/from CDF.
"""

from pathlib import Path

import akerbp.mlops.cdf.helpers as cdf
from akerbp.mlops.core import config, logger
from akerbp.mlops.core.helpers import confirm_prompt
from typing import Optional, Dict, Union
from cognite.client.data_classes import FileMetadata
import pandas as pd

env = config.envs.env
project_settings = config.read_project_settings()
logging = logger.get_logger(name="mlops_model_manager")


dataset_id = "mlops"


def setup(
    cdf_api_keys: Optional[Dict] = None, dataset_external_id: str = "mlops"
) -> None:
    """
    Set up the model manager. This involves setting up the CDF client and the
    dataset used to store artifacts.

    Args:
        cdf_api_keys (:obj:`dict`, optional): dictionary with cdf keys
        dataset_external_id (str): external id for the dataset (use None for no dataset)
    """
    if cdf_api_keys:
        cdf.api_keys = cdf_api_keys
    cdf.set_up_cdf_client()
    set_active_dataset(dataset_external_id)


def set_active_dataset(external_id: str) -> None:
    """
    Set current active dataset

    Args:
        external_id (str): external id for the dataset (use None for no dataset)
    """
    global dataset_id
    dataset_id = cdf.get_dataset_id(external_id)
    m = f"Active dataset: {external_id=}, {dataset_id=}"
    logging.debug(m)


def upload_new_model_version(
    model_name: str, env: str, folder: Path, metadata: Dict = {}
) -> FileMetadata:
    """
    Upload a new model version. Files in a folder are archived and stored
    with external id `model_name/env/version`, where version is automatically
    increased.

    Args:
        model_name: name of the model
        env: name of the environment ('dev', 'test', 'prod')
        folder: (Path) path to folder whose content will be uploaded
        metadata: dictionary with metadata (it should not contain a 'version' key)

    Returns:
        (dict): model metadata
    """
    file_list = cdf.query_file_versions(
        external_id_prefix=f"{model_name}/{env}/",
        directory_prefix="/mlops",
        uploaded=None,  # count any file
        dataset_id=dataset_id,
    )
    if not file_list.empty:
        latest_v = file_list.metadata.apply(lambda d: int(d["version"])).max()
    else:
        latest_v = 0

    version = int(latest_v) + 1  # int64 isn't json-serializable
    if "version" in metadata:
        logging.error(
            "Metadata should not contain a 'version' key. " "It will be overwritten"
        )
    metadata["version"] = version
    external_id = f"{model_name}/{env}/{version}"

    if not isinstance(folder, Path):
        folder = Path(folder)

    folder_info = cdf.upload_folder(
        external_id, folder, metadata, target_folder="/mlops", dataset_id=dataset_id
    )
    logging.info(f"Uploaded model with {external_id=} from {folder}")
    return folder_info


def find_model_version(model_name: str, env: str, metadata: Dict) -> str:
    """
    Model external id is specified by the model name and the environment
    (starts with `{model_name}/{env}`), and a query to the metadata. If this is
    not enough, the latest version is chosen.

    Args:
        model_name (str): name of the model
        env (str): name of the environment ('dev', 'test', 'prod')
        metadata (dict): metadata of the model artifacts
    Returns:
        (str): external id of the model
    """
    file_list = cdf.query_file_versions(
        directory_prefix="/mlops",
        external_id_prefix=f"{model_name}/{env}",
        metadata=metadata,
        dataset_id=dataset_id,
    )

    if (n_models := file_list.shape[0]) == 0:
        message = f"No model artifacts found for model with {model_name=}, {env=} and metadata {metadata}. \
            Upload/promote artifacts or specify the correct model name before redeploying"
        raise Exception(message)
    elif n_models > 1:
        logging.debug(
            f"Found {n_models} model artifact folders in {env} environment. Deploy using the latest version, or the version specified in mlops_setting.yaml"
        )

    for c in project_settings:
        if c.model_name == model_name:
            if c.artifact_version is not None:
                artifact_version = c.artifact_version
                if artifact_version > n_models:
                    raise Exception(
                        f"Artifact version {artifact_version} is greater than the number of artifacts {n_models} in {env}. Please specify a valid artifact version"
                    )
                external_id = f"{model_name}/{env}/{artifact_version}"
                logging.info(
                    f"Deploying model with specified artifact version {artifact_version} to {env} environment"
                )
            else:
                external_id = str(
                    file_list.loc[file_list.uploadedTime.argmax(), "externalId"]
                )
                artifact_version = external_id.split("/")[-1]
                logging.info(
                    f"No artifact version specified in the settings. Deploying model with latest artifact version ({artifact_version}) to {env} environment"
                )
        else:
            continue

    return external_id


def download_model_version(
    model_name: str,
    env: str,
    folder: Union[Path, str],
    metadata: Dict = {},
    version: Optional[str] = None,
) -> str:
    """
    Download a model version to a folder. First the model's external id is found
    (unless provided by the user), and then it is downloaded to the chosen
    folder (creating the folder if necessary).

    Args:
        model_name (str): name of the model
        env (str): name of the environment ('dev', 'test', 'prod')
        folder (Union[Path,str]): path to folder where the artifacts are downloaded
        metadata (dict): metadata of the artifacts, doesn't make sense when passing a version (see next parameter)
        version (int, optional): artifact version to download from CDF
    Returns:
        (str): external id of the downloaded model artifacts
    """
    if isinstance(folder, str):
        folder = Path(folder)

    if version:
        external_id = f"{model_name}/{env}/{version}"
    else:
        external_id = find_model_version(model_name, env, metadata)

    if not folder.exists():
        folder.mkdir()
    cdf.download_folder(external_id, folder)
    logging.info(f"Downloaded model with {external_id=} to {folder}")

    return external_id


def set_up_model_artifact(artifact_folder: Path, model_name: str) -> str:
    """
    Set up model artifacts.
    When the prediction service is deployed, we need the model artifacts. These
    are downloaded, unless there's already a folder (local development
    environment only)

    Args:
        artifact_folder (Path):
        model_name: str

    Returns:
        (str): model id provided by the model manager or an existing folder in dev
    """
    if artifact_folder.exists():
        if env == "dev":
            logging.info(f"Use model artifacts in {artifact_folder=}")
            model_id = f"{model_name}/dev/1"
            return model_id
        else:
            message = f"Existing artifacts won't be used ({env=})"
            logging.warning(message)

    logging.info("Download serialized model")
    model_id = download_model_version(model_name, env, artifact_folder)
    return model_id


def get_model_version_overview(
    model_name: Optional[str] = None, env: Optional[str] = None, metadata: Dict = {}
) -> pd.DataFrame:
    """
    Get overview of model artifact versions.

    Args:
        model_name (:obj:`str`, optional): name of the model or None for any
        env (:obj:`str`, optional): name of the environment ('dev', 'test', 'prod')
        metadata (dict): artifact metadata. Defaults to an empty dictionary.

    Returns:
        (pd.DataFrame): model artifact data (external id, id, etc.)
    """
    # All mlops files with right metadata
    file_list = cdf.query_file_versions(
        directory_prefix="/mlops",
        external_id_prefix=None,
        uploaded=None,
        metadata=metadata,
        dataset_id=dataset_id,
    )

    # query the external id
    if model_name:
        index = file_list.externalId.str.contains(model_name + "/")
        file_list = file_list.loc[index]
    if env:
        index = file_list.externalId.str.contains("/" + env + "/")
        file_list = file_list.loc[index]
    if not dataset_id:
        index = file_list.dataSetId.isnull()
        file_list = file_list.loc[index]
    return file_list


def validate_model_id(external_id: str, verbose: bool = True) -> bool:
    """
    Validate that model id follows MLOps standard: model/env/id

    Args:
        external_id (str): model id
        verbose (bool): Whether to print a warning if model id is invalid. Defaults to True.
    Returns:
        (bool): True if name is valid, False otherwise
    """
    supported_environments = ["dev", "test", "prod"]
    try:
        _, environment, version = external_id.split("/")
    except ValueError:
        if verbose:
            m = "Expected model id format: 'model/env/id'"
            logging.error(m)
        return False
    if environment not in supported_environments:
        if verbose:
            m = f"Supported environments: {supported_environments}"
            logging.error(m)
        return False
    try:
        int(version)
    except ValueError:
        if verbose:
            m = f"Version should be integer, got '{version}' instead"
            logging.error(m)
        return False
    return True


def delete_model_version(external_id: str, confirm: bool = True) -> None:
    """
    Delete a model artifact version

    Args:
        external_id (str): artifact's external id in CDF Files.
        confirm (bool): whether the user will be asked to confirm deletion. Defaults to True.
    """
    if not validate_model_id(external_id):
        raise ValueError()
    model, environment, version = external_id.split("/")
    if not cdf.file_exists(external_id, "/mlops"):
        return

    confirmed = False
    if confirm:
        question = f"Delete {model=}, {environment=}, {version=}?"
        confirmed = confirm_prompt(question)

    if not confirm or confirmed:
        cdf.delete_file(dict(external_id=external_id))


def promote_model(
    model_name: str, version: Union[int, str], confirm: bool = True
) -> None:
    """
    Promote a model version from test to prod

    Args:
        model_name (str): name of model
        version (Union[int, str]): version number in test
        confirm: (bool) whether the user will be asked to confirm promotion. Defaults to True.
    """
    external_id = f"{model_name}/test/{version}"
    if not cdf.file_exists(external_id, "/mlops", dataset_id):
        logging.warn(
            f"Model version {external_id} doesn't exist in test, nothing to promote."
        )
        return

    confirmed = False
    if confirm:
        question = f"Promote {model_name=}, environment=test, {version=} to production?"
        confirmed = confirm_prompt(question)

    target_ext_id = f"{model_name}/prod/{version}"
    if cdf.file_exists(
        external_id=target_ext_id, directory="/mlops", dataset_id=dataset_id
    ):
        logging.info(
            f"Model version {target_ext_id} already exists in production, nothing new to promote."
        )
        return

    if not confirm or confirmed:
        cdf.copy_file(external_id, target_ext_id, dataset_id=dataset_id)
