"""Command line interface: ``python -m clean_paper_tts paper.pdf -o paper.html``."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import Options, convert


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="clean_paper_tts", description="Convert a paper (PDF/HTML/MHTML) to TTS-friendly HTML.")
    ap.add_argument("input", type=Path)
    ap.add_argument("-o", "--output", type=Path, help="output HTML (default: <input>.clean.html)")
    ap.add_argument("--report", type=Path, help="write a JSON report (stats, warnings, dropped text)")
    ap.add_argument("--authors", action="store_true", help="include the author line")
    ap.add_argument("--drop-methods", action="store_true", help="drop the Methods / Experimental section")
    ap.add_argument("--no-figures", action="store_true", help="omit figure images (tables and formulas stay)")
    ap.add_argument("--keep-citations", action="store_true", help="keep [12] / (Smith 2020) citation markers")
    ap.add_argument("--keep-characterization", action="store_true", help="keep NMR / MS data listings")
    ap.add_argument("--no-fetch", action="store_true", help="never download images referenced by HTML")
    args = ap.parse_args(argv)

    opts = Options(include_authors=args.authors, drop_methods=args.drop_methods, include_figures=not args.no_figures,
                   strip_citations=not args.keep_citations, strip_author_year_citations=not args.keep_citations,
                   strip_characterization_data=not args.keep_characterization, fetch_remote_images=not args.no_fetch)
    result = convert(args.input.read_bytes(), args.input.name, opts)
    out = args.output or args.input.with_suffix(".clean.html")
    out.write_text(result.html, encoding="utf-8")
    doc = result.document
    print(f"{doc.title}\n  -> {out} ({out.stat().st_size / 1e6:.2f} MB)  {doc.stats()}")
    for w in doc.warnings:
        print("  warning:", w, file=sys.stderr)
    if args.report:
        args.report.write_text(json.dumps({
            "title": doc.title, "authors": doc.authors, "stats": doc.stats(), "warnings": doc.warnings,
            "dropped": [{"reason": d.reason, "page": d.page, "text": d.text[:300]} for d in doc.dropped]},
            indent=1, ensure_ascii=False), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
