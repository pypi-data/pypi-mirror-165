"""Declares :class:`JSONDefaultContentNegotiation`."""
from .default import DefaultContentNegotiation


class JSONDefaultContentNegotiation(DefaultContentNegotiation):
    """Content negotation that defaults to JSON. Used most commonly
    with misbehaving clients.
    """
    default_response_encoding: str  = "application/json"