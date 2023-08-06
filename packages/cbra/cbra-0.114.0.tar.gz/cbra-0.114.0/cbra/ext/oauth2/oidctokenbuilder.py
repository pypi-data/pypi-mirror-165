# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import copy
import secrets
from typing import Any

from ckms.core import Keychain
from ckms.jose import PayloadCodec
from ckms.utils import current_timestamp

from cbra.params import ServerKeychain
from .params import ServerCodec
from .params import CurrentServerMetadata
from .oidcclaimhandler import OIDCClaimHandler
from .types import AuthorizationRequest
from .types import AuthorizationRequestClaims
from .types import BaseGrant
from .types import AuthorizationCodeGrant
from .types import IClient
from .types import IOIDCTokenBuilder
from .types import ISubject
from .types import ServerMetadata
from .utils import openid_hash


class OIDCTokenBuilder(IOIDCTokenBuilder):
    __module__: str = 'cbra.ext.oauth2'
    claims_model: type[AuthorizationRequestClaims] = AuthorizationRequestClaims
    codec: PayloadCodec
    handlers: list[type[OIDCClaimHandler]] = []
    keychain: Keychain
    metadata:  ServerMetadata
    now: int

    def __init__(
        self,
        codec: PayloadCodec = ServerCodec,
        keychain: Keychain = ServerKeychain,
        metadata: ServerMetadata = CurrentServerMetadata
    ):
        self.codec = codec
        self.keychain = keychain
        self.metadata = metadata
        self.now = current_timestamp()

    def get_handlers(
        self,
        client: IClient,
        subject: ISubject,
        initial: dict[str, Any] | None = None,
        scope: set[str] | None = None
    ) -> list[OIDCClaimHandler]:
        """Return a list of handler instances to construct the claims
        set.
        """
        scope = scope or set()
        handlers: list[OIDCClaimHandler] = []
        for cls in self.handlers:
            handler = cls(
                client,
                subject,
                self.now,
                copy.deepcopy(initial or {})
            )
            if not handler.is_enabled(scope):
                continue
            handlers.append(handler)
        return handlers

    def get_initial_claims(
        self,
        signing_key: str,
        client: IClient,
        subject: ISubject,
        grant: BaseGrant,
        request: AuthorizationRequest | None = None,
        access_token: str | None = None,
        code: str | None = None
    ) -> dict[str, Any]:
        """Return a dictionary containing the initial claims to add to the
        ID Token.
        """
        key = self.keychain.get(signing_key)
        claims: dict[str, Any] = {
            **client.get_id_token_claims(self.now),
            'iat': self.now,
            'iss': self.metadata.issuer,
            'jti': secrets.token_urlsafe(24),
            'nbf': self.now,
            'sub': client.get_subject_id(subject)
        }
        if isinstance(grant, AuthorizationCodeGrant):
            assert isinstance(request, AuthorizationRequest) # nosec
            assert isinstance(request.auth_time, int)
            claims.update({
                'auth_time': request.auth_time,
                'c_hash': openid_hash(
                    alg=key.algorithm,
                    value=grant.code,
                    crv=key.curve
                )
            })
        if access_token is not None:
            claims['at_hash'] = openid_hash(
                alg=key.algorithm,
                value=access_token,
                crv=key.curve
            )
        if request is not None:
            claims["nonce"] = request.nonce
        return claims

    def requests(
        self,
        scope: set[str]
    ) -> set[str]:
        claims: set[str] = set()
        for handler in self.handlers:
            claims.update(handler.requests(scope))
        return claims

    async def build(
        self,
        *,
        signing_key: str,
        client: IClient,
        subject: ISubject,
        grant: BaseGrant,
        scope: set[str],
        request: AuthorizationRequest | None = None,
        access_token: str | None = None
    ) -> str | None:
        if not self._is_openid(grant, request):
            return None
        claims: dict[str, Any] = self.get_initial_claims(
            signing_key=signing_key,
            client=client,
            subject=subject,
            request=request,
            grant=grant,
            access_token=access_token
        )
        return await self.codec.encode(
            payload=await self.run_handlers(
                client=client,
                subject=subject,
                initial=claims,
                scope=scope,
                grant=grant,
                request=request
            ),
            signers=[signing_key],
            encrypters=client.get_encryption_keys() # type: ignore
        )

    async def run_handlers(
        self,
        client: IClient,
        subject: ISubject,
        initial: dict[str, Any] | None = None,
        scope: set[str] | None = None,
        grant: BaseGrant | None = None,
        request: AuthorizationRequest | None = None
    ) -> dict[str, Any]:
        """Run handlers to update the initial claims with their respective
        additions.
        """
        initial = initial or {}
        scope = scope or set()
        claims: dict[str, Any] = {}
        for handler in self.get_handlers(client, subject, initial, scope):
            claims.update(await handler.claims(grant, request))
        return {**initial, **claims}

    def _is_openid(
        self,
        grant: BaseGrant,
        request: AuthorizationRequest | None
    ) -> bool:
        return bool(grant.is_openid() or (request and request.is_openid()))