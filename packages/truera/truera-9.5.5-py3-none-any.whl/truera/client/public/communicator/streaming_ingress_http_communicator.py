import logging
from typing import Union

from truera.client.public.auth_details import AuthDetails
from truera.client.public.communicator.http_communicator import \
    HttpCommunicator
from truera.client.public.communicator.streaming_ingress_communicator import \
    StreamingIngressServiceCommunicator
from truera.protobuf.public.streaming import \
    streaming_ingress_service_pb2 as si_pb


class HttpStreamingIngressServiceCommunicator(
    StreamingIngressServiceCommunicator
):

    def __init__(
        self,
        connection_string: str,
        auth_details: AuthDetails,
        logger: logging.Logger,
        *,
        verify_cert: Union[bool, str] = True
    ):
        connection_string = connection_string.rstrip("/")
        self.connection_string = f"{connection_string}/api/v0/ingest"
        self.http_communcatior = HttpCommunicator(
            connection_string=self.connection_string,
            auth_details=auth_details,
            logger=logger,
            verify_cert=verify_cert
        )
        self.http_communcatior.__not_supported_message = "RPC not supported via HTTP client"

    def ping(self, req: si_pb.PingRequest) -> si_pb.PingResponse:
        uri = f"{self.connection_string}/streaming/ping"
        json_req = self.http_communcatior._proto_to_json(req)
        json_resp = self.http_communcatior.get_request(uri, json_req)
        return self.http_communcatior._json_to_proto(
            json_resp, si_pb.PingResponse()
        )

    def ingest_point(
        self, req: si_pb.IngestPointRequest
    ) -> si_pb.IngestPointResponse:
        uri = f"{self.connection_string}/streaming/point"
        json_req = self.http_communcatior._proto_to_json(req)
        json_resp = self.http_communcatior.post_request(uri, json_req)
        return self.http_communcatior._json_to_proto(
            json_resp, si_pb.IngestPointResponse()
        )

    def close(self):
        self.http_communcatior.close()
