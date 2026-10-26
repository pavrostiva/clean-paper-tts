from __future__ import annotations

import re

from ..model import Document, Heading, ListBlock, Paragraph, Visual
from ..options import Options
from ..textutil import heading_key


def _describe(b) -> str:
    if isinstance(b, (Heading, Paragraph)):
        return b.text
    if isinstance(b, ListBlock):
        return " ".join(b.items)
    return ""


def drop_sections(doc: Document, options: Options) -> None:
    """Remove whole sections (references, acknowledgements, ...) by heading text."""
    pats = [re.compile(rf"^(?:{p})$", re.I) for p in options.section_patterns()]
    out = []
    skip_level: int | None = None
    skip_reason = ""
    for b in doc.blocks:
        if isinstance(b, Heading):
            if skip_level is not None and b.level <= skip_level:
                skip_level = None
            if skip_level is None:
                key = heading_key(b.text)
                if any(p.match(key) for p in pats):
                    skip_level = b.level
                    skip_reason = f"section: {b.text}"
                    doc.drop(skip_reason, b.text)
                    continue
        if skip_level is not None:
            if not isinstance(b, Visual):
                doc.drop(skip_reason, _describe(b))
            continue
        out.append(b)
    doc.blocks = out
