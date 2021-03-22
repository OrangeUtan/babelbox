from typing import Iterable, Optional

from beet import Context
from beet.library.resource_pack import Language
from beet.toolchain.context import Plugin

import babelbox


def beet_default(ctx: Context):
    """ Entry point into beet pipeline. Loads configuration and executes babelbox plugin """

    config = ctx.meta.get("babelbox", {})

    csv_dialect_overwrites = {}
    load = config.get("load", ())
    if delimiter := config.get("delimiter"):
        csv_dialect_overwrites["delimiter"] = delimiter
    prefix_identifiers = config.get("prefix_identifiers")
    dialect = config.get("dialect")

    ctx.require(create_babelbox_plugin(load, csv_dialect_overwrites, prefix_identifiers))


def create_babelbox_plugin(
    load: Iterable[str] = (),
    csv_dialect_overwrites: Optional[dict] = None,
    prefix_identifiers: bool = False,
) -> Plugin:
    def plugin(ctx: Context):
        minecraft = ctx.assets["minecraft"]

        for pattern in load:
            for path in ctx.directory.glob(pattern):
                languages = babelbox.load_languages(
                    path,
                    prefix_identifiers,
                    dialect=None,
                    csv_dialect_overwrites=csv_dialect_overwrites,
                )

                minecraft.languages.merge(
                    {code: Language(translations) for code, translations in languages.items()}
                )

    return plugin
