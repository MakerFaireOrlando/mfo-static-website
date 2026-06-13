# Jekyll Collections

[Collections](https://jekyllrb.com/docs/collections/) let Jekyll treat a folder of
documents as a queryable set. This site defines three, configured in
[`_config.yml`](../_config.yml):

```yaml
collections:
  sponsors:
    output: false        # data only — no standalone pages
    sort_by: sponsor-level
  exhibits:
    output: true         # each exhibit gets its own page
    sort_by: Name
  categories:
    output: true         # each category gets its own page
    sort_by: Name
```

In templates they're available as `site.exhibits`, `site.categories`, and
`site.sponsors`.

> Note: `_documentation/` (where this file lives) is **not** a collection — it has
> no entry above and isn't published. It's internal docs only.

---

## `_exhibits/` — the maker exhibits

One Markdown file per exhibit (~290 of them), e.g.
`_exhibits/2025-3d-printed-cameras.md`.

**These are generated, not hand-edited.** The [Exhibit Pipeline](exhibit-pipeline.md)
(`_python/update_exhibits.py`) pulls submissions from JotForm, downloads and
resizes images, and writes these files. Manual edits get overwritten on the next
import.

### Front matter shape

```yaml
title: "3D Printed Cameras!"
slug: 3d-printed-cameras
permalink: /exhibits/3d-printed-cameras/
exhibit-id: 25-58
exhibit-zone: "Opportunity"        # which area / building
space-number: "OE10"               # booth assignment
description: "Short SEO/summary blurb."
description-long: "Full description shown on the exhibit page."
image: /assets/images/exhibit-images/25-58-...-300x200.jpg   # card image
image-primary:                     # responsive variants (full/large/medium/small)
  full:   { url: …, width: 3000, height: 2002 }
  medium: { url: …, width: 300,  height: 200  }
  …
additional-images: [ … ]           # gallery images, same variant shape
categories: [ … ]                  # links the exhibit into _categories
```

`title`, `description`, and `image` double as SEO fields. The responsive image
variants (`full`/`large`/`medium`/`small`) are produced by the importer.

Defaults applied in `_config.yml`: every exhibit gets `layout: exhibit`.

### How they render

- **Index & category pages** use `_layouts/category.html`, which loops
  `site.exhibits` and emits each via `_includes/exhibit-card.html` into an
  **Isotope** filterable/searchable grid.
  - On `/exhibits/` it shows all exhibits (excluding combat-robot `R` IDs).
  - On a `/exhibits/categories/<slug>/` page it shows only exhibits whose
    `categories` include that slug.
- **A single exhibit** uses `_layouts/exhibit.html` at its `permalink`.

---

## `_categories/` — exhibit categories

One Markdown file per category (~62), e.g. `_categories/art.md`. Each is short —
mostly front matter:

```yaml
title: "Art"
slug: art
permalink: /exhibits/categories/art/
description: Check out all the Art exhibits at Maker Faire Orlando!
image: /assets/images/site-branding/mfo_two_line_border.png
isotope-exhibits: true
```

Defaults in `_config.yml` give every category `layout: category` and
`sitemap: true`. An exhibit appears under a category when that category's `slug`
is present in the exhibit's `categories` list (the category layout matches on
`category.slug == page.slug`).

To **add a category**: create a new `_categories/<slug>.md` with the four fields
above. New exhibits reference it by slug (the importer maps JotForm category
selections to these slugs).

---

## `sponsors` — data-only collection

Defined as a collection with `output: false`, but in practice the sponsor list is
maintained as the data file **[`_data/sponsors.yaml`](../_data/sponsors.yaml)** —
that's what the sponsor includes loop over (`site.data.sponsors`). See
[Data Files](data-files.md#sponsors) for the schema and tier levels.

---

## Adding to a collection

| You want to… | Do this |
|---|---|
| Add/update exhibits | Run the [Exhibit Pipeline](exhibit-pipeline.md) — don't hand-write files. |
| Add a category | Create `_categories/<slug>.md` (see shape above). |
| Add/edit sponsors | Edit `_data/sponsors.yaml` (see [Data Files](data-files.md)). |

---

### See also
- [Architecture](architecture.md) — how layouts and includes assemble these.
- [Settings](settings.md) — `maker_exhibits_holdover` and
  `maker_exhibits_show_location` control exhibit display.
