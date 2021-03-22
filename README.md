![](https://img.shields.io/github/license/orangeutan/babelbox)
![](https://img.shields.io/badge/python-3.8|3.9-blue)
[![](https://img.shields.io/pypi/v/babelbox)](https://pypi.org/project/babelbox/)
![](https://raw.githubusercontent.com/OrangeUtan/babelbox/cabe03f93500e0ee2e0bf9f39c03e52007989ecb/coverage.svg)
![](https://img.shields.io/badge/mypy-checked-green)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![](https://img.shields.io/badge/pre--commit-enabled-green)
![](https://github.com/orangeutan/babelbox/workflows/test/badge.svg)

# Babelbox
Babelbox allows you to write your language files in .csv files and then generate Minecraft language.json files from them.<br>
Creating translations in CSV gives you an easy overview over any errors or missing translations.<br>

# Table of contents
- [Installation](#Installation)
- [Usage](#Usage)
- [Getting started](#Getting-started)
    - [Single file source](#Single-file-source)
    - [Directory source](#Directory-source)
    - [Shorten variable names](#Shorten-variable-names)
    - [Organize translations in folders](#Organize-translations-in-folders)
- [Contributing](#Contributing)
- [Changelog](https://github.com/OrangeUtan/babelbox/blob/main/CHANGELOG.md)

# Installation
```shell
$ pip install babelbox
```

# Usage
Reads translations from all sources and then generates minecraft language files for all language codes
```shell
$ # Single .csv file source
$ babelbox <file.csv>
$ # Directory containing .csv files as source
$ babelbox <directory>
$ # Multiple sources require output directory
$ babelbox <file1.csv> <directory> <file2.csv> -o <output_dir>
```

All options:
```shell
$ babelbox SOURCES...
    -o, --out                   The output directory of the generated files
    -p, --prefix-identifiers    Prefix identifiers with their path relative
                                to their SOURCES entry
    --dialect [excel|excel-tab|unix]
                                CSV dialect used to parse CSV. Dialect will
                                be automatically detected of omitted
    -d, --delimiter             CSV delimiter overwrite
    --quotechar                 CSV quote char overwrite
    -m, --minify                Minify generated files
    -i, --indent                Indentation used when generating files
    --dry                       Dry run. Don not generate any files
    -v, --verbose               Increase verbosity
    -q, --quiet                 Only output errors
```


# Getting started
## Single file source:
We have one `.csv` file containing translations:
```
resourcepack
⠇
└╴lang
  └╴ items.csv
```

| Item                                | en_us    | de_de      |
| ----------------------------------- | -------- | ---------- |
| item.stick.﻿name                   | stick    | Stock      |
| # You can create comments like this |          |            |
| item.snowball.﻿name                | snowball | Schneeball |

Passing **items.csv** as a source to babelbox generates the language files **en_us.json** and **de_de.json**:
```shell
$ babelbox resourcepack/.../lang/items.csv
```
```json
en_us.json
{
    "item.stick.name": "stick",
    "item.snowball.name": "snowball",
}

de_de.json
{
    "item.stick.name": "Stock",
    "item.snowball.name": "Schneeball",
}
```

```
resourcepack
⠇
└╴lang
  ├╴ items.csv
  ├╴ en_us.json
  └╴ de_de.json
```

## Directory source
We have two `.csv` files containing translations:
```
resourcepack
⠇
└╴lang
  ├╴ items.csv
  └╴ blocks.csv
```
**items.csv**
| Item                 | en_us    | de_de      |
| -------------------- | -------- | ---------- |
| item.stick.﻿name    | stick    | Stock      |

**blocks.csv**
| Block                 | en_us    | de_de     |
| --------------------- | -------- | --------- |
| block.log.﻿name      | log      | Holzstamm |

Passing the **lang** directory as a source to babelbox generates the language files **en_us.json** and **de_de.json**:
```shell
$ babelbox resourcepack/.../lang
```
```json
en_us.json
{
    "item.stick.name": "stick",
    "block.log.name": "log",
}

de_de.json
{
    "item.stick.name": "Stock",
    "block.log.name": "Holzstamm",
}
```
```
resourcepack
⠇
└╴lang
  ├╴ items.csv
  ├╴ blocks.csv
  ├╴ en_us.json
  └╴ de_de.json
```

## Shorten variable names:
We can use the `--prefix-identifiers` flag to save ourselve some typing. If all identifiers share a common prefix, we can name the file to that prefix and let Babelbox prepend it.

```
resourcepack
⠇
└╴lang
  └╴ item.swords.csv
```
| Swords         | en_us         | de_de          |
| -------------- | ------------- | -------------- |
| diamond.﻿name | Diamond Sword | Diamantschwert |
| gold.﻿name    | Gold sword    | Goldschwert    |

```shell
$ babelbox resourcepack/.../lang --prefix-identifiers
$ # Or abbreviated
$ babelbox resourcepack/.../lang -p
```

```json
en_us.json
{
    "item.swords.diamond.name": "Diamond Sword",
    "item.swords.gold.name": "Gold sword",
}

de_de.json
{
    "item.swords.diamond.name": "Diamantschwert",
    "item.swords.gold.name": "Goldschwert",
}
```

All identifiers have been prefixed with `item.swords.`

## Organize translations in folders
We can save ourselves even more typing and organize our translations files in a directory structure:

```
resourcepack
⠇
└╴lang
  ├╴ item
  │  └╴ swords.csv
  └╴ block
     └╴ heavy.csv
```
**swords.csv**
| Swords         | en_us         | de_de          |
| -------------- | ------------- | -------------- |
| gold.﻿name    | Gold sword    | Goldschwert    |

**heavy.csv**
| Heavy Blocks | en_us      | de_de       |
| ------------ | ---------- | ----------- |
| lead.﻿name  | Lead Block | Bleiblock |

```shell
$ babelbox resourcepack/.../lang -p
```

```json
en_us.json
{
    "item.swords.gold.name": "Gold sword",
    "block.heavy.lead.name": "Lead Block",
}

de_de.json
{
    "item.swords.gold.name": "Goldschwert",
    "block.heavy.lead.name": "Bleiblock",
}
```
```
resourcepack
⠇
└╴lang
  ├╴ item
  │  └╴ swords.csv
  ├╴ block
  │   └╴ heavy.csv
  ├╴ en_us.json
  └╴ de_de.json
```

# Contributing
Contributions are welcome. Make sure to first open an issue discussing the problem or the new feature before creating a pull request. The project uses [`poetry`](https://python-poetry.org/). Setup automatically with [`invoke`](http://www.pyinvoke.org/) or manualy with poetry:
```shell
$ # Either
$ invoke install
$ # or
$ poetry install
```
You can run test with pytest:
```shell
$ poetry run pytest
```
The project follows [`black`](https://github.com/psf/black) codestyle. Import statements are sorted with [`isort`](https://pycqa.github.io/isort/). Code formatting and type checking is enforced using [`pre-commit`](https://pre-commit.com/).
```shell
$ pre-commit install
```
