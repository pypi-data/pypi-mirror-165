# pylint: skip-file
import functools
from typing import Any
from typing import Callable

from cbra.exceptions import CanonicalException
from cbra.resource import Resource
from . import exceptions
from . import params
from . import types
from .authorizeendpoint import AuthorizationEndpoint
from .authorizationserver import AuthorizationServer
from .authorizationrequestclient import AuthorizationRequestClient
from .clientconfig import ClientConfig
from .configfileclientrepository import ConfigFileClientRepository
from .memorystorage import MemoryStorage
from .memoryclientrepository import MemoryClientRepository
from .memorysubjectrepository import MemorySubjectRepository
from .nullsubjectrepository import NullSubjectRepository
from .oidcclaimhandler import OIDCClaimHandler
from .oidctokenbuilder import OIDCTokenBuilder
from .pushedauthorizationrequestendpoint import PushedAuthorizationRequestEndpoint
from .rfc9068principal import RFC9068Principal
from .settingsclientrepository import SettingsClientRepository
from .settingssubjectrepository import SettingsSubjectRepository
from .staticsubjectepository import StaticSubjectRepository
from .tokenissuer import TokenIssuer
from .tokenrequesthandler import TokenRequestHandler
from .upstreamreturnhandler import UpstreamReturnHandler
from .upstreamprovider import UpstreamProvider


__all__: list[str] = [
    'exceptions',
    'params',
    'scope',
    'types',
    'AuthorizationEndpoint',
    'AuthorizationServer',
    'AuthorizationRequestClient',
    'ClientConfig',
    'ConfigFileClientRepository',
    'MemoryClientRepository',
    'MemoryStorage',
    'MemorySubjectRepository',
    'NullSubjectRepository',
    'OIDCClaimHandler',
    'OIDCTokenBuilder',
    'PushedAuthorizationRequestEndpoint',
    'RFC9068Principal',
    'SettingsClientRepository',
    'SettingsSubjectRepository',
    'StaticSubjectRepository',
    'TokenIssuer',
    'TokenRequestHandler',
    'UpstreamReturnHandler',
    'UpstreamProvider',
]


def scope(required: set[str]) -> Callable[..., Any]:
    """Method decorator for :class:`~cbra.Resource` implementations
    that enforces a given scope.
    """
    def decorator_factory(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        async def f(self: Resource, *args: Any, **kwargs: Any):
            if not self.principal.has_scope(required):
                raise CanonicalException(
                    http_status_code=401,
                    code="AUTHORIZATION_REQUIRED",
                    message=(
                        "The scope granted to the access token was not sufficient "
                        "to access this resource."
                    )
                )
            return await func(self, *args, **kwargs)
        return f
    return decorator_factory