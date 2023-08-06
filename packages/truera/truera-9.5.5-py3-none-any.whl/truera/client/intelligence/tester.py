from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from typing import Optional, Sequence, Tuple, TYPE_CHECKING

from truera.protobuf.public.modeltest import modeltest_pb2

if TYPE_CHECKING:
    from truera.client.intelligence.model_tests import ModelTestDetails
    from truera.client.intelligence.model_tests import ModelTestLeaderboard
    from truera.client.intelligence.model_tests import ModelTestResults

SUPPORTED_TEST_TYPES = ["performance", "fairness", "stability"]


class Tester(ABC):

    TEST_TYPE_STRING_TO_MODEL_TEST_TYPE_ENUM = {
        "performance": modeltest_pb2.MODEL_TEST_TYPE_PERFORMANCE,
        "stability": modeltest_pb2.MODEL_TEST_TYPE_STABILITY,
        "fairness": modeltest_pb2.MODEL_TEST_TYPE_FAIRNESS,
    }

    def _validate_test_types(
        self, test_types: Optional[Sequence[str]]
    ) -> Sequence[str]:
        if test_types is None:
            return SUPPORTED_TEST_TYPES
        for curr in test_types:
            if curr not in SUPPORTED_TEST_TYPES:
                raise ValueError(
                    f"{curr} not a valid test-type! Must be one of {SUPPORTED_TEST_TYPES}"
                )
        return test_types

    @abstractmethod
    def add_performance_test(
        self,
        data_split_name: str,
        metric: str,
        *,
        segment_group_name: Optional[str] = None,
        segment_name: Optional[str] = None,
        warn_if_less_than: Optional[float] = None,
        warn_if_greater_than: Optional[float] = None,
        warn_if_within: Optional[Tuple[float, float]] = None,
        warn_if_outside: Optional[Tuple[float, float]] = None,
        warn_threshold_type: str = "ABSOLUTE",
        fail_if_less_than: Optional[float] = None,
        fail_if_greater_than: Optional[float] = None,
        fail_if_within: Optional[Tuple[float, float]] = None,
        fail_if_outside: Optional[Tuple[float, float]] = None,
        fail_threshold_type: str = "ABSOLUTE",
        reference_split_name: Optional[str] = None,
        reference_model_name: Optional[str] = None,
        overwrite: bool = False
    ) -> None:
        """Add a performance test to the current data collection in context. To set warning condition, please provide one of [`warn_if_less_than`, `warn_if_greater_than`, `warn_if_within`, `warn_if_outside`].
        Similarly, to set fail condition please provide one of [`fail_if_less_than`, `fail_if_greater_than`, `fail_if_within`, `fail_if_outside`].

        Args:
            data_split_name: The name of the data split that we want to use for the test.
            metric: Performance metric for the test. Must be one of the options returned by `list_performance_metrics`.
            segment_group_name: Name of segment group to use as filter.
            segment_name: Name of the segment within the segment group.
            warn_if_less_than: Warn if score is less than the value specified in this argument.
            warn_if_greater_than: Warn if score is greter than the value specified in this argument.
            warn_if_within: Warn if `value[0] < score < value[1]`.
            warn_if_outside: Warn if `score < value[0] OR score > value[1]`.
            warn_threshold_type: Must be one of ["ABSOLUTE", "RELATIVE"]. Describe whether the warning threshold is defined as absolute value or relative to split in `reference_split_name`. If it's relative, the effective threshold is `value + score_of_reference_split`. Defaults to "ABSOLUTE".
            fail_if_less_than: Fail if score is less than the value specified in this argument.
            fail_if_greater_than: Fail if score is greter than the value specified in this argument.
            fail_if_within: Fail if `value[0] < score < value[1]`.
            fail_if_outside: Fail if `score < value[0] OR score > value[1]`.
            fail_threshold_type: Must be one of ["ABSOLUTE", "RELATIVE"]. Describe whether the fail threshold is defined as absolute value or relative to split in `reference_split_name`. If it's relative, the effective threshold is `value + score_of_reference_split`. Defaults to "ABSOLUTE".
            reference_split_name: Name of the reference split used for the "RELATIVE" threshold type. If not specified and `reference_model_name` is also not provided, the relative threshold will be calculated with respect to each models' train split (for models whose train split is not specified, then those will be treated as if no thresholds were specified).
            reference_model_name: Name of the reference model used for the "RELATIVE" threshold type. Can't be specified if `reference_split_name` is provided.
            overwrite: If set to `True`, will overwrite the thresholds for existing test specified under the given data_split_name, segment, and metric. Defaults to `False`.
        """
        pass

    @abstractmethod
    def add_stability_test(
        self,
        comparison_data_split_name: str,
        base_data_split_name: Optional[str] = None,
        metric: str = "DIFFERENCE_OF_MEAN",
        *,
        segment_group_name: Optional[str] = None,
        segment_name: Optional[str] = None,
        warn_if_less_than: Optional[float] = None,
        warn_if_greater_than: Optional[float] = None,
        warn_if_within: Optional[Tuple[float, float]] = None,
        warn_if_outside: Optional[Tuple[float, float]] = None,
        fail_if_less_than: Optional[float] = None,
        fail_if_greater_than: Optional[float] = None,
        fail_if_within: Optional[Tuple[float, float]] = None,
        fail_if_outside: Optional[Tuple[float, float]] = None,
        overwrite: bool = False
    ) -> None:
        """Add a stability test to the current data collection in context. To set warning condition, please provide one of [`warn_if_less_than`, `warn_if_greater_than`, `warn_if_within`, `warn_if_outside`].
        Similarly, to set fail condition please provide one of [`fail_if_less_than`, `fail_if_greater_than`, `fail_if_within`, `fail_if_outside`].

        Args:
            comparison_data_split_name: The name of the data split that we want to use for the test.
            base_data_split_name: The name of the reference data split to use as the comparison baseline for the test. If `None`, will be the model's train split.
            metric: Stability metric for the test. Must be one ["WASSERSTEIN", "DIFFERENCE_OF_MEAN", "POPULATION_STABILITY_INDEX"]
            segment_group_name: Name of segment group to use as filter.
            segment_name: Name of the segment within the segment group.
            warn_if_less_than: Warn if score is less than the value specified in this argument.
            warn_if_greater_than: Warn if score is greter than the value specified in this argument.
            warn_if_within: Warn if `value[0] < score < value[1]`.
            warn_if_outside: Warn if `score < value[0] OR score > value[1]`.
            fail_if_less_than: Fail if score is less than the value specified in this argument.
            fail_if_greater_than: Fail if score is greter than the value specified in this argument.
            fail_if_within: Fail if `value[0] < score < value[1]`.
            fail_if_outside: Fail if `score < value[0] OR score > value[1]`.
            overwrite: If set to `True`, will overwrite the thresholds for existing test specified under the given comparison_data_split_name, segment, and metric. Defaults to `False`.
        """
        pass

    @abstractmethod
    def add_fairness_test(
        self,
        data_split_name: str,
        segment_group_name: str,
        protected_segment_name: str,
        comparison_segment_name: Optional[str] = None,
        metric: str = "DISPARATE_IMPACT_RATIO",
        *,
        warn_if_less_than: Optional[float] = None,
        warn_if_greater_than: Optional[float] = None,
        warn_if_within: Optional[Tuple[float, float]] = None,
        warn_if_outside: Optional[Tuple[float, float]] = None,
        fail_if_less_than: Optional[float] = None,
        fail_if_greater_than: Optional[float] = None,
        fail_if_within: Optional[Tuple[float, float]] = None,
        fail_if_outside: Optional[Tuple[float, float]] = None,
        overwrite: bool = False
    ) -> None:
        """Add a fairness test to the current data collection in context. To set warning condition, please provide one of [`warn_if_less_than`, `warn_if_greater_than`, `warn_if_within`, `warn_if_outside`].
        Similarly, to set fail condition please provide one of [`fail_if_less_than`, `fail_if_greater_than`, `fail_if_within`, `fail_if_outside`].

        Args:
            data_split_name: The name of the data split that we want to use for the test.
            segment_group_name: Name of segment group to use as filter.
            protected_segment_name: Name of the segment within the segment group to check fairness for.
            comparison_segment_name: Name of the segment within the segment group to check fairness against.
            metric: Fairness metric for the test. Must be one of the options returned by `list_fairness_metrics`.
            warn_if_less_than: Warn if score is less than the value specified in this argument.
            warn_if_greater_than: Warn if score is greter than the value specified in this argument.
            warn_if_within: Warn if `value[0] < score < value[1]`.
            warn_if_outside: Warn if `score < value[0] OR score > value[1]`.
            fail_if_less_than: Fail if score is less than the value specified in this argument.
            fail_if_greater_than: Fail if score is greter than the value specified in this argument.
            fail_if_within: Fail if `value[0] < score < value[1]`.
            fail_if_outside: Fail if `score < value[0] OR score > value[1]`.
            overwrite: If set to `True`, will overwrite the thresholds for existing test specified under the given data_split_name, segment, and metric. Defaults to `False`.
        """
        pass

    @abstractmethod
    def get_model_tests(
        self, data_split_name: Optional[str] = None
    ) -> ModelTestDetails:
        """Get the details of all the model tests in the current data collection or the model tests associated with the given data split.

        Args:
            data_split_name: If provided, filters to the tests associated with this split.

        Returns:
            A `ModelTestDetails` object containing the details for each test that has been created.
            On Jupyter notebooks, this object will be displayed as a nicely formatted HTML table.
            This object also has a `pretty_print` as well as `as_json` and `as_dict` representation.
        """
        pass

    @abstractmethod
    def get_model_test_results(
        self,
        data_split_name: Optional[str] = None,
        comparison_models: Optional[Sequence[str]] = None,
        test_types: Optional[Sequence[str]] = None,
        wait: bool = True
    ) -> ModelTestResults:
        """Get the test results for the model in context.

        Args:
            data_split_name: If provided, filters to the tests associated with this split.
            comparison_models: If provided, compare the test results against this list of models.
            test_types: If provided, filter to only the given test-types. Must be a subset of ["performance", "stability", "fairness"] or None (which defaults to all). Defaults to None.
            wait: Whether to wait for test results to finish computing.

        Returns:
            A `ModelTestResults` object containing the test results for the model in context.
            On Jupyter notebooks, this object will be displayed as a nicely formatted HTML table.
            This object also has a `pretty_print` as well as `as_json` and `as_dict` representation.
        """
        pass

    @abstractmethod
    def get_model_leaderboard(
        self,
        sort_by: str = "performance",
        wait: bool = True
    ) -> ModelTestLeaderboard:
        """Get the summary of test outcomes for all models in the data collection.

        Args:
            sort_by: Rank models according to the test type specified in this arg (models with the fewest test failures will be at the top). Must be one of ["performance", "stability", "fairness"]. Defaults to "performance".
            wait: Whether to wait for test results to finish computing. Defaults to True.

        Returns:
            A `ModelTestLeaderboard` object containing the summary of test outcomes for all models in the data collection.
            On Jupyter notebooks, this object will be displayed as a nicely formatted HTML table.
            This object also has a `pretty_print` as well as `as_json` and `as_dict` representation.
        """
        pass

    @abstractmethod
    def delete_tests(
        self,
        test_type: Optional[str] = None,
        data_split_name: Optional[str] = None,
        segment_group_name: Optional[str] = None,
        segment_name: Optional[str] = None,
        metric: Optional[str] = None
    ) -> None:
        """Delete tests.

        Args:
            test_type: Only delete tests of this type. Must be one of ["performance", "stability", "fairness"] or None. If None, delete all test types. Defaults to None.
            data_split_name: Only delete tests associated with this data split. Defaults to None.
            segment_group_name: Only delete tests associated with this segment group. Defaults to None.
            segment_name: Only delete tests associated with this segment. Defaults to None.
            metric: Only delete tests associated with this metric. Defaults to None.
        """
        pass
