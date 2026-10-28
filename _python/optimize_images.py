#!/usr/bin/env python
"""
Generate web-sized WebP variants for the images the site actually references.

Originals are never touched -- each variant is written alongside its source as
<stem>-<N>w.webp (or -<N>h.webp for logos, which are sized by height). Re-runs
skip any variant already newer than its source, so this is safe to run again.

The reference lists are SCANNED from content rather than hard-coded, so adding a
carousel slide or swapping a sponsor logo is picked up automatically next run.

Usage:
    python optimize_images.py            # generate what's missing
    python optimize_images.py --force    # rebuild every variant
    python optimize_images.py --dry-run  # list the work without doing it
"""

import argparse
import glob
import os
import re
import sys

import yaml                                  # pip install pyyaml
from PIL import Image, ImageOps              # pip install pillow (not pil)

# Repo root, regardless of where this is run from.
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Sources at or below this size aren't worth a variant -- the WebP would often
# be larger than the original (already-optimized logos, small PNGs, .avif).
MIN_SOURCE_BYTES = 25 * 1024

QUALITY = 82          # photos
QUALITY_ALPHA = 90    # logos keep their edges crisp

# How wide each consumer actually draws its images: cards are ~370px (740 @2x),
# the carousel is full-bleed but capped at 600px tall, featured-maker thumbs are
# ~280px (560 @2x), marquee logos sit about 150px tall (300 @2x).
TIER_CAROUSEL = 1600
TIER_CARD = 800
TIER_FEATURED = 600
TIER_LOGO_HEIGHT = 300


def rel(path):
    """Repo-relative path, for display."""
    return os.path.relpath(path, ROOT).replace("\\", "/")


def abspath(url):
    """/assets/images/foo.jpg -> absolute path on disk."""
    return os.path.join(ROOT, url.lstrip("/").replace("/", os.sep))


# --------------------------------------------------------------------------
# Reference scanners -- each returns a set of site-absolute /assets/... URLs
# --------------------------------------------------------------------------

def front_matter(path):
    """Parse a Jekyll page's YAML front matter, or None."""
    try:
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
    except OSError:
        return None
    if not text.startswith("---"):
        return None
    try:
        return yaml.safe_load(text.split("---")[1])
    except yaml.YAMLError:
        return None


def carousel_slides():
    """Every image used as a carousel slide, across every page that has one."""
    found = set()
    pages = [os.path.join(ROOT, "index.md")]
    pages += sorted(glob.glob(os.path.join(ROOT, "pages", "*.md")))
    for page in pages:
        data = front_matter(page)
        if not data or not data.get("carousel"):
            continue
        for slide in data.get("carousel-slides") or []:
            if isinstance(slide, dict) and slide.get("image"):
                found.add(source_for(slide["image"]))
    return found


# background-image: url('/assets/...') -- bare, or wrapped in a Liquid filter
# as url({{ '/assets/...' | relative_url }}), which is how the includes write it.
BACKGROUND_RE = re.compile(
    r"background-image:\s*url\([^/)]*(/assets/images/[^'\"()\s|]+)")


def card_backgrounds():
    """
    Every image used as a .mf-card-media style background -- the card includes
    plus the page bodies, which hand-roll the same pattern. These are CSS
    backgrounds, so they can never be lazy-loaded; size is the only lever.
    """
    files = [os.path.join(ROOT, "_includes", n) for n in
             ("category-cards.html", "get-involved-cards.html")]
    files.append(os.path.join(ROOT, "index.md"))
    files += sorted(glob.glob(os.path.join(ROOT, "pages", "*.md")))

    found = set()
    for path in files:
        try:
            with open(path, encoding="utf-8") as fh:
                found.update(source_for(u) for u in BACKGROUND_RE.findall(fh.read()))
        except OSError:
            pass
    return found


# Image extensions we'll accept as an original, best first.
SOURCE_EXTS = (".jpg", ".jpeg", ".png", ".tif", ".tiff", ".bmp", ".webp")


def _first_existing(stem, skip=None):
    """First real file matching stem + a known image extension."""
    for ext in SOURCE_EXTS:
        for candidate in (stem + ext, stem + ext.upper()):
            path = abspath(candidate)
            if os.path.exists(path) and path != skip:
                return "/" + rel(path)
    return None


def source_for(url):
    """
    Resolve a reference back to the best original to resize from.

    Content files point at our generated variants once they've been updated, so
    this has to be reversible or a re-run would try to shrink a variant. Handles
    both of our naming shapes:
        .../devusol-300h.webp            -> .../devusol.png
        .../planes-1024x690.jpeg         -> .../planes-full.jpeg
    Falls back to the url itself when no better original is on disk.
    """
    # One of our own variants -- strip the tier suffix and find the original.
    stem = re.sub(r"-\d+[wh]\.webp$", "", url)
    if stem != url:
        found = _first_existing(stem) or _first_existing(stem + "-full")
        if found:
            return found
        return url

    # An exhibit thumbnail -- prefer its full-resolution sibling.
    stem = re.sub(r"-\d+x\d+\.\w+$", "", url)
    if stem != url:
        found = _first_existing(stem + "-full")
        if found:
            return found
    return url


def featured_makers():
    """
    The homepage featured-maker images. Resolves each entry the way
    _includes/featured-makers-grid.html does: the data-file `image:` override
    when present, else the exhibit's own image-primary.large.url.
    """
    path = os.path.join(ROOT, "_data", "featured-exhibits.yaml")
    try:
        with open(path, encoding="utf-8") as fh:
            data = yaml.safe_load(fh)
    except OSError:
        return set()

    # exhibit-id -> front matter, for the entries with no override.
    exhibits = {}
    for md in glob.glob(os.path.join(ROOT, "_exhibits", "*.md")):
        fm = front_matter(md)
        if fm and fm.get("exhibit-id"):
            exhibits[str(fm["exhibit-id"])] = fm

    found = set()
    for entry in (data or {}).get("homepage") or []:
        url = entry.get("image")
        if not url:
            fm = exhibits.get(str(entry.get("exhibit-id")), {})
            url = (fm.get("image-primary") or {}).get("large", {}).get("url")
        if url:
            found.add(source_for(url))
    return found


def sponsor_logos():
    """Logos for sponsors currently marked active."""
    path = os.path.join(ROOT, "_data", "sponsors.yaml")
    try:
        with open(path, encoding="utf-8") as fh:
            data = yaml.safe_load(fh)
    except OSError:
        return set()
    return set(
        source_for("/assets/images/sponsors/" + s["logo"])
        for s in (data or {}).get("sponsors") or []
        if str(s.get("active")).lower() == "true" and s.get("logo")
    )


def event_shirt():
    """The event shirt promo image."""
    path = os.path.join(ROOT, "_includes", "event-shirt.html")
    try:
        with open(path, encoding="utf-8") as fh:
            return set(source_for(u) for u in
                       re.findall(r'src="(/assets/images/[^"]+)"', fh.read()))
    except OSError:
        return set()


# --------------------------------------------------------------------------
# Variant generation
# --------------------------------------------------------------------------

def variant_path(src_abs, size, by_height):
    """
    Variant name next to the source. A sized source contributes only its base
    name, so ...-image-1-1024x1024.png yields ...-image-1-600w.webp rather than
    carrying the old dimensions through.
    """
    stem = os.path.splitext(src_abs)[0]
    stem = re.sub(r"-(?:\d+x\d+|full)$", "", stem)
    return "%s-%d%s.webp" % (stem, size, "h" if by_height else "w")


def build(url, size, by_height=False, force=False, dry_run=False):
    """Make one variant. Returns a result tuple on success, else a reason."""
    src = abspath(url)
    if not os.path.exists(src):
        return "missing source"
    if os.path.getsize(src) < MIN_SOURCE_BYTES:
        return "source already small"

    dst = variant_path(src, size, by_height)
    if (not force and os.path.exists(dst)
            and os.path.getmtime(dst) >= os.path.getmtime(src)):
        return "skipped"

    try:
        with Image.open(src) as im:
            im = ImageOps.exif_transpose(im)
            measure = im.height if by_height else max(im.width, im.height)
            if measure <= size:
                return "already smaller than target"

            has_alpha = im.mode in ("RGBA", "LA") or (
                im.mode == "P" and "transparency" in im.info)

            # thumbnail() preserves aspect ratio and never upscales.
            box = (im.width, size) if by_height else (size, size)
            im.thumbnail(box, Image.LANCZOS)

            if dry_run:
                return "would write"

            if has_alpha:
                # Which of lossy/lossless wins depends entirely on the artwork:
                # flat-colour logos compress better lossless, photographic ones
                # with a cut-out background much better lossy. Try both and keep
                # the smaller file rather than guessing.
                im = im.convert("RGBA")
                candidates = [
                    {"lossless": True, "method": 6},
                    {"quality": QUALITY_ALPHA, "method": 6},
                ]
                attempts = []
                try:
                    for n, params in enumerate(candidates):
                        tmp = "%s.try%d" % (dst, n)
                        im.save(tmp, "WEBP", **params)
                        attempts.append((os.path.getsize(tmp), tmp))
                    attempts.sort()
                    os.replace(attempts[0][1], dst)
                finally:
                    for _, tmp in attempts[1:]:
                        if os.path.exists(tmp):
                            os.remove(tmp)
            else:
                im = im.convert("RGB")
                im.save(dst, "WEBP", quality=QUALITY, method=6)
    except Exception as exc:                  # report and keep going
        return "ERROR: %s" % exc

    src_b, dst_b = os.path.getsize(src), os.path.getsize(dst)

    # Re-encoding doesn't always pay -- a small lossless logo can come out
    # bigger than its PNG. Throw the variant away so the caller keeps using
    # the original rather than shipping a regression.
    if dst_b >= src_b:
        os.remove(dst)
        return "variant not smaller"

    return ("written", src_b, dst_b)


def main():
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--force", action="store_true", help="rebuild every variant")
    ap.add_argument("--dry-run", action="store_true", help="list work only")
    args = ap.parse_args()

    jobs = [
        ("carousel slides",  carousel_slides(),  TIER_CAROUSEL,    False),
        ("card backgrounds", card_backgrounds(), TIER_CARD,        False),
        ("featured makers",  featured_makers(),  TIER_FEATURED,    False),
        ("event shirt",      event_shirt(),      TIER_CARD,        False),
        ("sponsor logos",    sponsor_logos(),    TIER_LOGO_HEIGHT, True),
    ]

    written = skipped = failed = 0
    before = after = 0

    for label, urls, size, by_height in jobs:
        print("\n%s  (%d referenced, target %d%s)"
              % (label, len(urls), size, "px tall" if by_height else "px"))
        if not urls:
            print("   nothing referenced")
            continue
        for url in sorted(urls):
            result = build(url, size, by_height, args.force, args.dry_run)
            if isinstance(result, tuple):
                _, src_b, dst_b = result
                written += 1
                before += src_b
                after += dst_b
                print("   %7.0f KB -> %6.0f KB  (-%2.0f%%)  %s"
                      % (src_b / 1024, dst_b / 1024,
                         100.0 * (src_b - dst_b) / src_b,
                         rel(variant_path(abspath(url), size, by_height))))
            elif result == "skipped":
                skipped += 1
            elif result == "missing source" or result.startswith("ERROR"):
                failed += 1
                print("   !! %-26s %s" % (result, url))
            else:
                print("   -- %-26s %s" % (result, url))

    print("\n" + "=" * 64)
    print("written %d   skipped %d   failed %d" % (written, skipped, failed))
    if before:
        print("source %.2f MB -> variants %.2f MB  (saves %.2f MB, -%.0f%%)"
              % (before / 1048576, after / 1048576,
                 (before - after) / 1048576,
                 100.0 * (before - after) / before))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
