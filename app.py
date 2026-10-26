"""Streamlit front-end for clean-paper-tts."""

from __future__ import annotations

import hashlib
from collections import defaultdict

import streamlit as st

from clean_paper_tts import Options, convert
from clean_paper_tts.model import Heading
from clean_paper_tts.options import DEFAULT_DROP_SECTIONS



def show_html(html: str, height: int = 700) -> None:
    """Preview the generated page (it contains only escaped text and <img> tags, no scripts)."""
    if hasattr(st, "iframe"):
        st.iframe(html, height=height)
    else:  # older Streamlit releases
        import streamlit.components.v1 as components

        components.html(html, height=height, scrolling=True)


st.set_page_config(page_title="Clean Paper TTS", page_icon="🎧", layout="wide")

st.title("🎧 Clean Paper TTS")
st.write(
    "Turn a scientific paper (PDF, HTML or MHTML) into a clean HTML file for a text-to-speech reader app. "
    "Prose stays as text; tables, figures and equations become images, and journal boiler-plate "
    "(headers, footers, watermarks, reference lists) is removed."
)

with st.sidebar:
    st.header("Options")
    include_authors = st.checkbox("Include author line", value=False)
    include_captions = st.checkbox("Read figure / table captions", value=True)
    include_figures = st.checkbox("Include figure images", value=True)
    drop_methods = st.checkbox("Drop Methods / Experimental section", value=False)
    strip_citations = st.checkbox("Remove citation markers ([12], (Smith 2020))", value=True)
    strip_chem = st.checkbox("Remove NMR / MS data listings", value=True)
    formulas_as_images = st.checkbox("Show display equations as images", value=True)
    fetch_remote = st.checkbox("Download images referenced by HTML files", value=True,
                               help="Only needed for plain .html pages. MHTML files already contain their images.")
    with st.expander("Advanced"):
        extra_sections = st.text_area("Extra section titles to drop (regex, one per line)", "", height=80)
        extra_noise = st.text_area("Extra paragraph patterns to drop (regex, one per line)", "", height=80,
                                   help="A paragraph matching any pattern is removed.")
        dpi = st.slider("Render resolution (DPI)", 100, 300, 170, 10)
    st.caption("Files are processed in memory and are not stored.")


def build_options() -> Options:
    extra = tuple(x.strip() for x in extra_sections.splitlines() if x.strip())
    return Options(
        include_authors=include_authors, include_captions=include_captions, include_figures=include_figures,
        drop_methods=drop_methods, strip_citations=strip_citations, strip_author_year_citations=strip_citations,
        strip_characterization_data=strip_chem, formulas_as_images=formulas_as_images,
        fetch_remote_images=fetch_remote, render_dpi=dpi, drop_sections=DEFAULT_DROP_SECTIONS + extra,
        extra_noise_patterns=[x.strip() for x in extra_noise.splitlines() if x.strip()],
    )


@st.cache_data(show_spinner=False, max_entries=8)
def run_conversion(data_hash: str, data: bytes, name: str, opts_repr: str, _opts: Options):
    result = convert(data, name, _opts)
    return result.html, result.document


files = st.file_uploader("Upload one or more papers", type=["pdf", "html", "htm", "mhtml", "mht"],
                         accept_multiple_files=True)
st.caption("Tip: for web articles use *Save as → Webpage, Single File (.mhtml)* in Chrome/Edge so figures are embedded.")

opts = build_options()
for f in files or []:
    data = f.getvalue()
    key = hashlib.sha1(data).hexdigest()
    with st.container(border=True):
        try:
            with st.spinner(f"Converting {f.name}…"):
                html, doc = run_conversion(key, data, f.name, repr(opts), opts)
        except Exception as e:  # keep the app alive on malformed files
            st.error(f"Could not convert **{f.name}**: {e}")
            continue
        st.subheader(doc.title or f.name)
        stats = doc.stats()
        cols = st.columns(6)
        for col, (label, k) in zip(cols, [("Words", "words"), ("Sections", "headings"), ("Paragraphs", "paragraphs"),
                                          ("Figures", "figures"), ("Tables", "tables"), ("Formulas", "formulas")]):
            col.metric(label, stats[k])
        for w in doc.warnings:
            st.warning(w)
        out_name = f.name.rsplit(".", 1)[0] + ".html"
        st.download_button("⬇️ Download HTML", html.encode("utf-8"), file_name=out_name, mime="text/html",
                           key=f"dl-{key}", type="primary")
        tab_prev, tab_out, tab_drop = st.tabs(["Preview", "Outline", "What was removed"])
        with tab_prev:
            if st.toggle("Show preview", value=len(html) < 6_000_000, key=f"pv-{key}"):
                show_html(html)
        with tab_out:
            for b in doc.blocks:
                if isinstance(b, Heading):
                    st.write("&nbsp;" * 4 * (b.level - 2) + b.text)
        with tab_drop:
            if not doc.dropped:
                st.write("Nothing was removed.")
            groups = defaultdict(list)
            for d in doc.dropped:
                groups[d.reason.split(":")[0]].append(d)
            for reason, items in sorted(groups.items(), key=lambda kv: -len(kv[1])):
                with st.expander(f"{reason} ({len(items)})"):
                    for d in items[:200]:
                        st.text((f"p.{d.page}: " if d.page else "") + d.text[:240])
