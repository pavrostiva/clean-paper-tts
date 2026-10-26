"""Intermediate document model shared by all readers and the HTML writer."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Heading:
    text: str
    level: int = 2  # 1 = document title, 2 = top-level section, 3 = subsection, ...


@dataclass
class Paragraph:
    text: str
    role: str = "body"  # "body" | "caption" | "abstract"


@dataclass
class ListBlock:
    items: list[str]
    ordered: bool = False


@dataclass
class Visual:
    """A rasterised element that a TTS engine should not try to read."""

    kind: str  # "figure" | "table" | "formula"
    data: bytes
    mime: str = "image/png"
    label: str = ""
    width: int = 0
    height: int = 0


Block = Heading | Paragraph | ListBlock | Visual


@dataclass
class Dropped:
    """Something removed from the output, kept so the user can audit the filters."""

    reason: str
    text: str
    page: int | None = None


@dataclass
class Document:
    title: str = ""
    authors: list[str] = field(default_factory=list)
    metadata: dict[str, str] = field(default_factory=dict)
    blocks: list[Block] = field(default_factory=list)
    dropped: list[Dropped] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    citations_removed: list[str] = field(default_factory=list)  # marker texts, for the audit tab
    source_type: str = ""

    def drop(self, reason: str, text: str, page: int | None = None) -> None:
        text = text.strip()
        if text:
            self.dropped.append(Dropped(reason, text, page))

    def stats(self) -> dict[str, int]:
        out = {"headings": 0, "paragraphs": 0, "captions": 0, "lists": 0,
               "figures": 0, "tables": 0, "formulas": 0, "words": 0}
        for b in self.blocks:
            if isinstance(b, Heading):
                out["headings"] += 1
                out["words"] += len(b.text.split())
            elif isinstance(b, Paragraph):
                out["captions" if b.role == "caption" else "paragraphs"] += 1
                out["words"] += len(b.text.split())
            elif isinstance(b, ListBlock):
                out["lists"] += 1
                out["words"] += sum(len(i.split()) for i in b.items)
            elif isinstance(b, Visual):
                out[b.kind + "s"] += 1
        return out
