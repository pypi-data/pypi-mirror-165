# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from ckms.core import Keychain
from ckms.types import JSONWebKeySet

import cbra
from cbra.cors import AnonymousReadCorsPolicy
from cbra.cors import CorsPolicyType


class ClientKeysEndpoint(cbra.Endpoint):
    """Single-tenant endpoint exposing the public keys used with the OAuth 2.x
    client of the server.
    """
    __module__: str = 'cbra.ext.service'
    cors_policy: type[CorsPolicyType] = AnonymousReadCorsPolicy
    name: str = 'service.oauth2-jwks'
    description: str = (
        "Provides the JSON Web Key Set (JWKS) that the server used to "
        "assert the ownership of its OAuth 2.x client."
    )
    keychain: Keychain
    method: str = 'GET'
    mount_path: str = '.well-known/oauth-client-jwks'
    summary: str = 'OAuth 2.x Client JWKS'
    response_model: type[JSONWebKeySet] = JSONWebKeySet
    response_model_by_alias: bool = True
    response_model_exclude_none: bool = True
    response_description: str = "The OAuth 2.x client public keys."
    tags: list[str] = ["Server metadata"]
    with_options: bool = True

    async def handle(self) -> JSONWebKeySet:
        return self.keychain.as_jwks(private=False)