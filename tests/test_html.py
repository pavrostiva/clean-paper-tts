import base64
import io

from PIL import Image

from clean_paper_tts import Options, convert
from clean_paper_tts.model import Heading, Paragraph, Visual

PARA = "Tumor cells release damage-associated molecular patterns and activate dendritic cells in vivo. " * 12


def page(body: str, extra_head: str = "") -> bytes:
    return f"""<html><head><title>Journal site - Paper</title>
    <meta name="citation_title" content="A Study of Things"><meta name="citation_author" content="Ann One">
    <meta name="citation_author" content="Bob Two"><meta name="citation_doi" content="10.1/abc">{extra_head}</head>
    <body><nav>Home | Journals | Login</nav><div class="cookie-banner">We use cookies</div>
    <article>{body}</article><footer>Terms of use</footer></body></html>""".encode()


def kinds(res):
    return [type(b).__name__ + (":" + b.kind if isinstance(b, Visual) else "") for b in res.document.blocks]


def test_metadata_and_boilerplate(png_data_uri):
    body = f"""<h1>A Study of Things</h1><h2>Introduction</h2><p>{PARA} <a href="#ref1" class="bibLink">[1]</a></p>
    <h2>References</h2><p>1. Somebody. Something. 2020.</p>"""
    res = convert(page(body), "p.html", Options())
    d = res.document
    assert d.title == "A Study of Things" and d.authors == ["Ann One", "Bob Two"]
    assert "cookies" not in res.html and "Terms of use" not in res.html and "Somebody" not in res.html
    assert "[1]" not in res.html
    assert kinds(res)[:2] == ["Heading", "Paragraph"]


def test_table_becomes_image_and_caption_stays_text():
    body = f"""<h2>Results</h2><p>{PARA}</p><div class="table-wrap"><div class="caption">Table 1. Hazard ratios</div>
    <table><thead><tr><th>Model</th><th colspan="2">HR</th></tr></thead>
    <tbody><tr><td>A</td><td>1.2</td><td>3.4</td></tr><tr><td>B</td><td>2.2</td><td>4.4</td></tr></tbody></table></div>"""
    res = convert(page(body), "p.html", Options())
    assert "Visual:table" in kinds(res)
    caps = [b for b in res.document.blocks if isinstance(b, Paragraph) and b.role == "caption"]
    assert caps and caps[0].text.startswith("Table 1")
    assert "<td>" not in res.html and "Hazard ratios" in res.html


def test_figure_embedded_and_caption(png_data_uri):
    body = f"""<h2>Results</h2><p>{PARA}</p><figure><img src="{png_data_uri}"><figcaption>Figure 1. A drawing.
    <a class="open-figure-link">Open in figure viewer</a></figcaption></figure>"""
    res = convert(page(body), "p.html", Options(fetch_remote_images=False))
    assert "Visual:figure" in kinds(res)
    assert "Open in figure viewer" not in res.html
    assert 'alt=""' in res.html  # images are silent for TTS
    res2 = convert(page(body), "p.html", Options(include_figures=False, fetch_remote_images=False))
    assert "<figure" not in res2.html


def test_display_equation_rendered_inline_math_kept_as_text():
    math_inline = '<math display="inline"><mi>x</mi><annotation encoding="application/x-tex">$x$</annotation></math>'
    math_block = ('<div class="disp-formula"><math display="block"><mi>y</mi><mo>=</mo><mi>a</mi>'
                  '<annotation encoding="application/x-tex">$y = a^2 + \\frac{1}{2}$</annotation></math></div>')
    body = f"<h2>Methods</h2><p>Let {math_inline} be a value. {PARA}</p>{math_block}<p>{PARA}</p>"
    res = convert(page(body), "p.html", Options())
    assert "Visual:formula" in kinds(res)
    assert "Let x be a value" in res.html


def test_mhtml_embedded_image():
    buf = io.BytesIO()
    Image.new("RGB", (300, 200), (200, 50, 50)).save(buf, "PNG")
    img_b64 = base64.encodebytes(buf.getvalue()).decode()
    html = page(f"<h2>Results</h2><p>{PARA}</p><figure><img src=\"/img/f1.png\"><figcaption>Figure 1. X.</figcaption></figure>").decode()
    mhtml = f"""From: <Saved by Blink>
MIME-Version: 1.0
Content-Type: multipart/related; type="text/html"; boundary="B"

--B
Content-Type: text/html; charset=utf-8
Content-Transfer-Encoding: 8bit
Content-Location: https://example.org/article/1

{html}
--B
Content-Type: image/png
Content-Transfer-Encoding: base64
Content-Location: https://example.org/img/f1.png

{img_b64}
--B--
""".encode()
    res = convert(mhtml, "paper.mhtml", Options(fetch_remote_images=False))
    assert res.document.source_type == "mhtml"
    assert "Visual:figure" in kinds(res)


def test_garbage_does_not_crash():
    res = convert(b"<html><body>hi</body></html>", "x.html", Options())
    assert res.document.warnings
