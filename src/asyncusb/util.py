from itertools import chain
from typing import Iterable, Iterator

from ._types import FindFilter, getfilterparts


def flatten(iterable: Iterable, depth: int = 1) -> Iterator:
    while depth > 0:
        iterable = chain.from_iterable(iterable)
        depth -= 1
    return iter(iterable)


def _type_dfs(iterable, typ):
    """
    A generator function that flattens an iterable tree, stopping at
    instances of the specified type. Essentially a depth-first search for
    the given type.
    """

    current_iter = iter(iterable)
    parent_id = id(iterable)

    stack = []
    visited = {parent_id}

    while True:
        try:
            while True:
                item = next(current_iter)

                if isinstance(item, typ):
                    yield item

                elif (isinstance(item, Iterable) and
                      not isinstance(item, (str, bytes))):
                    item_id = id(item)
                    if item_id in visited:
                        continue

                    stack.append((current_iter, parent_id))
                    visited.add(item_id)
                    current_iter = iter(item)
                    parent_id = item_id

        except StopIteration:
            visited.remove(parent_id)
            if not stack:
                break
            current_iter, parent_id = stack.pop()


# A sentinel used to ensure that unset attributes never match.
_null = object()

# TODO: find a way to remove recursion from subfilter checking
def find(obj: Iterable, ffilter: FindFilter) -> Iterator:
    """
    Takes an iterable and lazily deep-searches it for a match to the given
    filter.
    """

    ftype, query, extras = getfilterparts(ffilter)
    items = _type_dfs(obj, ftype)

    return filter(lambda item:
        (all(getattr(item, attr, _null) == query[attr] for attr in query) and
         all(any(find(item, extra)) for extra in extras)), items)


__all__ = [
    "flatten",
    "find"
]
