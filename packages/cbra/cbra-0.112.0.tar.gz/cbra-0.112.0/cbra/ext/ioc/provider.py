"""Declares :class:`Provider`."""
import typing
from collections import OrderedDict
from typing import Any

from .models import DependencyList


class Provider:
    """Provides an interface to load and resolve dependencies."""
    __module__: str = 'cbra.ext.ioc'
    DependencySatisfied = type('DependencySatisfied', (Exception,), {})
    _injected: OrderedDict[str, Any]

    def __init__(self):
        self._injected = OrderedDict()

    async def on_boot(self, *args: Any, **kwargs: Any) -> None:
        """Signal boot phase to all dependencies."""
        for obj in list(self._injected.values()):
            f = getattr(obj, 'on_asgi_boot', None)
            if f is None:
                continue
            await f(*args, **kwargs)

    async def on_shutdown(self, *args: Any, **kwargs: Any) -> None:
        """Signal shutdown phase to all dependencies."""
        for obj in list(self._injected.values()):
            f = getattr(obj, 'on_asgi_shutdown', None)
            if f is None:
                continue
            await f(*args, **kwargs)

    def is_satisfied(self, name: str) -> bool:
        """Return a boolean indicating if the dependency is satisfied."""
        return name in self._injected # type: ignore

    async def load_many(self, dependencies: DependencyList):
        """Loads all dependencies in the :class:`DependencyList`."""
        for dep, resolved in await dependencies.resolve():
            self.provide(
                name=dep.spec.name,
                value=resolved,
                force=dependencies.force
            )

    def provide(
        self,
        name: str,
        value: object,
        force: bool = False
    ) -> None:
        """Register Python object `value` as a dependency under the key `name` and
        return the object.

        The `force` argument indicates if any existing dependency under `name`
        must be overwrriten. If `force` is ``False``, an exception is raised if
        `name` is already provided.
        """
        if not force and name in self._injected: # pragma: no cover
            raise self.DependencySatisfied(name)
        self._injected[name] = value

    def resolve(self, name: str) -> typing.Any:
        """Resolve a priorly injected dependency by its name."""
        return self._injected[name]


_default: Provider = Provider()
