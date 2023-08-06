# pylint: skip-file
import typing
from typing import Any

from .dependency import Dependency
from .environment import Environment
from .injected import Injected
from .instance import Instance
from .parameterless import Parameterless
from .provider import Provider
from .provider import _default # type: ignore


__all__ = [
    'is_satisfied',
    'provide',
    'resolve',
    'Dependency',
    'Environment',
    'Injected',
    'Instance',
    'Parameterless',
    'Provider'
]

def instance(dependency: type[Any] | str) -> Any:
    return Instance(dependency)


def inject(dependency: typing.Union[str, type]) -> typing.Any:
    return Injected(dependency)


def is_satisfied(name: str, using: Provider | None = None) -> bool:
    """Return a boolean indicating if the dependency is satisfied."""
    return (using or _default).is_satisfied(name)


async def on_boot(*args: Any, using: Provider | None = None, **kwargs: Any) -> None:
    """Provides a hook to execute logic when booting an application."""
    await (using or _default).on_boot(*args, **kwargs)


async def on_shutdown(*args: Any, using: Provider | None = None, **kwargs: Any) -> None:
    """Provides a hook to execute logic when shutting down an application."""
    await (using or _default).on_shutdown(*args, **kwargs)


def provide(
    name: str,
    value: object,
    force: bool = False,
    using: Provider | None = None
) -> None:
    """Register Python object `value` as a dependency under the key `name` and
    return the object.

    The `force` argument indicates if any existing dependency under `name`
    must be overwrriten. If `force` is ``False``, an exception is raised if
    `name` is already provided.
    """
    return (using or _default).provide(name, value, force)


def resolve(name: str, using: Provider | None = None) -> typing.Any:
    """Resolve a priorly injected dependency by its name."""
    return (using or _default).resolve(name)
