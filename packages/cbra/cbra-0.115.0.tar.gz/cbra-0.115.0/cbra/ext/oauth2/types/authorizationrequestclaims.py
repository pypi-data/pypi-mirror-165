# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import pydantic

from .oidcrequestedclaims import OIDCRequestedClaims


class AuthorizationRequestClaims(pydantic.BaseModel):
    id_token: OIDCRequestedClaims | None = None

    def requests(self, scope: set[str]) -> set[str]:
        """Return the set of claims that are requested by the authorization
        request.
        """
        raise NotImplementedError