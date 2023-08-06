# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import fastapi

from .clientkeysendpoint import ClientKeysEndpoint
from .personaldatahandler import PersonalDataHandler
from .resource import Resource
from .service import Service
from .serviceclient import ServiceClient


__all__: list[str] = [
    'ClientKeysEndpoint',
    'Resource',
    'PersonalDataHandler',
    'PersonalDataService',
    'Service',
    'ServiceClient'
]


CurrentService: ServiceClient = fastapi.Depends(ServiceClient.current)

PersonalDataService: PersonalDataHandler = fastapi.Depends()