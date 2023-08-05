#  Copyright (c) ZenML GmbH 2022. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at:
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
#  or implied. See the License for the specific language governing
#  permissions and limitations under the License.
"""Implementation of the Seldon Deployer step."""

import os
from typing import Optional, cast

from pydantic import BaseModel, validator

from zenml.artifacts.model_artifact import ModelArtifact
from zenml.constants import MODEL_METADATA_YAML_FILE_NAME
from zenml.environment import Environment
from zenml.exceptions import DoesNotExistException
from zenml.integrations.seldon.model_deployers.seldon_model_deployer import (
    DEFAULT_SELDON_DEPLOYMENT_START_STOP_TIMEOUT,
    SeldonModelDeployer,
)
from zenml.integrations.seldon.seldon_client import (
    create_seldon_core_custom_spec,
)
from zenml.integrations.seldon.services.seldon_deployment import (
    SeldonDeploymentConfig,
    SeldonDeploymentService,
)
from zenml.io import fileio
from zenml.logger import get_logger
from zenml.steps import (
    STEP_ENVIRONMENT_NAME,
    BaseStepConfig,
    StepEnvironment,
    step,
)
from zenml.steps.step_context import StepContext
from zenml.utils import io_utils
from zenml.utils.materializer_utils import save_model_metadata
from zenml.utils.source_utils import import_class_by_path

logger = get_logger(__name__)


class CustomDeployParameters(BaseModel):
    """Custom model deployer step extra parameters.

    Attributes:
        predict_function: Path to Python file containing predict function.

    Raises:
        ValueError: If predict_function is not specified.
        TypeError: If predict_function is not a callable function.

    Returns:
        predict_function: Path to Python file containing predict function.
    """

    predict_function: str

    @validator("predict_function")
    def predict_function_validate(cls, predict_func_path: str) -> str:
        """Validate predict function.

        Args:
            predict_func_path: predict function path

        Returns:
            predict function path

        Raises:
            ValueError: if predict function path is not valid
            TypeError: if predict function path is not a callable function
        """
        try:
            predict_function = import_class_by_path(predict_func_path)
        except AttributeError:
            raise ValueError("Predict function can't be found.")
        if not callable(predict_function):
            raise TypeError("Predict function must be callable.")
        return predict_func_path


class SeldonDeployerStepConfig(BaseStepConfig):
    """Seldon model deployer step configuration.

    Attributes:
        service_config: Seldon Core deployment service configuration.
        secrets: a list of ZenML secrets containing additional configuration
            parameters for the Seldon Core deployment (e.g. credentials to
            access the Artifact Store where the models are stored). If supplied,
            the information fetched from these secrets is passed to the Seldon
            Core deployment server as a list of environment variables.
    """

    service_config: SeldonDeploymentConfig
    custom_deploy_parameters: Optional[CustomDeployParameters] = None
    timeout: int = DEFAULT_SELDON_DEPLOYMENT_START_STOP_TIMEOUT


@step(enable_cache=False)
def seldon_model_deployer_step(
    deploy_decision: bool,
    config: SeldonDeployerStepConfig,
    context: StepContext,
    model: ModelArtifact,
) -> SeldonDeploymentService:
    """Seldon Core model deployer pipeline step.

    This step can be used in a pipeline to implement continuous
    deployment for a ML model with Seldon Core.

    Args:
        deploy_decision: whether to deploy the model or not
        config: configuration for the deployer step
        model: the model artifact to deploy
        context: the step context

    Returns:
        Seldon Core deployment service
    """
    model_deployer = SeldonModelDeployer.get_active_model_deployer()

    # get pipeline name, step name and run id
    step_env = cast(StepEnvironment, Environment()[STEP_ENVIRONMENT_NAME])
    pipeline_name = step_env.pipeline_name
    pipeline_run_id = step_env.pipeline_run_id
    step_name = step_env.step_name

    # update the step configuration with the real pipeline runtime information
    config.service_config.pipeline_name = pipeline_name
    config.service_config.pipeline_run_id = pipeline_run_id
    config.service_config.pipeline_step_name = step_name

    def prepare_service_config(model_uri: str) -> SeldonDeploymentConfig:
        """Prepare the model files for model serving.

        This creates and returns a Seldon service configuration for the model.

        This function ensures that the model files are in the correct format
        and file structure required by the Seldon Core server implementation
        used for model serving.

        Args:
            model_uri: the URI of the model artifact being served

        Returns:
            The URL to the model ready for serving.

        Raises:
            RuntimeError: if the model files were not found
        """
        served_model_uri = os.path.join(
            context.get_output_artifact_uri(), "seldon"
        )
        fileio.makedirs(served_model_uri)

        # TODO [ENG-773]: determine how to formalize how models are organized into
        #   folders and sub-folders depending on the model type/format and the
        #   Seldon Core protocol used to serve the model.

        # TODO [ENG-791]: auto-detect built-in Seldon server implementation
        #   from the model artifact type

        # TODO [ENG-792]: validate the model artifact type against the
        #   supported built-in Seldon server implementations
        if config.service_config.implementation == "TENSORFLOW_SERVER":
            # the TensorFlow server expects model artifacts to be
            # stored in numbered subdirectories, each representing a model
            # version
            io_utils.copy_dir(model_uri, os.path.join(served_model_uri, "1"))
        elif config.service_config.implementation == "SKLEARN_SERVER":
            # the sklearn server expects model artifacts to be
            # stored in a file called model.joblib
            model_uri = os.path.join(model.uri, "model")
            if not fileio.exists(model.uri):
                raise RuntimeError(
                    f"Expected sklearn model artifact was not found at "
                    f"{model_uri}"
                )
            fileio.copy(
                model_uri, os.path.join(served_model_uri, "model.joblib")
            )
        else:
            # default treatment for all other server implementations is to
            # simply reuse the model from the artifact store path where it
            # is originally stored
            served_model_uri = model_uri

        service_config = config.service_config.copy()
        service_config.model_uri = served_model_uri
        return service_config

    # fetch existing services with same pipeline name, step name and
    # model name
    existing_services = model_deployer.find_model_server(
        pipeline_name=pipeline_name,
        pipeline_step_name=step_name,
        model_name=config.service_config.model_name,
    )

    # even when the deploy decision is negative, if an existing model server
    # is not running for this pipeline/step, we still have to serve the
    # current model, to ensure that a model server is available at all times
    if not deploy_decision and existing_services:
        logger.info(
            f"Skipping model deployment because the model quality does not "
            f"meet the criteria. Reusing last model server deployed by step "
            f"'{step_name}' and pipeline '{pipeline_name}' for model "
            f"'{config.service_config.model_name}'..."
        )
        service = cast(SeldonDeploymentService, existing_services[0])
        # even when the deploy decision is negative, we still need to start
        # the previous model server if it is no longer running, to ensure that
        # a model server is available at all times
        if not service.is_running:
            service.start(timeout=config.timeout)
        return service

    # invoke the Seldon Core model deployer to create a new service
    # or update an existing one that was previously deployed for the same
    # model
    service_config = prepare_service_config(model.uri)
    service = cast(
        SeldonDeploymentService,
        model_deployer.deploy_model(
            service_config, replace=True, timeout=config.timeout
        ),
    )

    logger.info(
        f"Seldon deployment service started and reachable at:\n"
        f"    {service.prediction_url}\n"
    )

    return service


@step(enable_cache=False)
def seldon_custom_model_deployer_step(
    deploy_decision: bool,
    config: SeldonDeployerStepConfig,
    context: StepContext,
    model: ModelArtifact,
) -> SeldonDeploymentService:
    """Seldon Core custom model deployer pipeline step.

    This step can be used in a pipeline to implement the
    the process required to deploy a custom model with Seldon Core.

    Args:
        deploy_decision: whether to deploy the model or not
        config: configuration for the deployer step
        model: the model artifact to deploy
        context: the step context

    Raises:
        ValueError: if the custom deployer is not defined
        DoesNotExistException: if an entity does not exist raise an exception

    Returns:
        Seldon Core deployment service
    """
    # verify that a custom deployer is defined
    if not config.custom_deploy_parameters:
        raise ValueError(
            "Custom deploy parameter is required as part of the step configuration this parameter is",
            "the path of the custom predict function",
        )
    # get the active model deployer
    model_deployer = SeldonModelDeployer.get_active_model_deployer()

    # get pipeline name, step name, run id, docker config and the runtime config
    step_env = cast(StepEnvironment, Environment()[STEP_ENVIRONMENT_NAME])
    pipeline_name = step_env.pipeline_name
    pipeline_run_id = step_env.pipeline_run_id
    step_name = step_env.step_name
    docker_configuration = step_env.docker_configuration
    runtime_configuration = step_env.runtime_configuration

    # update the step configuration with the real pipeline runtime information
    config.service_config.pipeline_name = pipeline_name
    config.service_config.pipeline_run_id = pipeline_run_id
    config.service_config.pipeline_step_name = step_name
    config.service_config.is_custom_deployment = True

    # fetch existing services with the same pipeline name, step name and
    # model name
    existing_services = model_deployer.find_model_server(
        pipeline_name=pipeline_name,
        pipeline_step_name=step_name,
        model_name=config.service_config.model_name,
    )
    # even when the deploy decision is negative if an existing model server
    # is not running for this pipeline/step, we still have to serve the
    # current model, to ensure that a model server is available at all times
    if not deploy_decision and existing_services:
        logger.info(
            f"Skipping model deployment because the model quality does not"
            f" meet the criteria. Reusing the last model server deployed by step "
            f"'{step_name}' and pipeline '{pipeline_name}' for model "
            f"'{config.service_config.model_name}'..."
        )
        service = cast(SeldonDeploymentService, existing_services[0])
        # even when the deployment decision is negative, we still need to start
        # the previous model server if it is no longer running, to ensure that
        # a model server is available at all times
        if not service.is_running:
            service.start(timeout=config.timeout)
        return service

    # entrypoint for starting Seldon microservice deployment for custom model
    entrypoint_command = [
        "python",
        "-m",
        "zenml.integrations.seldon.custom_deployer.zenml_custom_model",
        "--model_name",
        config.service_config.model_name,
        "--predict_func",
        config.custom_deploy_parameters.predict_function,
    ]

    # verify if there is an active stack before starting the service
    if not context.stack:
        raise DoesNotExistException(
            "No active stack is available. "
            "Please make sure that you have registered and set a stack."
        )
    stack = context.stack

    # prepare the custom deployment docker image
    custom_docker_image_name = model_deployer.prepare_custom_deployment_image(
        pipeline_name=pipeline_name,
        stack=stack,
        docker_configuration=docker_configuration,
        runtime_configuration=runtime_configuration,
        entrypoint=entrypoint_command,
    )

    # copy the model files to new specific directory for the deployment
    served_model_uri = os.path.join(context.get_output_artifact_uri(), "seldon")
    fileio.makedirs(served_model_uri)
    io_utils.copy_dir(model.uri, served_model_uri)

    # Get the model artifact to extract information about the model
    # and how it can be loaded again later in the deployment environment.
    artifact = stack.metadata_store.store.get_artifacts_by_uri(model.uri)
    if not artifact:
        raise DoesNotExistException("No artifact found at {}".format(model.uri))

    # save the model artifact metadata to the YAML file and copy it to the
    # deployment directory
    model_metadata_file = save_model_metadata(artifact[0])
    fileio.copy(
        model_metadata_file,
        os.path.join(served_model_uri, MODEL_METADATA_YAML_FILE_NAME),
    )

    # prepare the service configuration for the deployment
    service_config = config.service_config.copy()
    service_config.model_uri = served_model_uri

    # create the specification for the custom deployment
    service_config.spec = create_seldon_core_custom_spec(
        model_uri=service_config.model_uri,
        custom_docker_image=custom_docker_image_name,
        secret_name=model_deployer.kubernetes_secret_name,
        command=entrypoint_command,
    )

    # deploy the service
    service = cast(
        SeldonDeploymentService,
        model_deployer.deploy_model(
            service_config, replace=True, timeout=config.timeout
        ),
    )

    logger.info(
        f"Seldon Core deployment service started and reachable at:\n"
        f"    {service.prediction_url}\n"
    )

    return service
