# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any

import pydantic

from .basegrant import BaseGrant
from .iclient import IClient
from .isubject import ISubject


class IOpenIdTokenBuilder:
    __module__: str = 'cbra.ext.oauth2.types'
    claims_model: type[pydantic.BaseModel]

    def requests(self, scope: set[str]) -> set[str]:
        """Return the set of claims requested by the given scope and
        claims.
        """
        raise NotImplementedError

    async def build(
        self,
        *,
        signing_key: str,
        client: IClient,
        subject: ISubject,
        grant: BaseGrant,
        scope: set[str],
        request: Any | None = None,
        access_token: str | None = None
    ) -> str | None:
        """Build an OpenID Connect ID Token."""
        raise NotImplementedError

    def validate_claims(self, claims: dict[str, Any]) -> bool:
        """Return a boolean indicating if the ``claims`` parameter of an
        authorization request is valid.
        """
        try:
            self.claims_model.parse_obj(claims)
            return True
        except (pydantic.ValidationError, TypeError, ValueError):
            return False