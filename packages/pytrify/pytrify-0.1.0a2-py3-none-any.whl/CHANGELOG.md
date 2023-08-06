# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a
Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to
the [PEP 440 version scheme](https://peps.python.org/pep-0440/#version-scheme).

## [v0.1.0-alpha2]
### Changed
- Use tuple instead of ListView for pytrified sequences.
- pytrified Sequences are JSON serializable.

### Fixed
- TypeError when attempting to access `__class__` on pytrified object.


## [v0.1.0-alpha1]
### Added
- pytrify()
- ImmutableAttributeError
- ListView
- SetOnce
- Unit test suite
