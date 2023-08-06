"""Declares :class:`ClientSubject`."""
from typing import Any

from .types import ISubject


class ClientSubject(ISubject):
    """A subject implementation that represents a client."""
    __module__: str = 'cbra.ext.oauth2'

    def __init__(self, client_id: str, **kwargs: Any):
        self.sub = client_id