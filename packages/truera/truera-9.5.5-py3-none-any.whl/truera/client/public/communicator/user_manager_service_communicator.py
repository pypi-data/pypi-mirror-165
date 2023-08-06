from abc import ABC
from abc import abstractmethod

from truera.protobuf.rbac import rbac_pb2 as rbac_pb


class UserManagerServiceCommunicator(ABC):

    @abstractmethod
    def add_user_as_admin(
        self,
        req: rbac_pb.AdminRequest,
        request_context=None
    ) -> rbac_pb.AuthorizationResponse:
        pass

    @abstractmethod
    def remove_user_as_admin(
        self,
        req: rbac_pb.AdminRequest,
        request_context=None
    ) -> rbac_pb.AuthorizationResponse:
        pass

    @abstractmethod
    def add_user(
        self,
        req: rbac_pb.AddUserRequest,
        request_context=None
    ) -> rbac_pb.AuthorizationResponse:
        pass

    @abstractmethod
    def get_users(
        self,
        req: rbac_pb.GetUsersFilter,
        request_context=None
    ) -> rbac_pb.GetUsersResponse:
        pass

    @abstractmethod
    def auto_add_user(
        self,
        req: rbac_pb.AutoUserRequest,
        request_context=None
    ) -> rbac_pb.GetUsersResponse:
        pass

    @abstractmethod
    def add_user_to_project(
        self,
        req: rbac_pb.UserProjectRequest,
        request_context=None
    ) -> rbac_pb.AuthorizationResponse:
        pass

    @abstractmethod
    def remove_user_from_project(
        self,
        req: rbac_pb.UserProjectRequest,
        request_context=None
    ) -> rbac_pb.AuthorizationResponse:
        pass

    @abstractmethod
    def authorize_create_project(
        self,
        req: rbac_pb.ProjectRequest,
        request_context=None
    ) -> rbac_pb.AuthorizationResponse:
        pass

    @abstractmethod
    def authorize_archive_project(
        self,
        req: rbac_pb.ProjectRequest,
        request_context=None
    ) -> rbac_pb.AuthorizationResponse:
        pass

    @abstractmethod
    def accept_user_terms_of_service(
        self,
        req: rbac_pb.AutoUserRequest,
        request_context=None
    ) -> rbac_pb.GetUsersResponse:
        pass
