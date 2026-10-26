"""Extract text lines from a PDF page in an upright coordinate frame."""

from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass, field

from ...textutil import is_citation_superscript as _is_citation_superscript
from ...textutil import normalize
from .geometry import Orientation, Rect

BOLD_FONT_RE = re.compile(r"bold|black|semibold|demi|heavy|smbd|subhead|[-,]bd\b|\.b\b|-b$", re.I)
MATH_FONT_RE = re.compile(r"cmmi|cmsy|cmex|cmr\d|msbm|msam|symbol|mt-?extra|mtmi|mtsy|cambria ?math|math|euclid|"
                          r"mathematica|rsfs|eufm|lmmath|stixmath|stix.*math", re.I)
CITE_ONLY_RE = re.compile(r"^[\d\s,–—−\-]+$")


@dataclass
class Line:
    bbox: Rect
    text: str
    size: float
    bold: bool
    font: str
    page: int
    math_ratio: float = 0.0
    n_chars: int = 0
    gaps: int = 0  # number of large horizontal gaps inside the line (table-like)
    first_span_bold: bool = False
    raw_dir: tuple[float, float] = (1.0, 0.0)
    tags: set[str] = field(default_factory=set)
    removed: list[str] = field(default_factory=list)  # citation markers dropped from this line

    @property
    def cy(self): return self.bbox.cy
    @property
    def x0(self): return self.bbox.x0
    @property
    def x1(self): return self.bbox.x1
    @property
    def y0(self): return self.bbox.y0
    @property
    def y1(self): return self.bbox.y1


def _is_bold(font: str, flags: int) -> bool:
    return bool(flags & 16) or bool(BOLD_FONT_RE.search(font))


def orientation_for(page, direction: tuple[int, int]) -> Orientation:
    w, h = page.rect.width, page.rect.height
    if direction == (0, -1):
        return Orientation(1, w, h)
    if direction == (0, 1):
        return Orientation(2, w, h)
    return Orientation(0, w, h)


@dataclass
class PageText:
    lines: list[Line]
    orient: Orientation
    margin: list[Line] = field(default_factory=list)  # thin rotated strips such as download watermarks
    rotated: list[tuple[list[Line], Orientation]] = field(default_factory=list)  # sideways tables / figures


def extract_lines(page, page_no: int, strip_citation_marks: bool) -> PageText:
    d = page.get_text("dict", flags=1 | 2 | 64)  # ligatures, whitespace, clip to mediabox
    groups: dict[tuple[int, int], list[dict]] = {}
    for b in d["blocks"]:
        if b["type"] != 0:
            continue
        for ln in b["lines"]:
            if not "".join(s["text"] for s in ln["spans"]).strip():
                continue
            key = (round(ln["dir"][0]), round(ln["dir"][1]))
            groups.setdefault(key, []).append(ln)

    page_w, page_h = page.rect.width, page.rect.height
    built: dict[tuple[int, int], list[Line]] = {}
    for key, raw_lines in groups.items():
        orient = orientation_for(page, key if key in ((1, 0), (0, -1), (0, 1)) else (1, 0))
        out: list[Line] = []
        for ln in raw_lines:
            for line in _build_rows(ln, orient, page_no, strip_citation_marks):
                line.raw_dir = key
                out.append(line)
        built[key] = out

    def page_bbox(lines: list[Line], orient: Orientation) -> tuple[float, float]:
        rs = [orient.to_page(ln.bbox) for ln in lines]
        return (max(r[2] for r in rs) - min(r[0] for r in rs), max(r[3] for r in rs) - min(r[1] for r in rs))

    margin: list[Line] = []
    solid: dict[tuple[int, int], list[Line]] = {}
    for key, lines in built.items():
        if not lines:
            continue
        orient = orientation_for(page, key if key in ((1, 0), (0, -1), (0, 1)) else (1, 0))
        w, h = page_bbox(lines, orient)
        chars = sum(ln.n_chars for ln in lines)
        if key != (1, 0) and (min(w, h) < 0.07 * min(page_w, page_h) or chars < 60 or len(lines) < 2):
            margin.extend(lines)  # watermark strip, tiny rotated label, ...
        else:
            solid[key] = lines
    if not solid:
        return PageText([], Orientation(0, page_w, page_h), margin)
    chars = {k: sum(ln.n_chars for ln in v) for k, v in solid.items()}
    main = (1, 0) if (1, 0) in solid and chars[(1, 0)] * 3 >= max(chars.values()) else max(chars, key=chars.get)
    pt = PageText(_merge_row_fragments(solid[main]), orientation_for(page, main), margin)
    for key, lines in solid.items():
        if key != main:
            pt.rotated.append((_merge_row_fragments(lines), orientation_for(page, key)))
    return pt


def _build_rows(ln: dict, orient: Orientation, page_no: int, strip_cites: bool) -> list[Line]:
    """One PyMuPDF line may hold spans from several visual rows (e.g. a hanging heading number)."""
    spans = [s for s in ln["spans"] if s["text"] != ""]
    if not spans:
        return []

    def oy(s) -> float:
        ox, oyy = s["origin"]
        return orient.to_upright((ox, oyy, ox, oyy)).y0

    rows: list[list[dict]] = []
    for s in sorted(spans, key=lambda s: 0):  # keep stream order; cluster by baseline
        for row in rows:
            ref = max(row, key=lambda x: x["size"])
            if abs(oy(s) - oy(ref)) < 0.55 * max(s["size"], ref["size"]):
                row.append(s)
                break
        else:
            rows.append([s])
    out: list[Line] = []
    for row in rows:
        row.sort(key=lambda s: orient.to_upright(s["bbox"]).x0)
        x0 = min(orient.to_upright(s["bbox"]).x0 for s in row)
        x1 = max(orient.to_upright(s["bbox"]).x1 for s in row)
        y0 = min(orient.to_upright(s["bbox"]).y0 for s in row)
        y1 = max(orient.to_upright(s["bbox"]).y1 for s in row)
        fake = {"bbox": (0, 0, 0, 0)}
        line = _build_line(row, fake, orient, page_no, strip_cites)
        if line is not None:
            line.bbox = Rect(x0, y0, x1, y1)
            out.append(line)
    return out


def _build_line(spans, ln, orient: Orientation, page_no: int, strip_cites: bool) -> Line | None:
    sp = [(s, orient.to_upright(s["bbox"])) for s in spans]
    sizes: Counter = Counter()
    fonts: Counter = Counter()
    for s, _ in sp:
        n = len(s["text"].strip())
        sizes[round(s["size"], 1)] += n
        fonts[s["font"]] += n
    if not sizes:
        return None
    dom = sizes.most_common(1)[0][0]
    def origin_y(s) -> float:
        ox, oy = s["origin"]
        return orient.to_upright((ox, oy, ox, oy)).y0

    base_ys = [origin_y(s) for s, r in sp if abs(s["size"] - dom) < 0.6 and s["text"].strip()]
    base = sorted(base_ys)[len(base_ys) // 2] if base_ys else origin_y(sp[0][0])

    parts: list[str] = []
    gaps = 0
    prev_r: Rect | None = None
    glue_fix = False
    removed: list[str] = []
    n_chars = math_chars = bold_chars = 0
    raised_flags = [sp_[0]["size"] < dom * 0.9 and (origin_y(sp_[0]) < base - 0.2 * dom or bool(sp_[0]["flags"] & 1))
                    for sp_ in sp]
    skip_until = -1
    for i, (s, r) in enumerate(sp):
        if i <= skip_until:
            continue
        t = s["text"]
        if raised_flags[i] and strip_cites and t.strip():
            j = i  # a citation like "21-23" is often split over several raised spans
            while j + 1 < len(sp) and raised_flags[j + 1]:
                j += 1
            run = "".join(x[0]["text"] for x in sp[i:j + 1])
            after = sp[j + 1][0]["text"] if j + 1 < len(sp) else ""
            if CITE_ONLY_RE.match(run.strip() or "x") and _is_citation_superscript(run, "".join(parts), after):
                prev_r = sp[j][1]
                removed.append(run.strip())
                glue_fix = True
                skip_until = j
                continue
        if prev_r is not None and parts:
            gap = r.x0 - prev_r.x1
            if gap > 0.18 * dom and not parts[-1].endswith(" ") and not t.startswith(" "):
                parts.append(" ")
            elif glue_fix and parts[-1][-1:] in ".!?)" and t[:1].isupper():
                parts.append(" ")  # a removed citation marker hid the space after the sentence end
            if gap > 1.6 * dom:
                gaps += 1
        parts.append(t)
        prev_r = r
        glue_fix = False
        k = len(t.strip())
        n_chars += k
        if MATH_FONT_RE.search(s["font"]) or (s["size"] > 0 and any(0x2200 <= ord(c) <= 0x22ff for c in t)):
            math_chars += k
        if _is_bold(s["font"], s["flags"]):
            bold_chars += k
    text = normalize("".join(parts))
    if not text:
        return None
    bbox = Rect(0, 0, 0, 0)
    first_bold = _is_bold(sp[0][0]["font"], sp[0][0]["flags"])
    font = fonts.most_common(1)[0][0]
    return Line(bbox=bbox, text=text, size=dom, bold=bold_chars >= 0.7 * max(n_chars, 1), font=font, page=page_no,
                math_ratio=math_chars / max(n_chars, 1), n_chars=n_chars, gaps=gaps, first_span_bold=first_bold,
                removed=removed)


LABEL_RE = re.compile(r"^\s*(?:\d+(?:\.\d+)*|(?:fig(?:ure)?\.?|table|scheme|chart)\s*S?\d+[A-Za-z]?|[A-Za-z]\d+)\s*[|.:]?\s*$", re.I)


def _v_overlap(a: Line, b: Line) -> float:
    return min(a.y1, b.y1) - max(a.y0, b.y0)


def _join(a: Line, b: Line) -> Line:
    """Merge b (to the right of a) into one line."""
    gap = b.x0 - a.x1
    sep = " " if gap > 0.15 * max(a.size, b.size) and not a.text.endswith(" ") else ""
    big, small = (a, b) if a.n_chars >= b.n_chars else (b, a)
    n = a.n_chars + b.n_chars
    return Line(bbox=a.bbox.union(b.bbox), text=a.text + sep + b.text, size=big.size,
                bold=(a.bold * a.n_chars + b.bold * b.n_chars) >= 0.7 * max(n, 1), font=big.font, page=a.page,
                math_ratio=(a.math_ratio * a.n_chars + b.math_ratio * b.n_chars) / max(n, 1), n_chars=n,
                gaps=a.gaps + b.gaps + (1 if gap > 1.6 * big.size else 0),
                first_span_bold=a.first_span_bold, raw_dir=a.raw_dir, removed=a.removed + b.removed)


def _merge_row_fragments(lines: list[Line]) -> list[Line]:
    """Repair lines that PyMuPDF split inside one visual row.

    * drops exact / contained duplicates (text drawn twice, e.g. a hidden copy under a heading)
    * glues hanging labels ('2.1 |', 'FIGURE 1 |') to their text
    * glues inline-math pieces back into their sentence
    * drops tiny sub/superscript fragments left over on their own

    Everything works on y-sorted windows, so pages with thousands of tiny labels (vector plots) stay fast.
    """
    lines = sorted(lines, key=lambda ln: (ln.y0, ln.x0))
    # 1. duplicates: only lines starting at nearly the same height can be duplicates
    kept: list[Line] = []
    for a in lines:
        dup = False
        for k in range(len(kept) - 1, -1, -1):
            b = kept[k]
            if b.y0 < a.y0 - 12:
                break
            if _v_overlap(a, b) > 0.7 * min(a.bbox.h, b.bbox.h) and a.bbox.h_overlap(b.bbox) > 0.7 * min(a.bbox.w, b.bbox.w):
                ta, tb = re.sub(r"\W+", "", a.text.lower()), re.sub(r"\W+", "", b.text.lower())
                if ta and tb and (ta in tb or tb in ta):
                    if len(ta) > len(tb):
                        kept[k] = a
                    dup = True
                    break
        if not dup:
            kept.append(a)
    # 2. group lines into visual rows (by vertical centre), then merge neighbours inside each row
    rows: list[list[Line]] = []
    for ln in sorted(kept, key=lambda l: l.cy):
        placed = False
        for row in reversed(rows[-12:]):
            rep = max(row, key=lambda l: l.size)
            if rep.cy < ln.cy - 3 * max(rep.size, ln.size):
                break
            big = max(rep.size, ln.size)
            same = abs(rep.cy - ln.cy) <= 0.45 * big or (
                min(rep.size, ln.size) <= 0.8 * big and _v_overlap(rep, ln) >= 0.7 * min(rep.bbox.h, ln.bbox.h))
            if same:
                row.append(ln)
                placed = True
                break
        if not placed:
            rows.append([ln])
    merged: list[Line] = []
    for row in rows:
        row.sort(key=lambda l: l.x0)
        cur = row[0]
        for nxt in row[1:]:
            gap = nxt.x0 - cur.x1
            big = max(cur.size, nxt.size)
            label = bool(LABEL_RE.match(cur.text)) and len(cur.text) <= 14 and not LABEL_RE.match(nxt.text) and 0 <= gap <= 3.2 * cur.size
            overlap_ok = gap >= -18.0 and min(cur.n_chars, nxt.n_chars) <= 14  # inline-math glyph runs overlap a little
            if label or ((-2.0 <= gap or overlap_ok) and gap <= 0.9 * big):
                cur = _join(cur, nxt)
            else:
                merged.append(cur)
                cur = nxt
        merged.append(cur)
    # a label whose text sits on a neighbouring row ("2.1 |" centred beside a two-line heading)
    merged.sort(key=lambda ln: (ln.y0, ln.x0))
    out: list[Line] = []
    used: set[int] = set()
    for i, a in enumerate(merged):
        if id(a) in used:
            continue
        if LABEL_RE.match(a.text) and len(a.text) <= 14:
            for j in range(i + 1, min(i + 6, len(merged))):
                b = merged[j]
                if id(b) in used or LABEL_RE.match(b.text):
                    continue
                if 0 <= b.x0 - a.x1 <= 3.2 * a.size and (b.y0 <= a.cy <= b.y1) and abs(b.cy - a.cy) <= 1.3 * max(a.size, b.size):
                    out.append(_join(a, b))
                    used.add(id(b))
                    break
            else:
                out.append(a)
            continue
        out.append(a)
    # 3. stray sub/superscript fragments (windowed by y)
    out.sort(key=lambda ln: ln.y0)
    final: list[Line] = []
    for k, a in enumerate(out):
        if len(a.text) <= 2 and a.size <= 6.5:
            host = None
            for b in out[max(0, k - 40): k + 40]:
                if b is not a and b.size >= a.size + 1.2 and len(b.text) > 12 and b.x0 - 3 <= a.x0 and a.x1 <= b.x1 + 3 \
                        and abs(b.cy - a.cy) <= 0.9 * b.size:
                    host = b
                    break
            if host is not None:
                continue
        final.append(a)
    return final
