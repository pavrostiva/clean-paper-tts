"""Image helpers: format normalisation, down-scaling, SVG rasterisation."""

from __future__ import annotations

import io

from PIL import Image

from ..model import Visual

Image.MAX_IMAGE_PIXELS = 200_000_000


def _rasterize_svg(data: bytes, dpi: int) -> bytes | None:
    try:
        import pymupdf

        doc = pymupdf.open(stream=data, filetype="svg")
        pix = doc[0].get_pixmap(dpi=dpi, alpha=False)
        return pix.tobytes("png")
    except Exception:
        return None


def to_visual(data: bytes, kind: str, label: str = "", max_width: int = 1600,
              dpi: int = 170, mime_hint: str = "") -> Visual | None:
    """Decode any browser image (png/jpg/webp/gif/svg) and re-encode compactly."""
    if "svg" in mime_hint or data.lstrip()[:5] in (b"<?xml", b"<svg ") or b"<svg" in data[:400]:
        data = _rasterize_svg(data, dpi) or b""
        if not data:
            return None
    try:
        im = Image.open(io.BytesIO(data))
        im.load()
    except Exception:
        return None
    if im.width < 2 or im.height < 2:
        return None
    if im.width > max_width:
        im = im.resize((max_width, max(1, round(im.height * max_width / im.width))), Image.LANCZOS)
    has_alpha = im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info)
    if has_alpha:
        im = im.convert("RGBA")
        bg = Image.new("RGB", im.size, "white")
        bg.paste(im, mask=im.split()[-1])
        im = bg
    else:
        im = im.convert("RGB")
    buf = io.BytesIO()
    im.save(buf, "PNG", optimize=True)
    mime = "image/png"
    # photographs / dense micrographs compress far better as JPEG
    if kind == "figure" and buf.tell() > 500_000:
        jbuf = io.BytesIO()
        im.save(jbuf, "JPEG", quality=85, optimize=True)
        if jbuf.tell() < buf.tell():
            buf, mime = jbuf, "image/jpeg"
    return Visual(kind=kind, data=buf.getvalue(), mime=mime, label=label, width=im.width, height=im.height)
