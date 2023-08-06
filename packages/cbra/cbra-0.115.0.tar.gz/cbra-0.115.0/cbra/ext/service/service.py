# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from ckms.types import IKeychain

from cbra import Application
from cbra.conf import settings
from .clientkeysendpoint import ClientKeysEndpoint
from .personaldatahandler import PersonalDataHandler
from .serviceclient import ServiceClient
from .serviceidentity import ServiceIdentity


class Service(Application):
    """An API server that integrates various :mod:`cbra` components."""
    __module__: str = 'cbra.ext.service'
    client_keychain: IKeychain
    identity: ServiceIdentity
    pii: PersonalDataHandler

    async def boot(self):
        self.client_keychain = self.keychain.tagged('oauth2-client')
        self.client = ServiceClient(
            server=settings.OAUTH2_SERVER,
            identity=ServiceIdentity(
                client_id=settings.OAUTH2_SERVICE_CLIENT,
                keychain=self.client_keychain
            )
        )
        self.pii = PersonalDataHandler(self.keychain)
        await self.client.on_boot()
        self.add(ClientKeysEndpoint.new(keychain=self.client_keychain))
        return await super().boot()

    async def teardown(self):
        await self.client.on_teardown()
        return await super().teardown()