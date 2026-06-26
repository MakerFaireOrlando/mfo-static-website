# Exhibit Pipeline

The ~290 files in `_exhibits/` and the pages in `_categories/` are **generated**
from JotForm submissions by a Python script. This is the one part of the site you
don't author by hand.

**Script:** [`_python/update_exhibits.py`](../_python/update_exhibits.py)

> ⚠️ Hand-edits to files in `_exhibits/` are overwritten the next time the
> importer runs. Fix data at the source (the JotForm submission) and re-run.

---

## What it does

For each call-for-makers submission it:

1. Pulls submissions from **JotForm** via the JotForm API.
2. Reads two forms by title — the main Call for Makers and the Robot Ruckus
   (combat-robots) form. These titles are set at the top of the script:
   ```python
   eventYear  = 2025
   formCFM    = "Call For Makers MFO2025"
   formRuckus = "MFO2025 - Ruckus - CFM"
   ```
   **Update these for the new year before running.**
3. Downloads each submission's images, then **resizes** them into the responsive
   variants (`full` / `large` / `medium` / `small`) using Pillow.
4. Slugifies titles into stable URLs.
5. Writes one Markdown file per exhibit into `_exhibits/` (front matter described
   in [Collections](collections.md)), and exports the set of categories.

It also tallies counts (submissions, visible, removed, Field Trip Day) and can
build space-plan data.

> **Known quirk — `full` is unreliable, especially for additional images.**
> Each image's front matter lists a `full:` URL, but the importer frequently
> doesn't actually emit the `-full.png` file for *additional* images (only
> `small`/`medium`/`large` land on disk). Linking to `image.full.url` therefore
> 404s, so templates use **`large`** for additional images (e.g. the exhibit
> photo gallery / lightbox in `_layouts/exhibit.html`). A true full-resolution
> lightbox would require fixing the importer to always export the `full`
> variant.

---

## Credentials — `private.yaml`

The script needs a JotForm API key, read from `_python/private.yaml`:

```yaml
jotform-api-key: <your-jotform-api-key>
```

This file is **gitignored** (along with the generated CSVs and temp images) — it
must never be committed. If it's missing the script exits with
`Error: Cannot locate settings file`.

> JotForm note: in the account settings, image uploads must be viewable without
> login or the image downloads will fail (noted in the script's comments).

---

## Setup

The dependencies are in [`_python/requirements.txt`](../_python/requirements.txt):
`requests`, `jotform`, `pillow`, `python-slugify`, `pyyaml`.

```powershell
cd _python
pip install -r requirements.txt
```

> The vanilla `pip install jotform` historically didn't support Python 3; the
> script header documents installing it from GitHub if you hit issues:
> `pip install git+https://github.com/jotform/jotform-api-python.git`

---

## Running it

```powershell
cd _python
python update_exhibits.py            # normal run
python update_exhibits.py -o option  # outputAll — include everything
python update_exhibits.py --help     # usage
```

Or via Docker (no local Python needed) — defined in
[`docker-compose.yml`](../docker-compose.yml):

```powershell
docker compose up update-exhibits
```

That service `pip install`s the requirements and runs the script inside
`/site/_python/`.

---

## After running

1. Review the diff in `_exhibits/` and `_categories/` — confirm new exhibits look
   right and no good data was dropped.
2. Preview with a **full** build so images resolve
   (`bundle exec jekyll serve` — see [Build & Deploy](build-deploy.md); the fast
   preview skips exhibit images).
3. Flip exhibit-display settings when appropriate — e.g.
   `maker_exhibits_holdover` off once the new year is imported, and
   `maker_exhibits_show_location` on once booth/space numbers are final. See
   [Settings](settings.md).
4. Commit the generated files.

---

## Other scripts in `_python/`

The folder also holds related event tooling (ticket/invoice generation, counts,
space-plan updates), e.g. `generate_maker_tickets.py`, `generate_invoices.py`,
`the_count.py`, `space_plan_update.py`. These are operational utilities run
ad-hoc; `update_exhibits.py` is the one that feeds the website.

---

### See also
- [Collections](collections.md) — the exhibit/category front-matter shape this produces.
- [Settings](settings.md) — flags that control how imported exhibits display.
