"""A tool to determine whether an object is a list (iterable, no keys, not a string)."""
from collections.abc import Iterable, Mapping


def list_like(obj):
    """"Determine whether the object is like a list (iterable, no keys, not a string)."""
    return isinstance(obj, Iterable) and not isinstance(obj, Mapping) and not isinstance(obj, str)
