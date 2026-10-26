from clean_paper_tts import Options
from clean_paper_tts.filters import apply_filters
from clean_paper_tts.model import Document, Heading, Paragraph


def doc_with(*blocks):
    d = Document(title="t")
    d.blocks = list(blocks)
    return d


def texts(d):
    return [b.text for b in d.blocks if hasattr(b, "text")]


def test_reference_and_acknowledgement_sections_dropped():
    d = doc_with(Heading("1 Introduction", 2), Paragraph("Body text."), Heading("Acknowledgments", 2),
                 Paragraph("Thanks to everyone."), Heading("References", 2), Paragraph("1. A. Author."))
    apply_filters(d, Options())
    assert texts(d) == ["1 Introduction", "Body text."]
    assert any("References" in x.reason for x in d.dropped)


def test_subsection_of_dropped_section_is_dropped_too():
    d = doc_with(Heading("Author Information", 2), Heading("Corresponding Author", 3), Paragraph("Name"),
                 Heading("Next", 2), Paragraph("kept"))
    apply_filters(d, Options())
    assert texts(d) == ["Next", "kept"]


def test_methods_dropped_only_on_request():
    blocks = [Heading("Results", 2), Paragraph("r"), Heading("Materials and Methods", 2), Paragraph("m")]
    d1 = doc_with(*blocks)
    apply_filters(d1, Options())
    assert "m" in texts(d1)
    d2 = doc_with(*[Heading(b.text, b.level) if isinstance(b, Heading) else Paragraph(b.text) for b in blocks])
    apply_filters(d2, Options(drop_methods=True))
    assert "m" not in texts(d2)


def test_noise_lines_dropped_but_prose_kept():
    d = doc_with(Paragraph("Downloaded from https://x.org by guest"), Paragraph("© 2025 The Authors."),
                 Paragraph("Keywords: a; b; c"), Paragraph("The Creative Commons Attribution of tumors was studied in depth."
                                                         " " * 1 + "x" * 450))
    apply_filters(d, Options())
    assert len(texts(d)) == 1


def test_characterization_data_removed():
    d = doc_with(Paragraph("The mixture was stirred for 2 h to give 5 as a white solid. 1H NMR (400 MHz, DMSO-d6) "
                           "\u03b4 8.45 (s, 1H), 7.2 (d, J = 8 Hz, 2H). HRMS (ESI) m/z calcd for C9H9 found 120.1."))
    apply_filters(d, Options())
    assert texts(d) == ["The mixture was stirred for 2 h to give 5 as a white solid."]
    d2 = doc_with(Paragraph("The mixture was stirred. 1H NMR (400 MHz, DMSO-d6) \u03b4 8.45 (s, 1H), 7.2 (d, J = 8 Hz, 2H)."))
    apply_filters(d2, Options(strip_characterization_data=False))
    assert "NMR" in texts(d2)[0]


def test_custom_noise_pattern():
    d = doc_with(Paragraph("Share this article on social media"), Paragraph("Real text here."))
    apply_filters(d, Options(extra_noise_patterns=[r"share this article"]))
    assert texts(d) == ["Real text here."]
