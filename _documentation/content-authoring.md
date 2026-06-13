# Content Authoring

How to add or edit ordinary content pages (everything that isn't a generated
exhibit). For exhibits see the [Exhibit Pipeline](exhibit-pipeline.md); for nav,
sponsors, and schedule see [Data Files](data-files.md).

---

## Where pages live

- **[`pages/`](../pages/)** — most content pages (`attend.md`, `volunteer.md`,
  `sponsors.md`, `schedule.md`, `become-a-sponsor.md`, …).
- **[`index.md`](../index.md)** — the homepage (lives at the repo root).
- **`404.md`** — the not-found page.

Pages are Markdown with a YAML **front matter** block at the top. They can include
raw HTML and Liquid (`{% … %}` / `{{ … }}`) too.

---

## Front matter

A minimal page:

```yaml
---
title: Volunteer
permalink: /volunteer/
layout: full-width
---

# Page content starts here (Markdown + HTML + Liquid)
```

Common front matter keys used across this site:

| Key | Purpose |
|---|---|
| `title` | Page title (also used by SEO). |
| `permalink` | The URL the page is served at (e.g. `/volunteer/`). |
| `layout` | Which template wraps it — see table below. |
| `description` | SEO description (falls back to the site default). |
| `image` | Social/OpenGraph image (falls back to site logo). |
| `redirect_from` | Alias URLs that redirect here (via `jekyll-redirect-from`). |
| `sitemap` | Set `false` to keep a page out of `sitemap.xml`. |
| `noindex` | Set `true` for utility pages that shouldn't be indexed. |
| `carousel` + `carousel-*` | Enable/configure a hero carousel (see `index.md`). |
| `scrolltop` | Show a scroll-to-top control. |

### Layouts you'll pick from

| `layout:` | Use for |
|---|---|
| `default` | Standard content page with nav + footer. |
| `full-width` | Full-bleed pages (homepage, restyled exhibit/volunteer pages). |
| `category` | Exhibit index / category grids (usually only the collection uses this). |
| `schedule` / `schedule-app` | Schedule views. |

See [Architecture](architecture.md) for what each layout assembles.

---

## Reusing includes

Pull shared building blocks in with `{% include name.html %}`. Some accept
parameters:

```liquid
{% include cta-panel-widget.html
     cta_text="Get Tickets"
     cta_subtext=site.data.settings.event_location_descr
     cta_url=site.data.settings.cta_event_url %}
```

Frequently used includes:

- `cta-panel-widget.html` — the call-to-action band.
- `what-is-maker-faire.html`, `category-cards.html`, `get-involved-cards.html`,
  `featured-makers-grid.html` — homepage sections.
- `update-warning.html` — the "not updated for this year yet" banner.
- `date-event.html` / `date-edu.html` (+ `-short`) — render event dates from
  settings, so you never hard-code a date in copy.

Browse [`_includes/`](../_includes/) for the full set; see
[Architecture](architecture.md) for the rundown.

---

## Driving content with settings

Gate sections on feature flags so you can stage content and reveal it later:

```liquid
{% if site.data.settings.call_for_makers_open %}
  {% include call-for-makers-widget.html %}
{% else %}
  <p>Applications open soon — check back!</p>
{% endif %}
```

The exhibit and volunteer pages use this pattern to swap between an active form
and an "opening soon" message. The full flag list is in
**[Settings](settings.md)** — prefer a flag over editing copy whenever one exists.

---

## Editing dates, prices, and URLs

Don't hard-code these in page copy when a data source exists:

- **Event dates / hours / location** → `_data/settings.yaml` (rendered by the
  `date-*` includes).
- **Application & registration URLs** → `cfm_url`, `volunteer_checkout` in
  settings.
- **Nav / footer / CTA links** → `_data/menus.yaml`, `_data/cta.yaml`.

---

## Adding a new page — checklist

1. Create `pages/my-page.md`.
2. Add front matter with at least `title`, `permalink`, and a `layout`.
3. Write content (Markdown / HTML / Liquid).
4. Add a nav entry in `_data/menus.yaml` if it should be linked.
5. Preview with `.\serve-fast.ps1` and confirm the `permalink` resolves.

---

### See also
- [Settings](settings.md) · [Data Files](data-files.md) · [Architecture](architecture.md)
- [Build & Deploy](build-deploy.md) — previewing your changes.
