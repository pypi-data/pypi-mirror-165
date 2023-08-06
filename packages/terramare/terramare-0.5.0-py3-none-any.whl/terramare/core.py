import abc
import dataclasses
import logging
from dataclasses import dataclass, field
from typing import (
    TYPE_CHECKING,
    Any,
    Generic,
    Mapping,
    Optional,
    Sequence,
    Tuple,
    TypeVar,
    overload,
)

from typing_extensions import final

from .data import ConstructionConfig, Value
from .errors import FactoryError, InternalError, TerramareError
from .pretty_printer import (
    LoggablePrimitive,
    LoggableTarget,
    print_table,
    print_type_name,
)
from .safe_mapping import SafeMutableMapping
from .types import Primitive, Target

if TYPE_CHECKING:  # pragma: no cover
    from .metadata import TargetMetadata

_log = logging.getLogger(__name__)

_T_co = TypeVar("_T_co", covariant=True)


@dataclass(frozen=True)
class InternalFactoryError(TerramareError):
    """Internal exception raised when failing to create a constructor."""

    summary: str
    detail: str


class ConstructorCore(Generic[_T_co], abc.ABC):
    """
    Interface for constructor implementations.

    This should not be used directly - instead, use:
    - the InternalConstructor wrapper class, if constructing a sub-object from
      another constructor;
    - the public Constructor class, if constructing a top-level object.
    """

    @abc.abstractmethod
    def __call__(self, data: "Value") -> _T_co:
        """
        Create an instance of the target type.

        :param data: Primitive value from which to construct an instance of the
            target type.

        :returns: Instance of the target type.

        :raises terramare.errors.ConstructorError: If the primitive value has
            an incorrect type or structure.
        :raises terramare.errors.ValidationException: If the primitive value has
            the correct type and structure but fails value-level validation.
        """


@final
@dataclass
class ForwardRef(ConstructorCore[_T_co]):
    """
    Forward reference to a ConstructorCore.

    This is necessary to create constructors for recursive types. For example,
    consider:

    @dataclass
    class LinkedList:
        next: Optional["LinkedList"] = None

    With a naive implementation we would not be able to create a LinkedList
    constructor without already having a LinkedList constructor!

    A ForwardRef can be returned in place of a constructor from
    `create_constructor` when it is called with a target type from within a
    call to `create_constructor` for that type.

    All instances of the ForwardRef are then resolved to a real constructor
    before returning from the earlier call to `create_constructor`.

    For example, calling `create_constructor(LinkedList)` as part of creating a
    constructor for the `next` field of LinkedList will return a ForwardRef,
    preventing infinite recursion.

    By the time a constructor is returned from the top-level `create_constructor`
    call this ForwardRef has been resolved - the same constructor is used for
    constructing a top-level LinkedList instance _and_ its `next` member.
    """

    _impl: Optional[ConstructorCore[_T_co]] = None

    def __call__(self, data: "Value") -> _T_co:
        """
        Call the referenced constructor.

        See `ConstructorCore.__call__`.

        :raises InternalError: If the ForwardRef has not been resolved.
        """
        return self.deref()(data)

    def resolve_to(self, impl: ConstructorCore[_T_co]) -> None:
        """Resolve the forward reference to the given real constructor."""
        self._impl = impl

    def deref(self) -> ConstructorCore[_T_co]:
        """
        Retrieve the referenced constructor.

        :raises InternalError: If the ForwardRef has not been resolved.
        """
        if self._impl is None:  # pragma: no cover
            raise InternalError(
                f"attempted to dereference unresolved forward reference {id(self):x}"
            )
        return self._impl


@final
@dataclass
class InternalConstructor(Generic[_T_co]):
    """
    Internal-only wrapper class for constructor implementations.

    Provides logging, error context, and forward reference handling.
    """

    _impl: ConstructorCore[_T_co]
    _target: Target[_T_co]

    def __call__(self, data: "Value") -> _T_co:
        """
        Create an instance of the target type.

        See `ConstructorCore.__call__`.
        """
        if isinstance(self._impl, ForwardRef):
            self._impl = self._impl.deref()
        _log.debug(
            "Attempting to construct %s from data: %s",
            LoggableTarget(self._target),
            LoggablePrimitive(data.raw),
        )
        value = self._impl(data.clone().with_context(print_type_name(self._target)))
        _log.debug(
            "Constructed %s: %s",
            LoggableTarget(self._target),
            value,
        )
        return value

    def __str__(self) -> str:  # pragma: no cover
        """Return a human-readable representation of the constructor."""
        return f"Constructor[{print_type_name(self._target)}]"

    def unwrap(self) -> ConstructorCore[_T_co]:
        """Retrieve the wrapped ConstructorCore."""
        return self._impl


class FactoryCore(abc.ABC):
    """
    Interface for constructor factory implementations.

    This should not be used directly - instead, use:
    - the InternalFactory wrapper class, if creating a sub-constructor from
      another constructor factory;
    - the public Factory class, if creating a top-level constructor.
    """

    @abc.abstractmethod
    def create_constructor(
        self, factory: "InternalFactory", target: Target[_T_co]
    ) -> ConstructorCore[_T_co]:
        """
        Create a constructor for the given target type.

        :param factory: Constructor factory used when recursively creating sub-
            constructors.
        :param target: Target type.

        :returns: A `ConstructorCore` targeting the given type.

        :raises InternalFactoryError: If a constructor for the given target type
            cannot be created due to fundamental problems with the target type.
        :raises UnsupportedTargetTypeError: If a constructor for the given
            target type cannot be created by this factory, but another factory
            may be able to create such a constructor.
        """


@final
@dataclass(frozen=True)
class InternalFactory:
    """
    Internal-only wrapper class for constructor factory implementations.

    Provides logging, error context, caching and forward reference handling.

    A new instance of this class is created with each `create_constructor` call,
    including recursive calls. New instances share the persistent data of the
    parent instance.
    """

    _persistent_data: "PersistentData"
    _context: Sequence[Tuple[str, str]] = field(default_factory=list)

    @dataclass(frozen=True)
    class PersistentData:
        """Persistent data shared between recursive `create_constructor` calls."""

        impl: FactoryCore
        cache: SafeMutableMapping[Target[Any], InternalConstructor[Any]] = field(
            default_factory=SafeMutableMapping
        )

    def create_constructor(
        self, target: Target[_T_co], *, context: str = ""
    ) -> InternalConstructor[_T_co]:
        """
        Create a constructor for the given target type.

        :param target: Target type.
        :param context: Additional context for the constructor, such as an enum
            variant index.

        :returns: An `InternalConstructor` targeting the given type.

        :raises InternalFactoryError: If a constructor for the given target type
            cannot be created due to fundamental problems with the target type.
        :raises UnsupportedTargetTypeError: If a constructor for the given
            target type cannot be created by this factory, but another factory
            may be able to create such a constructor.
        """
        _log.debug(
            "Attempting to create constructor for target %s",
            LoggableTarget(target),
        )

        def create() -> ConstructorCore[_T_co]:
            return self._persistent_data.impl.create_constructor(
                self.add_context(target, context=context), target
            )

        if target not in self._persistent_data.cache:
            _log.debug("Cache miss for target %s", LoggableTarget(target))
            forward_ref: ForwardRef[_T_co] = ForwardRef()
            _log.debug(
                "Created ForwardRef %x for target %s",
                id(forward_ref),
                LoggableTarget(target),
            )
            self._persistent_data.cache[target] = InternalConstructor(
                forward_ref, target
            )
            try:
                constructor = create()
            except BaseException:
                # Remove the unresolved forward reference.
                del self._persistent_data.cache[target]
                raise
            forward_ref.resolve_to(constructor)
            _log.debug(
                "ForwardRef %x for target %s resolved to %s",
                id(forward_ref),
                LoggableTarget(target),
                constructor,
            )
            _log.debug("Cached constructor for target %s", LoggableTarget(target))
        _log.debug(
            "Retrieved constructor from cache for target %s",
            LoggableTarget(target),
        )
        return self._persistent_data.cache[target]

    def make_error(self, msg: str) -> InternalFactoryError:
        """
        Create an `InternalFactoryError` with the given message.

        The error will contain additional context including the stack of target
        types.
        """
        return InternalFactoryError(
            msg, print_table([("path", "type"), *self._context])
        )

    def add_context(
        self, target: Target[_T_co], *, context: str = ""
    ) -> "InternalFactory":
        return dataclasses.replace(
            self, _context=[*self._context, (context, print_type_name(target))]
        )


@final
@dataclass(frozen=True)
class Factory:
    _persistent_data: InternalFactory.PersistentData = field(
        # pylint: disable=unnecessary-lambda
        default_factory=lambda: Factory._make_persistent_data()
    )

    @classmethod
    def new(
        cls,
        *,
        _experimental_metadata: Optional[Mapping[Target[Any], "TargetMetadata"]] = None,
    ) -> "Factory":
        return cls(
            cls._make_persistent_data(_experimental_metadata=_experimental_metadata)
        )

    @overload
    def create_constructor(self, target: Target[_T_co]) -> "Constructor[_T_co]":
        # See terramare.py for an explanation of the overloads here.
        ...  # pragma: no cover

    @overload
    def create_constructor(self, target: Any) -> "Constructor[Any]":
        ...  # pragma: no cover

    def create_constructor(self, target: Any) -> "Constructor[_T_co]":
        factory = InternalFactory(self._persistent_data)
        try:
            constructor = factory.create_constructor(target)
        except InternalFactoryError as e:
            raise FactoryError(
                f"failed to create constructor for type '{print_type_name(target)}': "
                f"{e.summary}\n{e.detail}"
            ) from e
        return Constructor(constructor)

    @overload
    def structure(
        self, data: Primitive, *, into: Target[_T_co], coerce_strings: bool = False
    ) -> _T_co:
        # See terramare.py for an explanation of the overloads here.
        ...  # pragma: no cover

    @overload
    def structure(
        self, data: Primitive, *, into: Any, coerce_strings: bool = False
    ) -> Any:
        ...  # pragma: no cover

    def structure(
        self, data: Primitive, *, into: Any, coerce_strings: bool = False
    ) -> Any:
        return self.create_constructor(into)(data, coerce_strings=coerce_strings)

    @staticmethod
    def _make_persistent_data(
        *,
        _experimental_metadata: Optional[Mapping[Target[Any], "TargetMetadata"]] = None,
    ) -> InternalFactory.PersistentData:
        # pylint: disable=import-outside-toplevel, cyclic-import
        from .classes import ClassFactory
        from .composite import CompositeFactory
        from .enums import EnumFactory, LiteralFactory
        from .mappings import MappingFactory, TypedDictFactory
        from .metadata import MetadataCollection, MetadataFactory
        from .newtypes import NewTypeFactory
        from .primitives import (
            AnyFactory,
            BoolFactory,
            FloatFactory,
            IntFactory,
            NoneFactory,
            PrimitiveDictFactory,
            PrimitiveListFactory,
            StrFactory,
        )
        from .sequences import SequenceFactory, TupleFactory
        from .stdlib_metadata import DEFAULT_METADATA
        from .tagged_constructors import TaggedFactory
        from .unions import UnionFactory

        metadata = MetadataCollection.new(
            {**DEFAULT_METADATA, **(_experimental_metadata or {})}
        )

        return InternalFactory.PersistentData(
            CompositeFactory(
                [
                    MetadataFactory(metadata),
                    TaggedFactory(metadata),
                    NewTypeFactory(),
                    NoneFactory(),
                    BoolFactory(),
                    IntFactory(),
                    FloatFactory(),
                    StrFactory(),
                    PrimitiveListFactory(),
                    PrimitiveDictFactory(),
                    AnyFactory(),
                    EnumFactory(),
                    LiteralFactory(),
                    SequenceFactory(),
                    TupleFactory(),
                    MappingFactory(),
                    TypedDictFactory(),
                    UnionFactory(),
                    ClassFactory(metadata),
                ]
            )
        )


@final
@dataclass(frozen=True)
class Constructor(Generic[_T_co]):
    _impl: InternalConstructor[_T_co]

    def __call__(self, data: Primitive, *, coerce_strings: bool = False) -> _T_co:
        if not _is_primitive(data):
            raise TypeError("unsupported type for 'data': expected Primitive")
        if not isinstance(coerce_strings, bool):
            raise TypeError("unsupported type for 'coerce_strings': expected bool")
        return self._impl(
            Value.new(data, ConstructionConfig(coerce_strings=coerce_strings))
        )


def _is_primitive(data: Any) -> bool:
    if data is None:
        return True
    if isinstance(data, (bool, int, float, str)):
        return True
    if isinstance(data, list):
        return all(_is_primitive(element) for element in data)
    if isinstance(data, dict):
        return all(
            isinstance(key, str) and _is_primitive(value) for key, value in data.items()
        )
    return False
