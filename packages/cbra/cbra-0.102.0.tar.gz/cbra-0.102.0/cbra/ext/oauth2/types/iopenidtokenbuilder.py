# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from .authorizationrequest import AuthorizationRequest
from .basegrant import BaseGrant
from .iclient import IClient
from .isubject import ISubject


class IOpenIdTokenBuilder:
    __module__: str = 'cbra.ext.oauth2.types'

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
        """Build an OpenID Connect ID Token."""
        raise NotImplementedError