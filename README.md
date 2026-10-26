# clean-paper-tts

Scientific papers are a pain to listen to. Text-to-speech apps read journal headers, page numbers,
"Downloaded from…" watermarks, reference lists, and then try to pronounce a results table cell by cell.

This tool takes a paper as **PDF, HTML or MHTML** and writes one clean HTML file you can open in a
TTS reader on your phone:

- body text stays real text, in the right reading order (two-column layouts included);
- **tables, figures and display equations become images** (the reader skips them), captions stay as text;
- running headers/footers, margin watermarks, front matter (affiliations, dates, licence blurbs),
  citation markers like `[12]` or `(Smith et al., 2020)`, reference lists, acknowledgements and similar
  sections are removed;
- hyphenated line breaks are repaired, ligatures normalised, sidebar junk in web pages ignored.

It was built with biology, bioinformatics and chemoinformatics papers in mind (ACS, Wiley, Nature,
Elsevier, MDPI, Frontiers, PLOS, PMC layouts), but the heuristics are generic.

## Use it

### Web app

Start it locally (below) or deploy your own copy for free on
[Streamlit Community Cloud](https://streamlit.io/cloud): *New app → this repository → main file `app.py`*.
Open the link, drop in one or more files, download the `.html`, load it into your reader app.
A "What was removed" tab shows everything that was filtered out, which is handy when you tune the options.

Files are processed in memory and never stored.

### Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

### Command line

```bash
python -m clean_paper_tts paper.pdf -o paper.html
python -m clean_paper_tts paper.mhtml --drop-methods --authors --report report.json
```

`--help` lists all switches (keep citations, drop figures, keep NMR listings, …).

### From Python

```python
from clean_paper_tts import convert, Options

result = convert(open("paper.pdf", "rb").read(), "paper.pdf", Options(drop_methods=True))
open("paper.html", "w", encoding="utf-8").write(result.html)
print(result.document.stats(), result.document.warnings)
```

## Getting the best input

| Source | What to do |
|---|---|
| Publisher PDF | Works directly. Scanned PDFs (no text layer) are not supported. |
| Web article | In Chrome/Edge use **Save as → Webpage, Single File (.mhtml)**. Figures are embedded, so they end up in the output. A plain `.html` also works, images are then downloaded from the page's URLs if the "download images" option is on. |
| Preprints / PMC | PDF or MHTML both fine. |

In your reader app just open the generated `.html` (Speechify, @Voice Aloud Reader, Librera, Moon+ Reader,
Edge/Chrome "Read aloud"… anything that reads HTML). Images have empty `alt` text on purpose so they are skipped silently.

## Options worth knowing

- **Drop Methods / Experimental** – long reagent lists are tedious to hear.
- **Remove NMR / MS data listings** – cuts `1H NMR (400 MHz, DMSO-d6) δ 8.45 (s, 1H)…` tails out of synthesis paragraphs.
- **Extra section titles / paragraph patterns** – regexes, one per line, for journal-specific leftovers.

## How it works

```
clean_paper_tts/
├── readers/        input formats -> Document (list of headings / paragraphs / images)
│   ├── pdf/        PyMuPDF: lines -> regions (figure, table, equation) -> reading order -> paragraphs
│   ├── html.py     article-body detection + DOM walk (MathML / MathJax / KaTeX, tables, figures)
│   └── mhtml.py    unpacks web archives and their embedded images
├── filters/        post-processing on the Document: text clean-up, noise, section dropping, chemistry
├── render/         table -> PNG (Pillow), LaTeX -> PNG (matplotlib), HTML writer
├── convert.py      public entry point
└── cli.py
app.py              Streamlit UI
tests/              synthetic PDFs / HTML, no copyrighted papers
```

### Extending

- **A journal's web layout is not recognised** → add a selector to `BODY_SELECTORS` (or a class to
  `NOISE_CLASS_RE`) in `readers/html.py`.
- **A recurring junk line shows up in the text** → add a regex to `NOISE_PATTERNS` in `filters/noise.py`.
- **A new kind of clean-up** → write `def my_filter(doc, options)` and append it to `FILTERS` in `filters/__init__.py`.
- **A new input format** → implement a reader that returns a `Document` and route it in `convert.py`.
- **A new option** → add it to `Options` (`options.py`) and the sidebar in `app.py`.

## Known limits

- Inline maths inside sentences stays as text (sub/superscripts are flattened: `NH32Cl2`); only display equations become images.
- Tables that continue across pages are cut at the page break.
- PDF equation detection is heuristic (centred, operator-heavy lines); unusual layouts can slip through.
- No OCR for scanned documents.

If a paper converts badly, the quickest fix is usually a new noise pattern or selector; open an issue with the
journal name and (if you can share it) the file.

## Development

```bash
pip install -r requirements-dev.txt
pytest
```

MIT licensed.
