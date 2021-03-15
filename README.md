![](https://img.shields.io/github/license/orangeutan/babelbox)
![](https://img.shields.io/badge/python-3.8|3.9-blue)
[![](https://img.shields.io/pypi/v/babelbox)](https://pypi.org/project/babelbox/)
![](./coverage.svg)
![](https://img.shields.io/badge/mypy-checked-green)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![](https://img.shields.io/badge/pre--commit-enabled-green)
![](https://github.com/orangeutan/babelbox/workflows/test/badge.svg)

# Babelbox
Babelbox allows you to write your language files in the CSV format and then generate Minecraft language files from them.<br>
Creating translations in CSV gives you an easy overview over any errors or missing languages.<br>

## Install
`pip install bablebox`

## Usage
`babelbox <src_dir> [dest_dir]`<br>
Finds all `.csv` files in the source directory and generates minecraft language files

# Example
Lets assume we have two csv files "items.csv" and "blocks.csv" in the folder "resourcepack/assets/minecraft/lang":

| String             | en       | de         |
| ------------------ | -------- | ---------- |
| item.stick.name    | stick    | Stock      |
| item.snowball.name | snowball | Schneeball |

| String             | en      | de      |
| ------------------ | ------- | ------- |
| block.grass.name   | grass   | Gras    |
| block.diamond.name | diamond | Diamant |

Lets run `babelbox resourcepack/assets/minecraft/lang`<br>
Babelbox will now create the two language files "en.json" and "de.json" in the folder "resourcepack/assets/minecraft/lang":<br>
```json
{
    "item.stick.name": "stick",
    "item.snowball.name": "snowball",
    "block.grass.name": "grass",
    "block.diamond.name": "diamond"
}
```
```json
{
    "item.stick.name": "Stock",
    "item.snowball.name": "Schneeball",
    "block.grass.name": "Gras",
    "block.diamond.name": "Diamant"
}
```
