"""Primitive wrapper types which maintain context during construction."""

import collections.abc
import copy
import dataclasses
from dataclasses import dataclass, field
from typing import (
    TYPE_CHECKING,
    Iterator,
    List,
    Optional,
    Sequence,
    Tuple,
    TypeVar,
    Union,
    cast,
    overload,
)

from typing_extensions import final

from .errors import ConstructorError
from .pretty_printer import print_primitive, print_table
from .types import ArrayPrimitive, ObjectPrimitive, Primitive


@dataclass(frozen=True)
class ConstructionConfig:
    coerce_strings: bool = False


_Self = TypeVar("_Self", bound="Value")

_Index = Union[int, str]


@dataclass(frozen=True)
class Value:
    raw: Primitive
    config: ConstructionConfig
    _parent: Optional[Tuple[_Index, "Value"]]
    _context: Sequence[str] = field(default_factory=list)

    @classmethod
    def new(cls, data: Primitive, config: ConstructionConfig) -> "Value":
        return cls(data, config, None)

    def is_array(self) -> bool:
        return isinstance(self.raw, list)

    def as_array(self) -> "Array":
        if not self.is_array():
            raise self.make_error("expected array")
        return Array(
            cast(ArrayPrimitive, self.raw),
            self.config,
            self._parent,
            self._context,
        )

    def is_object(self) -> bool:
        return isinstance(self.raw, dict)

    def as_object(self) -> "Object":
        if not self.is_object():
            raise self.make_error("expected object")
        return Object(
            cast(ObjectPrimitive, self.raw),
            self.config,
            self._parent,
            self._context,
        )

    def with_context(self: _Self, context: str) -> _Self:
        return dataclasses.replace(self, _context=[*self._context, context])

    def clone(self: _Self) -> _Self:
        return copy.deepcopy(self)

    def make_error(self, msg: str) -> ConstructorError:
        # We are accessing private members of other instances of Value.
        # These members are not for public use but are expected to be used in
        # this way.
        # pylint: disable=protected-access
        return ConstructorError(
            f"{self._get_path()}: {msg}",
            print_table(
                [("path", "expected structure", "actual data")]
                + [
                    (v._get_path(), "/".join(v._context), print_primitive(v.raw))
                    for v in self._iter_parents()
                ]
            ),
            self._get_depth(),
        )

    def _get_path(self) -> str:
        # As above, we are accessing private members of other instances of
        # ValueView.
        # pylint: disable=protected-access
        path = [v._get_index() for v in self._iter_parents()]
        return "." + ".".join(
            _quote_context(index) for index in path if index is not None
        )

    def _get_index(self) -> Optional[_Index]:
        if self._parent:
            return self._parent[0]
        return None

    def _get_depth(self) -> Tuple[int, int]:
        return (len(list(self._iter_parents())), len(self._context))

    def _iter_parents(self) -> Iterator["Value"]:
        # As above, we are accessing private members of other instances of
        # ValueView.
        # pylint: disable=protected-access
        def inner() -> Iterator["Value"]:
            current: Value = self
            while current._parent:
                yield current
                _, current = current._parent
            yield current

        return reversed(list(inner()))


# See https://mypy.readthedocs.io/en/latest/runtime_troubles.html#using-classes-that-are-generic-in-stubs-but-not-at-runtime.  # noqa
if TYPE_CHECKING:  # pragma: no cover
    _BaseArray = collections.abc.Sequence[Value]
else:
    _BaseArray = collections.abc.Sequence


@final
@dataclass(frozen=True)
class Array(Value, _BaseArray):
    raw: ArrayPrimitive

    @overload
    def __getitem__(self, index: int) -> Value:
        ...  # pragma: no cover

    @overload
    def __getitem__(self, index: slice) -> List[Value]:
        ...  # pragma: no cover

    def __getitem__(self, index: Union[int, slice]) -> Union[Value, List[Value]]:
        def wrap(i: int) -> Value:
            return Value(self.raw[i], self.config, (i, self))

        if isinstance(index, int):
            return wrap(index)
        return [wrap(i) for i in range(0, len(self))[index]]

    def __len__(self) -> int:
        return len(self.raw)


# See https://mypy.readthedocs.io/en/latest/runtime_troubles.html#using-classes-that-are-generic-in-stubs-but-not-at-runtime.  # noqa
if TYPE_CHECKING:  # pragma: no cover
    _BaseObject = collections.abc.Mapping[str, Value]
else:
    _BaseObject = collections.abc.Mapping


@final
@dataclass(frozen=True)
class Object(Value, _BaseObject):
    raw: ObjectPrimitive

    def __getitem__(self, key: str) -> Value:
        return Value(self.raw[key], self.config, (key, self))

    def __delitem__(self, key: str) -> None:
        del self.raw[key]

    def __iter__(self) -> Iterator[str]:
        return iter(self.raw)

    def __len__(self) -> int:
        return len(self.raw)


def _quote_context(context: Union[int, str]) -> str:
    if isinstance(context, int):
        return str(context)
    return context.replace("\\", "\\\\").replace('"', '\\"')
