"""Post-processing filters. Each filter takes (Document, Options) and edits it in place.

Add a new filter by writing a function and appending it to ``FILTERS``.
"""

from __future__ import annotations

from collections.abc import Callable

from ..model import Document
from ..options import Options
from .chemistry import strip_characterization_data
from .noise import drop_noise_paragraphs
from .sections import drop_sections
from .text import clean_text

Filter = Callable[[Document, Options], None]

FILTERS: list[Filter] = [
    clean_text,
    drop_noise_paragraphs,
    drop_sections,
    strip_characterization_data,
]


def apply_filters(doc: Document, options: Options) -> Document:
    for f in FILTERS:
        f(doc, options)
    return doc
