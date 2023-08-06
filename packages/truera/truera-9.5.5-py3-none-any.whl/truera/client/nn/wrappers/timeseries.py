from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List, Union

import numpy as np

from truera.client.nn import NNBackend as B
from truera.client.nn.wrappers import Base
from truera.client.nn.wrappers import Wrapping


class Timeseries(Base):

    # Timeseries keys:
    #    - ids = array of size (batch x 1) : <ids to pair with records>
    #    - features = array of size (batch x features) : <feature values to which
    #      attributions explain>
    #    - lengths = array of size (batch x 1) : <number of timesteps associated
    #      with each record>
    #    - labels = array of size (batch x 1) : <label of each record>
    @dataclass
    class TruBatch:
        ids: np.ndarray  # of long
        features: np.ndarray  # of ???
        lengths: np.ndarray  # of long?
        labels: np.ndarray  # of ?

    # TODO: not currently used

    class ModelLoadWrapper(Base.ModelLoadWrapper):
        """A model load wrapper used for time series."""

    class SplitLoadWrapper(Base.SplitLoadWrapper):
        """A split load wrapper used for time series."""

        @Wrapping.required
        @abstractmethod
        def get_feature_names(self) -> List[str]:
            """
            This gets a list of feature names in the same index as the model
            inputs.

            Output
            ----------------
            - a list of feature names
            ----------------
            """
            ...

        @Wrapping.required
        @abstractmethod
        def get_short_feature_descriptions(self) -> Dict[str, str]:
            """
            This gets a dictionary of feature names to short feature
            descriptions

            Output
            ----------------
            - dictionary of feature names to short feature descriptions
            ----------------
            """
            ...

        @Wrapping.required
        @abstractmethod
        def get_missing_values(self) -> Union[Dict[str, List[Any]], List[str]]:
            """
            This returns either a dictionary of feature names to their
            respective missing feature vals, or it can return a list of features
            that have missing values. In this case, the explanations will
            naively assume the mode value is the missing value.
            
            Output
            ----------------
            - Mapping of features to missing values or list of features with
              missing values.
            ----------------
            """
            ...

    class ModelRunWrapper(Base.ModelRunWrapper):
        """
        A model run wrapper used for time series. Static methods only.

        - evaluate_model output shape should be (# in batch, # output timesteps,
          # classes).
        """

        @Wrapping.required
        @staticmethod
        @abstractmethod
        def ds_elements_to_truera_elements(
            ds_batch: Base.DataBatch, model: B.Model
        ) -> Timeseries.TruBatch:  # TODO: use hinted type
            """
            This transforms the dataset items into a form that the truera tool
            will use. The form should be a dictionary of `ids`, `features`,
            `lengths`, `labels` to the batched values Optional keys are
            `preprocessed_features`. If this is used, the wrapper method
            get_one_hot_sizes must be implemented.

            Example: - truera_elements = {} - truera_elements['ids'] = array of
            size (batch x 1) : <ids to pair with
              records>
            - truera_elements['features'] = array of size (batch x features) :
              <feature values to which attributions explain>
            - truera_elements['lengths'] = array of size (batch x 1) : <number
              of timesteps associated with each record>
            - truera_elements['labels'] = array of size (batch x 1) : <label of
              each record>

            - truera_elements['preprocessed_features']: Non mandatory. 
            Use this if preprocessing occurs like one hot
            encodings. If using this, truera_elements['features'] feature
            lengths should match the one hot encoding layer size
            truera_elements['preprocessed_features'] = array of size (batch x
            features) : <feature values of preprocessed features before
            encodings>
            
            Input
            ----------------
            - ds_batch: the output of a single iteration over the
              DataWrapper.get_ds object
            - model: the model object. This may be needed if the model does any
              preprocessing.
            ----------------
            Output
            ----------------
            - ds_batch transformed to be used by the Truera Platform. Features,
              lengths, and labels should by numpy ndarrays.
            ----------------
            """
            ...

        class WithOneHot(ABC):
            """
            Run wrapper requirements for models with one hot encodings.
            """

            @staticmethod
            @abstractmethod
            def get_one_hot_sizes() -> Dict[str, int]:
                """
                [Special Use Case, Optional] Only used if one hot encoding takes
                place within the model. The input layer should specify the layer
                containing the one hot encoded tensors. This method should then
                return a mapping of input feature to encoding size. This method
                assumes that the features layer is a single concatenated list of
                all encodings in order of the feature_names.
                """
                ...
