from __future__ import annotations

import logging
import time
from typing import (
    Callable, Mapping, Optional, Sequence, Tuple, TYPE_CHECKING, Union
)

from google.protobuf.json_format import MessageToDict

from truera.client.public.communicator.http_communicator import \
    AlreadyExistsError
from truera.client.public.communicator.model_test_http_communicator import \
    HttpModelTestCommunicator
from truera.client.services.mrc_client import MrcClient
from truera.client.services.pending_operation_client import \
    TimeoutExceededException
from truera.client.util.absolute_progress_bar import AbsoluteProgressBars
from truera.protobuf.public.aiq.accuracy_pb2 import \
    AccuracyType as _PBAccuracyType
from truera.protobuf.public.aiq.distance_pb2 import \
    DistanceType as _PBDistanceType
from truera.protobuf.public.aiq.intelligence_service_pb2 import \
    BiasType as _PBBiasType
from truera.protobuf.public.data.segment_pb2 import SegmentID as _PBSegmentID
from truera.protobuf.public.modeltest import modeltest_pb2
from truera.protobuf.public.modeltest import modeltest_service_pb2
from truera.protobuf.public.modeltest.modeltest_pb2 import \
    TestThreshold as _PBTestThreshold

if TYPE_CHECKING:
    from truera.client.public.auth_details import AuthDetails

SINGLE_VALUE_THRESHOLD_TYPE_TO_PB = {
    "ABSOLUTE": _PBTestThreshold.ThresholdType.ABSOLUTE_SINGLE_VALUE,
    "RELATIVE": _PBTestThreshold.ThresholdType.RELATIVE_SINGLE_VALUE
}
VALUE_RANGE_THRESHOLD_TYPE_TO_PB = {
    "ABSOLUTE": _PBTestThreshold.ThresholdType.ABSOLUTE_VALUE_RANGE,
    "RELATIVE": _PBTestThreshold.ThresholdType.RELATIVE_VALUE_RANGE
}


def _create_test_threshold_pb(
    threshold_type: str,
    *,
    fail_if_less_than: Optional[float] = None,
    fail_if_greater_than: Optional[float] = None,
    fail_if_within: Optional[Tuple[float, float]] = None,
    fail_if_outside: Optional[Tuple[float, float]] = None,
    reference_split_id: Optional[str] = None,
    reference_model_id: Optional[str] = None
) -> _PBTestThreshold:
    test_threshold = _PBTestThreshold()
    if fail_if_less_than is not None or fail_if_greater_than is not None:
        test_threshold.threshold_type = SINGLE_VALUE_THRESHOLD_TYPE_TO_PB[
            threshold_type]
        # pylint: disable=protobuf-type-error
        test_threshold.value.value = fail_if_less_than if fail_if_less_than is not None else fail_if_greater_than
        test_threshold.value.condition = _PBTestThreshold.ThresholdValue.WARN_OR_FAIL_IF_LESS_THAN if fail_if_less_than is not None else _PBTestThreshold.ThresholdValue.WARN_OR_FAIL_IF_GREATER_THAN
    elif fail_if_within is not None or fail_if_outside is not None:
        test_threshold.threshold_type = VALUE_RANGE_THRESHOLD_TYPE_TO_PB[
            threshold_type]
        value_range = fail_if_within if fail_if_within is not None else fail_if_outside
        test_threshold.value_range.lower_bound = value_range[0]
        test_threshold.value_range.upper_bound = value_range[1]
        test_threshold.value_range.condition = _PBTestThreshold.ThresholdValueRange.WARN_OR_FAIL_IF_OUTSIDE if fail_if_outside is not None else _PBTestThreshold.ThresholdValueRange.WARN_OR_FAIL_IF_WITHIN
    if test_threshold.threshold_type == _PBTestThreshold.ThresholdType.RELATIVE_SINGLE_VALUE or test_threshold.threshold_type == _PBTestThreshold.ThresholdType.RELATIVE_VALUE_RANGE:
        if reference_split_id:
            # pylint: disable=protobuf-type-error
            test_threshold.reference_split_id = reference_split_id
        elif reference_model_id:
            # pylint: disable=protobuf-type-error
            test_threshold.reference_model_id = reference_model_id
    return test_threshold


class ModelTestClient:

    def __init__(
        self,
        connection_string: str,
        auth_details: AuthDetails = None,
        logger=None,
        use_http: bool = False,
        *,
        verify_cert: Union[bool, str] = True
    ):
        if (not use_http):
            from truera.client.private.communicator.model_test_grpc_communicator import \
                GrpcModelTestCommunicator
        self.logger = logger or logging.getLogger(__name__)
        self.communicator = HttpModelTestCommunicator(
            connection_string, auth_details, logger, verify_cert=verify_cert
        ) if use_http else GrpcModelTestCommunicator(
            connection_string, auth_details, logger
        )
        self.mrc_client = MrcClient(
            f"{connection_string.rstrip('/')}/api/mrc",
            auth_details,
            logger,
            verify_cert=verify_cert
        )

    def create_tests_from_split(
        self, project_id: str, split_id: str
    ) -> Sequence[modeltest_pb2.ModelTest]:
        request = modeltest_service_pb2.CreateTestsFromSplitRequest(
            project_id=project_id, split_id=split_id
        )
        response = self.communicator.create_tests_from_split(request)
        return response.model_tests

    def create_performance_test(
        self,
        project_id: str,
        split_id: str,
        metric: str,
        *,
        segmentation_id: Optional[str] = None,
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
        reference_split_id: Optional[str] = None,
        reference_model_id: Optional[str] = None,
        autorun: bool = True,
        overwrite: bool = False
    ) -> str:
        if not metric in _PBAccuracyType.Type.keys():
            raise ValueError(
                f"Provided performance metric \"{metric}\" is not supported. Supported metrics: {_PBAccuracyType.Type.keys()}"
            )

        request = modeltest_service_pb2.CreatePerformanceTestRequest(
            project_id=project_id,
            split_id=split_id,
            autorun=autorun,
            overwrite=overwrite
        )
        if segmentation_id:
            if not segment_name:
                raise ValueError(
                    f"Need to provide `segment_name` to create test using segment."
                )
            segment_id = _PBSegmentID(
                segmentation_id=segmentation_id, segment_name=segment_name
            )
            request.segment_id.CopyFrom(segment_id)
        threshold_warning, threshold_fail = self._validate_and_get_thresholds(
            warn_if_less_than=warn_if_less_than,
            warn_if_greater_than=warn_if_greater_than,
            warn_if_within=warn_if_within,
            warn_if_outside=warn_if_outside,
            warn_threshold_type=warn_threshold_type,
            fail_if_less_than=fail_if_less_than,
            fail_if_greater_than=fail_if_greater_than,
            fail_if_within=fail_if_within,
            fail_if_outside=fail_if_outside,
            fail_threshold_type=fail_threshold_type,
            reference_split_id=reference_split_id,
            reference_model_id=reference_model_id
        )

        test_definition = modeltest_pb2.PerformanceTest()
        test_definition.performance_metric_and_threshold.accuracy_type = _PBAccuracyType.Type.Value(
            metric
        )
        if threshold_warning:
            test_definition.performance_metric_and_threshold.threshold_warning.CopyFrom(
                threshold_warning
            )
        if threshold_fail:
            test_definition.performance_metric_and_threshold.threshold_fail.CopyFrom(
                threshold_fail
            )
        request.test_definition.CopyFrom(test_definition)
        try:
            response = self.communicator.create_performance_test(request)
        except AlreadyExistsError as e:
            raise AlreadyExistsError(
                f"The specified performance test already exists. Set `overwrite=True` to overwrite the test parameters."
            ) from e
        return response.test_id

    def _validate_and_get_thresholds(
        self,
        *,
        warn_if_less_than: Optional[float] = None,
        warn_if_greater_than: Optional[float] = None,
        warn_if_within: Optional[Tuple[float, float]] = None,
        warn_if_outside: Optional[Tuple[float, float]] = None,
        warn_threshold_type: Optional[str] = None,
        fail_if_less_than: Optional[float] = None,
        fail_if_greater_than: Optional[float] = None,
        fail_if_within: Optional[Tuple[float, float]] = None,
        fail_if_outside: Optional[Tuple[float, float]] = None,
        fail_threshold_type: Optional[str] = None,
        reference_split_id: Optional[str] = "",
        reference_model_id: Optional[str] = "",
    ) -> Tuple[_PBTestThreshold, _PBTestThreshold]:
        if sum(
            [
                warn_if_less_than is not None, warn_if_greater_than is not None,
                warn_if_within is not None, warn_if_outside is not None
            ]
        ) > 1:
            raise ValueError(
                "Provided warning thresholds have conflicts! Please only provide one of [`warn_if_less_than`, `warn_if_greater_than`, `warn_if_within`, `warn_if_outside`]."
            )
        if sum(
            [
                fail_if_less_than is not None, fail_if_greater_than is not None,
                fail_if_within is not None, fail_if_outside is not None
            ]
        ) > 1:
            raise ValueError(
                "Provided fail thresholds have conflicts! Please only provide one of [`fail_if_less_than`, `fail_if_greater_than`, `fail_if_within`, `fail_if_outside`]."
            )

        if warn_if_within is not None or warn_if_outside is not None or fail_if_within is not None or fail_if_outside is not None:
            range_threshold = warn_if_within or warn_if_outside or fail_if_within or fail_if_outside
            if not isinstance(range_threshold,
                              Sequence) or len(range_threshold) != 2:
                raise ValueError(
                    "Range threshold needs to be a `Sequence` with 2 elements: `(lower_bound, upper_bound)`."
                )

        # SINGLE_VALUE_THRESHOLD_TYPE_TO_PB and VALUE_RANGE_THRESHOLD_TYPE_TO_PB have the same keys, so only check against one of them
        if warn_threshold_type not in SINGLE_VALUE_THRESHOLD_TYPE_TO_PB:
            raise ValueError(
                f"Warning threshold type need to be one of: {list(SINGLE_VALUE_THRESHOLD_TYPE_TO_PB.keys())}. Provided: \"{warn_threshold_type}\""
            )
        if fail_threshold_type not in SINGLE_VALUE_THRESHOLD_TYPE_TO_PB:
            raise ValueError(
                f"Fail threshold type need to be one of: {list(SINGLE_VALUE_THRESHOLD_TYPE_TO_PB.keys())}. Provided: \"{fail_threshold_type}\""
            )

        if reference_model_id and reference_split_id:
            raise ValueError(
                "Please only provide one of `reference_model_id` or `reference_split_id` for relative test threshold, but not both!"
            )

        threshold_warning = _create_test_threshold_pb(
            threshold_type=warn_threshold_type,
            fail_if_less_than=warn_if_less_than,
            fail_if_greater_than=warn_if_greater_than,
            fail_if_within=warn_if_within,
            fail_if_outside=warn_if_outside,
            reference_split_id=reference_split_id,
            reference_model_id=reference_model_id
        )
        threshold_fail = _create_test_threshold_pb(
            threshold_type=fail_threshold_type,
            fail_if_less_than=fail_if_less_than,
            fail_if_greater_than=fail_if_greater_than,
            fail_if_within=fail_if_within,
            fail_if_outside=fail_if_outside,
            reference_split_id=reference_split_id,
            reference_model_id=reference_model_id
        )
        return threshold_warning, threshold_fail

    def create_stability_test(
        self,
        project_id: str,
        comparison_data_split_id: str,
        base_data_split_id: Optional[str],
        metric: str,
        *,
        segmentation_id: Optional[str],
        segment_name: Optional[str],
        warn_if_less_than: Optional[float],
        warn_if_greater_than: Optional[float],
        warn_if_within: Optional[Tuple[float, float]],
        warn_if_outside: Optional[Tuple[float, float]],
        fail_if_less_than: Optional[float],
        fail_if_greater_than: Optional[float],
        fail_if_within: Optional[Tuple[float, float]],
        fail_if_outside: Optional[Tuple[float, float]],
        autorun: bool,
        overwrite: bool,
    ) -> str:
        if not metric in _PBDistanceType.keys():
            raise ValueError(
                f"Provided stability metric \"{metric}\" is not supported. Supported metrics: {_PBDistanceType.keys()}"
            )

        request = modeltest_service_pb2.CreateStabilityTestRequest(
            project_id=project_id,
            split_id=comparison_data_split_id,
            autorun=autorun,
            overwrite=overwrite
        )
        if segmentation_id:
            if not segment_name:
                raise ValueError(
                    f"Need to provide `segment_name` to create test using segment."
                )
            segment_id = _PBSegmentID(
                segmentation_id=segmentation_id, segment_name=segment_name
            )
            request.segment_id.CopyFrom(segment_id)

        threshold_warning, threshold_fail = self._validate_and_get_thresholds(
            warn_if_less_than=warn_if_less_than,
            warn_if_greater_than=warn_if_greater_than,
            warn_if_within=warn_if_within,
            warn_if_outside=warn_if_outside,
            warn_threshold_type="ABSOLUTE",
            fail_if_less_than=fail_if_less_than,
            fail_if_greater_than=fail_if_greater_than,
            fail_if_within=fail_if_within,
            fail_if_outside=fail_if_outside,
            fail_threshold_type="ABSOLUTE"
        )

        test_definition = modeltest_pb2.StabilityTest()
        if base_data_split_id:
            test_definition.base_split_id = base_data_split_id
        test_definition.stability_metric_and_threshold.distance_type = _PBDistanceType.Value(
            metric
        )
        if threshold_warning:
            test_definition.stability_metric_and_threshold.threshold_warning.CopyFrom(
                threshold_warning
            )
        if threshold_fail:
            test_definition.stability_metric_and_threshold.threshold_fail.CopyFrom(
                threshold_fail
            )
        request.test_definition.CopyFrom(test_definition)
        try:
            response = self.communicator.create_stability_test(request)
        except AlreadyExistsError as e:
            raise AlreadyExistsError(
                f"The specified stability test already exists. Set `overwrite=True` to overwrite the test parameters."
            ) from e
        return response.test_id

    def create_fairness_test(
        self,
        project_id: str,
        split_id: str,
        segmentation_id: str,
        protected_segment_name: str,
        comparison_segment_name: Optional[str],
        metric: str,
        *,
        warn_if_less_than: Optional[float],
        warn_if_greater_than: Optional[float],
        warn_if_within: Optional[Tuple[float, float]],
        warn_if_outside: Optional[Tuple[float, float]],
        fail_if_less_than: Optional[float],
        fail_if_greater_than: Optional[float],
        fail_if_within: Optional[Tuple[float, float]],
        fail_if_outside: Optional[Tuple[float, float]],
        autorun: bool,
        overwrite: bool,
    ) -> str:
        if not metric in _PBBiasType.Type.keys():
            raise ValueError(
                f"Provided fairness metric \"{metric}\" is not supported. Supported metrics: {_PBBiasType.Type.keys()}"
            )

        request = modeltest_service_pb2.CreateFairnessTestRequest(
            project_id=project_id,
            split_id=split_id,
            autorun=autorun,
            overwrite=overwrite
        )
        threshold_warning, threshold_fail = self._validate_and_get_thresholds(
            warn_if_less_than=warn_if_less_than,
            warn_if_greater_than=warn_if_greater_than,
            warn_if_within=warn_if_within,
            warn_if_outside=warn_if_outside,
            warn_threshold_type="ABSOLUTE",
            fail_if_less_than=fail_if_less_than,
            fail_if_greater_than=fail_if_greater_than,
            fail_if_within=fail_if_within,
            fail_if_outside=fail_if_outside,
            fail_threshold_type="ABSOLUTE"
        )

        test_definition = modeltest_pb2.FairnessTest()
        test_definition.segment_id_protected.segmentation_id = segmentation_id
        test_definition.segment_id_protected.segment_name = protected_segment_name
        test_definition.segment_id_comparison.segmentation_id = segmentation_id
        if comparison_segment_name:
            test_definition.segment_id_comparison.segment_name = comparison_segment_name
        test_definition.fairness_metric_and_threshold.bias_type = _PBBiasType.Type.Value(
            metric
        )
        if threshold_warning:
            test_definition.fairness_metric_and_threshold.threshold_warning.CopyFrom(
                threshold_warning
            )
        if threshold_fail:
            test_definition.fairness_metric_and_threshold.threshold_fail.CopyFrom(
                threshold_fail
            )
        request.test_definition.CopyFrom(test_definition)
        try:
            response = self.communicator.create_fairness_test(request)
        except AlreadyExistsError as e:
            raise AlreadyExistsError(
                f"The specified fairness test already exists. Set `overwrite=True` to overwrite the test parameters."
            ) from e
        return response.test_id

    def delete_model_test(
        self,
        project_id: str,
        test_id: str,
        as_json: bool = False
    ) -> Union[Mapping, modeltest_pb2.ModelTest]:
        request = modeltest_service_pb2.DeleteModelTestRequest(
            project_id=project_id, test_id=test_id
        )
        response = self.communicator.delete_model_test(request)
        if as_json:
            MessageToDict(
                response.deleted_test,
                including_default_value_fields=True,
                preserving_proto_field_name=True
            )
        return response.deleted_test

    def get_model_tests(
        self,
        project_id: str,
        *,
        model_test_type: Optional[modeltest_pb2.ModelTestType] = None,
        data_collection_id: Optional[str] = None,
        split_id: Optional[str] = None,
        segmentation_id: Optional[str] = None,
        segment_name: Optional[str] = None,
        metric: Optional[str] = None,
        test_id: Optional[str] = None,
        as_json: bool = False
    ) -> Union[Sequence[Mapping], Sequence[modeltest_pb2.ModelTest]]:
        if segment_name:
            if not segmentation_id:
                raise ValueError(
                    "Need to provide segment group to be able to filter results by `segment_name`."
                )
        request = modeltest_service_pb2.GetModelTestsRequest(
            project_id=project_id,
            test_type=model_test_type,
            data_collection_id=data_collection_id,
            split_id=split_id,
            test_id=test_id,
        )
        model_tests = self.communicator.get_model_tests(request).model_tests
        if segmentation_id:
            model_tests = [
                i for i in model_tests
                if i.segment_id.segmentation_id == segmentation_id
            ]
            if segment_name:
                model_tests = [
                    i for i in model_tests
                    if i.segment_id.segment_name == segment_name
                ]
        if metric:
            if not model_test_type:
                raise ValueError(
                    "Need to provide `model_test_type` to be able to filter results by `metric`."
                )
            if model_test_type == modeltest_pb2.ModelTestType.MODEL_TEST_TYPE_PERFORMANCE:
                # pylint: disable=protobuf-enum-value
                metric_enum = _PBAccuracyType.Type.Value(metric)
                model_tests = [
                    i for i in model_tests
                    if i.performance_test.performance_metric_and_threshold.
                    accuracy_type == metric_enum
                ]
            elif model_test_type == modeltest_pb2.ModelTestType.MODEL_TEST_TYPE_FAIRNESS:
                # pylint: disable=protobuf-enum-value
                metric_enum = _PBBiasType.Type.Value(metric)
                model_tests = [
                    i for i in model_tests
                    if i.fairness_test.fairness_metric_and_threshold.bias_type
                    == metric_enum
                ]
            elif model_test_type == modeltest_pb2.ModelTestType.MODEL_TEST_TYPE_STABILITY:
                # pylint: disable=protobuf-enum-value
                metric_enum = _PBDistanceType.Value(metric)
                model_tests = [
                    i for i in model_tests if i.stability_test.
                    stability_metric_and_threshold.distance_type == metric_enum
                ]

        if as_json:
            return [
                MessageToDict(
                    i,
                    including_default_value_fields=True,
                    preserving_proto_field_name=True
                ) for i in model_tests
            ]
        return model_tests

    def delete_model_tests_for_split(
        self,
        project_id: str,
        split_id: str,
        as_json: bool = False
    ) -> Union[Sequence[Mapping], Sequence[modeltest_pb2.ModelTest]]:
        request = modeltest_service_pb2.DeleteModelTestsForSplitRequest(
            project_id=project_id, split_id=split_id
        )
        response = self.communicator.delete_model_test_for_split(request)
        if as_json:
            return [
                MessageToDict(
                    i,
                    including_default_value_fields=True,
                    preserving_proto_field_name=True
                ) for i in response.deleted_tests
            ]
        return response.deleted_tests

    def _wait_for_model_test_results(
        self,
        project_id: str,
        model_id: str,
        test_type: Optional[modeltest_pb2.ModelTestType] = None,
        split_id: Optional[str] = None,
        wait: bool = True
    ):
        request = modeltest_service_pb2.GetTestResultsForModelRequest(
            project_id=project_id,
            model_id=model_id,
            test_type=test_type,
            split_id=split_id
        )
        request_func = lambda: self.communicator.get_test_results_for_model(
            request
        )
        if wait:
            return self._wait_till_complete(request_func, timeout=None)
        else:
            return request_func()

    def get_test_results_for_model(
        self,
        project_id: str,
        model_id: str,
        *,
        test_type: Optional[modeltest_pb2.ModelTestType] = None,
        split_id: Optional[str] = None,
        as_json: bool = False,
        wait: bool = True
    ) -> modeltest_service_pb2.GetTestResultsForModelResponse:

        resp = self._wait_for_model_test_results(
            project_id,
            model_id=model_id,
            test_type=test_type,
            split_id=split_id,
            wait=wait
        )
        if as_json:
            return MessageToDict(
                resp,
                including_default_value_fields=True,
                preserving_proto_field_name=True
            )
        return resp

    def _wait_till_complete(
        self, request_func: Callable, timeout: Optional[float] = None
    ):
        time_start = time.time()
        ret = request_func()
        initial_pending_count = len(
            set(ret.pending_operations.waiting_on_operation_ids)
        )
        if initial_pending_count == 0:
            return ret
        with AbsoluteProgressBars() as progress_bars:
            while (timeout is None) or (time.time() - time_start < timeout):
                ret = request_func()
                cur_pending_count = len(
                    set(ret.pending_operations.waiting_on_operation_ids)
                )
                percentages = {
                    'status':
                        (initial_pending_count - cur_pending_count) /
                        initial_pending_count * 100
                }
                progress_bars.set_percentages(percentages)
                if cur_pending_count == 0:
                    return ret
                time.sleep(1)
            raise TimeoutExceededException(timeout)
