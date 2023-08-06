from collections import UserList
from typing import MutableSequence, Optional

from . import SetOnce


class ListView(UserList):
    data: MutableSequence = SetOnce()

    # Note: We'll accept any MutableSequence. "Lists implement all of the common and mutable
    # sequence operations. Lists also provide the following additional method: [sort()]"
    # (https://docs.python.org/3/library/stdtypes.html#lists). Since sort() modifies the list, it's
    # not supported by ListView.
    def __init__(self, initlist: Optional[MutableSequence] = None):
        self.data = [] if initlist is None else initlist  # type: ignore

    def __hash__(self) -> int:
        return hash((id(self), id(self.data)))

    def __delitem__(self, *_args, **_kwargs):
        ListView._raise_type_error()

    def __iadd__(self, *_args, **_kwargs):  # type: ignore
        ListView._raise_type_error()

    def __imul__(self, *_args, **_kwargs):  # type: ignore
        ListView._raise_type_error()

    def __setitem__(self, *_args, **_kwargs):
        ListView._raise_type_error()

    def append(self, *_args, **_kwargs):
        ListView._raise_type_error()

    def clear(self, *_args, **_kwargs):
        ListView._raise_type_error()

    def extend(self, *_args, **_kwargs):
        ListView._raise_type_error()

    def insert(self, *_args, **_kwargs):
        ListView._raise_type_error()

    def pop(self, *_args, **_kwargs):
        ListView._raise_type_error()

    def remove(self, *_args, **_kwargs):
        ListView._raise_type_error()

    def reverse(self, *_args, **_kwargs):
        ListView._raise_type_error()

    def sort(self, *_args, **_kwargs):
        ListView._raise_type_error()

    @classmethod
    def _raise_type_error(cls):
        raise TypeError(f"'{cls.__name__}' object is immutable")
