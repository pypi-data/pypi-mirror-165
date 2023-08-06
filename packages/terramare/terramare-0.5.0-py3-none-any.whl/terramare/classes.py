"""Deserializer factory for a generic class."""

import dataclasses
import enum
import logging
from dataclasses import dataclass
from typing import (
    AbstractSet,
    Any,
    ClassVar,
    Dict,
    List,
    Mapping,
    Optional,
    Sequence,
    Tuple,
    Type,
    TypeVar,
    Union,
    overload,
)

from typing_extensions import Final, final

from . import type_utils
from .core import ConstructorCore, FactoryCore, InternalConstructor, InternalFactory
from .data import Value
from .errors import UnsupportedTargetTypeError, ValidationException
from .metadata import Metadata, MetadataCollection
from .pretty_printer import LoggableTarget
from .types import Target

_log = logging.getLogger(__name__)

_T_co = TypeVar("_T_co", covariant=True)
_T_in = TypeVar("_T_in")


@dataclass(frozen=True)
class _disallow_unknown_fields(Metadata[bool]):

    KEY: ClassVar[str] = f"{__name__}.allow_unknown_fields"
    DEFAULT: ClassVar[bool] = False

    @property
    def value(self) -> bool:
        return True


#: Raise :exc:`terramare.errors.ConstructorError` if there are fields present in
#: the primitive that are not defined by the decorated class.
disallow_unknown_fields = _disallow_unknown_fields()


@dataclass(init=False)
class handle_exception_types(Metadata[Tuple[Type[Exception], ...]]):
    """
    Handle the listed exception types when constructing an instance of the decorated class.

    An exception of one of these types will be caught and re-raised as a
    :exc:`terramare.errors.ValidationError` including the full construction
    context.

    >>> import attr
    >>> import terramare
    >>>
    >>> @terramare.handle_exception_types(ValueError)
    ... @attr.s(auto_attribs=True)
    ... class User:
    ...     id: int = attr.ib()
    ...     name: str
    ...
    ...     @id.validator
    ...     def positive(self, _, value):
    ...         if not value > 0:
    ...             raise ValueError("id must be positive!")
    >>>
    >>> terramare.structure({"id": 0, "name": "Alice"}, into=User)
    Traceback (most recent call last):
    ...
    terramare.errors.ConstructorError: .: id must be positive!
    ...
    """

    KEY: ClassVar[str] = f"{__name__}.handle_exception_types"
    DEFAULT: ClassVar[Tuple[Type[Exception], ...]] = ()

    _value: Tuple[Type[Exception], ...]

    @property
    def value(self) -> Tuple[Type[Exception], ...]:
        return self._value

    def __init__(self, *exceptions: Type[Exception]) -> None:
        self._value = exceptions


@enum.unique
class _FromType(enum.Enum):
    OBJECT = "object"
    ARRAY = "array"
    LEAF = "leaf"


FromType = AbstractSet[_FromType]

OBJECT: Final = frozenset({_FromType.OBJECT})
ARRAY: Final = frozenset({_FromType.ARRAY})
VALUE: Final = frozenset({_FromType.LEAF})

_AUTO_KEY: Final[str] = f"{__name__}.auto"


@dataclass(frozen=True)
class _auto(Metadata[Optional[FromType]]):
    KEY: ClassVar[str] = _AUTO_KEY
    DEFAULT: ClassVar[Optional[FromType]] = None

    @dataclass(frozen=True)
    class inner(Metadata[Optional[FromType]]):
        KEY: ClassVar[str] = _AUTO_KEY
        DEFAULT: ClassVar[Optional[FromType]] = None

        _value: FromType

        @property
        def value(self) -> FromType:
            return self._value

    @property
    def value(self) -> FromType:
        return OBJECT

    @overload
    def __call__(self, *, from_: FromType) -> "_auto.inner":
        ...  # pragma: no cover

    @overload
    def __call__(self, target: Target[_T_in]) -> Target[_T_in]:
        ...  # pragma: no cover

    def __call__(
        self,
        target: Optional[Target[_T_in]] = None,
        *,
        from_: Optional[FromType] = None,
    ) -> Union["_auto.inner", Target[_T_in]]:
        if from_ is not None:
            return _auto.inner(from_)
        assert target is not None
        return _auto.inner(self.value)(target)


#: Automatically create a constructor for the decorated class.
auto = _auto()


@final
@dataclass(frozen=True)
class ClassFactory(FactoryCore):
    _metadata: MetadataCollection

    @dataclass(frozen=True)
    class _Constructor(ConstructorCore[_T_co]):
        _from_object: Optional[ConstructorCore[_T_co]]
        _from_array: Optional[ConstructorCore[_T_co]]
        _from_value: Optional[ConstructorCore[_T_co]]
        _handle_exception_types: Tuple[Type[Exception], ...]

        def __call__(self, data: "Value") -> _T_co:
            def get_constructor() -> Optional[ConstructorCore[_T_co]]:
                if data.is_object() and self._from_object:
                    return self._from_object
                if data.is_array() and self._from_array:
                    return self._from_array
                return self._from_value

            constructor = get_constructor()
            if not constructor:
                constructors = []
                if self._from_object:
                    constructors.append("object")
                if self._from_array:
                    constructors.append("array")
                raise data.make_error(f"expected {' or '.join(constructors)}")
            try:
                return constructor(data)
            except self._handle_exception_types as e:
                raise data.make_error(str(e)) from e

    def create_constructor(
        self, factory: InternalFactory, target: Target[_T_co]
    ) -> ConstructorCore[_T_co]:
        if not hasattr(target, "__call__"):
            raise UnsupportedTargetTypeError

        try:
            type_utils.get_parameters(target)
        except type_utils.ParameterError as e:
            raise factory.make_error(str(e))

        fromtypes = _get_fromtypes(self._metadata, target)
        if not fromtypes:
            raise factory.make_error("class construction not enabled for target")

        from_object = None
        if OBJECT <= fromtypes:
            from_object = self._create_from_object_constructor(factory, target)

        from_array = None
        if ARRAY <= fromtypes:
            from_array = self._create_from_array_constructor(factory, target)

        from_value = None
        if VALUE <= fromtypes:
            from_value = self._create_from_value_constructor(factory, target)

        return type(self)._Constructor(
            _from_object=from_object,
            _from_array=from_array,
            _from_value=from_value,
            _handle_exception_types=(
                ValidationException,
                *handle_exception_types.read(self._metadata, target),
            ),
        )

    @dataclass(frozen=True)
    class _FromObjectConstructor(ConstructorCore[_T_co]):
        _required_fields: Mapping[str, InternalConstructor[Any]]
        _optional_fields: Mapping[str, InternalConstructor[Any]]
        _variadic_fields: Optional[InternalConstructor[Any]]
        _target: Target[_T_co]
        _disallow_unknown_fields: bool

        def __call__(self, data: Value) -> _T_co:
            object_data = data.as_object()
            arguments: Dict[str, Any] = {}

            for field_, constructor in self._required_fields.items():
                if field_ not in object_data:
                    raise data.make_error(f"missing required field: {field_}")
                arguments[field_] = constructor(object_data[field_])

            for field_, constructor in self._optional_fields.items():
                if field_ in object_data:
                    arguments[field_] = constructor(object_data[field_])

            if self._variadic_fields:
                for field_ in object_data:
                    if field_ in arguments:
                        continue
                    arguments[field_] = self._variadic_fields(object_data[field_])

            unused_fields = set(object_data) - set(arguments)
            if self._disallow_unknown_fields and unused_fields:
                raise data.make_error(f"unknown field: {sorted(unused_fields)[0]}")

            _log.debug(
                "Instantiating %s with arguments: %s",
                LoggableTarget(self._target),
                arguments,
            )
            return self._target(**arguments)  # type: ignore[call-arg]

    def _create_from_object_constructor(
        self, factory: InternalFactory, target: Target[_T_co]
    ) -> ConstructorCore[_T_co]:
        parameters = type_utils.get_parameters(target)
        if any(
            p.is_positional_only() and p.is_required() for p in parameters
        ):  # pragma: no cover
            # Covered on Python >3.6 only.
            raise factory.make_error(
                "cannot create from-object constructor for target with required "
                "positional-only parameters"
            )

        type_hints = type_utils.get_type_hints(target, parameters)

        variadic_fields = None
        for parameter in parameters:
            if parameter.is_keyword() and parameter.is_variadic():
                variadic_fields = factory.create_constructor(
                    type_hints[parameter.name], context=f'field "{parameter.name}"'
                )
                break

        return type(self)._FromObjectConstructor(
            _required_fields={
                p.name: factory.create_constructor(
                    type_hints[p.name], context=f'field "{p.name}"'
                )
                for p in parameters
                if p.is_keyword() and p.is_required()
            },
            _optional_fields={
                p.name: factory.create_constructor(
                    type_hints[p.name], context=f'field "{p.name}"'
                )
                for p in parameters
                if p.is_keyword() and p.is_optional()
            },
            _variadic_fields=variadic_fields,
            _target=target,
            _disallow_unknown_fields=disallow_unknown_fields.read(
                self._metadata, target
            ),
        )

    @dataclass(frozen=True)
    class _FromArrayConstructor(ConstructorCore[_T_co]):
        _required_elements: Sequence[InternalConstructor[Any]]
        _optional_elements: Sequence[InternalConstructor[Any]]
        _variadic_elements: Optional[InternalConstructor[Any]]
        _target: Target[_T_co]
        _disallow_extra_elements: bool

        def __call__(self, data: Value) -> _T_co:
            array_data = data.as_array()
            arguments: List[Any] = []

            index = 0
            for index, constructor in enumerate(self._required_elements):
                if index == len(array_data):
                    raise data.make_error(
                        f"too few elements ({len(array_data)}) - "
                        f"expected at least {len(self._required_elements)} "
                    )
                arguments.append(constructor(array_data[index]))

            for index, constructor in enumerate(self._optional_elements, index + 1):
                if index == len(array_data):
                    break
                arguments.append(constructor(array_data[index]))

            if self._variadic_elements:
                for index in range(index + 1, len(array_data)):
                    arguments.append(self._variadic_elements(array_data[index]))

            if self._disallow_extra_elements and len(array_data) > len(arguments):
                max_elements = len(self._required_elements) + len(
                    self._optional_elements
                )
                raise data.make_error(
                    f"too many elements ({len(array_data)}) - "
                    f"expected at most {max_elements}"
                )

            _log.debug(
                "Instantiating %s with arguments: %s",
                LoggableTarget(self._target),
                arguments,
            )
            return self._target(*arguments)  # type: ignore[call-arg]

    def _create_from_array_constructor(
        self, factory: InternalFactory, target: Target[_T_co]
    ) -> ConstructorCore[_T_co]:
        parameters = type_utils.get_parameters(target)
        if any(p.is_keyword_only() and p.is_required() for p in parameters):
            raise factory.make_error(
                "cannot create from-object constructor for target with required "
                "keyword-only parameters"
            )

        type_hints = type_utils.get_type_hints(target, parameters)

        variadic_fields = None
        for parameter in parameters:
            if parameter.is_positional() and parameter.is_variadic():
                variadic_fields = factory.create_constructor(
                    type_hints[parameter.name], context=f'field "{parameter.name}"'
                )
                break

        return type(self)._FromArrayConstructor(
            _required_elements=[
                factory.create_constructor(
                    type_hints[p.name], context=f'field "{p.name}"'
                )
                for p in parameters
                if p.is_positional() and p.is_required()
            ],
            _optional_elements=[
                factory.create_constructor(
                    type_hints[p.name], context=f'field "{p.name}"'
                )
                for p in parameters
                if p.is_positional() and p.is_optional()
            ],
            _variadic_elements=variadic_fields,
            _target=target,
            _disallow_extra_elements=disallow_unknown_fields.read(
                self._metadata, target
            ),
        )

    @dataclass(frozen=True)
    class _FromValueConstructor(ConstructorCore[_T_co]):
        _leaf_constructor: InternalConstructor[Any]
        _target: Target[_T_co]

        def __call__(self, data: Value) -> _T_co:
            argument = self._leaf_constructor(data)
            _log.debug(
                "Instantiating %s with argument: %s",
                LoggableTarget(self._target),
                argument,
            )
            return self._target(argument)  # type: ignore[call-arg]

    def _create_from_value_constructor(
        self,
        factory: InternalFactory,
        target: Target[_T_co],
    ) -> ConstructorCore[_T_co]:
        # pylint: disable=protected-access
        parameters = type_utils.get_parameters(target)
        if not parameters:
            raise factory.make_error(
                "cannot create from-value constructor for target with no parameters"
            )
        required = [p for p in parameters if p.is_required()]
        if len(required) > 1:
            raise factory.make_error(
                "cannot create from-value constructor for target "
                "with more than one required parameter"
            )
        if len(required) == 1:
            [parameter] = required
            if parameter.is_keyword_only():
                raise factory.make_error(
                    "cannot create from-value constructor for "
                    "target with required keyword-only parameter"
                )
        else:
            # No required parameters and at least one optional parameter.
            parameters = [p for p in parameters if p.is_positional()]
            if not parameters:
                raise factory.make_error(
                    "cannot create from-value constructor for "
                    "target with no positional parameters"
                )
            parameter = parameters[0]

        type_hints = type_utils.get_type_hints(target, [parameter])
        return type(self)._FromValueConstructor(
            factory.create_constructor(
                type_hints[parameter.name], context=f'field "{parameter.name}"'
            ),
            _target=target,
        )


def _get_fromtypes(metadata: MetadataCollection, target: Target[Any]) -> FromType:
    from_types = auto.read(metadata, target)
    if from_types is not None:
        return from_types
    if dataclasses.is_dataclass(target) or hasattr(target, "__attrs_attrs__"):
        return OBJECT
    if _is_namedtuple(target):
        return OBJECT | ARRAY
    return frozenset()


def _is_namedtuple(target: Target[_T_co]) -> bool:
    if getattr(target, "__bases__", None) != (tuple,):
        return False
    fields = getattr(target, "_fields", None)
    return isinstance(fields, tuple) and all(isinstance(field, str) for field in fields)
