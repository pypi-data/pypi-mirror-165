"""Automatically construct complex objects from simple Python types."""

import pkg_resources

from .classes import auto, disallow_unknown_fields, handle_exception_types
from .errors import ConstructorError, FactoryError, TerramareError
from .metadata import with_
from .tagged_constructors import externally_tagged, internally_tagged
from .terramare import structure

# Attempt to expose the package version as __version__ (see PEP 396).
try:
    __version__ = pkg_resources.get_distribution(__name__).version
except pkg_resources.DistributionNotFound:  # pragma: no cover
    pass


__all__ = [
    "ConstructorError",
    "FactoryError",
    "TerramareError",
    "auto",
    "disallow_unknown_fields",
    "externally_tagged",
    "handle_exception_types",
    "internally_tagged",
    "structure",
    "with_",
]
