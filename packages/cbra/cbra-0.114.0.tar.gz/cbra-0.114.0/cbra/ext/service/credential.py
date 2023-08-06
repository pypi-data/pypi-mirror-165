# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import logging
from typing import Callable
from typing import Coroutine

import httpx
from cbra.ext.oauth2.types import TokenResponse


class Credential:
    """Represents an access token for a specific resource server."""
    access_token: str
    assertion_factory: Callable[..., Coroutine[None, None, str]]
    client_id: str
    expires_in: int
    http: httpx.AsyncClient
    logger: logging.Logger = logging.getLogger("uvicorn")
    resource: str | None
    scope: set[str]
    CannotObtainCredential: type[Exception] = type('CannotObtainCredential', (Exception,), {})

    @staticmethod
    async def grant(
        http: httpx.AsyncClient,
        token_endpoint: str,
        client_id: str,
        assertion: str,
        scope: set[str],
        resource: str | None = None
    ) -> TokenResponse:
        """Invoke the token endpoint to obtain an access token."""
        params: dict[str, str] = {
            'grant_type': 'client_credentials',
            'client_assertion_type': 'urn:ietf:params:oauth:client-assertion-type:jwt-bearer',
            'client_assertion': assertion,
            'client_id': client_id,
            'scope': str.join(' ', sorted(scope)),
        }
        if resource is not None:
            params['resource'] = resource
        response = await http.post(url=token_endpoint, json=params) # type: ignore
        if response.status_code != 200:
            Credential.logger.critical(
                "Received non-200 response from %s: %s",
                token_endpoint, response.content[:256]
            )
            raise Credential.CannotObtainCredential(response.content[:256])
        return TokenResponse.parse_obj(response.json())

    @classmethod
    async def obtain(
        cls,
        http: httpx.AsyncClient,
        token_endpoint: str,
        client_id: str,
        assertion_factory: Callable[..., Coroutine[None, None, str]],
        scope: set[str],
        resource: str | None = None
    ) -> 'Credential':
        response = await Credential.grant(
            http=http,
            token_endpoint=token_endpoint,
            client_id=client_id,
            assertion=await assertion_factory(),
            scope=scope,
            resource=resource
        )
        return cls(
            client_id=client_id,
            access_token=response.access_token,
            expires_in=response.expires_in,
            http=http,
            assertion_factory=assertion_factory,
            scope=scope,
            resource=resource
        )

    def __init__(
        self,
        *,
        client_id: str,
        access_token: str,
        expires_in: int,
        http: httpx.AsyncClient,
        assertion_factory: Callable[..., Coroutine[None, None, str]],
        scope: set[str],
        resource: str | None = None
    ):
        self.access_token = access_token
        self.assertion_factory = assertion_factory
        self.client_id = client_id
        self.expires_in = expires_in
        self.http = http
        self.resource = resource
        self.scope = scope

    def __str__(self) -> str:
        return self.access_token

    