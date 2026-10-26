"""Publisher boiler-plate that survives layout analysis (web UI text, legal lines, ...)."""

from __future__ import annotations

import re

from ..model import Document, Paragraph
from ..options import Options

# One regex per known kind of noise. Extend freely; patterns are matched with
# ``re.search`` against a whole paragraph and only drop short paragraphs
# (see MAX_NOISE_CHARS) so real prose is never removed by accident.
NOISE_PATTERNS: tuple[tuple[str, str], ...] = (
    ("download notice", r"downloaded from\b|downloaded by\b|see the terms and conditions"),
    ("publisher url line", r"^\s*(https?://|www\.|pubs\.acs\.org|doi\.org|doi:)\S*\s*$"),
    ("citation banner", r"^\s*(cite this|read online|access\b|metrics (&|and) more|article recommendations)"),
    ("copyright", r"^\s*(©|\(c\)|copyright)\s*\d{0,4}|\ball rights reserved\b|published by .* on behalf of"),
    ("licence", r"creative commons|licen[cs]ed? under|open access article|this is an open access|permits? use, distribution"),
    ("history line", r"^\s*(received|revised|accepted|published|available online|publication date)\b.*\b(19|20)\d\d"),
    ("keywords line", r"^\s*(key ?words?|index terms)\s*[:—-]"),
    ("correspondence", r"^\s*(\*|†|‡)?\s*(corresponding authors?|correspondence|e-?mail)\s*[:—-]|^\s*\*?\s*correspondence\b"),
    ("check updates", r"check for updates|crossmark|click to see any corrections"),
    ("journal id line", r"^\s*(j\.|journal of)\s+[A-Za-z .]+\s*\d{4},\s*\d+,\s*\d+[–-]\d+\s*$"),
    ("page counter", r"^\s*(page\s+)?\d+\s*(of|/)\s*\d+\s*$"),
    ("bare number", r"^\s*\d{1,5}\s*$"),
    ("stray symbol", r"^[\W_]{1,3}$"),
    ("article tag", r"^\s*(article|review|research article|original article|letter|perspective|brief report)\s*$"),
    ("equal contribution", r"contributed equally|these authors contributed"),
    ("web ui", r"^\s*(open in figure viewer|download (figure|image|table)|powerpoint|view (full )?size|full text|pdf|share|tools|figures|tables?|references)\s*$"),
    ("supporting info pointer", r"^\s*(\*\s*)?(s[ıi]|supporting information)\s*$"),
    ("funding line", r"^\s*(funding|grant support)\s*[:—-]"),
    ("author note", r"^\s*(†|‡|⊥|#|§|∥)\s*(these authors|contributed equally|equal contribution|present address)"),
)

MAX_NOISE_CHARS = 400
_COMPILED = [(n, re.compile(p, re.I)) for n, p in NOISE_PATTERNS]


def match_noise(text: str) -> str | None:
    """Name of the first noise pattern matching a short paragraph, else None."""
    if len(text) > MAX_NOISE_CHARS:
        return None
    return next((n for n, rx in _COMPILED if rx.search(text)), None)


def drop_noise_paragraphs(doc: Document, options: Options) -> None:
    extra = []
    for p in options.extra_noise_patterns:
        p = p.strip()
        if p:
            try:
                extra.append(("custom pattern", re.compile(p, re.I)))
            except re.error:
                doc.warnings.append(f"Ignored invalid custom regex: {p!r}")
    compiled = [(n, re.compile(p, re.I)) for n, p in NOISE_PATTERNS] + extra
    kept = []
    for b in doc.blocks:
        if isinstance(b, Paragraph) and b.role != "caption":
            limit = None if any(n == "custom pattern" for n, _ in extra) else MAX_NOISE_CHARS
            hit = next((n for n, rx in compiled if rx.search(b.text)
                        and (limit is None or len(b.text) <= limit or n == "custom pattern")), None)
            if hit:
                doc.drop(f"noise: {hit}", b.text)
                continue
        kept.append(b)
    doc.blocks = kept
