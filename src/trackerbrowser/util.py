"""Utility functions"""

from collections.abc import Iterable   # drop `.abc` with Python 2.7 or lower

def iterable(obj):
    return isinstance(obj, Iterable)

def listify(obj):
    if obj is None:
        return []
    elif iterable(obj):
        return list(obj)
    else:
        return [obj]

def list_for_query(iterable):
    iterable = listify(iterable)
    iterable = [str(obj) for obj in iterable]
    return f"({','.join(iterable)})"
