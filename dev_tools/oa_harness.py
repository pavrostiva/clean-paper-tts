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
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "dev_data"          # git-ignored: downloads, cache, local state
CACHE = DATA / "cache"
STATE = DATA / "state.json"
REPORTS = ROOT / "dev_reports"    # small text reports (committed)
SAMPLES = ROOT / "dev_samples"    # a few problematic source files (committed, size-capped)
BLOCKLIST = Path(__file__).resolve().parent / "blocklist.json"  # public URLs / ids that cannot be fetched (committed)
CORPUS = Path(__file__).resolve().parent / "corpus.json"        # usable articles, for repeatable runs (committed)

EPMC = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
UNPAYWALL = "https://api.unpaywall.org/v2/"
UA = "Mozilla/5.0 (X11; Linux x86_64) clean-paper-tts-dev-harness/0.2"
MAX_DOWNLOAD = 25 * 1024 * 1024
HOST_STRIKES = 3  # skip a host for the rest of the run after this many 403/429 answers in a row

# only these paths may ever be committed from this tool (see the `check` command)
COMMIT_ALLOWED = ("dev_reports/", "dev_samples/", "dev_tools/")
SAMPLES_CAP_MB = 25


def scrub(text: str) -> str:
    """Remove anything that identifies the local machine from text that ends up in reports."""
    home = str(Path.home())
    for needle, repl in ((str(ROOT), "<repo>"), (home, "~")):
        if needle and needle != "/":
            text = text.replace(needle, repl)
    return re.sub(r"/(?:home|Users)/[^/\s]+", "~", text)


def load_json(path: Path, default):
    try:
        return json.loads(path.read_text())
    except Exception:
        return default


def save_json(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=1, sort_keys=True, ensure_ascii=False))


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
class FetchError(Exception):
    def __init__(self, status: str):
        super().__init__(status)
        self.status = status


def http_get(url: str, timeout: int = 40, accept: str = "*/*") -> tuple[bytes, str]:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": accept})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            data = r.read(MAX_DOWNLOAD + 1)
            if len(data) > MAX_DOWNLOAD:
                raise FetchError("too_large")
            return data, r.headers.get("Content-Type", "")
    except urllib.error.HTTPError as e:
        raise FetchError(f"http_{e.code}") from None
    except FetchError:
        raise
    except Exception as e:
        raise FetchError(type(e).__name__) from None


def search(journal_query: str, page: int, size: int = 25) -> list[dict]:
    q = f"({journal_query}) AND OPEN_ACCESS:y AND HAS_FT:y AND LICENSE:cc* AND PUB_YEAR:[2021 TO 2026]"
    params = urllib.parse.urlencode({"query": q, "format": "json", "resultType": "core", "pageSize": size, "page": page})
    try:
        data, _ = http_get(f"{EPMC}?{params}", accept="application/json")
        return json.loads(data)["resultList"]["result"]
    except Exception as e:
        print(f"    ! search failed: {e}")
        return []


def candidate_urls(rec: dict, kind: str, email: str | None) -> list[str]:
    """Ordered download candidates: publisher copies first, aggregator mirrors last."""
    urls: list[str] = []
    for u in (rec.get("fullTextUrlList") or {}).get("fullTextUrl", []):
        if u.get("availabilityCode") in ("OA", "F") and u.get("documentStyle") == kind and u.get("url"):
            urls.append(u["url"])
    urls.sort(key=lambda u: any(h in u for h in ("europepmc.org", "ncbi.nlm.nih.gov")))  # publisher first
    if kind == "pdf":
        if email and rec.get("doi"):
            try:
                data, _ = http_get(f"{UNPAYWALL}{rec['doi']}?email={urllib.parse.quote(email)}", accept="application/json")
                for loc in json.loads(data).get("oa_locations", []):
                    if loc.get("url_for_pdf"):
                        urls.insert(0, loc["url_for_pdf"])
            except Exception:
                pass
        if rec.get("pmcid"):
            urls.append(f"https://europepmc.org/articles/{rec['pmcid']}?pdf=render")
    elif rec.get("doi"):
        urls.append(f"https://doi.org/{rec['doi']}")
    seen, out = set(), []
    for u in urls:
        if u not in seen:
            seen.add(u)
            out.append(u)
    return out


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


def host_of(url: str) -> str:
    return urllib.parse.urlparse(url).netloc.lower()


def cache_path(key: str, kind: str) -> Path:
    return CACHE / f"{key}.{kind}"


def cmd_fetch(a: argparse.Namespace) -> Path:
    rnd = random.Random(a.seed if a.seed is not None else hashlib.sha1(a.name.encode()).hexdigest())
    CACHE.mkdir(parents=True, exist_ok=True)
    state = load_json(STATE, {"seen": []})
    block = load_json(BLOCKLIST, {"urls": {}, "ids": {}})
    corpus = {c["id"]: c for c in load_json(CORPUS, [])}
    seen: set[str] = set(state["seen"]) | set(corpus) | set(block["ids"])
    slugs = a.journals.split(",") if a.journals else list(JOURNALS)
    batch: list[dict] = []
    attempts: list[tuple[str, str, str, str]] = []  # journal, id, host, outcome
    strikes: dict[str, int] = {}
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
            ok_any = False
            for kind in (["pdf", "html"] if a.kinds == "both" else [a.kinds]):
                key_path = cache_path(pid, kind)
                if key_path.exists():
                    ok_any = True
                    batch.append({"id": pid, "kind": kind, "journal": slug})
                    continue
                for url in candidate_urls(rec, kind, a.unpaywall_email):
                    host = host_of(url)
                    if not a.retry_blocked and (url in block["urls"] or strikes.get(host, 0) >= HOST_STRIKES):
                        attempts.append((slug, pid, host, "skipped (blocklist)"))
                        continue
                    time.sleep(0.4)
                    try:
                        data, _ = http_get(url, accept="application/pdf" if kind == "pdf" else "text/html")
                        if not looks_like(data, kind):
                            raise FetchError("not_a_" + kind)
                    except FetchError as e:
                        attempts.append((slug, pid, host, e.status))
                        block["urls"][url] = e.status
                        strikes[host] = strikes.get(host, 0) + 1 if e.status in ("http_403", "http_429") else 0
                        print(f"    - {pid} {kind} {host}: {e.status}")
                        continue
                    strikes[host] = 0
                    key_path.write_bytes(data)
                    attempts.append((slug, pid, host, "ok"))
                    corpus[pid + ":" + kind] = {"id": pid + ":" + kind, "pid": pid, "kind": kind, "journal": slug,
                                                "doi": rec.get("doi"), "title": (rec.get("title") or "")[:140],
                                                "source_url": url}
                    batch.append({"id": pid, "kind": kind, "journal": slug})
                    print(f"    + {key_path.name} ({len(data) / 1e6:.1f} MB) via {host}")
                    ok_any = True
                    break
            seen.add(pid)
            if ok_any:
                done += 1
            else:
                block["ids"][pid] = "no usable url"
    state["seen"] = sorted(seen)
    save_json(STATE, state)
    save_json(BLOCKLIST, block)
    save_json(CORPUS, sorted(corpus.values(), key=lambda c: c["id"]))
    out = DATA / a.name
    out.mkdir(parents=True, exist_ok=True)
    save_json(out / "manifest.json", batch)
    write_fetch_report(a.name, attempts)
    print(f"batch {a.name}: {len(batch)} files (cache: {CACHE})")
    return out


def write_fetch_report(name: str, attempts: list[tuple[str, str, str, str]]) -> None:
    out = REPORTS / name
    out.mkdir(parents=True, exist_ok=True)
    by_host: dict[str, dict[str, int]] = {}
    for _, _, host, res in attempts:
        d = by_host.setdefault(host, {})
        d[res] = d.get(res, 0) + 1
    lines = [f"# Fetch report {name}\n", "| host | outcomes |", "|---|---|"]
    for h, d in sorted(by_host.items()):
        lines.append(f"| {h} | {', '.join(f'{k}: {v}' for k, v in sorted(d.items()))} |")
    (out / "fetch.md").write_text("\n".join(lines) + "\n")


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
        return {"file": path.name, "error": scrub((p.stderr.strip().splitlines() or ["failed"])[-1][:300])}
    try:
        return json.loads(p.stdout.splitlines()[-1])
    except Exception:
        return {"file": path.name, "error": "unparsable worker output"}


def ensure_cached(entry: dict) -> Path | None:
    """Cache path of a corpus entry, downloading it again if the cache was cleaned."""
    path = cache_path(entry["pid"], entry["kind"])
    if path.exists():
        return path
    try:
        data, _ = http_get(entry["source_url"], accept="application/pdf" if entry["kind"] == "pdf" else "text/html")
        if not looks_like(data, entry["kind"]):
            raise FetchError("not_usable")
    except FetchError as e:
        print(f"    ! cannot re-download {entry['id']}: {e.status}")
        return None
    CACHE.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return path


def collect_files(a: argparse.Namespace) -> list[dict]:
    if getattr(a, "corpus", False):
        items = []
        for c in load_json(CORPUS, []):
            if a.journals and c["journal"] not in a.journals.split(","):
                continue
            path = ensure_cached(c)
            if path:
                items.append({"path": path, "journal": c["journal"], "key": c["id"]})
        return items
    if a.dir:
        d = Path(a.dir).resolve()
        if ROOT not in d.parents and d != ROOT:
            print(f"note: {d} is outside the repository; excerpts of its files will appear in the report "
                  "(paths are scrubbed). Do not commit the report if these are private documents.")
        files = sorted(p for p in d.rglob("*") if p.suffix.lower() in (".pdf", ".html", ".htm", ".mhtml", ".mht"))
        return [{"path": f, "journal": f.parent.name, "key": f.name} for f in files]
    manifest = load_json(DATA / a.name / "manifest.json", [])
    return [{"path": cache_path(m["id"], m["kind"]), "journal": m["journal"], "key": f"{m['id']}:{m['kind']}"}
            for m in manifest if cache_path(m["id"], m["kind"]).exists()]


def cmd_run(a: argparse.Namespace) -> None:
    files = collect_files(a)
    out = REPORTS / a.name
    out.mkdir(parents=True, exist_ok=True)
    for old in ("summary.md", "details.md", "results.json"):
        (out / old).unlink(missing_ok=True)
    results = []
    for i, item in enumerate(files, 1):
        f: Path = item["path"]
        print(f"[{i}/{len(files)}] {item['journal']}/{f.name}")
        r = run_one(f, a.timeout)
        r["journal"], r["key"] = item["journal"], item["key"]
        r["file"] = f.name
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
    (out / "summary.md").write_text(scrub("\n".join(lines)) + "\n")
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
    text = scrub("\n".join(detail))
    (out / "details.md").write_text(text[: a.max_kb * 1024])
    (out / "results.json").write_text(scrub(json.dumps(results, indent=0))[: a.max_kb * 2048])
    flagged = sum(1 for r in results if r.get("flags") or "error" in r)
    print(f"\nreport: {out.relative_to(ROOT)}  ({flagged}/{len(results)} files with flags)")


def cmd_stash(a: argparse.Namespace) -> None:
    results = load_json(REPORTS / a.name / "results.json", [])
    scored = sorted(results, key=lambda r: -(len(r.get("flags", [])) + (5 if "error" in r else 0)))
    SAMPLES.mkdir(exist_ok=True)
    used = sum(f.stat().st_size for f in SAMPLES.glob("*"))
    cap = min(a.max_mb, SAMPLES_CAP_MB) * 1024 * 1024
    copied = 0
    for r in scored[: a.worst]:
        key = r.get("key", "")
        pid, _, kind = key.partition(":")
        options = ([cache_path(pid, kind)] if kind else []) + [DATA / a.name / r.get("journal", "") / r["file"]]
        if a.dir:
            options.append(Path(a.dir) / r.get("journal", "") / r["file"])
        f = next((o for o in options if o.exists()), None)
        if f and used + f.stat().st_size <= cap:
            shutil.copy2(f, SAMPLES / f"{a.name}__{r['journal']}__{r['file']}")
            used += f.stat().st_size
            copied += 1
    print(f"copied {copied} files, dev_samples is now {used / 1e6:.1f} MB (cap {cap / 1e6:.0f} MB)")


def cmd_clean(a: argparse.Namespace) -> None:
    """Delete batch folders; the download cache and blocklist survive unless --cache is given."""
    if DATA.exists():
        for d in DATA.iterdir():
            if d.is_dir() and d.name != "cache":
                shutil.rmtree(d)
                print("removed", d.relative_to(ROOT))
    if a.cache and CACHE.exists():
        shutil.rmtree(CACHE)
        print("removed", CACHE.relative_to(ROOT))
    if a.samples and SAMPLES.exists():
        shutil.rmtree(SAMPLES)
        print("removed", SAMPLES.relative_to(ROOT))
    if a.reports and REPORTS.exists():
        shutil.rmtree(REPORTS)
        print("removed", REPORTS.relative_to(ROOT))


def cmd_check(a: argparse.Namespace) -> int:
    """Guard: refuse to commit anything except reports, samples and tool files."""
    def git(*args: str) -> list[str]:
        p = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True)
        return [x for x in p.stdout.splitlines() if x]

    staged = git("diff", "--cached", "--name-only")
    bad = []
    for f in staged:
        path = ROOT / f
        if not f.startswith(COMMIT_ALLOWED):
            bad.append((f, "outside dev_reports/ dev_samples/ dev_tools/"))
        elif path.exists() and path.stat().st_size > SAMPLES_CAP_MB * 1024 * 1024:
            bad.append((f, "larger than the size cap"))
    for f in staged:
        path = ROOT / f
        if path.exists() and path.suffix in (".md", ".json", ".txt") and re.search(r"/(?:home|Users)/\w+", path.read_text(errors="ignore")):
            bad.append((f, "contains a local home-directory path"))
    if bad:
        print("NOT safe to commit:")
        for f, why in bad:
            print(f"  {f}: {why}")
        print("fix with: git restore --staged <file>")
        return 1
    print(f"ok: {len(staged)} staged files, all under {', '.join(COMMIT_ALLOWED)}")
    return 0


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)

    def fetch_args(p):
        p.add_argument("--name", required=True)
        p.add_argument("--journals", help="comma separated slugs (default: all)")
        p.add_argument("--per-journal", type=int, default=1)
        p.add_argument("--kinds", choices=["pdf", "html", "both"], default="pdf")
        p.add_argument("--seed", type=int)
        p.add_argument("--max-page", type=int, default=30)
        p.add_argument("--retry-blocked", action="store_true", help="ignore blocklist.json")
        p.add_argument("--unpaywall-email", help="optional: use Unpaywall to find more PDF locations")

    def run_args(p):
        p.add_argument("--timeout", type=int, default=240)
        p.add_argument("--max-kb", type=int, default=160)

    f = sub.add_parser("fetch", help="download new articles into the cache")
    fetch_args(f)
    r = sub.add_parser("run", help="analyse a batch (or --dir folder)")
    r.add_argument("--name", required=True)
    r.add_argument("--dir")
    r.add_argument("--corpus", action="store_true", help="all articles in corpus.json (re-downloads missing ones)")
    r.add_argument("--journals")
    run_args(r)
    rg = sub.add_parser("regress", help="re-run the whole saved corpus (no new downloads unless the cache is gone)")
    rg.add_argument("--name", required=True)
    rg.add_argument("--journals")
    run_args(rg)
    al = sub.add_parser("all", help="fetch + run")
    fetch_args(al)
    run_args(al)
    st = sub.add_parser("stash", help="copy the worst source files of a report to dev_samples/")
    st.add_argument("--name", required=True)
    st.add_argument("--dir")
    st.add_argument("--worst", type=int, default=3)
    st.add_argument("--max-mb", type=float, default=15)
    c = sub.add_parser("clean", help="delete batch folders (keeps cache + blocklist)")
    c.add_argument("--cache", action="store_true", help="also delete downloaded articles")
    c.add_argument("--samples", action="store_true")
    c.add_argument("--reports", action="store_true")
    sub.add_parser("check", help="verify that staged files are safe to commit")
    o = sub.add_parser("_one")
    o.add_argument("path")
    a = ap.parse_args()
    if a.cmd == "fetch":
        cmd_fetch(a)
    elif a.cmd == "run":
        cmd_run(a)
    elif a.cmd == "regress":
        a.corpus, a.dir = True, None
        cmd_run(a)
    elif a.cmd == "all":
        cmd_fetch(a)
        a.dir, a.corpus = None, False
        cmd_run(a)
    elif a.cmd == "stash":
        cmd_stash(a)
    elif a.cmd == "clean":
        cmd_clean(a)
    elif a.cmd == "check":
        raise SystemExit(cmd_check(a))
    elif a.cmd == "_one":
        print(json.dumps(analyse(Path(a.path))))


if __name__ == "__main__":
    main()
