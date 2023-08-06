from typing import Iterable

from truera.client.nn import NNBackend
from truera.client.nn.wrappers import DataBatch

try:
    torch = __import__('torch')
    data = torch.utils.data

except:
    raise RuntimeError(
        "Could not load torch; if you are wrapping a torch model, make sure pytorch is installed."
    )


class Backend(NNBackend[torch.Tensor, torch.nn.Module]):
    # TODO(piotrm): see if we can reuse trulens NNBackend

    # backend-specific model representations for pytorch are torch.nn.Module
    Model = torch.nn.Module

    class Tensor(torch.Tensor):
        torch = __import__('torch')
        # TODO(piotrm): figure out how not have to import here too

        @classmethod
        def __torch_function__(cls, func, types, args=(), kwargs=None):
            """Undo our custom tensor types once any torch method is called
            on them."""
            return super().__torch_function__(
                func, map(lambda t: cls.torch.Tensor, types),
                map(
                    lambda arg: arg.as_subclass(cls.torch.Tensor)
                    if isinstance(arg, cls.torch.Tensor) else arg, args
                ), kwargs
            )

        @staticmethod
        def __new__(cls, tensor):
            return tensor.as_subclass(cls)

    # yapf: disable
    class Inputs(Tensor): ...
    class Batchable(Inputs): ...
    class Parameter(Inputs): ...
    class Embeddings(Batchable): ...
    class Masks(Batchable): ...
    class Words(Batchable): ...
    class Outputs(Tensor): ...
    class Logits(Outputs): ...
    class Probits(Outputs): ...
    # yapf: enable


class Torch:
    """Pytorch-specific methods and wrapper requirements."""

    class IterableDataset(data.IterableDataset):
        """
        A basic implementation of pytorch's IterableDataset. Constructed with an
        iterable of instances and iterates them when called upon.
        """

        def __init__(self, instances: Iterable):
            self._instances = instances

        def __iter__(self):
            return iter(self._instances)

    class DataLoader(data.DataLoader):
        """
        A variant of pytorch's DataLoader that can collate dataclasses like
        DataBatch.
        """

        def __init__(self, *args, **kwargs):
            super().__init__(collate_fn=DataBatch.collate, *args, **kwargs)

    @staticmethod
    def get_device() -> torch.device:
        # TODO: might need to generalize or configure this method. However, it
        # should probably not be a user provided method.
        use_cuda = torch.cuda.is_available()
        device = torch.device("cuda:0" if use_cuda else "cpu")
        return device
