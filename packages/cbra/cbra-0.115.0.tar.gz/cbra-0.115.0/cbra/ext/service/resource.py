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

from .credential import Credential


class Resource:
    """Provides an interface to interace with a resource server."""
    __module__: str = 'cbra.ext.service'
    credential: Credential
    http: httpx.AsyncClient
    logger: logging.Logger = logging.getLogger("uvicorn")
    server: str

    def __init__(
        self,
        *,
        server: str,
        credential: Credential
    ):
        if str.endswith(server, '/'):
            raise ValueError("The `server` parameter must not end with a slash.")
        self.credential = credential
        self.http = httpx.AsyncClient(base_url=server)
        self.server = server

    async def connect(self) -> None:
        """Setup the HTTP client for the specified resource server."""
        await self.http.__aenter__()
        self.logger.info("Connected to resource server %s", self.server)

    async def close(self) -> None:
        """Close the HTTP connection to the resource server."""
        await self.http.__aexit__(None, None, None)
        self.logger.info("Closed connection to resource server %s", self.server)

    async def request(
        self,
        *,
        method: str,
        path: str,
        headers: dict[str, str] | None = None
    ) -> httpx.Response:
        if not str.startswith(path, '/'):
            raise ValueError("Path must start with a slash.")
        response = await self.http.request( # type: ignore
            method=method,
            url=path,
            headers={
                'Authorization': f'Bearer {self.credential}',
                **(headers or {})
            }
        )
        return response