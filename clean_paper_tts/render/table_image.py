"""Draw an HTML <table> as a clean PNG without needing a browser."""

from __future__ import annotations

import io
from dataclasses import dataclass

from bs4 import Tag
from PIL import Image, ImageDraw

from .fonts import get_font

_SUP = str.maketrans("0123456789+-=()niabcdefghjklmoprstuvwxyz",
                     "\u2070\u00b9\u00b2\u00b3\u2074\u2075\u2076\u2077\u2078\u2079\u207a\u207b\u207c\u207d\u207e\u207f\u2071\u1d43\u1d47\u1d9c\u1d48\u1d49\u1da0\u1d4d\u02b0\u02b2\u1d4f\u02e1\u1d50\u1d52\u1d56\u02b3\u02e2\u1d57\u1d58\u1d5b\u02b7\u02e3\u02b8\u1dbb")
_SUB = str.maketrans("0123456789+-=()", "\u2080\u2081\u2082\u2083\u2084\u2085\u2086\u2087\u2088\u2089\u208a\u208b\u208c\u208d\u208e")


@dataclass
class _Cell:
    text: str
    row: int
    col: int
    rowspan: int = 1
    colspan: int = 1
    header: bool = False
    align: str = "left"
    lines: list[str] | None = None


def cell_text(node) -> str:
    """Text of a cell with <sup>/<sub> mapped to unicode where possible."""
    parts: list[str] = []

    def walk(n, mode=""):
        if isinstance(n, Tag):
            if n.name in ("script", "style"):
                return
            if n.name == "br":
                parts.append("\n")
                return
            m = "sup" if n.name == "sup" else "sub" if n.name == "sub" else mode
            for c in n.children:
                walk(c, m)
        else:
            s = str(n)
            if mode == "sup":
                s = s.translate(_SUP)
            elif mode == "sub":
                s = s.translate(_SUB)
            parts.append(s)

    walk(node)
    txt = "".join(parts).replace("\xa0", " ")
    return "\n".join(" ".join(line.split()) for line in txt.split("\n")).strip()


def _align(el: Tag) -> str:
    style = (el.get("style") or "").replace(" ", "").lower()
    cls = " ".join(el.get("class", [])).lower()
    a = (el.get("align") or "").lower()
    for key in ("center", "right", "left"):
        if key in a or f"text-align:{key}" in style or f"{key}-aligned" in cls or f"text-{key}" in cls:
            return key
    return "left"


def parse_table(table: Tag) -> tuple[list[_Cell], int, int]:
    cells: list[_Cell] = []
    occupied: dict[tuple[int, int], bool] = {}
    rows = [tr for tr in table.find_all("tr") if tr.find_parent("table") is table]
    ncols = 0
    for r, tr in enumerate(rows):
        c = 0
        for td in tr.find_all(["td", "th"], recursive=False):
            while occupied.get((r, c)):
                c += 1
            rs = max(1, min(int(td.get("rowspan", 1) or 1) if str(td.get("rowspan", 1)).isdigit() else 1, 50))
            cs = max(1, min(int(td.get("colspan", 1) or 1) if str(td.get("colspan", 1)).isdigit() else 1, 50))
            cell = _Cell(cell_text(td), r, c, rs, cs, td.name == "th" or tr.find_parent("thead") is not None,
                         _align(td))
            cells.append(cell)
            for dr in range(rs):
                for dc in range(cs):
                    occupied[(r + dr, c + dc)] = True
            c += cs
            ncols = max(ncols, c)
    return cells, len(rows), ncols


def _wrap(text: str, font, max_w: int, draw) -> list[str]:
    out: list[str] = []
    for para in text.split("\n"):
        words, cur = para.split(" "), ""
        for w in words:
            trial = (cur + " " + w).strip()
            if draw.textlength(trial, font=font) <= max_w or not cur:
                cur = trial
            else:
                out.append(cur)
                cur = w
        out.append(cur)
    return out or [""]


def render_table(table: Tag, scale: float = 1.6, max_col: int = 340) -> bytes | None:
    cells, nrows, ncols = parse_table(table)
    if not cells or ncols == 0:
        return None
    base = max(10, round(11 * scale))
    font, bold = get_font(base), get_font(base, bold=True)
    pad_x, pad_y = round(7 * scale), round(4 * scale)
    probe = ImageDraw.Draw(Image.new("RGB", (4, 4)))
    col_w = [round(30 * scale)] * ncols

    # single-column cells fix the column widths; spanning cells only widen if needed
    for cell in (c for c in cells if c.colspan == 1):
        f = bold if cell.header else font
        w = max((probe.textlength(line, font=f) for line in cell.text.split("\n")), default=0)
        col_w[cell.col] = max(col_w[cell.col], min(round(w) + 2 * pad_x, round(max_col * scale)))
    for cell in (c for c in cells if c.colspan > 1):
        f = bold if cell.header else font
        w = max((probe.textlength(line, font=f) for line in cell.text.split("\n")), default=0) + 2 * pad_x
        have = sum(col_w[cell.col: cell.col + cell.colspan])
        if w > have:
            extra = round((w - have) / cell.colspan) + 1
            for k in range(cell.col, min(ncols, cell.col + cell.colspan)):
                col_w[k] += extra

    row_h = [round(font.size * 1.3) + 2 * pad_y] * nrows
    line_h = round(font.size * 1.3)
    for cell in cells:
        span_w = sum(col_w[cell.col: cell.col + cell.colspan]) - 2 * pad_x
        cell.lines = _wrap(cell.text, bold if cell.header else font, max(span_w, 10), probe)
        need = len(cell.lines) * line_h + 2 * pad_y
        have = sum(row_h[cell.row: cell.row + cell.rowspan])
        if need > have:
            row_h[cell.row + cell.rowspan - 1] += need - have

    margin = round(8 * scale)
    width, height = sum(col_w) + 2 * margin, sum(row_h) + 2 * margin
    if width * height > 60_000_000:
        return None
    img = Image.new("RGB", (width, height), "white")
    d = ImageDraw.Draw(img)
    xs = [margin]
    for w in col_w:
        xs.append(xs[-1] + w)
    ys = [margin]
    for h in row_h:
        ys.append(ys[-1] + h)

    header_rows = {c.row for c in cells if c.header}
    last_header = max(header_rows) if header_rows else -1
    for cell in cells:
        x0, x1 = xs[cell.col], xs[min(ncols, cell.col + cell.colspan)]
        y0, y1 = ys[cell.row], ys[min(nrows, cell.row + cell.rowspan)]
        if cell.header:
            d.rectangle([x0, y0, x1, y1], fill=(240, 243, 247))
        f = bold if cell.header else font
        ty = y0 + pad_y
        for line in cell.lines or []:
            tw = d.textlength(line, font=f)
            align = "center" if cell.header and cell.colspan > 1 else cell.align
            tx = x0 + pad_x if align == "left" else x1 - pad_x - tw if align == "right" else x0 + (x1 - x0 - tw) / 2
            d.text((tx, ty), line, font=f, fill=(20, 20, 20))
            ty += line_h
        d.line([x0, y1, x1, y1], fill=(210, 214, 220), width=1)
    d.line([margin, margin, width - margin, margin], fill=(30, 30, 30), width=2)
    if last_header >= 0:
        d.line([margin, ys[last_header + 1], width - margin, ys[last_header + 1]], fill=(30, 30, 30), width=2)
    d.line([margin, height - margin, width - margin, height - margin], fill=(30, 30, 30), width=2)
    buf = io.BytesIO()
    img.save(buf, "PNG", optimize=True)
    return buf.getvalue()
