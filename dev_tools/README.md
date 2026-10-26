# Dev tools (temporary)

Open-access test harness used while tuning the converter. **Remove this folder, `dev_reports/` and
`dev_samples/` before the final release:** `git rm -r dev_tools dev_reports dev_samples`.

## What lives where

| path | committed? | what |
|---|---|---|
| `dev_data/` | **never** (git-ignored) | downloaded articles (`cache/`), local state |
| `dev_tools/blocklist.json` | yes | public URLs / ids that cannot be fetched (403, bot checks), so they are never retried |
| `dev_tools/corpus.json` | yes | the usable articles (public ids + URLs) so the same set can be re-run any time |
| `dev_reports/<batch>/` | yes | small text reports (summary, details, fetch outcome) |
| `dev_samples/` | yes, size-capped | a few problematic source PDFs for debugging |

The tool only writes to those places; paths of the local machine are scrubbed from every report, and
`check` refuses staged files outside `dev_reports/ dev_samples/ dev_tools/`.

## Commands

```bash
python dev_tools/oa_harness.py all --name b3                 # fetch new articles (PDF) + convert + report
python dev_tools/oa_harness.py regress --name r1             # re-run the whole saved corpus; downloads only what is missing
python dev_tools/oa_harness.py stash --name b3 --worst 3     # copy the worst source files to dev_samples/ (cap 25 MB)
python dev_tools/oa_harness.py check                         # are the staged files safe to commit?
python dev_tools/oa_harness.py clean                         # drop batch folders, keep cache + blocklist
python dev_tools/oa_harness.py clean --cache --samples       # also forget downloaded files / samples
```

Useful switches for `fetch` / `all`: `--journals plos_one,sci_rep`, `--per-journal 2`, `--kinds pdf|html|both`,
`--retry-blocked`, `--unpaywall-email you@example.org` (finds extra PDF locations via Unpaywall).

Hosts that answer 403/429 three times in a row are skipped for the rest of the run.
