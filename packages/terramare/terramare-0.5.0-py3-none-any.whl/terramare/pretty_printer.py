"""Pretty-printer for error messages."""

import contextlib
from dataclasses import dataclass
from typing import (
    Any,
    Callable,
    Dict,
    FrozenSet,
    Iterable,
    Iterator,
    List,
    Mapping,
    MutableMapping,
    MutableSequence,
    Sequence,
    Set,
    Tuple,
    Union,
)

from typing_extensions import Literal

from . import type_utils
from .types import Primitive, Target


def print_primitive(
    value: Primitive,
    short: bool = False,
    max_string_length: int = 16,
    max_dict_length: int = 3,
    max_list_length: int = 3,
) -> str:
    """Pretty-print a primitive value."""
    if isinstance(value, str):
        if len(value) > max_string_length:
            value = value[: max_string_length - 3] + "..."
        return f'"{value}"'
    if not value:
        return str(value)
    if isinstance(value, dict):
        if short:
            return "{...}"
        else:
            elts = [
                print_primitive(k) + ": " + print_primitive(v, short=True)
                for k, v in value.items()
            ]
            if len(elts) > max_dict_length:
                elts = elts[: max_dict_length - 1] + ["..."]
            return f"{{{', '.join(elts)}}}"
    if isinstance(value, list):
        if short:
            return "[...]" if value else "[]"
        else:
            elts = [print_primitive(v, short=True) for v in value]
            if len(elts) > max_list_length:
                elts = elts[: max_list_length - 1] + ["..."]
            return f"[{', '.join(elts)}]"
    return str(value)


@dataclass(frozen=True)
class LoggablePrimitive:
    """Lazy formatting for Primitive."""

    _primitive: Primitive

    def __str__(self) -> str:  # pragma: no cover
        return print_primitive(self._primitive)


def print_type_name(type_: Any) -> str:
    """Return the best available user-facing name for a type."""
    overrides: Dict[Target[Any], str] = {
        dict: "dict",
        frozenset: "frozenset",
        set: "set",
        list: "list",
        tuple: "tuple",
    }
    try:
        hash(type_)
    except TypeError:  # pragma: no cover
        pass
    else:
        if type_ in overrides:
            return overrides[type_]
    base = type_utils.get_base_of_generic_type(type_)
    if base in {
        Callable,
        Dict,
        FrozenSet,
        Iterable,
        Iterator,
        Literal,
        List,
        Mapping,
        MutableMapping,
        MutableSequence,
        Sequence,
        Set,
        Tuple,
        Union,
    }:
        parameters = type_utils.get_type_parameters(type_)
        if (
            base is Union
            and len(parameters) == 2
            and parameters[-1] is type(None)  # noqa: E721
        ):
            return f"Optional[{print_type_name(parameters[0])}]"
        return (
            _get_type_name(base)
            + "["
            + ", ".join([print_type_name(t) for t in parameters])
            + "]"
        )
    return _get_type_name(type_)


@dataclass(frozen=True)
class LoggableTarget:
    """Lazy formatting for Target."""

    _target: Target[Any]

    def __str__(self) -> str:  # pragma: no cover
        return f"'{print_type_name(self._target)}'"


def print_table(rows: Sequence[Tuple[str, ...]]) -> str:
    if not rows:
        return ""
    col_nos = list(range(0, max(len(row) for row in rows)))
    col_widths = [
        max(len(row[col_no]) if col_no < len(row) else 0 for row in rows)
        for col_no in col_nos
    ]
    col_nos = [col_no for col_no in col_nos if col_widths[col_no]]
    lines = []
    for row in rows:
        cols = []
        for col_no in col_nos:
            col = ""
            if col_no < len(row):
                col = row[col_no]
            cols.append(f"{col:{col_widths[col_no]}}")
        lines.append("  ".join(cols).strip())
    return "\n".join(lines)


def _get_type_name(type_: Any) -> str:
    overrides = {Any: "Any", Ellipsis: "...", Literal: "Literal", Union: "Union"}
    if type_ in overrides:
        return overrides[type_]
    with contextlib.suppress(AttributeError):  # pragma: no cover TODO
        # pylint: disable=protected-access
        if type_._name is not None:
            return type_._name
    with contextlib.suppress(AttributeError):
        return type_.__name__
    with contextlib.suppress(AttributeError):
        return type_.__qualname__
    if hasattr(type_, "__origin__"):  # pragma: no cover TODO
        return _get_type_name(type_.__origin__)
    return str(type_)
