# Changelog

<!--next-version-placeholder-->

## v2.1.1 (2021-04-07)
### Fix
* Fix invalid imports from beet ([`7841a48`](https://github.com/OrangeUtan/babelbox/commit/7841a483f5b6a0972e2d9a7196d734413b7d1f24))

### Documentation
* Update README ([`4d64001`](https://github.com/OrangeUtan/babelbox/commit/4d640017a18169b17871a7abd8fbb05576db7628))

## v2.1.0 (2021-03-22)
### Feature
- [`beet`](https://github.com/mcbeet/beet) plugin integration
- `--delimiter` option
- `--quotechar` option
- `--dialect` option

## v2.0.0 (2021-03-20)
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

## v1.2.0 (2021-03-17)
### Added
- Added `--dry` option
- Added `--verbose` option
- Warns if language is missing translation for variable
- Checks if variabel is empty

## v1.1.0 (2021-03-15)
### Added
- Added `--prefix-filename` CLI option
### Fixed
- Error when not supplying any args to CLI

## v1.0.1 (2021-03-15)
### Fixed
- Tbump didn't bump all version strings

## v1.0.0 (2021-03-15)
### Added
- `bump` task
- Added options to `test` task
- Added abbreviations for CLI options/flags
### Changed
- Testing CLI with typer.testing.CLIRunner
- Improved CLI argument parsing/checking

## v0.2.0 (2021-03-15)
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
