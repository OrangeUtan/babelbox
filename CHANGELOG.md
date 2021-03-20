# Changelog

## [2.0.0] - 2021-03-20
### Feature
- `--quiet` flag
- Source can now be file or directory
- Accepts multiple sources
- Improved logging configurability
- Added support for csv comments

### Breaking
- Changed output dir to `--out`/`-o` option
- Renamed `--pretty-print`/`-p` to `--minify`/`-m`
- Renamed `--prefix-filename`/`-n` to `--prefix-identifiers`/`-p`
- Prefix option now prefixes relative path to source
- Missing translations are no longer skipped. Instead the default to ""

## [1.2.0] - 2021-03-17
### Added
- Added `--dry` option
- Added `--verbose` option
- Warns if language is missing translation for variable
- Checks if variabel is empty

## [1.1.0] - 2021-03-15
### Added
- Added `--prefix-filename` CLI option
### Fixed
- Error when not supplying any args to CLI

## [1.0.1] - 2021-03-15
### Fixed
- Tbump didn't bump all version strings

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
