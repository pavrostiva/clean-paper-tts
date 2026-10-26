"""Cut analytical characterisation data (NMR / MS listings) from experimental text."""

from __future__ import annotations

import re

from ..model import Document, Paragraph
from ..options import Options

# Start of a data listing, e.g. "1H NMR (400 MHz, DMSO-d6) δ 8.4 (s, 1H) ..." or "HRMS (ESI) m/z ...".
_DATA_START = re.compile(
    r"(?:\b\d{1,3}[A-Z][a-z]?\s*(?:\{\s*\d*H?\s*\}\s*)?NMR\b|\bNMR\s*\(|\bHRMS\b|\bESI-?MS\b|\bLC-?MS\b|"
    r"\bMALDI\b|\bElemental analysis\b|\bAnal\.?\s*calcd\b|\bIR\s*\(|\bmp\s*\d|\bHPLC purity\b|\b\[?α\]?D\b)"
)
_DATA_SIGNS = re.compile(r"δ|\bm/z\b|\bcalcd\b|\bfound\b|\bppm\b|\bMHz\b|\bHz\b|\(\s*[sdtqm]{1,3}\s*,", re.I)


_SHIFT_LIST = re.compile(r"\(\s*(?:br\s*)?[sdtqm]{1,3}\s*,|\bJ\s*=\s*\d|\u03b4\s*\d")


def strip_characterization_data(doc: Document, options: Options) -> None:
    if not options.strip_characterization_data:
        return
    kept = []
    for b in doc.blocks:
        if isinstance(b, Paragraph) and b.role == "body":
            m = _DATA_START.search(b.text)
            if m and len(_DATA_SIGNS.findall(b.text[m.start():])) >= (1 if m.start() < 3 else 2):
                head, tail = b.text[: m.start()].rstrip(" ,;:(-"), b.text[m.start():]
                doc.drop("characterization data", tail)
                if len(head.split()) < 3:
                    continue
                b.text = head if head.endswith((".", "!", "?")) else head + "."
            elif len(_SHIFT_LIST.findall(b.text)) >= 3:  # peak list that lost its "NMR (...)" lead-in
                doc.drop("characterization data", b.text)
                continue
        kept.append(b)
    doc.blocks = kept
