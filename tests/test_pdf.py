import pymupdf
import pytest

from clean_paper_tts import Options, convert
from clean_paper_tts.model import Heading, Paragraph, Visual

LEFT = ("Immunogenic cell death is a regulated form of cell death that activates adaptive immunity. "
        "Dying tumour cells release damage-associated molecular patterns, which recruit dendritic cells "
        "and promote cross-priming of cytotoxic T lymphocytes against tumour antigens in the micro- "
        "environment of solid cancers. ") * 3
RIGHT = ("We trained gradient boosting classifiers on the training cohort and evaluated them on the held-out "
         "validation cohort using the concordance index as the primary accuracy metric across all cancers. ") * 3


def make_pdf() -> bytes:
    doc = pymupdf.open()
    for n in range(3):
        page = doc.new_page(width=595, height=782)
        page.insert_text((45, 30), "Journal of Testing Science 2025", fontsize=8)
        page.insert_text((270, 760), f"{n + 1} of 3", fontsize=8)
        page.insert_text((578, 700), "Downloaded from https://example.org/doi/10.1000/xyz", fontsize=6, rotate=90)
        top = 70
        if n == 0:
            page.insert_text((45, 60), "A Synthetic Paper About Cell Death", fontsize=18)
            page.insert_text((45, 82), "Ann One | Bob Two | Cara Three", fontsize=10)
            page.insert_text((45, 100), "Department of Tests, University of Examples, Testland", fontsize=8)
            page.insert_text((45, 125), "ABSTRACT", fontsize=10, fontname="hebo")
            page.insert_textbox(pymupdf.Rect(45, 130, 550, 200), "We study cell death in tumours. " * 8, fontsize=9)
            top = 215
        page.insert_textbox(pymupdf.Rect(45, top, 285, top + 220), LEFT, fontsize=9)
        page.insert_textbox(pymupdf.Rect(306, top, 550, top + 220), RIGHT, fontsize=9)
        if n == 1:
            y = top + 240
            page.insert_text((45, y), "Table 1. Hazard ratios of the models.", fontsize=8)
            rows = [["Model", "Train", "Test"], ["Base", "3.45", "1.35"], ["XGB", "3.62", "1.36"], ["LGBM", "3.38", "1.43"]]
            for r, row in enumerate(rows):
                for c, cell in enumerate(row):
                    page.insert_text((60 + c * 90, y + 22 + r * 12), cell, fontsize=7.5)
            for yy in (y + 12, y + 26, y + 22 + len(rows) * 12):
                page.draw_line((45, yy), (330, yy), width=0.6)
            fy = y + 22 + len(rows) * 12 + 40
            page.draw_rect(pymupdf.Rect(60, fy, 280, fy + 120), color=(0, 0, 1), fill=(0.8, 0.9, 1))
            for k in range(14):
                page.draw_line((60 + k * 15, fy), (60 + k * 15, fy + 120), color=(1, 0, 0), width=0.5)
                page.draw_circle((70 + k * 14, fy + 20 + (k * 7) % 80), 4, color=(0, 0.5, 0), fill=(0, 0.5, 0))
            page.insert_text((140, fy + 135), "AXISLABEL", fontsize=7)
            page.insert_text((45, fy + 155), "Figure 1. Scatter plot of the synthetic data.", fontsize=8)
    return doc.tobytes()


@pytest.fixture(scope="module")
def result():
    return convert(make_pdf(), "synthetic.pdf", Options())


def body_text(result) -> str:
    return " ".join(b.text for b in result.document.blocks if isinstance(b, (Paragraph, Heading)))


def test_title_authors_and_abstract(result):
    d = result.document
    assert d.title == "A Synthetic Paper About Cell Death"
    assert d.authors == ["Ann One", "Bob Two", "Cara Three"]
    heads = [b.text for b in d.blocks if isinstance(b, Heading)]
    assert heads and heads[0].lower() == "abstract"
    assert "Department of Tests" not in body_text(result)


def test_running_headers_footers_and_watermark_removed(result):
    txt = body_text(result)
    assert "Journal of Testing Science" not in txt
    assert "of 3" not in txt
    assert "Downloaded from" not in txt


def test_two_column_reading_order(result):
    txt = body_text(result)
    assert txt.index("Immunogenic cell death") < txt.index("We trained gradient boosting")


def test_line_break_hyphen_rejoined(result):
    assert "microenvironment" in body_text(result)


def test_table_and_figure_become_images(result):
    vis = [b for b in result.document.blocks if isinstance(b, Visual)]
    assert sorted(v.kind for v in vis) == ["figure", "table"]
    txt = body_text(result)
    assert "Table 1. Hazard ratios" in txt and "Figure 1. Scatter plot" in txt
    assert "3.62" not in txt and "AXISLABEL" not in txt


def test_html_output_is_self_contained(result):
    assert result.html.count("<img ") == 2
    assert 'alt=""' in result.html and "http://" not in result.html.split("</style>")[1].replace("example.org", "")


def test_encrypted_or_empty_pdf_gives_clear_error():
    doc = pymupdf.open()
    doc.new_page()
    res = convert(doc.tobytes(), "blank.pdf", Options())
    assert any("scanned" in w or "No readable" in w for w in res.document.warnings)
