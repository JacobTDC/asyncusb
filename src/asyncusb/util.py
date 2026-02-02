from itertools import chain
from typing import Iterable, Iterator

from ._types import FindFilter, getfilterparts


def flatten(iterable: Iterable, depth: int = 1) -> Iterator:
    while depth > 0:
        iterable = chain.from_iterable(iterable)
        depth -= 1
    return iter(iterable)


# This function is not public, and may change without notice.
# Operates in O(V + E) time..
def _type_dfs(iterable, typ):
    """
    A generator function that flattens an iterable tree, yielding instances
    of the specified type. Essentially a depth-first search for the given
    type.
    """

    parent_id = id(iterable)
    stack = [(iter(iterable), parent_id)]
    visited = {parent_id}

    while stack:
        current_iter, parent_id = stack.pop()

        while (item := next(current_iter, _null)) is not _null:
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

        visited.remove(parent_id)


# A sentinel value.
_null = object()

# This is a fully iterative implementation, and the only limit to how deep
# it can search is how much memory is available.
# Operates in O(D × (V + E)) time (worst case).
def find(iterable: Iterable, ffilter: FindFilter) -> Iterator:
    """
    Takes an iterable and lazily deep-searches it for a match to the given
    filter.
    """

    ftype, query, filters = getfilterparts(ffilter)
    stack = [(iterable, _type_dfs(iterable, ftype), query, filters, 0)]

    while stack:
        _, current_iter, query, filters, idx = stack.pop()

        while (item := next(current_iter, _null)) is not _null:
            if not query(item):
                # Query doesn't match, so skip this item.
                continue

            while True:
                if idx < len(filters):
                    # We still have subfilters to check for this item.
                    if isinstance(item, Iterable):
                        # Item is iterable, so save current state to stack
                        # and begin matching children against subfilters.
                        stack.append((item, current_iter, query, filters, idx))
                        ftype, query, filters = getfilterparts(filters[idx])
                        current_iter = _type_dfs(item, ftype)
                        idx = 0

                elif stack:
                    # Unwind the stack one level.
                    item, current_iter, query, filters, idx = stack.pop()
                    idx += 1
                    continue

                else:
                    # We've reached the bottom of the stack, so this item
                    # is a match.
                    yield item

                # Get the next item from the current iterator.
                break


__all__ = [
    "FindFilter",
    "flatten",
    "find"
]
