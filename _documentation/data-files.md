# Data Files

Everything in [`_data/`](../_data/) is loaded by Jekyll and exposed to templates
as `site.data.<filename>`. This is how the site stays content-driven instead of
hard-coded. YAML is **whitespace-sensitive** — indent with spaces, never tabs.

| File | Drives | Detailed in |
|---|---|---|
| `settings.yaml` | Event year, dates, feature flags. | **[Settings](settings.md)** |
| `menus.yaml` | Top nav + footer. | below |
| `sponsors.yaml` | Sponsor list + tiers. | below |
| `schedule.yaml` | Event schedule. | below |
| `cta.yaml` | Nav/footer call-to-action buttons. | below |
| `featured-exhibits.yaml` | Optional homepage featured makers. | below |
| `crew-roles.yaml` | Crew roles listed on `/join-the-crew/`. | below |
| `mediacoverage.yaml` | Press / media coverage list. | below |

---

## `menus.yaml` — navigation & footer

Two top-level keys: `topnav` and `footernav`.

### Top nav

```yaml
topnav:
  - title: Things to See & DO
    subfolderitems:
      - page: Makers & Exhibits
        url: /exhibits/
      - page: Event Schedule
        url: /schedule/
```

Each top item has a `title` and a list of `subfolderitems` (`page` + `url`).
URLs can be internal (`/volunteer/`) or external (`https://…`). Rendered by
`_includes/topnav.html`. Commented-out blocks are kept as a parking lot for
seasonal items — leave the indentation intact when editing.

### Footer

`footernav` has two columns:

- **Maker Faire Orlando** — local links (`subfolderitems`) + `socialitems`
  (Facebook / Instagram / YouTube), each with a Font Awesome `icon`.
- **Maker Faire** (global) — grouped `columns` (About / Explore / Subscribe), each
  with a `heading` and `items`; plus its own 5-icon `socialitems` set
  (X / Facebook / YouTube / Instagram / Discord). All links carry
  `utm_source=mforlando&utm_medium=footer`.

Rendered by `_includes/footer.html`. The grouping/icons were aligned to the global
Maker Faire footer during the redesign — see [Redesign 2026](redesign-2026.md).

---

## `sponsors.yaml` — sponsors {#sponsors}

```yaml
sponsorlevels:
  - 1: Goldsmith Sponsors
  - 2: Silversmith Sponsors
  - 3: Coppersmith Sponsors
  - 4: Blacksmith Sponsors
  - 5: Contributing Sponsors

sponsors:
  - name: Make
    url: https://www.makezine.com
    logo: makeLogo_url_2012.png       # file in assets/images/sponsors/
    level: 3
    active: true                      # set false to keep history but hide
```

- `level` maps to a tier (1 = top). `active: false` retains a sponsor in the file
  but hides it from the site.
- Logos live under `assets/images/` (sponsor logo path).
- Rendered by the sponsor includes: `sponsors-grid-modern.html` (the `/sponsors/`
  page), `sponsors-marquee.html` (homepage scrolling band), and the legacy
  `sponsors-grid.html` / `sponsors-carousel.html` (kept for reference).
- Showing **last year's** sponsors while the new list fills in? Set `sponsor_year`
  in [Settings](settings.md).

---

## `schedule.yaml` — event schedule

A flat list of events. **Entries must be sorted by date manually** (note the
`#YOU MUST SORT THESE ITEMS!!!` warning at the top of the file).

```yaml
- title: Minecraft Makers
  slug: ftd-mcparks
  location: Main Stage
  description: From castles to coasters…    # HTML allowed
  date: 2025-11-07 10:30:00
  enddate: 2025-11-07 10:55:00
  image: /assets/images/stage/2025/mcparks.jpg
  guests:
    - name: MCParks
      image: /assets/images/stage/2025/mcparks.jpg
      url: /exhibits/mcparks-theme-parks-in-minecraft/
```

- `location` and `date` feed the day/stage filters on the schedule pages
  (`location | slugify`, `date | date: "%A" | slugify`).
- Rendered by `_layouts/schedule.html` (`/schedule/`) and
  `_layouts/schedule-app.html` (`/schedule-app/`), and exported as JSON at
  `/schedule-json/` (see [Architecture](architecture.md#json-exports)).

---

## `cta.yaml` — call-to-action buttons

Defines the button text/URL for the nav and footer CTAs:

```yaml
topnav:
  text: Get Tickets!
  url: /attend/
footer:
  text: Get Tickets!
  url: /attend/
```

Swap to a newsletter signup off-season by editing text/url (commented examples are
in the file).

---

## `featured-exhibits.yaml` — homepage featured makers

A `homepage:` list of featured exhibits, referenced by `exhibit-id`. You can
override `title`/`description`/`image` per entry. Only shown when
`featured_makers` is true in [Settings](settings.md). The file's header explains
how to find an exhibit's id (inspect the title on the exhibit page).

---

## `crew-roles.yaml` — crew roles (`/join-the-crew/`)

A `roles:` list powering both role blocks on [`pages/join-the-crew.md`](../pages/join-the-crew.md):
the "Featured Roles" jump cards (entries with `featured: true`) and the full
alphabetical descriptions below them. Per entry:

| Key | Purpose |
|---|---|
| `id` | Anchor target — the featured card links to `#{{ id }}` on the full role block. Keep it URL-safe. |
| `name` | Role title. The full list is sorted alphabetically by this. |
| `icon` | Font Awesome class (e.g. `fa-solid fa-school`). |
| `featured` | `true` → also shown as a jump card near the top. Keep to 3 so the grid stays balanced. |
| `teaser` | One line, featured card only. |
| `body` | List of paragraphs — the full description. |
| `great_for` | Completes the sentence "Great for: …". |

Adding or retiring a role is a change to this file only. The page is **evergreen** —
keep entries free of dates, the event year, and attendance figures.

---

## `mediacoverage.yaml` — press coverage

List of media/press mentions surfaced on the press/about areas of the site.

---

### See also
- [Settings](settings.md) — `settings.yaml` gets its own page; it's the most-edited.
- [Architecture](architecture.md) — how includes consume these files.
