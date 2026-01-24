class FindFilter:
    def __init__(self, typ, query):
        self._type = typ

        if isinstance(query, tuple):
            self._query, *self._extras = query
        else:
            self._query = query
            self._extras = None

    def __repr__(self):
        if self._type.__module__ == 'builtins':
            name = f"{self._type.__name__}"
        else:
            name = f"{self._type.__module__}.{self._type.__name__}"

        if self._extras:
            args = ", ".join([repr(self._query), *map(repr, self._extras)])
            return f"{name}[{args}]"
        else:
            return f"{name}[{repr(self._query)}]"

class FilterableMeta(type):
    def __getitem__(self, key):
        return FindFilter(self, key)

class Filterable(metaclass=FilterableMeta):
    """
    Subclasses allow creation of a util.find filter using Class[filter_args].
    """
    __slots__ = ()

def getfilterparts(ffilter: FindFilter) -> tuple[type, dict, list]:
    return ffilter._type, ffilter._query or {}, ffilter._extras or []
