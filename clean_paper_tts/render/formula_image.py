"""Render a display equation to PNG from its LaTeX source (matplotlib mathtext)."""

from __future__ import annotations

import io
import re

_REPLACEMENTS = [
    (r"\\text\{", r"\\mathrm{"), (r"\\textrm\{", r"\\mathrm{"), (r"\\mathbb\{", r"\\mathbf{"),
    (r"\\boldsymbol\{", r"\\mathbf{"), (r"\\bm\{", r"\\mathbf{"), (r"\\operatorname\{", r"\\mathrm{"),
    (r"\\displaystyle", ""), (r"\\nolimits", ""), (r"\\limits", ""), (r"\\!", ""), (r"\;", r"\\ "),
    (r"\\tfrac", r"\\frac"), (r"\\dfrac", r"\\frac"), (r"\\mathop\{", r"\\mathrm{"),
    (r"\\begin\{(?:aligned|align\*?|equation\*?|split)\}", ""), (r"\\end\{(?:aligned|align\*?|equation\*?|split)\}", ""),
    (r"&", " "), (r"\\\\", " "), (r"\\label\{[^}]*\}", ""), (r"\\tag\{[^}]*\}", ""),
]


def _prepare(latex: str) -> str:
    s = latex.strip()
    s = re.sub(r"^\$+|\$+$", "", s).strip()
    s = re.sub(r"^\\\[|\\\]$|^\\\(|\\\)$", "", s).strip()
    for pat, rep in _REPLACEMENTS:
        s = re.sub(pat, rep, s)
    return s.strip()


def render_latex(latex: str, dpi: int = 300, fontsize: int = 14) -> bytes | None:
    body = _prepare(latex)
    if not body:
        return None
    try:
        import matplotlib

        matplotlib.use("Agg")
        from matplotlib import mathtext

        buf = io.BytesIO()
        mathtext.math_to_image(f"${body}$", buf, dpi=dpi, format="png", prop=_prop(fontsize))
        return buf.getvalue()
    except Exception:
        return None


def _prop(size: int):
    from matplotlib.font_manager import FontProperties

    return FontProperties(size=size)
