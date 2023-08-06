# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any

from ckms.core import Keychain
from ckms.jose import PayloadCodec
from ckms.types import JSONWebToken
from ckms.utils import b64encode_str

from cbra.conf import settings


class PersonalDataHandler:
    """Exposes an interface to handle personal data."""
    __module__: str = 'cbra.ext.service'
    encryption_key: str | None = getattr(settings, 'PII_ENCRYPTION_KEY', None)
    codec: PayloadCodec
    index_key: str | None = getattr(settings, 'PII_INDEX_KEY', None)
    keychain: Keychain

    def __init__(self, keychain: Keychain):
        self.codec = PayloadCodec(
            decrypter=keychain,
            encrypter=keychain,
        )
        self.keychain = keychain

    async def decrypt(self, token: str) -> dict[str, Any]:
        """Decrypt the token using JSON Web Encryption (JWT)."""
        jwt = await self.codec.decode(token)
        if not isinstance(jwt, JSONWebToken):
            raise TypeError("Expected the token to contain an encrypted JWT.")
        return jwt.dict()

    async def encrypt(self, **kwargs: Any) -> str:
        """Encrypt the keyword parameters using JSON Web Encryption (JWT)."""
        if self.encryption_key is None:
            raise ValueError(
                'Specify the indexing key with setting PII_ENCRYPTION_KEY'
            )
        return await self.codec.encode(
            payload=kwargs,
            encrypters=[self.encryption_key]
        )

    async def index(self, value: str, encoding: str = 'utf-8') -> str:
        """Create a HMAC of the given value to store it as an index
        for sensitive data. Return the ASCII-encoded digest.
        """
        if self.index_key is None:
            raise ValueError('Specify the indexing key with setting PII_INDEX_KEY')
        k = self.keychain.get(self.index_key)
        return b64encode_str(await k.sign(str.encode(value, encoding=encoding)))