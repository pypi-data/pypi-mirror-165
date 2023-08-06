# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import os
import logging
from typing import Any

from ckms import core

from cbra.conf import settings


AUTOLOAD: bool = getattr(settings, 'USE_DEFAULT_KEYS', False)

DEFAULT_KEYS: list[tuple[str, str]] = [
    ('enc', 'APP_ENCRYPTION_KEY'),
    ('sig', 'APP_SIGNING_KEY'),
    ('pii', 'PII_ENCRYPTION_KEY'),
    ('idx', 'PII_INDEX_KEY')
]

keychain: core.Keychain = core.get_default_keychain()


def get_keyspec_from_env(
    name: str,
    varname: str
) -> dict[str, Any] | None:
    """Inspect the environment variables for the present of `varname`,
    assume that its content is a DSN, and parse it into the keychain.
    """
    if varname not in os.environ:
        return None
    params: dict[str, Any] = core.parse_dsn(os.environ[varname])
    version: str | None = os.environ.get(f'{varname}_VERSION')
    if version is not None:
        # TODO: This is basically only used by Google Cloud KMS
        # keys.
        params['version'] = version
    return {name: params}


async def init():
    """Inspects the environment variables to add standardized keys to the
    global keychain.
    """
    if not AUTOLOAD:
        return
    logger = logging.getLogger("uvicorn")
    for name, varname in DEFAULT_KEYS:
        spec = get_keyspec_from_env(name, varname)
        if spec is None:
            continue
        keychain.configure(spec)
        logger.info("Configured keychain from environment variable %s", varname)
    await keychain