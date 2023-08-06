# Changelog

This file documents all notable changes to the project.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
Commit messages and changelog entries should follow the [Conventional Commits](https://www.conventionalcommits.org) specification.

## [Unreleased]

## [0.5.0] - 2022-08-28

### Breaking Changes
- feat!: A major rewrite of the interface and the internals:
  - The `deserialize_into` function is removed and replaced by the `structure` function.
    The interface of the function has changed significantly - see the documentation for details.
  - The `DeserializationError` exception is replaced by the `ConstructorError` exception.
  - The `DeserializerFactoryError` exception is replaced by the `FactoryError` exception.
  - The `experimental` module is removed entirely.
  - The following decorators are added:
    - `auto`, for marking classes as constructable by `terramare`.
    - `disallow_unknown_fields`, for raising exceptions when unexpected fields are encountered.
    - `externally_tagged` and `internally_tagged`, for constructing variant types.
    - `handle_exception_types`, for catching and re-raising validation exceptions.
    - `with_`, for implementing custom construction.

## [0.4.3] - 2021-02-04

### Fixed

- fix: Clarify error messages produced by a class deserializer when only one `from_` type is available.
- fix: Sort keys in missing/unexpected key error messages.
- fix: Expose `terramare.experimental` module in `__all__`.
- fix: Handle empty mapping in `terramare.experimental.keyed` metadata.

## [0.4.2] - 2021-02-02

### Changed

- docs: Update docs theme.

## [0.4.1] - 2020-10-07

### Fixed

- chore: Add `py.typed` file to mark the package as [PEP 561](https://www.python.org/dev/peps/pep-0561/) compliant.
  This allows `mypy` to typecheck code using this package.
- fix: Correct some type hints on the public interface.
- fix: Actually apply the key deserializer when deserializing a mapping type (e.g. `Dict`).
  Mapping types with string keys are unaffected.

## [0.4.0] - 2020-08-15

### Added

- feat: Support for Python 3.9
- feat(experimental): `keyed`, `from_`, and `with_` metadata decorators
- feat: Deserialization support for a handful of standard library types

### Changed

- feat: Rework error handling to produce more readable error messages
- feat(experimental): The `keyed` metadata is renamed to `Keyed`

### Removed

- feat(experimental): Removed support for attrs metadata
- feat!: Removed `handle_reentrancy` keyword argument to `terramare.deserialize_into`.
  `terramare.DeserializationError` should be passed to `handle_exception_types` instead.
- feat!: Deserializers are no longer created by default for arbitrary classes:
  - List and dictionary deserializers are created for `NamedTuple`-based classes;
  - Dictionary deserializers are created for dataclasses and `attrs`-based classes;
  - Deserializers may be created for arbitrary classes or functions annotated with the `from_` metadata.

## [0.3.6] - 2020-05-25

### Added

- feat(experimental): Pass type metadata to `terramare.deserialize_into` via the `_experimental_metadata` keyword argument

### Fixed

- fix: Improve error message when attempting to create a `KeyedDeserializer` with an empty mapping

## [0.3.5] - 2020-05-17

### Added

- feat: Deserialize `TypedDict` types
- feat: `experimental` module containing experimental features to which breaking changes to be made without warning.
  See the "Experimental Features" page in the documentation for more details.
- feat: Experimental `keyed` metadata allowing for a dictionary to be deserialized based on the value of one of its keys

### Removed

- chore: Removed CachingDeserializerFactory

## [0.3.4] - 2020-03-25

### Fixed

- fix: Provide more useful errors when `coerce_strings` is used with non-string leaf primitives (`bool`, `int`, and `float`)

## [0.3.3] - 2020-03-23

### Fixed

- fix: Avoid mistakenly omitting useful information from some error messages

## [0.3.2] - 2020-03-16

### Fixed

- fix: Use standard caret requirement for Python version in pyproject.toml

## [0.3.1] - 2020-03-16

### Changed

- chore: Specify license in package metadata

## [0.3.0] - 2020-03-15

### Added

- feat: Add `deserialize_into` keyword arguments:
  - `handle_exception_types`, allowing `terramare` to catch and handle custom exceptions, e.g.
    those raised by additional validation on a class;
  - `handle_reentrancy`, controlling how `terramare` handles deserialzation targets that themselves
    call into `terramare`.
- feat: Add support for variadic tuples
- feat: Add support for `functools.partial`
- docs: Usage guide

### Changed

- refactor: Extract common deserializer logic into "deserializer combinators" and use throughout.
- improvement: Improve class deserialization error messages

### Fixed

- docs: Document public API only

### Removed

- refactor!: Remove `create_deserializer` and `create_deserializer_factory` functions from public API

## [0.2.0] - 2020-02-09

### Added

- test: Test for simple forward reference type
- feat: Deserialize enum types
- feat: Optionally coerce strings to `int`, `float`, or `bool` where the latter are required
- feat: Deserialize `Set`, `FrozenSet`, `Iterable` and `Iterator` types

### Changed

- chore(infra): Enable linters in vscode
- improvement: Improve handling of forward references
- improvement: Improve error messages
- feat: Create class deserializers in more situations

### Fixed

- fix: Fix `AttributeError` on querying description of `Any` deserializer
- fix: Fix type name in `ClassDeserializerFactoryError`
- fix: Fix inadvertantly persisting state between `CachingDeserializerFactory` instances
- fix: Raise correct error when re-raising `InternalDeserializationError`

## [0.1.0] - 2019-10-11

### Added

- Initial version

[Unreleased]: https://gitlab.com/tomwatson1024/terramare/compare/0.5.0...master
[0.4.4]: https://gitlab.com/tomwatson1024/terramare/compare/0.4.3...0.5.0
[0.4.3]: https://gitlab.com/tomwatson1024/terramare/compare/0.4.2...0.4.3
[0.4.2]: https://gitlab.com/tomwatson1024/terramare/compare/0.4.1...0.4.2
[0.4.1]: https://gitlab.com/tomwatson1024/terramare/compare/0.4.0...0.4.1
[0.4.0]: https://gitlab.com/tomwatson1024/terramare/compare/0.3.6...0.4.0
[0.3.6]: https://gitlab.com/tomwatson1024/terramare/compare/0.3.5...0.3.6
[0.3.5]: https://gitlab.com/tomwatson1024/terramare/compare/0.3.4...0.3.5
[0.3.4]: https://gitlab.com/tomwatson1024/terramare/compare/0.3.3...0.3.4
[0.3.3]: https://gitlab.com/tomwatson1024/terramare/compare/0.3.2...0.3.3
[0.3.2]: https://gitlab.com/tomwatson1024/terramare/compare/0.3.1...0.3.2
[0.3.1]: https://gitlab.com/tomwatson1024/terramare/compare/0.3.0...0.3.1
[0.3.0]: https://gitlab.com/tomwatson1024/terramare/compare/0.2.0...0.3.0
[0.2.0]: https://gitlab.com/tomwatson1024/terramare/compare/0.1.0...0.2.0
[0.1.0]: https://gitlab.com/tomwatson1024/terramare/-/tags/0.1.0
