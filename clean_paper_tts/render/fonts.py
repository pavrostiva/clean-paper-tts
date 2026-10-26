from __future__ import annotations

import functools
import os

from PIL import ImageFont


@functools.lru_cache(maxsize=1)
def _font_dir() -> str:
    import matplotlib

    return os.path.join(matplotlib.get_data_path(), "fonts", "ttf")


@functools.lru_cache(maxsize=64)
def get_font(size: int, bold: bool = False, italic: bool = False) -> ImageFont.FreeTypeFont:
    name = "DejaVuSans" + ("-BoldOblique" if bold and italic else "-Bold" if bold
                           else "-Oblique" if italic else "")
    return ImageFont.truetype(os.path.join(_font_dir(), name + ".ttf"), size)
