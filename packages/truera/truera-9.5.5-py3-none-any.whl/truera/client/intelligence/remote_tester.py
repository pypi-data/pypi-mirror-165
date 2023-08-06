from __future__ import annotations

import logging
from typing import Any, Mapping, Optional, Sequence, Tuple, TYPE_CHECKING

from truera.client.errors import MetadataNotFoundException
from truera.client.errors import NotFoundError
from truera.client.intelligence.model_tests import ModelTestDetails
from truera.client.intelligence.model_tests import ModelTestLeaderboard
from truera.client.intelligence.model_tests import ModelTestResults
from truera.client.intelligence.tester import SUPPORTED_TEST_TYPES
from truera.client.intelligence.tester import Tester
from truera.client.services.artifactrepo_client import ArtifactMetaFetchMode
from truera.client.services.model_test_client import ModelTestClient
from truera.protobuf.public.aiq.intelligence_service_pb2 import BiasType
from truera.utils import accuracy_utils

if TYPE_CHECKING:
    from truera.client.intelligence.segment import SegmentGroup
    from truera.client.public.auth_details import AuthDetails
    from truera.client.remote_truera_workspace import RemoteTrueraWorkspace
    from truera.client.services.artifact_interaction_client import \
        ArtifactInteractionClient


class RemoteTester(Tester):

    def __init__(
        self, workspace: RemoteTrueraWorkspace,
        artifact_interaction_client: ArtifactInteractionClient,
        connection_string: str, auth_details: AuthDetails, verify_cert: bool
    ) -> None:
        self._logger = logging.getLogger(__name__)
        self._workspace = workspace
        self.artifact_interaction_client = artifact_interaction_client
        self.model_test_client = ModelTestClient(
            connection_string=connection_string,
            auth_details=auth_details,
            use_http=True,
            verify_cert=verify_cert
        )
        self.connection_string = connection_string
        self._split_id_to_name_cache: Mapping[str, str] = {}

    def _get_split_name_from_id(
        self, project_name: str, data_collection_name: str, split_id: str
    ) -> str:
        if not split_id:
            return ""
        if split_id not in self._split_id_to_name_cache:
            # devnote: this will overwrite existing cache entries for other projects, but that is ok.
            self._split_id_to_name_cache = {
                pair["id"]: pair["name"]
                for pair in self.artifact_interaction_client.
                get_all_datasplits_in_data_collection(
                    project_name, data_collection_name, fetch_metadata=True
                )["name_id_pairs"]
            }
        return self._split_id_to_name_cache.get(split_id)

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
        project_name = self._workspace._ensure_project()
        self._workspace._ensure_data_collection()
        valid_metrics = []
        if self._workspace._get_output_type() == "classification":
            valid_metrics = accuracy_utils.BINARY_CLASSIFICATION_SCORE_ACCURACIES_STR + accuracy_utils.MULTICLASS_CLASSIFICATION_SCORE_ACCURACIES_STR + accuracy_utils.CLASSIFICATION_SCORE_ACCURACIES_STR + accuracy_utils.PROBITS_OR_LOGITS_SCORE_ACCURACIES_STR
        elif self._workspace._get_output_type() == "regression":
            valid_metrics = accuracy_utils.REGRESSION_SCORE_ACCURACIES_STR
        if metric not in valid_metrics:
            raise ValueError(
                f"Only the following metrics are allowed for projects with \"{self._workspace._get_output_type()}\" output type: {valid_metrics}"
            )
        if (
            warn_threshold_type == "RELATIVE" or
            fail_threshold_type == "RELATIVE"
        ) and (reference_model_name and reference_split_name):
            raise ValueError(
                "Please only provide one of `reference_model_name` or `reference_split_name` for relative test threshold, but not both!"
            )
        data_split_id = self._get_split_id(data_split_name)
        segmentation_id = None
        if segment_group_name:
            segmentation_id = self._get_segment_group_id(segment_group_name)

        reference_split_id = None
        if reference_split_name:
            reference_split_id = self._get_split_id(reference_split_name)
        reference_model_id = None
        if reference_model_name:
            reference_model_id = self.artifact_interaction_client.get_model_metadata(
                project_name, model_name=reference_model_name
            )["id"]

        # TODO: AB #6899 (expose this as function params when we support autorun of tests)
        autorun: bool = False

        self.model_test_client.create_performance_test(
            project_id=self._workspace.project.id,
            split_id=data_split_id,
            segmentation_id=segmentation_id,
            segment_name=segment_name,
            metric=metric,
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
            reference_model_id=reference_model_id,
            autorun=autorun,
            overwrite=overwrite
        )

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
        self._workspace._ensure_project()
        self._workspace._ensure_data_collection()
        valid_metrics = [
            "NUMERICAL_WASSERSTEIN", "DIFFERENCE_OF_MEAN",
            "NUMERICAL_POPULATION_STABILITY_INDEX"
        ]
        if metric not in valid_metrics:
            raise ValueError(
                f"Invalid `metric` \"{metric}\"! Only the following metrics are allowed: {valid_metrics}"
            )
        comparison_data_split_id = self._get_split_id(
            comparison_data_split_name
        )
        base_data_split_id = None
        if base_data_split_name:
            base_data_split_id = self._get_split_id(base_data_split_name)
        segmentation_id = None
        if segment_group_name:
            segmentation_id = self._get_segment_group_id(segment_group_name)

        # TODO: AB #6899 (expose this as function params when we support autorun of tests)
        autorun: bool = False
        self.model_test_client.create_stability_test(
            project_id=self._workspace.project.id,
            comparison_data_split_id=comparison_data_split_id,
            base_data_split_id=base_data_split_id,
            metric=metric,
            segmentation_id=segmentation_id,
            segment_name=segment_name,
            warn_if_less_than=warn_if_less_than,
            warn_if_greater_than=warn_if_greater_than,
            warn_if_within=warn_if_within,
            warn_if_outside=warn_if_outside,
            fail_if_less_than=fail_if_less_than,
            fail_if_greater_than=fail_if_greater_than,
            fail_if_within=fail_if_within,
            fail_if_outside=fail_if_outside,
            autorun=autorun,
            overwrite=overwrite
        )

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
        self._workspace._ensure_project()
        self._workspace._ensure_data_collection()
        valid_metrics = [
            curr for curr in BiasType.Type.keys() if curr != "UNKNOWN"
        ]
        if metric not in valid_metrics:
            raise ValueError(
                f"Only the following metrics are allowed: {valid_metrics}"
            )
        data_split_id = self._get_split_id(data_split_name)
        segmentation_id = self._get_segment_group_id(segment_group_name)

        # TODO: AB #6899 (expose this as function params when we support autorun of tests)
        autorun: bool = False
        self.model_test_client.create_fairness_test(
            project_id=self._workspace.project.id,
            split_id=data_split_id,
            segmentation_id=segmentation_id,
            protected_segment_name=protected_segment_name,
            comparison_segment_name=comparison_segment_name,
            metric=metric,
            warn_if_less_than=warn_if_less_than,
            warn_if_greater_than=warn_if_greater_than,
            warn_if_within=warn_if_within,
            warn_if_outside=warn_if_outside,
            fail_if_less_than=fail_if_less_than,
            fail_if_greater_than=fail_if_greater_than,
            fail_if_within=fail_if_within,
            fail_if_outside=fail_if_outside,
            autorun=autorun,
            overwrite=overwrite
        )

    def get_model_tests(
        self, data_split_name: Optional[str] = None
    ) -> ModelTestDetails:
        project_name = self._workspace._ensure_project()
        data_collection_name = self._workspace._ensure_data_collection()
        data_collection_id = self._workspace.data_collection.id
        data_split_id = None
        if data_split_name:
            data_split_id = self._get_split_id(data_split_name)
        # getting the result as dict since the float values in the native proto instance actually looks weird
        model_tests = self.model_test_client.get_model_tests(
            self._workspace.project.id,
            data_collection_id=data_collection_id,
            split_id=data_split_id,
            as_json=True
        )
        self._resolve_metadata_for_model_tests(
            project_name, data_collection_name, model_tests
        )
        return ModelTestDetails(model_tests)

    def get_model_test_results(
        self,
        data_split_name: Optional[str] = None,
        comparison_models: Optional[Sequence[str]] = None,
        test_types: Optional[Sequence[str]] = None,
        wait: bool = True
    ) -> ModelTestResults:
        project_name = self._workspace._ensure_project()
        data_collection_name = self._workspace._ensure_data_collection()
        self._workspace._ensure_model()
        test_types = self._validate_test_types(test_types)
        if comparison_models:
            existing_models = self.artifact_interaction_client.get_all_models_in_project(
                project_id=self._workspace.project.id,
                data_collection_name=self._workspace.
                _get_current_active_data_collection_name(),
                ar_meta_fetch_mode=ArtifactMetaFetchMode.ALL
            )["name_id_pairs"]
            model_name_to_id = {
                model["name"]: model["id"] for model in existing_models
            }
            for model_name in comparison_models:
                if model_name not in model_name_to_id:
                    raise ValueError(
                        f"Could not find model {model_name} in project {self._workspace._get_current_active_project_name()}"
                    )
            comparison_models = [
                {
                    "name": model_name,
                    "id": model_name_to_id[model_name]
                } for model_name in comparison_models
            ]
        else:
            comparison_models = []

        data_split_id = None
        if data_split_name:
            data_split_id = self._get_split_id(data_split_name)
        test_results = self.model_test_client.get_test_results_for_model(
            project_id=self._workspace.project.id,
            model_id=self._workspace.model.model_id,
            split_id=data_split_id,
            wait=wait,
            as_json=True
        )

        comparison_models_test_results = [
            self.model_test_client.get_test_results_for_model(
                project_id=self._workspace.project.id,
                model_id=model["id"],
                split_id=data_split_id,
                wait=wait,
                as_json=True
            ) for model in comparison_models
        ]
        for test_type in test_types:
            results_type = f"{test_type}_test_results"
            model_tests = [
                t["test_details"] for t in test_results[results_type]
            ]
            self._resolve_metadata_for_model_tests(
                project_name, data_collection_name, model_tests
            )
            for i in range(len(comparison_models_test_results)):
                model_tests = [
                    t["test_details"]
                    for t in comparison_models_test_results[i][results_type]
                ]
                self._resolve_metadata_for_model_tests(
                    project_name, data_collection_name, model_tests
                )
        return ModelTestResults(
            self._workspace._get_current_active_project_name(),
            self._workspace._get_current_active_model_name(),
            self._workspace.model.model_id,
            test_results,
            test_types,
            connection_string=self._workspace.connection_string,
            comparison_models=comparison_models,
            comparison_models_test_results=comparison_models_test_results
        )

    def get_model_leaderboard(
        self,
        sort_by: str = "performance",
        wait: bool = True
    ) -> ModelTestLeaderboard:
        if sort_by not in Tester.TEST_TYPE_STRING_TO_MODEL_TEST_TYPE_ENUM:
            raise ValueError(
                f"`sort_by` must be one of {Tester.TEST_TYPE_STRING_TO_MODEL_TEST_TYPE_ENUM.keys()}!"
            )
        project_name = self._workspace._ensure_project()
        data_collection_name = self._workspace._ensure_data_collection()
        all_model_metadata = {
            model_metadata["name"]: model_metadata for model_metadata in
            self.artifact_interaction_client.get_all_model_metadata_in_project(
                project_id=self._workspace.project.id,
                data_collection_id=self._workspace.data_collection.id
            )
        }
        for model in all_model_metadata:
            training_metadata = all_model_metadata[model]["training_metadata"]
            training_metadata["train_split_name"
                             ] = self._get_split_name_from_id(
                                 project_name, data_collection_name,
                                 training_metadata["train_split_id"]
                             )
        test_results = {
            model: self.model_test_client.get_test_results_for_model(
                project_id=self._workspace.project.id,
                model_id=all_model_metadata[model]["id"],
                wait=wait,
                as_json=True
            ) for model in list(all_model_metadata.keys())
        }

        for model_name in test_results:
            model_tests = []
            for test_type in SUPPORTED_TEST_TYPES:
                results_type = f"{test_type}_test_results"
                model_tests.extend(
                    [
                        t["test_details"]
                        for t in test_results[model_name][results_type]
                    ]
                )
            self._resolve_metadata_for_model_tests(
                project_name,
                data_collection_name,
                model_tests,
                resolve_segment_definitions=False
            )
            test_results[model_name] = ModelTestResults(
                project_name,
                model_name,
                all_model_metadata[model]["id"],
                test_results[model_name],
                SUPPORTED_TEST_TYPES,
                connection_string=self._workspace.connection_string
            )

        return ModelTestLeaderboard(
            test_results=test_results,
            models_metadata=all_model_metadata,
            data_collection_name=data_collection_name,
            sort_by=sort_by
        )

    def delete_tests(
        self,
        test_type: Optional[str] = None,
        data_split_name: Optional[str] = None,
        segment_group_name: Optional[str] = None,
        segment_name: Optional[str] = None,
        metric: Optional[str] = None
    ) -> None:
        self._workspace._ensure_project()
        data_collection_name = self._workspace._ensure_data_collection()
        if test_type and test_type not in Tester.TEST_TYPE_STRING_TO_MODEL_TEST_TYPE_ENUM:
            raise ValueError(
                f"`test_type` must be one of {Tester.TEST_TYPE_STRING_TO_MODEL_TEST_TYPE_ENUM.keys()} or `None`!"
            )
        data_collection_id = self._workspace.data_collection.id
        data_split_id = None
        if data_split_name:
            data_split_id = self._get_split_id(data_split_name)
        segmentation_id = None
        if segment_group_name:
            segmentation_id = self._get_segment_group_id(segment_group_name)
        model_test_type = None
        if test_type:
            model_test_type = Tester.TEST_TYPE_STRING_TO_MODEL_TEST_TYPE_ENUM[
                test_type]
        model_tests = self.model_test_client.get_model_tests(
            project_id=self._workspace.project.id,
            model_test_type=model_test_type,
            data_collection_id=data_collection_id,
            split_id=data_split_id,
            segmentation_id=segmentation_id,
            segment_name=segment_name,
            metric=metric,
            as_json=True
        )
        for test_proto in model_tests:
            self.model_test_client.delete_model_test(
                project_id=self._workspace.project.id, test_id=test_proto["id"]
            )

    def _resolve_metadata_for_model_tests(
        self,
        project_name: str,
        data_collection_name: str,
        model_tests: Sequence[Mapping],
        resolve_segment_definitions: bool = True
    ) -> None:
        self._resolve_split_names_for_model_tests(
            project_name, data_collection_name, model_tests
        )
        if resolve_segment_definitions:
            self._resolve_segment_and_threshold_definitions_for_model_tests(
                model_tests
            )

    def _resolve_split_names_for_model_tests(
        self, project_name: str, data_collection_name: str,
        model_tests: Sequence[Mapping]
    ) -> None:
        for model_test in model_tests:
            model_test["split_name"] = self._get_split_name_from_id(
                project_name, data_collection_name, model_test["split_id"]
            )
            if "stability_test" in model_test:
                stability_test = model_test["stability_test"]
                stability_test["base_split_name"
                              ] = self._get_split_name_from_id(
                                  project_name, data_collection_name,
                                  stability_test["base_split_id"]
                              )

    def _resolve_segment_and_threshold_definitions_for_model_tests(
        self, model_tests: Mapping
    ):
        for model_test in model_tests:
            self._resolve_segment_and_threshold_definition_for_model_test(
                model_test
            )

    def _resolve_segment_and_threshold_definition_for_model_test(
        self, model_test: Mapping
    ) -> Mapping:
        segment_desc, segment_index = self._describe_segment(
            model_test["segment_id"]
        )
        model_test["segment_id"]["segment_desc"] = segment_desc
        model_test["segment_id"]["segment_index"] = segment_index
        performance_test = model_test.get("performance_test")
        if performance_test:
            self._resolve_comparison_reference_in_test_threshold(
                performance_test["performance_metric_and_threshold"]
                ["threshold_warning"]
            )
            self._resolve_comparison_reference_in_test_threshold(
                performance_test["performance_metric_and_threshold"]
                ["threshold_fail"]
            )
        fairness_test = model_test.get("fairness_test")
        if fairness_test:
            segment_desc, segment_index = self._describe_segment(
                fairness_test["segment_id_protected"]
            )
            model_test["fairness_test"]["segment_id_protected"]["segment_desc"
                                                               ] = segment_desc
            model_test["fairness_test"]["segment_id_protected"]["segment_index"
                                                               ] = segment_index
            segment_desc, segment_index = self._describe_segment(
                fairness_test["segment_id_comparison"]
            )
            model_test["fairness_test"]["segment_id_comparison"]["segment_desc"
                                                                ] = segment_desc
            model_test["fairness_test"]["segment_id_comparison"][
                "segment_index"] = segment_index

    def _resolve_comparison_reference_in_test_threshold(
        self, test_threshold: Mapping
    ) -> None:
        reference_split_id = test_threshold.get("reference_split_id")
        if reference_split_id:
            test_threshold[
                "reference_split_name"] = self._get_split_name_from_id(
                    self._workspace._get_current_active_project_name(),
                    self._workspace._get_current_active_data_collection_name(),
                    reference_split_id
                )
        reference_model_id = test_threshold.get("reference_model_id")
        if reference_model_id:
            test_threshold[
                "reference_model_name"
            ] = self.artifact_interaction_client.get_model_metadata(
                self._workspace.project.id, model_id=reference_model_id
            )["name"]

    def _describe_segment(
        self, segment_id_proto_as_mp: Mapping[str, Any]
    ) -> Tuple[str, Optional[int]]:
        segment_desc = "ALL POINTS"
        segment_index = None
        if segment_id_proto_as_mp["segmentation_id"]:
            sg = self._get_segment_group_from_id(
                segment_id_proto_as_mp["segmentation_id"]
            )
            segment_name = segment_id_proto_as_mp["segment_name"]
            if segment_name:
                segment_desc = f'{sg.name}--{segment_name}: {sg.get_segments()[segment_name].ingestable_definition()}'
                segment_index = self._get_segment_index(sg, segment_name)
            else:
                segment_desc = "REST OF POPULATION"
                segment_index = None

        return segment_desc, segment_index

    def _get_segment_group_from_id(self, segmentation_id: str) -> SegmentGroup:
        segment_groups = self._workspace.aiq_client.get_wrapped_segmentations(
            self._workspace.project.id, segmentation_ids=[segmentation_id]
        ).response
        if len(segment_groups) > 0:
            return next(iter(segment_groups.values()))
        raise NotFoundError(
            f"Could not find segment group with id: \"{segmentation_id}\""
        )

    def _get_segment_index(self, sg: SegmentGroup, segment_name: str) -> int:
        for i in range(len(sg._segmentation_proto.segments)):
            if sg._segmentation_proto.segments[i].name == segment_name:
                return i
        raise NotFoundError(
            f"Couldn't find segment \"{segment_name}\" in segment group \"{sg.name}\""
        )

    def _get_segment_group_id(self, segment_group_name: str) -> str:
        segment_groups = self._workspace.aiq_client.get_wrapped_segmentations(
            self._workspace.project.id
        ).response
        if segment_group_name in segment_groups:
            return segment_groups[segment_group_name].id
        raise NotFoundError(
            f"Could not find segment group with name: \"{segment_group_name}\""
        )

    def _get_split_id(self, data_split_name: str) -> str:
        try:
            return self.artifact_interaction_client.get_split_metadata(
                self._workspace._get_current_active_project_name(),
                self._workspace._get_current_active_data_collection_name(),
                data_split_name
            )["id"]
        except MetadataNotFoundException:
            raise NotFoundError(
                f"Data split \"{data_split_name}\" does not exist."
            )
