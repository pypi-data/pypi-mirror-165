from typing import Optional


def _login_request_info(username: str, password: str, scope: Optional[str] = None) -> dict:
    return {
        "url": f"https://auth.algoralabs.com/auth/realms/production/protocol/openid-connect/token",
        "data": {
            "client_id": "algora-api",
            "scope": scope,
            "grant_type": "password",
            "username": username,
            "password": password
        }
    }


def _refresh_token_request_info(refresh_token: Optional[str] = None) -> dict:
    return {
        "url": f"https://auth.algoralabs.com/auth/realms/production/protocol/openid-connect/token",
        "data": {
            "client_id": "algora-api",
            "grant_type": "refresh_token",
            "refresh_token": refresh_token
        }
    }
