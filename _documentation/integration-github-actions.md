# Integration: GitHub Actions

**Status:** Design / not yet implemented. This documents the target design for
moving the exhibit importer off a maintainer's laptop and onto GitHub Actions,
plus a companion workflow for the Illustrator space-plan CSVs.

Related: [Exhibit Pipeline](exhibit-pipeline.md) · [Image Storage](image-storage.md) ·
script [`_python/update_exhibits.py`](../_python/update_exhibits.py)

---

## Why Actions (and not Azure Functions)

The importer is **stateful, and its state is the git repo itself**:

- Incremental skip logic reads existing `_exhibits/*.md` and compares
  `last-exported` against JotForm's `updated_at`.
- Image processing only downloads/resizes when the file isn't already on disk
  (`path.exists`).
- The output *is* a git commit.

A GitHub Action checks out the repo, so all of that "compare against what's
already there" logic works unchanged: run the script, then commit. Azure
Functions are stateless/ephemeral (you'd have to clone the repo every run),
carry a 5–10 min consumption-plan timeout that a full image rebuild can exceed,
and add secrets/deployment plumbing — reimplementing for cost what Actions gives
free. The only thing a Function would add is a webhook endpoint for near-real-time
triggers; see [Future: webhook trigger](#future-webhook-trigger).

---

## Workflows

| Workflow | File | Trigger | Output |
|---|---|---|---|
| Exhibit importer | `.github/workflows/import-exhibits.yml` | manual (`workflow_dispatch`), optional `schedule` | commits generated `_exhibits/*.md`, `_categories/*.md`, `_includes/category-options.html`, images |
| Invoice sync + treasurer notice | `.github/workflows/sync-invoices.yml` | after import (`workflow_call`), nightly `schedule`, manual | creates PayPal **draft** invoices, syncs fee status to JotForm, emails `treasurer@themakereffect.org` when invoices need sending — **no commit** |
| Space-plan CSVs | `.github/workflows/space-plan-csv.yml` | manual only | uploads the four CSVs as run **artifacts** (no commit) |

Keeping the space-plan CSVs separate matters: they are internal Illustrator
inputs with nothing to do with the published site, so they must not trigger site
commits. Invoice sync is separated because it touches money (live PayPal) and
carries its own safety rules — see [Workflow 3](#workflow-3--invoice-sync--treasurer-notification).

---

## Script refactors required first

These are prerequisites; the workflows assume them.

1. **Secret from env.** Read the JotForm key from `os.environ["JOTFORM_API_KEY"]`,
   falling back to `private.yaml` for local runs. `private.yaml` stays gitignored
   and out of CI.
2. **🔴 Remove the API-key print.** The script currently prints the token to
   stdout — in CI that leaks the secret into logs. Delete it before this runs in
   Actions.
3. **Separate CSV generation.** Today the CSV block lives inside `export()`,
   gated on whether exhibits changed. Split it behind a flag so each workflow runs
   exactly one job:
   - `--no-csv` (or default) — importer path, skip CSV writing.
   - `--csv-only` — build only the space-plan CSVs, write nothing else, make no
     commits.
4. **Working directory.** The `../` relative paths assume `cwd = _python/`; the
   workflows set `working-directory: _python`.
5. **Resilience (recommended, can follow later).** A single missing JotForm field
   hits `except: sys.exit(1)`, and network calls (JotForm, YouTube oembed, image
   downloads) have no retry. For unattended runs, add light retry and avoid
   hard-exiting on one bad record so a transient hiccup doesn't fail the whole run.

### Dependencies

```
pyyaml
python-slugify
pillow
requests
git+https://github.com/jotform/jotform-api-python.git
```

Pin these in `_python/requirements.txt` so CI installs are reproducible.

---

## Secrets

Store as repository secrets (Settings → Secrets and variables → Actions):

- `JOTFORM_API_KEY` — the JotForm API key currently in `private.yaml`.
- `PAYPAL_CLIENT_ID` / `PAYPAL_CLIENT_SECRET` — **live** PayPal credentials
  (invoice sync only). Because these move money, scope who can trigger that
  workflow — see [Workflow 3 safety rules](#safety-rules-financial).
- Email delivery for the treasurer notice (invoice sync only) — one of:
  - a transactional-email API key (e.g. `SENDGRID_API_KEY` / `RESEND_API_KEY` /
    AWS SES creds) — **recommended**, most reliable from CI; or
  - SMTP creds (`MAIL_USERNAME` / `MAIL_PASSWORD`) for a Google Workspace app
    password if you prefer SMTP.

Committing back (importer only) uses the built-in `GITHUB_TOKEN` (needs
`contents: write`); no PAT required since we push to the same repo. Invoice sync
and CSV workflows need no `contents` write permission.

---

## Workflow 1 — Exhibit importer

```yaml
# .github/workflows/import-exhibits.yml
name: Import Exhibits

on:
  workflow_dispatch:
    inputs:
      rebuild:
        description: "Rebuild all exhibits (ignore incremental skip)"
        type: boolean
        default: false
  # Optional — enable once trusted. Conservative cadence.
  # schedule:
  #   - cron: "0 12 * * *"   # daily at 12:00 UTC

permissions:
  contents: write

concurrency:
  group: import-exhibits
  cancel-in-progress: false

jobs:
  import:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        # Full working tree is required so the incremental skip logic and
        # "image already on disk" checks see previously generated files.

      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: pip

      - name: Install dependencies
        working-directory: _python
        run: pip install -r requirements.txt

      - name: Run importer
        working-directory: _python
        env:
          JOTFORM_API_KEY: ${{ secrets.JOTFORM_API_KEY }}
        run: |
          if [ "${{ inputs.rebuild }}" = "true" ]; then
            python update_exhibits.py --no-csv -o rebuild
          else
            python update_exhibits.py --no-csv
          fi

      - name: Commit generated content
        run: |
          git config user.name  "mfo-importer[bot]"
          git config user.email "importer@makerfaireorlando.com"
          git add _exhibits _categories _includes/category-options.html assets/images/exhibit-images
          if git diff --cached --quiet; then
            echo "No changes to commit."
          else
            git commit -m "Update exhibits from JotForm ($(date -u +%Y-%m-%d))"
            git push
          fi
```

Notes:
- Triggered by dispatch/cron, so pushing back cannot loop into re-triggering.
- The commit step is a no-op when nothing changed (the incremental logic keeps
  diffs minimal), so scheduled runs stay quiet on quiet days.
- `date` in the commit message runs in the shell (UTC), avoiding the script's
  own timestamp handling.

---

## Workflow 2 — Space-plan CSVs

```yaml
# .github/workflows/space-plan-csv.yml
name: Space Plan CSVs

on:
  workflow_dispatch:

jobs:
  csv:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: pip

      - name: Install dependencies
        working-directory: _python
        run: pip install -r requirements.txt

      - name: Build CSVs
        working-directory: _python
        env:
          JOTFORM_API_KEY: ${{ secrets.JOTFORM_API_KEY }}
        run: python update_exhibits.py --csv-only

      - name: Upload CSVs
        uses: actions/upload-artifact@v4
        with:
          name: space-plan-csv
          path: |
            _python/curiosity.csv
            _python/spirit.csv
            _python/opportunity.csv
            _python/maker-tent.csv
```

No `contents: write`, no commit — you download the CSVs from the run's Artifacts
section when you need them for Illustrator.

---

## Workflow 3 — Invoice sync & treasurer notification

Replaces [`_python/generate_invoices.py`](../_python/generate_invoices.py).

### What the script does

For each **visible** JotForm submission whose `feeStatus` is `Fee Not Invoiced`
or `Fee Due`, it reconciles the maker's fee against **PayPal Invoicing**:

1. Authenticates to PayPal (**live** API, `https://api-m.paypal.com`).
2. Searches PayPal for invoice `MFO-<exhibitID>`.
   - **not-found** → creates a **draft** invoice ($150 seller fee, or the Ruckus
     registration fee). It does *not* send it — a human sends it from PayPal.
   - **DRAFT** → flags "needs to be sent."
   - **SENT** → updates JotForm `feeStatus` → `Fee Due`.
   - **PAID** → updates JotForm `feeStatus` → `Fee Paid`.
3. Prints reconciliation stats.

### Why it's a good Actions fit

Unlike the importer, this script is **stateless with respect to the repo** — it
reads/writes JotForm and PayPal over their APIs and writes nothing to disk. So
there's no checkout-for-state and **no commit**; it's pure API orchestration,
which is exactly what a scheduled Action does well. It's also largely
**idempotent** (it searches before creating, so re-runs don't duplicate), which
makes a nightly cron safe.

### Triggers — "on import, and nightly"

Author it as a **reusable** workflow (`workflow_call`) so both entry points share
one definition:

- The **importer** calls it as a downstream job (`needs: import`), so invoices
  reconcile right after exhibits refresh.
- A **nightly `schedule`** catches payment-status changes (SENT→PAID) with no
  human action.
- `workflow_dispatch` for manual runs.

Add to `import-exhibits.yml`:

```yaml
  invoices:
    needs: import
    uses: ./.github/workflows/sync-invoices.yml
    secrets: inherit
```

### The treasurer notification

"Invoices that need to be sent" = the set of PayPal **drafts** (both newly
created and pre-existing `DRAFT`s). Design:

1. Refactor the script to **accumulate** those into a list (exhibit ID, exhibit
   name, maker name, email, fee) instead of only printing "LOGIN TO PAYPAL AND
   SEND", and write it to `_python/invoices-to-send.md` (plus a count on stdout /
   `$GITHUB_OUTPUT`).
2. A workflow step emails `treasurer@themakereffect.org` **only when the list is
   non-empty** — so quiet nights send nothing.

Recommended: send via a transactional-email API (SendGrid/Resend/SES) for
reliability from CI. Simple alternative using SMTP:

```yaml
      - name: Email treasurer if invoices need sending
        if: steps.sync.outputs.needs_sending != '0'
        uses: dawidd6/action-send-mail@v3
        with:
          server_address: smtp.gmail.com
          server_port: 465
          username: ${{ secrets.MAIL_USERNAME }}
          password: ${{ secrets.MAIL_PASSWORD }}
          from: Maker Faire Orlando <${{ secrets.MAIL_USERNAME }}>
          to: treasurer@themakereffect.org
          subject: "[MFO] ${{ steps.sync.outputs.needs_sending }} invoice(s) need sending"
          html_body: file://_python/invoices-to-send.md
```

> PayPal *can* auto-send via `POST /v2/invoicing/invoices/{id}/send`. We
> deliberately keep the human-send step and just notify — safer for a money flow,
> and it preserves the treasurer's review. Auto-send is a future option, not this
> design.

### Script refactors specific to this workflow

In addition to the shared "secret-from-env" change:

1. **Secrets from env** — `JOTFORM_API_KEY`, `PAYPAL_CLIENT_ID`,
   `PAYPAL_CLIENT_SECRET` from `os.environ`, `private.yaml` fallback for local.
2. **Collect the drafts list** and write `invoices-to-send.md` + emit a
   `needs_sending` count (see above).
3. **`--dry-run` mode** — hit PayPal search/read but skip create/send and skip
   JotForm edits. Essential for testing a money flow in CI without side effects.
4. **Proper exit codes** — today an unknown invoice type does `sys.exit(0)`
   (silent success) and errors are only printed; a failed PayPal/JotForm call
   should fail the job so it surfaces.
5. **Remove/park the hardcoded hack** — `if (mfoID == "24-30"): mfoID="24-30-2"`
   is stale per-year data massaging that shouldn't live in an automated run.
6. **Drop ANSI color** (or gate it on a TTY) — the escape codes are noise in
   Actions logs.

### Sample workflow

```yaml
# .github/workflows/sync-invoices.yml
name: Sync Invoices

on:
  workflow_call:      # invoked by import-exhibits.yml
  workflow_dispatch:  # manual
  schedule:
    - cron: "0 6 * * *"   # nightly ~06:00 UTC (after any imports)

permissions:
  contents: read

concurrency:
  group: sync-invoices          # serialize: never create invoices twice at once
  cancel-in-progress: false

jobs:
  sync:
    runs-on: ubuntu-latest
    # environment: treasury      # optional: require-reviewer gate on the money flow
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: pip
      - name: Install dependencies
        working-directory: _python
        run: pip install -r requirements.txt
      - name: Reconcile invoices
        id: sync
        working-directory: _python
        env:
          JOTFORM_API_KEY:      ${{ secrets.JOTFORM_API_KEY }}
          PAYPAL_CLIENT_ID:     ${{ secrets.PAYPAL_CLIENT_ID }}
          PAYPAL_CLIENT_SECRET: ${{ secrets.PAYPAL_CLIENT_SECRET }}
        run: python generate_invoices.py   # writes invoices-to-send.md, sets needs_sending
      - name: Email treasurer if invoices need sending
        if: steps.sync.outputs.needs_sending != '0'
        uses: dawidd6/action-send-mail@v3
        with:
          server_address: smtp.gmail.com
          server_port: 465
          username: ${{ secrets.MAIL_USERNAME }}
          password: ${{ secrets.MAIL_PASSWORD }}
          from: Maker Faire Orlando <${{ secrets.MAIL_USERNAME }}>
          to: treasurer@themakereffect.org
          subject: "[MFO] ${{ steps.sync.outputs.needs_sending }} invoice(s) need sending"
          html_body: file://_python/invoices-to-send.md
```

### Safety rules (financial)

This workflow moves real money, so it gets guardrails the others don't need:

- **Serialize** with a `concurrency` group so the nightly run and an
  import-triggered run can't double-create invoices.
- **Restrict triggering.** Consider a GitHub **Environment** (`treasury`) with
  required reviewers on `workflow_dispatch`, and limit who can run it.
- **Keep secrets as live PayPal credentials** — never commit them; they only
  exist as Actions secrets.
- **Test with `--dry-run`** before enabling the schedule.
- **Idempotency is load-bearing** — the search-before-create check is what makes
  re-runs safe; keep it, and fail loudly if a search errors rather than falling
  through to create.

---

## Interaction with the image-storage plan

Until images move out of git ([Image Storage](image-storage.md)), Workflow 1
commits image binaries and the repo keeps growing. The two efforts pair well:
once the importer uploads resized images to an external store + CDN, Workflow 1
commits **only** the generated Markdown/HTML, and the `assets/images/exhibit-images`
line drops out of the commit step. Sequence-wise, migrating to Actions and moving
images can land together.

---

## Yearly maintenance

`eventYear`, `formCFM`, and `formRuckus` are hardcoded near the top of **both**
scripts and must be bumped each year before the first run (see
[Exhibit Pipeline](exhibit-pipeline.md)). Note the two scripts even disagree on
the Ruckus form title (`"MFO2026 - Ruckus - CFM"` in the importer vs
`"CFM - Ruckus - MFO2026"` in the invoicer) — reconcile these. Consider promoting
all of them to repo variables so a new year doesn't require code edits in two
places.

---

## Future: webhook trigger

If near-real-time updates are ever wanted: JotForm supports webhooks. The clean
pattern is JotForm webhook → a tiny relay (small Azure Function or similar) →
fires a GitHub `repository_dispatch` → Workflow 1 runs. Not needed for now;
manual `workflow_dispatch` (plus optional daily cron) covers the use case.

---

## Open decisions

- Enable the `schedule` cron, or keep it manual-only to start?
- Move `eventYear` / form titles to workflow inputs or repo variables (and
  reconcile the mismatched Ruckus form title between the two scripts)?
- Land the image-storage migration in the same pass, or Actions first then images?
- How much resilience hardening (retry/skip-bad-record) to include in the initial
  cut vs. as a follow-up.
- **Invoice sync:** which email path — transactional API (recommended) vs SMTP
  app password?
- **Invoice sync:** gate the money flow behind a protected `treasury` Environment
  with required reviewers, or trust repo-secret access control?
- **Invoice sync:** ever auto-send invoices via PayPal's `/send` endpoint, or keep
  the human-in-the-loop send step permanently?
