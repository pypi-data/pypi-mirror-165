from base64 import b64encode
from typing import Sequence, Tuple, Union


def format_headers(func):

    def wrapper(self, use_http: bool = False):
        headers = func(self)
        return dict(headers) if use_http else headers

    return wrapper


class AuthDetails(object):

    def __init__(self, **kwargs):
        self.username = kwargs.get("username", None)
        self.password = kwargs.get("password", None)
        self.token = kwargs.get("token", None)
        # works only within TruEra cluster
        self.impersonation_metadata = kwargs.get("impersonation_metadata", None)

    @format_headers
    def get_auth_headers(
        self, use_http: bool = False
    ) -> Union[dict, Sequence[Tuple]]:
        if self.username and self.password:
            user_pass_bytes = bytes(
                "{}:{}".format(self.username, self.password), 'utf-8'
            )
            user_pass_b64_encoded = b64encode(user_pass_bytes).decode("ascii")
            # Note: For grpc metadata, the keys must be lower case. Http requests perform this conversion automatically.
            return [('authorization', "Basic {}".format(user_pass_b64_encoded))]

        if self.token:
            return [('authorization', f"Bearer {self.token}")]

        return self.impersonation_metadata or []
