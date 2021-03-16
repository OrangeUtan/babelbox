# Changelog

## [Unreleased]
### Added
- Added `--dry` option
- Added `--verbose` option
- Warns if language is missing translation for variable

## [1.1.0] - 2021-03-15
### Added
- Added `--prefix-filename` CLI option
### Fixed
- Error when not supplying any args to CLI

## [1.0.1] - 2021-03-15
### Fixed
- Tbump didn'T bump all version strings

## [1.0.0] - 2021-03-15
### Added
- `bump` task
- Added options to `test` task
- Added abbreviations for CLI options/flags
### Changed
- Testing CLI with typer.testing.CLIRunner
- Improved CLI argument parsing/checking

## [0.2.0] - 2021-03-15
### Added
- Added CSV localization parser
- Added CLI
- Made package to executable script
- Setup Poetry project
- Formatting: isort, black
- Checks: pre-commit, mypy
- Code Coverage
- Github Actions
- tasks
- Automatic version bumbing
- MIT LICENSE
