"""Serialise a Document to one self-contained, reader-app-friendly HTML file."""

from __future__ import annotations

import base64
from html import escape

from ..model import Document, Heading, ListBlock, Paragraph, Visual
from ..options import Options

CSS = """
:root{color-scheme:light dark}
body{font-family:Georgia,'Times New Roman',serif;line-height:1.6;max-width:42rem;margin:0 auto;padding:1rem;
 background:#fff;color:#1a1a1a;font-size:1.05rem}
h1{font-size:1.6rem;line-height:1.25}
h2{font-size:1.3rem;margin-top:2rem}
h3{font-size:1.15rem;margin-top:1.5rem}
h4,h5,h6{font-size:1.05rem;margin-top:1.2rem}
p.authors{color:#555;font-style:italic}
p.caption{font-size:.92rem;color:#444;margin:.3rem 0 1.4rem}
figure{margin:1.4rem 0}
figure img{max-width:100%;height:auto;display:block;margin:0 auto;background:#fff}
@media (prefers-color-scheme:dark){body{background:#121212;color:#e6e6e6}p.caption,p.authors{color:#aaa}}
"""


def _img(v: Visual) -> str:
    b64 = base64.b64encode(v.data).decode("ascii")
    size = f' width="{v.width}" height="{v.height}"' if v.width and v.height else ""
    # alt is intentionally empty so text-to-speech apps skip the image
    return f'<img src="data:{v.mime};base64,{b64}" alt=""{size}>'


def write_html(doc: Document, options: Options) -> str:
    out: list[str] = []
    title = doc.title or "Untitled paper"
    meta = [f'<meta charset="utf-8">',
            '<meta name="viewport" content="width=device-width, initial-scale=1">']
    if doc.authors:
        meta.append(f'<meta name="author" content="{escape(", ".join(doc.authors), quote=True)}">')
    for k in ("doi", "journal"):
        if doc.metadata.get(k):
            meta.append(f'<meta name="{k}" content="{escape(doc.metadata[k], quote=True)}">')
    out.append("<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n" + "\n".join(meta)
               + f"\n<title>{escape(title)}</title>\n<style>{CSS}</style>\n</head>\n<body>")
    out.append(f"<h1>{escape(title)}</h1>")
    if options.include_authors and doc.authors:
        out.append(f'<p class="authors">{escape(", ".join(doc.authors))}</p>')
    for b in doc.blocks:
        if isinstance(b, Heading):
            lvl = min(6, max(2, b.level))
            out.append(f"<h{lvl}>{escape(b.text)}</h{lvl}>")
        elif isinstance(b, Paragraph):
            if b.role == "caption":
                if options.include_captions:
                    out.append(f'<p class="caption">{escape(b.text)}</p>')
            else:
                out.append(f"<p>{escape(b.text)}</p>")
        elif isinstance(b, ListBlock):
            tag = "ol" if b.ordered else "ul"
            items = "".join(f"<li>{escape(i)}</li>" for i in b.items)
            out.append(f"<{tag}>{items}</{tag}>")
        elif isinstance(b, Visual):
            if b.kind == "figure" and not options.include_figures:
                continue
            out.append(f'<figure class="{b.kind}">{_img(b)}</figure>')
    out.append("</body>\n</html>\n")
    return "\n".join(out)
