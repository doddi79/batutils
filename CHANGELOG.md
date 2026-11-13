# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [2.2.1] - 2026-11-13

### Added

- A task-oriented public API index in `docs/api-index.md`, linked from the README
- Documentation of the constants and `DeltaSplit` in the `dtu` README, which
  also now covers timestamp/instant casting and the parsers

### Changed

- Tidied up the main README and replaced the stub `tpu` README with an overview


## [2.2.0] - 2026-04-26

### Added

- New method to `batutils.tpu.casting` called `enum_value_lookup_map` that returns a value to Enum member dict that 
  also supports multi-value Enums by including each individual value in the dict as a key, as well as the value tuple 
  itself.
- Support for multi-value Enums to `enum_eval` and `EnumEx`
- Official support (as in: unit tests) for Python 3.13 and 3.14
- Super basic unittests for `instant_to_datetime` and `timestamp_to_datetime` 
  cause there was a super dumb error which those would have caught 

### Changed

- The unittest for `any_to_datetime` to account for "instant"

### Removed

- Official support for Python 3.8 and 3.9 (as in: removed from unit tests)

### Fixed

- The `any_to_datetime` call where it's accidentally casting "instant" to 
  "timestamp"


## [2.1.0] - 2025-08-31

### Added

- Support for enum alias values to `enum_eval` (multiple names with same value).


## [2.0.0] - 2024-11-14

Forked and renamed!!

### Added

- This project by forking [`ccptools`](https://github.com/ccpgames/ccptools)
