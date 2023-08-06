from typing import Any, Optional, Type, TypeVar

from . import ImmutableAttributeError

T = TypeVar("T")


class MutableWhileNone:
    """
    A descriptor used to make immutable attributes that default to `None`

    Creates attributes that default to `None` and can be initialized to another value. Attributes
    become immutable once their value is no longer None.

    Example:
        >>> from typing import Optional
        >>> from pytrify import MutableWhileNone
        >>> class T:
        ...     a: Optional[int] = MutableWhileNone()
        ...
        >>> t = T()
        >>> t.a is None
        True
        >>> t.a = 1
        >>> t.a
        1
        >>> t.a = 2
        Traceback (most recent call last):
          File "<stdin>", line 1, in <module>
          File "/home/user/git/pytrify/pytrify/mutable_while_none.py", line 17, in __set__
            raise ImmutableAttributeError(
        pytrify.ImmutableAttributeError: The attribute "T.a" is immutable after initialization

    """

    def __set_name__(self, owner: Type, name: str):
        self._attribute_name = name
        self._private_attribute_name = f"_mutable_while_none_{name}"

    def __get__(self, obj: T, type: Optional[Type[T]] = None) -> Any:
        return getattr(obj, self._private_attribute_name, None)

    def __set__(self, obj: Any, value: Any) -> None:
        # TODO: Figure out how to make self._private_attribute_name immutable too
        if getattr(obj, self._private_attribute_name, None) is not None:
            raise ImmutableAttributeError(
                f'The attribute "{obj.__class__.__name__}.{self._attribute_name}" is immutable '
                "after initialization"
            )

        setattr(obj, self._private_attribute_name, value)
