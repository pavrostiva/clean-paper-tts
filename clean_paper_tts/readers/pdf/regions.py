"""Detect figures, tables and display equations on a page (all in upright coordinates)."""

from __future__ import annotations

import re
from dataclasses import dataclass

from .geometry import Orientation, Rect
from .lines import Line

CAPTION_RE = re.compile(
    r"^\s*(?P<label>(?:Supplementary\s+)?(?:Figure|Fig\.?|FIGURE|FIG\.?|Scheme|SCHEME|Chart|CHART|Plate|Box|"
    r"Table|TABLE|Graphical Abstract|GRAPHICAL ABSTRACT)\s*[S]?\s*\d*[A-Za-z]?)\s*(?P<delim>[.:|–—-]?)")
TABLE_LABEL_RE = re.compile(r"^\s*(?:Supplementary\s+)?table\s*[S]?\d", re.I)


@dataclass
class Region:
    kind: str  # figure | table | formula
    bbox: Rect
    native_dpi: float = 0.0
    label: str = ""
    visual: object = None  # rendered Visual, filled in by the reader


# ----------------------------------------------------------------- captions
def is_caption_start(line: Line, body_size: float) -> bool:
    m = CAPTION_RE.match(line.text)
    if not m:
        return False
    label = m.group("label").strip()
    has_number = bool(re.search(r"\d", label)) or label.lower().startswith("graphical")
    if not has_number:
        return False
    rest = line.text[m.end():].strip()
    if not rest and not m.group("delim"):
        return line.bold or line.first_span_bold
    if m.group("delim"):
        return True
    return line.first_span_bold or line.bold or line.size < body_size - 0.4


# ------------------------------------------------------------ raster/vector
def _cluster(rects: list[Rect], gap: float) -> list[Rect]:
    rects = list(rects)
    changed = True
    while changed:
        changed = False
        out: list[Rect] = []
        for r in rects:
            for i, o in enumerate(out):
                if r.expanded(gap / 2).inter_area(o.expanded(gap / 2)) > 0 or r.gap_to(o) <= gap and \
                        (r.h_overlap(o) > 0 or min(r.y1, o.y1) - max(r.y0, o.y0) > 0):
                    out[i] = o.union(r)
                    changed = True
                    break
            else:
                out.append(r)
        rects = out
    return rects


def find_visual_regions(page, orient: Orientation, page_rect: Rect) -> list[Region]:
    regions: list[Region] = []
    raster: list[tuple[Rect, float]] = []
    try:
        infos = page.get_image_info()
    except Exception:
        infos = []
    for im in infos:
        r = orient.to_upright(im["bbox"])
        if r.w < 40 or r.h < 25 or r.area < 3000:
            continue
        if r.area > 0.85 * page_rect.area:
            continue  # full-page scan background
        dpi = (im.get("width", 0) / (r.w / 72.0)) if r.w else 0
        raster.append((r, dpi))
    vec: list[Rect] = []
    try:
        drawings = page.get_drawings()
    except Exception:
        drawings = []
    for dr in drawings:
        r = orient.to_upright(dr["rect"])
        items = dr.get("items", [])
        if r.w > 0.45 * page_rect.w and r.h < 3.0:
            continue  # table / header rules
        if r.h > 0.45 * page_rect.h and r.w < 3.0:
            continue
        if r.w < 0.5 and r.h < 0.5:
            continue
        if len(items) == 1 and items[0][0] == "re" and r.area > 0.2 * page_rect.area:
            continue  # page background / shaded abstract box
        vec.append(r)
    vec_clusters = [c for c in _cluster(vec, 6.0)] if vec else []
    n_items = lambda c: sum(1 for v in vec if v.frac_inside(c.expanded(1)) > 0.8)  # noqa: E731
    vec_clusters = [c for c in vec_clusters if c.w >= 60 and c.h >= 40 and n_items(c) >= 8]
    merged = _cluster([r for r, _ in raster] + vec_clusters, 12.0)
    for m in merged:
        dpis = [d for r, d in raster if r.frac_inside(m) > 0.5 or m.frac_inside(r) > 0.5]
        regions.append(Region("figure", m, native_dpi=max(dpis) if dpis else 0.0))
    return regions


# ------------------------------------------------------------------ tables
def _horizontal_rules(page, orient: Orientation) -> list[Rect]:
    rules: list[Rect] = []
    try:
        drawings = page.get_drawings()
    except Exception:
        return rules
    for dr in drawings:
        r = orient.to_upright(dr["rect"])
        if r.h <= 2.5 and r.w >= 30:
            rules.append(r)
    return sorted(rules, key=lambda r: r.y0)


def _looks_tabular(line: Line, body: float) -> bool:
    if line.gaps >= 1:
        return True
    digits = sum(c.isdigit() for c in line.text)
    if line.n_chars and digits / line.n_chars >= 0.3:
        return True
    words = line.text.split()
    return line.size < body - 0.4 and len(words) <= 8


def find_table_region(caption: Line, cap_last: Line, lines: list[Line], rules: list[Rect], body: float,
                      col: tuple[float, float], page_rect: Rect, forbidden: list[Rect],
                      extra: list[Rect]) -> Rect | None:
    """Locate the table body belonging to a table caption (below it, else above it)."""
    below = _walk(cap_last, lines, rules, body, col, page_rect, forbidden, extra, direction=1)
    if below is not None:
        return below
    return _walk(caption, lines, rules, body, col, page_rect, forbidden, extra, direction=-1)


def _in_col(r: Rect, col: tuple[float, float]) -> bool:
    return r.x1 > col[0] - 3 and r.x0 < col[1] + 3 and r.h_overlap(Rect(col[0], 0, col[1], 1)) > 0.3 * min(r.w, col[1] - col[0])


def _walk(anchor: Line, lines: list[Line], rules: list[Rect], body: float, col, page_rect: Rect,
          forbidden: list[Rect], extra: list[Rect], direction: int) -> Rect | None:
    cand = [ln for ln in lines if ln is not anchor and _in_col(ln.bbox, col)
            and not any(ln.bbox.frac_inside(f) > 0.5 for f in forbidden)
            and ((ln.y0 >= anchor.y1 - 1) if direction > 0 else (ln.y1 <= anchor.y0 + 1))]
    cand.sort(key=lambda ln: ln.y0 if direction > 0 else -ln.y1)
    region: Rect | None = None
    last_edge = anchor.y1 if direction > 0 else anchor.y0
    nontab = 0
    n_tab = 0
    foot_ok = False
    for ln in cand:
        gap = (ln.y0 - last_edge) if direction > 0 else (last_edge - ln.y1)
        if gap > 2.4 * body + 6 and region is not None:
            break
        if gap > 4.0 * body + 14:
            break
        if CAPTION_RE.match(ln.text) and is_caption_start(ln, body) and region is not None:
            break
        full_line = ln.size >= body - 0.3 and ln.bbox.w > 0.75 * (col[1] - col[0]) and ln.gaps == 0
        rule_near = any(abs(ln.cy - r.cy) < 14 and r.h_overlap(ln.bbox) > 0 for r in rules)
        inside_extra = any(ln.bbox.frac_inside(e) > 0.5 for e in extra)
        tab = inside_extra or (_looks_tabular(ln, body) and not full_line)
        if tab or (rule_near and not full_line):
            n_tab += 1
            nontab = 0
            region = ln.bbox if region is None else region.union(ln.bbox)
            last_edge = ln.y1 if direction > 0 else ln.y0
        else:
            nontab += 1
            if region is None and nontab >= 1 and full_line:
                break
            if nontab >= 2 or full_line:
                break
    if region is None or n_tab < 2:
        return None
    # extend to include the rules that frame the table
    for r in rules:
        if r.h_overlap(region) > 0.4 * region.w and region.y0 - 10 <= r.y0 <= region.y1 + 10:
            region = region.union(Rect(min(r.x0, region.x1 + 400), r.y0, r.x1, r.y1)) if r.w < page_rect.w else region
    for e in extra:
        if e.frac_inside(region.expanded(8)) > 0.6 or region.frac_inside(e) > 0.6:
            region = region.union(e)
    return region


# ---------------------------------------------------------------- equations
MATH_OPS_RE = re.compile(r"[=≈≠≤≥±∑∫√∂∇∈∞×÷−⋅→←⊙]")
EQ_NUMBER_RE = re.compile(r"\(\s*[A-Z]?\d+[a-z]?\s*\)\s*$")


def find_equation_regions(lines: list[Line], body: float, col_of, taken: list[Rect]) -> list[Region]:
    """Display equations: short, centred, operator-heavy lines (often in math fonts)."""
    mathy: list[Line] = []
    for ln in lines:
        if any(ln.bbox.frac_inside(t) > 0.5 for t in taken):
            continue
        if ln.size > body + 1.5 or ln.bold:
            continue
        cx0, cx1 = col_of(ln)
        text = ln.text
        letters = sum(c.isalpha() for c in text)
        long_words = len([w for w in re.findall(r"[A-Za-z]{4,}", text)])
        score = 0
        if ln.math_ratio >= 0.3:
            score += 2
        if MATH_OPS_RE.search(text) or "=" in text:
            score += 1
        else:
            continue
        if long_words <= 1:
            score += 1
        elif long_words >= 5:
            continue
        nonalnum = sum(not (c.isalnum() or c.isspace()) for c in text)
        if len(text) and nonalnum / len(text) >= 0.2:
            score += 1
        left_gap, right_gap = ln.x0 - cx0, cx1 - ln.x1
        width = max(cx1 - cx0, 1)
        eq_num = bool(EQ_NUMBER_RE.search(text))
        centred = left_gap > 0.08 * width and (right_gap > 0.08 * width or eq_num)
        if centred:
            score += 1
        if letters and ln.bbox.w > 0.92 * width and not eq_num and ln.math_ratio < 0.3:
            continue  # a full-width prose line
        compact = len(text.replace(" ", "")) >= 5 or ln.math_ratio >= 0.5
        strong = eq_num and ("=" in text or MATH_OPS_RE.search(text)) and ln.bbox.w < 0.9 * width
        if compact and (score >= 4 or strong):
            mathy.append(ln)
    mathy.sort(key=lambda ln: (ln.y0, ln.x0))
    regions: list[Region] = []
    used: set[int] = set()
    for i, ln in enumerate(mathy):
        if i in used:
            continue
        box = ln.bbox
        for j in range(i + 1, len(mathy)):
            o = mathy[j]
            if o.y0 - box.y1 <= 1.6 * body and o.bbox.h_overlap(box) > 0:
                box = box.union(o.bbox)
                used.add(j)
        # absorb small sub/superscript fragments, fraction bars and the equation number
        for o in lines:
            if o is ln or any(o is m for m in mathy):
                continue
            near = o.bbox.expanded(0).gap_to(box) <= 0.9 * body and o.bbox.h_overlap(box) > 0
            same_row = o.cy > box.y0 - 2 and o.cy < box.y1 + 2 and 0 <= o.x0 - box.x1 < 80
            if (near and (o.size < body - 0.6 or len(o.text) <= 3)) or (same_row and EQ_NUMBER_RE.search(o.text)):
                box = box.union(o.bbox)
        if box.h <= 9 * body:
            regions.append(Region("formula", box.expanded(2)))
    return regions


# -------------------------------------------------------------- code listings
_NUMBERED = re.compile(r"^\s*(\d{1,3})\s*[:.)]?\s+\S")
# a pseudo-code statement starts with a keyword (after the line number) or is an assignment
_CODE_WORDS = re.compile(
    r"^\s*\d{1,3}\s*[:.)]?\s+(?:(?:for|end|if|then|else|while|do|return|procedure|function|input|output|require|ensure|let|set|"
    r"foreach|repeat|until|call|break|continue|initialize)\b|\w+(?:\[[^\]]*\])?\s*(?:\u2190|:=|<-|=))", re.I)
_LISTING_HEAD = re.compile(r"^\s*(algorithm\s*\d*|input|output|require|ensure|procedure|function)\b", re.I)


def find_listing_regions(lines: list[Line], body: float, taken: list[Rect]) -> list[Region]:
    """Numbered pseudo-code ('1: for i in ...') is unreadable aloud; show it as an image instead."""
    cands = sorted((ln for ln in lines if not any(ln.bbox.frac_inside(t) > 0.5 for t in taken)),
                   key=lambda ln: (ln.x0 > 0 and ln.y0, ln.x0))
    regions: list[Region] = []
    i = 0
    cands = sorted(cands, key=lambda ln: (ln.y0, ln.x0))
    while i < len(cands):
        m = _NUMBERED.match(cands[i].text)
        if not m:
            i += 1
            continue
        run = [cands[i]]
        last = int(m.group(1))
        j = i + 1
        while j < len(cands):
            ln = cands[j]
            mm = _NUMBERED.match(ln.text)
            if mm and int(mm.group(1)) == last + 1 and abs(ln.x0 - run[0].x0) < 80 and ln.y0 - run[-1].y1 < 2.5 * body:
                run.append(ln)
                last += 1
                j += 1
            elif not mm and ln.y0 - run[-1].y1 < 1.2 * body and ln.x0 >= run[0].x0 - 3 and ln.bbox.w < 0.9 * (run[0].bbox.w + 200):
                j += 1  # continuation line of a long statement
            else:
                break
        keyword_share = sum(bool(_CODE_WORDS.search(ln.text)) for ln in run) / len(run)
        colon_share = sum(bool(re.match(r"^\s*\d{1,3}\s*:", ln.text)) for ln in run) / len(run)
        if len(run) >= 5 and keyword_share >= 0.5 and (colon_share >= 0.6 or keyword_share >= 0.8):
            box = run[0].bbox
            for ln in cands[i:j]:
                box = box.union(ln.bbox)
            for ln in cands:  # header lines right above: "Algorithm 1 ...", "Input: ..."
                if _LISTING_HEAD.match(ln.text) and 0 <= box.y0 - ln.y1 <= 2.0 * body and ln.bbox.h_overlap(box) > 0:
                    box = box.union(ln.bbox)
            regions.append(Region("figure", box.expanded(3), label="algorithm"))
            i = j
        else:
            i += 1
    return regions


# ------------------------------------------------- numbered display equations
_NUMBER_ONLY = re.compile(r"^\s*\(\s*\d{1,3}[a-z]?\s*\)\s*$")


def find_numbered_equations(lines: list[Line], body: float, col_of, taken: list[Rect]) -> list[Region]:
    """Equations with a right-aligned number '(n)': take the whole stack of non-prose rows around it.

    Fractions, sums and sub/superscripts are spread over several rows that no single-line heuristic can
    pair up; the equation number is a reliable anchor and the surrounding flush-left prose delimits the block.
    """
    free = [ln for ln in lines if not any(ln.bbox.frac_inside(t) > 0.5 for t in taken)]
    free.sort(key=lambda ln: ln.y0)
    regions: list[Region] = []
    used: set[int] = set()
    for anchor in free:
        if id(anchor) in used:
            continue
        cx0, cx1 = col_of(anchor)
        w = max(cx1 - cx0, 1.0)
        text = anchor.text.strip()
        at_right = anchor.x1 >= cx1 - 0.06 * w
        number_only = bool(_NUMBER_ONLY.match(text))
        ends_with_number = bool(EQ_NUMBER_RE.search(text)) and anchor.x0 - cx0 > 0.1 * w
        if not (at_right and (number_only or ends_with_number)):
            continue

        def prose(ln: Line) -> bool:
            longw = sum(len(re.sub(r"\W", "", x)) >= 4 for x in ln.text.split())
            return ln.x0 - cx0 <= 0.06 * w and (longw >= 1 or len(ln.text.split()) >= 5) and ln.math_ratio < 0.4

        def near(ln: Line) -> bool:
            return col_of(ln) == col_of(anchor) and ln.size <= body + 1.5 and not ln.bold

        box = anchor.bbox
        members = [anchor]
        pool = [ln for ln in free if ln is not anchor and near(ln) and id(ln) not in used]
        changed = True
        while changed and len(members) < 40:
            changed = False
            for ln in pool:
                if any(ln is m for m in members):
                    continue
                dist = max(ln.y0 - box.y1, box.y0 - ln.y1, 0.0)  # rows of one equation interleave vertically
                if dist <= 0.9 * body and not prose(ln) and not is_caption_start(ln, body):
                    members.append(ln)
                    box = box.union(ln.bbox)
                    changed = True
        content = [m for m in members if m is not anchor]
        if not content and not ends_with_number:
            continue  # only a bare number: nothing to render
        for m in members:
            used.add(id(m))
        regions.append(Region("formula", box.expanded(2)))
    return regions
