"""Public entry point: bytes in, TTS-friendly HTML out."""

from __future__ import annotations

from dataclasses import dataclass

from .filters import apply_filters
from .model import Document
from .options import Options
from .readers.mhtml import looks_like_mhtml, unpack_mhtml
from .readers.resources import Resources
from .render.html_writer import write_html


@dataclass
class ConversionResult:
    html: str
    document: Document

    @property
    def title(self) -> str:
        return self.document.title


def detect_type(data: bytes, filename: str = "") -> str:
    name = filename.lower()
    if data[:5] == b"%PDF-" or name.endswith(".pdf"):
        return "pdf"
    if name.endswith((".mhtml", ".mht")) or looks_like_mhtml(data):
        return "mhtml"
    return "html"


def convert(data: bytes, filename: str = "", options: Options | None = None) -> ConversionResult:
    options = options or Options()
    kind = detect_type(data, filename)
    if kind == "pdf":
        from .readers.pdf import read_pdf

        doc = read_pdf(data, options)
    elif kind == "mhtml":
        from .readers.html import read_html

        html, base, resources = unpack_mhtml(data)
        resources.fetch_remote = options.fetch_remote_images
        doc = read_html(html, resources, options)
        doc.source_type = "mhtml"
    else:
        from .readers.html import read_html

        text = _decode(data)
        doc = read_html(text, Resources(fetch_remote=options.fetch_remote_images), options)
    apply_filters(doc, options)
    if not doc.title:
        doc.title = (filename.rsplit(".", 1)[0] if filename else "Untitled paper")
    if not any(True for _ in doc.blocks):
        doc.warnings.append("No readable content was extracted.")
    return ConversionResult(write_html(doc, options), doc)


def _decode(data: bytes) -> str:
    for enc in ("utf-8", "utf-16"):
        try:
            return data.decode(enc)
        except UnicodeDecodeError:
            continue
    return data.decode("latin-1", errors="replace")
