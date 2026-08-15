# Maker Faire Orlando — Brand Redesign (2026)

> Living document. Captures the concepts, decisions, design tokens, and task
> list for bringing the MFO site in line with the current Maker Faire event-page
> brand. Update this file as work progresses.

**Last updated:** 2026-06-27 (theme system §6.17; dark-mode image/logo audit checklist §6.18)
**Status:** **IN PROGRESS.** On branch `redesign`,
not yet merged to `master`. Core re-skin + multiple pages/components done and
browser-verified. See the dated sub-sections (§6.x) and the Decisions log (§7)
for everything completed; see **§9 Resume Here** for what's open.

Done so far: navy/charcoal + coral re-skin; Archivo/Inter type; nav/CTA; footer
(white, Happy-Valley-style, 5 social icons); flag-banner removed; homepage
"What is Maker Faire" styled intro, Explore + Get-Involved card rows (image-zoom
hover, balanced grids, Stage Talks card, `explore_card_links` toggle); sponsor
**marquee** (drag-scrub) on homepage + **modern sponsors grid** on `/sponsors/`;
exhibit, volunteer, and promote pages restyled. **Carousels are imagery only —
no text overlay** (hero overlay reversed, see §7).

**Primary reference:** https://makerfaire.com/bay-area/?2026 — the Maker Faire
**Bay Area event page**, chosen because it is an event page like MFO (the
makerfaire.com global landing page is a less apt model).

---

## 1. Context & Goal

The MFO site is a Jekyll port of the **old Maker Faire Global "minimakerfaire"
WordPress theme**. The comment header in `assets/css/mfo-style.css` says it was a
*"reskin to look like the new Maker Faire Global theme"* — but that was the
*previous* global brand. Maker Faire has since rebranded, so the MFO site now
reads a generation behind makerfaire.com.

**Goal:** Full modernization that **matches the Maker Faire Bay Area event page
closely** — swap the blue-dominant legacy look for a **deep navy/charcoal +
white** system with a **coral / orange-red CTA accent**, modern sans-serif
typography, full-bleed hero photography, generous whitespace, soft shadows, and
a punchier editorial voice.

### Decisions (locked)
- **Scope:** Full modernization (re-skin + hero/voice + retire dated patterns).
- **Brand fidelity:** Match makerfaire.com closely (read as part of the global
  brand family).

---

## 2. Current State (baseline)

| Aspect | Today |
|---|---|
| Generator | Jekyll, `jekyll-theme-minimal` base, GitHub Pages |
| CSS framework | Bootstrap **3.3.7** (CDN) |
| Main theme CSS | `assets/css/minimakerfaire-style.css` (~29,800 lines, minified) |
| Custom CSS | `assets/css/mfo-style.css` (~388 lines) |
| Palette | Blue-dominant: `#00A3DA` primary, `#00597E`/`#005980` teal, red hover accents |
| Fonts | Roboto (body) + Roboto Slab (headings), Google Fonts |
| Decoration | Rotated `.flag-banner` border strip; heavy `4px 4px 10px #888` card shadows, 4px radii |
| Layout | Full-width carousel hero, card grids (Isotope), two-column dark footer |

### Key files
- `_includes/stylesheets.html` — CSS + font `<link>` tags (load order matters)
- `_includes/head.html` — meta, favicons, analytics
- `_includes/topnav.html` — nav bar + header CTA button
- `_includes/footer.html` — two-column footer
- `_includes/carousel.html` — homepage/page hero carousel
- `_includes/cta-panel-widget.html` — yellow CTA strip
- `_includes/what-is-maker-faire.html` — intro section
- `_layouts/default.html` — header flag-banner, page body, footer wiring
- `index.md` — homepage content + carousel slides
- `assets/css/mfo-style.css` — current custom overrides (uses `!important`)

---

## 3. Maker Faire Bay Area Event Page — Target Design Language

Reference: https://makerfaire.com/bay-area/?2026

- **Color:** **Deep navy / charcoal** backgrounds with **white** text,
  alternating with **white** sections (dark text). Bright **coral / orange-red**
  reserved for primary CTAs ("BUY TICKETS"). High contrast, polished.
- **Type:** Bold **uppercase sans-serif** for major headlines
  (e.g. *"Think It. BUILD It. Break It. Make It Better!"*); title-case section
  headers; regular-weight sans body; small-caps descriptive taglines.
- **Hero:** **Full-bleed venue photograph** with dark gradient overlay and white
  text; tagline + date (*"September 25–27th"*) + prominent coral **BUY TICKETS**
  button. Date/location woven into body copy below.
- **Sections (top→bottom):** Hero → anniversary/about blurb → **four category
  cards** (Tech & Electronics, Science & Engineering, Crafts & Artisans, Live &
  Interactive) → **"Get Involved" role cards** (Makers, Sponsors, Stewards,
  Attendees) → photo carousel → sponsor testimonial → global faire carousel.
- **Buttons:** Primary = solid coral fill, white text, slightly rounded
  rectangle. Secondary = text link with arrow ("Apply Now →", "Get In Touch →").
- **Cards:** Square hero image, subtle rounded corners, white text overlay,
  minimal shadow, clean even grid spacing.
- **Mood:** Energetic yet polished — DIY maker spirit packaged as a flagship
  event. Lots of whitespace, high-quality photography, warm coral accents.

> **Open item:** Exact hex + font names could not be extracted remotely (page is
> JS-rendered; fetch tool strips `<head>`). Using grounded approximations below;
> **sample exact values from the live page / brand assets when available.**

---

## 4. Design Tokens (proposed — revised for event-page reference)

All tokens live in `:root` in `assets/css/mfo-redesign.css` so the look can be
retuned in one place.

### Color
| Token | Value (approx) | Use |
|---|---|---|
| `--mf-navy` | `#16213E` | Primary dark sections, footer, hero overlay |
| `--mf-navy-deep` | `#0E1628` | Deepest background |
| `--mf-charcoal` | `#1E2230` | Alt dark surface |
| `--mf-red` | `#DB2B2F` | Primary accent / CTA fill (makerfaire.com red) |
| `--mf-red-dark` | `#B82328` | Accent hover / pressed (darker red) |
| `--mf-ink` | `#1A1A1A` | Body text on white |
| `--mf-white` | `#FFFFFF` | Light sections, text on dark |
| `--mf-gray-50…800` | neutrals | Backgrounds, borders, muted text |

> **Note:** Legacy MFO blue (`#00A3DA`) is dropped as the lead; navy is the new
> dark base and coral is the action color. (Open question: retain a hint of MFO
> blue as a tertiary accent?)

### Typography
- Headings: **Archivo** (heavy/grotesque, supports bold uppercase headlines) —
  `--mf-font-head`
- Body: **Inter** — `--mf-font-body`
- (Both free Google Fonts; close, license-safe matches. Headlines set uppercase
  with tight tracking to echo the Bay Area page.)

### Surface
- Radius: `12px` cards / `6px` buttons (slightly-rounded rectangles, not pills)
- Shadows: soft, layered (`0 6px 24px rgba(16,22,40,.12)` → hover lift)
- Buttons: **coral fill, white text, rounded rectangle**; hover = darker coral +
  subtle lift. Secondary = text + arrow.

---

## 5. Approach

Layer a **single override stylesheet** (`assets/css/mfo-redesign.css`) loaded
**last** in `_includes/stylesheets.html`, built on CSS custom properties. This
overrides the legacy 29.8k-line theme **without rewriting it** — lowest risk,
reversible. Legacy buttons use `!important`, so brand overrides match that
specificity where needed.

Markup changes are kept minimal and additive (e.g. a hero overlay element,
brand-voice copy), preserving existing layouts, Isotope grids, and data-driven
includes.

---

## 6. Task List

- [x] **1. Foundation stylesheet** — `assets/css/mfo-redesign.css` with tokens +
  component overrides.
- [x] **2. Wire in** — added stylesheet + Archivo/Inter font links to
  `_includes/stylesheets.html`, loaded last; replaced Roboto links.
- [x] **3. Navigation + CTA** — navbar + header CTA restyled via redesign CSS
  (white nav, coral underline on hover, coral pill→rect CTA button).
- [x] ~~**4. Hero + voice** — full-bleed hero overlay on the carousel~~
  **REVERSED 2026-06-13:** per user, **no text is overlaid on the main
  carousels** — they are imagery only. The `.mf-hero-overlay` markup
  (`_includes/carousel.html`), its CSS (§4), and all `hero-*` front matter were
  removed. Page titles/taglines now live solely in the content sections below
  the carousel (each page already has its own `<h1>`).
- [x] **5. Components** — cards, buttons (coral), shadows, `.cta-panel` (navy),
  `.what-is-maker-faire`, footer (navy), FAQ all rebranded.
- [x] **6. Retire flag-banner** — rotated strip removed entirely via
  `display:none` (CSS override). (Swap back to a 5px coral rule by restoring
  `height`/`background-color` if a thin brand rule is wanted instead.)
- [x] **7. Verify** — `bundle exec jekyll build` clean (42s); redesign CSS link,
  fonts, hero, and both card rows confirmed in `_site/index.html`.

### Stretch (event-page structural patterns) — DONE this pass
- [x] **S1. Category cards** — `_includes/category-cards.html`: Robots & Combat /
  3D Printing & Tech / Art & Cosplay / Hands-On Workshops, linking to real
  `_categories` pages with slider imagery.
- [x] **S2. "Get Involved" role cards** — `_includes/get-involved-cards.html`:
  Makers / Sponsors / Volunteers / Attendees, linking to existing MFO pages.

## 6.5 Files Changed (this pass)

| File | Change |
|---|---|
| `assets/css/mfo-redesign.css` | **New** — all design tokens + overrides |
| `_includes/stylesheets.html` | Load redesign CSS last; swap Roboto → Archivo/Inter |
| `_includes/carousel.html` | Optional front-matter-driven hero overlay |
| `_includes/category-cards.html` | **New** — "Explore the Faire" card row |
| `_includes/get-involved-cards.html` | **New** — "Be Part of the Making" card row |
| `index.md` | Hero front matter + include the two card rows |

**Preview:** `bundle exec jekyll serve` → http://localhost:4000
**Retune brand:** edit the `:root` variables at the top of `mfo-redesign.css`.

## 6.6 Footer Update (ref: happyvalley.makerfaire.com)

Per request, the footer was reworked to mirror the Happy Valley Maker Faire
footer while keeping our own left-column (MFO) links:

- **Background:** switched to **white** with dark text (overrides the navy from
  the first pass). Coral link hover; social circles on light gray. *(Note: the
  remote fetch reported this footer as dark, but the live page reads white per
  user; went with white.)*
- **Layout:** responsive cascade mirroring Happy Valley:
  - **Top level:** MFO block (`col-sm-4 col-md-3`) beside the Maker Faire global
    block (`col-sm-8 col-md-9`); below `sm` (768px) the global block wraps under.
  - **Global groups:** the three groups (About/Explore/Subscribe) use **flexbox**
    (`.mf-footer-cols` flex-wrap, items `flex: 1 1 150px`) so they sit
    side-by-side and wrap gracefully **3 → 2 → 1** as width shrinks — rather than
    a hard breakpoint jump (the rigid nested-grid version stacked into one tall
    column and looked broken; see fix note below).
  - Divider switches vertical (border-left) ↔ horizontal (border-top) at 768px.
    `hidden-xs` was removed so the global side shows on phones too.
  - **Logo fix:** the legacy theme allowed the local logo up to 310px
    (`.footer-logo-div .footer-logos.footer-local-logo`, specificity 0,3,0),
    which overflowed the narrow footer column and collided with the robot logo.
    A higher-specificity override (`.gmf-footer .footer-logo-div
    .footer-logos.footer-local-logo { max-width:100% }`) keeps it in-column.

**Browser-tested** (headless Edge at 1280 / 900 / 480px): desktop shows all four
columns side-by-side; ~900px wraps the global groups 3→2 (Subscribe drops below);
480px stacks the global block under MFO with About/Explore 2-up. Logos contained
at every width, no divider collision.

### Social icons + 5-icon set (ref: happyvalley.makerfaire.com)
- **Darkened:** legacy theme rendered social circles faint — a light-gray
  `#D3D3D3` circle with a white glyph. Overrode to **dark ink circles with white
  glyphs** (coral on hover) via higher-specificity
  `.gmf-footer .social-network.social-circle li a` / `... i` rules. Applies to
  both footer columns.
- **5-icon set:** the Maker Faire (global) column now matches Happy Valley —
  **X · Facebook · YouTube · Instagram · Discord** (was Facebook/Instagram/
  Pinterest). Updated `mf.socialitems` in `_data/menus.yaml`.
- **Font Awesome bumped 6.2.0 → 6.7.2** in `_includes/head.html` so the
  `fa-x-twitter` glyph (added after 6.2) renders; `fa-discord` included. SRI
  attribute dropped to avoid stale-hash breakage on the version bump.

## 6.7 Prose content sections (reusable)

Reusable classes in `mfo-redesign.css` for alternating prose bands matching the
event-page rhythm: `.mf-prose-section` (`.is-light` / `.is-dark`), `.mf-prose`
(readable 760px measure, 1.15rem/1.75), `.mf-prose.mf-lead` (1.35rem). Light/
dark bands with coral-underlined links. Apply to any text-heavy page.

> **Note:** these were first built for the About page, which has since been
> **removed** (see below). The classes remain available for other pages.

## 6.9 Exhibit / Call-for-Makers page restyle

Reworked `pages/exhibit-at-maker-faire-orlando.md` from a wall of text into a
scannable, sectioned layout modeled on makerfaire.com/bay-area/call-for-makers/.
Switched the page to `layout: full-width` for full-bleed bands. Sections:
1. **Hero** overlay ("Become an Exhibitor").
2. **Lead** intro (`.mf-prose.mf-lead`).
3. **Application status callout** — data-driven on `settings.call_for_makers_open`:
   - open → coral callout + **Apply to Exhibit** button → `settings.cfm_url`
   - closed → navy "Opening Soon" message (no button).
4. **Ways to Take Part** — four `.mf-info-card`s (Makers free / Selling $150 /
   Businesses → sponsor / Combat Robots → Robot Ruckus) with coral FA icons.
5. **What You'll Need to Apply** — `.mf-checklist` (coral fa-check bullets).
6. **How Exhibits Are Selected** — navy prose band.
7. Contact **CTA panel**.

New CSS (`mfo-redesign.css` §11): `.mf-apply-callout` (`.is-open`),
`.mf-info-grid`/`.mf-info-card` (+ `.mf-info-fee.is-free`), `.mf-checklist`.
New setting `cfm_url` in `settings.yaml` (update per year before opening the
call). Both open and closed states browser-verified; flag left at `false`.

## 6.9b Volunteer page restyle

Same treatment as the exhibit page (`pages/volunteer.md`, now `full-width`):
1. **Hero** overlay ("Volunteer With Us").
2. **Lead** ("We Need You!").
3. **Why Volunteer?** — four `.mf-info-card`s: Free Admission (fa-ticket),
   Volunteer T-Shirt (fa-shirt), Give Back (fa-hands-holding-heart), Service
   Hours (fa-graduation-cap).
4. **Good to Know** — `.mf-checklist` (age, no-cost registration, special
   skills/questions).
5. **Sign Up to Volunteer** — data-driven on `settings.volunteer_open`:
   open → instructions + embedded **Humanitix** shift widget (`.mf-widget-wrap`,
   slug from `settings.volunteer_checkout`); closed → "Opening Soon" callout.

New settings: `volunteer_open` (default `true`) + `volunteer_checkout` (Humanitix
slug — **update per year**, currently the 2025 slug). New CSS: `.mf-widget-wrap`.
Reused `.mf-apply-callout` / `.mf-info-card` / `.mf-checklist` from §11.

## 6.8 About page removed

The About page was dropped entirely (per request): deleted `pages/about.md`,
removed the `ABOUT` top-level item from `topnav` and the `About` link from the
MFO footer column in `_data/menus.yaml`. Verified no `/about/` is output and no
menu references remain. (The homepage "What is Maker Faire?" section —
`_includes/what-is-maker-faire.html` — is unrelated and stays.)

### CTA panel — two lines
The event CTA panel now splits onto two lines: date + time on top, location
(with the chevron) below. `cta-panel-widget.html` gained an optional
`cta_subtext` param (falls back to single-line when absent); `index.md` passes
`event_location_descr` as the subtext. Styled via
`.cta-panel .cta-panel-main` / `.cta-panel-sub` in `mfo-redesign.css`.

### Nav dropdown width
Dropdowns were content-width, so they rendered narrower than the (wider) menu
header they drop from. Added `min-width: 100%; width: max-content;` to
`body .navbar-nav > li > .dropdown-menu` in `mfo-redesign.css` — the `.dropdown`
`<li>` is the positioned ancestor, so the menu is now at least as wide as its
header, expanding further only if an item is wider. Browser-verified.
- **Robot logo:** right column now uses the "Makey welding" Maker Faire logo,
  downloaded to `assets/images/site-branding/makerfaire-welding.webp`.
- **Right column links:** replaced the old flat 8-link list with the global
  footer's three grouped columns:
  - **About** — About Maker Faire, Maker Movement, Advertise, Contact Us
  - **Explore** — Make: magazine, Maker Faire, Maker Shed, Makerspaces
  - **Subscribe** — Purchase, Give A Gift, Manage Subscription, Newsletters
  - (all carry `utm_source=mforlando&utm_medium=footer`)

**Files:** `_data/menus.yaml` (Maker Faire entry → `columns:` with `heading`/
`items`), `_includes/footer.html` (right column renders `mf.columns`),
`assets/css/mfo-redesign.css` (§8 footer → white + `.mf-footer-heading`),
`assets/images/site-branding/makerfaire-welding.webp` (new).

---

## 6.10 Sponsor logo marquee (ref: makerfaire.com/bay-area sponsor strip)

Added a **new** include `_includes/sponsors-marquee.html` emulating the Bay Area
event page's single, slowly/continuously-scrolling band of sponsor logos. The
original `_includes/sponsors-carousel.html` (Bootstrap level-by-level carousel)
is **retained, unchanged** — the homepage (`index.md`) now includes the marquee
instead.

- **Technique:** pure CSS, no Swiper/JS. The active-sponsor logo set is rendered
  twice (second copy `aria-hidden` + `inert`); `.mf-marquee-track` animates
  `translate3d(-50%)` linearly + infinitely for a seamless loop. Speed is
  per-logo: `animation-duration` is set inline = `active_sponsors × 3s`
  (min 24s), so the pace stays constant regardless of sponsor count.
- **UX:** edge-fade mask on the viewport; pauses on hover/focus-within;
  `prefers-reduced-motion` collapses it to a static centered wrapped grid (dupe
  set hidden). Title + subtitle above ("… Sponsors" / "Thank You to the Sponsors
  Who Help Make Maker Faire Happen!").
- **Drag-to-scrub (progressive enhancement):** a small inline `<script>` in the
  include takes over from the CSS animation (adds `.is-grabbable`, drives the
  transform via rAF) so the band can be **clicked/dragged back and forth** like
  the Bay Area Swiper strip; auto-scroll resumes on release; a real drag (>6px)
  suppresses the sponsor-link click. No-JS → CSS auto-scroll still runs;
  reduced-motion → script is skipped.
- **Logos:** `loading="eager"` + `decoding="async"` (lazy-loading made tiles
  pop in blank mid-scroll); `draggable="false"`.
- **Data:** loops `site.data.sponsors` by level then name (same source as the
  old carousel); footer keeps the "Become a Sponsor • All Sponsors" links.
- **CSS:** `mfo-redesign.css` §12 (`.mf-sponsor-marquee` / `.mf-marquee-*`,
  incl. `.is-grabbable` / `.is-dragging`).
- **Verified:** Jekyll build clean; 23 active sponsors → 46 tiles + 69s duration;
  drag enhancement confirmed via post-JS DOM dump (`.is-grabbable` applied,
  transform advancing).

## 6.11 Modern sponsors grid (/sponsors/ page)

New include `_includes/sponsors-grid-modern.html` replaces the legacy
`_includes/sponsors-grid.html` on `pages/sponsors.md` (original include kept
intact). Same data source (`site.data.sponsors`); reworked presentation:
- Each active tier is a section with an **uppercase heading + short coral
  underline rule** (replaces the legacy thin blue `title-w-border`).
- Logos sit on **clean white rounded tiles** (soft shadow + border), centered
  in a flex grid; hover = subtle lift + coral border.
- **Tier size hierarchy:** tiles are sized per tier via CSS variables
  (`--tile-h` / `--tile-basis`) — tier 1 (Goldsmith) largest → tier 5
  (Contributing) smallest — so sponsor level reads at a glance.
- CSS: `mfo-redesign.css` §13 (`.mf-sponsors` / `.mf-sponsor-tier` /
  `.mf-sponsor-tile`); reduced-motion drops the lift.
- Browser-verified at 1280px. (Note: logos with dark/transparent backgrounds
  show their own box on the white tile — a per-logo asset issue, not styling.)

## 6.12 Balanced card grids (no orphaned card)

All card rows now wrap to balanced layouts instead of stranding a single card:
- **4-card grids** (`.mf-card-grid` Get Involved; `.mf-info-grid` volunteer &
  exhibit "Why/Ways" cards): **4 → 2 + 2 → 1** via percentage flex-basis with
  breakpoints (≤991px = 2 columns, ≤767px = 1). Previously `flex: 1 1 240px`
  dropped to a **3 + 1 orphan** at medium widths (~970px container).
- **5-card grid** (`.mf-card-grid--3up` Explore the Faire): **3 + 2** (unchanged
  from §6.11). Selector bumped to `.mf-card-grid.mf-card-grid--3up .mf-card` so
  it always beats the default 4-up rule regardless of source order.
- CSS: `mfo-redesign.css` §6b (`.mf-card`) and §11 (`.mf-info-card`).
- Verified at 1100px (4-up / 3+2) and 900px (2+2) for volunteer + homepage.

## 6.13 Promote / press-kit page restyle

Reworked `pages/promote.md` (now `layout: full-width`) from a long markdown
list into a sectioned press-kit, matching the volunteer/exhibit pattern:
1. **Hero** overlay ("Help Spread the Word") + retained `update-warning`
   (gated on `promote_show_update_warning`).
2. **Lead** intro (`.mf-prose.mf-lead`).
3. **Badges & Logos** — 3 download cards (web badge, one-line, two-line logo) +
   usage note.
4. **Maker Faire Hashtags** — styled chips (`.mf-hashtags` / `.mf-hashtag`).
5. **Print Materials** — 3 cards (postcard front/back, poster) linking high-res
   PDFs.
6. **Social Media Images** — 2 cards (FB cover, profile).
7. **Photos** — navy/gray prose band with the Flickr group link.
8. Contact **CTA panel**.

New CSS (`mfo-redesign.css` §14): `.mf-hashtags`/`.mf-hashtag` chips and a
reusable `.mf-asset-grid`/`.mf-asset-card` download-card component (thumb on a
light tile, `object-fit: contain` for mixed aspect ratios, 3→2→1 responsive,
hover lift). Asset paths/hashtags still reference **2025** — update to 2026 once
new materials are produced.

## 6.14 Homepage "What is Maker Faire?" — styled intro

`_includes/what-is-maker-faire.html` gained typographic hierarchy (CSS §5):
`.wimf-lead` (larger lead paragraph) → `.wimf-tagline` (bold navy statement,
Archivo, with the signature phrase wrapped in `<span class="mf-hl">` = coral)
→ `.wimf-closer` (coral uppercase kicker). Section stays light.

## 6.15 Homepage content cards — hover, Stage card, link toggle

- **Image-zoom hover:** `.mf-card` no longer lifts the whole card; instead the
  media image scales (`.mf-card-media::before { transform: scale(1.2) }` on
  hover, clipped by `overflow:hidden`), à la the Bay Area cards. `background-image:
  inherit` on the `::before` reuses the inline `url()` (no markup change).
  Reduced-motion disables it. (CSS §6b.)
- **Balanced grids:** see §6.12 (Explore = 3+2 via `.mf-card-grid--3up`;
  4-card rows = 4→2+2→1).
- **Stage Talks card:** a 5th Explore card → `/stage/`, image
  `assets/images/stage/stage-talks-2025.jpg` (downloaded from the MFO Flickr
  pool, photo by Roberto Gonzalez). Currently positioned **second**.
- **`explore_card_links` setting** (`_data/settings.yaml`, default `true`): when
  `false`, the Explore cards render but with **no `href` and no "See …→" arrow**
  — for early in the year before category/stage pages have fresh content. Gated
  in `_includes/category-cards.html` via an `card_links` variable. (Get-Involved
  cards are not gated — those pages always exist.)

## 6.16 Attend / Sponsor / Field Trip Day page restyles

Three more `layout: default` wall-of-text pages reworked to the full-width
hero + sectioned pattern (same components as exhibit/volunteer/promote):

- **`pages/attend.md`** (`/attend/`, the primary "Get Tickets" CTA target):
  lead intro → **"Plan Your Visit"** 4 info-cards (When / Where / Free Parking /
  250+ Exhibits) with a plan-your-weekend links line → **Tickets** band (intro +
  Humanitix `data-checkout="makerfaireorlando"` widget in `.mf-widget-wrap` +
  student-ID note) → **Discounted & Free Admission** `.mf-checklist` (5 programs:
  Educators / Field Trip Day / Title I / First Responders & Military / Making For
  All) → **Good to Know** `.mf-checklist` → contact CTA panel. Dropped the stale
  commented 2022/2023 3D-printer giveaway blocks.
- **`pages/become-a-sponsor.md`** (`/become-a-sponsor/`): lead (refreshed copy —
  removed the dated "recovering from the pandemic" line) + coral **Download the
  Sponsor Packet** button → "why sponsor" video → **Sponsorship Packet** as an
  `.mf-asset-card` → sponsor-stories video → **{sponsor_year} Sponsors** via the
  **modern** grid include (`sponsors-grid-modern.html`, swapped off the legacy
  `sponsors-grid.html`) + Orange County funding note → 501(c)(3) closing →
  contact CTA. Videos use Bootstrap `.embed-responsive.embed-responsive-16by9`
  in a `col-md-8 col-md-offset-2`.
- **`pages/field-trip-day.md`** (`/field-trip-day/`): lead → **"A Day of
  Discovery"** 4 info-cards (Meet / Explore / Build / Imagine) → **Planning**
  section with the Educator's Guide `.mf-asset-card` (+ "guide not yet updated
  for 2026" caveat retained) and exhibit-category links → **"Who Can Take Part"**
  2 info-cards (School Field Trips / Homeschool & Virtual) → **Register** via a
  `.mf-apply-callout.is-open` with the JotForm button
  (`mfo2026-field-trip-day`) → **Important Notes** `.mf-checklist` → contact CTA.
  The seasonal `{% comment %}` "at capacity / deadline passed" toggle blocks were
  **preserved** (inside the two Who-Can-Take-Part cards) for the maintainer.

No new CSS — all three reuse existing components. Build clean; all three
browser-verified at 1280px (Humanitix iframe is blank in headless, loads via JS
at runtime, same as the volunteer widget). 2025 asset paths (sponsor packet,
educator's guide) left as-is pending 2026 materials.

## 6.16b Join the Crew page (`/join-the-crew/`)

New **evergreen** crew-recruitment page supporting the LinkedIn recruiting push:
producers post to their networks, and this page is the "learn more" destination
for people who want role detail before raising their hand. Built from the source
spec `crew-page-build-spec.md` (written without repo access — its placeholder
green/pink dark palette and self-contained CSS were **dropped** in favour of the
site's existing components; the copy and section order were kept).

- **`pages/join-the-crew.md`** — carousel hero with the optional `hero-title`
  overlay (its first real use on the site: headline + meta line + mailto CTA),
  then lead ledes → mission band (`.mf-prose-section.is-light`) → "what you'll
  gain" `.mf-info-grid` → **Featured Roles** cards that are anchor links into the
  full list → `.mf-apply-callout` "No experience? No problem." → full role
  descriptions (`.mf-roles`) → dark "booked weekend is no barrier" band →
  `.mf-apply-callout.is-open` off-ramp to `/volunteer/` → final CTA (mailto +
  `a.btn-w-ghost`). The lead section deliberately has **no heading** — the hero
  overlay supplies the page's single `<h1>`.
- **`_data/crew-roles.yaml`** — role content (see
  [Data Files](data-files.md)). Adding a role never touches markup.
- **CSS §15** — the only new rules: `scroll-behavior`, `scroll-margin-top`, and
  the `:target` coral highlight for the anchor jump, all scoped behind
  `html:has(.mf-crew-roles)` so smooth scrolling never leaks to the rest of the
  site (`/volunteer/` shares `.mf-role` and is unaffected).

Deliberately **not** done, per the site owner: no nav entry (traffic comes from
external posts) and no cross-links from `/volunteer/` or the homepage cards.
Adding a "Join the Crew" entry under **Get Involved** in `menus.yaml` later is a
two-line change. No attendance figures are published anywhere on the page (the
numbers in circulation are unverified) — it says "thousands of students" instead.

## 6.17 Theme system — dark mode + 2026 "Maker Invasion" skin (UFO toggle)

Two buttons in the header (`_includes/topnav.html`) drive a single
`<html data-theme="…">` value (`light` | `dark` | `invasion`):

> - **`#theme-mode-toggle`** (sun/moon) — permanent **light ↔ dark** switch.
> - **`#theme-toggle`** (UFO) — TEMPORARY: toggles the 2026 **Invasion** neon
>   skin on/off, remembering the light/dark base to return to.

Two layers, deliberately separated so the fun 2026 look is **trivially
removable** while a clean dark mode stays behind:

1. **Neutral dark mode** (`assets/css/mfo-theme-dark.css`) — permanent,
   brand-agnostic. `[data-theme="dark"]`.
2. **2026 "Maker Invasion" skin** (`assets/css/mfo-theme-invasion.css`) —
   temporary neon alien-invasion skin + immersive scene. `[data-theme="invasion"]`.
   Based on `assets/images/site-branding/2026/mfo2026-humanitix-header.jpg`
   (black sky, neon lime + hot magenta, cream).

### How it works (no per-selector rework)

The 2026 redesign already routes nearly all color through the `--mf-*` custom
properties in `mfo-redesign.css`. **Most tokens are single-role, so each theme
just *redefines the tokens*** in a `[data-theme="…"]` block — the cascade
re-skins every component automatically.

Two tokens were **overloaded** (used as both a background *and* as text/accent),
which a naive swap would break (e.g. `--mf-white` is a light surface *and* the
text color on dark bands). Their **background role** was split out into two new
**semantic tokens** in `mfo-redesign.css`:

| Semantic token | Light value (alias) | Role |
|---|---|---|
| `--mf-bg` | `var(--mf-white)` | page background (applied to `body`) |
| `--mf-surface` | `var(--mf-white)` | raised light surfaces: navbar, cards, footer, panels |
| `--mf-dark-bg` | `var(--mf-navy)` | intentionally-dark bands: `.cta-panel`, `.mtm-search`, `.is-dark` |

In light mode these alias the original values, so **the site renders
identically** (verified). All other tokens (`--mf-ink`, `--mf-navy` as text,
grays, `--mf-red`) are single-role and simply get new values per theme.

**Legacy hardcoded text:** the old `minimakerfaire` theme hardcodes content text
to `#4a4a4a` on bare `body`/`p` (not a token), so paragraphs stayed dark-on-dark
in the themes. Both theme sheets re-anchor generic content text to the ink token
with a low-specificity rule — `[data-theme="…"] :where(p, li, td, small,
.text-muted, …) { color: var(--mf-ink); }` — chosen via `:where()` so any
component that sets an explicit token color (or `!important`) still wins, and
light mode is untouched. A full rendered-HTML sweep (all `_site/**`) confirmed no
other hardcoded-dark-text-on-transparent text on the public pages; the only other
touch-ups needed were **Bootstrap `.alert`** banners (light box → dark surface +
light text + amber/lime warning accent, both themes) and a couple of inline gray
status strings in the internal `schedule-editor` (switched to `opacity` so they
inherit the themed color).

### No-flash, session-only persistence

- **Session-only persistence (by design):** the active theme is kept in
  **`sessionStorage`** — it survives reloads and navigation *within the tab*, but
  a **new session** (window closed/reopened, fresh tab) starts at
  `settings.theme_default` (currently `light`). No `localStorage`/cookies, so
  nothing is remembered long-term.
- **No flash:** an inline `<script>` in `_includes/head.html` (right after the
  stylesheets) sets `<html data-theme="…">` **before paint** — from
  `sessionStorage('mfo-theme')` if present (and valid), else `theme_default`.
- **Turning on invasion:** the `/invasion/` page sets `sessionStorage('mfo-theme')
  = 'invasion'` and redirects home; from then on the skin sticks for the session.
- **Invasion homepage carousel:** when the homepage loads in invasion, the
  carousel init (`_includes/optional-js.html`) prepends `invasion-header.jpg` as
  the active first slide (instead of the usual random start). Detected via the
  `data-theme` attribute, so it works on the `/invasion/` redirect and any
  in-session homepage load.
- **Controller:** `assets/js/mfo-theme.js` (loaded unconditionally in
  `_includes/scripts.html`) wires the toggle buttons (if shown) — writing the
  choice (and the light/dark base) to `sessionStorage` — and **lazily builds the
  immersive FX scene** when invasion runs. The sun/moon icon swaps via pure CSS
  on `data-theme`.

### Settings (`_data/settings.yaml`)

| Setting | Default | Effect |
|---|---|---|
| `theme_toggle_enabled` | `true` | Show/hide the sun/moon **light↔dark** toggle in the header. |
| `theme_default` | `light` | Theme at the start of each session: `light` \| `dark` \| `system` (follows OS `prefers-color-scheme`) \| `invasion`. Session-persisted, not long-term. |
| `theme_invasion_icon` | `true` | Show/hide the **UFO** button. Hiding it does **not** disable invasion — `/invasion/` still triggers the skin (share-link / kiosk), and the scene still renders on pages with the nav. |
| `theme_invasion_fx_duration` | `10` | Seconds of full UFO activity; after this the on-screen saucers finish their pass but **no new ones cross** (phase A). Resets per page load. `0` = run indefinitely (no wind-down). |
| `theme_invasion_fx_fadeout` | `10` | Seconds **after** `_duration` before the remaining saucers fade out and are removed, dropping the FX layer back behind the content for readability (phase B). |

Both are passed to `mfo-theme.js` via an inline `window.MFO_THEME` global in `scripts.html`. While active the FX layer sits **above the content but below the nav** (`z-index: 2` — over `#page_content` at z1, under the navbar at z3, `pointer-events: none`) so the saucers fly over the hero/cards without covering the navbar, mobile menu, or focus outlines; after the wind-down it drops to `z-index: 0` (`--ambient`) behind the content. (`prefers-reduced-motion` keeps it behind the content the whole time.) The scene is rebuilt fresh on each activation — toggling invasion off cancels the pending wind-down and removes the layer, so toggling it back on restarts the burst.

The two header buttons are gated by `theme_toggle_enabled` / `theme_invasion_icon`
in `_includes/topnav.html`; absent buttons are simply not wired (the controller is
null-safe). The default feeds the no-flash head script.

### Immersive scene (invasion only)

`mfo-theme.js` injects `.mf-invasion-fx` (a fixed, `pointer-events:none`,
`contain:strict` layer) as the first child of `<body>`: a two-layer parallax
**starfield** (pure CSS radial-gradients) and three drifting **saucers**. Each
saucer is a nested pair (outer `.mf-ufo` = horizontal `translateX` sweep, inner
`.mf-ufo-craft` = vertical `translateY` bob) and runs a **tractor beam** pulling
an **abductee** up into its underside (the three are desynced via negative
`animation-delay`s so they don't pulse in lockstep). The craft stacks three
separate SVG layers so the abductee is sandwiched and never drawn over the saucer:

| Layer | Asset | z | Role |
|---|---|---|---|
| `.mf-craft-beam` | `invasion_Beam.svg` (2700×2303) | 0 | beam, behind the abductee |
| `.mf-abductee` | `invasion_{Makey,Mothman,Bigfoot}.svg` (600×600) | 1 | rises up the beam |
| `.mf-craft-body` | `invasion_Saucer.svg` (2700×1323) | 2 | body, **occludes** the abductee as it's drawn in |

The abductee is **weighted-random** — pool `["Makey","Makey","Mothman",
"Bigfoot"]`, so Makey is twice as likely (50% / 25% / 25%). On each abduction
loop the image is swapped (at the invisible boundary, via `animationiteration`)
to a fresh pick that **excludes the previous one**, so a saucer that pulls in a
second object shows something different (the weighting carries to the remaining
choices). All three abductee SVGs share the 2700-wide centerline, so the layers
align with no offset math.

While active the layer sits above the content but below the nav (`z-index: 2`) so
the saucers fly over the hero/cards without covering the navbar/menu; after the
wind-down (see the settings above) it drops behind the content, where the
now-saucer-less starfield shows through the slightly-translucent surfaces.

The scene is built **only on pages that have the header nav** (`#slide-nav`) — a
topnav-less layout (e.g. the schedule app, `_layouts/schedule-app.html`) inherits
the theme *colors* but never gets an immersive scene the visitor couldn't
dismiss. Gating on the nav (not the UFO button) means `/invasion/` still renders
the full scene even when the UFO icon is hidden via settings.

**Performance & a11y safeguards:** animations are strictly `transform`/`opacity`
(the UFOs use a nested element so the horizontal sweep `translateX` and the
vertical bob `translateY` compose without animating any layout property);
`prefers-reduced-motion` freezes the scene (static saucers, palette intact) and
keeps the layer behind the content; the FX trims to just the abducting saucer
≤768px; assets are five small SVGs in
`assets/images/site-branding/2026/invasion/` — no raster, no JS animation libs.
Light-mode visitors never load or build any of it.

### >>> Retiring the 2026 skin after the event <<<

1. Remove the **invasion** `<link>` from `_includes/stylesheets.html`.
2. Remove the **`#theme-toggle`** (UFO) button block from `_includes/topnav.html`.
3. Delete `assets/css/mfo-theme-invasion.css`,
   `assets/images/site-branding/2026/invasion/`, and `invasion.html` (the
   `/invasion/` shortcut page).

`assets/js/mfo-theme.js` needs no edits — with no UFO button it just wires the
sun/moon control. The **light ↔ dark** toggle, semantic tokens, neutral dark
mode, and persistence all remain. Nothing in content pages changes.

### Files

| File | Change |
|---|---|
| `assets/css/mfo-redesign.css` | **Edit** — semantic tokens in `:root`; `body` bg; split white/navy *background* uses to `--mf-surface`/`--mf-dark-bg`; `.mf-theme-toggle` button styles |
| `assets/css/mfo-theme-dark.css` | **New** — neutral dark mode (token redefinitions + small touch-ups) |
| `assets/css/mfo-theme-invasion.css` | **New (temporary)** — 2026 neon skin + immersive FX |
| `assets/js/mfo-theme.js` | **New** — toggle controller + lazy FX injection |
| `assets/images/site-branding/2026/invasion/invasion_{Saucer,Beam,Makey,Mothman,Bigfoot}.svg` + `invasion-header.jpg` | **New (temporary)** — scene art (saucer body, beam, 3 abductees) + carousel header slide |
| `invasion.html` (`/invasion/`) | **New (temporary)** — shareable shortcut: redirects home with `?theme=invasion` (no storage) |
| `_includes/head.html` | No-flash theme restore script |
| `_includes/topnav.html` | UFO toggle button (`#theme-toggle`) |
| `_includes/stylesheets.html` | Link the two theme sheets (after redesign) |
| `_includes/scripts.html` | Load `mfo-theme.js` |

## 6.18 Dark-mode image / logo audit (checklist)

Dark mode + the Invasion skin flip several formerly-white surfaces to dark
(`--mf-surface`, `--mf-gray-50`, the footer, sponsor tiles, the sponsor marquee,
promote `.mf-asset-thumb`). Any logo that is **dark ink on transparent** — or
that assumed a white backdrop — washes out or vanishes on those surfaces. Photos
and multi-color/self-contained badges are unaffected. This section is the audit
of every contrast-sensitive image and what to do about each. *(Audited
2026-06-27; raster assets visually spot-checked, not inferred from filenames.)*

### Two remediation strategies

- **A — Light "logo chip" (CSS, no new assets). PREFERRED for third-party logos.**
  Keep the logo's *immediate container* on a light/cream rounded background in
  dark/invasion (e.g. `[data-theme="dark"] .mf-sponsor-tile { background:#f4f6fb }`).
  One rule covers an entire data-driven set and survives yearly sponsor churn.
  Sponsor/partner/funding logos are designed for white, so this matches intent.
- **B — Separate reverse/dark asset variant (new file).** Only where a white chip
  would look wrong — usually first-party brand marks. Add a `-reverse`/`-white`
  PNG/SVG and swap via CSS or `<picture>` on `[data-theme]`. Higher upkeep.

> **Recommended order:** do the **A** chip fixes first (clears the large majority
> of the risk in a few CSS rules), then decide case-by-case if any first-party
> mark in **B** is worth a bespoke variant. Most items below need **A**, not new art.

### Checklist — contrast-sensitive images

**Funding logos** — `_includes/footer-notices.html` (on the now-dark footer):
- [x] `site-branding/tmef_logo_rectangle_black.png` — **VANISHES** (pure black/transparent). → **A applied** (cream chip via `img[src*="tmef_logo"]`). Optional **B**: white/reverse TMEF from the foundation.
- [x] `site-branding/26.01_OC_Logo_H-Black_RGB.png` — **VANISHES** (black/transparent). Also used on `become-a-sponsor.md`. → **A applied** (`img[src*="OC_Logo"]`, covers both pages). Optional **B**: OC's official `*_H-White_*` mark.

**Sponsor logos** — data-driven `_data/sponsors.yaml` → `assets/images/sponsors/*`, rendered on `.mf-sponsor-tile` (`sponsors-grid-modern.html`, the `/sponsors/` page) and `.mf-marquee-item` (`sponsors-marquee.html`, homepage):
- [x] **Whole set (49 logos)** — mixed: many are black-on-transparent (e.g. `EPAX-3D-Black-Logo.png`, `ftd-LogoBlack.png`, `flux.png`, `fulament.png`, `WTI_Logo.png`) or have black *sub-text* on otherwise-colored art (e.g. `skycraft_saucer_logo_wht-line-Maker.png`). → **A applied** — light chip on `.mf-sponsor-tile` (grid) and a solid light band on `.mf-marquee-viewport` (homepage strip). (Legacy `sponsors-grid*.html`/`sponsors-carousel.html` use different classes — add a chip/band there too if ever re-enabled.) Did **not** hand-make 49 variants.

**Promote / press-kit asset cards** — `pages/promote.md`, thumbs on `.mf-asset-thumb`:
- [x] `site-branding/mfo_one_line_border.png` and `mfo_two_line_border.png` — white-fill boxes; survive as white cards but look like stickers on dark. → **A applied** (`.mf-asset-thumb` kept light in dark/invasion).
- [ ] `site-branding/2025/MFO2025_Round_logo_V3_w_date.jpg` — self-contained (teal disc); fine. Verify only.
- [ ] Flyer/poster/social JPGs (`MFO2025_flyer_*`, `_poster`, `_facebook`, `_profile`) — self-contained art. **No action.**

**Footer + header brand marks:**
- [ ] `site-branding/mfo_one_line_border.png` (footer local logo, `footer.html`) — white-box mark; **legible** on dark (white card). Optional **B** reverse for elegance.
- [ ] `site-branding/mfo_two_line_border.png` (header, `topnav.html`; category OG meta) — white-box mark; **legible** (verified). Optional **B**.
- [ ] `site-branding/makerfaire-welding.webp` (footer MF mark, `menus.yaml`) — red art on transparent; **reads on dark** (verified). Low priority.

**Mascot / badge graphics:**
- [ ] `site-branding/makey.png` (`makey-border.html`, schedule fallbacks) — solid **red**, reads on dark. No action (note: Invasion has its own `invasion/invasion_Makey.svg`).
- [ ] `site-branding/call-for-makers.png` (`call-for-makers-widget.html`) — self-contained navy badge; fine. No action.
- [ ] `site-branding/makey-vortex-sm2.gif` (`404.md`) — verify it reads on dark (404 was recently restyled). Likely fine.

**Print-only pages (always light — flag, low priority):**
- [ ] `pages/table-signs.md` QR codes (`*_qr_code*.png`, black/transparent) and the table-sign header — print/table context, effectively always light. Only matters if viewed on screen in dark mode.

**No action (confirmed safe):** carousel/hero/slider photos, `.mf-card-media` category & get-involved photos, stage portraits, exhibit images, favicons (browser chrome), the `2026/bottom-footer.png` banner (self-contained), and the Invasion `invasion_*.svg` scene art (theme-specific, designed for dark).

### Implementation status — Strategy A DONE (2026-06-27)

The logo-chip rules are live in both theme sheets (look for the "Logo chips"
block in `mfo-theme-dark.css` and `mfo-theme-invasion.css`):
- **Grid/card logos** → light chip on `.mf-sponsor-tile` + `.mf-asset-thumb`
  (`#f4f6fb` dark / `#ffffff` invasion), plus the funding logos via
  `img[src*="tmef_logo"]` / `img[src*="OC_Logo"]`.
- **Sponsor marquee** → a single solid light **band** on `.mf-marquee-viewport`
  (not per-logo chips), so the scrolling strip reads as one clean row; its
  title/subtitle stay on the dark section above. Invasion adds a faint lime glow.

This clears every sponsor logo + both funding logos + promote thumbs in one pass.
**Still open (optional, Strategy B):** bespoke reverse/white variants for the
first-party MFO header/footer marks — only if the white-card look is unwanted.
The legacy sponsor includes (`sponsors-grid*.html`, `sponsors-carousel.html`)
use different classes and would need their own chip rule if re-enabled.

## 7. Decisions / Open Questions Log

- **2026-06-12** — Scope = full modernization; fidelity = match closely. (User)
- **2026-06-12** — Reference changed from makerfaire.com landing page to the
  **Bay Area event page** (`/bay-area/?2026`); it's an event page like MFO. This
  flipped the palette from yellow/black to **navy/charcoal + white + coral CTA**.
  (User)
- **2026-06-13** — Accent set to **`#DB2B2F`** (makerfaire.com red), per user,
  and the token renamed `--mf-coral` → **`--mf-red`** (`--mf-red-dark` =
  `#B82328`) across `mfo-redesign.css`. (User)
- **OPEN** — Confirm exact navy hex and official font names from brand guide.
- **OPEN** — Retain a hint of legacy MFO blue as a tertiary accent, or go pure
  navy/coral? (Currently leaning pure.)
- **2026-06-13** — Retire flag-banner **entirely** (`display:none`), not the
  thin coral rule. (User)
- **2026-06-13** — **DESIGN RULE: no text overlaid on the main carousels** —
  they are imagery only by **default**. (User)
- **2026-06-27** — Hero overlay **capability restored as opt-in** (User): the
  `.mf-hero-overlay` markup (`_includes/carousel.html`) + CSS (§4) are back, but
  gated on a page setting `hero-title`. With no page setting it, carousels stay
  imagery-only (the default rule above still holds); pages can opt in to hero
  text (`hero-title`, `hero-meta`/`hero-meta-event`, `hero-cta-text`+`hero-cta-url`).
  Full front-matter syntax + example: [content-authoring.md](content-authoring.md)
  → "Hero overlay".
- **2026-06-27** — **FAQ accordion** styling retained (User): re-homed from
  `mfo-style.css` into `mfo-redesign.css` (§4b) and re-branded from legacy blue
  to the navy/coral palette. Markup: `<details class="faq-item">` with
  `.faq-question` / `.faq-answer` inside a `.faq-container`.
- **OPEN** — Adopt the structural event-page patterns (category cards, Get
  Involved role cards)? Tracked as stretch items S1/S2.
- **2026-06-27** — **Theme system added** (User, branch `dark-mode`): UFO toggle
  in the header cycling **light → 2026 "Maker Invasion" neon skin → neutral dark
  → light**. Architected in two layers — a *permanent, brand-agnostic dark mode*
  plus a *removable 2026 neon skin* with an immersive UFO/Makey scene — so the
  fun look reverts to a clean dark mode after the event by deleting one file +
  one link + one JS entry. Implemented via a thin semantic-token layer
  (`--mf-bg`/`--mf-surface`/`--mf-dark-bg`) over the existing `--mf-*` tokens;
  light mode is unchanged. Full spec: **§6.17**.
- **2026-06-28** — **Session-only persistence; default light** (User): no
  long-term persistence (all `localStorage` removed). The active theme is kept in
  `sessionStorage`, so it sticks across reloads/navigation within the tab but a
  new session starts at `theme_default` (set to `light`). The 2026 skin is turned
  on by visiting `/invasion/` (sets the session value + bounces home). Net: visit
  `/invasion/` → stays in invasion for that session; close/reopen → back to light.
  Full spec: **§6.17**.

---

## 8. Rollback

The redesign is additive. To revert: remove the `mfo-redesign.css` `<link>`
(and restore Roboto font links) in `_includes/stylesheets.html`. No legacy CSS
is deleted.

---

## 9. Resume Here (paused 2026-06-13)

**Where things stand:** branch `redesign`, not merged. All work above is
browser-verified. `mfo-redesign.css` is the single override stylesheet (loaded
last); reusable components now exist for cards (`.mf-card` / `.mf-info-grid` /
`.mf-card-grid--3up`), download cards (`.mf-asset-*`), hashtag chips, sponsor
marquee/grid, prose bands (`.mf-prose-section`), and a centered page header
(`.mf-page-header`).

**Preview:** `.\serve-fast.ps1` → http://localhost:4000 (see
[build-deploy.md](build-deploy.md)). For headless visual checks during dev I've
used Edge `--headless=new --screenshot` against a local static server of `_site`.

**Open / next steps:**
- **Open questions (§7):** confirm exact navy hex + official fonts from the brand
  guide; decide on a legacy-blue tertiary accent (leaning pure navy/red).
- **2025 → 2026 content:** the promote page assets/paths and `#MFO2025` hashtag
  still say 2025 (see §6.13); `sponsor_year` is 2025 while `event_year` is 2026.
  Bump when 2026 materials exist. The Stage card image is `stage-talks-2025.jpg`.
- **Pages not yet restyled to the new pattern:** `attend.md`,
  `become-a-sponsor.md`, and `field-trip-day.md` are now done (§6.16). Remaining
  candidates to audit for the full-width hero + prose/section treatment:
  `educators.md`, `power-racing.md`, `stage.md`, `program.md`, `maker-manual.md`,
  `badge.md`, and the schedule pages. (`about.md` was deleted 2026-06-13,
  finally matching §6.8.)
- **Exhibits grid / Isotope (deferred — own branch):** assessment + options in
  **§10**. Not part of the `redesign` branch; tackle on a dedicated branch.
- **Merge plan:** eventually merge `redesign` → `master` (GitHub Pages serves
  `master`). Do a **full** build (`_config.yml` only) before merging to catch
  anything the fast/dev config hides (exhibit images, JSON feeds).
- **Reminder:** carousels stay imagery-only (no text overlay — §7 rule).

---

## 10. Exhibits grid / Isotope — assessment (DEFERRED to its own branch)

> **Status: IN PROGRESS on branch `isotope-rework` (2026-06-27).** Option **C
> (Muuri)** chosen — to keep the masonry/collage feel + shuffle while dropping
> the jQuery-Isotope dependency (a head start on the eventual Bootstrap-3/jQuery
> migration). **Exhibits grid: migrated to Muuri** (`assets/js/exhibits-muuri.js`,
> vanilla; masonry via `fillGaps`, shuffle via Fisher-Yates `grid.sort`, quick
> search via `grid.filter` with a plain substring — no more regex pitfall,
> lazy-loaded images with `aspect-ratio` so layout doesn't jump; the visual card
> moved to `.item-content` so it doesn't fight Muuri's transform; old
> `exhibits-isotope.js` deleted; `#exhibits-no-results` message added).
> **Still on Isotope: the schedule** (`schedule-isotope.js`) — migrate next, then
> Isotope/imagesLoaded can be dropped entirely. The analysis below is the
> original pre-work assessment.

**Current setup:** `/exhibits/` (layout `category`, `pages/exhibits.md`) renders
all exhibits (~194 of 293 cards; `R`-prefixed combat robots excluded) via
`_includes/exhibit-card.html` into `#exhibits`, then **Isotope v3** (masonry,
`gutter:20`, `isFitWidth`) + **imagesLoaded v4** + **jQuery 1.12.4** lay it out
(`assets/js/exhibits-isotope.js`, loaded by `scripts.html` when
`page.isotope-exhibits`). Category filtering **navigates** to server-rendered
`/exhibits/categories/<slug>/` pages (the `.filters-select` dropdown redirects);
Isotope itself only does layout + quicksearch (regex over card text, debounced) +
shuffle.

**Doing well:**
- Category filtering via real server-rendered pages → shareable URLs, SEO,
  works without JS. (Isotope isn't doing the category filtering.)
- Single `isotope('layout')` on `window.load` (replaced an imagesLoaded
  `.progress()` that fired hundreds of times — see the code comment).
- `width`/`height` on card images (good for CLS).
- Debounced quicksearch.

**Issues / quick wins (keep Isotope):**
1. **No image lazy-loading** — ~200 full images load eagerly on one page. Add
   `loading="lazy"` + `decoding="async"` to the `exhibit-card.html` img. Biggest
   perceived-speed win. *(Caveat: lazy + masonry → relayout jank on scroll; see
   grid note below.)*
2. **Bug:** stray `}s` at `exhibits-isotope.js:149`, and the entire **schedule**
   filter block (lines ~160–203) is dead code living in the *exhibits* file
   (schedule pages load `schedule-isotope.js`). Plus many commented experiments.
3. **Quicksearch regex not escaped** (line ~92): typing `(`, `[`, `*` builds an
   invalid `RegExp` and breaks search. Escape input or use `.includes()`.
4. **No "no results" message** on empty search.
5. **Aging stack:** jQuery 1.12.4 (2016) + Isotope-as-jQuery-plugin. Can't drop
   jQuery yet — **Bootstrap 3 depends on it** (couple this with a Bootstrap
   migration). Isotope is also **GPLv3-or-commercial** (low risk on a public
   nonprofit repo; note if ever closed-source).

**Strategic options (effort order):**
- **A — Keep Isotope, just fix the above.** Lowest risk, good ROI now.
- **B — CSS Grid + ~30 lines vanilla JS** (search/shuffle). Best long-term
  endgame for a static site: no layout lib, no license question, smooth with
  lazy-loading; category filtering already server-side. Pairs with the
  jQuery/Bootstrap-3 migration. **Recommended direction.**
- **C — Maintained modern lib** if the animated reflow/shuffle feel matters:
  **Muuri** (MIT, no jQuery, closest to Isotope) or **Shuffle.js** (vanilla).

**Plan:** do **A** (lazy-load + bug/cleanup + regex escape) on the new branch as
a fast win; keep **B** for the Bootstrap-3/jQuery modernization. Don't rip out
Isotope just to rip it out — it works.
