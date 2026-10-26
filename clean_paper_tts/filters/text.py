from __future__ import annotations

import re

from ..model import Document, Heading, ListBlock, Paragraph
from ..options import Options
from ..textutil import build_vocabulary, resolve_soft_breaks, strip_citations, tidy_spacing


def _all_texts(doc: Document) -> list[str]:
    out: list[str] = []
    for b in doc.blocks:
        if isinstance(b, (Paragraph, Heading)):
            out.append(b.text)
        elif isinstance(b, ListBlock):
            out.extend(b.items)
    return out


_GLITCHES = ((re.compile(r"fi\s*br\s+br"), "fibr"), (re.compile(r"fibr\s+br"), "fibr"))


def _fix_glitches(t: str) -> str:
    """Known text-layer artefacts of ligature fonts (e.g. 'anti\ufb01 br brotic')."""
    for rx, rep in _GLITCHES:
        t = rx.sub(rep, t)
    return t


_CAPTION_PLACEHOLDER = re.compile(
    r"^\s*(?:fig(?:ure)?\.?|table|scheme|chart)\s*S?\d+[A-Za-z]?\s*[.:|\u2013-]?\s*"
    r"(?:legend on next page|legend continued on next page|continued|\(continued\)|\(continued on next page\))\.?\s*", re.I)


def clean_text(doc: Document, options: Options) -> None:
    """Resolve line-break hyphens, strip citation markers, tidy spacing."""
    vocab = build_vocabulary(_all_texts(doc))

    def fix(t: str, body: bool) -> str:
        t = _fix_glitches(resolve_soft_breaks(t, vocab))
        if body and options.strip_citations:
            t = strip_citations(t, numeric=True, author_year=options.strip_author_year_citations)
        return tidy_spacing(t)

    kept = []
    for b in doc.blocks:
        if isinstance(b, Heading):
            b.text = fix(b.text, body=False)
        elif isinstance(b, Paragraph):
            b.text = fix(b.text, body=b.role != "caption")
            if b.role == "caption":
                b.text = _CAPTION_PLACEHOLDER.sub("", b.text).strip()
            if not b.text:
                continue
        elif isinstance(b, ListBlock):
            b.items = [x for x in (fix(i, True) for i in b.items) if x]
            if not b.items:
                continue
        kept.append(b)
    doc.blocks = kept
