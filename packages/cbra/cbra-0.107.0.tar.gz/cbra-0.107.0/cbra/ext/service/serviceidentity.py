# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import secrets

from ckms.jose import PayloadCodec
from ckms.types import IKeychain
from ckms.utils import current_timestamp


class ServiceIdentity:
    """Represents the identity of the service, using its signing and
    encryption keys.
    """
    __module__: str = 'cbra.ext.service'
    client_id: str
    codec: PayloadCodec
    keychain: IKeychain
    ttl: int = 60

    def __init__(self, client_id: str, keychain: IKeychain):
        self.client_id = client_id
        self.keychain = keychain
        self.codec = PayloadCodec(
            encrypter=self.keychain,
            decrypter=self.keychain,
            signer=self.keychain
        )

    async def get_client_assertion(
        self,
        token_endpoint: str
    ) -> str:
        """Encode a client assertion used to authenticate with the authorization
        server.
        """
        now = current_timestamp()
        return await self.codec.encode(
            payload={
                'aud': token_endpoint,
                'exp': now + self.ttl,
                'iat': now,
                'iss': self.client_id,
                'jti': secrets.token_urlsafe(48),
                'nbf': now,
                'sub': self.client_id,
            },
            signers=[ # type: ignore
                x for x in self.keychain
                if (not x.is_public() and x.can_sign())
            ]
        )