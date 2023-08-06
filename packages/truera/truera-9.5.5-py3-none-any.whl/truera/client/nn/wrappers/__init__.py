"""
Defines wrappers to help get information from a customer's code development to
Truera's system. Since NN development environments are so varied, we need to do
this to convert to some standards that Truera can guarantee. Wrappers are
designed with 2 paradigms.

1) Loading into memory '[X]LoadWrappers' - The most common things that we need
   loaded into memory for NN is the model and the dataset. This can be expanded
   to domain specifics. In local compute mode: we don't need the model load
   since it is already loaded. SplitLoadWrappers are still used because most NN
   datasets are backed by file storage.

  - ModelLoadWrapper - includes model and tokenizer loading

  - SplitLoadWrapper - data loading

   The pathways datasets take in the demo are as follows:

   a. Path -- SplitLoadWrapper.__init__ receives data_path from where it will
      load things.

   b. DataReader / Iterable[DataBatch] -- Users implement
      SplitLoadWrapper.get_ds which produces a DataReader by using
      data_path.

   c. (for model execution) Iterable[Inputs], Dict[str, Inputs] -- Users
      implement ModelRunWrapper.model_input_args_kwargs which takes in a
      DataBatch and produces arguments to send to a model.

   e. (for ui/display purposes) TruBatch -- Users implement
      ModelRunWrapper.ds_elements_to_truera_elements that converts DataBatch to
      TruBatch.

 2) Running the model and capturing important artifacts '[X]ModelRunWrappers' -
    These wrappers have methods defined that take the in-memory objects from the
    load wrappers (model and dataset), to transform into Truera system needs.
    The models are expected to be callable, and the datasets are expected to be
    iterable, with batched inputs alongside other arbitrary inputs.

  - ModelRunWrapper

Base wrappers should not depend on neural network backend (pytorch or
tensorflow). There are two classes here that are specific to each of these
backends and further refine the base classes with backend-specific requirements.

# Design Notes

Run wrappers contain only static methods. We did not want to impose requirements
that users store relevant data in wrappers. As a result of this, the wrapper
contain static methods that accept arbitrary inputs named "model" and/or
"tokenizer" which are the users' existing structures. We do not impose
requirements on these structures so the users can use whatever they already have
with zero changes to these hopefully. However, we require that in wrappers, the
users write methods for loading and saving models and tokenizers. The load
wrappers are not static; the SplitLoadWrapper is especially non-static as
different instantiations with different data paths are made during artifact
generation.

* TokenizerWrapper is presently an exception to the "static wrappers" only rule.

# "Initialize-time" checking

The wrappers here make heavy use of abstract methods which have the benefit of
throwing errors during class initialization if a required method is not provided
by the user. Some wrappers come with "optional" methods for some analyses. These
are put into sub-classes with (required) abstract methods. A user wishing to
perform those analyses needs to extend/mixin those classes to indicate so. The
abstract method system will then require they implement the required methods.
These are:

- Base.ModelRunWrapper.WithBinaryClassifier

- Timeseries.ModelRunWrapper.WithOneHot

- NLP.ModelRunWrapper.WithEmbeddings

- NLP.SplitLoadWrapper.WithSegmentByWord

See their docstrings for info about their means.

TODO: In the future we might redesign the wrapper/input structure so as to
require users store anything they need (model, tokenizer) in the wrapping class
itself which could then be provided as self to all of the presently static
methods that they need to implement.
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Dict, Iterable, List, TypeVar

import numpy as np
from tqdm.auto import tqdm

from truera.client.nn import Batch
from truera.client.nn import NNBackend as NNB
from truera.client.util.func_utils import Deprecate
from truera.client.util.func_utils import WrapperMeta
from truera.utils.file_utils import as_path

MODEL_RUN_WRAPPER_SAVE_NAME = 'truera_model_run_wrapper.pickle'
MODEL_LOAD_WRAPPER_SAVE_NAME = 'truera_model_load_wrapper.pickle'
SPLIT_LOAD_WRAPPER_SAVE_NAME = 'truera_split_load_wrapper.pickle'

# For generics and type hints.
T = TypeVar("T")

TruBatch = Dict[str, np.ndarray]


class Wrapping:
    # TODO: When decorating a method, include into its docstring what its type aliases alias to.

    @staticmethod
    def deprecates(oldfunc_name: str, dep_version: str, remove_version: str):
        # TODO: docstrings
        return WrapperMeta.deprecates(
            oldfunc_name=oldfunc_name,
            dep_version=dep_version,
            remove_version=remove_version
        )

    @staticmethod
    def require_init(func):
        func.__doc__ = "REQUIRED\n\nExtending classes need to define an __init__ method and call this initializer." + (
            func.__doc__ or ""
        )

        return WrapperMeta.require(func)

    @staticmethod
    def require_init_if_extended(func):
        func.__doc__ = "REQUIRED\n\nIf extending classes define an __init__ method, they need to call this initializer." + (
            func.__doc__ or ""
        )

        return WrapperMeta.require_if_extended(func)

    @staticmethod
    def required(func):
        """Decorator for required methods in wrappers."""

        func.__doc__ = "REQUIRED\n" + (func.__doc__ or "")
        return func

    @staticmethod
    def optional(func):
        """Decorator for optional methods in wrappers."""

        func.__doc__ = "OPTIONAL\n" + (func.__doc__ or "")
        return func

    @staticmethod
    def utility(obj):
        """Decorator for utility methods which should not be overriden in wrappers."""

        obj.__doc__ = "UTILITY; DO NOT OVERRIDE\n" + (obj.__doc__ or "")

        # Mark object protected.
        return WrapperMeta.protect(obj)

    @staticmethod
    def protected(obj):
        """Decorator for methods which should not be overriden in wrappers."""

        # Mark object protected.
        return WrapperMeta.protect(obj)


class DataBatch(Batch):
    """
    Client-specific, framework-specific data batch. Need to be able to produce
    InputBatch and TruBatch from this. One iteration from iter(DataReader).
    """
    pass


DataReader = Iterable[DataBatch]
# Client-specific, framework-specific data reader, produced by SplitLoadWrapper.get_ds
# pytorch: can use torch.utils.data.DataLoader
# tf2 ?
# tf1 ?


@dataclass
class InputBatch:  # TODO: use a generic Batch class
    args: List[NNB.Inputs]
    kwargs: Dict[str, NNB.Inputs]

    def __len__(self):
        return len(self.first())

    def for_batch(
        self, func: Callable[[InputBatch], None], batch_size: int, *args,
        **kwargs
    ) -> None:
        """
        Calls the given function with stored args but rebatched into the given
        batch_size. Ignores the result so should only be used with effectful
        functions. Rest of args are sent to tqdm when iterating.
        """

        assert len(self) > 0, "cannot call `func` on empty InputBatch"

        for batch in tqdm(self.rebatch(batch_size=batch_size), *args, **kwargs):
            func(batch)

    def map_batch(
        self, func: Callable[[InputBatch], T], batch_size: int, *args, **kwargs
    ) -> T:
        """
        Call the given function with stored args but rebatched into the given
        batch_size, outputs are collected and stacked. Rest of args are sent to
        tqdm when iterating.
        """

        assert len(self) > 0, "cannot call `func` on empty InputBatch"

        outputs = []

        for batch in tqdm(self.rebatch(batch_size=batch_size), *args, **kwargs):
            outputs.append(func(batch))

        # move this to some utility or backend module
        #if isinstance(outputs[0], torch.Tensor):
        #    return torch.cat(outputs, axis=0)
        if isinstance(outputs[0], np.ndarray):
            return np.concatenate(outputs, axis=0)
        elif isinstance(outputs[0], Batch):
            return Batch.collate(outputs)
        else:
            raise RuntimeError(
                f"do not know how to stack items of type {type(outputs[0])}"
            )

    def first(self) -> NNB.Inputs:
        if len(self.args) > 0:
            return self.args[0]
        if len(self.kwargs) > 0:
            return next(iter(self.kwargs.values()))
        else:
            raise ValueError("InputBatch has no args or kwargs")

    def rebatch(self, batch_size: int) -> Iterable[InputBatch]:
        """
        Batch this batch into (smaller) batches.
        """
        # Temporary poor-design. Need better handling of batching throughout entire pipeline.

        original_batch_size = len(
            self.first()
        )  # assume first dim is batch_size
        # TODO DIM_ORDER

        for i in range(0, original_batch_size, batch_size):
            args = [arg[i:i + batch_size] for arg in self.args]
            kwargs = {
                k: arg[i:i + batch_size] for k, arg in self.kwargs.items()
            }
            yield InputBatch(args=args, kwargs=kwargs)


@dataclass
class OutputBatch(DataBatch):
    logits: np.ndarray = Batch.field(factory=np.array)
    probits: np.ndarray = Batch.field(factory=np.array)


class Base:  # WANT: Generic in an implementation of NNBackend
    """
    Base requirements over all nn model / data types. Each project must provide
    the following wrappers:
    
        - `SplitLoadWrapper` - responsible for loading data splits `get_ds`,
          producing an iteration over `DataBatch` which itself is
          project-specific. The value `DataBatch` defined here is merely a type
          variable used to annotate methods with type hints.

        - `ModelLoadWrapper` - loads a model, producing `model`. This is, again,
          a project-specific type defined as a type variable here.

        - `ModelRunWrapper` - the meat of the wrappers:

          - model_input_args_kwargs - transforms `DataBatch` into `InputBatch`.
            `InputBatch` specifies the positional and keyword arguments with
            which a model is evaluated. The values of these arguments are
            project/framework-specific tensors.

          - evaluate_model - evaluates a model on a given `InputBatch`,
            producing `OutputBatch`. This is a framework-specific tensor whose
            first dimension is the batch index. Additional requirements on this
            tensor are specified under `Timeseries` and `NLP` wrapper variants.

          - ds_elements_to_truera_elements - transforms `DataBatch` into
            `TruBatch`, which is a collection of tensors required for operation
            of the Truera product. Each type of model imposes different
            requirements of what a `TruBatch` must contain.
    """

    class ModelRunWrapper(metaclass=WrapperMeta):
        """
        A wrapper to run nn models. The base class contains methods that will be
        needed for nn models of any type.
        
        * Static methods only. *
        """

        @Wrapping.deprecates(
            "model_input_args_kwargs",
            dep_version="0.0.1",
            remove_version="0.1.0"
        )
        @Wrapping.required
        @staticmethod
        @abstractmethod
        def inputbatch_of_databatch(
            databatch: DataBatch, model: NNB.Model
        ) -> InputBatch:
            """
            This method should convert what comes out of a dataset into model
            args and kwargs
            
            Input
            ----------------
            - ds_batch: the output of a single iteration over the
              DataLoadWrapper.get_ds object
            - model: client's model
            ----------------
            Output
            ----------------
            - InputBatch of args and kwargs to run the ModelLoadWrapper.get_model object
            ----------------
            """
            ...

        @Wrapping.required
        @staticmethod
        @abstractmethod
        def evaluate_model(model: NNB.Model, inputs: InputBatch) -> OutputBatch:
            """
            This method return a batched evaluation of the model.

            Input
            ----------------
            - model: user model
            - batch: InputBatch containing args and kwargs
            ----------------
            Output
            ----------------
            - a batched evaluation of the model.
            ----------------
            """
            ...

        class WithBinaryClassifier(ABC):
            """Models that can be converted to a binary classifier. This is
            required for certain error analyses."""

            # TODO: verify type hints
            @staticmethod
            @abstractmethod
            def convert_model_eval_to_binary_classifier(
                ds_batch: DataBatch,
                model_eval_output_or_labels: NNB.Outputs,
                labels: bool = False
            ) -> NNB.Outputs:
                """
                [Optional] Only used if post_model_filter_splits is used. See
                README on run_configuration.yml This method returns batched
                binary evaluations to help determine model performance. The
                value should be between 0 and 1, with 1 indicating a 'truth'
                value. This method is used to create post_model_filters This
                method already contains the model_eval_output_or_labels to save
                compute time If labels=True, the explainer will send the labels
                from ds_elements_to_truera_elements['labels'] into
                model_eval_output_or_labels

                Input
                ----------------
                - ds_batch: contains a batch of data from the dataset. This is
                  an iteration of SplitLoadWrapper.get_ds .
                - model_eval_output: the output of ModelWrapper.evaluate_model
                  this is precomputed to save time.
                - labels: boolean indicating whether model output is being
                  converted to binary preds, or if labels are being passed in
                ----------------
                Output
                ----------------
                - predictions - batched binary predictions or labels - batched
                  binary labels
                ----------------
                """
                ...

    class ModelLoadWrapper(metaclass=WrapperMeta):
        """A wrapper to load nn models. The base class contains methods that will
        be needed for nn models of any type.
        """

        @Wrapping.require_init_if_extended
        def __init__(self, model_path: Path):
            """
            Load wrappers are constructed in context of a path where models
            are expected to be stored.
            """

            self._model_path = model_path

        @Deprecate.method(
            message="Use the model_path property instead.",
            dep_version="0.0.1",
            remove_version="0.1.0"
        )
        def get_model_path(self) -> Path:
            return self.model_path

        @Wrapping.utility
        @property
        def model_path(self) -> Path:
            return self._model_path

        @Wrapping.required
        @abstractmethod
        def get_model(self) -> NNB.Model:
            """This method should return access to the model.
            Output
            ----------------
            - a model object
            ----------------
            """
            ...

    class SplitLoadWrapper(metaclass=WrapperMeta):
        """
        A wrapper to load nn splits. The base class contains methods that will
        be needed for nn models of any type.
        """

        @Wrapping.require_init_if_extended
        def __init__(self, data_path: Path):
            self._data_path = as_path(data_path)

        @Deprecate.method(
            message="Use the data_path property instead.",
            dep_version="0.0.1",
            remove_version="0.1.0"
        )
        def get_data_path(self) -> Path:
            return self.data_path

        @Wrapping.utility
        @property
        def data_path(self) -> Path:
            return self._data_path

        @Wrapping.required
        @abstractmethod
        def get_ds(self, batch_size: int = 128) -> Iterable[DataBatch]:
            # TODO: DataReaders in RNN do not implement any abstract class
            # presently. What they need to implement is unclear. Fix.
            """
            Constructs a dataset object.

            Input
            ----------------
            - batch_size: int -- how much data (in terms of number of instances)
              to read at once. DataReader should not read all of the batches
              immediately but read/produce them during iteration.
            ----------------

            Output
            ----------------
            - Collection of DataBatch in some iterable container.
            ----------------
            """
            ...
