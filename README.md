# Maker Faire Orlando — Website

The source for **[www.makerfaireorlando.com](https://www.makerfaireorlando.com)**.

It's a [Jekyll](https://jekyllrb.com/) static site, hosted on **GitHub Pages**, and
produced by **The Maker Effect Foundation**. Content is driven by a mix of
Markdown pages, Jekyll collections (exhibits, categories, sponsors), and YAML
data files, with most year-to-year behavior toggled from a single settings file.

---

## Quick start

```powershell
# 1. Install Ruby + Bundler, then install gems
bundle install

# 2. Serve a fast local preview (skips the ~4,000 exhibit images)
.\serve-fast.ps1            # → http://localhost:4000

# …or a full build with all assets
bundle exec jekyll serve
```

No Ruby? Use Docker instead — `docker compose up jekyll-dev` (fast) or
`docker compose up jekyll` (full). See **[Build & Deploy](_documentation/build-deploy.md)**.

> The fast preview intentionally 404s on exhibit images — that's expected.
> Full details and the why are in the build doc.

---

## The 5-minute mental model

- **Static site.** There is no server or database. `jekyll build` turns Markdown +
  data + templates into plain HTML in `_site/`, which GitHub Pages serves.
- **One settings file runs the year.** `_data/settings.yaml` holds the event year,
  dates, and the feature flags that open/close the call-for-makers, volunteer
  signup, homepage promos, and "page not updated yet" warnings.
- **Exhibits are generated, not hand-written.** The ~290 files in `_exhibits/` are
  produced by a Python script that pulls from JotForm. You normally don't edit
  them by hand. See **[Exhibit Pipeline](_documentation/exhibit-pipeline.md)**.
- **The look is mid-redesign.** A 2026 rebrand is layered on top of the legacy
  theme via a single override stylesheet. See
  **[Redesign 2026](_documentation/redesign-2026.md)**.

---

## Repository layout

| Path | What it is |
|---|---|
| `_config.yml` | Main Jekyll config (theme, plugins, collections, SEO). |
| `_config_dev.yml` | Local-only overrides that speed up builds. |
| `_data/` | YAML data: `settings.yaml`, `menus.yaml`, `sponsors.yaml`, `schedule.yaml`, … |
| `_exhibits/` | **Generated** exhibit collection (one `.md` per exhibit). |
| `_categories/` | Exhibit category pages (one `.md` per category). |
| `_layouts/` | Page templates (`default`, `category`, `schedule`, `exhibit`, …). |
| `_includes/` | Reusable HTML/Liquid partials (nav, footer, cards, carousels). |
| `_documentation/` | **These docs.** Internal-only; not published to the site. |
| `_python/` | Tooling — chiefly the JotForm → exhibits importer. |
| `pages/` | Hand-authored content pages (attend, volunteer, sponsors, schedule…). |
| `assets/` | CSS, JS, images, PDFs. |
| `index.md` | Homepage. |
| `.well-known/` | BIMI logo / security files copied verbatim into the build. |

---

## Documentation

Start here, then dig into the focused docs as needed:

| Doc | Read it when you want to… |
|---|---|
| **[Architecture](_documentation/architecture.md)** | Understand how a request becomes a page — Jekyll flow, layouts/includes, CSS layering. |
| **[Settings & Feature Flags](_documentation/settings.md)** | Open/close registrations, roll the site to a new event year, flip homepage promos. |
| **[Jekyll Collections](_documentation/collections.md)** | Understand exhibits, categories, and sponsors and how they render. |
| **[Data Files](_documentation/data-files.md)** | Edit the nav menu, footer, schedule, sponsor list, or CTAs. |
| **[Build & Deploy](_documentation/build-deploy.md)** | Run it locally (Ruby or Docker) and understand how GitHub Pages publishes. |
| **[Content Authoring](_documentation/content-authoring.md)** | Add or edit a page, use front matter, and reuse includes. |
| **[Exhibit Pipeline](_documentation/exhibit-pipeline.md)** | Regenerate `_exhibits/` from JotForm submissions. |
| **[Redesign 2026](_documentation/redesign-2026.md)** | Understand the in-progress brand modernization (tokens, decisions, tasks). |

---

## Common tasks at a glance

- **New event year?** → [Settings](_documentation/settings.md) (dates, `event_year`,
  registration URLs) + [Exhibit Pipeline](_documentation/exhibit-pipeline.md).
- **Open the Call for Makers / Volunteer signup?** → flip the flags in
  [Settings](_documentation/settings.md).
- **Change the top nav or footer?** → `_data/menus.yaml`, see [Data Files](_documentation/data-files.md).
- **Restyle something?** → `assets/css/mfo-redesign.css`, see [Redesign 2026](_documentation/redesign-2026.md).
- **Add a regular content page?** → `pages/`, see [Content Authoring](_documentation/content-authoring.md).