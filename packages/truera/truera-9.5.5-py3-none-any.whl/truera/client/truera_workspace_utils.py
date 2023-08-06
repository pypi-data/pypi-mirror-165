import logging
import tempfile
from typing import Optional

import pandas as pd

import truera.public.feature_influence_constants as fi_constants


def get_output_type_from_score_type(score_type: str) -> str:
    if score_type in fi_constants.VALID_SCORE_TYPES_FOR_CLASSIFICATION:
        return "classification"
    elif score_type in fi_constants.VALID_SCORE_TYPES_FOR_REGRESSION:
        return "regression"
    else:
        raise ValueError(f"Score type \"{score_type}\" not recognized!")


def is_regression_score_type(score_type: str) -> bool:
    return get_output_type_from_score_type(score_type) == "regression"


def sample_spark_dataframe(
    spark_dataframe,
    sample_count: int,
    sample_kind: str,
    seed: int,
    logger=None,
) -> pd.DataFrame:
    logger = logger if logger else logging.getLogger(__name__)
    total_count = spark_dataframe.count()
    sample_count = min(sample_count, total_count)
    if total_count == 0:
        raise ValueError("Provided Spark Dataframe is empty!")
    if sample_kind.lower() == "first":
        logger.info(
            f"Sampling first {sample_count} rows from PySpark DataFrame"
        )
        return spark_dataframe.limit(sample_count).toPandas()

    logger.info(
        f"Sampling approximately {sample_count} rows from PySpark DataFrame"
    )
    return spark_dataframe.sample(sample_count / total_count, seed).toPandas()


def create_temp_file_path(extension: Optional[str] = None) -> str:
    # In some scenarios, we cannot use NamedTemporaryFile
    # directly as it doesn't allow second open on Windows NT.
    # So we use NamedTemporaryFile to just create a name for us
    # and let it delete the file, but use the name later.
    with tempfile.NamedTemporaryFile(mode="w+") as file:
        file_name = file.name
        if extension:
            file_name += "." + extension
    return file_name
