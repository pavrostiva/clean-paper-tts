#!/usr/bin/env python3
"""Download open-access papers (Europe PMC) and run the converter over them, writing small reports.

Temporary development helper: the downloaded papers stay in ``dev_data/`` (git-ignored); only compact
text reports are written to ``dev_reports/<batch>/`` so they can be committed and reviewed.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import re
import shutil
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "dev_data"
REPORTS = ROOT / "dev_reports"
SAMPLES = ROOT / "dev_samples"

EPMC = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
UA = "Mozilla/5.0 (X11; Linux x86_64) clean-paper-tts-dev-harness/0.1"
MAX_DOWNLOAD = 25 * 1024 * 1024

# slug -> Europe PMC journal query. Mix of biology / bioinformatics / cheminformatics layouts.
JOURNALS: dict[str, str] = {
    "plos_one": 'JOURNAL:"PLoS One"',
    "plos_comp_biol": 'JOURNAL:"PLoS Comput Biol"',
    "sci_rep": 'JOURNAL:"Sci Rep"',
    "nat_commun": 'JOURNAL:"Nat Commun"',
    "elife": 'JOURNAL:"eLife"',
    "nucleic_acids_res": 'JOURNAL:"Nucleic Acids Res"',
    "bioinformatics": 'JOURNAL:"Bioinformatics"',
    "brief_bioinform": 'JOURNAL:"Brief Bioinform"',
    "bmc_bioinformatics": 'JOURNAL:"BMC Bioinformatics"',
    "genome_biol": 'JOURNAL:"Genome Biol"',
    "j_cheminform": 'JOURNAL:"J Cheminform"',
    "j_chem_inf_model": 'JOURNAL:"J Chem Inf Model"',
    "j_med_chem": 'JOURNAL:"J Med Chem"',
    "acs_omega": 'JOURNAL:"ACS Omega"',
    "molecules": 'JOURNAL:"Molecules"',
    "ijms": 'JOURNAL:"Int J Mol Sci"',
    "cells": 'JOURNAL:"Cells"',
    "cancers": 'JOURNAL:"Cancers (Basel)"',
    "front_immunol": 'JOURNAL:"Front Immunol"',
    "front_pharmacol": 'JOURNAL:"Front Pharmacol"',
    "rsc_adv": 'JOURNAL:"RSC Adv"',
    "heliyon": 'JOURNAL:"Heliyon"',
    "iscience": 'JOURNAL:"iScience"',
    "comput_struct_biotec": 'JOURNAL:"Comput Struct Biotechnol J"',
    "cell_rep": 'JOURNAL:"Cell Rep"',
}


# ------------------------------------------------------------------ network
def http_get(url: str, timeout: int = 40, accept: str = "*/*") -> tuple[bytes, str] | None:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": accept})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            data = r.read(MAX_DOWNLOAD + 1)
            if len(data) > MAX_DOWNLOAD:
                return None
            return data, r.headers.get("Content-Type", "")
    except Exception as e:
        print(f"    ! {url[:90]}: {e}")
        return None


def search(journal_query: str, page: int, size: int = 25) -> list[dict]:
    q = f"({journal_query}) AND OPEN_ACCESS:y AND HAS_FT:y AND LICENSE:cc* AND PUB_YEAR:[2021 TO 2026]"
    params = urllib.parse.urlencode({"query": q, "format": "json", "resultType": "core", "pageSize": size, "page": page})
    got = http_get(f"{EPMC}?{params}", accept="application/json")
    if not got:
        return []
    try:
        return json.loads(got[0])["resultList"]["result"]
    except Exception:
        return []


def pick_urls(rec: dict) -> dict[str, str]:
    urls: dict[str, str] = {}
    for u in (rec.get("fullTextUrlList") or {}).get("fullTextUrl", []):
        if u.get("availabilityCode") not in ("OA", "F"):
            continue
        style = u.get("documentStyle")
        if style in ("pdf", "html") and style not in urls:
            urls[style] = u["url"]
    if rec.get("pmcid"):
        urls.setdefault("pdf", f"https://europepmc.org/articles/{rec['pmcid']}?pdf=render")
    if rec.get("doi"):
        urls["doi_html"] = f"https://doi.org/{rec['doi']}"
    return urls


def looks_like(data: bytes, kind: str) -> bool:
    if kind == "pdf":
        return data[:5] == b"%PDF-"
    head = data[:3000].lower()
    if b"<html" not in head and b"<!doctype html" not in head:
        return False
    low = data[:60000].lower()
    blocked = (b"checking your browser", b"requires javascript to function", b"recaptcha", b"access denied",
               b"just a moment", b"are you a robot", b"enable javascript and cookies")
    return not (any(m in low for m in blocked) and len(data) < 80_000)


def cmd_fetch(a: argparse.Namespace) -> Path:
    rnd = random.Random(a.seed if a.seed is not None else hashlib.sha1(a.name.encode()).hexdigest())
    out = DATA / a.name
    out.mkdir(parents=True, exist_ok=True)
    seen_file = DATA / "seen.json"
    seen: set[str] = set(json.loads(seen_file.read_text())) if seen_file.exists() else set()
    slugs = a.journals.split(",") if a.journals else list(JOURNALS)
    manifest = []
    for slug in slugs:
        if slug not in JOURNALS:
            print(f"unknown journal slug: {slug}")
            continue
        print(f"== {slug}")
        recs = search(JOURNALS[slug], rnd.randint(1, a.max_page))
        rnd.shuffle(recs)
        done = 0
        for rec in recs:
            pid = rec.get("pmcid") or rec.get("id")
            if pid in seen or done >= a.per_journal:
                continue
            urls = pick_urls(rec)
            kinds = []
            if a.kinds in ("pdf", "both") and "pdf" in urls:
                kinds.append(("pdf", urls["pdf"]))
            if a.kinds in ("html", "both"):
                h = urls.get("html") or urls.get("doi_html")
                if h:
                    kinds.append(("html", h))
            ok_any = False
            for kind, url in kinds:
                time.sleep(0.4)
                got = http_get(url, accept="application/pdf" if kind == "pdf" else "text/html")
                if not got or not looks_like(got[0], kind):
                    print(f"    - {pid} {kind}: not usable")
                    continue
                d = out / slug
                d.mkdir(exist_ok=True)
                path = d / f"{pid}.{kind}"
                path.write_bytes(got[0])
                manifest.append({"file": str(path.relative_to(out)), "journal": slug, "id": pid, "doi": rec.get("doi"),
                                 "title": (rec.get("title") or "")[:140], "source_url": url})
                print(f"    + {path.name} ({len(got[0]) / 1e6:.1f} MB)")
                ok_any = True
            if ok_any:
                seen.add(pid)
                done += 1
    seen_file.write_text(json.dumps(sorted(seen)))
    (out / "manifest.json").write_text(json.dumps(manifest, indent=1))
    print(f"downloaded {len(manifest)} files into {out}")
    return out


# --------------------------------------------------------------- analysis
NOISE_IN_TEXT = {
    "download notice": r"downloaded from|downloaded by",
    "doi/url": r"https?://|doi\.org|www\.",
    "copyright": r"©|all rights reserved|creative commons",
    "history": r"\b(received|accepted)\s*:?\s*\d{1,2}\s+\w+\s+\d{4}",
    "web ui": r"open in figure viewer|check for updates|skip to|cookie",
    "journal line": r"j\.\s*med\.\s*chem\.|nucleic acids res|sci\.? rep\.",
}


def analyse(path: Path) -> dict:
    sys.path.insert(0, str(ROOT))
    from clean_paper_tts import Options, convert
    from clean_paper_tts.model import Heading, ListBlock, Paragraph, Visual

    t0 = time.time()
    res = convert(path.read_bytes(), path.name, Options(fetch_remote_images=True))
    d = res.document
    dt = time.time() - t0
    paras = [b for b in d.blocks if isinstance(b, Paragraph) and b.role == "body"]
    caps = [b for b in d.blocks if isinstance(b, Paragraph) and b.role == "caption"]
    heads = [b for b in d.blocks if isinstance(b, Heading)]
    vis = [b for b in d.blocks if isinstance(b, Visual)]
    body = "\n".join(p.text for p in paras)
    flags: list[str] = []
    st = d.stats()
    if not d.title or len(d.title) < 10:
        flags.append("no_title")
    if not any(re.match(r"abstract|summary", h.text, re.I) for h in heads):
        flags.append("no_abstract_heading")
    if st["words"] < 1500:
        flags.append(f"few_words({st['words']})")
    if not heads:
        flags.append("no_headings")
    short = [p for p in paras if len(p.text.split()) < 5]
    if paras and len(short) / len(paras) > 0.25:
        flags.append(f"many_short_paragraphs({len(short)}/{len(paras)})")
    lower_start = [p for p in paras if p.text[:1].islower() and not re.match(r"(where|and|with|in which|respectively)\b", p.text)]
    if lower_start:
        flags.append(f"lowercase_starts({len(lower_start)})")
    no_end = [p for p in paras if len(p.text) > 120 and not p.text.rstrip().endswith((".", "!", "?", ":", ")", '"', "'", "]"))]
    if len(no_end) > 3:
        flags.append(f"unterminated_paragraphs({len(no_end)})")
    if any(len(p.text) > 3500 for p in paras):
        flags.append("huge_paragraph")
    long_heads = [h for h in heads if len(h.text) > 150]
    if long_heads:
        flags.append(f"long_headings({len(long_heads)})")
    for name, rx in NOISE_IN_TEXT.items():
        n = len(re.findall(rx, body, re.I))
        if n:
            flags.append(f"noise:{name}({n})")
    fig_caps = [c for c in caps if re.match(r"\s*(fig|scheme|chart)", c.text, re.I)]
    tab_caps = [c for c in caps if re.match(r"\s*table", c.text, re.I)]
    nfig, ntab = st["figures"], st["tables"]
    if len(fig_caps) > nfig + 1:
        flags.append(f"figure_captions_without_image({len(fig_caps)}>{nfig})")
    if len(tab_caps) > ntab:
        flags.append(f"table_captions_without_image({len(tab_caps)}>{ntab})")
    if len(re.findall(r"[^\x00-\x7f]", body)) / max(len(body), 1) > 0.08:
        flags.append("many_non_ascii")
    refs = [p for p in paras if re.match(r"^\d{1,3}[.)]?\s+[A-Z][a-z]+.*\b(19|20)\d\d\b", p.text)]
    if len(refs) > 3:
        flags.append(f"reference_like_paragraphs({len(refs)})")
    reasons: dict[str, int] = {}
    for x in d.dropped:
        k = x.reason.split(":")[0]
        reasons[k] = reasons.get(k, 0) + 1
    return {
        "file": path.name, "type": d.source_type, "seconds": round(dt, 1), "title": d.title[:160],
        "authors": len(d.authors), "stats": st, "flags": flags, "warnings": d.warnings[:6],
        "dropped_reasons": reasons, "html_mb": round(len(res.html) / 1e6, 2),
        "outline": [("  " * (h.level - 2)) + h.text[:90] for h in heads[:40]],
        "head_text": [p.text[:260] for p in paras[:4]],
        "suspect_paragraphs": [p.text[:200] for p in (lower_start + no_end)[:5]],
        "dropped_sample": [f"[{x.reason[:24]}] {x.text[:100]}" for x in d.dropped
                           if not x.reason.startswith(("running header", "section", "figure text",
                                                       "table body", "sideways", "equation"))][:12],
    }


def run_one(path: Path, timeout: int) -> dict:
    cmd = [sys.executable, str(Path(__file__).resolve()), "_one", str(path)]
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return {"file": path.name, "error": f"timeout after {timeout}s"}
    if p.returncode != 0:
        return {"file": path.name, "error": (p.stderr.strip().splitlines() or ["failed"])[-1][:300]}
    try:
        return json.loads(p.stdout.splitlines()[-1])
    except Exception:
        return {"file": path.name, "error": "unparsable worker output"}


def cmd_run(a: argparse.Namespace) -> None:
    src = Path(a.dir) if a.dir else DATA / a.name
    files = sorted(p for p in src.rglob("*") if p.suffix.lower() in (".pdf", ".html", ".htm", ".mhtml", ".mht"))
    manifest = {}
    if (src / "manifest.json").exists():
        manifest = {m["file"]: m for m in json.loads((src / "manifest.json").read_text())}
    out = REPORTS / a.name
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    results = []
    for i, f in enumerate(files, 1):
        print(f"[{i}/{len(files)}] {f.relative_to(src)}")
        r = run_one(f, a.timeout)
        r["journal"] = manifest.get(str(f.relative_to(src)), {}).get("journal", f.parent.name)
        r["path"] = str(f.relative_to(src))
        results.append(r)
    lines = [f"# Batch {a.name}: {len(results)} files\n",
             "| journal | file | type | s | words | H | P | fig | tab | eq | flags |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in results:
        if "error" in r:
            lines.append(f"| {r['journal']} | {r['file']} | - | - | - | - | - | - | - | - | **ERROR** {r['error']} |")
            continue
        s = r["stats"]
        lines.append(f"| {r['journal']} | {r['file']} | {r['type']} | {r['seconds']} | {s['words']} | {s['headings']} | "
                     f"{s['paragraphs']} | {s['figures']} | {s['tables']} | {s['formulas']} | {'; '.join(r['flags']) or 'ok'} |")
    (out / "summary.md").write_text("\n".join(lines) + "\n")
    detail = []
    for r in results:
        if "error" in r:
            detail.append(f"## {r['journal']} / {r['file']}\nERROR: {r['error']}\n")
            continue
        detail.append(
            f"## {r['journal']} / {r['file']}\n**{r['title']}** ({r['type']}, {r['seconds']}s, {r['html_mb']} MB, "
            f"authors parsed: {r['authors']})\n\nflags: {', '.join(r['flags']) or 'none'}\n\n"
            f"warnings: {r['warnings'] or 'none'}\n\ndropped: {r['dropped_reasons']}\n\n"
            "outline:\n```\n" + "\n".join(r["outline"]) + "\n```\n"
            "first paragraphs:\n" + "\n".join(f"- {t}" for t in r["head_text"]) + "\n\n"
            "suspect paragraphs:\n" + ("\n".join(f"- {t}" for t in r["suspect_paragraphs"]) or "- none") + "\n\n"
            "dropped sample:\n" + ("\n".join(f"- {t}" for t in r["dropped_sample"]) or "- none") + "\n")
    text = "\n".join(detail)
    (out / "details.md").write_text(text[: a.max_kb * 1024])
    (out / "results.json").write_text(json.dumps(results, indent=0)[: a.max_kb * 2048])
    flagged = sum(1 for r in results if r.get("flags") or "error" in r)
    print(f"\nreport: {out}  ({flagged}/{len(results)} files with flags)")


def cmd_stash(a: argparse.Namespace) -> None:
    res_path = REPORTS / a.name / "results.json"
    results = json.loads(res_path.read_text())
    src = Path(a.dir) if a.dir else DATA / a.name
    scored = sorted(results, key=lambda r: -(len(r.get("flags", [])) + (5 if "error" in r else 0)))
    SAMPLES.mkdir(exist_ok=True)
    used = sum(f.stat().st_size for f in SAMPLES.glob("*"))
    cap = a.max_mb * 1024 * 1024
    copied = 0
    for r in scored[: a.worst]:
        f = src / r.get("path", r["file"])
        if f.exists() and used + f.stat().st_size <= cap:
            shutil.copy2(f, SAMPLES / f"{a.name}__{r['journal']}__{f.name}")
            used += f.stat().st_size
            copied += 1
    print(f"copied {copied} files, dev_samples is now {used / 1e6:.1f} MB (cap {a.max_mb} MB)")


def cmd_clean(a: argparse.Namespace) -> None:
    for d in (DATA, SAMPLES) + ((REPORTS,) if a.reports else ()):
        if d.exists():
            shutil.rmtree(d)
            print("removed", d)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)
    f = sub.add_parser("fetch")
    f.add_argument("--name", required=True)
    f.add_argument("--journals", help="comma separated slugs (default: all)")
    f.add_argument("--per-journal", type=int, default=1)
    f.add_argument("--kinds", choices=["pdf", "html", "both"], default="both")
    f.add_argument("--seed", type=int)
    f.add_argument("--max-page", type=int, default=30)
    r = sub.add_parser("run")
    r.add_argument("--name", required=True)
    r.add_argument("--dir")
    r.add_argument("--timeout", type=int, default=240)
    r.add_argument("--max-kb", type=int, default=160)
    al = sub.add_parser("all")
    al.add_argument("--name", required=True)
    al.add_argument("--journals")
    al.add_argument("--per-journal", type=int, default=1)
    al.add_argument("--kinds", choices=["pdf", "html", "both"], default="both")
    al.add_argument("--seed", type=int)
    al.add_argument("--max-page", type=int, default=30)
    al.add_argument("--timeout", type=int, default=240)
    al.add_argument("--max-kb", type=int, default=160)
    st = sub.add_parser("stash")
    st.add_argument("--name", required=True)
    st.add_argument("--dir")
    st.add_argument("--worst", type=int, default=3)
    st.add_argument("--max-mb", type=float, default=15)
    c = sub.add_parser("clean")
    c.add_argument("--reports", action="store_true")
    o = sub.add_parser("_one")
    o.add_argument("path")
    a = ap.parse_args()
    if a.cmd == "fetch":
        cmd_fetch(a)
    elif a.cmd == "run":
        cmd_run(a)
    elif a.cmd == "all":
        cmd_fetch(a)
        a.dir = None
        cmd_run(a)
    elif a.cmd == "stash":
        cmd_stash(a)
    elif a.cmd == "clean":
        cmd_clean(a)
    elif a.cmd == "_one":
        print(json.dumps(analyse(Path(a.path))))


if __name__ == "__main__":
    main()
