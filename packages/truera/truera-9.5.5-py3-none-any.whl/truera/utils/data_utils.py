from typing import Optional, Sequence

import numpy as np
import pandas as pd

import truera.protobuf.public.aiq.intelligence_service_pb2 as is_pb

MAX_UNIQUE_VALS_FOR_CATEGORICAL_FEATURES = 5


def update_value_table_from_dataframe(
    df: pd.DataFrame, value_table: is_pb.ValueTable
):
    for col, col_dtype in df.dtypes.iteritems():
        value_list = value_table.column_value_map[col]
        series = df[col]
        if pd.api.types.is_string_dtype(col_dtype):
            series = series.fillna("").astype(str)
            value_list.strings.values.extend(series.tolist())
        elif pd.api.types.is_integer_dtype(col_dtype):
            value_list.integers.values.extend(series.tolist())
        else:
            value_list.floats.values.extend(series.tolist())
    if df.index.name:
        #TODO(AB#5405): always return df index regardless of whether or not it is named (indicating system IDs are present)
        # will require updating many tests (pyclient, split data, model data)
        value_table.row_labels.extend(df.index.tolist())


def update_float_table_from_dataframe(
    df: pd.DataFrame, float_table: is_pb.FloatTable
):
    for col in df.columns:
        float_list = float_table.column_value_map[col]
        float_list.values.extend(df[col].tolist())
    if df.index.name:
        float_table.row_labels.extend(df.index.tolist())


def update_string_table_from_dataframe(
    df: pd.DataFrame, string_table: is_pb.StringTable
):
    for col in df.columns:
        string_list = string_table.column_value_map[col]
        string_list.values.extend(df[col].tolist())
    if df.index.name:
        string_table.row_labels.extend(df.index.tolist())


def is_categorical_feature(feature_data: pd.Series) -> bool:
    return (not np.issubdtype(feature_data.dtype, np.number)) or (
        len(feature_data.unique()) <= MAX_UNIQUE_VALS_FOR_CATEGORICAL_FEATURES
    )


def value_table_to_df(
    value_table: is_pb.ValueTable,
    ordered_column_names: Optional[Sequence[str]] = None
):
    cvm = value_table.column_value_map
    cols = ordered_column_names if ordered_column_names else cvm.keys()
    mp = {col: get_list_from_value_list(cvm[col]) for col in cols}
    ret = pd.DataFrame(mp, columns=cols)
    row = value_table.row_labels
    if row:
        ret.index = row
    return ret


def string_table_to_df(
    string_table: is_pb.StringTable,
    ordered_column_names: Optional[Sequence[str]] = None
):
    cvm = string_table.column_value_map
    cols = ordered_column_names if ordered_column_names else cvm.keys()
    mp = {col: list(cvm[col].values) for col in cols}
    ret = pd.DataFrame(mp, columns=cols)
    row = string_table.row_labels
    if row:
        ret.index = row
    return ret


def value_table_to_df_or_series(
    value_table: is_pb.ValueTable,
    ordered_column_names: Optional[Sequence[str]] = None
):
    df = value_table_to_df(
        value_table, ordered_column_names=ordered_column_names
    )
    if df.shape[1] == 1:
        return df[df.columns[0]]
    return df


def float_table_to_df(float_table, ordered_column_names=None):
    cvm = float_table.column_value_map
    cols = ordered_column_names if ordered_column_names else cvm.keys()
    mp = {col: list(cvm[col].values) for col in cols}
    ret = pd.DataFrame(mp, columns=cols)
    row = float_table.row_labels
    if row:
        ret.index = row
    return ret


def get_list_from_value_list(value_list):
    has_strings = hasattr(value_list,
                          "strings") and len(value_list.strings.values) > 0
    has_integers = hasattr(value_list,
                           "integers") and len(value_list.integers.values) > 0
    if has_integers:
        ret = value_list.integers.values
    elif has_strings:
        ret = value_list.strings.values
    else:
        ret = value_list.floats.values
    return list(ret)
