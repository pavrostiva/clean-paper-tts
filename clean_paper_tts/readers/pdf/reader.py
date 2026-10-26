"""Orchestrates the PDF pipeline and produces a Document."""

from __future__ import annotations

import io
import re
from difflib import SequenceMatcher
from collections import Counter
from dataclasses import dataclass, field

from PIL import Image

from ...model import Document, Heading, Paragraph, Visual
from ...options import Options
from ...render.images import to_visual
from ...filters.noise import match_noise
from ...textutil import clean_heading, join_lines, normalize
from .geometry import Orientation, Rect
from .lines import Line, PageText, extract_lines
from .regions import (CAPTION_RE, TABLE_LABEL_RE, Region, find_equation_regions, find_table_region,
                      find_visual_regions, _horizontal_rules, is_caption_start)

MAX_PAGES = 400
HEADER_ZONE = 0.075
BULLET_RE = re.compile(r"^\s*(?:[•▪●◦‣\-–—*]\s+|\(?\d{1,2}[.)]\s+\S|\(?[a-z][.)]\s+[A-Z])")
SENTENCE_END = (".", "!", "?", ":", ";", ")", "]", '"', "'", "”")
ABSTRACT_RE = re.compile(r"^\s*(?:a\s?b\s?s\s?t\s?r\s?a\s?c\s?t|summary|abstract)\s*[:.—–-]?\s*", re.I)
AFFIL_WORDS = re.compile(r"\b(department|university|institute|hospital|school|laborator|college|center|centre|"
                         r"faculty|academy|corresponding|e-?mail|china|usa|germany|united|kingdom)\b", re.I)


@dataclass
class PageData:
    idx: int
    lines: list[Line]
    off: list[Line]
    orient: Orientation
    rect: Rect
    rotated: list = field(default_factory=list)
    regions: list[Region] = field(default_factory=list)


@dataclass
class RawPara:
    lines: list[Line]
    page: int
    role: str = "body"
    col: tuple[float, float] = (0, 0)

    @property
    def size(self) -> float:
        return max(ln.size for ln in self.lines)

    @property
    def bold(self) -> bool:
        return all(ln.bold for ln in self.lines)

    @property
    def text(self) -> str:
        return join_lines([ln.text for ln in self.lines])


@dataclass
class RotatedGroup:
    """A sideways table / figure on an otherwise upright page, already rendered."""

    bbox: Rect
    items: list


@dataclass
class RawVisual:
    region: Region
    page: int
    caption_for: str = ""


# ------------------------------------------------------------------ helpers
def _percentile(vals: list[float], q: float) -> float:
    vals = sorted(vals)
    return vals[min(len(vals) - 1, max(0, int(q * (len(vals) - 1))))]


class Layout:
    """Column geometry of one page."""

    def __init__(self, lines: list[Line], page_rect: Rect, hint_gx: float | None = None):
        long_lines = [ln for ln in lines if ln.n_chars >= 20] or lines
        if not long_lines:
            self.x_min, self.x_max, self.two_col, self.gx = page_rect.x0, page_rect.x1, False, page_rect.cx
            self.left = self.right = (self.x_min, self.x_max)
            return
        self.x_min = _percentile([ln.x0 for ln in long_lines], 0.03)
        self.x_max = _percentile([ln.x1 for ln in long_lines], 0.97)
        width = max(self.x_max - self.x_min, 1)
        mid = (self.x_min + self.x_max) / 2
        best, best_cross = mid, 10 ** 9
        x = mid - 0.12 * width
        while x <= mid + 0.12 * width:
            cross = sum(1 for ln in long_lines if ln.x0 < x - 2 and ln.x1 > x + 2)
            if cross < best_cross or (cross == best_cross and abs(x - mid) < abs(best - mid)):
                best, best_cross = x, cross
            x += 2
        self.gx = best
        left_only = [ln for ln in lines if ln.x1 <= self.gx + 3 and ln.n_chars >= 8]
        right_only = [ln for ln in lines if ln.x0 >= self.gx - 3 and ln.n_chars >= 8]
        crossing = [ln for ln in long_lines if ln.x0 < self.gx - 6 and ln.x1 > self.gx + 6]
        self.two_col = (len(left_only) >= 6 and len(right_only) >= 6 and len(crossing) <= 0.3 * len(long_lines)
                        and width > 0.5 * page_rect.w)
        if not self.two_col and hint_gx is not None and len(long_lines) < 30:
            # sparse page (mostly a figure): trust the column structure of the rest of the document
            l2 = [ln for ln in lines if ln.x1 <= hint_gx + 3 and ln.n_chars >= 8]
            r2 = [ln for ln in lines if ln.x0 >= hint_gx - 3 and ln.n_chars >= 8]
            cross = [ln for ln in long_lines if ln.x0 < hint_gx - 6 and ln.x1 > hint_gx + 6]
            if len(l2) >= 2 and len(r2) >= 2 and len(cross) <= 0.5 * len(long_lines):
                self.gx, self.two_col, left_only, right_only = hint_gx, True, l2, r2
        if self.two_col:
            self.left = (self.x_min, _percentile([ln.x1 for ln in left_only], 0.95))
            self.right = (_percentile([ln.x0 for ln in right_only], 0.05), self.x_max)
        else:
            self.left = self.right = (self.x_min, self.x_max)

    def side(self, r: Rect) -> str:
        if not self.two_col:
            return "wide"
        if r.x0 < self.gx - 6 and r.x1 > self.gx + 6:
            return "wide"
        return "left" if r.cx < self.gx else "right"

    def col_of(self, ln: Line) -> tuple[float, float]:
        s = self.side(ln.bbox)
        return (self.x_min, self.x_max) if s == "wide" else self.left if s == "left" else self.right


def _order(items: list, layout: Layout, rect_of) -> list:
    """Reading order: top-to-bottom, left column before right between full-width items."""
    items = sorted(items, key=lambda it: (rect_of(it).y0, rect_of(it).x0))
    if not layout.two_col:
        return items
    out, seg_l, seg_r = [], [], []

    def flush():
        out.extend(sorted(seg_l, key=lambda it: rect_of(it).y0))
        out.extend(sorted(seg_r, key=lambda it: rect_of(it).y0))
        seg_l.clear()
        seg_r.clear()

    for it in items:
        s = layout.side(rect_of(it))
        if s == "wide":
            flush()
            out.append(it)
        elif s == "left":
            seg_l.append(it)
        else:
            seg_r.append(it)
    flush()
    return out


def _mode_x0(lines: list[Line]) -> float:
    c = Counter(round(ln.x0) for ln in lines if ln.n_chars >= 25)
    return float(c.most_common(1)[0][0]) if c else min((ln.x0 for ln in lines), default=0.0)


# ---------------------------------------------------------------- the reader
class PdfReader:
    def __init__(self, data: bytes, options: Options):
        import pymupdf

        self.pymupdf = pymupdf
        self.pdf = pymupdf.open(stream=data, filetype="pdf")
        if self.pdf.needs_pass:
            raise ValueError("The PDF is password-protected.")
        self.opt = options
        self.doc = Document(source_type="pdf")
        self.pages: list[PageData] = []
        self.body = 9.0
        self.col_hint: float | None = None

    # --------------------------------------------------------------- run
    def read(self) -> Document:
        n = min(len(self.pdf), MAX_PAGES)
        if len(self.pdf) > MAX_PAGES:
            self.doc.warnings.append(f"Only the first {MAX_PAGES} pages were processed.")
        for i in range(n):
            page = self.pdf[i]
            try:
                page.set_rotation(0)
                pt = extract_lines(page, i, self.opt.strip_citations)
            except Exception as e:  # keep going on damaged pages
                self.doc.warnings.append(f"Page {i + 1}: text extraction failed ({e}).")
                continue
            uw, uh = pt.orient.upright_size
            self.pages.append(PageData(i, pt.lines, pt.margin, pt.orient, Rect(0, 0, uw, uh), pt.rotated))
        total_chars = sum(ln.n_chars for p in self.pages for ln in p.lines)
        if total_chars < 200 and len(self.pdf) > 0:
            self.doc.warnings.append(
                "Almost no selectable text found: this looks like a scanned PDF. OCR is not supported yet.")
        self.doc.citations_removed = [c for p in self.pages for ln in p.lines for c in ln.removed]
        self._body_size()
        self._drop_margin_text()
        self._drop_running_headers()
        gxs = [lay.gx for lay in (Layout(p.lines, p.rect) for p in self.pages if p.lines) if lay.two_col]
        self.col_hint = sorted(gxs)[len(gxs) // 2] if len(gxs) >= max(2, 0.4 * len(self.pages)) else None
        self._read_metadata()
        raw: list[RawPara | RawVisual] = []
        for pd in self.pages:
            raw.extend(self._process_page(pd))
        self._finish(raw)
        return self.doc

    def _body_size(self) -> None:
        c: Counter = Counter()
        for p in self.pages:
            for ln in p.lines:
                c[round(ln.size * 2) / 2] += ln.n_chars
        if c:
            (top, n_top), *rest = c.most_common(4)
            body = top
            # journals often use a smaller font for methods / references; prefer the larger main-text size
            for size, n in rest:
                if body < size <= top + 2.5 and n >= 0.6 * n_top:
                    body = size
            self.body = body

    def _read_metadata(self) -> None:
        md = self.pdf.metadata or {}
        t = (md.get("title") or "").strip()
        if t and len(t) > 12 and not re.search(r"\.(pdf|docx?|tex|indd)\b|^untitled|microsoft word", t, re.I):
            self.doc.metadata["pdf_title"] = normalize(t)
        if md.get("author"):
            self.doc.metadata["pdf_author"] = md["author"]
        m = re.search(r"10\.\d{4,9}/[^\s\"<>]+", (md.get("subject") or "") + " " + (md.get("keywords") or ""))
        if m:
            self.doc.metadata["doi"] = m.group(0).rstrip(".,;")

    # --------------------------------------------------------- noise passes
    def _drop_margin_text(self) -> None:
        seen = set()
        for p in self.pages:
            for ln in p.off:
                key = re.sub(r"\d+", "#", ln.text.lower())[:60]
                if key not in seen:
                    seen.add(key)
                    self.doc.drop("margin watermark", ln.text, p.idx + 1)

    def _drop_running_headers(self) -> None:
        n = len(self.pages)
        keys: Counter = Counter()

        def key_of(ln: Line) -> str:
            return re.sub(r"\d+", "#", ln.text.lower()).strip()

        def zone(p: PageData, ln: Line) -> bool:
            return ln.cy < p.rect.h * HEADER_ZONE or ln.cy > p.rect.h * (1 - HEADER_ZONE)

        for p in self.pages:
            for k in {key_of(ln) for ln in p.lines if zone(p, ln)}:
                keys[k] += 1
        thresh = max(2, int(0.3 * n))
        for p in self.pages:
            kept = []
            for ln in p.lines:
                if zone(p, ln):
                    k = key_of(ln)
                    if (n >= 2 and keys[k] >= thresh) or re.fullmatch(r"[#\s|/of]*", k) or re.fullmatch(r"page # of #", k):
                        self.doc.drop("running header/footer", ln.text, p.idx + 1)
                        continue
                kept.append(ln)
            p.lines = kept

    # ------------------------------------------------------------ per page
    def _caption_groups(self, lines: list[Line], layout: Layout) -> list[list[Line]]:
        """Caption paragraphs (start line + continuation) in reading order."""
        groups: list[list[Line]] = []
        taken: set[int] = set()
        for ln in sorted(lines, key=lambda l: (l.y0, l.x0)):
            if id(ln) in taken or not is_caption_start(ln, self.body):
                continue
            grp = [ln]
            taken.add(id(ln))
            cur = ln
            col = layout.col_of(ln)
            while len(grp) < 40:
                nxt = [o for o in lines if id(o) not in taken
                       and abs(o.x0 - ln.x0) < 12 + 2 * ln.size and o.x1 <= col[1] + 6
                       and 0 <= o.y0 - cur.y1 <= 0.6 * cur.size + 2 and abs(o.size - ln.size) < 0.7
                       and not is_caption_start(o, self.body)]
                if not nxt:
                    break
                cur = min(nxt, key=lambda o: o.y0)
                taken.add(id(cur))
                grp.append(cur)
            groups.append(grp)
        return groups

    def _render(self, pd: PageData, rect: Rect, kind: str, native_dpi: float = 0.0) -> Visual | None:
        pm = self.pymupdf
        page = self.pdf[pd.idx]
        clip = Rect(max(rect.x0, 0), max(rect.y0, 0), min(rect.x1, pd.rect.w), min(rect.y1, pd.rect.h))
        if clip.w < 8 or clip.h < 8:
            return None
        dpi = self.opt.render_dpi
        if kind == "figure" and native_dpi:
            dpi = int(max(dpi, min(native_dpi, 260)))
        elif kind == "formula":
            dpi = max(dpi, 220)
        while clip.w * dpi / 72 * clip.h * dpi / 72 > 36_000_000 and dpi > 72:
            dpi = int(dpi * 0.8)
        try:
            pr = pm.Rect(*pd.orient.to_page(clip))
            pix = page.get_pixmap(matrix=pm.Matrix(dpi / 72, dpi / 72), clip=pr, alpha=False)
            im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        except Exception as e:
            self.doc.warnings.append(f"Page {pd.idx + 1}: could not render a {kind} ({e}).")
            return None
        if pd.orient.kind == 1:
            im = im.rotate(-90, expand=True)
        elif pd.orient.kind == 2:
            im = im.rotate(90, expand=True)
        buf = io.BytesIO()
        im.save(buf, "PNG")
        return to_visual(buf.getvalue(), kind, "", self.opt.max_image_width * (2 if kind == "table" else 1), dpi)

    def _process_page(self, pd: PageData) -> list[RawPara | RawVisual]:
        page = self.pdf[pd.idx]
        lines = list(pd.lines)
        layout = Layout(lines, pd.rect, self.col_hint)
        regions = find_visual_regions(page, pd.orient, pd.rect)
        caption_groups = self._caption_groups(lines, layout)
        cap_ids = {id(ln) for g in caption_groups for ln in g}

        def absorb(region: Region, reason: str, only_short: bool = False) -> None:
            nonlocal lines
            keep = []
            for ln in lines:
                if id(ln) in cap_ids:
                    keep.append(ln)
                    continue
                inside = ln.bbox.frac_inside(region.bbox) >= (0.75 if only_short else 0.6)
                if inside:
                    self.doc.drop(reason, ln.text, pd.idx + 1)
                else:
                    keep.append(ln)
            lines = keep

        # figures: absorb labels around vector drawings, then drop text inside
        for r in regions:
            for _ in range(2):
                for ln in lines:
                    if id(ln) in cap_ids or ln.n_chars > 60 or ln.bbox.frac_inside(r.bbox) >= 0.6:
                        continue
                    if ln.size > self.body + 0.3 and ln.n_chars > 25:
                        continue
                    if r.bbox.expanded(9).inter_area(ln.bbox) > 0 and ln.bbox.h_overlap(r.bbox) > 0:
                        r.bbox = r.bbox.union(ln.bbox)
            absorb(r, "figure text")

        # tables
        rules = None
        extra: list[Rect] = []
        for grp in caption_groups:
            first = grp[0]
            if not TABLE_LABEL_RE.match(first.text):
                continue
            if rules is None:
                rules = _horizontal_rules(page, pd.orient)
                try:
                    for t in page.find_tables().tables:
                        if t.row_count >= 2 and t.col_count >= 2:
                            extra.append(pd.orient.to_upright(t.bbox))
                except Exception:
                    pass
            col = layout.col_of(first)
            if first.bbox.w > 0.6 * (layout.x_max - layout.x_min):
                col = (layout.x_min, layout.x_max)
            candidates = [ln for ln in lines if id(ln) not in cap_ids]
            reg = find_table_region(first, grp[-1], candidates, rules, self.body, col, pd.rect,
                                    [r.bbox for r in regions], extra)
            if reg is None:
                self.doc.warnings.append(f"Page {pd.idx + 1}: could not locate the body of '{first.text[:40]}'; "
                                         "its text is left inline.")
                continue
            tr = Region("table", reg.expanded(3), label=first.text[:30])
            regions.append(tr)
            absorb(tr, "table body")

        # display equations
        if self.opt.formulas_as_images:
            eqs = find_equation_regions([ln for ln in lines if id(ln) not in cap_ids], self.body, layout.col_of,
                                        [r.bbox for r in regions])
            for e in eqs:
                regions.append(e)
                absorb(e, "equation")
        if pd.idx == self.pages[0].idx:  # small vector boxes at the bottom of page 1: dates, logos, cover thumbnails
            for r in list(regions):
                if r.kind == "figure" and r.native_dpi == 0 and r.bbox.area < 30000 and r.bbox.y0 > 0.6 * pd.rect.h:
                    regions.remove(r)
                    self.doc.drop("page-1 metadata box", "[vector box near page foot]", pd.idx + 1)
        pd.regions = regions

        # sideways tables (landscape tables on a portrait page)
        rotated_groups = [g for g in (self._rotated_group(pd, rl, ro) for rl, ro in pd.rotated) if g is not None]

        # reading order over text lines and visual regions
        items: list = [ln for ln in lines] + [RawVisual(r, pd.idx) for r in regions] + rotated_groups

        def rect_of(it) -> Rect:
            if isinstance(it, (Line, RotatedGroup)):
                return it.bbox
            return it.region.bbox

        ordered = _order(items, layout, rect_of)
        out: list[RawPara | RawVisual] = []
        cur: RawPara | None = None
        prev: Line | None = None
        col_x0 = {s: _mode_x0([ln for ln in lines if layout.side(ln.bbox) == s]) for s in ("left", "right", "wide")}
        col_x1 = {}
        for s in ("left", "right", "wide"):
            xs = [ln.x1 for ln in lines if layout.side(ln.bbox) == s and ln.n_chars >= 25]
            col_x1[s] = _percentile(xs, 0.9) if xs else layout.x_max
        for it in ordered:
            if isinstance(it, (RawVisual, RotatedGroup)):
                if cur:
                    out.append(cur)
                    cur, prev = None, None
                out.extend(it.items) if isinstance(it, RotatedGroup) else out.append(it)
                continue
            ln = it
            side = layout.side(ln.bbox)
            if cur is None or prev is None or self._para_break(prev, ln, side, col_x0, col_x1, id(ln) in cap_ids,
                                                                id(prev) in cap_ids, ln, cap_ids):
                if cur:
                    out.append(cur)
                cur = RawPara([ln], pd.idx, "caption" if id(ln) in cap_ids and is_caption_start(ln, self.body) else "body",
                              layout.col_of(ln))
                if id(ln) in cap_ids and cur.role != "caption":
                    cur.role = "caption"
            else:
                cur.lines.append(ln)
            prev = ln
        if cur:
            out.append(cur)
        for it in out:
            if isinstance(it, RawVisual) and it.region.visual is None:
                it.region.visual = self._render(pd, it.region.bbox, it.region.kind, it.region.native_dpi)
        return out

    def _rotated_group(self, pd: PageData, rlines: list[Line], rorient: Orientation) -> RotatedGroup | None:
        ruw, ruh = rorient.upright_size
        rpd = PageData(pd.idx, rlines, [], rorient, Rect(0, 0, ruw, ruh))
        layout = Layout(rlines, rpd.rect)
        groups = self._caption_groups(rlines, layout)
        cap_ids = {id(ln) for g in groups for ln in g}
        body = [ln for ln in rlines if id(ln) not in cap_ids]
        if not body:
            return None
        box = body[0].bbox
        for ln in body[1:]:
            box = box.union(ln.bbox)
        is_table = (not groups) or any(TABLE_LABEL_RE.match(g[0].text) for g in groups)
        kind = "table" if is_table else "figure"
        items: list = []
        paras = []
        for g in groups:
            para = RawPara(g, pd.idx, "caption", layout.col_of(g[0]))
            paras.append((g[0].y0, para))
        above = [p for y, p in paras if y < box.y0]
        below = [p for y, p in paras if y >= box.y0]
        region = Region(kind, box.expanded(3))
        region.visual = self._render(rpd, region.bbox, kind)
        items = above + [RawVisual(region, pd.idx)] + below
        for ln in body:
            self.doc.drop("sideways table text", ln.text, pd.idx + 1)
        page_rect = Rect(*rorient.to_page(box))
        return RotatedGroup(pd.orient.to_upright(page_rect.tuple()), items)

    def _para_break(self, prev: Line, ln: Line, side: str, x0s, x1s, ln_cap: bool, prev_cap: bool, _l, cap_ids) -> bool:
        if ln_cap != prev_cap:
            return True
        if ln_cap and is_caption_start(ln, self.body):
            return True
        gap = ln.y0 - prev.y1
        if gap > 0.5 * max(ln.size, prev.size):
            return True
        if ln.y0 < prev.y0 - 2 * prev.size:  # jumped up: different column
            return True
        if abs(ln.size - prev.size) > 0.7:
            return True
        if ln.bold != prev.bold:
            return True
        if BULLET_RE.match(ln.text) and not ln_cap:
            return True
        x0, x1 = x0s[side], x1s[side]
        width = max(x1 - x0, 1)
        if ln.x0 - x0 > 0.9 * ln.size and prev.x1 > x1 - 0.1 * width and not ln_cap and abs(prev.x0 - x0) < 0.5 * ln.size:
            return True
        if prev.x1 < x1 - max(1.2 * ln.size, 0.05 * width) and ln.text[:1].isupper() and not ln_cap \
                and prev.text.rstrip().endswith(SENTENCE_END):
            return True
        return False

    # -------------------------------------------------------------- finish
    def _finish(self, raw: list[RawPara | RawVisual]) -> None:
        doc = self.doc
        body = self.body
        # --- title
        first_page = [it for it in raw if isinstance(it, RawPara) and it.page == (self.pages[0].idx if self.pages else 0)]
        title_para = None
        cands = [p for p in first_page if p.role == "body" and p.size >= body * 1.25]
        if cands:
            top = max(p.size for p in cands)
            group = [p for p in cands if abs(p.size - top) < 0.6]
            title_para = max(group, key=lambda p: len(p.text))
            # a title can be split into several paragraphs of identical size
            siblings = [p for p in group if p is not title_para and abs(p.lines[0].y0 - title_para.lines[-1].y1) < 2 * top]
            tp = [title_para] + siblings
            doc.title = normalize(" ".join(p.text for p in sorted(tp, key=lambda p: p.lines[0].y0)))
            for p in tp:
                p.role = "title"
        meta_title = doc.metadata.get("pdf_title", "")
        if meta_title:
            # the embedded metadata is usually free of text-layer glitches; use it when it is the same title
            a, b = re.sub(r"\W+", "", doc.title.lower()), re.sub(r"\W+", "", meta_title.lower())
            if not doc.title or SequenceMatcher(None, a, b).ratio() >= 0.85:
                doc.title = meta_title
        if self.pages:
            h = self.pages[0].rect.h
            for it in first_page:
                if it.role == "body" and all(ln.y0 > 0.85 * h and ln.size < body - 0.8 for ln in it.lines):
                    it.role = "dropme:page-1 footnote"

        # --- web-UI / legal boiler-plate lines that survive layout analysis
        for it in raw:
            if isinstance(it, RawPara) and it.role == "body":
                hit = match_noise(it.text)
                if hit:
                    it.role = f"dropme:noise: {hit}"

        # --- classify paragraphs: headings / captions
        for it in raw:
            if isinstance(it, RawPara) and it.role == "body" and self._is_heading(it):
                it.role = "heading"

        blocks: list = []
        for it in raw:
            if isinstance(it, RawVisual):
                blocks.append(it)
            elif it.role == "title":
                continue
            elif it.role.startswith("dropme"):
                doc.drop(it.role.split(":", 1)[1], it.text, it.page + 1)
            elif it.role == "heading":
                txt = clean_heading(it.text)
                blocks.append(["heading", txt, 0, it.page, (round(it.size * 2) / 2, it.text.isupper())])
            else:
                blocks.append(it)

        blocks = self._merge_dangling(blocks)
        blocks = self._relocate_captions(blocks)
        # --- abstract label inside a paragraph ("ABSTRACT: text ...")
        expanded: list = []
        for b in blocks:
            if isinstance(b, RawPara) and b.role == "body":
                m = ABSTRACT_RE.match(b.text)
                if m and (b.lines[0].bold or b.lines[0].first_span_bold or b.text[:8].isupper()) and len(b.text) - m.end() > 40:
                    expanded.append(["heading", "Abstract", 2, b.page, None])
                    b.lines[0].text = b.lines[0].text[m.end():] if m.end() <= len(b.lines[0].text) else b.lines[0].text
                    expanded.append(b)
                    continue
            expanded.append(b)
        blocks = expanded

        # --- front matter (everything before the abstract on page 1)
        abs_idx = next((i for i, b in enumerate(blocks) if isinstance(b, list) and re.match(r"^(abstract|summary)\b", b[1], re.I)), None)
        if abs_idx is None:
            abs_idx = next((i for i, b in enumerate(blocks) if isinstance(b, RawPara) and ABSTRACT_RE.match(b.text) and len(b.text) > 120), None)
        first_idx = self.pages[0].idx if self.pages else 0
        keep: list = []
        for i, b in enumerate(blocks):
            page_of = b[3] if isinstance(b, list) else b.page
            if abs_idx is not None and i < abs_idx and page_of == first_idx:
                if isinstance(b, RawVisual):
                    doc.drop("front matter", f"[{b.region.kind} image]", page_of + 1)
                    continue
                txt = b[1] if isinstance(b, list) else b.text
                names = self._parse_authors(txt)
                if len(names) > len(doc.authors):
                    doc.authors = names
                doc.drop("front matter", txt, page_of + 1)
                continue
            keep.append(b)
        blocks = keep
        if not doc.authors and doc.metadata.get("pdf_author"):
            doc.authors = [a.strip() for a in re.split(r"[;,]", doc.metadata["pdf_author"]) if a.strip()]

        # --- heading levels: numbering first, otherwise rank of the visual style
        styles = Counter(b[4] for b in blocks if isinstance(b, list) and b[4] is not None
                         and not re.match(r"^\d+(?:\.\d+)*[.)]?\s", b[1]))
        rank = {k: i for i, k in enumerate(sorted(styles, key=lambda k: (-k[0], not k[1])))}
        for b in blocks:
            if isinstance(b, list):
                m = re.match(r"^(\d+(?:\.\d+)*)[.)]?\s", b[1])
                if m:
                    b[2] = min(5, 2 + m.group(1).count("."))
                elif b[4] is not None:
                    b[2] = min(5, 2 + rank.get(b[4], 0))

        # --- emit
        vocab_blocks: list = []
        for b in blocks:
            if isinstance(b, RawVisual):
                vis = b.region.visual
                if vis is not None:
                    vocab_blocks.append(vis)
                else:
                    doc.warnings.append(f"Page {b.page + 1}: a {b.region.kind} could not be rendered.")
            elif isinstance(b, list):
                vocab_blocks.append(Heading(b[1], b[2]))
            else:
                text = b.text
                if text.strip():
                    vocab_blocks.append(Paragraph(text, role="caption" if b.role == "caption" else "body"))
        doc.blocks = vocab_blocks

    _LABEL = re.compile(r"^\s*(fig(?:ure)?|scheme|chart)\.?\s*S?(\d+)", re.I)
    _PLACEHOLDER = re.compile(r"legend (continued )?on (the )?next page|continued on next page", re.I)

    def _relocate_captions(self, blocks: list) -> list:
        """Some journals print 'Legend on next page' under a full-page figure; move the real legend next to it."""
        pending: dict[str, RawVisual] = {}
        out: list = []
        for b in blocks:
            if isinstance(b, RawPara) and b.role == "caption":
                m = self._LABEL.match(b.text)
                key = f"{m.group(1)[:3].lower()}{m.group(2)}" if m else ""
                if self._PLACEHOLDER.search(b.text) and len(b.text) < 80:
                    prev = next((x for x in reversed(out) if isinstance(x, RawVisual)), None)
                    if prev is not None and key:
                        pending[key] = prev
                    self.doc.drop("caption placeholder", b.text, b.page + 1)
                    continue
                if key in pending:
                    vis = pending.pop(key)
                    out.insert(out.index(vis) + 1, b)
                    continue
            out.append(b)
        return out

    @staticmethod
    def _parse_authors(text: str) -> list[str]:
        if len(text) > 900 or AFFIL_WORDS.search(text):
            return []
        parts = [re.sub(r"[\d*†‡§⊥#,]+$|^[\d*]+", "", p).strip(" *†‡")
                 for p in re.split(r"\s*(?:\||;|,|\band\b|&)\s*", re.sub(r"\d+(?:,\d+)*", "", text))]
        names = [p for p in parts if 2 <= len(p.split()) <= 4 and all(w[:1].isupper() for w in p.split() if w[:1].isalpha())]
        return names if len(names) >= 2 else []

    def _is_heading(self, p: RawPara) -> bool:
        if len(p.lines) > (4 if p.bold else 2):
            return False
        txt = p.text.strip()
        if not txt or len(txt) > 180 or CAPTION_RE.match(txt) and re.search(r"\d", txt[:12]):
            return False
        if txt.endswith((",", ":", ";")) or (txt.endswith(".") and len(txt.split()) > 10):
            return False
        if re.fullmatch(r"[\d\s.,()-]+", txt):
            return False
        letters = sum(c.isalpha() for c in txt)
        if letters < 3:
            return False
        if p.bold and len(txt.split()) <= 25:
            return True
        if p.size >= self.body + 1.5 and not txt.endswith("."):
            return True
        return False

    def _merge_dangling(self, blocks: list) -> list:
        """Join paragraphs interrupted by a column / page break or by an inline figure."""
        out: list = []
        i = 0
        while i < len(blocks):
            b = blocks[i]
            if isinstance(b, RawPara) and b.role == "caption" and i + 1 < len(blocks):
                nxt = blocks[i + 1]
                if isinstance(nxt, RawPara) and nxt.role == "body" and nxt.size < self.body - 0.5 \
                        and abs(nxt.size - b.size) < 0.4 and not self._is_heading(nxt):
                    b = RawPara(b.lines + nxt.lines, b.page, "caption", b.col)
                    blocks[i + 1] = b
                    i += 1
                    continue
            if isinstance(b, RawPara) and b.role == "body":
                j = i + 1
                skipped: list = []
                while True:
                    t = b.text.rstrip()
                    if j >= len(blocks):
                        break
                    nxt = blocks[j]
                    if isinstance(nxt, RawVisual) or (isinstance(nxt, RawPara) and nxt.role == "caption"):
                        skipped.append(nxt)
                        j += 1
                        continue
                    if isinstance(nxt, RawPara) and nxt.role == "body" and b.role == "caption":
                        break
                    if isinstance(nxt, RawPara) and nxt.role == "body":
                        starts_lower = nxt.text[:1].islower()
                        open_end = not t.endswith(SENTENCE_END) or t.endswith("­")
                        same_flow = nxt.size - b.size < 0.7 and abs(nxt.size - b.size) < 0.7
                        if same_flow and (starts_lower or (open_end and nxt.text[:1].isalnum() and not BULLET_RE.match(nxt.text)
                                                          and (nxt.page != b.page or nxt.col != b.col))):
                            b = RawPara(b.lines + nxt.lines, b.page, "body", b.col)
                            j += 1
                            continue
                    break
                # figures / captions that sat inside the paragraph go after it
                if j > i + 1 and b is not blocks[i]:
                    out.append(b)
                    out.extend(skipped)
                    i = j
                    continue
                out.append(blocks[i])
                i += 1
                continue
            out.append(b)
            i += 1
        return out


def read_pdf(data: bytes, options: Options) -> Document:
    return PdfReader(data, options).read()
