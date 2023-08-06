"""Deserializer for a newtype alias."""

from typing import TypeVar

from .core import ConstructorCore, FactoryCore, InternalFactory
from .errors import UnsupportedTargetTypeError
from .types import Target

_T_co = TypeVar("_T_co", covariant=True)


class NewTypeFactory(FactoryCore):
    def create_constructor(
        self, factory: "InternalFactory", target: Target[_T_co]
    ) -> ConstructorCore[_T_co]:
        if not getattr(target, "__qualname__", None) == "NewType.<locals>.new_type":
            raise UnsupportedTargetTypeError
        return factory.create_constructor(getattr(target, "__supertype__")).unwrap()
