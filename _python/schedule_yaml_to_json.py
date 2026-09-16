"""Convert _data/schedule.yaml to _data/schedule.json without touching a timestamp.

The whole point of this script is the loader choice. yaml.SafeLoader coerces
`date: 2025-11-07 10:00:00` into a Python datetime, and anything that then writes
it back out has to pick a format and a zone -- which is exactly the bug that made
the old schedule-editor shift every session by 4-5 hours. BaseLoader returns every
scalar as a str, so the timestamp survives as the literal text that was typed.
There are no booleans or numbers in this file, so nothing else is harmed by that.

--check re-reads the emitted JSON and asserts every date/enddate is byte-identical
to the text that followed `date:`/`enddate:` in the YAML. That is the converter
proving it did not touch a timestamp, rather than us assuming it.
"""

import argparse
import io
import json
import os
import re
import sys

import yaml

# Key order the site's YAML reads in, kept so the git diff on the website repo is
# readable -- which is the only reason anyone will ever open that file.
KEY_ORDER = ["title", "slug", "location", "description", "date", "enddate",
             "image", "url", "guests"]
GUEST_ORDER = ["name", "url", "image"]

# A parked image: `#image: /assets/...` or `#image: in the queue for graven`.
# Commenting the line out is how the current file says "not ready yet".
PARKED = re.compile(r"^\s*#\s*image:\s*(.+?)\s*$")
ITEM = re.compile(r"^-\s")


def parked_notes(text):
    """Map event index -> the parked #image: text sitting inside that event block."""
    notes, idx = {}, -1
    for lineno, line in enumerate(text.splitlines(), 1):
        if ITEM.match(line):
            idx += 1
        m = PARKED.match(line)
        if m and idx >= 0:
            notes.setdefault(idx, []).append((lineno, m.group(1)))
    return notes


def ordered(event, order):
    out = {}
    for k in order:
        v = event.get(k)
        if v is None or v == "" or v == []:
            continue
        out[k] = v
    for k in sorted(event):
        if k not in out and k not in order:
            v = event[k]
            if v not in (None, "", []):
                out[k] = v
    return out


def convert(text):
    events = yaml.load(text, Loader=yaml.BaseLoader)
    if not isinstance(events, list):
        raise SystemExit("schedule.yaml is not a list of events")
    out = []
    for ev in events:
        ev = dict(ev)
        guests = ev.get("guests") or []
        ev["guests"] = [ordered(dict(g), GUEST_ORDER) for g in guests if (g or {}).get("name")]
        out.append(ordered(ev, KEY_ORDER))
    return out


def raw_timestamps(text):
    """Every `date:`/`enddate:` value as literal text, in file order."""
    found = []
    for line in text.splitlines():
        m = re.match(r"^\s{2}(date|enddate):\s*(.+?)\s*$", line)
        if m:
            found.append((m.group(1), m.group(2)))
    return found


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--site", default=r"C:\Users\ianco\GitHub\mfo-static-website")
    ap.add_argument("--out", default=None)
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    src = os.path.join(args.site, "_data", "schedule.yaml")
    with io.open(src, encoding="utf-8") as f:
        text = f.read()

    events = convert(text)

    notes = parked_notes(text)
    if notes:
        print("Parked #image: lines found (these become imageNote in the builder,")
        print("and are NOT exported to the site):")
        for idx in sorted(notes):
            for lineno, val in notes[idx]:
                title = events[idx].get("title", "?") if idx < len(events) else "?"
                print("  line %-4d  event %-2d  %-38s  %s" % (lineno, idx, title[:38], val))
        print()

    # The check: literal text in, literal text out.
    raw = [v for _, v in raw_timestamps(text)]
    emitted = []
    for ev in events:
        for k in ("date", "enddate"):
            if k in ev:
                emitted.append(ev[k])
    bad = [(a, b) for a, b in zip(raw, emitted) if a != b]
    if len(raw) != len(emitted) or bad:
        print("TIMESTAMP CHECK FAILED", file=sys.stderr)
        print("  yaml had %d, json has %d" % (len(raw), len(emitted)), file=sys.stderr)
        for a, b in bad[:10]:
            print("  %r != %r" % (a, b), file=sys.stderr)
        return 1
    print("timestamp check: %d date/enddate values byte-identical" % len(raw))

    if args.check:
        return 0

    dst = args.out or os.path.join(args.site, "_data", "schedule.json")
    with io.open(dst, "w", encoding="utf-8", newline="\n") as f:
        json.dump(events, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print("wrote %s  (%d events)" % (dst, len(events)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
