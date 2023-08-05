#  Copyright (c) ZenML GmbH 2022. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at:
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
#  or implied. See the License for the specific language governing
#  permissions and limitations under the License.
"""Implementation of the Evidently Profile Step."""

from typing import Any, Dict, List, Optional, Sequence, Tuple, Union, cast

import pandas as pd
from evidently.model_profile import Profile  # type: ignore[import]
from evidently.pipeline.column_mapping import (  # type: ignore[import]
    ColumnMapping,
)
from pydantic import BaseModel, Field
from typing_extensions import Literal

from zenml.integrations.evidently.data_validators import EvidentlyDataValidator
from zenml.steps import Output
from zenml.steps.base_step import BaseStep
from zenml.steps.step_interfaces.base_drift_detection_step import (
    BaseDriftDetectionConfig,
    BaseDriftDetectionStep,
)
from zenml.steps.utils import clone_step


class EvidentlyColumnMapping(BaseModel):
    """Column mapping configuration for Evidently.

    This class is a 1-to-1 serializable analogue of Evidently's
    ColumnMapping data type that can be used as a step configuration field
    (see https://docs.evidentlyai.com/features/dashboards/column_mapping).

    Attributes:
        target: target column
        prediction: target column
        datetime: datetime column
        id: id column
        numerical_features: numerical features
        categorical_features: categorical features
        datetime_features: datetime features
        target_names: target column names
        task: model task (regression or classification)
    """

    target: Optional[str] = None
    prediction: Optional[Union[str, Sequence[str]]] = None
    datetime: Optional[str] = None
    id: Optional[str] = None
    numerical_features: Optional[List[str]] = None
    categorical_features: Optional[List[str]] = None
    datetime_features: Optional[List[str]] = None
    target_names: Optional[List[str]] = None
    task: Optional[Literal["classification", "regression"]] = None

    def to_evidently_column_mapping(self) -> ColumnMapping:
        """Convert this Pydantic object to an Evidently ColumnMapping object.

        Returns:
            An Evidently column mapping converted from this Pydantic object.
        """
        column_mapping = ColumnMapping()

        # preserve the Evidently defaults where possible
        column_mapping.target = self.target or column_mapping.target
        column_mapping.prediction = self.prediction or column_mapping.prediction
        column_mapping.datetime = self.datetime or column_mapping.datetime
        column_mapping.id = self.id or column_mapping.id
        column_mapping.numerical_features = (
            self.numerical_features or column_mapping.numerical_features
        )
        column_mapping.datetime_features = (
            self.datetime_features or column_mapping.datetime_features
        )
        column_mapping.target_names = (
            self.target_names or column_mapping.target_names
        )
        column_mapping.task = self.task or column_mapping.task

        return column_mapping


class EvidentlyProfileConfig(BaseDriftDetectionConfig):
    """Config class for Evidently profile steps.

    Attributes:
        column_mapping: properties of the DataFrame columns used
        ignored_cols: columns to ignore during the Evidently profile step
        profile_sections: a list identifying the Evidently profile sections to be
            used. The following are valid options supported by Evidently:
            - "datadrift"
            - "categoricaltargetdrift"
            - "numericaltargetdrift"
            - "classificationmodelperformance"
            - "regressionmodelperformance"
            - "probabilisticmodelperformance"
        verbose_level: Verbosity level for the Evidently dashboards. Use
            0 for a brief dashboard, 1 for a detailed dashboard.
        profile_options: Optional list of options to pass to the
            profile constructor. See `EvidentlyDataValidator._unpack_options`.
        dashboard_options: Optional list of options to pass to the
            dashboard constructor. See `EvidentlyDataValidator._unpack_options`.
    """

    column_mapping: Optional[EvidentlyColumnMapping] = None
    ignored_cols: Optional[List[str]] = None
    profile_sections: Optional[Sequence[str]] = None
    verbose_level: int = 1
    profile_options: Sequence[Tuple[str, Dict[str, Any]]] = Field(
        default_factory=list
    )
    dashboard_options: Sequence[Tuple[str, Dict[str, Any]]] = Field(
        default_factory=list
    )


class EvidentlyProfileStep(BaseDriftDetectionStep):
    """Step implementation implementing an Evidently Profile Step."""

    def entrypoint(  # type: ignore[override]
        self,
        reference_dataset: pd.DataFrame,
        comparison_dataset: pd.DataFrame,
        config: EvidentlyProfileConfig,
    ) -> Output(  # type:ignore[valid-type]
        profile=Profile, dashboard=str
    ):
        """Main entrypoint for the Evidently categorical target drift detection step.

        Args:
            reference_dataset: a Pandas DataFrame
            comparison_dataset: a Pandas DataFrame of new data you wish to
                compare against the reference data
            config: the configuration for the step

        Raises:
            ValueError: If ignored_cols is an empty list
            ValueError: If column is not found in reference or comparison
                dataset

        Returns:
            profile: Evidently Profile generated for the data drift
            dashboard: HTML report extracted from an Evidently Dashboard
              generated for the data drift
        """
        data_validator = cast(
            EvidentlyDataValidator,
            EvidentlyDataValidator.get_active_data_validator(),
        )
        column_mapping = None

        if config.ignored_cols is None:
            pass

        elif not config.ignored_cols:
            raise ValueError(
                f"Expects None or list of columns in strings, but got {config.ignored_cols}"
            )

        elif not (
            set(config.ignored_cols).issubset(set(reference_dataset.columns))
        ) or not (
            set(config.ignored_cols).issubset(set(comparison_dataset.columns))
        ):
            raise ValueError(
                "Column is not found in reference or comparison datasets"
            )

        else:
            reference_dataset = reference_dataset.drop(
                labels=list(config.ignored_cols), axis=1
            )
            comparison_dataset = comparison_dataset.drop(
                labels=list(config.ignored_cols), axis=1
            )

        if config.column_mapping:
            column_mapping = config.column_mapping.to_evidently_column_mapping()
        profile, dashboard = data_validator.data_profiling(
            dataset=reference_dataset,
            comparison_dataset=comparison_dataset,
            profile_list=config.profile_sections,
            column_mapping=column_mapping,
            verbose_level=config.verbose_level,
            profile_options=config.profile_options,
            dashboard_options=config.dashboard_options,
        )
        return [profile, dashboard.html()]


def evidently_profile_step(
    step_name: str,
    config: EvidentlyProfileConfig,
) -> BaseStep:
    """Shortcut function to create a new instance of the EvidentlyProfileConfig step.

    The returned EvidentlyProfileStep can be used in a pipeline to
    run model drift analyses on two input pd.DataFrame datasets and return the
    results as an Evidently profile object and a rendered dashboard object.

    Args:
        step_name: The name of the step
        config: The configuration for the step

    Returns:
        a EvidentlyProfileStep step instance
    """
    return clone_step(EvidentlyProfileStep, step_name)(config=config)
