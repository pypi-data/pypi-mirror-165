# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import pydantic

from .oidcclaimrequest import OIDCClaimRequest


Empty = type('Empty', (object,), {})


class OIDCRequestedClaims(pydantic.BaseModel):
    iss: OIDCClaimRequest | None = None
    sub: OIDCClaimRequest | None = None
    aud: OIDCClaimRequest | None = None
    exp: OIDCClaimRequest | None = None
    iat: OIDCClaimRequest | None = None
    auth_time: OIDCClaimRequest | None = None
    nonce: OIDCClaimRequest | None = None
    acr: OIDCClaimRequest | None = None
    amr: OIDCClaimRequest | None = None
    azp: OIDCClaimRequest | None = None