import logging
from typing import Union

from truera.client.public.auth_details import AuthDetails
from truera.client.public.communicator.http_communicator import \
    HttpCommunicator
from truera.client.public.communicator.user_manager_service_communicator import \
    UserManagerServiceCommunicator
from truera.protobuf.rbac import rbac_pb2 as rbac_pb


class HttpUserManagerServiceCommunicator(
    HttpCommunicator, UserManagerServiceCommunicator
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
        self.connection_string = f"{connection_string}/api/usermanager"
        self.http_communicator = HttpCommunicator(
            connection_string=self.connection_string,
            auth_details=auth_details,
            logger=logger,
            verify_cert=verify_cert
        )

    def add_user_as_admin(
        self,
        req: rbac_pb.AdminRequest,
        request_context=None
    ) -> rbac_pb.AuthorizationResponse:
        uri = "{conn}/admin/{subject_id}".format(
            conn=self.connection_string, subject_id=req.subject_id
        )
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.post_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp, rbac_pb.AuthorizationResponse()
        )

    def remove_user_as_admin(
        self,
        req: rbac_pb.AdminRequest,
        request_context=None
    ) -> rbac_pb.AuthorizationResponse:
        uri = "{conn}/admin/{subject_id}".format(
            conn=self.connection_string, subject_id=req.subject_id
        )
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.delete_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp, rbac_pb.AuthorizationResponse()
        )

    def add_user(
        self,
        req: rbac_pb.AddUserRequest,
        request_context=None
    ) -> rbac_pb.AuthorizationResponse:
        uri = "{conn}/user/{user_id}".format(
            conn=self.connection_string, user_id=req.user.id
        )
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.post_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp, rbac_pb.AuthorizationResponse()
        )

    def get_users(
        self,
        req: rbac_pb.GetUsersFilter,
        request_context=None
    ) -> rbac_pb.GetUsersResponse:
        uri = "{conn}/user".format(conn=self.connection_string)
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.get_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp, rbac_pb.GetUsersResponse()
        )

    def auto_add_user(
        self,
        req: rbac_pb.AutoUserRequest,
        request_context=None
    ) -> rbac_pb.GetUsersResponse:
        uri = "{conn}/user:auto".format(conn=self.connection_string)
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.post_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp, rbac_pb.GetUsersResponse()
        )

    def add_user_to_project(
        self,
        req: rbac_pb.UserProjectRequest,
        request_context=None
    ) -> rbac_pb.AuthorizationResponse:
        uri = "{conn}/user/{subject_id}/project/{project_id}".format(
            conn=self.connection_string,
            subject_id=req.subject_id,
            project_id=req.project_id
        )
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.post_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp, rbac_pb.AuthorizationResponse()
        )

    def remove_user_from_project(
        self,
        req: rbac_pb.UserProjectRequest,
        request_context=None
    ) -> rbac_pb.AuthorizationResponse:
        uri = "{conn}/user/{subject_id}/project/{project_id}".format(
            conn=self.connection_string,
            subject_id=req.subject_id,
            project_id=req.project_id
        )
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.delete_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp, rbac_pb.AuthorizationResponse()
        )

    def authorize_create_project(
        self,
        req: rbac_pb.ProjectRequest,
        request_context=None
    ) -> rbac_pb.AuthorizationResponse:
        uri = "{conn}/user/project/{project_id}".format(
            conn=self.connection_string, project_id=req.project_id
        )
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.post_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp, rbac_pb.AuthorizationResponse()
        )

    def authorize_archive_project(
        self,
        req: rbac_pb.ProjectRequest,
        request_context=None
    ) -> rbac_pb.AuthorizationResponse:
        uri = "{conn}/user/project/{project_id}".format(
            conn=self.connection_string, project_id=req.project_id
        )
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.delete_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp, rbac_pb.AuthorizationResponse()
        )

    def accept_user_terms_of_service(
        self,
        req: rbac_pb.AutoUserRequest,
        request_context=None
    ) -> rbac_pb.GetUsersResponse:
        uri = "{conn}/user:accept_terms_of_service".format(
            conn=self.connection_string
        )
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.post_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp, rbac_pb.GetUsersResponse()
        )
