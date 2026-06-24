# Settings & Feature Flags

Almost everything that changes year-to-year — or that gets turned on and off as an
event approaches — lives in one file:

**[`_data/settings.yaml`](../_data/settings.yaml)**

Because it's a Jekyll data file, any value is available in templates as
`site.data.settings.<key>`. Includes and pages read these to decide what to show.

> Rule of thumb: if you find yourself about to edit page content to "open the
> volunteer form" or "change the event date," check here first — there's almost
> always a flag for it.

---

## Rolling the site to a new event year

These are the values you change for a new Maker Faire:

| Key | Example | Notes |
|---|---|---|
| `event_year` | `2026` | The current event year. |
| `event_dates.edu_day` | `2026-11-06` | Education / Field Trip Day. |
| `event_dates.day1` | `2026-11-07` | Saturday. |
| `event_dates.day2` | `2026-11-08` | Sunday. |
| `event_hours` | `10am to 5pm` | Public event hours. |
| `edu_hours` | `10am to 3pm` | Field Trip Day hours. |
| `event_location_descr` | `Central Florida Fairgrounds & Expo Halls` | Shown in CTAs. |
| `event_name` | `Maker Faire Orlando` | |
| `sponsor_year` | `2025` | Set this to show the **prior** year's sponsors while the new year fills in. |

The `event_dates` / `event_hours` values feed the `date-event*.html` and
`date-edu*.html` includes, which render human-readable dates across the site —
update them in one place here, not in page copy.

---

## Registration flags

These gate the application/registration widgets on their respective pages. When
**closed**, the page shows an "opening soon" message instead of the form.

| Key | Controls | Page |
|---|---|---|
| `call_for_makers_open` | Shows the **Apply to Exhibit** button. | `/exhibit-at-maker-faire-orlando/` |
| `cfm_url` | The exhibit application URL the button points to. | — |
| `volunteer_open` | Shows the Humanitix volunteer shift widget. | `/volunteer/` |
| `volunteer_checkout` | Humanitix slug for the volunteer widget. | — |
| `tickets_on_sale` | Shows the Humanitix ticket widget; when false, a "tickets not on sale yet" message. | `/attend/` |

> **Update the URLs/slugs to the current year before flipping the flag open.**
> `cfm_url` is the JotForm call-for-makers form; `volunteer_checkout` is the
> Humanitix event slug (currently still the 2025 slug — change it for 2026).

---

## Homepage promos

The homepage ([`index.md`](../index.md)) includes optional sections only when
their flag is true, so you can stage content and reveal it when ready:

| Key | Shows |
|---|---|
| `featured_makers` | Featured-makers grid (`featured-makers-grid.html`). |
| `event_shirt_promo` | Event T-shirt promo (`event-shirt.html`). |
| `explore_meet_makers` | "Explore / meet the makers" section. |
| `explore_card_links` | Whether the "Explore the Faire" category cards link out. Set `false` early in the year before the category/stage pages have fresh content. |
| `footer_ad` / `footer_ad_url` | An optional footer ad and its target. |

---

## "Page not updated yet" warnings

Several pages carry a banner (via `_includes/update-warning.html`) reminding
visitors the content is still from the prior year. Each is independently gated:

| Key | Page |
|---|---|
| `badge_show_update_warning` | `/badge/` |
| `maker_manual_show_update_warning` | `/maker-manual/` |
| `schedule_show_update_warning` | `/schedule/` |
| `promote_show_update_warning` | `/promote/` |
| `program_show_update_warning` | `/program/` |

Also under the badge page:

- `badge_show_space_plans` — toggles the space-plan section.

Set each to `false` once that page has been refreshed for the current year.

---

## Exhibit display

| Key | Effect |
|---|---|
| `maker_exhibits_holdover` | Show last year's exhibits as a "holdover" set until the new ones are imported. |
| `maker_exhibits_show_location` | Show booth/zone/space numbers on exhibit cards (turn on once space assignments are final). |

See the [Exhibit Pipeline](exhibit-pipeline.md) for how exhibit data is generated.

---

## Other values

| Key | Use |
|---|---|
| `newsletter_url` | Mailing-list signup link. |
| `contact_email` | Public contact address (`makers@makerfaireorlando.com`). |
| `cta_event_url` | Where the main event CTA points (`/attend/`). |

---

## How a flag gets used (example)

In `index.md`:

```liquid
{% if site.data.settings.call_for_makers_open %}
{% include call-for-makers-widget.html %}
{% endif %}
```

And on the exhibit page, the same flag swaps between an **Apply** button (open)
and an **Opening Soon** callout (closed), with the button pointing at
`site.data.settings.cfm_url`. This is the standard pattern: **flag decides
visibility, a companion key supplies the URL/slug.**

---

### See also
- [Data Files](data-files.md) — the other YAML files (menus, sponsors, schedule).
- [Content Authoring](content-authoring.md) — using these flags inside page copy.