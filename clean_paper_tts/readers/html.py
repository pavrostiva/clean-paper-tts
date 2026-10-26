"""HTML reader: locate the article body, walk it, emit Document blocks.

Publisher quirks live in ``BODY_SELECTORS`` / ``NOISE_SELECTORS`` / ``NOISE_CLASS_RE`` so
supporting a new journal normally means adding one line to one of them.
"""

from __future__ import annotations

import re

from bs4 import BeautifulSoup, NavigableString, Tag

from ..model import Document, Heading, ListBlock, Paragraph, Visual
from ..options import Options
from ..render.formula_image import render_latex
from ..render.images import to_visual
from ..render.table_image import render_table
from ..textutil import clean_heading, is_citation_superscript, normalize
from .resources import Resources

# First selector that yields >= MIN_BODY_CHARS of text wins (most specific first).
BODY_SELECTORS = (
    "div.article__body",                    # Wiley
    "div.article_content-left", "div#article-content", "div.NLM_sec_level_1",  # ACS (old/new)
    "section#bodymatter", "div.core-container",  # Cell / Science (Atypon)
    "div#body", "div.Body", "article div.article-section__content",  # Elsevier ScienceDirect
    "div.c-article-body", "div.main-content article",  # Springer / Nature
    "div.jig-ncbiinpagenav", "section.body", "div.tsec",  # PMC
    "div.html-body", "div.html-article-content",  # MDPI
    "div.JournalFullText", "div.article-container",  # Frontiers
    "div.article-text", "div#artText",      # PLOS
    "div.article-body", "div.article__sections",  # OUP / T&F / generic
    "div.fulltext-view", "div.article.fulltext-view",  # bioRxiv / medRxiv
    "article", "main", "div[role=main]",
)
MIN_BODY_CHARS = 1500

NOISE_TAGS = ("script", "style", "noscript", "nav", "footer", "aside", "form", "button", "select",
              "option", "input", "textarea", "iframe", "template", "svg", "canvas", "dialog", "audio", "video")
NOISE_CLASS_RE = re.compile(
    r"(^|[\s_-])(cookie|consent|banner|advert|ads?|sponsor|social|share|sharing|toolbar|coolbar|breadcrumb|"
    r"modal|popup|tooltip|dropdown|sidebar|related|recommend|cited-?by|citing|metrics|altmetric|download|"
    r"permissions?|rights|crossmark|tabs?|skip|sr-only|visually-hidden|hidden|print-hidden|pagination|"
    r"article-?tools|extra-links|getFTR|footnote-?back|back-?link|author-?info|affiliation|corresp|"
    r"figure-?extra|open-?figure|ppt-?figure|figure-?link|fig-?tools|figure-?viewer)($|[\s_-])",
    re.I)
NOISE_ID_RE = re.compile(r"(cookie|consent|breadcrumb|sidebar|related|cited|trendmd|advert|toolbar|header|footer)", re.I)
UI_TEXT_RE = re.compile(
    r"(Open in figure viewer|PowerPoint|Download (figure|image|table|PowerPoint)|View (full|larger) (size|image)|"
    r"Full size (image|table)|Open in new tab|Download (high-res|full-size) image)", re.I)
CITATION_LINK_TEXT = re.compile(r"^\s*[\[(]?\s*\d{1,3}(?:\s*[,–—−-]\s*\d{1,3})*\s*[\])]?\s*$")
CITATION_LINK_CLASS = re.compile(r"bib|ref|cite|citation|footnote|fn|noteLink|xref|noteref", re.I)
# fragment ids that point into the reference list: #bib4, #ref12, #B7, #CR3, #fn2, #core-r5 ...
REFERENCE_FRAGMENT_RE = re.compile(r"(?:^|[-_.])(?:bbib|bib|ref|refs|cit|cite|cr|fn|b|r|c|xref-ref|ref-ref)[-_.]?\d+", re.I)
SEPARATOR_ONLY_RE = re.compile(r"^[\s,;\u2013\u2014\u2212-]+$")
CITE_ONLY_RE = re.compile(r"^[\d\s,\u2013\u2014\u2212-]+$")
INLINE = {"a", "span", "b", "strong", "i", "em", "u", "sup", "sub", "small", "mark", "code", "abbr",
          "cite", "q", "font", "label", "time", "bdi", "bdo", "kbd", "var", "samp", "math", "br", "wbr"}
BLOCK_CONTAINERS = {"div", "section", "article", "main", "body", "header", "blockquote", "figure",
                    "fieldset", "details", "summary", "dl", "dd", "dt", "td", "th", "li", "ul", "ol",
                    "table", "p", "h1", "h2", "h3", "h4", "h5", "h6", "pre", "address", "hr"}
SKIP_IMG_RE = re.compile(r"logo|icon|sprite|spinner|avatar|badge|banner|button|pixel|tracking|cover|orcid|loading", re.I)
FIGURE_CLASS_RE = re.compile(r"(^|[\s_-])(fig|figure|graphic|inline-figure|figure-?wrap|fig-?group)($|[\s_-])", re.I)
TABLE_WRAP_RE = re.compile(r"(table-?wrap|article-table-content|table-?container|c-article-table|tbl|table-block)", re.I)
CAPTION_RE = re.compile(r"caption", re.I)
FOOT_RE = re.compile(r"(foot|note)", re.I)
EQUATION_RE = re.compile(r"(disp-?formula|display-?equation|inline-equation|equation-?block|math-?block|\beq\b|ltx_equation)", re.I)


class HtmlReader:
    def __init__(self, html: str, resources: Resources, options: Options):
        self.soup = BeautifulSoup(html, "lxml")
        self.res = resources
        self.opt = options
        self.doc = Document(source_type="html")
        self._seen_imgs: set[str] = set()

    # ------------------------------------------------------------ public
    def read(self) -> Document:
        self._read_metadata()
        self._normalize_math()
        root = self._find_root()
        self._strip_noise(root)
        self._walk_container(root)
        self._postprocess()
        return self.doc

    # ---------------------------------------------------------- metadata
    def _meta(self, *names: str, all_: bool = False):
        vals = []
        for n in names:
            for m in self.soup.find_all("meta", attrs={"name": n}) + self.soup.find_all("meta", attrs={"property": n}):
                c = (m.get("content") or "").strip()
                if c:
                    vals.append(c)
            if vals and not all_:
                break
        return vals if all_ else (vals[0] if vals else "")

    def _read_metadata(self) -> None:
        d = self.doc
        title = self._meta("citation_title", "dc.title", "DC.Title", "og:title", "twitter:title")
        if not title:
            h1 = self.soup.find("h1")
            title = h1.get_text(" ", strip=True) if h1 else (self.soup.title.get_text(strip=True) if self.soup.title else "")
        d.title = normalize(title)
        authors = self._meta("citation_author", "dc.creator", "DC.Creator", all_=True)
        d.authors = [normalize(a) for a in authors]
        d.metadata = {
            "doi": self._meta("citation_doi", "dc.identifier", "DC.Identifier"),
            "journal": self._meta("citation_journal_title", "prism.publicationName", "og:site_name"),
            "date": self._meta("citation_publication_date", "citation_date", "dc.date", "article:published_time"),
        }
        if self.res.base_url == "":
            self.res.base_url = self._meta("citation_fulltext_html_url", "og:url") or ""
        link = self.soup.find("base", href=True)
        if link and not self.res.base_url:
            self.res.base_url = link["href"]

    # -------------------------------------------------------------- math
    def _normalize_math(self) -> None:
        """Collapse rendered MathJax / KaTeX markup back to a single <math> element."""
        soup = self.soup

        def new_math(latex: str, display: bool) -> Tag:
            m = soup.new_tag("math", display="block" if display else "inline")
            ann = soup.new_tag("annotation", encoding="application/x-tex")
            ann.string = latex
            m.append(ann)
            return m

        for c in soup.find_all(["mjx-container"]):
            inner = c.find("math")
            display = (c.get("display") or "").lower() == "true"
            if inner is not None:
                inner.extract()
                inner["display"] = "block" if display else "inline"
                c.replace_with(inner)
            elif c.get("data-semantic-speech-none"):
                c.replace_with(NavigableString(" " + c["data-semantic-speech-none"] + " "))
            else:
                c.decompose()
        for c in soup.select("span.katex-display, span.katex"):
            if c.parent is None or (c.name == "span" and "katex" in (c.parent.get("class") or []) and c.parent.name == "span"):
                continue
            display = "katex-display" in (c.get("class") or [])
            ann = c.find("annotation")
            if ann is not None:
                c.replace_with(new_math(ann.get_text(), display))
        for sc in soup.find_all("script", attrs={"type": re.compile(r"^math/tex")}):
            display = "mode=display" in (sc.get("type") or "")
            sc.replace_with(new_math(sc.get_text(), display))
        for c in soup.select(".MathJax_Preview, .MathJax_Display, .MathJax, span.MathJax_SVG"):
            c.decompose()

    # -------------------------------------------------------------- root
    def _find_root(self) -> Tag:
        # drop the page chrome first so selectors can't match huge wrappers around it
        for sel in BODY_SELECTORS:
            for cand in self.soup.select(sel):
                if len(cand.get_text(" ", strip=True)) >= MIN_BODY_CHARS:
                    return cand
        best, best_score = None, 0
        for el in self.soup.find_all(["div", "section", "article", "main"]):
            paras = el.find_all("p", recursive=False) or el.find_all("p")
            score = sum(len(p.get_text(" ", strip=True)) for p in paras if len(p.get_text(strip=True)) > 80)
            links = sum(len(a.get_text()) for a in el.find_all("a"))
            score -= links * 0.5
            if score > best_score:
                best, best_score = el, score
        if best is not None:
            self.doc.warnings.append("Article body located by text-density heuristic; verify the output.")
            return best
        self.doc.warnings.append("Could not locate an article body; using the whole page.")
        return self.soup.body or self.soup

    def _strip_noise(self, root: Tag) -> None:
        for t in root.find_all(NOISE_TAGS):
            t.decompose()
        for el in list(root.find_all(True)):
            if el.decomposed if hasattr(el, "decomposed") else False:
                continue
            if el.attrs is None:
                continue
            cls = " ".join(el.get("class", []))
            style = (el.get("style") or "").replace(" ", "").lower()
            keep = bool(el.find(["figure", "table", "math"])) and el.name in ("div", "section")
            if ("display:none" in style or el.get("aria-hidden") == "true" and el.name not in ("math",)
                    or el.get("hidden") is not None):
                el.decompose()
            elif el.get("role") in ("navigation", "banner", "contentinfo", "complementary", "dialog"):
                el.decompose()
            elif cls and NOISE_CLASS_RE.search(cls) and not keep and not self._contains_body_text(el):
                el.decompose()
            elif el.get("id") and NOISE_ID_RE.search(el["id"]) and not keep and not self._contains_body_text(el) \
                    and el is not root:
                el.decompose()

    @staticmethod
    def _contains_body_text(el: Tag) -> bool:
        return len(el.get_text(" ", strip=True)) > 1200

    # -------------------------------------------------------------- walk
    def _walk_container(self, node: Tag) -> None:
        buf: list = []

        def flush():
            if buf:
                text = self._inline_text(buf)
                if text:
                    self.doc.blocks.append(Paragraph(text))
                buf.clear()

        for child in node.children:
            if isinstance(child, NavigableString):
                if not isinstance(child, (type(child) if False else ())) and str(child).strip():
                    buf.append(child)
                continue
            if not isinstance(child, Tag):
                continue
            if self._is_inline_run(child):
                buf.append(child)
                continue
            flush()
            self._handle_block(child)
        flush()

    def _is_inline_run(self, el: Tag) -> bool:
        if el.name == "math":
            return not self._is_display_math(el)
        if el.name not in INLINE:
            return False
        return not el.find(["table", "figure", "p", "div", "ul", "ol", "h1", "h2", "h3", "h4", "h5", "h6", "img"]) \
            or (el.name == "a" and not el.find(["table", "figure", "p", "div"]) and not el.find("img"))

    def _handle_block(self, el: Tag) -> None:
        name = el.name
        cls = " ".join(el.get("class", []))
        if name in ("h1", "h2", "h3", "h4", "h5", "h6"):
            text = clean_heading(self._inline_text([el]))
            if text:
                self.doc.blocks.append(Heading(text, int(name[1])))
        elif name == "p":
            self._handle_paragraph(el)
        elif name in ("ul", "ol"):
            items = [self._inline_text([li]) for li in el.find_all("li", recursive=False)]
            items = [i for i in items if i]
            if items:
                self.doc.blocks.append(ListBlock(items, ordered=name == "ol"))
        elif name == "table":
            self._handle_table(el, wrapper=None)
        elif name in ("figure",) or (name in ("div", "section") and FIGURE_CLASS_RE.search(cls)
                                     and (el.find("img") or el.find("picture") or el.find(["figcaption"]))):
            self._handle_figure(el)
        elif name in ("div", "section", "article") and TABLE_WRAP_RE.search(cls + " " + (el.get("id") or "")) \
                and (el.find("table") or el.find("img")):
            self._handle_table_wrapper(el)
        elif name == "math" or (name in ("div", "span", "section") and EQUATION_RE.search(cls) and el.find("math")):
            self._handle_equation(el)
        elif name == "img":
            self._handle_loose_image(el)
        elif name == "pre":
            txt = el.get_text(" ", strip=True)
            if txt:
                self.doc.blocks.append(Paragraph(normalize(txt)))
        elif name == "hr":
            return
        elif name in BLOCK_CONTAINERS or name in INLINE:
            if name in ("div", "section", "article", "main", "header", "body", "blockquote", "details",
                        "summary", "dl", "dd", "dt", "td", "th", "li", "fieldset", "address"):
                self._walk_container(el)
            else:
                self._walk_container(el)
        else:
            self._walk_container(el)

    # --------------------------------------------------------- paragraphs
    def _handle_paragraph(self, p: Tag) -> None:
        # paragraphs can wrap display maths / images / figures in sloppy markup
        if p.find(["figure", "table"]) or any(self._is_display_math(m) for m in p.find_all("math")):
            self._walk_container(p)
            return
        text = self._inline_text([p])
        if text:
            self.doc.blocks.append(Paragraph(text))
        for img in p.find_all("img"):
            self._handle_loose_image(img)

    def _inline_text(self, nodes: list) -> str:
        parts: list[str] = []

        def walk(n):
            if isinstance(n, NavigableString):
                if n.__class__.__name__ in ("Comment", "Doctype", "ProcessingInstruction", "Declaration", "CData"):
                    return
                parts.append(str(n))
                return
            if not isinstance(n, Tag):
                return
            name = n.name
            if name == "br":
                parts.append(" ")
            elif name in ("script", "style"):
                return
            elif name == "math":
                parts.append(" " + self._math_text(n) + " ")
            elif name in ("a", "sup", "span") and self._is_citation_marker(n):
                self.doc.citations_removed.append(n.get_text("", strip=True))
                return
            elif name == "sup" or name == "sub":
                inner = n.get_text("", strip=True)
                if name == "sup" and self.opt.strip_citations and inner:
                    if SEPARATOR_ONLY_RE.match(inner):  # commas between linked citation numbers
                        return
                    if CITE_ONLY_RE.match(inner) and is_citation_superscript(inner, "".join(parts), ""):
                        self.doc.citations_removed.append(inner)
                        return
                parts.append(inner)
            elif name == "img":
                alt = n.get("alt", "")
                if alt and len(alt) < 40 and not SKIP_IMG_RE.search(alt):
                    parts.append(alt)
            elif name in ("div", "span") and n.get("class") and EQUATION_RE.search(" ".join(n["class"])) and n.find("math"):
                for c in n.children:
                    walk(c)
            else:
                for c in n.children:
                    walk(c)

        for n in nodes:
            walk(n)
        text = UI_TEXT_RE.sub(" ", "".join(parts))
        return normalize(text)

    def _is_citation_marker(self, n: Tag) -> bool:
        """A link (or a <sup>/<span> wrapping one) that points into the reference list and shows only numbers."""
        if not self.opt.strip_citations:
            return False
        txt = n.get_text("", strip=True)
        if not txt or not CITATION_LINK_TEXT.match(txt):
            return False
        if n.name == "a":
            return self._points_to_reference(n)
        if n.name in ("sup", "span"):
            anchors = n.find_all("a")
            return bool(anchors) and all(self._points_to_reference(a) for a in anchors) \
                and CITE_ONLY_RE.match(re.sub(r"[\[\]()]", "", txt)) is not None
        return False

    @staticmethod
    def _points_to_reference(a: Tag) -> bool:
        href = a.get("href", "") or ""
        frag = href.split("#", 1)[1] if "#" in href else ""
        cls = " ".join(a.get("class", []))
        attrs = " ".join(str(a.get(k, "")) for k in ("data-xocs-content-type", "data-test", "data-track-action",
                                                      "role", "epub:type", "aria-label", "data-reference-type"))
        if re.search(r"reference|citation|noteref|bibr", attrs, re.I):
            return True
        if CITATION_LINK_CLASS.search(cls) and (frag or href.startswith("#")):
            return True
        return bool(frag and REFERENCE_FRAGMENT_RE.search(frag))

    # ---------------------------------------------------------- math
    @staticmethod
    def _is_display_math(m: Tag) -> bool:
        if (m.get("display") or "").lower() == "block":
            return True
        for anc in list(m.parents)[:4]:
            if isinstance(anc, Tag) and anc.get("class") and EQUATION_RE.search(" ".join(anc["class"])) \
                    and "inline-equation__construct" not in " ".join(anc.get("class", [])) \
                    and anc.name in ("div", "p", "section", "disp-formula"):
                if (m.get("display") or "inline").lower() == "inline" and not re.search(r"inline-equation|disp", " ".join(anc["class"])):
                    return False
                return True
        return False

    @staticmethod
    def _latex_of(m: Tag) -> str:
        ann = m.find("annotation", attrs={"encoding": re.compile(r"tex", re.I)})
        if ann is not None and ann.get_text(strip=True):
            return ann.get_text(strip=True)
        return m.get("alttext", "") if m.get("alttext", "").count("\\") else ""

    @staticmethod
    def _math_text(m: Tag) -> str:
        clone = BeautifulSoup(str(m), "lxml")
        for a in clone.find_all("annotation"):
            a.decompose()
        for a in clone.find_all("annotation-xml"):
            a.decompose()
        return normalize(clone.get_text("", strip=True))

    def _handle_equation(self, el: Tag) -> None:
        math = el if el.name == "math" else el.find("math")
        label = ""
        lab = el.find(class_=re.compile(r"label|number|eq-?num", re.I)) if el.name != "math" else None
        if lab is not None:
            label = normalize(lab.get_text(" ", strip=True))
        if self.opt.formulas_as_images and math is not None:
            png = render_latex(self._latex_of(math)) if self._latex_of(math) else None
            vis = to_visual(png, "formula", label, self.opt.max_image_width, self.opt.render_dpi) if png else None
            if vis is None:
                src = None
                holder = el.find(attrs={"data-altimg": True})
                if holder is not None:
                    src = holder["data-altimg"]
                elif math.get("altimg") and not str(math.get("altimg")).startswith("urn:"):
                    src = math["altimg"]
                got = self.res.get(src)
                if got:
                    vis = to_visual(got[0], "formula", label, self.opt.max_image_width, self.opt.render_dpi, got[1])
            if vis is not None:
                self.doc.blocks.append(vis)
                return
        text = self._math_text(math) if math is not None else normalize(el.get_text(" ", strip=True))
        if text:
            self.doc.blocks.append(Paragraph(text))

    # ---------------------------------------------------------- figures
    def _best_img_src(self, scope: Tag) -> tuple[bytes, str] | None:
        cands: list[str] = []
        for img in scope.find_all("img"):
            for attr in ("data-lg-src", "data-full-src", "data-original", "data-src", "src"):
                v = img.get(attr)
                if v and not v.startswith("data:image/gif"):
                    cands.append(v)
            srcset = img.get("srcset") or ""
            cands += [s.split()[0] for s in srcset.split(",") if s.strip()]
        for src in scope.find_all("source"):
            cands += [s.strip().split()[0] for s in (src.get("srcset") or "").split(",") if s.strip()]
        for a in scope.find_all("a", href=True):
            if re.search(r"\.(png|jpe?g|gif|webp|svg)(\?|$)", a["href"], re.I):
                cands.append(a["href"])
        best = None
        for c in cands:
            got = self.res.get(c)
            if got and (best is None or len(got[0]) > len(best[0])) and not SKIP_IMG_RE.search(c.rsplit("/", 1)[-1]):
                best = got
        return best

    def _caption_text(self, scope: Tag) -> str:
        cap = scope.find("figcaption") or scope.find(class_=CAPTION_RE) or scope.find("header")
        if cap is None:
            return ""
        return self._inline_text([cap])

    def _handle_figure(self, el: Tag) -> None:
        caption = self._caption_text(el)
        got = self._best_img_src(el)
        if got:
            key = str(hash(got[0]))
            if key not in self._seen_imgs:
                self._seen_imgs.add(key)
                vis = to_visual(got[0], "figure", "", self.opt.max_image_width, self.opt.render_dpi, got[1])
                if vis is not None:
                    self.doc.blocks.append(vis)
                else:
                    self.doc.warnings.append(f"Could not decode a figure image ({caption[:40]!r}).")
            else:
                got = None
        else:
            if el.find("img") or el.find("picture"):
                self.doc.warnings.append(f"Figure image not available offline: {caption[:50]!r}. "
                                         "Save the page as MHTML to embed images.")
        if caption:
            self.doc.blocks.append(Paragraph(caption, role="caption"))

    def _handle_loose_image(self, img: Tag) -> None:
        src = img.get("src") or img.get("data-src") or ""
        w = img.get("width", "")
        if SKIP_IMG_RE.search(src.rsplit("/", 1)[-1]) or SKIP_IMG_RE.search(" ".join(img.get("class", []))):
            return
        if str(w).isdigit() and int(w) < 80:
            return
        got = self._best_img_src(img.parent if isinstance(img.parent, Tag) and img.parent.name in ("a", "picture") else img)
        if got:
            vis = to_visual(got[0], "figure", "", self.opt.max_image_width, self.opt.render_dpi, got[1])
            if vis is not None and vis.width >= 120 and vis.height >= 80:
                key = str(hash(got[0]))
                if key not in self._seen_imgs:
                    self._seen_imgs.add(key)
                    self.doc.blocks.append(vis)

    # ----------------------------------------------------------- tables
    def _handle_table_wrapper(self, el: Tag) -> None:
        table = el.find("table")
        cap_el = None
        for cand in el.find_all(True):
            if cand.name == "table" or cand.find_parent("table") is not None:
                continue
            c = " ".join(cand.get("class", []))
            if (cand.name in ("caption", "figcaption", "header") or CAPTION_RE.search(c)) and cand.get_text(strip=True):
                cap_el = cand
                break
        if cap_el is None and table is not None and table.find("caption"):
            cap_el = table.find("caption")
        caption = self._inline_text([cap_el]) if cap_el is not None else ""
        foot_els = [f for f in el.find_all(True)
                    if f.find_parent("table") is None and f.name != "table"
                    and FOOT_RE.search(" ".join(f.get("class", []))) and "link" not in " ".join(f.get("class", []))
                    and f.get_text(strip=True) and not f.find(["table"]) and f.find_parent(class_=FOOT_RE) is None]
        foot = " ".join(self._inline_text([f]) for f in foot_els)
        if caption:
            self.doc.blocks.append(Paragraph(caption, role="caption"))
        self._emit_table(table, el)
        if foot and self.opt.include_captions:
            self.doc.blocks.append(Paragraph(foot, role="caption"))

    def _handle_table(self, table: Tag, wrapper: Tag | None) -> None:
        cap = table.find("caption")
        if cap is not None:
            text = self._inline_text([cap])
            if text:
                self.doc.blocks.append(Paragraph(text, role="caption"))
        self._emit_table(table, wrapper)

    def _emit_table(self, table: Tag | None, wrapper: Tag | None) -> None:
        if table is not None:
            if len(table.find_all("tr")) <= 1 and len(table.find_all(["td", "th"])) <= 1:
                text = self._inline_text([table])  # layout table, not data
                if text:
                    self.doc.blocks.append(Paragraph(text))
                return
            png = render_table(table)
            vis = to_visual(png, "table", "", self.opt.max_image_width * 2, self.opt.render_dpi) if png else None
            if vis is not None:
                self.doc.blocks.append(vis)
                return
            self.doc.warnings.append("A table could not be rendered as an image and was skipped.")
        elif wrapper is not None:
            got = self._best_img_src(wrapper)
            if got:
                vis = to_visual(got[0], "table", "", self.opt.max_image_width, self.opt.render_dpi, got[1])
                if vis is not None:
                    self.doc.blocks.append(vis)

    # --------------------------------------------------------- finishing
    def _postprocess(self) -> None:
        blocks, out = self.doc.blocks, []
        title_key = re.sub(r"\W+", "", self.doc.title.lower())
        for b in blocks:
            if isinstance(b, Heading):
                if re.sub(r"\W+", "", b.text.lower()) == title_key:
                    continue  # title is emitted by the writer
            if isinstance(b, Paragraph) and out and isinstance(out[-1], Paragraph) and b.text == out[-1].text:
                continue
            out.append(b)
        # shift heading levels so the top-most body heading is an <h2>
        levels = [b.level for b in out if isinstance(b, Heading)]
        if levels:
            shift = min(levels) - 2
            for b in out:
                if isinstance(b, Heading):
                    b.level = max(2, b.level - shift)
        self.doc.blocks = out


def read_html(html: str, resources: Resources, options: Options) -> Document:
    return HtmlReader(html, resources, options).read()
