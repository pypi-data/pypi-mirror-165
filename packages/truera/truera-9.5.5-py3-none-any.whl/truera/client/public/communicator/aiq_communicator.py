from abc import ABC
from abc import abstractmethod
from typing import Iterator

from truera.protobuf.public.aiq import intelligence_service_pb2 as is_pb


class AiqCommunicator(ABC):

    @abstractmethod
    def get_model_predictions(
        self, req: is_pb.ModelPredictionsRequest
    ) -> Iterator[is_pb.ModelPredictionsResponse]:
        pass

    @abstractmethod
    def get_model_influences(
        self, req: is_pb.ModelInfluencesRequest
    ) -> Iterator[is_pb.ModelInfluencesResponse]:
        pass

    @abstractmethod
    def get_model_data(
        self, req: is_pb.ModelDataRequest
    ) -> Iterator[is_pb.ModelDataResponse]:
        pass

    @abstractmethod
    def get_partial_dependence_plot(
        self, req: is_pb.PartialDependencePlotRequest
    ) -> Iterator[is_pb.PartialDependencePlotResponse]:
        pass

    @abstractmethod
    def get_split_data(
        self, req: is_pb.ModelDataRequest
    ) -> Iterator[is_pb.ModelDataResponse]:
        pass

    @abstractmethod
    def compute_accuracy(
        self, req: is_pb.AccuracyRequest
    ) -> Iterator[is_pb.AccuracyResponse]:
        pass

    @abstractmethod
    def compute_batched_accuracy(
        self, req: is_pb.BatchAccuracyRequest
    ) -> Iterator[is_pb.BatchAccuracyResponse]:
        pass

    @abstractmethod
    def compute_model_score_instability(
        self, req: is_pb.CompareModelOutputRequest
    ) -> Iterator[is_pb.CompareModelOutputResponse]:
        pass

    @abstractmethod
    def compute_feature_drift(
        self, req: is_pb.FeatureDriftRequest
    ) -> Iterator[is_pb.FeatureDriftResponse]:
        pass

    @abstractmethod
    def update_manual_segmentation(
        self, req: is_pb.UpdateManualSegmentationRequest
    ) -> Iterator[is_pb.UpdateManualSegmentationResponse]:
        pass

    @abstractmethod
    def get_interesting_segments(
        self, req: is_pb.InterestingSegmentsRequest
    ) -> Iterator[is_pb.InterestingSegmentsResponse]:
        pass
