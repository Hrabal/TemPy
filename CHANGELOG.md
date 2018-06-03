# TemPy Changelog

All notable changes to this project will be documented in this file.

This changelog starts from version 1.0.0, previous versions are considered beta versions.

## [1.2.0](https://github.com/Hrabal/TemPy/compare/6cde4add75bcde5c23614573980caf7684bae76b...master) - 2018-06-03

### Added
- `T.from_markdown(some_markdown_text)` Method to convert markdown text into TemPy nodes.

## [1.1.0](https://github.com/Hrabal/TemPy/compare/6cde4add75bcde5c23614573980caf7684bae76b...master) - 2017-11-25

### Added
- TempyList widget now manages the `dl` tag, using `typ=tempy.tags.Dl` or `typ='Dl'`
- added `DOMElement.wrap_many()` method, to copy a TemPy element inside other TemPy elements
- added `T.dump_string(html_string, filename)` method to directly convert an html string to a TemPy template in a .py file
- Named element insertion now support the naming of a group of objects (lists), not just single instances
- Python version checking, importing TemPy with Python < 3.3 will raise a RuntimeError

### Fixed
- TempyREPR feature refactored
- Element insertion yielding refactored
- Documentation

## [1.0.0](https://github.com/Hrabal/TemPy/compare/d6a5e155b26a48d17bf1b26863b32f4a449ec12d...6cde4add75bcde5c23614573980caf7684bae76b) - 2017-11-05

### Added
- Everything :)
