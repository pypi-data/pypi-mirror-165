from __future__ import annotations

from abc import ABC
from abc import abstractmethod
import itertools
import json
import logging
from typing import Any, Mapping, Optional, Sequence, TYPE_CHECKING, Union

import numpy as np
import pandas as pd

import truera.client.cli.verify_nn_ingestion as verify_nn_ingestion
from truera.client.client_environment import LocalContextStorage
from truera.client.client_utils import _STRING_TO_INPUT_DATA_FORMAT
from truera.client.client_utils import _STRING_TO_QOI
from truera.client.ingestion_client import Credential
from truera.client.ingestion_client import IngestionClient
from truera.client.ingestion_client import Table
from truera.client.intelligence.explainer import Explainer
from truera.client.intelligence.segment import SegmentGroup
from truera.client.nn import NNBackend
from truera.client.nn.client_configs import AttributionConfiguration
from truera.client.nn.client_configs import RNNAttributionConfiguration
from truera.client.nn.client_configs import RNNUserInterfaceConfiguration
from truera.client.nn.wrappers.nlp import NLP
from truera.client.public.communicator.http_communicator import \
    AlreadyExistsError
from truera.client.truera_workspace_utils import \
    get_output_type_from_score_type
from truera.protobuf.public.metadata_message_types_pb2 import \
    FEATURE_TRANSFORM_TYPE_MODEL_FUNCTION
from truera.protobuf.public.metadata_message_types_pb2 import \
    FEATURE_TRANSFORM_TYPE_NO_TRANSFORM
from truera.protobuf.public.metadata_message_types_pb2 import \
    FEATURE_TRANSFORM_TYPE_PRE_POST_DATA
from truera.protobuf.public.metadata_message_types_pb2 import \
    FeatureTransformationType
from truera.protobuf.public.util import split_mode_pb2 as sm_pb
from truera.public.artifact_repo_lib import ensure_valid_identifier
import truera.public.feature_influence_constants as fi_constants

if TYPE_CHECKING:
    from truera.client.nn.wrappers import Base
    from truera.client.nn.wrappers import Timeseries


def verify_label_values_for_classification(ys: Union[pd.Series, np.ndarray]):
    if not np.isin(ys, [0, 1]).all():
        raise ValueError(
            "Classification models require label data to be binary!"
        )


def verify_label_values_for_regression(ys: Union[pd.Series, np.ndarray]):
    if not pd.api.types.is_numeric_dtype(ys):
        raise ValueError("Regression models require label data to be numeric!")


class BaseTrueraWorkspace(ABC):

    _DEFAULT_NUM_DEFAULT_INFLUENCES = 1000

    def __init__(self):
        self.logger = logging.Logger(__name__)

    def __str__(self) -> str:
        return json.dumps(self.get_context(), indent=4)

    def __repr__(self) -> str:
        return json.dumps(self.get_context(), indent=4)

    @abstractmethod
    def get_projects(self) -> Sequence[str]:
        """Get all projects accessible by current user for the current workspace environment.
        """
        pass

    @abstractmethod
    def set_project(self, project: str):
        """Set the current project to use for the current workspace environment. This will unset the rest of the context (data collection, data split, model, etc.) if set prior.
        Args:
            project: Name of the project.
        Raises:
            ValueError: Raised if the project does not exist.
        """
        pass

    @abstractmethod
    def add_project(
        self,
        project: str,
        score_type: str,
        input_type: Optional[str] = "tabular",
        num_default_influences: Optional[int] = None
    ):
        """Adds and sets project to use for the current workspace environment. This will unset the rest of the context (data collection, data split, model, etc) if set prior.
        Args:
            project: Name of the project.
            score_type: Scorer type configuration for the project. Options are ["logits", "probits", "classification", "regression"].
            input_type: Input data type for the project. Must be one of ["tabular", "time_series_tabular"]. Defaults to "tabular".
            num_default_influences: Number of influences used by default for most influence-requiring graphs, computations, etc. Note that this will take the first of the provided many from the data split --- therefore, shuffling data splits is generally advised prior to ingestion. If creating a project and left as None, then will be set as 1000.
        """
        pass

    def list_valid_score_types(self) -> Sequence[str]:
        """List the valid score types that can be set for the currently set project.
        Returns:
            Sequence[str]: Valid score types.
        """
        if self._get_output_type() == "regression":
            return fi_constants.VALID_SCORE_TYPES_FOR_REGRESSION
        return fi_constants.VALID_SCORE_TYPES_FOR_CLASSIFICATION

    @abstractmethod
    def set_score_type(self, score_type: str):
        """Set the score type of the currently set project.
        Args:
            score_type: Scorer type configuration.
                Options are ["logits", "probits", "classification", "regression", None]. Defaults to None.
        """
        pass

    @abstractmethod
    def get_num_default_influences(self) -> int:
        """Get the number of influences computed by default of the currently set project.
        Returns:
            int: Number of default influences.
        """
        pass

    @abstractmethod
    def set_num_default_influences(self, num_default_influences: int):
        """Set the number of influences computed by default of the currently set project.
        Args:
            num_default_influences: Number of influences used by default for most influence-requiring graphs, computations, etc. Note that this will take the first of the provided many from the data split --- therefore, shuffling data splits is generally advised prior to ingestion.
        """
        pass

    @abstractmethod
    def get_num_internal_qii_samples(self) -> int:
        """Get the number of samples used internally in influence computations of the currently set project.

        Returns:
            int: Number of samples to be used internally for influence computations.
        """
        pass

    @abstractmethod
    def set_num_internal_qii_samples(self, num_samples: int):
        """Set the number of samples used internally in influence computations of the currently set project.
        Args:
            num_samples: Number of samples to be used internally for influence computations.
        """
        pass

    @abstractmethod
    def set_maximum_model_runner_failure_rate(
        self, maximum_model_runner_failure_rate: float
    ):
        """Sets the maximum model runner failure rate (fraction of points on which the model can fail for a model run to be considered successful) for the current project.
        Args:
            maximum_model_runner_failure_rate (float): Maximum failure rate. Must be in [0, 1). By default, it is set to 0.
        """
        pass

    @abstractmethod
    def get_maximum_model_runner_failure_rate(self) -> float:
        """Get the maximum model runner failure rate (fraction of points on which the model can fail for a model run to be considered successful) for the current project.
        """
        pass

    def _validate_num_default_influences(self, num_default_influences: int):
        self._ensure_project()
        if num_default_influences <= 0:
            raise ValueError("`num_default_influences` must be > 0!")

    def _validate_num_samples_for_influences(self, num_samples: int):
        self._ensure_project()
        if num_samples <= 0:
            raise ValueError("`num_samples` must be > 0!")

    @abstractmethod
    def get_models(self) -> Sequence[str]:
        """Get all models in the connected project.
        Raises:
            ValueError: Raised if the workspace isn't connected to any project.
        Returns:
            Name of models in the project.
        """
        pass

    @abstractmethod
    def set_model(self, model_name: str):
        """Set the current model to use for all operations in the current workspace. This will also change the data collection to the one corresponding to the provided model if different than the priorly set data collection.
        Args:
            model_name: Name of the model. If None, will unset the model.
        Raises:
            ValueError: Raised if no project is associated with the current workspace.
                Use set_project to set the correct project.
            ValueError: Raised if there is no such model in the project.
        """
        pass

    @abstractmethod
    def delete_model(self, model_name: Optional[str] = None):
        """Delete a model from the current TruEra workspace. This will only delete artifacts within the current location context (either local or remote).
        Args:
            model_name: Name of the model to be deleted. By default the currently set model will be deleted.
        Raises:
            ValueError: Raised if no project is associated with the current workspace. Use set_project
                to set the correct project.
        """
        pass

    @abstractmethod
    def get_data_collections(self) -> Sequence[str]:
        """Get all data-collections in the connected project.
        Raises:
            ValueError: Raised if the workspace isn't connected to any project.
        Returns:
            Name of data-collections in the project.
        """
        pass

    @abstractmethod
    def get_data_splits(self) -> Sequence[str]:
        """Get all data-splits in the connected data-collection.
        Raises:
            ValueError: Raised if the workspace isn't connected to any project.
            ValueError: Raised if the workspace isn't connected to any data-collection.
        Returns:
            Name of data-splits in the project.
        """
        pass

    @abstractmethod
    def add_data_collection(
        self,
        data_collection_name: str,
        pre_to_post_feature_map: Optional[Mapping[str, Sequence[str]]] = None,
        provide_transform_with_model: Optional[bool] = None
    ):
        """Creates and sets the current data collection to use for all operations in the workspace. Must specify feature mapping if some data transformation is being done.
        Args:
            data_collection_name: Name of the data_collection.
            pre_to_post_feature_map: One-to-many mapping from a single pre-processed human-readable feature name to post-processed model-readable feature names. Ignored if post-processed data is not provided for the data collection.
            provide_transform_with_model: Specifies if tranform function will be mentioned for each model using this data collection. If `True`, then feature mapping is via a `transform` function and if `False`, then separate pre-/post-transform data is expected in all splits. Defaults to `None`. Must be set, if feature map is provided for the data collection.
        Raises:
            ValueError: Raised if no project is associated with the current workspace.
                Use set_project to set the correct project.
        """
        pass

    @abstractmethod
    def set_data_collection(self, data_collection_name: str):
        """Set the current data collection to use for all operations in the workspace. This will also unset the current model if it is not associated with the provided data collection.
        Args:
            data_collection_name: Name of the data_collection. If None, will unset the data collection.
        Raises:
            ValueError: Raised if no project is associated with the current workspace.
                Use set_project to set the correct project.
            ValueError: Raised if there is no such data_collection in the project.
        """
        pass

    @abstractmethod
    def _get_feature_transform_type_for_data_collection(self):
        pass

    @abstractmethod
    def set_data_split(self, data_split_name: str):
        """Set the current data split to use for all operations in the current workspace.
        Args:
            data_split_name: Name of the data_split. If None, will unset the data split.
        Raises:
            ValueError: Raised if no project is associated with the current workspace.
                Use set_project to set the correct project.
            ValueError: Raised if no data_collection is associated with the current workspace.
                Use set_data_collection to set the correct data_collection.
            ValueError: Raised if there is no such data_split in the data_collection.
        """
        pass

    @abstractmethod
    def add_python_model(
        self,
        model_name: str,
        model: Any,
        *,
        additional_pip_dependencies: Optional[Sequence[str]] = None,
        additional_modules: Optional[Sequence[Any]] = None,
        classification_threshold: Optional[float] = None,
        train_split_name: Optional[str] = None,
        train_parameters: Optional[Mapping[str, Any]] = None,
        verify_model: bool = True,
        compute_predictions: bool = True,
        compute_feature_influences: bool = False,
        compute_for_all_splits: bool = False,
        **kwargs
    ):
        """Registers and adds a new model, including the executable model object provided. This method deduces the model framework to appropriately serialize
            and upload the model object to TruEra server. Models of supported frameworks can be passed directly.
            Supported Model Frameworks: sklearn, xgboost, catboost, lightgbm, pyspark (tree models only).
            If you cannot ingest your model via this function due to custom logic, feature transforms, etc., see `create_packaged_python_model()`.

            [ALPHA] For frameworks that are not yet supported, or for custom model implementations the prediction
            function for the model can be provided as the model.
            For binary classifiers, the prediction function should accept a pandas DataFrame as input and produce
            a pandas DataFrame as output with the class probabilities and [0, 1] as the column header.
            For regression models, the prediction function should accept a pandas DataFrame as input and produce
            the result as a pandas DataFrame with "Result" as the column header.
            All required dependencies to execute the prediction function should be provide as additional_pip_dependencies.
            For example:
            ```python
            def predict(df):
                return pd.DataFrame(my_model.predict_proba(df, validate_features=False), columns=[0, 1])
            tru.add_python_model("my_model", predict, additional_pip_dependencies=["xgboost==1.3.1", "pandas==1.1.1"])
            ```
        Args:
            model_name: Name assigned to the model.
            model: The python model object or the prediction function.
                Supported frameworks are catboost, lightgbm, sklearn and xgboost, and tree-based PySpark models. For prediction function, please see the description above.
            additional_pip_dependencies: List of pip dependencies required to execute the model. When model object
                is from a supported framework, pip dependency for that framework is automatically inferred. If a prediction function is provided as the model,
                additional pip dependencies are not automatically inferred and must be explicitly provided.
                Defaults to None. Example: ["pandas==1.1.1", "numpy==1.20.1"]
            additional_modules: List of modules not available as pip packages required for the model. These must already be imported.  Defaults to None.
            classification_threshold: Threshold that is applied to model predictions to determine classification outcomes. Ignored for regression models.
            train_split_name: The name of the train split of the model
            train_parameters: Train parameters of the model. Ex. {'n_estimators": 10}"}
            verify_model: Locally verify the model is packaged properly and can operate on existing split data. Defaults to True.
            compute_predictions: Trigger computations of model predictions on the base/default split of the model's data collection, if such a split exists. Ignored for local models. 
            compute_feature_influences: Trigger computations of model feature influences on the base/default split of the model's data collection, if such a split exists. Ignored for local models.
            compute_for_all_splits: If `compute_predictions` and/or `compute_feature_influences`, triggers computations for all existing data splits (not solely the base/default split). Ignored for local models.
        Raises:
            NotSupportedError: Raised if the model type is not supported.
                You can still use the [`add_packaged_python_model`][truera.client.truera_workspace.TrueraWorkspace.add_packaged_python_model]
                method to upload a pre-serialized model to TruEra server.
        """
        pass

    @abstractmethod
    def add_packaged_python_model(
        self,
        model_name: str,
        model_dir: str,
        *,
        data_collection_name: Optional[str] = None,
        train_split_name: Optional[str] = None,
        train_parameters: Optional[Mapping[str, Any]] = None,
        verify_model: bool = True,
        compute_predictions: bool = True,
        compute_feature_influences: bool = False,
        compute_for_all_splits: bool = False
    ):
        """Registers and adds a new model, along with a pre-serialized and packaged executable Python model object.
        The model is also attached to the workspace as the current model.
        Args:
            model_name: Name assigned to the model.
            model_dir: Directory where packaged model is located.
            data_collection_name: Data collection to attach to the model,
                by default the data collection attached to the workspace will be used. Defaults to None.
            train_split_name: The name of the train split of the model
            train_parameters: Train parameters of the model. Ex. {'n_estimators": 10}"}
            verify_model: Locally verify the model is packaged properly and can operate on existing split data. Defaults to True.
            compute_predictions: Trigger computations of model predictions on the base/default split of the model's data collection, if such a split exists. Ignored for local models.
            compute_feature_influences: Trigger computations of model feature influences on the base/default split of the model's data collection, if such a split exists. Ignored for local models.
            compute_for_all_splits: If `compute_predictions` and/or `compute_feature_influences`, triggers computations for all existing data splits (not solely the base/default split). Ignored for local models.
        """
        pass

    @abstractmethod
    def create_packaged_python_model(
        self,
        output_dir: str,
        model_obj: Optional[Any] = None,
        additional_pip_dependencies: Optional[Sequence[str]] = None,
        model_path: Optional[str] = None,
        model_code_files: Optional[Sequence[str]] = None
    ):
        """Creates a template of a packaged Python model object to be edited and then uploaded to TruEra server.
        Can be used to package either Python model objects, or serialized model data. This workflow should only be used for custom models or to debug model ingestion.
        To upload a models of a known framework, it is recommended to use the `add_python_model()` function.
        Args:
            output_dir: Path to the directory to create template. Cannot be an existing directory.
            model_obj: The Python model object to package. Supported frameworks are catboost, lightgbm, sklearn, xgboost, and tree-based PySpark models.
            additional_pip_dependencies: List of pip dependencies required to execute the model. When model object
                is from a supported framework, pip dependency for that framework is automatically inferred. If a prediction function is provided as the model,
                additional pip dependencies are not automatically inferred and must be explicitly provided.
                Defaults to None. Example: ["pandas==1.1.1", "numpy==1.20.1"].
            model_path: Path to a model file or directory. Can be a serialized model or a directory containing multiple files of serialized data.
                Ignored if `model_obj` is passed in.
            model_code_files: List of paths to additional files to be packaged with the model. Ignored if `model_obj` is passed in.
        """
        pass

    @abstractmethod
    def verify_packaged_model(self, model_path: str):
        """Locally verifies a packaged Python model by loading the model and, if available, running it on split data ingested into the TruEra system.
        The model must already be packaged, e.g. via `create_packaged_python_model()`. The project and data collection for the model must also be set in the current workspace context.
        This function assumes that it is running an environment with any model dependencies/packages installed.
        Args:
            model_path (str): Path to packaged model directory.
        """
        pass

    @abstractmethod
    def add_rnn_model(
        self,
        model_name: str,
        model_or_load_wrapper: Union[Any, Timeseries.ModelLoadWrapper],
        model_run_wrapper: Timeseries.ModelRunWrapper,
        attribution_config: dict,
        train_split_name: Optional[str] = None,
        train_parameters: Optional[Mapping[str, Any]] = None,
        **kwargs
    ):
        """[Alpha] Upload a RNN model to TruEra server. The model is also attached to the workspace as the current model.
        Args:
            model_name: Name assigned to the model.
            model_or_load_wrapper: Either the model object or a wrapper object to load the model
                (should be an instance of `Timeseries.ModelLoadWrapper` abstract class). If a model object is given (instead of the wrapper),
                the model binary will not be uploaded to the TruEra platform during `upload_project` call.
            model_run_wrapper: A wrapper class to call evaluate and other model run values.
                Should be an instance of `Timeseries.ModelRunWrapper` abstract class.
            attribution_config: An attribution config containing attribution run parameters.
            train_split_name: The name of the train split of the model
            train_parameters: Train parameters of the model. Ex. {'n_estimators": 10}"}

        Raises:
            ValueError: Raised if no project is associated with the current workspace. Use set_project
                to set the correct project.
            ValueError: Raised if workspace is not attached to a data_collection. Either attach workspace
                to a data-collection or provide the data_collection_name.
            ValueError: Raised if the provided data_collection_name does not exist in the current project.
        """
        pass

    @abstractmethod
    def add_model(
        self,
        model_name: str,
        train_split_name: Optional[str] = None,
        train_parameters: Optional[Mapping[str, Any]] = None
    ):
        """Registers and adds a new model in TruEra. By default, the model is "virtual" in that it
        does not have an executable model object attached. To add the model object itself, see `add_python_model()`.
        Args:
            model_name: Name of model to create
            train_split_name: The name of the train split of the model
            train_parameters: Train parameters of the model. Ex. {'n_estimators": 10}"}
        """
        pass

    @abstractmethod
    def delete_data_split(
        self,
        data_split_name: Optional[str] = None,
        *,
        recursive: bool = False
    ):
        """Delete a data split from the current TruEra workspace. This will only delete artifacts within the current location context (either local or remote).
        Args:
            data_split_name: Name of the data split to be deleted. By default the currently set data split will be deleted.
            recursive: Whether to delete any model tests associated with the data split. Defaults to False.
        """
        pass

    @abstractmethod
    def delete_data_collection(
        self,
        data_collection_name: Optional[str] = None,
        *,
        recursive: bool = False
    ):
        """Delete a data collection from the current TruEra workspace. This will only delete artifacts within the current location context (either local or remote). Note: Data collection can be deleted only after all
            the data splits in the data collection have been deleted.
        Args:
            data_collection_name: Name of the data collection to be deleted. By default the currently set
                data collection will be deleted.
            recursive: Whether to delete any data splits as well in the data collection. Defaults to False.
        """
        pass

    @abstractmethod
    def add_data_split(
        self,
        data_split_name: str,
        pre_data: pd.DataFrame,
        *,
        post_data: Optional[pd.DataFrame] = None,
        label_data: Optional[Union[pd.DataFrame, pd.Series, np.ndarray]] = None,
        label_col_name: Optional[str] = None,
        id_col_name: Optional[str] = None,
        extra_data_df: Optional[pd.DataFrame] = None,
        split_type: Optional[str] = "all",
        **kwargs
    ):
        """Adds a data split to TruEra system from a DataFrame and sets it in the current context.
        Args:
            data_split_name: Name of the split to be added.
            pre_data: A DataFrame containing the split data. If `post_data` is not specified, `pre_data` is assumed to be both human- and model-readable.
                pd.DataFrame:
                    The shape of the data frame should be aligned with the expected shape for the model. In case the data contains the label column
                    and `label_col_name` is provided, the label column will be dropped before uploading the data to the server.
                pyspark.sql.dataframe.DataFrame:
                    This is expected to be a flat DataFrame with one column for each feature. This will sample from the DataFrame according to the provided `sample_count` and `sample_kind`.
            post_data: A pd.DataFrame or PySpark DataFrame containing the model-readable post-processed data that is aligned with the provided pre-processed data. Can be ignored if pre-processed data is provided.
                    If providing different pre- and post-processed data, be sure the mapping between them adheres to the feature map of the data collection specified during the data collection's creation.
                    If providing a PySpark DataFrame, ensure that the DataFrame is flat and contains one column for each feature.
            label_data: The labels or ground truth aligned with the provided pre- and/or post-processed data. Defaults to None.
            label_col_name: Column name for the labels or ground truth in the pre-processed data. Defaults to None.
            id_col_name: Column name for the unique identifier of each data point in both the pre- and post-processed data if provided. This column will be dropped from the data before it is given to the model. Defaults to None.
            split_type: The type of the data split. Options are ["all", "train", "test", "validate", "oot", "custom"]. Defaults to "all".
            extra_data_df: Extra columns which are not used / consumed by the model, but could be used for other analysis like defining segments. Must be aligned with the provided pre- and/or post-processed data.
            **sample_count (Optional[int]): Maximum rows to use when creating the split. Defaults to 5000.
            **sample_kind (Optional[str]): Specifies the strategy to use while sub-sampling the rows.  One of ["random", "first"]. Defaults to "random".
            **seed (Optional[int]): Specifies the seed to use for sampling. Defaults to a deterministic seed.
            **prediction_col_name (Optional[str]): Column name for the predictions or model output in the pre-processed data. Defaults to None.
            **timestamp_col_name (Optional[str]): Column name for the data point timestamps in the pre-processed data. Defaults to None.
            **split_time_range_begin (Optional[Union[str, float, datetime.datetime]]): Begin time for the split. Needed only if split used for monitoring.
            **split_time_range_end (Optional[Union[str, float, datetime.datetime]]): End time for the split. Needed only if split used for monitoring.
        """
        pass

    @abstractmethod
    def add_data_split_from_data_source(
        self,
        data_split_name: str,
        pre_data: Union[Table, str],
        *,
        post_data: Optional[Union[Table, str]] = None,
        label_col_name: Optional[str] = None,
        id_col_name: Optional[str] = None,
        extra_data: Optional[Union[Table, str]] = None,
        split_type: Optional[str] = "all",
        **kwargs
    ):
        """Adds a data split from a remote data source to TruEra system and sets it in the current context.
        Args:
            data_split_name: Name of the split to be added.
            pre_data: A Table or URI of file containing the split data. If `post_data` is not specified, `pre_data` is assumed to be both human- and model-readable.
                Table:
                    Use `add_data_source` or `get_data_source` to get a Table. You can optionally futher filter the Table by applying `filter`.
                URI:
                    Used to load external data source into the system. This is similar to ingesting via `add_data_source` and Table,
                    without the filters. The data in the external data source will be sub-sampled (random or first N) and ingested into the system.
                    By default up to 5000 rows are ingested as the split. You can override this by specifying `sample_count=X`.
                    Sampling is either done by using first N rows or sampling rows randomly (without replacement). Defaults to random. You can override this by specifying `sample_kind="first"`.
            post_data: A Table or URI of file containing the model-readable post-processed data that is aligned with the provided pre-processed data. Can be ignored if pre-processed data is provided.
                    If providing different pre- and post-processed data, be sure the mapping between them adheres to the feature map of the data collection specified during the data collection's creation.
            label_col_name: Column name for the labels or ground truth in the pre-processed data. Defaults to None.
            id_col_name: Column name for the unique identifier of each data point in both the pre- and post-processed data if provided. This column will be dropped from the data before it is given to the model. Defaults to None.
            extra_data: A Table or URI of file for extra columsn which are not used / consumed by the model, but could be used for other analysis like defining segments. Must be aligned with the provided pre- and/or post-processed data.
            split_type: The type of the data split. Options are ["all", "train", "test", "validate", "oot", "custom"]. Defaults to "all".
            **column_spec_file (Optional[str]): File containing list of columns for each split file: pre_transform, post_transform, labels, id column, extra_data, predictions.
            **format (Optional[str]):The format in which the file (local) or blob (AWS S3, Azure WASB etc.) are stored in.
            **column_schema (Optional[Union[str, List[Tuple[str, str]]]]): For providing a schema that should be respected by the data source. This can be provided in the form of a path to a JSON/YAML file containing the schema, or a list columns each represented as a tuple<name:str, static_data_type:str>
            **credential (Optional[Credential]): Provide the credential object if the data source requires authentication to read from it. Defaults to None.
            **first_row_is_header (Optional[bool]): For text based delimited files (csv, tsv etc.), indicates if the first row provides header information. Defaults to True.
            **column_delimiter (Optional[str]): For text based delimited files (csv, tsv etc.), provides the delimiter to separate column values. Defaults to ','.
            **quote_character (Optional[str]): For text based delimited files (csv, tsv etc.), if quotes are used provide the quote character. Defaults to '"'.
            **null_value (Optional[str]): For text based delimited files (csv, tsv etc.), the string that signifies null value. Defaults to 'null'.
            **empty_value (Optional[str]): For text based delimited files (csv, tsv etc.), the string that signifies empty value. Defaults to '""'.
            **date_format (Optional[str]): For text based delimited files (csv, tsv etc.), if any column has date time, provide the format string. Defaults to 'yyyy-MM-dd HH:mm:ssZZ'.
            **account_key (Optional[str]): For reading from Azure Storage Blob (WASB), provide the account_key to be used to read the blob. Not required if `credential` object is provided.
            **access_key_id (Optional[str]): For reading from a s3 bucket, provide the access key id to be used to read the blob. Not required if `credential` object is provided or the underlying deployment is in a role with access to the bucket.
            **secret_access_key (Optional[str]): For reading from a s3 bucket, provide the secret access key to be used to read the blob. Not required if `credential` object is provided or the underlying deployment is in a role with access to the bucket.
            **database_name (Optional[str]): For reading from MySQL database, provide the database name to use. Required for MySQL data source.
            **table_name (Optional[str]): For reading from MySQL database, provide the table name to use. Required for MySQL data source.
            **sample_count (Optional[int]): Maximum rows to use when creating the split. Defaults to 5000.
            **sample_kind (Optional[str]): Specifies the strategy to use while sub-sampling the rows.  One of ["random", "first"]. Defaults to "random".
            **seed (Optional[int]): Specifies the seed to use for sampling. Defaults to a deterministic seed.
            **prediction_col_name (Optional[str]): Column name for the predictions or model output in the pre-processed data. Defaults to None.
            **timestamp_col_name (Optional[str]): Column name for the data point timestamps in the pre-processed data. Defaults to None.
            **pre_data_additional_skip_cols  (Optional[Sequence[str]]): Identical to all_columns_pre except omits the specified columns.
            **timeout_seconds (Optional[int]): Number of seconds to wait for data source. Defaults to 300.
            **split_time_range_begin (Optional[Union[str, float, datetime.datetime]]): Begin time for the split. Needed only if split used for monitoring.
            **split_time_range_end (Optional[Union[str, float, datetime.datetime]]): End time for the split. Needed only if split used for monitoring.
        """
        pass

    def add_data_split_no_features_for_model(
        self,
        data_split_name: str,
        label_data: Union[pd.Series, np.ndarray],
        prediction_data: Optional[Union[pd.Series, np.ndarray]],
        extra_data_df: Optional[pd.DataFrame] = None,
        split_type: Optional[str] = "all",
        **kwargs
    ):
        """Adds a "super lite" data split (split without any feature data) to TruEra system and sets it in the current context.
           These splits require labels and predictions for any virtual model in the split's parent data collection.
        Args:
            data_split_name: Name of the split to be added.
            label_data: The labels or ground truth for the split.
            prediction_data: The prediction data for this split, using the model in the current context.
            extra_data_df: Extra columns which are not used / consumed by the model, but could be used for other analysis like defining segments. Must be aligned with the provided label data.
            split_type: The type of the data split. Options are ["all", "train", "test", "validate", "oot", "custom"]. Defaults to "all".
            **split_time_range_begin (Union[str, float, datetime.datetime]): Begin time for the split. Needed only if split used for monitoring.
            **split_time_range_end (Union[str, float, datetime.datetime]): End time for the split. Needed only if split used for monitoring.
        """
        if len(label_data) != len(prediction_data):
            raise ValueError(
                "Label data and prediction data must be the same length!"
            )
        if label_data.ndim != 1:
            raise ValueError(
                f"Expected single-dimension `label_data`, but provided labels are shape {label_data.shape}!"
            )
        if prediction_data.ndim != 1:
            raise ValueError(
                f"Expected single-dimension `prediction_data`, but provided predictions are shape {prediction_data.shape}!"
            )
        data_df = pd.DataFrame(
            {
                "label_col": label_data,
                "prediction_col": prediction_data
            }
        )
        self.add_data_split(
            data_split_name=data_split_name,
            pre_data=data_df,
            label_col_name="label_col",
            prediction_col_name="prediction_col",
            extra_data_df=extra_data_df,
            split_type=split_type,
            split_mode=sm_pb.SplitMode.SPLIT_MODE_PREDS_REQUIRED,
            **kwargs
        )

    @abstractmethod
    def add_labels(
        self, label_data: Union[Table, str], label_col_name: str,
        id_col_name: str, **kwargs
    ):
        """[Alpha] Add labels to an existing data split.

        Args:
            label_data: A Table or URI of file containing the label data.
                Table:
                    Use `add_data_source` or `get_data_source` to get a Table. You can optionally futher filter the Table by applying `filter`.
                URI:
                    Used to load external data source into the system. This is similar to ingesting via `add_data_source` and Table,
                    without the filters. The data in the external data source will be sub-sampled (random or first N) and ingested into the system.
                    By default up to 5000 rows are ingested as the split. You can override this by specifying `sample_count=X`.
                    Sampling is either done by using first N rows or sampling rows randomly (without replacement). Defaults to random. You can override this by specifying `sample_kind="first"`.
            label_col_name: Column name for the labels or ground truth in the provided label_data.
            id_col_name: Column name for the unique row identifier in the provided label_data.  Used to match labels with corresponding data points.

            **credential (Credential, optional): Provide the credential object if the data source requires authentication to read from it. Defaults to None.
            **format (str):The format in which the file (local) or blob (AWS S3, Azure WASB etc.) are stored in.
            **first_row_is_header (bool): For text based delimited files (csv, tsv etc.), indicates if the first row provides header information. Defaults to True.
            **column_delimiter (str): For text based delimited files (csv, tsv etc.), provides the delimiter to separate column values. Defaults to ','.
            **quote_character (str): For text based delimited files (csv, tsv etc.), if quotes are used provide the quote character. Defaults to '"'.
            **null_value (str): For text based delimited files (csv, tsv etc.), the string that signifies null value. Defaults to 'null'.
            **empty_value (str): For text based delimited files (csv, tsv etc.), the string that signifies empty value. Defaults to '""'.
            **date_format (str): For text based delimited files (csv, tsv etc.), if any column has date time, provide the format string. Defaults to 'yyyy-MM-dd HH:mm:ssZZ'.
            **account_key (str): For reading from Azure Storage Blob (WASB), provide the account_key to be used to read the blob. Not required if `credential` object is provided.
            **access_key_id (str): For reading from a s3 bucket, provide the access key id to be used to read the blob. Not required if `credential` object is provided or the underlying deployment is in a role with access to the bucket.
            **secret_access_key (str): For reading from a s3 bucket, provide the secret access key to be used to read the blob. Not required if `credential` object is provided or the underlying deployment is in a role with access to the bucket.
            **database_name (str): For reading from MySQL database, provide the database name to use. Required for MySQL data source.
            **table_name (str): For reading from MySQL database, provide the table name to use. Required for MySQL data source.
            **sample_count (int): Maximum rows to use when creating the split. Defaults to 5000.
            **sample_kind (str): Specifies the strategy to use while sub-sampling the rows. Defaults to "random".
            **timeout_seconds (int): Number of seconds to wait for data source. Defaults to 300.
        """

        pass

    @abstractmethod
    def add_extra_data(
        self, extra_data: Union[Table, str],
        extras_col_name: Union[str, Sequence[str]], id_col_name: str, **kwargs
    ):
        """[Alpha] Add extra data to an existing data split.
        Args:
            extra_data: A Table or URI of file containing the label data.
                Table:
                    Use `add_data_source` or `get_data_source` to get a Table. You can optionally futher filter the Table by applying `filter`.
                URI:
                    Used to load external data source into the system. This is similar to ingesting via `add_data_source` and Table,
                    without the filters. The data in the external data source will be sub-sampled (random or first N) and ingested into the system.
                    By default up to 5000 rows are ingested as the split. You can override this by specifying `sample_count=X`.
                    Sampling is either done by using first N rows or sampling rows randomly (without replacement). Defaults to random. You can override this by specifying `sample_kind="first"`.
            extras_col_name: Column name(s) for the extra data columns to be ingested.
            id_col_name: Column name for the unique row identifier in the provided label_data.  Used to match labels with corresponding data points.
            **credential (Credential, optional): Provide the credential object if the data source requires authentication to read from it. Defaults to None.
            **format (str):The format in which the file (local) or blob (AWS S3, Azure WASB etc.) are stored in.
            **first_row_is_header (bool): For text based delimited files (csv, tsv etc.), indicates if the first row provides header information. Defaults to True.
            **column_delimiter (str): For text based delimited files (csv, tsv etc.), provides the delimiter to separate column values. Defaults to ','.
            **quote_character (str): For text based delimited files (csv, tsv etc.), if quotes are used provide the quote character. Defaults to '"'.
            **null_value (str): For text based delimited files (csv, tsv etc.), the string that signifies null value. Defaults to 'null'.
            **empty_value (str): For text based delimited files (csv, tsv etc.), the string that signifies empty value. Defaults to '""'.
            **date_format (str): For text based delimited files (csv, tsv etc.), if any column has date time, provide the format string. Defaults to 'yyyy-MM-dd HH:mm:ssZZ'.
            **account_key (str): For reading from Azure Storage Blob (WASB), provide the account_key to be used to read the blob. Not required if `credential` object is provided.
            **access_key_id (str): For reading from a s3 bucket, provide the access key id to be used to read the blob. Not required if `credential` object is provided or the underlying deployment is in a role with access to the bucket.
            **secret_access_key (str): For reading from a s3 bucket, provide the secret access key to be used to read the blob. Not required if `credential` object is provided or the underlying deployment is in a role with access to the bucket.
            **database_name (str): For reading from MySQL database, provide the database name to use. Required for MySQL data source.
            **table_name (str): For reading from MySQL database, provide the table name to use. Required for MySQL data source.
            **sample_count (int): Maximum rows to use when creating the split. Defaults to 5000.
            **sample_kind (str): Specifies the strategy to use while sub-sampling the rows. Defaults to "random".
            **timeout_seconds (int): Number of seconds to wait for data source. Defaults to 300.
        """

        pass

    @abstractmethod
    def add_nn_data_split(
        self,
        data_split_name: str,
        split_load_wrapper: Base.SplitLoadWrapper,
        split_type: Optional[str] = "all"
    ):
        """[Alpha] Upload a time-series tabular data split to TruEra server.
        Args:
            data_split_name: Name of the split to be uploaded.
            split_load_wrapper: A Base.SplitLoadWrapper that helps load data files from files. This must be implemented via subclassing the truera.client.nn.wrappers.Base.SplitLoadWrapper
            split_type: The type of the data split. Options are ["all", "train", "test", "validate", "oot", "custom"]. Defaults to "all".
        """
        pass

    @abstractmethod
    def add_model_predictions(
        self,
        prediction_data: Union[pd.Series, np.ndarray, Table, str],
        *,
        prediction_col_name: Optional[str] = None,
        id_col_name: Optional[str] = None,
        data_split_name: Optional[str] = None
    ):
        """Adds prediction data for the current model. Assumes predictions are calculated for the default score type of the project. Adding predictions is only supported for virtual models.

        Args:
            prediction_data: Prediction data to add. If a pd.Series or np.ndarray is provided, it is assumed that predictions
                are present/fully aligned to all rows in the split. If a Table or string URI is provided, then `prediction_col_name`
                and `id_col_name` must be provided. Partial prediction data can only be provided if ingesting via a Table or string URI with an ID column present.
            prediction_col_name: Column name from which to pull prediction data. Only required if `prediction_data` is a Table or URI.
            id_col_name: Column name for the unique row identifier in the provided `prediction_data`. Used to match predictions with corresponding split data. Only required if `prediction_data` is a Table or URI.
            data_split_name: Data split that predictions are associated with. If None, defaults to split set in the current context.
        """
        pass

    @abstractmethod
    def add_model_feature_influences(
        self,
        feature_influence_data: pd.DataFrame,
        *,
        data_split_name: Optional[str] = None,
        background_data_split_name: Optional[str] = None
    ):
        """Adds feature influence for the current model and split. Assumes influences are calculated for the default score type of the project. Adding influences is only supported for virtual models.

        Args:
            feature_influence_data: Feature influence data to add. Must be aligned with the pre-processed data of the given split.
            data_split_name: Data split that influences are associated with. If None, defaults to split set in the current context.
            background_data_split_name: Background data split that influences are computed against. If None, defaults to the base split of the data collection (if this is not explicitly set, it is an ingested split of type "all" or "train").
        """
        pass

    @abstractmethod
    def attach_packaged_python_model_object(
        self, model_object_dir: str, verify_model: bool = True
    ):
        """Attaches a pre-serialized and packaged executable model object to the current model, which must be virtual.
        This effectively "converts" the virtual model to a non-virtual one, as the system can now call the model to generate predictions.
        Args:
            model_object_dir: Directory where packaged model object is located.
            verify_model: [Alpha] Locally verify the model is packaged properly and can operate on existing split data. Defaults to True.
        """
        pass

    @abstractmethod
    def attach_python_model_object(
        self,
        model_object: Any,
        additional_pip_dependencies: Optional[Sequence[str]] = None,
        verify_model: bool = True,
    ):
        """Attaches the provided executable model object to the current model, which must be virtual.
        This effectively "converts" the virtual model to a non-virtual one, as the system can now call the model to generate predictions.
            Supported Model Frameworks: sklearn, xgboost, catboost, lightgbm, pyspark (tree models only).
            If you cannot ingest your model object via this function due to custom logic, feature transforms, etc., see `attach_packaged_python_model_object()`.

            [ALPHA] For frameworks that are not yet supported, or for custom model implementations the prediction
            function for the model can be provided as the model.
            For binary classifiers, the prediction function should accept a pandas DataFrame as input and produce
            a pandas DataFrame as output with the class probabilities and [0, 1] as the column header.
            For regression models, the prediction function should accept a pandas DataFrame as input and produce
            the result as a pandas DataFrame with "Result" as the column header.
            All required dependencies to execute the prediction function should be provide as additional_pip_dependencies.
            For example:
            ```python
            def predict(df):
                return pd.DataFrame(my_model.predict_proba(df, validate_features=False), columns=[0, 1])
            tru.add_python_model("my_model", predict, additional_pip_dependencies=["xgboost==1.3.1", "pandas==1.1.1"])
            ```
        Args:
            model_object: The Python model object or the prediction function to attach.
                Supported frameworks are catboost, lightgbm, sklearn and xgboost, and tree-based PySpark models. For prediction function, please see the description above.
            additional_pip_dependencies: List of pip dependencies required to execute the model object. If the model object
                is from a supported framework, the pip dependency for that framework is automatically inferred. If a prediction function is provided as the model,
                additional pip dependencies are not automatically inferred and must be explicitly provided.
                Defaults to None. Example: ["pandas==1.1.1", "numpy==1.20.1"]
            verify_model: [Alpha] Locally verify the model is packaged properly and can operate on existing split data. Defaults to True.
        """
        pass

    @abstractmethod
    def add_feature_metadata(
        self,
        feature_description_map: Optional[Mapping[str, str]],
        missing_values: Optional[Sequence[str]] = None,
        force_update: bool = False
    ):
        """Upload metadata describing features and feature groupings to the server.
        Args:
            feature_description_map: Map from pre-processed feature name, as provided in the data, to the description of the feature.
            missing_values: List of strings to be registered as missing values when reading split data.
            force_update: Overwrite any existing feature metadata.
        """
        pass

    @abstractmethod
    def _get_pre_to_post_feature_map(
        self
    ) -> Optional[Mapping[str, Sequence[str]]]:
        pass

    def get_feature_names(self) -> Sequence[str]:
        """Get the feature names associated with the current data-collection.
        Returns:
            Sequence[str]: Feature names.
        """
        return list(self.get_xs(0, 1).columns)

    def get_xs(
        self,
        start: Optional[int] = 0,
        stop: Optional[int] = None,
        extra_data: bool = False,
        system_data: bool = False
    ) -> pd.DataFrame:
        """Get the inputs/data/x-values associated with the current data-split.
        Args:
            start: The lower bound (inclusive) of the index of points to include. Defaults to 0.
            stop: The upper bound (exclusive) of the index of points to include. Defaults to None which is interpreted as the total number of points for local projects and the setting for "Number of default influences" for remote projects.
            extra_data: Include extra data columns in the response. Defaults to False.
            system_data: Include system data (e.g. timestamps) if available in response. Defaults to False.
        Returns:
            The inputs/data/x-values associated with the current data-split.
        """
        pass

    def get_ys(
        self,
        start: Optional[int] = 0,
        stop: Optional[int] = None,
        system_data: bool = False
    ) -> Union[pd.Series, pd.DataFrame]:
        """Get the targets/y-values associated with the current data-split.
        Args:
            start: The lower bound (inclusive) of the index of points to include. Defaults to 0.
            stop: The upper bound (exclusive) of the index of points to include. Defaults to None which is interpreted as the total number of points for local projects and the setting for "Number of default influences" for remote projects.
            system_data: Include system data (e.g. timestamps) if available in response. Defaults to False.
        Returns:
            The targets/y-values associated with the current data-split.
        """
        pass

    def get_ys_pred(
        self,
        start: Optional[int] = 0,
        stop: Optional[int] = None,
        system_data: bool = False,
        wait: bool = True
    ) -> pd.Series:
        """Get the model predictions associated with the current data-split.
        Args:
            start: The lower bound (inclusive) of the index of points to include. Defaults to 0.
            stop: The upper bound (exclusive) of the index of points to include. Defaults to None which is interpreted as the total number of points for local projects and the setting for "Number of default influences" for remote projects.
            system_data: Include system data (e.g. timestamps) if available in response. Defaults to False.
            wait: Whether to wait for the job to finish. Defaults to True.
        Returns:
            The model predictions associated with the current data-split.
        """
        self._ensure_data_split()
        return self.get_explainer(
            self.get_context()["data-split"]
        ).get_ys_pred(start, stop, system_data=system_data, wait=wait)

    def get_feature_influences(
        self,
        start: Optional[int] = 0,
        stop: Optional[int] = None,
        score_type: Optional[str] = None,
        system_data: bool = False,
        wait: bool = True
    ) -> pd.DataFrame:
        """Get the QIIs/shapley-values associated with the current data-split.
        Args:
            start: The lower bound (inclusive) of the index of points to include. Defaults to 0.
            stop: The upper bound (exclusive) of the index of points to include. Defaults to None which is interpreted as the total number of points for local projects and the setting for "Number of default influences" for remote projects.
            score_type: The score type to use when computing influences. If None, uses default score type of project. Defaults to None. For a list of valid score types, see `list_valid_score_types`.
            system_data: Include system data (e.g. timestamps) if available in response. Defaults to False.
            wait: Whether to wait for the job to finish. Defaults to True.
        Returns:
            The QIIs/shapley-values associated with the current data-split.
        """
        self._ensure_data_split()
        return self.get_explainer(self.get_context()["data-split"]
                                 ).get_feature_influences(
                                     start,
                                     stop,
                                     score_type=score_type,
                                     wait=wait,
                                     system_data=system_data
                                 )

    @abstractmethod
    def get_explainer(
        self,
        base_data_split: Optional[str] = None,
        comparison_data_splits: Optional[Sequence[str]] = None
    ) -> Explainer:
        """Get the explainer associated with the TruEra workspace.
        Args:
            base_data_split: The name of the data split to set as the base split for explainer operations.
            comparison_data_splits: The name(s) of the data splits to set as the comparison splits for explainer operations.

        Returns:
            Explainer: Explainer for current context of the TruEra workspace.
        """
        pass

    @abstractmethod
    def add_segment_group(
        self, name: str, segment_definitions: Mapping[str, str]
    ) -> None:
        """[Alpha] Create a segment group where each segments is defined by an SQL expression.
        Args:
            name: The name of the segment group.
            segment_definitions: A dictionary containing the name of the segment and an SQL expression that defines the segment. Supported expressions:
                    `=`  : filters for equality, ex: amount = 1000
                    `!=` : filters for inequality, ex: amount != 1000
                    `<`  : filters for less-than, ex: amount < 1000
                    `<=` : filters for less-than-or-equal, ex: amount <= 1000
                    `>`  : filters for greater-than, ex: amount > 1000
                    `>=` : filters for great-than-or-equal, ex: amount >= 1000
                    `NOT`: filters records if the inner condition is not true, ex: NOT(amount >= 1000)
                    `AND`: filters records if both the conditions are true, ex: (amount >= 1000) AND (state = 'WA')
                    `OR` : filters records if any of the two conditions is true, ex: (amount >= 1000) OR (state = 'WA')
                String literals should be within quotes (''), numeric literals should not have quotes('').
                Left side of a binary expression should be either column name (without quotes) or one of the special keywords (see below for the list of supported special keywords). Right side of an expression should be a literal.
                For example, (amount < salary) is not a valid expression, as both left and right side of the expression are column-names.
                Supported special keywords:
                    _DATA_GROUND_TRUTH : filters using the data label, ex: _DATA_GROUND_TRUTH == 1
                    _MODEL_<score_type>: filters using the <score_type> of the model where <score_type> is "REGRESSION" for regression models or one of ["PROBITS", "LOGITS", "CLASSIFICATION"] for classification models, ex: _MODEL_REGRESSION >= 5
                    _MODEL_<score_type>$<model_name>: filters using the <score_type> of the model with name <model_name> where <score_type> is "REGRESSION" for regression models or one of ["PROBITS", "LOGITS", "CLASSIFICATION"] for classification models, example to filter by "REGRESSION" score of "model_a": _MODEL_REGRESSION$model_a >= 5
        """
        pass

    @abstractmethod
    def set_as_protected_segment(
        self, segment_group_name: str, segment_name: str
    ):
        """Sets the provided segment as a "protected" segment. This enables fairness analysis for this segment.

        Args:
            segment_group_name : Name of segment group.
            segment_name: Name of segment in provided segment group.
        """
        pass

    @abstractmethod
    def delete_segment_group(self, name: str) -> None:
        """[Alpha] Delete a segment group.
        Args:
            name: The name of the segment group.
        """
        pass

    @abstractmethod
    def get_segment_groups(self) -> Mapping[str, Mapping[str, str]]:
        """[Alpha] Get all segment groups associated with the current TruEra workspace, along with their respective segments.
        Returns:
            Mapping[str, Mapping[str, str]]: Mapping of segment group names to the corresponding segment group definition.
        """
        pass

    @abstractmethod
    def get_ingestion_client(self) -> IngestionClient:
        """[Alpha] Get the data ingestion client associated with the TruEra workspace. Valid only for "remote" workspace.
        The ingestion client can be used to pull data from different data sources into TruEra to perform analytics.
        Raises:
            ValueError: Raised if no project is associated with the current workspace. Use set_project
                to set the correct project.
            ValueError: Raised if no data collection is associated with the current workspace. Use set_data_collection
                to set the correct data collection.
            ValueError: Raised if the current project is a local project.
        Returns:
            IngestionClient: IngestionClient for current context of the TruEra workspace.
        """
        pass

    def add_credential(
        self,
        name: str,
        secret: str,
        identity: Optional[str] = None
    ) -> Credential:
        """[Alpha] Add a new credential to TruEra product. The credential is saved in a secure manner and is used
        to authenticate with the data source to be able to perform various operations (read, filter, sample etc.).
        Args:
            name: Friendly name of the credential.
            secret: The secret to be stored.
            identity: Identity portion of the secret. Not needed in all cases. Defaults to None.
        Returns:
            Credential: Returns an object with the credential name and id. The secret is not stored in this object.
        """
        pass

    def get_credential_metadata(self, name: str) -> Credential:
        """[Alpha] Get metadata about a credential in the TruEra product. The credential details are not returned.
        Args:
            name: Friendly name of the credential.
        Returns:
            Credential: Returns an object with the credential name and id.
        """
        pass

    def delete_credential(self, name) -> None:
        """[Alpha] Removes a credential from the TruEra product.
        Args:
            name: Friendly name of the credential.
        """
        pass

    def add_data_source(
        self,
        name: str,
        uri: str,
        credential:
        Credential = None,  # TODO(AB#3679) take cred name as the input
        **kwargs
    ) -> Table:
        """[Alpha] Add a new data source in the system.
        Args:
            name (str): Friendly name of the data source.
            uri (str): URI describing the location of the data source.
                For local files this can be file:///path/to/my/file or /path/to/my/file
                For files stored in Azure Storage Blobs the expected path is wasb://container@account.blob.core.windows.net/blob
            credential (Credential, optional): Provide the credential object if the data source requires authentication to read from it. Defaults to None.
            **format (str):The format in which the file (local) or blob (AWS S3, Azure WASB etc.) are stored in.
            **first_row_is_header (bool): For text based delimited files (csv, tsv etc.), indicates if the first row provides header information. Defaults to True.
            **column_delimiter (str): For text based delimited files (csv, tsv etc.), provides the delimiter to separate column values. Defaults to ','.
            **quote_character (str): For text based delimited files (csv, tsv etc.), if quotes are used provide the quote character. Defaults to '"'.
            **null_value (str): For text based delimited files (csv, tsv etc.), the string that signifies null value. Defaults to 'null'.
            **empty_value (str): For text based delimited files (csv, tsv etc.), the string that signifies empty value. Defaults to '""'.
            **date_format (str): For text based delimited files (csv, tsv etc.), if any column has date time, provide the format string. Defaults to 'yyyy-MM-dd HH:mm:ssZZ'.
            **account_key (str): For reading from Azure Storage Blob (WASB), provide the account_key to be used to read the blob. Not required if `credential` object is provided.
            **database_name (str): For reading from sql databases, provide the database name to use. Required for MySQL or Hive data source.
            **table_name (str): For reading from sql databases, provide the table name to use. Required for MySQL or Hive data source.
        Raises:
            ValueError: Raised if the current project is a local project.
        Returns:
            Table: Returns a Table object which allows interaction with the attached data.
        """
        pass

    def get_data_source(self, name) -> Table:
        """[Alpha] Get a data source that was already created in the system.
        Args:
            name (str): The friendly name of the data source.
        Raises:
            ValueError: Raised if the current project is a local project.
        Returns:
            Table: Returns a Table object which allows interaction with the attached data.
        """
        pass

    def get_data_sources(self) -> Sequence[str]:
        """[Alpha] Get list of data sources attached in the current project.
        Raises:
            ValueError: Raised if the current project is a local project.
        """
        pass

    def delete_data_source(self, name: str):
        """[Alpha] Delete a data source that was already created in the system.
        Args:
            name (str): The friendly name of the data source.
        """
        pass

    @abstractmethod
    def set_influences_background_data_split(
        self,
        data_split_name: str,
        data_collection_name: Optional[str] = None
    ) -> None:
        """Set the background data split used for computing feature influences.
        Args:
            data_split_name: Name of the data split.
            data_collection_name: (Optional) Name of the data collection. Defaults to the current data collection in context.
        """
        pass

    @abstractmethod
    def get_influences_background_data_split(
        self, data_collection_name: Optional[str] = None
    ) -> str:
        """Get the background data split used for computing feature influences.
        Args:
            data_collection_name: (Optional) Name of the data collection. Defaults to the current data collection in context.
        Returns:
            str: Name of the background data split.
        """
        pass

    def _validate_get_model_threshold(self):
        self._ensure_project()
        self._ensure_model()
        if self._get_output_type() == "regression":
            raise ValueError("Regression models do not have model thresholds!")

    @abstractmethod
    def get_model_threshold(self) -> float:
        """Gets the model threshold for the currently set model and score type in the TruEra workspace.
        Returns:
            Optional[float]: The model threshold.
        """
        pass

    @abstractmethod
    def update_model_threshold(self, classification_threshold: float) -> None:
        """Update the classification threshold for the model associated with the TruEra workspace. A model score (probits, logits) that is greater than or equal to the threshold is assigned a positive classification outcome.
        Args:
            classification_threshold: New threshold to update. Ignored for regression models.
        """
        pass

    @abstractmethod
    def get_context(self) -> Mapping[str, str]:
        pass

    @abstractmethod
    def reset_context(self):
        pass

    @abstractmethod
    def _get_project_settings(self,
                              project: str) -> Mapping[str, Union[str, int]]:
        pass

    def activate_client_setting(self, setting_name: str) -> None:
        """
        Activates a setting for client side behavior.
        Args:
            setting_name: Client setting to activate.
        """
        context = LocalContextStorage.get_workspace_env_context()
        context.set_feature_switch_value(setting_name, True)

    def deactivate_client_setting(self, setting_name: str) -> None:
        """
        Deactivates a setting for client side behavior.
        Args:
            setting_name: Client setting to deactivate.
        """
        context = LocalContextStorage.get_workspace_env_context()
        context.set_feature_switch_value(setting_name, False)

    def get_client_setting_value(self, setting_name: str) -> bool:
        """
        Gets current value of a setting for client side behavior.
        """
        context = LocalContextStorage.get_workspace_env_context()
        return context.get_feature_switch_value(setting_name)

    def _validate_score_type(self, score_type: str):
        if score_type is None:
            raise ValueError(
                "Must specify `score_type` when creating projects!"
            )
        if score_type not in self.list_valid_score_types():
            raise ValueError(
                f"Invalid `score_type` of {score_type} was provided."
            )

    def _validate_model_threshold(self, threshold: float, score_type: str):
        if score_type == "regression":
            return None
        if score_type == "probits" or score_type == "classification":
            if threshold is None:
                return 0.5
            if threshold > 1 or threshold < 0:
                raise ValueError(
                    f"Thresholds for score type {score_type} must be between 0 and 1. Provided threshold: {threshold}"
                )
            return threshold
        if score_type == "logits":
            return 0 if threshold is None else threshold
        raise ValueError(
            f"Attempted to set threshold for unrecognized score type {score_type}."
        )

    def _validate_set_project(
        self,
        project: str,
    ):
        if not project in self.get_projects():
            raise ValueError(
                f"No such project \"{project}\"! See `add_project` to add it."
            )

    def _validate_add_project(
        self,
        project: str,
        score_type: str,
        input_type: Optional[str] = "tabular",
        num_default_influences: Optional[int] = None
    ):
        # Returns whether project already exists.
        if project in self.get_projects():
            raise AlreadyExistsError(f"Project \"{project}\" already exists!")
        self._ensure_valid_identifier(project)
        if not score_type:
            raise ValueError(
                "Must specify `score_type` when creating projects!"
            )
        if score_type not in _STRING_TO_QOI:
            raise ValueError(
                f"\"{score_type}\" is not a valid score type! Must be one of {list(_STRING_TO_QOI.keys())}."
            )
        if input_type not in _STRING_TO_INPUT_DATA_FORMAT:
            raise ValueError(
                f"\"{input_type}\" is not a valid input data type! Must be one of {list(_STRING_TO_INPUT_DATA_FORMAT.keys())}."
            )
        if num_default_influences is not None and num_default_influences <= 0:
            raise ValueError("`num_default_influences` must be positive!")

    def _validate_feature_map_types(
        self, pre_to_post_feature_map: Mapping[str, Sequence[str]]
    ):
        if not all(
            isinstance(val, (list, tuple))
            for val in pre_to_post_feature_map.values()
        ):
            raise ValueError(
                "`pre_to_post_feature_map` must map each pre-transform column (str) to all associated post-transform columns (list)"
            )

    def _validate_add_model(self, model_name: str):
        self._ensure_project()
        self._ensure_data_collection()
        if model_name in self.get_models():
            raise AlreadyExistsError(f"Model \"{model_name}\" already exists!")
        self._ensure_valid_identifier(model_name)

    def _validate_add_data_split_generic(
        self,
        data_split_name: str,
        label_data: Optional[Union[pd.DataFrame, pd.Series, np.ndarray]] = None,
        label_col_name: Optional[str] = None,
        split_type: Optional[str] = "all",
        **kwargs
    ):
        self._ensure_project()
        self._ensure_data_collection()
        if data_split_name in self.get_data_splits():
            raise AlreadyExistsError(
                f"Data split \"{data_split_name}\" already exists!"
            )
        self._ensure_valid_identifier(data_split_name)
        valid_split_types = [
            "all", "train", "test", "validate", "oot", "custom"
        ]
        if split_type not in valid_split_types:
            raise ValueError(
                f"Provided `split_type` \"{split_type}\" is not valid! Must be one of {valid_split_types}"
            )
        if kwargs.get("prediction_col_name"):
            self._ensure_model()
        if label_col_name and label_data is not None:
            raise ValueError(
                f"`label_data` and `label_col_name` both given, but at most one is allowed!"
            )

    def _validate_add_data_split(
        self,
        data_split_name: str,
        pre_data: Union[pd.DataFrame, Table, str],
        post_data: Optional[pd.DataFrame] = None,
        label_data: Optional[Union[pd.DataFrame, pd.Series, np.ndarray]] = None,
        label_col_name: Optional[str] = None,
        id_col_name: Optional[str] = None,
        timestamp_col_name: Optional[str] = None,
        extra_data_df: Optional[pd.DataFrame] = None,
        split_type: Optional[str] = "all",
        split_mode: sm_pb.SplitMode = sm_pb.SplitMode.SPLIT_MODE_INVALID,
        upload_via_data_layer: bool = False,
        **kwargs
    ):
        self._validate_add_data_split_generic(
            data_split_name,
            label_data=label_data,
            label_col_name=label_col_name,
            split_type=split_type
        )
        if split_mode != sm_pb.SplitMode.SPLIT_MODE_PREDS_REQUIRED and pre_data is None:
            raise ValueError(
                f"`pre_data` must be provided for this configuration."
            )
        if split_mode != sm_pb.SplitMode.SPLIT_MODE_PREDS_REQUIRED and not isinstance(
            pre_data, pd.DataFrame
        ):
            raise ValueError(
                f"`pre_data` must be of type `pandas.DataFrame`! Was {type(pre_data)}."
            )
        self.validate_split_for_dataframe(
            pre_data,
            post_data,
            label_data,
            label_col_name,
            extra_data_df,
            self._get_pre_to_post_feature_map(),
            self._get_output_type(),
            id_column_name=id_col_name,
            timestamp_col_name=timestamp_col_name,
            prediction_col_name=kwargs.get("prediction_col_name"),
            split_mode=split_mode
        )

    def _validate_add_data_split_from_data_source(
        self,
        data_split_name: str,
        *,
        pre_data: Union[Table, str],
        post_data: Optional[Union[Table, str]] = None,
        label_col_name: Optional[str] = None,
        extra_data: Optional[Union[Table, str]] = None,
        split_type: Optional[str] = "all",
        split_mode: sm_pb.SplitMode = sm_pb.SplitMode.SPLIT_MODE_INVALID,
        **kwargs
    ):
        self._validate_add_data_split_generic(
            data_split_name,
            label_data=None,
            label_col_name=label_col_name,
            split_type=split_type
        )
        if split_mode == sm_pb.SplitMode.SPLIT_MODE_PREDS_REQUIRED:
            if pre_data is not None:
                raise ValueError(
                    "`pre_data` must be None if adding a split without feature data!"
                )
            return
        if split_mode != sm_pb.SplitMode.SPLIT_MODE_PREDS_REQUIRED and not isinstance(
            pre_data, (Table, str)
        ):
            raise ValueError(
                f"`pre_data` must be of type `Table` or `str`! Was {type(pre_data)}."
            )

        #TODO(AB#5195): Validate upload from data source given existing feature map on backend
        for arg, arg_name in [
            (extra_data, "extra_data"), (post_data, "post_data")
        ]:
            if arg is not None:
                #TODO(AB#5143): Support post/extra data for remote data sources.
                raise NotImplementedError(
                    f"Ingesting data split with `{arg_name}` is not yet supported for data sources!"
                )

    def _validate_split_against_data_collection(
        self,
        feature_transform_type: FeatureTransformationType,
        post_data: Optional[Union[pd.DataFrame, Table, str]] = None
    ):
        if feature_transform_type == FEATURE_TRANSFORM_TYPE_PRE_POST_DATA and post_data is None:
            raise ValueError(
                "Cannot add a split without post data when feature transform is set to have pre-/post- transform data."
            )
        elif feature_transform_type in [
            FEATURE_TRANSFORM_TYPE_MODEL_FUNCTION,
            FEATURE_TRANSFORM_TYPE_NO_TRANSFORM
        ] and post_data is not None:
            raise ValueError(
                "Cannot add a split with post data when there is no feature transform or it is being done with a model transform function."
            )

    def _validate_add_labels(self, label_data: Union[Table, str]):
        self._ensure_project()
        self._ensure_data_collection()
        self._ensure_data_split()
        if not (isinstance(label_data, (Table, str))):
            raise ValueError("`label_data` must be of type `Table` or `str`!")

    def _validate_add_extra_data(self, extra_data: Union[Table, str]):
        self._ensure_project()
        self._ensure_data_collection()
        self._ensure_data_split()
        if not (isinstance(extra_data, (Table, str))):
            raise ValueError(
                f"`extra_data` is type {type(extra_data).__name__} but must be of type `Table` or `str`! "
            )

    def _validate_add_nn_data_split(self, data_split_name: str):
        self._ensure_project()
        self._ensure_data_collection()
        if data_split_name in self.get_data_splits():
            raise AlreadyExistsError(
                f"Data split \"{data_split_name}\" already exists!"
            )
        self._ensure_valid_identifier(data_split_name)

    def _validate_set_data_collection(self, data_collection_name: str):
        # Returns whether data collection already exists.
        self._ensure_valid_identifier(data_collection_name)
        self._ensure_project()
        if data_collection_name not in self.get_data_collections():
            raise ValueError(
                f"No such data collection \"{data_collection_name}\"! See `add_data_collection` to add it."
            )

    def _is_feature_map_identity_transform(
        self, pre_to_post_feature_map: Optional[Mapping[str, Sequence[str]]]
    ) -> bool:
        if pre_to_post_feature_map is None:
            return True
        return all(
            len(v) == 1 and k == v[0]
            for k, v in pre_to_post_feature_map.items()
        )

    def _validate_pre_to_post_feature_map(
        self, pre_to_post_feature_map: Optional[Mapping[str, Sequence[str]]]
    ) -> bool:
        if pre_to_post_feature_map:
            post_features = list()
            for features in pre_to_post_feature_map.values():
                for f in features:
                    if f in post_features:
                        raise ValueError(
                            "Feature transform with many-to-many mapping is not supported."
                        )
                    else:
                        post_features.append(f)

    def _validate_add_data_collection(
        self,
        data_collection_name: str,
        pre_to_post_feature_map: Optional[Mapping[str, Sequence[str]]] = None,
        provide_transform_with_model: Optional[bool] = None
    ):
        self._ensure_valid_identifier(data_collection_name)
        self._ensure_project()
        if data_collection_name in self.get_data_collections():
            raise AlreadyExistsError(
                f"Data collection \"{data_collection_name}\" already exists!"
            )
        self._validate_pre_to_post_feature_map(pre_to_post_feature_map)
        if pre_to_post_feature_map and provide_transform_with_model is None and not self._is_feature_map_identity_transform(
            pre_to_post_feature_map
        ):
            raise ValueError(
                "Must use `provide_transform_with_model` to specify how feature mapping will be done in this data collection."
            )

    def _validate_explainer_context(
        self, context: Mapping[str, Union[Sequence[str], str]]
    ):
        keys = ["project", "model", "data-collection", "data-split"]
        for key in keys:
            if key not in context:
                raise ValueError(f"Context does not contain {key} key!")
            if not context[key]:
                raise ValueError(
                    f"Provided {key} cannot be set to \"{context[key]}\"!"
                )

    def _create_base_context(
        self,
        project: Optional[str] = None,
        model: Optional[str] = None,
        data_collection: Optional[str] = None,
        data_split: Optional[str] = None
    ) -> Mapping[str, Union[Sequence[str], str]]:
        return {
            "project": project or "",
            "data-collection": data_collection or "",
            "data-split": data_split or "",
            "model": model or "",
        }

    def _verify_nn_wrappers(
        self,
        clf: NNBackend.Model,
        model_input_type: str,
        model_output_type: str,
        *,
        model_run_wrapper: Base.ModelRunWrapper,
        split_load_wrapper: Base.SplitLoadWrapper,
        model_load_wrapper: Optional[Base.ModelLoadWrapper] = None,
        tokenizer_wrapper: Optional[NLP.TokenizerWrapper] = None,
        attr_config: Optional[AttributionConfiguration] = None,
        logger: Optional[logging.Logger] = None
    ) -> None:
        """ Passes the wrapper implementations to the validation step.
        Args:
            clf (NNBackend.Model): The model object in memory.
            model_input_type (str): The type of input. Currently supports 'time_series_tabular' and 'text'.
            model_output_type (str): The type of output. currently supports 'classification' and 'regression'.
            model_run_wrapper (Base.ModelRunWrapper): A wrapper to run a model.
            model_load_wrapper (Base.ModelLoadWrapper): A wrapper to load a model.
            split_load_wrapper (Base.SplitLoadWrapper): A wrapper to load split data.
            tokenizer_wrapper (Optional[NLP.TokenizerWrapper]): A wrapper to run a tokenizer. Only needed for 'text'
            attr_config (AttributionConfiguration): A configuration file for the project.
            logger (logging.Logger): The logger.
        """
        if attr_config is None:
            raise ValueError(
                f"Please pass in an `AttributionConfiguration` to the attr_config parameter"
            )
        verify_nn_ingestion.verify_split(
            split_load_wrapper.get_data_path(),
            split_load_wrapper,
            tokenizer_wrapper=tokenizer_wrapper,
            logger=logger
        )
        verify_nn_ingestion.verify_run(
            model_input_type=model_input_type,
            model_output_type=model_output_type,
            split_path=split_load_wrapper.get_data_path(),
            split_wrapper=split_load_wrapper,
            model=clf,
            model_run_wrapper=model_run_wrapper,
            model_load_wrapper=model_load_wrapper,
            tokenizer_wrapper=tokenizer_wrapper,
            attr_config=attr_config,
            logger=logger
        )

    @abstractmethod
    def _get_score_type(self):
        pass

    @abstractmethod
    def _get_input_type(self):
        pass

    def _get_output_type(self) -> str:
        return get_output_type_from_score_type(self._get_score_type())

    @abstractmethod
    def get_rnn_user_configs(
        self
    ) -> Union[RNNAttributionConfiguration, RNNUserInterfaceConfiguration]:
        """
        Get RNN user configurations for project and model set in the current context.
        Returns:
            Union[RNNAttributionConfiguration, RNNUserInterfaceConfiguration]: RNN user config.
        """
        pass

    @abstractmethod
    def update_rnn_user_config(
        self, config: Union[RNNAttributionConfiguration,
                            RNNUserInterfaceConfiguration]
    ):
        """
        Update RNN user configurations for project and model set in the current context.
        Args:
            config: Config to set.
        """
        pass

    @abstractmethod
    def add_model_metadata(
        self,
        train_split_name: Optional[str] = None,
        train_parameters: Optional[Mapping[str, Any]] = None,
        overwrite: bool = False
    ) -> None:
        """
        Add or update metadata for the current model in context.
        Args:
            train_split_name: The name of the train split of the model
            train_parameters: Train parameters of the model. Ex. {'n_estimators": 10}"}
            overwrite: Overwrite existing values (if exist).
        """
        pass

    @abstractmethod
    def delete_model_metadata(self) -> None:
        """ Unset `train_split_name` and `train_parameters` for the current model in context.
        """
        pass

    @abstractmethod
    def get_model_metadata(self) -> Mapping[str, Union[str, Mapping[str, str]]]:
        """ Get model metadata for the current model in context.
        """
        pass

    @abstractmethod
    def _get_model_metadata(
        self, model_name: str
    ) -> Mapping[str, Union[str, Mapping[str, str]]]:
        """ Get model metadata for the given `model_name`
        """
        pass

    def _get_current_active_project_name(self) -> str:
        return self.get_context()["project"]

    def _get_current_active_model_name(self) -> str:
        return self.get_context()["model"]

    def _get_current_active_data_collection_name(self) -> str:
        return self.get_context()["data-collection"]

    def _get_current_active_data_split_name(self) -> str:
        return self.get_context()["data-split"]

    def _ensure_project(self) -> str:
        project_name = self._get_current_active_project_name()
        if not project_name:
            raise ValueError("Set the current project using `set_project`")
        return project_name

    def _ensure_data_collection(self) -> str:
        data_collection_name = self._get_current_active_data_collection_name()
        if not data_collection_name:
            raise ValueError(
                "Set the current data_collection using `set_data_collection`"
            )
        return data_collection_name

    def _ensure_data_split(self) -> str:
        split_name = self._get_current_active_data_split_name()
        if not split_name:
            raise ValueError(
                "Set the current data_split using `set_data_split`"
            )
        return split_name

    def _ensure_model(self) -> str:
        model_name = self._get_current_active_model_name()
        if not model_name:
            raise ValueError("Set the current model using `set_model`")
        return model_name

    def _delete_empty_project(self):
        """Delete the currently set project non-recursively. This should only be called when all child models and data are deleted already.
        """
        pass

    def delete_project(self, project_name: Optional[str] = None):
        """Delete a project from the current TruEra workspace. This will only delete artifacts within the current location context (either local or remote).
        Args:
            project_name: Name of the project to be deleted. By default the currently set project will be deleted.
        """
        if project_name is None:
            raise ValueError("`project_name` must be set!")
        if project_name != self._get_current_active_project_name(
        ) and project_name not in self.get_projects():
            raise ValueError(f"Not a valid project: {project_name}!")
        with WorkspaceContextCleaner(self):
            self.set_project(project_name)
            for model_name in self.get_models():
                self.delete_model(model_name)
            for data_collection_name in self.get_data_collections():
                self.delete_data_collection(
                    data_collection_name, recursive=True
                )
            self._delete_empty_project()

    def _ensure_valid_identifier(self, artifact_name):
        ensure_valid_identifier(
            to_check=artifact_name,
            context=None,
            ignore_empty=False,
            logger=None,
            raise_value_error=True
        )

    def _validate_data_collection(self, data_collection_name: str) -> None:
        if data_collection_name not in self.get_data_collections():
            raise ValueError(
                f"Data collection \"{data_collection_name}\" does not exist!"
            )

    def _validate_add_segment_group(
        self, name: str, segment_definitions: Mapping[str, str]
    ) -> None:
        self._ensure_project()
        # Even though technically one can create a segment without data split, for safety we'll require data split
        # so that we can check that the features given in the segment_definitions are valid features
        self._ensure_data_collection()
        self._ensure_data_split()
        if not name:
            raise ValueError("Segment group name cannot be empty!")
        if not segment_definitions:
            raise ValueError("`segments_definitions` cannot be empty!")

    def _print_change_data_collection_message(
        self, logger: logging.Logger, from_data_collection_name: str,
        to_data_collection_name: str, is_remote: bool
    ) -> None:
        environment = "remote" if is_remote else "local"
        if from_data_collection_name:
            message = ""
            if to_data_collection_name:
                message += f"Data collection in {environment} environment is now set to \"{to_data_collection_name}\". "
            message += f"The previous data collection (\"{from_data_collection_name}\") and its associated data splits and/or models have been cleared from the {environment} environment workspace context."
            logger.info(message)

    def _print_add_data_split_message(
        self, logger: logging.Logger, data_split_name: str, is_remote: bool
    ) -> None:
        environment = "remote" if is_remote else "local"
        logger.info(
            f"Data split \"{data_split_name}\" is added to {environment} data collection \"{self._get_current_active_data_collection_name()}\", and set as the data split for the workspace context."
        )

    def _print_add_model_message(
        self, logger: logging.Logger, model_name: str,
        data_collection_name: str, is_remote: bool
    ) -> None:
        environment = "remote" if is_remote else "local"
        logger.info(
            f"Model \"{model_name}\" is added and associated with {environment} data collection \"{data_collection_name}\". \"{model_name}\" is set as the model for the workspace context."
        )

    def _print_model_associated_with_different_data_collection_message(
        self, logger: logging.Logger, model_name: str,
        data_collection_name: str, current_data_collection_name: str,
        is_remote: bool
    ) -> None:
        environment = "remote" if is_remote else "local"
        if current_data_collection_name and data_collection_name != current_data_collection_name:
            logger.info(
                f"Model \"{model_name}\" in {environment} is associated with a different data_collection "
                f"(\"{data_collection_name}\") than the one in context (\"{current_data_collection_name}\")."
            )

    def _print_set_model_context(
        self, logger: logging.Logger, model_name: str, is_remote: bool
    ) -> None:
        environment = "remote" if is_remote else "local"
        logger.info(f"Setting {environment} model context to \"{model_name}\".")

    def validate_split_for_dataframe(
        self,
        pre_data: Optional[pd.DataFrame],
        post_data: Optional[pd.DataFrame],
        label_data: Optional[Union[pd.DataFrame, pd.Series, np.ndarray]],
        label_col_name: Optional[str],
        extra_data_df: Optional[pd.DataFrame],
        pre_to_post_feature_map: Optional[Mapping[str, Sequence[str]]],
        output_type: str,
        id_column_name: Optional[str] = None,
        timestamp_col_name: Optional[str] = None,
        prediction_col_name: Optional[str] = None,
        split_mode=sm_pb.SplitMode.SPLIT_MODE_DATA_REQUIRED
    ):
        # verify types and length of rows
        if pre_data is not None and not isinstance(pre_data, pd.DataFrame):
            raise ValueError("`pre_data` must be of type `pandas.DataFrame`!")
        if post_data is not None:
            if not isinstance(post_data, pd.DataFrame):
                raise ValueError(
                    "`post_data` must be of type `pandas.DataFrame`!"
                )
            if len(pre_data) != len(post_data):
                raise ValueError(
                    f"Length of `pre_data` and `post_data` must match! `pre_data` has length {len(pre_data)} but `post_data` has length {len(post_data)}."
                )
        if split_mode != sm_pb.SplitMode.SPLIT_MODE_PREDS_REQUIRED:
            if label_data is not None and len(label_data) != len(pre_data):
                raise ValueError(
                    f"`label_data` and `pre_data` must have the same number of rows!"
                )
        if extra_data_df is not None and len(extra_data_df) != len(pre_data):
            raise ValueError(
                f"`extra_data_df` and `pre_data` must have the same number of rows!"
            )
        expected_label_cols = 1 + (1 if id_column_name is not None else 0)
        if label_data is not None and (
            label_data.ndim > expected_label_cols and
            label_data.shape[1] != expected_label_cols
        ):
            raise ValueError(
                f"`label_data` has {label_data.shape[1]} columns! Pass in a one-dimensional np.ndarray, a pd.Series or a single-column pd.DataFrame."
            )

        # verify presence of special cols
        if isinstance(pre_data, pd.DataFrame):
            # devnote: we could consider applying this check to tables too.
            pre_data_columns = pre_data.columns
            if id_column_name:
                if id_column_name not in pre_data_columns:
                    raise ValueError(
                        f"Provided `id_column_name` \"{id_column_name}\" not found in `pre_data`!"
                    )
                if post_data is not None and id_column_name not in post_data.columns:
                    raise ValueError(
                        f"Provided `id_column_name` \"{id_column_name}\" not found in `post_data`!"
                    )
            if label_col_name and label_col_name not in pre_data_columns:
                raise ValueError(
                    f"Provided `label_col_name` \"{label_col_name}\" not found in `pre_data`!"
                )
            if prediction_col_name and prediction_col_name not in pre_data_columns:
                raise ValueError(
                    f"Provided `prediction_column_name` \"{prediction_col_name}\" not found in `pre_data`!"
                )
            num_pre_cols = len(pre_data_columns) - bool(
                prediction_col_name
            ) - bool(label_col_name) - bool(id_column_name)
            if num_pre_cols <= 0 and split_mode != sm_pb.SplitMode.SPLIT_MODE_PREDS_REQUIRED:
                raise ValueError(
                    "Provided `pre_data` DataFrame does not have any non-label or non-prediction columns!"
                )

        # verify against feature map
        if pre_to_post_feature_map:
            pre_data_dropping_cols = pre_data
            post_data_dropping_cols = post_data
            if id_column_name:
                pre_data_dropping_cols = pre_data_dropping_cols.drop(
                    columns=[id_column_name]
                )
                post_data_dropping_cols = post_data_dropping_cols.drop(
                    columns=[id_column_name]
                )
            if timestamp_col_name:
                pre_data_dropping_cols = pre_data_dropping_cols.drop(
                    columns=[timestamp_col_name]
                )
            self.validate_split_with_feature_map(
                pre_to_post_feature_map, pre_data_dropping_cols,
                post_data_dropping_cols
            )

        # verify label values
        label_verification_fn = verify_label_values_for_classification if output_type == "classification" else verify_label_values_for_regression
        label_data_to_verify = label_data
        if label_col_name:
            label_data_to_verify = pre_data[label_col_name]
        elif isinstance(
            label_data, pd.DataFrame
        ) and id_column_name in label_data.columns:
            col_to_index = [
                c for c in label_data.columns if c != id_column_name
            ][0]
            label_data_to_verify = label_data_to_verify[col_to_index]
        if label_data_to_verify is not None:
            label_verification_fn(label_data_to_verify)

    def validate_split_with_feature_map(
        self, feature_map: Mapping[str, Sequence[str]], pre_data: pd.DataFrame,
        post_data: Optional[pd.DataFrame]
    ):
        pre_features_from_map = set(feature_map.keys())
        pre_features_from_data = set(pre_data.columns)
        post_features_from_map = set(
            itertools.chain.from_iterable(feature_map.values())
        )
        if pre_features_from_map != pre_features_from_data:
            missing_cols = sorted(
                list(pre_features_from_map - pre_features_from_data)
            )
            added_cols = sorted(
                list(pre_features_from_data - pre_features_from_map)
            )
            raise ValueError(
                f"`pre_data` does not match existing feature map! Missing columns: {missing_cols} \nAdditional columns: {added_cols}"
            )
        if post_features_from_map:
            if post_data is None:
                self.logger.warning(
                    "Feature map detected, but post-transformed data is not provided with this split. Make sure that uploaded models contain a transform function to perform the feature mapping!"
                )
            else:
                post_features_from_data = set(post_data.columns)
                missing_cols = sorted(
                    list(post_features_from_map - post_features_from_data)
                )
                added_cols = sorted(
                    list(post_features_from_data - post_features_from_map)
                )
                if missing_cols or added_cols:
                    raise ValueError(
                        f"`post_data` does not match existing feature map! Missing columns: {missing_cols} \nAdditional columns: {added_cols}"
                    )

    def _get_str_desc_of_segment_groups(
        self, segment_groups: Mapping[str, SegmentGroup]
    ) -> Mapping[str, Mapping[str, str]]:
        sg_description = {}
        for sg_name in segment_groups:
            sg_description[sg_name] = {}
            segments = segment_groups[sg_name].get_segments()
            for segment_name in segments:
                sg_description[sg_name][segment_name] = segments[
                    segment_name].ingestable_definition()
        return sg_description

    @abstractmethod
    def schedule_ingestion(self, raw_json: str, cron_schedule: str):
        """[Alpha] Schedule a new scheduled ingestion based off a JSON request tree.

        Templating:
            Templating is supported for uris, split names, and filter expessions for scheduled
            ingestion.  The scheduler passes in several variables and functions when evaluating the
            supported field, which can be accessed by using the syntax: ${<field>}.

            For example, to add the run date to the split name you can add the following suffix when
            submitting a split name to scheduled ingestion: "split_name_${formatDate("yyyy-MM-dd", now)}"

            Supported variables:
                - now: The Date of the run.
                - last: The Date of the last run.
                - lastSuccess: The Date of the last successful run.

            Supported functions:
                - uuid(): Generate a random v4 uuid.
                - formatDate(<format>, <date>): Format the given Date as a string.  Format follows
                    Java SimpleDateFormat (https://docs.oracle.com/javase/7/docs/api/java/text/SimpleDateFormat.html).
                - epochMillis(<date>): The epoch millis of the given Date.

        Args:
            raw_json (str): The JSON string representation of the request tree.  To build a json
                string, you can use the serialize_split function.
            cron_schedule (str): The schedule for the periodic ingestion.  Follows cron unix format:
                ┌───────────── minute (0 - 59)
                │ ┌───────────── hour (0 - 23)
                │ │ ┌───────────── day of the month (1 - 31)
                │ │ │ ┌───────────── month (1 - 12)
                │ │ │ │ ┌───────────── day of the week (0 - 6) (Sunday to Saturday;
                │ │ │ │ │                                   7 is also Sunday on some systems)
                │ │ │ │ │
                │ │ │ │ │
                * * * * *

                For example, to run a cron on the first of every month: "0 0 1 * *"


        Returns:
            str: A workflow_id for looking up the workflow.
        """
        pass

    @abstractmethod
    def get_scheduled_ingestion(self, workflow_id: str):
        """[Alpha] Get the metadata about a scheduled ingestion from a workflow_id
        Args:
            workflow_id (str): The id of the scheduled ingestion workflow.
        Returns:
            Returns an object containing the request_template, schedule, and run_results of a workflow.
        """
        pass

    @abstractmethod
    def schedule_existing_data_split(
        self, split_name: str, cron_schedule: str, override_split_name: str
    ):
        """[Alpha] Schedule a new scheduled ingestion based off an existing split.
        Args:
            split_name (str): The name of an already materialized split.
            cron_schedule (str): The schedule for the periodic ingestion.  Follows cron unix format:
                ┌───────────── minute (0 - 59)
                │ ┌───────────── hour (0 - 23)
                │ │ ┌───────────── day of the month (1 - 31)
                │ │ │ ┌───────────── month (1 - 12)
                │ │ │ │ ┌───────────── day of the week (0 - 6) (Sunday to Saturday;
                │ │ │ │ │                                   7 is also Sunday on some systems)
                │ │ │ │ │
                │ │ │ │ │
                * * * * *

                For example, to run a cron on the first of every month: "0 0 1 * *"
            override_split_name (str): The name of the new splits to be created.  For information on
                templating, see the schedule_ingestion function.
        Returns:
            str: A workflow_id for looking up the workflow.
        """
        pass

    @abstractmethod
    def serialize_split(
        self,
        split_name: str,
        override_split_name: str = None,
    ) -> str:
        """[Alpha] Build a request tree represented as a JSON string.

        Templating:
            Templating is supported for uris, split names, and filter expessions for scheduled
            ingestion.  The scheduler passes in several variables and functions when evaluating the
            supported field, which can be accessed by using the syntax: ${<field>}.

            For example, to add the run date to the split name you can add the following suffix when
            submitting a split name to scheduled ingestion: "split_name_${formatDate("yyyy-MM-dd", now)}"

            Supported variables:
                - now: The Date of the run.
                - last: The Date of the last run.
                - lastSuccess: The Date of the last successful run.

            Supported functions:
                - uuid(): Generate a random v4 uuid.
                - formatDate(<format>, <date>): Format the given Date as a string.  Format follows
                    Java SimpleDateFormat (https://docs.oracle.com/javase/7/docs/api/java/text/SimpleDateFormat.html).
                - epochMillis(<date>): The epoch millis of the given Date.

        Args:
            split_name (str): The name of an already materialized split.
            override_split_name (str): The optional name to replace the original split name.  For
                information on templating, see the schedule_ingestion function.
        Returns:
            str: A JSON string representing the request tree that can be used for scheduled ingestion.
        """
        pass

    @abstractmethod
    def cancel_scheduled_ingestion(self, workflow_id: str) -> str:
        """[Alpha] Cancel a scheduled ingestion.

        Args:
            workflow_id (str): The id of the scheduled ingestion workflow.
        Returns:
            Returns an object containing the canceled_on timestamp of a workflow.
        """
        pass

    @abstractmethod
    def list_scheduled_ingestions(
        self, last_key: str = None, limit: int = 50
    ) -> str:
        """[Alpha] List workflows.

        Args:
            last_key (str): The last id to fetch workflows after. Defaults to None.
            limit (int): The number of workflows to fetch. Defaults to 50.

        Returns:
            Returns a list of objects containing the workflow_id and active state of all workflows.
        """
        pass


class WorkspaceContextCleaner:
    """Utility to complete workspace operations but return to original context. 
    """

    def __init__(self, tru: BaseTrueraWorkspace):
        self.tru = tru
        self.context: Mapping[str, str] = {}

    def __enter__(self):
        self.context = self.tru.get_context()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # devnote: we could check that these projects, splits etc. still exist before setting them
        # but we do this validation in the setters anyways.
        # wrapping in try-catches to avoid duplicate calls to list/validate artifact names.
        self.tru.reset_context()
        # try to set project. if it fails, reset everything.
        try:
            self.tru.set_project(self.context.get("project"))
        except:
            return True

        # try to set data collection and split. if it fails, reset dc and split.
        try:
            self.tru.set_data_collection(self.context.get("data-collection"))
            self.tru.set_data_split(self.context.get("data-split"))
        except:
            pass

        # set model
        try:
            self.tru.set_model(self.context.get("model"))
        except:
            pass
        if exc_val:
            raise exc_val
        return True
