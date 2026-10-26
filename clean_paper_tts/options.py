"""User-facing conversion options."""

from __future__ import annotations

from dataclasses import dataclass, field

# Section titles removed by default. Matched case-insensitively against the
# heading text with any leading numbering stripped.
DEFAULT_DROP_SECTIONS: tuple[str, ...] = (
    r"references?( and notes)?",
    r"bibliography",
    r"literature cited",
    r"works cited",
    r"acknowledge?ments?",
    r"author contributions?",
    r"authors?['’]? contributions?",
    r"credit authorship contribution statement",
    r"(declaration of )?(competing|conflicts? of|conflicting) interests?( statement)?",
    r"declaration of interests?",
    r"funding( information| sources?| statement)?",
    r"financial support",
    r"ethics( statement| approval.*)?",
    r"data (and code )?availability( statement)?",
    r"code availability",
    r"availability of data and materials?",
    r"supporting information( available)?",
    r"supplementary (information|material|materials|data)",
    r"associated content",
    r"author information",
    r"abbreviations?( used)?",
    r"publisher['’]?s? note",
    r"open access",
    r"citing literature",
    r"related (articles|content|information)",
    r"notes",
    r"additional information",
    r"peer review( information)?",
    r"reporting summary",
    r"rights and permissions",
    r"about this article",
    r"consent for publication",
    r"disclosures?",
)

METHODS_SECTIONS: tuple[str, ...] = (
    r"(materials? and )?methods?( and materials?)?",
    r"experimental( section| procedures?| methods?)?",
    r"online methods",
    r"star ?★? ?methods",
    r"supporting methods",
)


@dataclass
class Options:
    # content selection
    include_authors: bool = False
    include_captions: bool = True
    include_figures: bool = True
    drop_sections: tuple[str, ...] = DEFAULT_DROP_SECTIONS
    drop_methods: bool = False
    # text clean-up
    strip_citations: bool = True
    strip_author_year_citations: bool = True
    strip_characterization_data: bool = True
    # rendering
    render_dpi: int = 170
    max_image_width: int = 1600
    formulas_as_images: bool = True
    fetch_remote_images: bool = True
    # extra regexes (one per line in the UI) to remove whole paragraphs
    extra_noise_patterns: list[str] = field(default_factory=list)

    def section_patterns(self) -> tuple[str, ...]:
        return self.drop_sections + (METHODS_SECTIONS if self.drop_methods else ())
