# Maker Faire Orlando — Brand Redesign (2026)

> Living document. Captures the concepts, decisions, design tokens, and task
> list for bringing the MFO site in line with the current Maker Faire event-page
> brand. Update this file as work progresses.

**Last updated:** 2026-06-13
**Status:** **PAUSED 2026-06-13** (work resumes later). On branch `redesign`,
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
  they are imagery only. Reverses the original "hero overlay" (task #4); the
  `.mf-hero-overlay` markup + CSS (§4) and all `hero-*` front matter were
  removed. Page titles/taglines live in the content sections below. (User)
- **OPEN** — Adopt the structural event-page patterns (category cards, Get
  Involved role cards)? Tracked as stretch items S1/S2.

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
- **Pages not yet restyled to the new pattern:** audit remaining `pages/*.md`
  (e.g. `attend.md`, `become-a-sponsor.md`, `field-trip-day.md`, schedule pages)
  for the full-width hero + prose/section treatment.
- **Merge plan:** eventually merge `redesign` → `master` (GitHub Pages serves
  `master`). Do a **full** build (`_config.yml` only) before merging to catch
  anything the fast/dev config hides (exhibit images, JSON feeds).
- **Reminder:** carousels stay imagery-only (no text overlay — §7 rule).
