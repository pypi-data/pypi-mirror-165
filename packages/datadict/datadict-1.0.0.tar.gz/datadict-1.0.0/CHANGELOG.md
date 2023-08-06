# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [Unreleased]


## [1.0.0] - 2022-08-30

### Added

- Support for PEP 681 data class transform, contributed by [Blake Naccarato](https://github.com/blakeNaccarato) in [#2].
- `CHANGELOG.md` detailing changes made to `datadict` since its initial publication ([#3]).
- `AUTHORS.md` with a list of maintainers and contributors ([#3]).
- Explicit support for Python 3.10 ([#2]) and 3.11 ([#3]).

### Removed

- Support for Python 3.6, because of dependency on [`typing-extensions`](https://pypi.org/project/typing-extensions/) ([#2]).


## [0.1.0] - 2020-07-20

- Initial commit with basic functionality and explicit support for Python 3.6, 3.7, 3.8, and 3.9.


[Unreleased]: https://github.com/gahjelle/datadict/compare/v1.0.0-20220830...HEAD
[1.0.0]: https://github.com/gahjelle/datadict/compare/v0.1.0-20200720...v1.0.0-20220830
[0.1.0]: https://github.com/gahjelle/datadict/releases/tag/v0.1.0-20200720

[#3]: https://github.com/gahjelle/datadict/pull/3
[#2]: https://github.com/gahjelle/datadict/pull/2
