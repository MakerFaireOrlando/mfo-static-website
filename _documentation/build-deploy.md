# Build & Deploy

How to run the site locally and how it gets published.

---

## Prerequisites

You need **Ruby + Bundler** (the gems are pinned via the
[`Gemfile`](../Gemfile) / `Gemfile.lock`). The key gem is `github-pages`, which
locks the whole toolchain to the exact versions GitHub Pages runs in production —
so a clean local build closely matches the deployed site.

If you'd rather not install Ruby, use **Docker** (see below).

```powershell
bundle install
```

---

## Running locally

### Fast preview (recommended day-to-day)

```powershell
.\serve-fast.ps1                 # → http://localhost:4000
.\serve-fast.ps1 --port 4001     # extra args are forwarded to jekyll
```

This layers [`_config_dev.yml`](../_config_dev.yml) on top of
[`_config.yml`](../_config.yml). The dev config **excludes the bulk image assets
and the JSON exports** so builds are quick:

- `assets/images/exhibit-images` — ~4,000 files / ~273 MB that Jekyll otherwise
  re-copies into `_site/` on **every** build.
- `pages/makers-json.json` + `pages/schedule-json.json` — together ~5s of Liquid
  rendering (they loop every exhibit/event through `smartify` + `jsonify`).

> **Trade-off:** exhibit images **404** in the fast preview, and the JSON
> endpoints aren't generated. That's expected. Working on images or the JSON
> feeds? Do a full build instead (below).

The raw command, if you don't want the script:

```powershell
bundle exec jekyll serve --config _config.yml,_config_dev.yml
```

### Full build (all assets)

```powershell
bundle exec jekyll serve     # serve with everything
bundle exec jekyll build     # just build into _site/
```

Uses `_config.yml` only — exactly what production builds. A full build takes
noticeably longer (the redesign doc notes ~40s+).

---

## Running with Docker

No Ruby needed — [`docker-compose.yml`](../docker-compose.yml) defines three
services (image: `bretfisher/jekyll-serve`):

```powershell
docker compose up jekyll-dev      # fast build (mirrors serve-fast.ps1) → :4000
docker compose up jekyll          # full build with all assets → :4000
docker compose up update-exhibits # runs the Python exhibit importer (see below)
```

`jekyll-dev` passes `--config _config.yml,_config_dev.yml`, so it has the same
fast-build trade-offs as `serve-fast.ps1`.

---

## Deploy (GitHub Pages)

Production publishing is GitHub Pages' built-in Jekyll build (there is **no**
Actions workflow involved in production — the Netlify workflow below is only for
branch previews):

1. Push to the branch GitHub Pages is configured to serve (the default branch,
   **`master`**).
2. GitHub Pages installs the `github-pages` gem set and runs `jekyll build` with
   `_config.yml` (production — `jekyll.environment == 'production'`, so analytics
   and the Facebook pixel render).
3. The generated `_site/` is served at the custom domain.

### Domain & verification files

- [`CNAME`](../CNAME) → `www.makerfaireorlando.com` (the custom domain).
- [`.well-known/`](../.well-known/) (BIMI logo, security files) is force-included
  via `include: [".well-known"]` in `_config.yml` — directories starting with `.`
  are otherwise skipped.
- `assets/**` is excluded from the sitemap via `_config.yml` `defaults`.

### Branches

- `master` — production (what GitHub Pages serves).
- `redesign` — the in-progress 2026 rebrand. See [Redesign 2026](redesign-2026.md).

---

## Preview deploys (Netlify via GitHub Actions)

To share a branch (e.g. `redesign`) without touching the live GitHub Pages site,
[`.github/workflows/netlify-preview.yml`](../.github/workflows/netlify-preview.yml)
builds the site on GitHub's runners and pushes the output to a Netlify site.

**Why build in Actions instead of letting Netlify do it:** Netlify clones the
*full* git repo, and this repo's history is several GB (years of binary image
churn). The Actions `checkout` is **shallow** (`fetch-depth: 1`), so it pulls
only the current tree (~284 MB) — far cheaper. GitHub also doesn't support Ruby
in its own Static Web Apps-style builder; doing it here keeps full control.

The workflow: shallow checkout → `ruby/setup-ruby` (version from `.ruby-version`;
`Gemfile.lock` is gitignored so gems resolve fresh for Linux) → `bundle exec
jekyll build` (full `_config.yml`, `JEKYLL_ENV=production`, `PAGES_REPO_NWO` set
so the github-pages metadata plugin works) → `nwtgck/actions-netlify` deploys
`_site/`. Triggers on push to `redesign` and manual `workflow_dispatch`.

### One-time setup

1. Create a Netlify site **not connected to git** (so Netlify doesn't also try to
   build): Netlify dashboard *Add new site → Deploy manually* (drop any folder
   once to create it), or `netlify sites:create --name mfo-redesign`.
2. Grab two values:
   - **Auth token** — Netlify *User settings → Applications → Personal access
     tokens → New access token*.
   - **Site API ID** — the site's *Site configuration → General → Site
     information → API ID*.
3. Add them as GitHub repo secrets (*Settings → Secrets and variables →
   Actions*): `NETLIFY_AUTH_TOKEN` and `NETLIFY_SITE_ID`.
4. Push to `redesign` (or run the workflow manually). The shared URL is the
   Netlify site's primary URL (rename it under *Site configuration* to e.g.
   `mfo-redesign.netlify.app`).

> Public repo → GitHub Actions minutes are free. The build/deploy runs a few
> minutes (mostly the ~300 MB asset upload); no Netlify build minutes are used
> since Netlify only receives the finished `_site/`.

---

## Build gotchas

- **Don't enable `incremental`.** It's commented out in `_config.yml` — it caused
  stale/broken builds locally.
- **`Gemfile.lock` is gitignored.** It's regenerated by `bundle install`; the
  `github-pages` gem keeps versions aligned with production regardless.
- **Long Windows paths:** `.gitconfig` sets `core.longpaths = true` because some
  exhibit image filenames are long.
- **`_site/` is generated** and gitignored — never edit it by hand.

---

### See also
- [Architecture](architecture.md) — what the build actually assembles.
- [Exhibit Pipeline](exhibit-pipeline.md) — the separate Python step that
  generates exhibit content before a build.
