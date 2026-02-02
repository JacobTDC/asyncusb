from functools import reduce
from typing import Any, Callable


def _noop(_) -> bool:
    return True


class FindFilter:
    def __init__(self, typ: type, query: dict[str, Any] | None = None,
                 *subfilters: 'FindFilter'):
        self._type = typ
        self._query = query
        self._subfilters = subfilters
        self._test: Callable[[object], bool]

        if query:
            attrs = tuple(zip(map(lambda name: name.split('.'), query.keys()),
                              query.values()))

            def func(obj) -> bool:
                try:
                    for name, val in attrs:
                        if reduce(getattr, name, obj) != val:
                            return False
                except AttributeError:
                    return False

                return True

            self._test = func
        else:
            self._test = _noop

    def __repr__(self):
        if self._type.__module__ == 'builtins':
            name = f"{self._type.__name__}"
        else:
            name = f"{self._type.__module__}.{self._type.__name__}"

        args = ", ".join((repr(self._query), *map(repr, self._subfilters)))
        return f"{name}[{args}]"


class FilterableMeta(type):
    def __getitem__(self, key):
        if isinstance(key, tuple):
            return FindFilter(self, *key)
        else:
            return FindFilter(self, key)


class Filterable(metaclass=FilterableMeta):
    """
    Subclasses allow creation of a util.find filter using Class[filter_args].
    """
    __slots__ = ()


def getfilterparts(ffilter: FindFilter) -> tuple[type, Callable[[object], bool],
                                                 tuple[FindFilter, ...]]:
    return ffilter._type, ffilter._test, ffilter._subfilters
