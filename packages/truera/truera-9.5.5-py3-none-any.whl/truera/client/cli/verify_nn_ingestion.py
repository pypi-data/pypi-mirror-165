# pylint: disable=import-error
from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from dataclasses import fields
import logging
from logging import Logger
import os
from pathlib import Path
import sys
import types
from typing import Any, Dict, Optional, Sequence

import numpy as np
import yaml

from truera.client.nn import NNBackend as WrapperNNBackend
from truera.client.nn.client_configs import AttributionConfiguration
from truera.client.nn.client_configs import Dimension
from truera.client.nn.client_configs import Layer
from truera.client.nn.client_configs import LayerAnchor
from truera.client.nn.client_configs import NLPAttributionConfiguration
from truera.client.nn.client_configs import RNNAttributionConfiguration
from truera.client.nn.wrappers import Base
from truera.client.nn.wrappers.nlp import NLP
from truera.client.nn.wrappers.timeseries import Timeseries


class RequiredFileNotFoundException(Exception):

    def __init__(self, message):
        self.message = message


class ArgValidationException(Exception):

    def __init__(self, message):
        self.message = message


class WrapperOutputValidationException(Exception):

    def __init__(self, message):
        self.message = message


class convert_struct:
    """
    convert yaml entries to dict.
    """

    def __init__(self, **entries):
        self.__dict__.update(entries)


def _add_ingestion_path(model_path):
    """
    Add local wrapper location to sys path for testing.
    """
    code_path = os.path.abspath(model_path)
    wrappers_file = "ingestion_wrappers.py"
    if not wrappers_file in os.listdir(code_path):
        raise RequiredFileNotFoundException(
            "%s was not found in supplied dir: %s. Please see CLI documentation on packaging %s."
            % (wrappers_file, model_path, wrappers_file)
        )
    if code_path not in sys.path:
        sys.path.append(code_path)


def load_yaml(yaml_filepath):
    with open(yaml_filepath, "r") as stream:
        config = yaml.safe_load(stream)
    for k, v in config.items():
        if "path" in k:
            config[k] = os.path.expandvars(v)
    return convert_struct(**config)


def assert_arg_val(
    name: str,
    arg: Any,
    arg_type: Any,
    source: Any = AttributionConfiguration
) -> None:
    """Checks if arguments are the right type.

    Args:
        name (str): name of the argument
        arg (Any): the argument.
        arg_type (Any): the type the argument should be.
        source (Any, optional): The source that the argument comes from. Usually from the configs

    Raises:
        ArgValidationException: If the argument is the wrong type, raise this exception.
    """
    if arg is None or not isinstance(arg, arg_type):
        raise ArgValidationException(
            f"{name} arg from {source} must be of type {arg_type}. Instead got {str(type(arg))}:{str(arg)}"
        )


def _assert_truera_elements_shape(
    truera_elements: Dict[str, Any],
    key: str,
    shape: Sequence[int],
    shape_desc: str,
    logger: Logger,
    additional_logger_info: str = ""
) -> None:
    if truera_elements[key].shape != shape:
        raise WrapperOutputValidationException(
            f"ModelRunWrapper.ds_elements_to_truera_elements[\"{key}\"] should be an array of size {shape_desc}. Expecting {shape} but received {truera_elements[key].shape}.{additional_logger_info}"
        )
    print(f"Passed! {key} size check,")


def _assert_attention_mask_truera_elements(
    truera_elements: Dict[str, Any]
) -> None:
    """Validate the 'attention_mask' data.

    Args:
        truera_elements (Dict[str, Any]): The dictionary of truera elements.
    """
    assert truera_elements['attention_mask'].shape == truera_elements[
        "token_ids"].shape
    # The attention mask should add nothing over 0s and 1s.
    assert len(
        np.union1d([0, 1], np.unique(truera_elements['attention_mask']))
    ) == 2


def _assert_lengths_truera_elements(
    n_time_step_input: int, truera_elements: Dict[str, Any], batch_size: int,
    logger: Logger
):
    """Validate the 'lengths' data.

    Args:
        n_time_step_input (int): The number of input timesteps
        truera_elements (Dict[str, Any]): The dictionary of truera elements.
        batch_size (int): the number of items in a batch.
        logger (Logger): The logger object
    """
    _assert_truera_elements_shape(
        truera_elements, "lengths", (batch_size,), "(batch_size,)", logger
    )

    lengths_data = truera_elements['lengths']
    min_val = np.min(lengths_data)
    max_val = np.max(lengths_data)
    if min_val < 1:
        raise WrapperOutputValidationException(
            f"ModelRunWrapper.ds_elements_to_truera_elements[\"lengths\"] has minimum value of {min_val}. Length values must be between 1 and AttributionConfiguration.n_time_step_input:{n_time_step_input}"
        )
    if max_val > n_time_step_input:
        raise WrapperOutputValidationException(
            f"ModelRunWrapper.ds_elements_to_truera_elements[\"lengths\"] has maximum value of {max_val}. Length values must be between 1 and AttributionConfiguration.n_time_step_input:{n_time_step_input}"
        )
    if min_val == max_val and max_val != n_time_step_input:
        logger.warning(
            f"ModelRunWrapper.ds_elements_to_truera_elements[\"lengths\"] are all the same length of {max_val}, even though the AttributionConfiguration.n_time_step_input is {n_time_step_input}. You may want to double check that this is intentional."
        )


def _assert_dimension_ordering(
    config_value: Sequence[Dimension], truera_elements: Dict[str, Any],
    truera_key: str, expected_dimensions: Sequence[Dimension],
    expected_dimensions_config_values: Sequence[int],
    expected_dimensions_strs: Sequence[str], logger: Logger
) -> None:
    """
    validates the dimension orderings
    Parameters
    ===============
    config_value: one of input_dimension_order, output_dimension_order, internal_dimension_order
    truera_key: the key of the data to check in truera_elements
    expected_dimensions: the dimensions expected in the config value
    expected_dimensions_config_values: the config value numbers associated with the expected dimensions. Should be indexed the same as expected_dimensions
    expected_dimensions_strs: the string values associated with the expected dimension. Should be indexed the same as expected_dimensions
    """
    assert len(config_value) == 3
    # Check that the config values contain expected dimensions
    for dimension in expected_dimensions:
        assert dimension in config_value
    expected_shape = []
    expected_shape_str_components = []
    # In the order of the config value dimensions, construct the expected shapes and logging errors if not matching
    for dimension in config_value:
        for i in range(len(expected_dimensions)):
            if dimension == expected_dimensions[i]:
                expected_shape.append(expected_dimensions_config_values[i])
                expected_shape_str_components.append(
                    expected_dimensions_strs[i]
                )
    _assert_truera_elements_shape(
        truera_elements, truera_key, tuple(expected_shape),
        "%s x %s x %s" % tuple(expected_shape_str_components), logger
    )


def assert_get_feature_names(data_wrapper, split_path, logger):
    if isinstance(data_wrapper.get_feature_names, types.FunctionType):
        feature_names = data_wrapper.get_feature_names(split_path)
    else:
        feature_names = data_wrapper.get_feature_names()
    if not isinstance(feature_names, list):
        raise WrapperOutputValidationException(
            "DataWrapper.get_feature_names must be a list. instead got %s" %
            str(type(feature_names))
        )

    for feature in feature_names:
        if not isinstance(feature, str):
            raise WrapperOutputValidationException(
                "DataWrapper.get_feature_names must be a list of \"str\". instead got %s:%s"
                % (str(type(feature)), feature)
            )

    print("Passed! DataWrapper.get_feature_names")
    return feature_names


def assert_feature_names_match_sizes(
    truera_elements: Dict[str, Any],
    feature_names: Sequence[str],
    model_run_wrapper: Timeseries.ModelRunWrapper,
    logger: Logger,
    feature_dimension: int = 2
) -> None:
    features_shape = truera_elements["features"].shape
    num_features = features_shape[feature_dimension]
    one_hot_sizes = model_run_wrapper.get_one_hot_sizes()
    if truera_elements.get("preprocessed_features") is not None:
        logger.info("starting preprocessed feature validation")
        remaining_features_with_one_hot = num_features
        pp_f_shape = truera_elements["preprocessed_features"].shape
        if not len(feature_names) == pp_f_shape[feature_dimension]:
            raise WrapperOutputValidationException(
                f"Number of features in DataWrapper.get_features should match the third dimension in ModelRunWrapper.ds_elements_to_truera_elements[\"preprocessed_features\"]. Number of features in get_features is {len(feature_names)}, and third dimension of ds_elements_to_truera_elements[\"preprocessed_features\"] is {pp_f_shape[feature_dimension]}, with total shape {str(pp_f_shape)}."
            )

        remaining_features = len(feature_names)
        for oh_feature in one_hot_sizes:
            if (oh_feature in feature_names):
                remaining_features_with_one_hot -= one_hot_sizes[oh_feature]
                remaining_features -= 1
        remaining_features_without_one_hot = remaining_features_with_one_hot
        if not remaining_features == remaining_features_without_one_hot:
            raise WrapperOutputValidationException(
                f"ModelRunWrapper.ds_elements_to_truera_elements[\"features\"]\"s third dimension should add to all onehot sizes plus non onehot features. The shape of ds_elements_to_truera_elements[\"features\"] is {features_shape}, third dimension is {num_features}, and total features calculated is { num_features - remaining_features_with_one_hot + remaining_features}. debug info -- features:{str(feature_names)}\n\nModelRunWrapper.get_one_hot_sizes:{str(one_hot_sizes)}"
            )
        print("Passed! DataWrapper.get_one_hot_sizes")
    else:
        if not len(feature_names) == num_features:
            raise WrapperOutputValidationException(
                f"Number of features in DataWrapper.get_features should match the third dimension in ModelRunWrapper.ds_elements_to_truera_elements[\"features\"]. Number of features in get_features is {len(feature_names)}, and third dimension of ds_elements_to_truera_elements[\"features\"] is {num_features}, with total shape {features_shape}."
            )

        if not len(one_hot_sizes) == 0:
            raise WrapperOutputValidationException(
                f"ModelRunWrapper.get_one_hot_sizes cannot be 0. If there are no one hot encodings, return None. got {str(one_hot_sizes)}"
            )

    print("Passed! feature name and size validation.")
    return feature_names


def assert_get_short_feature_descriptions(
    feature_names, data_wrapper, split_path, logger
):
    if isinstance(
        data_wrapper.get_short_feature_descriptions, types.FunctionType
    ):
        short_feature_descriptions = data_wrapper.get_short_feature_descriptions(
            split_path
        )
    else:
        short_feature_descriptions = data_wrapper.get_short_feature_descriptions(
        )
    if not isinstance(short_feature_descriptions, dict):
        raise WrapperOutputValidationException(
            "DataWrapper.get_short_feature_descriptions should be of type \"dict\". Got %s"
            % str(type(short_feature_descriptions))
        )

    if not set(feature_names) == short_feature_descriptions.keys():
        raise WrapperOutputValidationException(
            "DataWrapper.get_short_feature_descriptions keys must match DataWrapper.get_features. features:%s\n\ndescription keys:%s"
            % (str(feature_names), str(short_feature_descriptions.keys()))
        )

    for feature in feature_names:
        if not isinstance(feature, str):
            raise WrapperOutputValidationException(
                "DataWrapper.get_features contents should be of type \"str\". Got %s:%s"
                % (str(type(feature)), str(feature))
            )

    print("Passed! DataWrapper.get_short_feature_descriptions")


def assert_get_missing_values(feature_names, data_wrapper, split_path, logger):
    if isinstance(data_wrapper.get_missing_values, types.FunctionType):
        missing_vals = data_wrapper.get_missing_values(split_path)
    else:
        missing_vals = data_wrapper.get_missing_values()
    if not (
        missing_vals is None or isinstance(missing_vals, dict) or
        isinstance(missing_vals, list)
    ):
        raise WrapperOutputValidationException(
            "DataWrapper.missing_vals needs to return dict, list, or None"
        )
    if missing_vals is None:
        print("Passed! DataWrapper.missing_vals is not implemented")
    else:
        if not len(missing_vals) > 0:
            raise WrapperOutputValidationException(
                "DataWrapper.missing_vals cannot be empty. If there are no missing values, return None."
            )

    def _verify_missing_vals_subset(names):
        if not set(names).issubset(set(feature_names)):
            raise WrapperOutputValidationException(
                "DataWrapper.missing_vals must be a subset of the features: %s"
                % str(feature_names)
            )

    if isinstance(missing_vals, dict):
        _verify_missing_vals_subset(missing_vals.keys())
        print("Passed! DataWrapper.missing_vals is a dictionary of values")
    elif isinstance(missing_vals, list):
        _verify_missing_vals_subset(missing_vals)
        print("Passed! DataWrapper.missing_vals is a list of values")


def assert_evaluate_model(
    *,
    model_input_type: str,
    ds_batch: Any,
    truera_elements: Dict[str, Any],
    attr_config: AttributionConfiguration,
    model: WrapperNNBackend.Model,
    model_run_wrapper: Base.ModelRunWrapper,
    model_load_wrapper: Optional[Base.ModelLoadWrapper] = None,
    logger: Optional[Logger] = None
) -> None:
    """Checks that the ModelRunWrapper evaluate_model method is correctly formed

    Args:
        model_input_type (str): The type of input. Currently allows 'time_series_tabular' and 'text'.
        ds_batch (Any): Batchable components coming from the SplitLoadWrapper get_ds method.
        truera_elements (Dict[str, Any]): A Dictionary of truera elements coming from the ModelRunWrapper get_truera_elements method.
        model (WrapperNNBackend.Model): The model object
        model_run_wrapper (Base.ModelRunWrapper): The ModelRunWrapper implementation
        model_load_wrapper (Base.ModelLoadWrapper): The ModelLoadWrapper implementation
        attr_config (AttributionConfiguration): A run configuration.
        logger (Logger): the logger

    Raises:
        WrapperOutputValidationException: An exception raised if the method is incorrectly defined.

    """
    # TODO: need update return type expectation
    args, kwargs = model_run_wrapper.inputbatch_of_databatch(ds_batch, model)
    if not isinstance(args, list):
        raise WrapperOutputValidationException(
            f"ModelRunWrapper.model_input_args_kwargs first item should return a \"list\". got {str(type(args))}"
        )

    if not isinstance(kwargs, dict):
        raise WrapperOutputValidationException(
            f"ModelRunWrapper.model_input_args_kwargs second item should return a \"dict\". got {str(type(kwargs))}"
        )
    output = model_run_wrapper.evaluate_model(model, args, kwargs)
    param_validation = VerifyHelper._get_naming_params_by_input_output_types(
        attr_config, model_input_type, model_run_wrapper
    )
    if not output.shape[0] == len(truera_elements["ids"]):
        raise WrapperOutputValidationException(
            f"ModelRunWrapper.evaluate_model batch size should match ModelRunWrapper.ds_elements_to_truera_elements[\"ids\"] batch size. Evaluate batch size is {output.shape[0]}, from shape {str(output.shape)}. \"ids\" batch size is {len(truera_elements['ids'])}"
        )
    print("Passed! ids check input and output batch sizes match")

    if param_validation.seq_2_seq:
        if not output.shape[1] == attr_config.n_time_step_output:
            raise WrapperOutputValidationException(
                f"The second dimension in ModelRunWrapper.evaluate_model should be the specified n_time_step_output size. The dimension found is {output.shape[1]} in shape {str(output.shape)}. The n_time_step_output specified in the projects is {attr_config.n_time_step_output}."
            )
        print("Passed! check output timestep sizes match")
        class_dimension_idx = 2
    else:
        class_dimension_idx = 1

    if not output.shape[class_dimension_idx] == attr_config.n_output_neurons:
        raise WrapperOutputValidationException(
            f"The dimension index of {class_dimension_idx} in ModelRunWrapper.evaluate_model should be the specified num classes. The dimension found is {output.shape[class_dimension_idx]} in shape {str(output.shape)}. The num classes specified in the projects is {attr_config.n_output_neurons}."
        )

    print("Passed! check output num classes match")
    print(
        "Passed! model_run_wrapper.model_input_args_kwargs and model_run_wrapper.evaluate_model"
    )
    return output


def assert_convert_model_eval_to_binary_classifier(
    ds_batch, model_eval_output, model_run_wrapper, logger, labels=False
):

    binary_output = model_run_wrapper.convert_model_eval_to_binary_classifier(
        ds_batch, model_eval_output, labels=labels
    )
    logger.info("check binary output shape is batch x 1")
    expected_binary_shape_1 = (model_eval_output.shape[0], 1)
    expected_binary_shape_2 = (model_eval_output.shape[0],)
    if not (
        binary_output.shape == expected_binary_shape_1 or
        binary_output.shape == expected_binary_shape_2
    ):
        raise WrapperOutputValidationException(
            "ModelRunWrapper.convert_model_eval_to_binary_classifier should have batch size matching ModelRunWrapper.evaluate_model, each with one value. expected size %s or %s, but got %s."
            % (
                expected_binary_shape_1, expected_binary_shape_2,
                binary_output.shape
            )
        )

    if max(binary_output) > 1 or min(binary_output) < 0:
        raise WrapperOutputValidationException(
            "The values of ModelRunWrapper.convert_model_eval_to_binary_classifier should be between 0 and 1. min found: %d, max found %d. labels param is %s"
            % (min(binary_output), max(binary_output), str(labels))
        )

    print("Passed! model_run_wrapper.convert_model_eval_to_binary_classifier")


def verify_wrapper_types(
    *,
    project_input_type: str,
    attr_config: AttributionConfiguration,
    model_run_wrapper: Base.ModelRunWrapper,
    split_load_wrapper: Base.SplitLoadWrapper,
    model_load_wrapper: Optional[Base.ModelLoadWrapper] = None
) -> None:
    """Verifies that this method's parameters and types are all consistent with the project_input_type

    Args:
        project_input_type (str): The type of input. Currently allows 'time_series_tabular' and 'text'.
        attr_config (AttributionConfiguration): A run configuration that will be RNNAttributionConfiguration or NLPAttributionConfiguration
        model_run_wrapper (Base.ModelRunWrapper): The ModelRunWrapper where the parent Base class should match the project_input_type.
        split_load_wrapper (Base.SplitLoadWrapper): The SplitLoadWrapper where the parent Base class should match the project_input_type.
        model_load_wrapper (Optional[Base.ModelLoadWrapper], optional): The SplitLoadWrapper where the parent Base class should match the project_input_type.
    """
    if project_input_type == 'text':
        verify_helper = NLPVerifyHelper
    if project_input_type == 'time_series_tabular':
        verify_helper = TimeseriesVerifyHelper
    verify_helper.verify_wrapper_types(
        attr_config=attr_config,
        model_run_wrapper=model_run_wrapper,
        split_load_wrapper=split_load_wrapper,
        model_load_wrapper=model_load_wrapper
    )


def verify_attr_config(attr_config, config_path, logger):
    logger.info("Start validate config keys for '{}'".format(config_path))

    assert_arg_val("input_layer", attr_config.input_layer, (str, Layer))
    assert_arg_val("input_anchor", attr_config.input_anchor, (str, LayerAnchor))
    if not attr_config.input_anchor in [
        "in", "out", LayerAnchor.IN, LayerAnchor.OUT
    ]:
        raise ArgValidationException(
            "input_anchor must be either \"in\" or \"out\". Got %s" %
            str(attr_config.input_anchor)
        )

    assert_arg_val("output_layer", attr_config.output_layer, (str, Layer))
    assert_arg_val(
        "output_anchor", attr_config.output_anchor, (str, LayerAnchor)
    )
    if not attr_config.output_anchor in [
        "in", "out", LayerAnchor.IN, LayerAnchor.OUT
    ]:
        raise ArgValidationException(
            "output_anchor must be either \"in\" or \"out\". Got %s" %
            str(attr_config.output_anchor)
        )
    verify_helper = VerifyHelper.get_helper_from_attr_config(attr_config)
    verify_helper.verify_attr_config(attr_config)

    assert_arg_val("n_output_neurons", attr_config.n_output_neurons, int)
    print("Passed! Validate config keys for '{}'".format(config_path))


def verify_model(
    model_load_wrapper, attr_config, config_path, model_path, logger
):
    verify_attr_config(attr_config, config_path, logger)
    if isinstance(model_load_wrapper.get_model, types.FunctionType):
        model = model_load_wrapper.get_model(model_path)
    else:
        model = model_load_wrapper.get_model()
    return model, model_load_wrapper


def verify_split(
    split_path: Path,
    data_wrapper: Base.SplitLoadWrapper,
    tokenizer_wrapper: Optional[NLP.TokenizerWrapper] = None,
    logger: Optional[Logger] = None
) -> None:
    """Verifies all the SplitLoadWrapper methods are well formed.

    Args:
        split_path (Path): The path to split files.
        data_wrapper (Base.SplitLoadWrapper): The SplitLoadWrapper implementation.
        tokenizer_wrapper (Optional[NLP.TokenizerWrapper], optional): If the input_type is 'text'. Check the TokenizerWrapper.
        logger (Logger, optional): The Logger.
    """
    if isinstance(data_wrapper.get_ds, types.FunctionType):
        # This is for legacy support on ingestion_wrappers.py
        dataset = data_wrapper.get_ds(split_path)
    else:
        if isinstance(data_wrapper, Timeseries.SplitLoadWrapper):
            dataset = data_wrapper.get_ds()
        elif isinstance(data_wrapper, NLP.SplitLoadWrapper):
            dataset = data_wrapper.get_ds(tokenizer_wrapper)
    is_iterable = hasattr(dataset,
                          "__getitem__") or hasattr(dataset, "__iter__")
    if not is_iterable:
        raise WrapperOutputValidationException(
            "DataLoadWrapper.get_ds did not return an iterable object."
        )
    print("Passed! DataLoadWrapper.get_ds")

    dataset_single_batch = None
    if hasattr(dataset, "__getitem__"):
        dataset_single_batch = dataset[0]  # get item directly
    else:
        for d in dataset:
            dataset_single_batch = d
            break
    feature_names = None
    if isinstance(data_wrapper, Timeseries.SplitLoadWrapper):
        feature_names = assert_get_feature_names(
            data_wrapper, split_path, logger
        )
        assert_get_short_feature_descriptions(
            feature_names, data_wrapper, split_path, logger
        )
        assert_get_missing_values(
            feature_names, data_wrapper, split_path, logger
        )
    return dataset_single_batch, data_wrapper, feature_names


def verify_data(
    *,
    model_input_type: str,
    model_output_type: str,
    split_path: str,
    model: WrapperNNBackend.Model,
    data_wrapper: Base.SplitLoadWrapper,
    model_run_wrapper: Base.ModelRunWrapper,
    model_load_wrapper: Optional[Base.ModelLoadWrapper] = None,
    tokenizer_wrapper: Optional[NLP.TokenizerWrapper] = None,
    attr_config: AttributionConfiguration,
    logger: Optional[Logger] = None
) -> None:
    """Verifies that the data coming from the get_truera_elements is consistent with all data inputs.

    Args:
        model_input_type (str): The type of input. Currently allows 'time_series_tabular' and 'text'.
        model_output_type (str): The type of output. Currently allows 'classification' and 'regression'.
        split_path (str): The path to split files.
        data_wrapper (Base.SplitLoadWrapper): The SplitLoadWrapper implementation
        model (WrapperNNBackend.Model): The model object.
        model_run_wrapper (Base.ModelRunWrapper): The ModelRunWrapper implementation
        model_load_wrapper (Base.ModelLoadWrapper): The ModelLoadWrapper implementation
        attr_config (AttributionConfiguration): A run configuration that will be RNNAttributionConfiguration or NLPAttributionConfiguration
        logger (Logger): The Logger.

    Raises:
        WrapperOutputValidationException: _description_

    Returns:
        _type_: _description_
    """
    verify_helper = VerifyHelper.get_helper_from_attr_config(attr_config)

    dataset_single_batch, data_wrapper, feature_names = verify_split(
        split_path, data_wrapper, logger=logger
    )

    dataset_single_batch_dup, _, _ = verify_split(
        split_path, data_wrapper, logger=logger
    )

    truera_elements = verify_helper.assert_ds_elements_to_truera_elements(
        ds_batch=dataset_single_batch,
        model=model,
        model_input_type=model_input_type,
        model_output_type=model_output_type,
        feature_names=feature_names,
        model_run_wrapper=model_run_wrapper,
        tokenizer_wrapper=tokenizer_wrapper,
        attr_config=attr_config,
        logger=logger
    )
    truera_elements_dup = verify_helper.assert_ds_elements_to_truera_elements(
        dataset_single_batch_dup,
        model=model,
        model_input_type=model_input_type,
        model_output_type=model_output_type,
        feature_names=feature_names,
        model_run_wrapper=model_run_wrapper,
        tokenizer_wrapper=tokenizer_wrapper,
        attr_config=attr_config,
        logger=logger
    )
    for i in range(len(truera_elements["ids"])):
        if not (truera_elements["ids"][i] == truera_elements_dup["ids"][i]):
            raise WrapperOutputValidationException(
                "Dataset loads a different set of records on each load."
            )
    print("Passed! Dataset returns same ordering on each run")
    return dataset_single_batch, truera_elements


def verify_tokenizer(
    text_ds: Sequence[str], tokenizer_wrapper: NLP.TokenizerWrapper
):
    tokenization: NLP.TruTokenization[
        NLP.Token] = tokenizer_wrapper.tokenize_into_tru_tokens(texts=text_ds)
    if not isinstance(tokenization, NLP.TruTokenization):
        raise WrapperOutputValidationException(
            f"wrapper method TokenizerWrapper.tokenize_into_tru_tokens() does not return valid NLP.TruTokenization with fields {fields(NLP.TruTokenization)}."
        )

    print(
        "Passed! Tokenizer.tokenize_into_tru_tokens returns proper data structure"
    )


def verify_model_eval(
    dataset_single_batch: Any,
    *,
    model_input_type: str,
    truera_elements: Dict[str, Any],
    model: WrapperNNBackend.Model,
    attr_config: AttributionConfiguration,
    model_run_wrapper: Base.ModelRunWrapper,
    model_load_wrapper: Optional[Base.ModelLoadWrapper] = None,
    logger: Optional[Logger] = None
) -> None:
    """Verifies the ModelRunWrapper evaluate_model method is well formed.

    Args:
        dataset_single_batch (Any): A batchable input coming from SplitLoadWrapper get_ds method.
        model_input_type (str): The type of input. Currently allows 'time_series_tabular' and 'text'.
        truera_elements (Dict[str, Any]): A Dictionary of truera elements coming from the ModelRunWrapper get_truera_elements method.
        model (WrapperNNBackend.Model): The model object.
        model_run_wrapper (Base.ModelRunWrapper): The ModelRunWrapper implementation.
        model_load_wrapper (Base.ModelLoadWrapper): The ModelLoadWrapper implementation.
        attr_config (AttributionConfiguration): A run configuration that will be RNNAttributionConfiguration or NLPAttributionConfiguration
        logger (Logger): The Logger.

    Raises:
        NotImplementedError: _description_
    """
    verify_helper = VerifyHelper.get_helper_from_attr_config(attr_config)
    verify_helper.assert_input_sizes(
        model_input_type,
        truera_elements,
        attr_config=attr_config,
        model_run_wrapper=model_run_wrapper,
        input_dimension_order=attr_config.input_dimension_order,
        logger=logger,
    )
    model_eval_output = assert_evaluate_model(
        model_input_type=model_input_type,
        ds_batch=dataset_single_batch,
        truera_elements=truera_elements,
        model=model,
        model_run_wrapper=model_run_wrapper,
        model_load_wrapper=model_load_wrapper,
        attr_config=attr_config,
        logger=logger
    )

    try:
        if not isinstance(
            model_run_wrapper, Timeseries.ModelRunWrapper.WithBinaryClassifier
        ):
            raise NotImplementedError

        assert_convert_model_eval_to_binary_classifier(
            dataset_single_batch,
            model_eval_output,
            model_run_wrapper,
            logger,
            labels=False
        )
        assert_convert_model_eval_to_binary_classifier(
            dataset_single_batch,
            truera_elements["labels"],
            model_run_wrapper,
            logger,
            labels=True
        )
    except NotImplementedError:
        logger.warning(
            "ModelRunWrapper does not implement WithBinaryClassifier. Confusion Matrix sampling feature will not be available."
        )


def verify_run(
    *,
    model_input_type: str,
    model_output_type: str,
    split_path: str,
    split_wrapper: Base.SplitLoadWrapper,
    model: WrapperNNBackend.Model,
    model_run_wrapper: Base.ModelRunWrapper,
    model_load_wrapper: Optional[Base.ModelLoadWrapper] = None,
    tokenizer_wrapper: Optional[NLP.TokenizerWrapper] = None,
    attr_config: Optional[AttributionConfiguration] = None,
    logger: Optional[Logger] = None
):
    """Verifies that all components needed for running attributions is well defined.

    Args:
        model_input_type (str): The type of input. Currently allows 'time_series_tabular' and 'text'.
        model_output_type (str): The type of output. Currently allows 'classification' and 'regression'.
        split_path (str): The path to split files.
        split_wrapper (Base.SplitLoadWrapper): The SplitLoadWrapper implementation.
        model (WrapperNNBackend.Model): The model object.
        model_run_wrapper (Base.ModelRunWrapper): The ModelRunWrapper implementation
        model_load_wrapper (Base.ModelLoadWrapper): The ModelLoadWrapper implementation.
        tokenizer_wrapper (Optional[NLP.TokenizerWrapper], optional): The TokenizerWrapper implementation. Only needed when input_type is 'text'.
        attr_config (AttributionConfiguration): A run configuration that will be RNNAttributionConfiguration or NLPAttributionConfiguration
        logger (Logger): The Logger.
    """
    # Check Data loading

    dataset_single_batch, truera_elements = verify_data(
        model_input_type=model_input_type,
        model_output_type=model_output_type,
        split_path=split_path,
        data_wrapper=split_wrapper,
        model=model,
        model_run_wrapper=model_run_wrapper,
        model_load_wrapper=model_load_wrapper,
        attr_config=attr_config,
        logger=logger,
        tokenizer_wrapper=tokenizer_wrapper
    )

    # Check Model running on Data
    verify_model_eval(
        dataset_single_batch=dataset_single_batch,
        model_input_type=model_input_type,
        truera_elements=truera_elements,
        model=model,
        model_run_wrapper=model_run_wrapper,
        model_load_wrapper=model_load_wrapper,
        attr_config=attr_config,
        logger=logger
    )
    if tokenizer_wrapper:
        assert isinstance(
            split_wrapper, NLP.SplitLoadWrapper
        ), f"Expected split_wrapper to be of type NLP.SplitLoadWrapper. Got {type(split_wrapper)}"
        verify_tokenizer(
            # TODO: get_text_ds not longer provided
            text_ds=split_wrapper.get_text_ds(),
            tokenizer_wrapper=tokenizer_wrapper
        )


def get_logger(set_level):
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(name="verify-nn-ingestion")
    if set_level == "silent":
        logger.setLevel("ERROR")
    elif set_level == "default":
        logger.setLevel("INFO")
    elif set_level == "verbose":
        logger.setLevel("DEBUG")
    else:
        logger.setLevel("INFO")
    return logger


def get_parser():
    """Get parser object. These items are specified in the command line"""
    from argparse import ArgumentDefaultsHelpFormatter
    from argparse import ArgumentParser
    parser = ArgumentParser(
        description=__doc__, formatter_class=ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "--model_dir",
        dest="model_dir",
        help="The path to the model directory",
        required=True
    )
    parser.add_argument(
        "--data_dir",
        dest="data_dir",
        help="The path to the split directory",
        required=True
    )
    parser.add_argument(
        "--log_level",
        dest="log_level",
        help="Options: silent, default, verbose.",
        required=False
    )

    return parser


class VerifyHelper(ABC):

    @dataclass(eq=True)
    class ParamValidationContainer:
        input_seq_dimension: Dimension
        input_data_dimension: Dimension
        config_input_seq_param: int
        config_input_data_param: int
        config_input_seq_param_str: str
        config_input_data_param_str: str
        input_dimension_order_str: str
        output_dimension_order_str: str
        expected_labels_shape: int
        input_data_key: str
        seq_2_seq: bool

    @staticmethod
    def _get_naming_params_by_input_output_types(
        attr_config: AttributionConfiguration,
        model_input_type: str,
        model_run_wrapper: Optional[Base.ModelRunWrapper] = None
    ) -> ParamValidationContainer:
        """Returns an object container that contains many commonly referenced parameters.

        Args:
            attr_config (AttributionConfiguration): The run configuration.
            model_input_type (str): The type of input. Currently allows 'time_series_tabular' and 'text'.
            model_load_wrapper (Base.ModelLoadWrapper): The ModelLoadWrapper implementation.
        Returns:
            ParamValidationContainer: an object container that contains many commonly referenced parameters.
        """
        if model_input_type == "text":
            input_seq_dimension = Dimension.POSITION
            input_data_dimension = Dimension.EMBEDDING
            config_input_seq_param = model_run_wrapper.n_tokens
            config_input_data_param = model_run_wrapper.n_embeddings
            config_input_seq_param_str = "n_tokens"
            config_input_data_param_str = "n_embeddings"

            input_data_key = "token_ids"
            seq_2_seq = False
            input_dimension_order_str = f"(batch x {config_input_seq_param_str})"

        elif model_input_type == "time_series_tabular":
            input_seq_dimension = Dimension.TIMESTEP
            input_data_dimension = Dimension.FEATURE
            config_input_seq_param = attr_config.n_time_step_input
            config_input_data_param = attr_config.n_features_input
            config_input_seq_param_str = "n_time_step_input"
            config_input_data_param_str = "n_features_input"

            input_data_key = "features"
            seq_2_seq = True
            input_dimension_order_str = f"(batch x {config_input_seq_param_str} x {config_input_data_param_str})"
        if seq_2_seq:
            output_dimension_order_str = "(batchsize x num_timesteps x num_classes)"
            expected_labels_shape = 3
        else:
            output_dimension_order_str = "(batchsize,)"
            expected_labels_shape = 1
        return VerifyHelper.ParamValidationContainer(
            input_seq_dimension=input_seq_dimension,
            input_data_dimension=input_data_dimension,
            config_input_seq_param=config_input_seq_param,
            config_input_data_param=config_input_data_param,
            config_input_seq_param_str=config_input_seq_param_str,
            config_input_data_param_str=config_input_data_param_str,
            input_dimension_order_str=input_dimension_order_str,
            output_dimension_order_str=output_dimension_order_str,
            expected_labels_shape=expected_labels_shape,
            input_data_key=input_data_key,
            seq_2_seq=seq_2_seq
        )

    @staticmethod
    def _verify_wrapper_types(
        *,
        attr_config: AttributionConfiguration,
        model_run_wrapper: Base.ModelRunWrapper,
        split_load_wrapper: Base.SplitLoadWrapper,
        model_load_wrapper: Optional[Base.ModelLoadWrapper] = None,
        attr_config_type: Any = None,
        model_run_wrapper_type: Any = None,
        split_load_wrapper_type: Any = None,
        model_load_wrapper_type: Any = None
    ) -> None:
        """A common method among validation types to check parameter types.

        Args:
            attr_config (AttributionConfiguration): The run configuration.
            model_run_wrapper (Base.ModelRunWrapper): The ModelRunWrapper implementation.
            split_load_wrapper (Base.SplitLoadWrapper): The SplitLoadWrapper implementation.
            model_load_wrapper (Optional[Base.ModelLoadWrapper], optional): The ModelLoadWrapper implementation.
            attr_config_type (Any, optional): _description_. The attr_config (AttributionConfiguration) type based on the input type.
            model_run_wrapper_type (Any, optional): The model_run_wrapper (Parent.ModelRunWrapper) type and parent type based on the input type.
            split_load_wrapper_type (Any, optional): The split_load_wrapper (Parent.SplitLoadWrapper) type and parent type based on the input type.
            model_load_wrapper_type (Any, optional): The model_load_wrapper (Parent.ModelLoadWrapper) type and parent type based on the input type.
        """
        assert_arg_val(
            "attr_config", attr_config, attr_config_type, source='user method'
        )
        assert_arg_val(
            "model_run_wrapper", model_run_wrapper, model_run_wrapper_type
        )
        assert_arg_val(
            "split_load_wrapper", split_load_wrapper, split_load_wrapper_type
        )
        if model_load_wrapper is not None:
            assert_arg_val(
                "model_load_wrapper", model_load_wrapper,
                model_load_wrapper_type
            )

    @staticmethod
    def _assert_ds_elements_to_truera_elements(
        *,
        model_input_type: str,
        model_output_type: str,
        truera_elements: Dict[str, Any],
        truera_keys: Sequence[str],
        attr_config: Optional[AttributionConfiguration] = None,
        model_run_wrapper: Optional[Base.ModelRunWrapper] = None,
        logger: Optional[Logger] = None
    ) -> None:
        """A common method among validation types to check truera_elements.

        Args:
            model_input_type (str): The type of input. Currently allows 'time_series_tabular' and 'text'.
            model_output_type (str): The type of output. Currently allows 'classification' and 'regression'.
            truera_elements (Dict[str, Any]): A dictionary of customer to TruEra mapping data.
            truera_keys (Sequence[str]): The truera_elements expected keyset.
            attr_config (AttributionConfiguration): A run configuration that will be RNNAttributionConfiguration or NLPAttributionConfiguration
            model_run_wrapper (Base.ModelRunWrapper): The ModelRunWrapper implementation.
            logger (Logger): The Logger.
        """
        if not truera_keys.issubset(truera_elements.keys()):
            raise WrapperOutputValidationException(
                f"wrapper method ModelRunWrapper.ds_elements_to_truera_elements keys must contain all of {str(truera_keys)}. Got {str(truera_elements.keys())}"
            )

        batch_size = len(truera_elements["ids"])
        for key in truera_keys:
            if not isinstance(truera_elements[key], np.ndarray):
                raise WrapperOutputValidationException(
                    f"wrapper method ModelRunWrapper.ds_elements_to_truera_elements values should be of type np.ndarray. Instead got {type(truera_elements[key])} for key: '{key}'"
                )
            if not len(truera_elements[key]) == batch_size:
                raise WrapperOutputValidationException(
                    f"wrapper method ModelRunWrapper.ds_elements_to_truera_elements values must match the batch size of \"ids\". "
                    +
                    f"\"ids\" batch size is {batch_size}. \"{key}\" batch size is {len(truera_elements[key])}"
                )

        labels_shape = truera_elements["labels"].shape

        param_validation = VerifyHelper._get_naming_params_by_input_output_types(
            attr_config, model_input_type, model_run_wrapper
        )
        if not len(labels_shape) == param_validation.expected_labels_shape:
            raise WrapperOutputValidationException(
                f"wrapper method ds_elements_to_truera_elements[\"labels\"] must have shape of dimension {param_validation.expected_labels_shape} to denote "
                +
                f"{param_validation.output_dimension_order_str}. Found {len(labels_shape)} dimensions with shape {str(labels_shape)}"
            )
        if model_output_type == "classification":
            assert np.issubdtype(truera_elements["labels"].dtype, np.integer)
        else:
            assert np.issubdtype(truera_elements["labels"].dtype, np.float)
        _assert_truera_elements_shape(
            truera_elements, "ids", (batch_size,), "(batch_size,)", logger
        )

    @staticmethod
    def _assert_input_sizes(
        *,
        model_input_type: str,
        truera_elements: Dict[str, Any],
        attr_config: AttributionConfiguration,
        input_dimension_order: Sequence[Dimension] = None,
        model_run_wrapper: Optional[Base.ModelRunWrapper] = None,
        logger: Optional[Logger] = None,
    ) -> None:
        """A common method among validation types to check input data shapes.

        Args:
            model_input_type (str): The type of input. Currently allows 'time_series_tabular' and 'text'.
            truera_elements (Dict[str, Any]): A dictionary of customer to TruEra mapping data.
            attr_config (AttributionConfiguration): A run configuration that will be RNNAttributionConfiguration or NLPAttributionConfiguration
            input_dimension_order (Sequence[Dimension], optional): The expected input dimension order.
            model_load_wrapper (Base.ModelLoadWrapper): The ModelLoadWrapper implementation.
            logger (Logger): The Logger.

        """
        param_validation = VerifyHelper._get_naming_params_by_input_output_types(
            attr_config, model_input_type, model_run_wrapper
        )
        features_shape = truera_elements[param_validation.input_data_key].shape

        if input_dimension_order is not None:
            logger.info(
                "Input dimensions have been customized because input_dimension_order is set."
            )
            n_seq_input_idx = input_dimension_order.index(
                param_validation.input_seq_dimension
            )
        else:
            logger.info(
                f"Input dimension defaults are {param_validation.input_dimension_order_str}. You can change this with the input_dimension_order in the AttributionConfiguration."
            )
            n_seq_input_idx = 1
        if not features_shape[n_seq_input_idx
                             ] == param_validation.config_input_seq_param:

            raise WrapperOutputValidationException(
                f"The dimension index {n_seq_input_idx} in ModelRunWrapper.ds_elements_to_truera_elements[\"{param_validation.input_data_key}\"] "
                +
                f"should be the specified {param_validation.input_seq_dimension.name.lower()} dimension size. The dimension found is {features_shape[1]} in shape {str(features_shape)}. "
                +
                f"The {param_validation.input_seq_dimension.name.lower()} dimension size specified in the projects is {param_validation.config_input_seq_param}."
            )

        print(
            f"Passed! input {param_validation.input_seq_dimension.name.lower()} dimension size matches model config"
        )

    @staticmethod
    @abstractmethod
    def verify_wrapper_types(
        attr_config: AttributionConfiguration,
        model_run_wrapper: Base.ModelRunWrapper,
        split_load_wrapper: Base.SplitLoadWrapper,
        model_load_wrapper: Optional[Base.ModelLoadWrapper] = None
    ) -> None:
        pass

    @staticmethod
    @abstractmethod
    def verify_attr_config(attr_config: AttributionConfiguration):
        pass

    @staticmethod
    @abstractmethod
    def assert_ds_elements_to_truera_elements(
        ds_batch: Any,
        model: WrapperNNBackend.Model,
        model_input_type: str,
        model_output_type: str,
        feature_names: Sequence[str],
        model_run_wrapper: Base.ModelRunWrapper,
        tokenizer_wrapper: Optional[NLP.TokenizerWrapper] = None,
        attr_config: AttributionConfiguration = None,
        logger: Logger = None
    ) -> None:
        pass

    @staticmethod
    @abstractmethod
    def assert_input_sizes(
        model_input_type: str,
        truera_elements: Dict[str, Any],
        attr_config: AttributionConfiguration,
        input_dimension_order: Sequence[Dimension] = None,
        logger: Logger = None
    ) -> None:
        pass

    @staticmethod
    def get_helper_from_attr_config(attr_config: AttributionConfiguration):
        """Returns an appropriate VerifyHelper implementation to help validate different modelling types.

        Args:
            attr_config (AttributionConfiguration): The run configuration. At this point it will be based on the input type.

        Returns:
            VerifyHelper: The specific input type VerifyHelper.
        """
        print(type(attr_config))
        if isinstance(attr_config, NLPAttributionConfiguration):
            return NLPVerifyHelper
        if isinstance(attr_config, RNNAttributionConfiguration):
            return TimeseriesVerifyHelper


class NLPVerifyHelper(VerifyHelper):

    @staticmethod
    def verify_wrapper_types(
        attr_config: NLPAttributionConfiguration,
        model_run_wrapper: NLP.ModelRunWrapper,
        split_load_wrapper: NLP.SplitLoadWrapper,
        model_load_wrapper: NLP.ModelLoadWrapper
    ) -> None:
        """The NLP Specific validation for verify_wrapper_types. See the VerifyHelper for more details.
        """
        VerifyHelper._verify_wrapper_types(
            attr_config=attr_config,
            model_run_wrapper=model_run_wrapper,
            split_load_wrapper=split_load_wrapper,
            model_load_wrapper=model_load_wrapper,
            attr_config_type=NLPAttributionConfiguration,
            model_run_wrapper_type=NLP.ModelRunWrapper,
            split_load_wrapper_type=NLP.SplitLoadWrapper,
            model_load_wrapper_type=NLP.ModelLoadWrapper
        )

    @staticmethod
    def verify_attr_config(attr_config: NLPAttributionConfiguration):
        """The NLP Specific validation for verify_attr_config. See the VerifyHelper for more details.
        """
        if attr_config.rebatch_size is not None:
            assert_arg_val("rebatch_size", attr_config.rebatch_size, int)
        if attr_config.ref_token is not None:
            assert_arg_val("ref_token", attr_config.ref_token, str)
        if attr_config.resolution is not None:
            assert_arg_val("resolution", attr_config.resolution, int)

    @staticmethod
    def assert_ds_elements_to_truera_elements(
        ds_batch: Any,
        model: WrapperNNBackend.Model,
        model_input_type: str,
        model_output_type: str,
        feature_names: Sequence[str],
        model_run_wrapper: Base.ModelRunWrapper,
        tokenizer_wrapper: Optional[NLP.TokenizerWrapper] = None,
        attr_config: AttributionConfiguration = None,
        logger: Logger = None
    ) -> None:
        """The NLP Specific validation for assert_ds_elements_to_truera_elements. See the VerifyHelper for more details.
        """
        truera_elements = model_run_wrapper.ds_elements_to_truera_elements(
            ds_batch, model, tokenizer_wrapper=tokenizer_wrapper
        )
        truera_keys = set(["ids", "token_ids", "attention_mask", "labels"])
        VerifyHelper._assert_ds_elements_to_truera_elements(
            model_input_type=model_input_type,
            model_output_type=model_output_type,
            truera_elements=truera_elements,
            truera_keys=truera_keys,
            attr_config=attr_config,
            model_run_wrapper=model_run_wrapper,
            logger=logger
        )
        _assert_attention_mask_truera_elements(truera_elements)
        print("Passed! ModelRunWrapper.assert_ds_elements_to_truera_elements")
        batch_size = len(truera_elements["ids"])
        param_validation = VerifyHelper._get_naming_params_by_input_output_types(
            attr_config, model_input_type, model_run_wrapper
        )
        _assert_truera_elements_shape(
            truera_elements,
            param_validation.input_data_key,
            (batch_size, param_validation.config_input_seq_param),
            param_validation.input_dimension_order_str,
            logger,
        )

        _assert_truera_elements_shape(
            truera_elements, "labels", (batch_size,), "(batch,)", logger
        )

        print("Passed! ModelRunWrapper.assert_ds_elements_to_truera_elements")
        return truera_elements

    @staticmethod
    def assert_input_sizes(
        model_input_type: str,
        truera_elements: Dict[str, Any],
        attr_config: AttributionConfiguration,
        model_run_wrapper: Base.ModelRunWrapper = None,
        input_dimension_order: Sequence[Dimension] = None,
        logger: Logger = None,
    ) -> None:
        """The NLP Specific validation for assert_input_sizes. See the VerifyHelper for more details.
        """
        VerifyHelper._assert_input_sizes(
            model_input_type=model_input_type,
            truera_elements=truera_elements,
            input_dimension_order=input_dimension_order,
            attr_config=attr_config,
            model_run_wrapper=model_run_wrapper,
            logger=logger
        )

        print("Passed! input features match model config")


class TimeseriesVerifyHelper(VerifyHelper):

    @staticmethod
    def verify_wrapper_types(
        attr_config: RNNAttributionConfiguration,
        model_run_wrapper: Timeseries.ModelRunWrapper,
        split_load_wrapper: Timeseries.SplitLoadWrapper,
        model_load_wrapper: Optional[Timeseries.ModelLoadWrapper] = None
    ) -> None:
        """The Timeseries Specific validation for verify_wrapper_types. See the VerifyHelper for more details.
        """
        VerifyHelper._verify_wrapper_types(
            attr_config=attr_config,
            model_run_wrapper=model_run_wrapper,
            split_load_wrapper=split_load_wrapper,
            model_load_wrapper=model_load_wrapper,
            attr_config_type=RNNAttributionConfiguration,
            model_run_wrapper_type=Timeseries.ModelRunWrapper,
            split_load_wrapper_type=Timeseries.SplitLoadWrapper,
            model_load_wrapper_type=Timeseries.ModelLoadWrapper
        )

    @staticmethod
    def verify_attr_config(attr_config: RNNAttributionConfiguration):
        """The Timeseries Specific validation for verify_attr_config. See the VerifyHelper for more details.
        """
        if attr_config.internal_layer is not None:
            assert_arg_val("internal_layer", attr_config.internal_layer, str)
            assert_arg_val(
                "internal_anchor", attr_config.internal_anchor,
                (str, LayerAnchor)
            )
            if not attr_config.internal_anchor in [
                "in", "out", LayerAnchor.IN, LayerAnchor.OUT
            ]:
                raise ArgValidationException(
                    "internal_anchor must be either \"in\" or \"out\". Got %s" %
                    str(attr_config.internal_anchor)
                )

            assert_arg_val(
                "n_internal_neurons", attr_config.n_internal_neurons, int
            )
            if not attr_config.n_internal_neurons > 2:
                raise ArgValidationException(
                    "n_internal_neurons must be greater than 2. Got %s" %
                    str(attr_config.n_internal_neurons)
                )

        assert_arg_val("n_time_step_input", attr_config.n_time_step_input, int)
        assert_arg_val(
            "n_time_step_output", attr_config.n_time_step_output, int
        )
        assert_arg_val("n_features_input", attr_config.n_features_input, int)

    @staticmethod
    def assert_ds_elements_to_truera_elements(
        ds_batch: Any,
        model: WrapperNNBackend.Model,
        model_input_type: str,
        model_output_type: str,
        feature_names: Sequence[str],
        model_run_wrapper: Base.ModelRunWrapper,
        tokenizer_wrapper: Optional[
            NLP.TokenizerWrapper
        ] = None,  # keep in TimeSeriesVerifyHelper to share standardized interface with NLP
        attr_config: AttributionConfiguration = None,
        logger: Logger = None
    ) -> None:
        """The Timeseries Specific validation for assert_ds_elements_to_truera_elements. See the VerifyHelper for more details.
        """
        truera_elements = model_run_wrapper.ds_elements_to_truera_elements(
            ds_batch, model
        )
        truera_keys = set(["ids", "features", "lengths", "labels"])
        VerifyHelper._assert_ds_elements_to_truera_elements(
            model_input_type=model_input_type,
            model_output_type=model_output_type,
            truera_elements=truera_elements,
            truera_keys=truera_keys,
            attr_config=attr_config,
            model_run_wrapper=model_run_wrapper,
            logger=logger
        )
        batch_size = len(truera_elements["ids"])

        _assert_lengths_truera_elements(
            attr_config.n_time_step_input, truera_elements, batch_size, logger
        )

        if isinstance(model_run_wrapper, Timeseries.ModelRunWrapper.WithOneHot):
            if not attr_config.input_dimension_order:
                assert_feature_names_match_sizes(
                    truera_elements, feature_names, model_run_wrapper, logger
                )
            else:
                assert_feature_names_match_sizes(
                    truera_elements,
                    feature_names,
                    model_run_wrapper,
                    logger,
                    feature_dimension=attr_config.input_dimension_order.index(
                        Dimension.FEATURE
                    )
                )
        param_validation = VerifyHelper._get_naming_params_by_input_output_types(
            attr_config, model_input_type, model_run_wrapper
        )
        if not attr_config.input_dimension_order:
            _assert_truera_elements_shape(
                truera_elements,
                param_validation.input_data_key, (
                    batch_size, param_validation.config_input_seq_param,
                    param_validation.config_input_data_param
                ),
                param_validation.input_dimension_order_str,
                logger,
                additional_logger_info=
                " Or you may need to supply 'input_dimension_order' in your AttributionConfig."
            )
        else:
            _assert_dimension_ordering(
                config_value=attr_config.input_dimension_order,
                truera_elements=truera_elements,
                truera_key=param_validation.input_data_key,
                expected_dimensions=[
                    Dimension.BATCH, param_validation.input_seq_dimension,
                    param_validation.input_data_dimension
                ],
                expected_dimensions_config_values=[
                    batch_size, param_validation.config_input_seq_param,
                    param_validation.config_input_data_param
                ],
                expected_dimensions_strs=[
                    "batch", param_validation.config_input_seq_param_str,
                    param_validation.config_input_data_param_str
                ],
                logger=logger
            )

        # Todo: generalize this if we ever get to nlp seq2seq
        if not attr_config.output_dimension_order:
            _assert_truera_elements_shape(
                truera_elements,
                "labels", (
                    batch_size, attr_config.n_time_step_output,
                    attr_config.n_output_neurons
                ),
                "batch x n_time_step_output x n_output_neurons",
                logger,
                additional_logger_info=
                " Or you may need to supply 'output_dimension_order' in your RNNAttributionConfig."
            )
        else:
            _assert_dimension_ordering(
                config_value=attr_config.output_dimension_order,
                truera_elements=truera_elements,
                truera_key="labels",
                expected_dimensions=[
                    Dimension.BATCH, Dimension.TIMESTEP, Dimension.CLASS
                ],
                expected_dimensions_config_values=[
                    batch_size, attr_config.n_time_step_output,
                    attr_config.n_output_neurons
                ],
                expected_dimensions_strs=[
                    "batch", "n_time_step_output", "n_output_neurons"
                ],
                logger=logger
            )

        if attr_config.input_dimension_order is not None:
            n_data_input_idx = attr_config.input_dimension_order.index(
                param_validation.input_data_dimension
            )
        else:
            n_data_input_idx = 2

        pp_features = truera_elements.get("preprocessed_features")
        features_shape = truera_elements[param_validation.input_data_key].shape
        if pp_features is not None:
            pp_features_shape = pp_features.shape
            if not pp_features_shape[
                n_data_input_idx] == param_validation.config_input_data_param:
                raise WrapperOutputValidationException(
                    f"The dimension index {n_data_input_idx} in ModelRunWrapper.ds_elements_to_truera_elements[\"preprocessed_features\"] should be the specified feature size. The dimension found is {pp_features_shape[n_data_input_idx]} in shape {str(pp_features_shape)}. The feature size specified in the projects is {param_validation.config_input_data_param}."
                )

        else:
            if not features_shape[n_data_input_idx
                                 ] == param_validation.config_input_data_param:
                raise WrapperOutputValidationException(
                    f"The dimension index {n_data_input_idx} in ModelRunWrapper.ds_elements_to_truera_elements[\"{param_validation.input_data_key}\"] should be the specified feature size. The dimension found is {features_shape[n_data_input_idx]} in shape {str(features_shape)}. The feature size specified in the projects is {param_validation.config_input_data_param}."
                )

        print("Passed! input features match model config")

        print("Passed! ModelRunWrapper.assert_ds_elements_to_truera_elements")
        return truera_elements

    @staticmethod
    def assert_input_sizes(
        model_input_type: str,
        truera_elements: Dict[str, Any],
        attr_config: AttributionConfiguration,
        model_run_wrapper: Optional[Base.ModelRunWrapper] = None,
        input_dimension_order: Sequence[Dimension] = None,
        logger: Logger = None,
    ) -> None:
        """The Timeseries Specific validation for assert_input_sizes. See the VerifyHelper for more details.
        """
        VerifyHelper._assert_input_sizes(
            model_input_type=model_input_type,
            truera_elements=truera_elements,
            input_dimension_order=input_dimension_order,
            attr_config=attr_config,
            logger=logger
        )

        print("Passed! input features match model config")
