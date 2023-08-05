"""
deploy.py

Deploy services in either Google Cloud Run or CDF Functions.
Model registry uses CDF Files.
"""
import json
import os
import subprocess
import sys
import traceback
from pathlib import Path
from typing import Dict, List

import akerbp.mlops.model_manager as mm
from akerbp.mlops import __version__ as package_version
from akerbp.mlops.cdf import helpers as cdf
from akerbp.mlops.core import config, logger
from akerbp.mlops.core.config import ServiceSettings
from akerbp.mlops.deployment import helpers, platforms

logging = logger.get_logger(name="mlops_deployment")

api_keys = config.api_keys
cdf_client = cdf.get_client(
    api_key=api_keys["functions"], api_key_label="functions"
)  # for creating the schedule keeping the functions warm
platform_methods = platforms.get_methods()

logging.info(
    f"Deploying prediction service using MLOps framework version {package_version}"
)


def deploy_model(
    model_settings: ServiceSettings,
    platform_methods: Dict = platform_methods,
) -> str:
    """
    Deploy a model.

    This will create a deployment folder and change current working directory
    to it.

    Return "OK" if deployment was successful, otherwise return a string with the traceback for the failed deployment

    Args:
        model_settings (ServiceSettings): settings for the model service
        platform_methods (dict): where key is the platform and value is a tuple with deploy and test functions.
            Defaults to the globally set platform_methods variable.

    Returns:
        (str): status of the deployment
    """
    try:
        c = model_settings
        env = config.envs.env
        testing_only = config.envs.testing_only
        local_deployment = config.envs.local_deployment
        service_name = config.envs.service_name
        deployment_folder = helpers.deployment_folder_path(c.model_name)
        function_name = f"{c.model_name}-{service_name}-{env}"
        human_readable_function_name = c.human_friendly_model_name

        logging.info(
            f"Starting deployment and/or testing of model {c.human_friendly_model_name} with external id {function_name}"
        )

        if (service_name == "prediction") and c.artifact_folder:
            mm.set_active_dataset(c.dataset)
            c.model_id = mm.set_up_model_artifact(c.artifact_folder, c.model_name)

        logging.info("Create deployment folder and move required files/folders")
        deployment_folder.mkdir()
        helpers.copy_to_deployment_folder(c.files, deployment_folder)

        logging.debug(f"cd {deployment_folder}")
        os.chdir(deployment_folder)
        helpers.set_up_requirements(c)
        config.store_service_settings(c)

        # Local testing
        if c.platform == "local" and c.test_file:
            logging.info("Performing local testing")
            logging.warn(
                "Be aware that your local packages will overwrite the model dependencies. Consequenctly, tests might fail due to conflicting dependencies"
            )
            command = [sys.executable, "-m", "akerbp.mlops.services.test_service"]
            output = subprocess.check_output(command, encoding="UTF-8")
        else:
            logging.info(
                "Skipping local tests. Either test file not found, or deploying locally or remote in pipeline"
            )

        if c.platform == "cdf":
            if (env == "test" or env == "prod") and testing_only == "True":
                logging.info("Running tests only, will not deploy model(s)")
                command = [sys.executable, "-m", "akerbp.mlops.services.test_service"]
                subprocess.check_output(command, encoding="UTF-8")
            elif (
                (env == "test" or env == "prod") and testing_only == "False"
            ) or local_deployment == "True":
                logging.info(f"Deploying model(s) to {c.platform}")
                # Extract latest artifact version if not specified, and set model version
                if c.artifact_version is None:
                    latest_artifact_version = cdf.get_latest_artifact_version(
                        external_id=function_name
                    )
                    logging.info(
                        f"Latest artifact version in {env} environment is {latest_artifact_version}"
                    )
                    artifact_version = latest_artifact_version
                else:
                    artifact_version = c.artifact_version

                external_id = function_name + "-" + str(artifact_version)
                predictable_external_id = function_name

                # Extract the deployment and test functions
                deploy_function, redeploy_function, test_function = platform_methods[
                    c.platform
                ]

                # Deploy function with version number included in the external id (model-service-env-version)
                logging.info(
                    f"Deploying function {human_readable_function_name} with external id {external_id} to {c.platform}"
                )
                deploy_function(
                    human_readable_function_name, external_id, info=c.info[service_name]
                )
                if c.test_file:
                    logging.info(
                        f"Make a test call to function with external id {external_id}"
                    )
                    command = [
                        sys.executable,
                        "-m",
                        "akerbp.mlops.services.test_service",
                    ]
                    output = subprocess.check_output(command, encoding="UTF-8")
                    model_input = json.loads(output.splitlines()[-1])
                    test_function(external_id, model_input)
                else:
                    logging.warning(
                        f"No test file was set up. End-to-end test skipped for function {external_id}!"
                    )
                if artifact_version == latest_artifact_version:
                    # Redeploy latest function with a predictable external id (model-service-env)
                    logging.info(
                        f"Redeploying latest model {human_readable_function_name} with predictable external id {predictable_external_id} to {c.platform}"
                    )
                    (
                        name,
                        file_id,
                        description,
                        metadata,
                        owner,
                    ) = cdf.get_arguments_for_redeploying_latest_model_version(
                        external_id=external_id
                    )
                    redeploy_function(
                        name,
                        predictable_external_id,
                        file_id,
                        description,
                        metadata,
                        owner,
                    )
                    if (
                        c.test_file
                    ):  # model input already initialized in the above if-block
                        logging.info(
                            f"Make a test call to the latest model with predictable external id {predictable_external_id}"
                        )
                        test_function(predictable_external_id, model_input)
                    else:
                        logging.warning(
                            f"No test file was set up. End-to-end test skipped for function {predictable_external_id}!"
                        )
                else:
                    logging.info(
                        f"Deployment is based on an old artifact version ({artifact_version}/{latest_artifact_version}). Skipping redeployment with a predictable external id."
                    )
            else:
                logging.warning(
                    f"Will not run tests nor deploy model(s), check your environment variables: {config.envs}"
                )

        else:  # GCP deployment, not used by our team
            external_id = function_name
            deploy_function, test_function = platform_methods[c.platform]
            logging.info(
                f"Deploying model {human_readable_function_name} with external id {external_id} to {c.platform}"
            )
            deploy_function(
                human_readable_function_name, external_id, info=c.info[service_name]
            )

        # Create a schedule for keeping the latest function warm in prod
        if env == "prod" and c.platform == "cdf":
            logging.info(
                f"Creating a schedule for keeping the function {predictable_external_id} warm on weekdays during extended working hours"
            )
            # With the API-key SDK, schedules are persistent, so they are not deleted when functions are deleted
            schedules = cdf_client.functions.schedules.list(
                function_external_id=predictable_external_id
            )
            if len(schedules) > 0:
                logging.info("A schedule already exist and will be overwritten")
                for schedule in schedules:
                    schedule_id = schedule.id
                    cdf_client.functions.schedules.delete(id=schedule_id)

            _ = cdf_client.functions.schedules.create(
                name="Keep warm schedule",
                description="Keep the function warm by calling it with an empty payload every 30 minutes during extended working hours on weekdays",
                cron_expression="*/30 7-19 * * 1-5",
                function_external_id=predictable_external_id,
                data={},
            )
            logging.info("Schedule created")

        return "OK"
    except Exception:
        trace = traceback.format_exc()
        return f"Model failed to deploy!\n{trace}"


def deploy(project_settings: List[ServiceSettings]) -> None:
    """
    Deploy a machine learning project that potentially contains multiple models.
    Deploy each model in the settings and make sure that if one model fails it
    does not affect the rest. At the end, if any model failed, it raises an
    exception with a summary of all models that failed.

    Args:
        Project settings as described by the user in the config file.

    Raises:
        Exception: If any model failed to deploy.
    """
    failed_models = {}
    cwd_path = Path.cwd()

    for c in project_settings:
        status = deploy_model(c)
        if status != "OK":
            logging.error(status)
            failed_models[c.human_friendly_model_name] = status

        logging.debug("cd ..")
        os.chdir(cwd_path)
        helpers.rm_deployment_folder(c.model_name)

    if failed_models:
        for model, message in failed_models.items():
            logging.info(f"Model {model} failed: {message}")
        raise Exception("At least one model failed.")


if __name__ == "__main__":
    mm.setup()
    settings = config.read_project_settings()
    deploy(settings)
