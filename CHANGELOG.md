# Change log
This log follows the conventions of
[keepachangelog.com](http://keepachangelog.com/). It picks up from `punwrap`
version 0.1.0.

## [Unreleased]
Nothing yet.

## [0.2.5] – 2024-08-01
No efficacious changes to source code were made for this release.

### Added
- Build for Python v3.12.

## [0.2.4] – 2023-07-25
No efficacious changes to source code were made for this release.

### Changed
- Centralized compilation.

## [0.2.3] – 2023-07-23
No efficacious changes to source code were made for this release.

### Changed
- Updated build system to `maturin` v1.
- Started using Docker for `musllinux` builds, not just `manylinux`.

### Added
- Build for Python v3.11.

### Removed
- Builds for Python v3.6, v3.7.

## [0.2.2] – 2023-07-23
No efficacious changes to source code were made for this release.
It is only a rebuild made to fix a `manylinux_2_17` `libc` compliance problem
when downloading v0.2.1 to newer systems.

## [0.2.1] – 2022-03-17
This release does not fix bugs. It was made for wider portability, following
changes in the wider ecosystem.

### Changed
- Updated Python interpreters in the `musl` build environment to the latest
  point releases of Python 3.6–3.10.

## [0.2.0] – 2021-07-12
### Added
- Support for `musl`-based Linux platforms under PEP 656.
  (At the time of this release, `pip` cannot yet install `musl` artifacts,
  nor does `pypi` accept them for upload.)

[Unreleased]: https://github.com/veikman/punwrap/compare/punwrap-v0.2.5...HEAD
[0.2.5]: https://github.com/veikman/punwrap/compare/punwrap-v0.2.4...v0.2.5
[0.2.4]: https://github.com/veikman/punwrap/compare/punwrap-v0.2.3...v0.2.4
[0.2.3]: https://github.com/veikman/punwrap/compare/punwrap-v0.2.2...v0.2.3
[0.2.2]: https://github.com/veikman/punwrap/compare/punwrap-v0.2.1...v0.2.2
[0.2.1]: https://github.com/veikman/punwrap/compare/punwrap-v0.2.0...v0.2.1
[0.2.0]: https://github.com/veikman/punwrap/compare/punwrap-v0.1.0...v0.2.0
