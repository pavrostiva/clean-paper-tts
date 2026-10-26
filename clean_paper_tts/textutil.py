"""Text normalisation helpers shared by every reader."""

from __future__ import annotations

import re
import unicodedata
from collections import Counter

SOFT_BREAK = "­"  # marks a hyphen removed at a line break; resolved later

_LIGATURES = {
    "ﬀ": "ff", "ﬁ": "fi", "ﬂ": "fl", "ﬃ": "ffi",
    "ﬄ": "ffl", "ﬅ": "st", "ﬆ": "st",
}
_CHAR_MAP = {
    " ": " ", " ": " ", " ": " ", " ": " ", " ": " ",
    " ": " ", "​": "", "‌": "", "‍": "", "﻿": "",
    "‐": "-", "‑": "-", "‒": "-",
    "‘": "'", "’": "'", "“": '"', "”": '"',
}
_TRANS = str.maketrans({**_LIGATURES, **_CHAR_MAP})

_WS = re.compile(r"[ \t\r\f\v]+")
_SPACE_BEFORE_PUNCT = re.compile(r"\s+([,.;:!?%)\]])")
_SPACE_AFTER_OPEN = re.compile(r"([(\[])\s+")


def normalize(text: str) -> str:
    """Replace ligatures / exotic spaces and collapse whitespace (keeps SOFT_BREAK)."""
    text = text.translate(_TRANS)
    text = _WS.sub(" ", text.replace("\n", " "))
    return text.strip()


def tidy_spacing(text: str) -> str:
    text = _SPACE_BEFORE_PUNCT.sub(r"\1", text)
    text = _SPACE_AFTER_OPEN.sub(r"\1", text)
    return re.sub(r"\s{2,}", " ", text).strip()


def join_lines(lines: list[str]) -> str:
    """Join physical lines into one paragraph, marking removable line-break hyphens."""
    out = ""
    for raw in lines:
        line = normalize(raw)
        if not line:
            continue
        if not out:
            out = line
        elif re.search(r"[A-Za-zÀ-ɏ]-$", out) and line[:1].islower():
            out = out[:-1] + SOFT_BREAK + line
        elif out.endswith(SOFT_BREAK):
            out = out[:-1] + SOFT_BREAK + line
        else:
            out = out + " " + line
    return out


def build_vocabulary(texts: list[str]) -> Counter:
    vocab: Counter = Counter()
    for t in texts:
        t = re.sub(r"\w*" + SOFT_BREAK + r"\w*", " ", t)  # broken-word halves are not words of their own
        for w in re.findall(r"[A-Za-z][A-Za-z\-]+", t):
            vocab[w.lower()] += 1
    return vocab


def resolve_soft_breaks(text: str, vocab: Counter) -> str:
    """Decide for each removed line-break hyphen whether it was a real hyphen."""
    if SOFT_BREAK not in text:
        return text

    def repl(m: re.Match) -> str:
        left, right = m.group(1), m.group(2)
        joined = (left + right).lower()
        hyph = (left + "-" + right).lower()
        if vocab.get(hyph, 0) > vocab.get(joined, 0):
            return left + "-" + right
        if vocab.get(joined, 0) == 0:
            # both halves are words of their own ("cohort" + "conserved") or the left one is an acronym ("TME")
            if left.isupper() and len(left) >= 2:
                return left + "-" + right
            if len(left) >= 3 and len(right) >= 4 and vocab.get(left.lower(), 0) >= 1 and vocab.get(right.lower(), 0) >= 1:
                return left + "-" + right
        return left + right

    text = re.sub(r"([A-Za-zÀ-ɏ]+)" + SOFT_BREAK + r"([A-Za-zÀ-ɏ]+)", repl, text)
    return text.replace(SOFT_BREAK, "")


# ---------------------------------------------------------------- citations

_NUM = r"\d{1,3}"
_RANGE_SEP = r"\s*[,–—−-]\s*"
_NUMERIC_CITE = re.compile(rf"\s*\[\s*{_NUM}(?:{_RANGE_SEP}{_NUM})*\s*\]")
_EMPTY_BRACKETS = re.compile(r"\s*[\[(]\s*[\])]")
_NAME = r"[A-Z][A-Za-z'’\-À-ɏ]+"
_AUTHORS = rf"{_NAME}(?:\s+(?:et al\.?|and|&)\s*(?:{_NAME})?)?(?:,?\s+{_NAME})?"
_YEAR = r"(?:19|20)\d\d[a-z]?"
_AUTHOR_YEAR_ITEM = rf"{_AUTHORS},?\s+{_YEAR}(?:\s*,\s*{_YEAR})*"
_AUTHOR_YEAR = re.compile(
    rf"\s*\((?:e\.g\.,?\s+|see\s+|reviewed in\s+)?{_AUTHOR_YEAR_ITEM}(?:\s*;\s*{_AUTHOR_YEAR_ITEM})*\)"
)


def strip_citations(text: str, numeric: bool = True, author_year: bool = True) -> str:
    if numeric:
        text = _NUMERIC_CITE.sub("", text)
    text = _EMPTY_BRACKETS.sub("", text)  # leftovers of removed citation links
    if author_year:
        text = _AUTHOR_YEAR.sub("", text)
    return text


# ----------------------------------------------------------------- headings

_NUMBERING = re.compile(r"^\s*(?:(?:\d+\.)*\d+|[IVX]+|[A-Z])[.)]?\s*[|:–—-]?\s+(?=\S)")
_BULLETS = "■▪●•◦□‣⁃*"


def heading_key(text: str) -> str:
    """Lower-case heading text without numbering / bullets, for matching."""
    t = text.strip().lstrip(_BULLETS + " ")
    t = _NUMBERING.sub("", t)
    return re.sub(r"[\s:.]+$", "", t).lower()


def clean_heading(text: str) -> str:
    t = normalize(text).lstrip(_BULLETS + " ")
    t = re.sub(r"^((?:\d+\.)*\d+)\s*\|\s*", r"\1 ", t)  # "2.8 | Title" -> "2.8 Title"
    return t.strip()
