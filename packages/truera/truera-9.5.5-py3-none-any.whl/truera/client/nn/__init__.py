from __future__ import annotations

import dataclasses
from dataclasses import astuple
from dataclasses import dataclass
from dataclasses import fields
from enum import Enum
from typing import Any, Generic, Iterable, Type, TypeVar

# NN product version
__version__ = "0.0.1"

# Backend-specific models:
BaseModel = TypeVar("BaseModel")

# Backend-specific tensors:
BaseTensor = TypeVar("BaseTensor")

# from trulens.utils.typing import BaselineLike
BaselineLike = Any
# Any is actually BaselineLike from trulens but don't want to import trulens
# here. This file is imported by truera.client.truera_workspace which is common
# across diagnostic and nn products.


class BaselineType(Enum):
    """Baselines for integrated gradients.

    - FIXED -- A baseline that does not depend on input instance, is the same
      regardless of instance. E.g. all zeros.
    - DYNAMIC -- A baseline that is a function of the input instance. E.g. word
      embeddings replaced by zeros, control token embeddings kept as is.
    - DYNAMIC_INDEP: a baseline that is a function of more than just the input
      instance. Not presently supported. E.g. baseline that is another instance
      in a dataset.
    - CLS_PAD: TODO: Documentation
    """

    FIXED = 'fixed'
    DYNAMIC = 'dynamic'
    DYNAMIC_INDEP = 'dynamic_indep'
    CLS_PAD = 'cls_pad'

    @staticmethod
    def from_str(label):
        if label == 'fixed':
            return BaselineType.FIXED
        elif label == 'dynamic':
            return BaselineType.DYNAMIC
        elif label == 'dynamic_indep':
            return BaselineType.DYNAMIC_INDEP
        elif label == 'cls_pad':
            return BaselineType.CLS_PAD
        raise NotImplementedError(f'BaselineType {label} not supported')


class NNBackend(Generic[BaseTensor, BaseModel]):
    """
    Various decorators over the base tensor type to indicate their function in a
    model or ML pipeline. Included here are Model and Tensor which are meant to
    extend BaseModel and BaseTensor respectively. The goal of these is to be
    able to distinguish objects which are wrapped for us or by us from ones
    which are not. Base versions may not be ready for us, while the ones in this
    backend are created or wrapped by us. They can further indicate some
    information like whether a tensor represents an input or output or something
    else.
    """

    # TODO: reuse or merge with trulens backends
    class Model(object):  # WANT: subclass BaseModel
        """
        Backend's representation of a model. A user model should contain this
        somewhere inside of it (or be it). This should subclass BaseModel
        but cannot specify that in python right now.
        """
        ...

    class Tensor(object):  # WANT: subclass BaseTensor
        """Backend's tensors."""
        ...
        # Decorators might need some NNBackend-specific hacks to wrap. Define as
        # Tensor class, extending BaseTensor. However, due to python's type var
        # issues, I cannot label Tensor as subclass of BaseTensor here.

    # yapf: disable
    class Inputs(Tensor): ...
    class Batchable(Inputs): ...
    class Parameter(Inputs): ... # non-batchable model args
    class Embeddings(Batchable): ...
    class Masks(Batchable): ...
    class Words(Batchable): ... # TODO: perhaps rename to Tokens ?
    class Outputs(Tensor): ...
    class Logits(Outputs): ...
    class Probits(Outputs): ...
    # yapf: enable


@dataclass
class Batch:
    """
    Project-specific data batch based on dataclasses. This class must be
    extended for a project. Fields can be customized but each must have values
    that are iterable (i.e. list) with the same number of items. Each field must
    be defined using the `field` method giving it a constructor. Common
    constructors are

    - tuple constructs tuple
    - list constructs list
    - torch.tensor constructs torch.Tensor
    - numpy.array constructs numpy.ndarray
    - TODO tensorflow something
    """

    def __len__(self):
        return len(getattr(self, fields(self)[0].name))

    def __getitem__(self, slice):
        """
        Want `take` below but providing getitem for prefixes for compatility
        with other structures not implementing take.
        """

        start, stop, step = slice.start, slice.stop, slice.step

        if stop is None:
            stop = len(self)

        if step is None:
            step = 1

        assert start == 0 and step == 1, "only prefix is subscriptable"

        return self.take(slice.stop)

    def take(self, n: int):
        """
        Create a batch that contains only the first n instances in this batch.
        """

        tup_batch = tuple([] for _ in range(len(fields(self.__class__))))

        tup = astuple(self)

        for num_instances, item in enumerate(zip(*tup)):
            if num_instances > n:
                break

            for i, iv in enumerate(item):
                tup_batch[i].append(iv)

        storage_classes = list(map(Batch._get_factory, fields(self.__class__)))

        tup_batch = tuple(
            map(
                lambda storage_class_v: storage_class_v[0](storage_class_v[1]),
                zip(storage_classes, tup_batch)
            )
        )

        return self.__class__(*tup_batch)

    @staticmethod
    def field(factory):
        """
        Create a dataclass field with metadata including a reference to the
        given factory.
        """
        return dataclasses.field(metadata=dict(factory=factory))

    @staticmethod
    def _get_factory(field):
        if "factory" not in field.metadata:
            raise ValueError(
                f"Field {field.name} does not have a factory. "
                "Make sure you define your fields with DataBatch.field ."
            )
        return field.metadata['factory']

    @staticmethod
    def flatten_batches(batches: Iterable[Batch]) -> Iterable[Batch]:
        """
        Given batches of some number of instances, return batches containing
        only one instance each.
        """
        for batch in batches:
            tup = astuple(batch)
            for vals in zip(
                *tup
            ):  # requires each value in tup is iterable, and has same number of items
                yield batch.__class__(*[[v] for v in vals])

    @staticmethod
    def collate(items: Iterable[Batch]) -> Batch:
        """
        Given a collection of batches, produce one batch that contains all of
        the same items.
        """

        tup_batch = None
        databatch = None

        for databatch in items:
            if tup_batch is None:
                tup_batch = tuple(
                    [] for _ in range(len(fields(databatch.__class__)))
                )

            tup = astuple(databatch)
            # Add each field's value to its appropriate list.

            for item in zip(*tup):
                for i, iv in enumerate(item):
                    tup_batch[i].append(iv)

        assert databatch is not None, "no databatches given to collate"

        storage_classes = list(
            map(Batch._get_factory, fields(databatch.__class__))
        )

        tup_batch = tuple(
            map(
                lambda storage_class_v: storage_class_v[0](storage_class_v[1]),
                zip(storage_classes, tup_batch)
            )
        )

        return databatch.__class__(*tup_batch)

    def batch(self, batch_size: int) -> Iterable[Batch]:
        return self.rebatch(batches=[self], batch_size=batch_size)

    @classmethod
    def _batch(cls: Type[Batch], items: Iterable[Batch],
               batch_size: int) -> Iterable[Batch]:
        """
        Given an iterable of DataBatches containing one instance each, batch the
        them into size `batch_size` DataBatches. The result is a DataBatch with
        the values for the various fields being of the `batch_size` size.
        """

        it = iter(items)

        while True:
            instances = []
            try:
                for _ in range(batch_size):
                    instances.append(next(it))
            except StopIteration:
                pass

            if len(instances) > 0:
                yield cls.collate(instances)
            else:
                return

    @classmethod
    def rebatch(cls: Type[Batch], batches: Iterable[Batch],
                batch_size: int) -> Iterable[Batch]:
        """
        Given an iterable over DataBatches of some size, rebatch them into
        DataBatches of `batch_size` size.
        """

        # First flatten into single-instance batches.
        instances = cls.flatten_batches(batches)

        # The batch into the new size.
        return cls._batch(items=instances, batch_size=batch_size)
