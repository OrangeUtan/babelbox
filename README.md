![](https://img.shields.io/github/license/orangeutan/babelbox)
![](https://img.shields.io/badge/python-3.8|3.9-blue)
[![](https://img.shields.io/pypi/v/babelbox)](https://pypi.org/project/babelbox/)
![](https://raw.githubusercontent.com/OrangeUtan/babelbox/cabe03f93500e0ee2e0bf9f39c03e52007989ecb/coverage.svg)
![](https://img.shields.io/badge/mypy-checked-green)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![](https://img.shields.io/badge/pre--commit-enabled-green)
![](https://github.com/orangeutan/babelbox/workflows/test/badge.svg)

# Babelbox
Babelbox allows you to write your language files in the CSV format and then generate Minecraft language files from them.<br>
Creating translations in CSV gives you an easy overview over any errors or missing languages.<br>

# Table of contents
- [Installation](#Installation)
- [Usage](#Usage)
- [Examples](#Examples)
    - [Basic usage](#Basic-usage)
    - [Shorten variable names](#Shorten-variable-names)
- [Changelog](https://github.com/OrangeUtan/babelbox/blob/main/CHANGELOG.md)

# Installation
```
pip install babelbox
```

# Usage
Finds all `.csv` files in the source directory and generates minecraft language files<br>
```
babelbox <src_dir> [dest_dir]
    -p, --pretty-print      Pretty print json
    -i, -indent TEXT        String used to indent json
    -n, --prefix-filename   Prefixes all variables with filename
    --dry                   Dry run. Don't create any files
    -v, --verbose
```

# Examples
## Basic usage:
We have these two CSV files containing our translations:

**.../lang/items.csv:**
| Variable           | en_us    | de_de      |
| ------------------ | -------- | ---------- |
| item.stick.name    | stick    | Stock      |
| item.snowball.name | snowball | Schneeball |

**.../lang/blocks.csv:**
| Variable           | en_us   | de_de   |
| ------------------ | ------- | ------- |
| block.grass.name   | grass   | Gras    |
| block.diamond.name | diamond | Diamant |

Running `babelbox .../lang/` makes Babelbox parse the CSV files and generate the following language files in the same folder:<br>
**.../lang/en_us.json:**
```json
{
    "item.stick.name": "stick",
    "item.snowball.name": "snowball",
    "block.grass.name": "grass",
    "block.diamond.name": "diamond"
}
```
**.../lang/de_de.json:**
```json
{
    "item.stick.name": "Stock",
    "item.snowball.name": "Schneeball",
    "block.grass.name": "Gras",
    "block.diamond.name": "Diamant"
}
```

## Shorten variable names:
We can use the `--prefix-filename` flag to save ourselve some typing. If all variables in a CSV file share a common prefix, we can name the file to that prefix and let Babelbox prepend it.

**.../lang/item.swords.csv**
| Variable     | en_us         | de_de          |
| ------------ | ------------- | -------------- |
| diamond.name | Diamond Sword | Diamantschwert |
| gold.name    | Gold sword    | Goldschwert    |

Running `babelbox .../lang/ --prefix-filename` creates these two files:

**.../lang/en_us.json**
```json
{
    "item.swords.diamond.name": "Diamond Sword",
    "item.swords.gold.name": "Gold sword",
}
```
**.../lang/de_de.json**
```json
{
    "item.swords.diamond.name": "Diamantschwert",
    "item.swords.gold.name": "Goldschwert",
}
```

All variables have been prefixed with **item.swords**
