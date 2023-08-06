"""Declares :func:`RFC9068Principal`."""
import inspect
import typing

import fastapi
import httpx
from ckms.core import Keychain
from ckms.jose import PayloadCodec
from ckms.types import ClaimSet
from ckms.types import JSONWebKeySet
from ckms.types import ServerMetadata
from fastapi.security import HTTPBearer
from fastapi.security import HTTPAuthorizationCredentials

from cbra.params import ServerKeychain
from cbra.exceptions import AuthenticationRequired
from cbra.exceptions import CanonicalException
from cbra.exceptions import ForgedAccessToken
from cbra.exceptions import InvalidAuthorizationScheme
from cbra.exceptions import UntrustedIssuer
from cbra.utils import retry
from .principal import Principal
from .types import IPrincipal
from .params import LocalIssuer


security = HTTPBearer(auto_error=False)
ISSUER_JWKS_CACHE: dict[str, JSONWebKeySet] = {}


@retry(5, interval=2.0)
async def get_issuer_jwks(issuer: str) -> JSONWebKeySet | None:
    jwks = ISSUER_JWKS_CACHE.get(issuer)
    if jwks is None:
        async with httpx.AsyncClient() as client:
            metadata = await ServerMetadata.discover(client, issuer)
            jwks = await metadata.get_jwks(client)
        if jwks is not None:
            ISSUER_JWKS_CACHE[issuer] = jwks
    return jwks


def RFC9068Principal(
    auto_error: bool = True,
    client_id: typing.Optional[str] = None,
    trusted_issuers: typing.Optional[typing.Set[str]] = None,
    header: str = 'Authorization',
    path: typing.Optional[str] = None,
    max_age: int = 300,
    principal_factory: typing.Callable[[ClaimSet], IPrincipal] = Principal.fromclaimset,
    scope: set[str] | None = None
) -> typing.Any:
    """Resolves the principal in a request to a subject using an
    :rfc:`9068` access token.
    """
    scope = scope or set()
    issuers: typing.Set[str] = trusted_issuers or set()
    if path is not None and not str.startswith(path, '/'):
        raise ValueError("The `path` parameter must start with a slash.")

    async def resolve_principal(
        request: fastapi.Request,
        issuer: str = LocalIssuer,
        bearer: typing.Optional[
            HTTPAuthorizationCredentials
        ] = fastapi.Depends(security),
        keychain: Keychain = ServerKeychain
    ):
        codec = PayloadCodec()
        if bearer is None:
            if auto_error and 'Authorization' not in request.headers:
                raise AuthenticationRequired
            if auto_error:
                # The header was present but a parsing error occurred.
                raise InvalidAuthorizationScheme
            return None

        if str.lower(bearer.scheme or '') != "bearer":
            raise InvalidAuthorizationScheme

        audience = {
            f"{request.url.scheme}://{request.url.netloc}",
            f"{request.url.scheme}://{request.url.netloc}{path or ''}",
            f"{request.url.scheme}://{request.url.netloc}{request.url.path}"
        }
        jws, claims = await codec.jwt(bearer.credentials, accept="at+jwt")
        claims.verify(
            audience=audience,
            required={"jti", "iss", "aud", "sub", "iat", "nbf", "exp", "client_id"},
            max_age=max_age
        )
        if claims.iss not in (issuers | {issuer}):
            assert claims.iss is not None # nosec
            raise UntrustedIssuer(claims.iss)

        granted_scope: set[str] = {
            x for x in str.split((claims.extra.get('scope') or ''), ' ')
            if x
        }
        if not (granted_scope > scope):
            raise CanonicalException(
                http_status_code=401,
                code="AUTHORIZATION_REQUIRED",
                message=(
                    "The scope granted to the access token was not sufficient "
                    "to access this resource."
                )
            )

        # If the issuer was valid but the signature validation fails here,
        # then the token was most probably forged.
        if claims.iss == issuer:
            is_valid_signature = jws.verify(keychain, require_kid=True)
        else:
            # Token was not issued by this server. The issuer must then be in the
            # trusted issuers set.
            assert claims.iss in issuers # nosec
            jwks = await get_issuer_jwks(claims.iss)
            if jwks is None:
                raise CanonicalException(
                    http_status_code=503,
                    code="ISSUER_UNREACHABLE",
                    message=(
                        "Unable to reach the issuer specified by the access token."
                    )
                )
            is_valid_signature = jws.verify(jwks, require_kid=True)
        if inspect.isawaitable(is_valid_signature):
            is_valid_signature = await is_valid_signature
        if not is_valid_signature:
            raise ForgedAccessToken
        return principal_factory(claims)

    return resolve_principal