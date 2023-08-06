"""Terramare-specific metadata for attrs classes."""

import abc
from dataclasses import dataclass, field
from typing import (
    Any,
    Callable,
    ClassVar,
    Dict,
    Generic,
    Iterator,
    Mapping,
    Optional,
    Sequence,
    Tuple,
    TypeVar,
    Union,
    cast,
)

from typing_extensions import final

from .core import ConstructorCore, FactoryCore, InternalFactory
from .errors import TerramareError, UnsupportedTargetTypeError
from .safe_mapping import SafeMapping
from .types import Lazy, Target

_METADATA_FIELD = "__terramare_terramare__"

_T_co = TypeVar("_T_co", covariant=True)
_T_in = TypeVar("_T_in")


@dataclass(frozen=True)
class MetadataError(TerramareError):
    message: str


_Metadata = TypeVar("_Metadata")


def write(target: Target[_T_in], key: str, value: Any) -> Target[_T_in]:
    metadata = _read_from_target(target)
    if not metadata:
        metadata = {}
        setattr(target, _METADATA_FIELD, (metadata, target))
    metadata[key] = value
    return target


TargetMetadata = Sequence[Union["Metadata[Any]", Tuple[str, Any]]]


@dataclass(frozen=True)
class MetadataCollection:
    _metadata: SafeMapping[Target[Any], Mapping[str, Any]] = field(
        default_factory=SafeMapping
    )

    @classmethod
    def new(
        cls, metadata: Mapping[Target[Any], TargetMetadata]
    ) -> "MetadataCollection":
        def normalize(target_metadata: TargetMetadata) -> Iterator[Tuple[str, Any]]:
            for element in target_metadata:
                if isinstance(element, Metadata):
                    yield (element.KEY, element.value)
                else:
                    yield element

        return cls(
            SafeMapping(
                [
                    (target, dict(normalize(target_metadata)))
                    for target, target_metadata in metadata.items()
                ]
            )
        )

    def read(self, target: Target[Any], key: str, default: _Metadata) -> _Metadata:
        if target in self._metadata:
            target_metadata = self._metadata[target]
            if key in target_metadata:
                return cast(_Metadata, target_metadata[key])
        target_metadata = _read_from_target(target)
        if key in target_metadata:
            return cast(_Metadata, target_metadata[key])
        return default


class Metadata(Generic[_Metadata], abc.ABC):
    KEY: ClassVar[str]
    DEFAULT: ClassVar[_Metadata]

    @classmethod
    def read(cls, metadata: MetadataCollection, target: Target[Any]) -> _Metadata:
        return metadata.read(target, cls.KEY, cls.DEFAULT)

    @property
    @abc.abstractmethod
    def value(self) -> _Metadata:
        ...  # pragma: no cover

    def __call__(self, target: Target[_T_in]) -> Target[_T_in]:
        return write(target, self.KEY, self.value)


@dataclass(frozen=True)
class with_(Metadata[Optional[Lazy[Callable[..., Any]]]]):
    """Construct the decorated class using the given function."""

    KEY: ClassVar[str] = f"{__name__}.with_"
    DEFAULT: ClassVar[Optional[Lazy[Callable[..., Any]]]] = None

    _value: Lazy[Callable[..., Any]]

    @property
    def value(self) -> Lazy[Callable[..., Any]]:
        return self._value


@final
@dataclass(frozen=True)
class MetadataFactory(FactoryCore):
    _metadata: MetadataCollection

    def create_constructor(
        self, factory: InternalFactory, target: Target[_T_co]
    ) -> ConstructorCore[_T_co]:
        _with = with_.read(self._metadata, target)
        if _with:
            return factory.create_constructor(
                _with(), context="metadata 'with'"
            ).unwrap()
        raise UnsupportedTargetTypeError


def _read_from_target(target: Target[_T_in]) -> Dict[str, Any]:
    if not hasattr(target, _METADATA_FIELD):
        return {}
    attr = getattr(target, _METADATA_FIELD)
    if not (isinstance(attr, tuple) and isinstance(attr[0], dict)):
        raise MetadataError("unexpected type metadata")
    meta, t = attr
    # Ensure that the metadata was applied to `t` itself, rather than a base
    # class of `t`.
    # This is important because the base class may define metadata that is
    # not appropriate for derived classes, such as tagged polymorphism.
    if target != t:
        return {}
    return meta
