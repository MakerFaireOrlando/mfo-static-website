# Image Storage Plan

**Status:** Planned / not yet started. Tracked in GitHub issue (see below).

This documents a future change to how exhibit images are stored, plus a one-time
git-history cleanup. It is **not implemented yet** — this file is the plan of
record so we can pick it up on another day.

Related: [Exhibit Pipeline](exhibit-pipeline.md) · script
[`_python/update_exhibits.py`](../_python/update_exhibits.py)

---

## The problem

The importer downloads each exhibit's images and resizes them into responsive
variants (`full` / `large` / `medium` / `small`) using Pillow, writing them into
[`assets/images/exhibit-images/`](../assets/images/exhibit-images/). Those files
are committed to git.

Two facts make this expensive over time:

1. **Images are wiped and regenerated each event year** (previous years' images
   are deleted the next year). They are fully **regenerable** from the JotForm
   source images, so they have no archival value in git history.
2. **Deleting files in a normal commit does not reclaim space.** Every image blob
   ever committed stays in history forever. As of 2026-07 the `.git` directory
   is **~4.1 GB** (working tree holds ~996 image files for the current year).

So the repo grows without bound, and the annual "wipe" does nothing to shrink it.

Image filenames are prefixed by the 2-digit event year via the JotForm exhibit ID
(e.g. `26-11-e-chipscapes-…`), so prior years are cleanly targetable as
`25-*`, `24-*`, etc.

---

## Part 1 — One-time history cleanup (reclaim the ~4.1 GB)

Rewrite history to strip the image blobs. Because the images are regenerable,
this is low-risk archivally. Use
[`git-filter-repo`](https://github.com/newren/git-filter-repo) (modern,
GitHub-recommended; `git filter-branch` is deprecated).

```bash
pip install git-filter-repo

# 1. BACK UP FIRST — a full mirror you can restore from
git clone --mirror . ../mfo-backup.git

# 2. Remove the entire image directory from ALL history
git filter-repo --path assets/images/exhibit-images/ --invert-paths

# 3. Reclaim space locally
git reflog expire --expire=now --all
git gc --prune=now --aggressive

# 4. Force-push the rewritten history
git push origin --force --all
git push origin --force --tags
```

Then re-run the importer with `-o rebuild` to regenerate the current year's
images and commit them once.

To keep the current year in place and strip only prior years instead, replace
step 2 with repeated globs:
`git filter-repo --invert-paths --path-glob 'assets/images/exhibit-images/25-*' --path-glob 'assets/images/exhibit-images/24-*' …`

(BFG Repo-Cleaner is a friendlier alternative: `bfg --delete-folders exhibit-images`
or `bfg --strip-blobs-bigger-than 100K`.)

### Caveats — this is destructive and not reversible
- **Every commit hash changes.** Anyone with a clone must re-clone. Confirm no
  open forks/PRs depend on old SHAs first.
- **Force-push required** — an outward-facing, hard-to-undo action. Do not run
  without explicit confirmation.
- GitHub may retain the old objects server-side until its own GC runs; the remote
  size can lag before it drops.

---

## Part 2 — Sustainable fix: stop tracking images in git

So this becomes a one-time cleanup rather than an annual ritual, move images out
of the repo entirely:

- Store resized images in an **external object store + CDN** (Cloudflare R2 /
  Azure Blob / S3). The Jekyll site references the CDN URLs instead of repo paths.
- The importer **uploads** the resized variants to the bucket instead of writing
  them into `assets/images/exhibit-images/`.
- Benefits:
  - git never bloats again — no future history surgery.
  - "Wipe last year" = delete a bucket folder/prefix. Done.
  - Drops in cleanly with the planned **GitHub Actions** migration of the
    importer (the Action uploads to the bucket; only the generated `_exhibits/*.md`
    and `_categories/*.md` get committed).

### Open decisions for implementation day
- Which store/CDN (R2 vs Azure Blob vs S3) — cost, existing org accounts.
- URL scheme / bucket layout (per-year prefix mirrors current naming).
- How the importer authenticates to the bucket (secret in env / Actions secret).
- Migration of the current year's images to the bucket, or just regenerate.

---

## Suggested sequence

1. One-time `git-filter-repo` cleanup (Part 1) to reclaim the ~4.1 GB.
2. Move images to external store (Part 2), ideally alongside the GitHub Actions
   migration of `update_exhibits.py`, so it never has to be repeated.
