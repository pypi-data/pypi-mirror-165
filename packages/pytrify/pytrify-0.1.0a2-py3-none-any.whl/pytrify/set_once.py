from typing import Any, Optional, Type, TypeVar

from . import ImmutableAttributeError

T = TypeVar("T")


class SetOnce:
    """
    A descriptor used to make immutable attributes

    Allows attributes to be immutable after initialization.

    Example:
        >>> from pytrify import SetOnce
        >>> class T:
        ...     a: int = SetOnce()
        ...
        >>> t = T()
        >>> t.a = 1
        >>> t.a = 2
        Traceback (most recent call last):
          File "<stdin>", line 1, in <module>
          File "/home/msalvatore/git/pytrify/pytrify/set_once.py", line 42, in __set__
            raise ImmutableAttributeError(
        pytrify.ImmutableAttributeError: The attribute "T.a" is immutable after initialization
    """

    def __set_name__(self, owner: Type, name: str):
        self._name = f"_setonce_{name}"
        self._flag_name = f"_setonce_{name}_flag"

    def __get__(self, obj: T, type: Optional[Type[T]] = None) -> Any:
        return getattr(obj, self._name)

    def __set__(self, obj: Any, value: Any) -> None:
        # TODO: Figure out how to make the flag immutable (set once) too.
        if getattr(obj, self._flag_name, False):
            raise ImmutableAttributeError(
                f'The attribute "{obj.__class__.__name__}.{self._name}" is immutable after '
                "initialization"
            )

        setattr(obj, self._flag_name, True)
        setattr(obj, self._name, value)
