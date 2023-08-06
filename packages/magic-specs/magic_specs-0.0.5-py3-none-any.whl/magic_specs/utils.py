from functools import wraps
from typing import Any, Callable


__all__ = [
    "iterable_cache",
    "Sentinel",
]


class Sentinel:
    pass


def iterable_cache(provider: str, *args, **kwargs) -> Callable:
    r"""Decorate classes "__next__" magic method. This creates a cache that remembers
    the current iterator object the instance is iterating over. The cached instance is
    provided to "__next__" as an argument, so it can just call next(...) on it.
    Once the iterator is iterated, it clears the cached iterator,
    so the class can then be iterated again.

    class A:
        def __iter__(self):
            return self

        @iterable_cache(provider="keys")
        def __next__(self, keys):
            return

        def keys(self):
            # items are provided here

    :params provider: Function that procides the items to iterate over.
                      Additional arguments can be provided to it from *args and **kwargs.
    """

    def decorator(func) -> Callable:
        items = None

        @wraps(func)
        def wrapper(self) -> Any:
            nonlocal items
            if items is None:
                items = iter(getattr(self, provider)(*args, **kwargs))

            try:
                result = func(self, items)
                return result
            except StopIteration as error:
                items = None
                raise error

        return wrapper

    return decorator
