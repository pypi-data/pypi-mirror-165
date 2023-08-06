from dataclasses import dataclass
from typing import Any, ClassVar, Generic, Mapping, Optional, Type, TypeVar

from typing_extensions import final

from .core import ConstructorCore, FactoryCore, InternalConstructor, InternalFactory
from .data import Value
from .errors import UnsupportedTargetTypeError
from .metadata import Metadata, MetadataCollection
from .types import Lazy, Target

_T_co = TypeVar("_T_co", covariant=True)


@dataclass(frozen=True)
class externally_tagged(Metadata[Optional[Lazy[Mapping[str, Target[Any]]]]]):
    """
    Mark the decorated class as an externally-tagged variant type.

    >>> import terramare
    >>> from dataclasses import dataclass
    >>>
    >>> @terramare.externally_tagged(lambda: {"request": Request, "response": Response})
    ... class Message:
    ...     pass
    >>>
    >>> @dataclass
    ... class Request:
    ...     method: str
    >>>
    >>> @dataclass
    ... class Response:
    ...     code: int
    >>>
    >>> terramare.structure({"request": {"method": "GET"}}, into=Message)
    Request(method='GET')
    """

    KEY: ClassVar[str] = f"{__name__}.externally_tagged"
    DEFAULT: ClassVar[Optional[Lazy[Mapping[str, Target[Any]]]]] = None

    _value: Lazy[Mapping[str, Target[Any]]]

    @property
    def value(self) -> Lazy[Mapping[str, Target[Any]]]:
        return self._value


@dataclass(frozen=True)
class internally_tagged(Metadata[Optional["internally_tagged"]]):
    """
    Mark the decorated class as an internally-tagged variant type.

    >>> import terramare
    >>> from dataclasses import dataclass
    >>>
    >>> @terramare.internally_tagged(key="type", variants=lambda: {
    ...     "request": Request, "response": Response
    ... })
    ... class Message:
    ...     pass
    >>>
    >>> @dataclass
    ... class Request:
    ...     method: str
    >>>
    >>> @dataclass
    ... class Response:
    ...     code: int
    >>>
    >>> terramare.structure({"type": "request", "method": "GET"}, into=Message)
    Request(method='GET')
    """

    KEY: ClassVar[str] = f"{__name__}.internally_tagged"
    DEFAULT: ClassVar[Optional["internally_tagged"]] = None

    key: str
    variants: Lazy[Mapping[Any, type]]

    @property
    def value(self) -> "internally_tagged":
        return self


@final
@dataclass(frozen=True)
class TaggedFactory(FactoryCore):
    _metadata: MetadataCollection

    def create_constructor(
        self, factory: InternalFactory, target: Target[_T_co]
    ) -> ConstructorCore[_T_co]:
        externally_tagged_variants = externally_tagged.read(self._metadata, target)
        if externally_tagged_variants:
            return ExternallyTaggedConstructor.new(
                factory, externally_tagged_variants()
            )

        internally_tagged_variants = internally_tagged.read(self._metadata, target)
        if internally_tagged_variants:
            return InternallyTaggedConstructor.new(
                factory,
                internally_tagged_variants.key,
                internally_tagged_variants.variants(),
            )

        raise UnsupportedTargetTypeError


@final
@dataclass(frozen=True)
class ExternallyTaggedConstructor(ConstructorCore[_T_co]):
    _variants: Mapping[str, InternalConstructor[_T_co]]

    @classmethod
    def new(
        cls,
        factory: InternalFactory,
        variants: Mapping[str, Target[_T_co]],
    ) -> "ExternallyTaggedConstructor[_T_co]":
        return cls(
            {
                tag: factory.create_constructor(
                    variant, context=f'externally-tagged variant "{tag}"'
                )
                for tag, variant in variants.items()
            },
        )

    def __call__(self, data: Value) -> _T_co:
        object_data = data.as_object()
        if not object_data:
            raise data.make_error("missing variant")
        if len(object_data) > 1:
            raise data.make_error("multiple variants")
        tag = next(iter(object_data.keys()))
        if tag in self._variants:
            return self._variants[tag](object_data[tag])
        variants_str = ",".join(sorted(self._variants))
        raise data.make_error(
            f"unknown variant ({tag}) - expected one of {{{variants_str}}}"
        )


@final
@dataclass(frozen=True)
class InternallyTaggedConstructor(Generic[_T_co], ConstructorCore[_T_co]):
    _tag_field: str
    _tag_constructor: InternalConstructor[str]
    _variants: Mapping[str, InternalConstructor[_T_co]]

    @classmethod
    def new(
        cls,
        factory: InternalFactory,
        tag_field: str,
        variants: Mapping[str, Type[_T_co]],
    ) -> "InternallyTaggedConstructor[_T_co]":
        return cls(
            tag_field,
            factory.create_constructor(str),
            {
                tag: factory.create_constructor(
                    variant, context=f'internally-tagged variant "{tag}"'
                )
                for tag, variant in variants.items()
            },
        )

    def __call__(self, data: Value) -> _T_co:
        object_data = data.as_object()
        if self._tag_field not in object_data:
            raise data.make_error(f"missing required field: {self._tag_field}")
        tag = self._tag_constructor(object_data[self._tag_field])
        if tag in self._variants:
            del object_data[self._tag_field]
            return self._variants[tag](object_data)
        variants_str = ",".join(sorted(str(v) for v in self._variants))
        raise data.make_error(
            f"unknown variant ({tag}) - expected one of {{{variants_str}}}"
        )
