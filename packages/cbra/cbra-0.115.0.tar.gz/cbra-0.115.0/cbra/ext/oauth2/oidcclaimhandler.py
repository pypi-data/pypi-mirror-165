# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import functools
from typing import Any

from .types import BaseGrant
from .types import AuthorizationRequest
from .types import IClient
from .types import ISubject


class OIDCClaimHandler:
    """Provides an interface to update a claims set for a given
    scope.
    """
    __module__: str = 'cbra.ext.oauth2'
    client: IClient
    handles: set[str] = set()
    now: int
    subject: ISubject

    @classmethod
    def requests(cls, scope: set[str]) -> set[str]:
        return cls.get_requested_claims(scope)

    @classmethod
    def get_requested_claims(cls, scope: set[str]) -> set[str]:
        raise NotImplementedError(f'{cls.__name__}.get_requested_claims() must be overriden.')

    def __init__(
        self,
        client: IClient,
        subject: ISubject,
        now: int,
        initial: dict[str, Any]
    ):
        self.client = client
        self.now = now
        self.subject = subject

    async def claims(
        self,
        grant: BaseGrant | None = None,
        request: AuthorizationRequest | None = None
    ) -> dict[str, Any]:
        """Return a mapping holding the claims that are added to the
        claims set by this handler.
        """
        raise NotImplementedError

    @functools.singledispatchmethod
    @classmethod
    def is_enabled(self, config: set[str]) -> bool:
        """Return a boolean if the handler is enabled for the given
        scope or claims `config.
        """
        raise NotImplementedError(type(config))

    @is_enabled.register
    def _is_enabled_for_scope(self, scope: set) -> bool: # type: ignore
        return self.is_enabled_for_scope(scope) # type: ignore

    def is_enabled_for_scope(self, scope: set[str]) -> bool:
        """Return a boolean if the handler is enabled for the given
        scope `scope`.
        """
        return set(scope) >= set(self.handles)