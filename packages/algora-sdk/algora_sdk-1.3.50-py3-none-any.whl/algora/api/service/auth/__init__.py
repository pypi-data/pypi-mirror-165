"""
Auth API.
"""
from algora.api.service.auth.asynchronous import (
    async_login, async_refresh_token
)
from algora.api.service.auth.synchronous import (
    login, refresh_token
)
