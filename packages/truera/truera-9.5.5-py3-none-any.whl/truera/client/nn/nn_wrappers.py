"""Deprecated"""

from truera.client import nn
from truera.client.nn import wrappers
from truera.client.nn.wrappers import nlp
from truera.client.nn.wrappers import tabular
from truera.client.nn.wrappers import timeseries
from truera.client.util.func_utils import Deprecate

Deprecate.module(
    name=__name__,
    message="Use truera.client.nn.wrappers* instead.",
    dep_version="0.0.1",
    remove_version="0.1.0"
)

# replicate names from new locations
BaselineLike = nn.BaselineLike
BaselineType = nn.BaselineType

DataReader = wrappers.DataReader
DataBatch = wrappers.DataBatch
TruBatch = wrappers.TruBatch

BaseTensor = nn.BaseTensor
BaseModel = nn.BaseModel

Base = wrappers.Base
Tabular = tabular.Tabular
Timeseries = timeseries.Timeseries
NLP = nlp.NLP
NNBackend = nn.NNBackend
Model = NNBackend.Model