from truera.client.nn.wrappers import Base


class Tabular(Base):
    """
    Wrappers for models that take tabular data. Could be handled as timeseries
    with a single time step.

    * CURRENTLY NOT USED *
    """

    class ModelRunWrapper(Base.ModelRunWrapper):
        ...

    class ModelLoadWrapper(Base.ModelLoadWrapper):
        ...

    class SplitLoadWrapper(Base.SplitLoadWrapper):
        ...
