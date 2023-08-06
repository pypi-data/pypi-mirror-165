# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any

from cbra import Endpoint
from cbra.types import ICorsPolicy

from .cors import CORSPolicy
from .principal import ISessionPrincipal
from .principal import SessionPrincipal



class SessionEndpoint(Endpoint):
    __module__: str = 'libwebid.lib'
    cors_policy: type[ICorsPolicy] = CORSPolicy
    principal: ISessionPrincipal
    principal_factory: Any = SessionPrincipal.fromcookie
    require_authentication: bool = True
    session_required: bool = False