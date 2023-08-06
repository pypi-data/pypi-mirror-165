# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import logging
from typing import Any

import fastapi
from httpx import AsyncClient
from httpx import Response
from ckms.types import AuthorizationServerNotDiscoverable
from ckms.types import AuthorizationServerMisbehaves
from ckms.types import JSONWebKeySet
from ckms.types import ServerMetadata

from cbra.conf import settings
from cbra.utils import retry
from .credential import Credential
from .resource import Resource
from .serviceidentity import ServiceIdentity


RESOURCE_SERVERS: dict[str, Any] = getattr(settings, 'RESOURCE_SERVERS', {})


class ServiceClient:
    __module__: str = 'cbra.ext.service'
    credential: Credential | None
    http: AsyncClient
    identity: ServiceIdentity
    jwks: JSONWebKeySet | None
    logger: logging.Logger
    metadata: ServerMetadata
    server: str
    timeout: float
    resources: dict[str, Resource]

    @staticmethod
    def current(request: fastapi.Request) -> 'ServiceClient':
        return request.app.client

    def __init__(
        self,
        server: str,
        identity: ServiceIdentity,
        logger: logging.Logger | None = None,
        timeout: float = 60.0
    ):
        self.identity = identity
        self.logger = logger or logging.getLogger("uvicorn")
        self.resources = {}
        self.server = server
        self.timeout = timeout

    async def configure(self, resource: str) -> Resource:
        """Configure the named resource `resource` and return a
        :class:`~cbra.ext.service.Resource` instance.
        """
        if resource not in RESOURCE_SERVERS:
            raise ValueError(f"Resource not configured: {resource}")
        if resource not in self.resources:
            url = RESOURCE_SERVERS[resource]['server']
            self.resources[resource] = Resource(
                server=url,
                credential=await self.get_credential(
                    scope=RESOURCE_SERVERS[resource].get('scope') or set(),
                    resource=url
                )
            )
            await self.resources[resource].connect()
            self.logger.info("Configured resource server %s", url)
        return self.resources[resource]

    async def get_client_assertion(self) -> str:
        """Encode a client assertion used to authenticate with the authorization
        server.
        """
        return await self.identity.get_client_assertion(
            token_endpoint=self.metadata.token_endpoint
        )

    async def get_credential(
        self,
        scope: set[str],
        resource: str | None = None
    ) -> Credential:
        """Obtain a credential for the given resource."""
        return await Credential.obtain(
            http=self.http,
            token_endpoint=self.metadata.token_endpoint,
            client_id=self.identity.client_id,
            assertion_factory=self.get_client_assertion,
            scope=scope,
            resource=resource
        )

    @retry(6, interval=5.0)
    async def get_server_jwks(self) -> JSONWebKeySet | None:
        return await self.metadata.get_jwks(self.http)

    @retry(6, interval=5.0)
    async def get_server_metadata(self) -> ServerMetadata:
        return await ServerMetadata.discover(self.http, self.server)

    async def on_boot(self):
        try:
            self.logger.info("Booting service client")
            self.http = await AsyncClient(timeout=self.timeout).__aenter__()
            self.metadata = await self.get_server_metadata()
            self.jwks = await self.get_server_jwks()
        except AuthorizationServerNotDiscoverable:
            self.logger.fatal("Unable to discover authorization server %s", self.server)
            raise
        self.logger.info("Succesfully discovered authorization server %s", self.server)
        if not self.metadata.token_endpoint:
            self.logger.critical(
                "The authorization server did not advertise a token endpoint."
            )
            raise AuthorizationServerMisbehaves

    async def introspect(self, access_token: str) -> None:
        """Introspect the given access token using the Token Introspection
        Endpoint of the configured authorization server.
        """
        if not self.credential:
            self.credential = await self.get_credential(
                scope={"oauth2.introspect"},
                resource=self.server
            )
        raise NotImplementedError

    async def on_teardown(self):
        self.logger.info("Teardown service client")
        for resource in self.resources.values():
            await resource.close()
        await self.http.__aexit__(None, None, None)

    async def request(
        self,
        method: str,
        resource: str,
        path: str,
        headers: dict[str, str] | None = None,
        **kwargs: Any
    ):
        """Make a HTTP request to the specified resource and path."""
        if resource not in self.resources:
            await self.configure(resource)
        return await self.resources[resource].request(
            method=method,
            path=path,
            headers=headers,
            **kwargs
        )

    async def delete(
        self,
        resource: str,
        path: str,
        headers: dict[str, str] | None = None,
        **kwargs: Any
    ) -> Response:
        """Perform a DELETE request to the specified resource."""
        return await self.request(
            method="DELETE",
            resource=resource,
            path=path,
            headers=headers,
            **kwargs
        )

    async def get(
        self,
        resource: str,
        path: str,
        headers: dict[str, str] | None = None,
        **kwargs: Any
    ) -> Response:
        """Perform a POST request to the specified resource."""
        return await self.request(
            method="GET",
            resource=resource,
            path=path,
            headers=headers,
            **kwargs
        )

    async def post(
        self,
        resource: str,
        path: str,
        headers: dict[str, str] | None = None,
        **kwargs: Any
    ) -> Response:
        """Perform a POST request to the specified resource."""
        return await self.request(
            resource=resource,
            method="POST",
            path=path,
            headers=headers,
            **kwargs
        )