# Dev tools (temporary)

Open-access test harness used while tuning the converter. **Remove this folder, `dev_reports/` and
`dev_samples/` before the final release** (`git rm -r dev_tools dev_reports dev_samples`).

Articles are downloaded into `dev_data/` (git-ignored, never committed). Only small text reports go
to `dev_reports/<batch>/` and, optionally, a few problematic source files to `dev_samples/` (hard size cap).

```bash
python dev_tools/oa_harness.py all --name b1            # fetch + convert + report
python dev_tools/oa_harness.py fetch --name b2 --per-journal 2 --journals plos_one,sci_rep
python dev_tools/oa_harness.py run --dir dev_data/b2 --name b2
python dev_tools/oa_harness.py stash --name b2 --max-mb 15   # copy the worst source files to dev_samples/
python dev_tools/oa_harness.py clean                      # delete downloaded articles and old samples
```
