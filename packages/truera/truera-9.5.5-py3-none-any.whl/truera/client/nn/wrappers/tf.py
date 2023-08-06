"""Utilities for wrapping tensorflow models of both v1/v2 types."""


def get_tf(version=None):
    try:
        tf = __import__("tensorflow")

        if tf.__version__[0] not in set(['1', '2']):
            raise RuntimeError("Only tensorflow versions 1 or 2 are supported.")

        if version is not None:
            assert tf.__version__.startswith(str(version))

    except:
        raise RuntimeError(
            f"Could not load tensorflow version {version}.*. "
            f"If you are wrapping a tensorflow {version} model, make sure you have an appropriate tensorflow version installed."
            f"If you intend to wrap a tensorflow {3-version} model, implement TensorFlowV{3-version}[ModelRunWrapper] instead."
        )

    return tf
