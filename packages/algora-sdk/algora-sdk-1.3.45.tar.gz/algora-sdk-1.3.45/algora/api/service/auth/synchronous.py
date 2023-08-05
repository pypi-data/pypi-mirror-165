"""
Auth API requests.
"""
from typing import Optional

import requests
from requests import Response

from algora.api.service.auth.__util import _login_request_info, _refresh_token_request_info


def login(username: str, password: str, scope: Optional[str] = None) -> Response:
    """
    Login.

    Args:
        username (str): Username
        password (str): Password
        scope (Optional[str]): Token scope, such as 'offline_access'

    Returns:
        dict: Authentication/authorization response
    """
    request_info = _login_request_info(username, password, scope)
    return requests.post(**request_info)


def refresh_token(token: Optional[str]) -> Response:
    """
    Refresh token. To get an offline access token, initial authentication (login) needs to use the scope
    'offline_access', then an offline token can be created using the refresh_token in the authentication response.
    [Stack overflow reference](https://stackoverflow.com/questions/69207734/keycloak-offline-access-token-with-refresh-token-grant-type).

    Args:
        token (str): Refresh token

    Returns:
        dict: Authentication/authorization response
    """
    request_info = _refresh_token_request_info(token)
    return requests.post(**request_info)
