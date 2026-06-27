# Architecture

How the Maker Faire Orlando site is put together and how a page is produced.
For running it, see [Build & Deploy](build-deploy.md).

---

## Big picture

```
Markdown pages  ─┐
Collections      │
(_exhibits,      ├──►  Jekyll (Liquid templating)  ──►  _site/  ──►  GitHub Pages
 _categories)    │      + plugins (SEO, sitemap)
YAML data        │
(_data/*.yaml)  ─┘
```

- **No server, no database.** Everything is rendered to static HTML at build time.
  GitHub Pages runs the build automatically on push (see [Build & Deploy](build-deploy.md)).
- **Liquid** is the templating language. Pages and includes use `{% ... %}` tags
  and `{{ ... }}` output. Data files and front matter feed values in.
- **Three plugins** (declared in `_config.yml`): `jekyll-seo-tag`,
  `jekyll-redirect-from`, `jekyll-sitemap`.

---

## Base theme + the redesign layer

The site started as a Jekyll port of the **old Maker Faire Global
"minimakerfaire" WordPress theme**, on top of the `jekyll-theme-minimal` base
and **Bootstrap 3.3.7** (loaded from a CDN).

CSS loads in a deliberate order in [`_includes/stylesheets.html`](../_includes/stylesheets.html):

1. Bootstrap 3.3.7 (CDN) + Bootstrap theme
2. `assets/css/mfo-style.css` — small set of legacy custom overrides
3. `assets/css/minimakerfaire-style.css` — the large (~29k line) ported theme
4. Google Fonts (Archivo + Inter, added in the redesign)
5. **`assets/css/mfo-redesign.css` — loaded LAST so it overrides everything above**

> The redesign is intentionally **additive**: it re-skins the legacy theme through
> one override stylesheet built on CSS custom properties, rather than rewriting
> the old CSS. To roll back, remove the `mfo-redesign.css` link. Full rationale,
> design tokens, and task list live in **[Redesign 2026](redesign-2026.md)**.

Font Awesome 6.7.2 is loaded in [`_includes/head.html`](../_includes/head.html)
for brand/social icons.

---

## How a page renders

1. A file (e.g. [`pages/volunteer.md`](../pages/volunteer.md)) declares a `layout`
   and a `permalink` in its YAML front matter.
2. Jekyll wraps the page's body in that layout from `_layouts/`.
3. Layouts pull in shared partials from `_includes/` — `head.html`, `topnav.html`,
   `footer.html`, `scripts.html`, etc.
4. Liquid resolves data references (`site.data.settings.*`, `site.exhibits`, …) and
   emits HTML into `_site/`.

### Layouts (`_layouts/`)

| Layout | Used for |
|---|---|
| `default.html` | Standard content pages — nav, optional carousel, content, footer. |
| `full-width.html` | Full-bleed pages (homepage, restyled exhibit/volunteer pages). |
| `category.html` | Exhibits index and category pages — loops `site.exhibits` into an Isotope card grid. |
| `exhibit.html` | A single exhibit detail page. |
| `schedule.html` / `schedule-app.html` | Event schedule views driven by `_data/schedule.yaml`. |
| `table-signs.html` | Printable per-exhibit table signs (not indexed). |
| `redirect.html` | Support for redirects. |

The `default`, `category`, and `schedule` layouts share the same skeleton:
`head` → `flag-banner` → `topnav` → optional `carousel` → page body → `footer` →
`scripts` → `optional-js`.

### Key includes (`_includes/`)

- **Chrome:** `head.html`, `topnav.html`, `footer.html`, `stylesheets.html`,
  `scripts.html`, `analytics.html`, `facebook-pixel.html`.
- **Homepage sections:** `carousel.html` (hero), `what-is-maker-faire.html`,
  `category-cards.html`, `get-involved-cards.html`, `cta-panel-widget.html`,
  `sponsors-marquee.html`.
- **Exhibits:** `exhibit-card.html`, `exhibits-header.html`, `category-options.html`.
- **Sponsors:** `sponsors-grid-modern.html`, `sponsors-grid.html`,
  `sponsors-carousel.html`, `sponsors-marquee.html`.
- **Dates:** `date-event.html`, `date-edu.html` and `-short` variants compute the
  human-readable event dates from `_data/settings.yaml`.
- **Conditional notices:** `update-warning.html` (the "this page isn't updated for
  the current year yet" banner, gated by settings flags).

Most includes are **data-driven** — they read from `site.data.*` and the settings
flags rather than hard-coded content. See [Data Files](data-files.md) and
[Settings](settings.md).

---

## Content sources, at a glance

| Source | Drives |
|---|---|
| `pages/*.md`, `index.md` | Hand-authored content pages. See [Content Authoring](content-authoring.md). |
| `_exhibits/`, `_categories/` | Exhibit + category collections. See [Collections](collections.md). |
| `_data/*.yaml` | Nav, footer, sponsors, schedule, CTAs, settings. See [Data Files](data-files.md). |
| `_data/settings.yaml` | The master switchboard. See [Settings](settings.md). |
| `_python/update_exhibits.py` | Regenerates `_exhibits/` from JotForm. See [Exhibit Pipeline](exhibit-pipeline.md). |

---

## JSON exports

Two pages emit JSON instead of HTML for external consumers (e.g. the Maker Faire
Global maker directory and schedule apps):

- [`pages/makers-json.json`](../pages/makers-json.json) → `/makers-json/` — every
  exhibit, looped through `smartify` + `jsonify`.
- [`pages/schedule-json.json`](../pages/schedule-json.json) → `/schedule-json/` —
  the schedule data file as JSON.

These are relatively expensive to render, so the dev config excludes them — see
[Build & Deploy](build-deploy.md).

---

## SEO, analytics & redirects

- **SEO:** `jekyll-seo-tag` (`{% seo %}` in `head.html`) reads `title`,
  `description`, `image`, and per-page front matter. Site-wide defaults are set in
  `_config.yml`.
- **Sitemap:** `jekyll-sitemap` auto-generates `/sitemap.xml`. Assets are excluded
  from it via `_config.yml` `defaults`.
- **Redirects:** `jekyll-redirect-from` — add `redirect_from:` in a page's front
  matter to create alias URLs (e.g. `/makers/` → `/exhibits/`).
- **Analytics + pixels:** Google Analytics and the Facebook pixel only render when
  `jekyll.environment == 'production'` (i.e. on the GitHub Pages build), so local
  previews don't pollute analytics.