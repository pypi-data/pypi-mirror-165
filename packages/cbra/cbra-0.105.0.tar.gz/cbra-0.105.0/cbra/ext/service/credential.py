# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import logging

import httpx
from cbra.ext.oauth2.types import TokenResponse


class Credential:
    """Represents an access token for a specific resource server."""
    access_token: str
    expires_in: int
    logger: logging.Logger = logging.getLogger("uvicorn")
    CannotObtainCredential: type[Exception] = type('CannotObtainCredential', (Exception,), {})

    @classmethod
    async def obtain(
        cls,
        http: httpx.AsyncClient,
        token_endpoint: str,
        client_id: str,
        assertion: str,
        scope: set[str]
    ):
        response = await http.post( # type: ignore
            url=token_endpoint,
            json={
                'grant_type': 'client_credentials',
                'client_assertion_type': 'urn:ietf:params:oauth:client-assertion-type:jwt-bearer',
                'client_assertion': assertion,
                'client_id': client_id,
                'scope': str.join(' ', sorted(scope))
            }
        )
        if response.status_code != 200:
            Credential.logger.critical(
                "Received non-200 response from %s: %s",
                token_endpoint, response.content[:256]
            )
            raise Credential.CannotObtainCredential
        token_response = TokenResponse.parse_obj(response.json())
        return cls(
            token_response.access_token,
            expires_in=token_response.expires_in
        )

    def __init__(
        self,
        access_token: str,
        expires_in: int
    ):
        self.access_token = access_token
        self.expires_in = expires_in

    