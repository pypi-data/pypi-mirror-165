# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import logging

from httpx import AsyncClient
from ckms.types import AuthorizationServerNotDiscoverable
from ckms.types import AuthorizationServerMisbehaves
from ckms.types import JSONWebKeySet
from ckms.types import ServerMetadata

from cbra.utils import retry
from .credential import Credential
from .serviceidentity import ServiceIdentity


class ServiceClient:
    __module__: str = 'cbra.ext.service'
    http: AsyncClient
    identity: ServiceIdentity
    jwks: JSONWebKeySet | None
    logger: logging.Logger
    metadata: ServerMetadata
    server: str
    timeout: float

    def __init__(
        self,
        server: str,
        identity: ServiceIdentity,
        logger: logging.Logger | None = None,
        timeout: float = 60.0
    ):
        self.identity = identity
        self.logger = logger or logging.getLogger("uvicorn")
        self.server = server
        self.timeout = timeout

    async def get_client_assertion(self) -> str:
        """Encode a client assertion used to authenticate with the authorization
        server.
        """
        return await self.identity.get_client_assertion(
            token_endpoint=self.metadata.token_endpoint
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

        # Obtain an initial access token from the authorization server. This
        # is used by the ServiceClient to interfact with its resources, such
        # as the Token Introspection Endpoint.
        self.credential = await Credential.obtain(
            http=self.http,
            token_endpoint=self.metadata.token_endpoint,
            client_id=self.identity.client_id,
            assertion=await self.get_client_assertion(),
            scope={"oauth2.introspect"}
        )

    async def on_teardown(self):
        self.logger.info("Teardown service client")
        await self.http.__aexit__(None, None, None)