from collections.abc import Mapping, Sequence
from functools import lru_cache
from inspect import ismethod
from types import MappingProxyType
from typing import Type

from . import ImmutableAttributeError

IMMUTABLE_TYPES = {  # using dict, not set, to preserve order
    bool: None,
    bytes: None,
    complex: None,
    float: None,
    int: None,
    type(None): None,
    str: None,
    range: None,
}


def pytrify(obj: object):
    if type(obj) in IMMUTABLE_TYPES:
        return obj

    if isinstance(obj, Mapping):
        return _make_immutable_mapping(obj)

    if isinstance(obj, Sequence):
        return _make_immutable_sequence(obj)

    if isinstance(obj, set) or isinstance(obj, frozenset):
        return frozenset(map(pytrify, obj))

    Wrapper = _create_wrapper_class(obj.__class__)  # ignore: type
    return Wrapper(obj)


def _make_immutable_sequence(sequence):
    return tuple(list(map(pytrify, sequence)))


def _make_immutable_mapping(mapping):
    return MappingProxyType({pytrify(key): pytrify(value) for key, value in mapping.items()})


@lru_cache(maxsize=None)
def _create_wrapper_class(class_: Type):
    return type(
        f"RO{class_.__name__}",
        (class_,),
        {
            "__init__": immutable_wrapper_init,
            "__getattribute__": immutable_wrapper_getattribute,
            "__setattr__": immutable_wrapper_setattr,
        },
    )


def immutable_wrapper_init(self, obj):
    object.__setattr__(self, "_obj", obj)


def immutable_wrapper_getattribute(self, attr):
    attr_reference = getattr(object.__getattribute__(self, "_obj"), attr)

    if ismethod(attr_reference):
        return object.__getattribute__(self, attr)

    if attr == "__class__":
        return object.__getattribute__(self, "__class__")

    return pytrify(attr_reference)


def immutable_wrapper_setattr(self, name, value):
    raise ImmutableAttributeError(
        "Objects that are wrapped by a read-only wrapper do not support assignment"
    )
