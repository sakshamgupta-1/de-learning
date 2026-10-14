# Guide for AI agents (and humans) editing DE Learning

Read this whole file before changing anything. It describes how the site is built and the rules that keep it consistent.

## What this project is

A static, dependency-free study site for data engineering interview prep. Readers are experienced engineers preparing for Lead Data Engineer / Data Architect interviews. Content must be **technically correct, concise and interview-oriented**.

## Hard constraints

- **No build step, no frameworks, no package manager.** Plain HTML, one shared `styles.css`, and inline `<script>` per page.
- **No new external hosts.** Fonts come from Google Fonts only. Don't add CDNs, analytics, trackers, iframes or remote images. Embed images as inline SVG.
- **Every page is self-contained** apart from `styles.css` and links to other pages.
- **Works offline and from `file://`.** No `fetch()` of local files.
- **Light and dark themes.** Use only the CSS tokens defined in `:root` in `styles.css` (`--bg`, `--fg`, `--accent`, `--blue`, `--ok`, `--warn`, `--bad`, and their `-soft` variants). Never hard-code a colour in a page or an SVG.
- **Phone width (~400 px) must work.** Wide diagrams and tables go inside `.fig` / `.tbl` containers, which scroll horizontally on their own.

## Module structure: overview first, depth on demand

This is the core content directive. Every topic is taught as a **module**: one short **overview page** that works as a refresher, plus optional **sub-pages** for depth. A returning reader should get the essentials from the overview alone. A first-time reader follows the links down as far as they need.

Hierarchy: **Area** (e.g. Spark Core) → **Module** (e.g. Architecture & memory) → **Sub-pages**.

### Folder layout

```
index.html                        hub + topic tracker (topic data lives in the GROUPS array)
styles.css                        shared tokens + components
scripts/check.py                  validation run in CI
<area>/
  index.html                      area landing: modules in learning order, one line each
  <module>/
    index.html                    overview (required)
    deep-dive.html                optional sub-pages, see table below
    examples.html
    use-cases.html
    production.html
```

Folder names are short, lowercase and hyphenated: `spark/architecture/`, `streaming/watermarks/`, `delta/merge-and-cdc/`.

### The overview page (required)

A refresher, readable in about **10 minutes**. It must make sense without opening any sub-page. In this order:

1. **What it is and why it matters**: 2–3 short paragraphs.
2. **One core diagram** showing the mechanism.
3. **Key facts**: a cheat-sheet table of the defaults, configs and comparisons people forget.
4. **Say it in an interview**: one to three short answers.
5. **Quick check**: 3–5 questions with hidden answers.
6. **Go deeper**: one card per existing sub-page, each with a one-line description of what's in it.
7. **Mark this module's topics** (`#mine`) and module-level previous/next links.

Keep calculators, steppers and long scenario walkthroughs on sub-pages unless one is central to understanding the topic.

### Sub-pages (optional: create only what has real substance)

| Type | File | What goes in it |
| --- | --- | --- |
| Deep dive | `deep-dive.html` | Internals, edge cases, config details, version differences |
| Examples | `examples.html` | Runnable code, `explain()` output, worked numbers, interactive demos and calculators |
| Real-world use cases | `use-cases.html` | Advanced patterns at scale, design trade-offs, how the topic appears in system-design rounds |
| Production issues | `production.html` | Common failures and mitigations. Each issue follows: symptom → why it happens → how to confirm → fix → how to prevent → interview answer |

Don't create stub or "coming soon" sub-pages. A simple topic may have only an overview and one sub-page. Each sub-page goes deeper than the overview; it doesn't repeat it. Link back to the overview for the basics.

### Navigation on every module page

- A **breadcrumb**: `Hub › Area › Module › Sub-page`.
- A **module tab bar**: `Overview · Deep dive · Examples · Use cases · Production`. List only the pages that exist, and mark the current one with `aria-current="page"`.
- Pages in folders reference shared files relatively: `../../styles.css`, `../../index.html`, `../index.html`.

### Tracker links

Link a topic to the module overview by default. Link to a sub-page anchor (`spark/tuning/production.html#skew`) when the topic is mainly taught there.

### Migrating the existing Spark Core pages

The four `spark-*.html` pages at the repo root predate this structure; each one mixes overview and depth. Split them into `spark/<module>/` **one module per PR**. Until then, don't add new content in the old layout. When a page moves:

- Leave a small redirect page at the old path (`<meta http-equiv="refresh" content="0; url=spark/architecture/">` plus a plain link) so bookmarks and shared links keep working.
- Update every tracker link in `index.html` that pointed to the old page. Keep the `GROUPS` order unchanged.
- Keep existing section ids where the content lands, so anchors still resolve.

## Page skeleton

Copy the closest existing page as a starting point. Every content page has:

1. `<header class="top">` with the site nav, then the breadcrumb and module tab bar described above.
2. Eyebrow (`Spark Core · Module N of M`), `h1`, `.lede`, and a `.toc` row of in-page anchor links when the page has more than three sections.
3. Content `<section id="...">` blocks. Section ids may be linked from `index.html` or other pages, so **don't rename existing ids**.
4. A `Check yourself` / `Quick check` section (`.qa` with `<details>` items).
5. On overview pages: the `Mark this module's topics` block (`#mine`) driven by the page script.
6. `<nav class="next">` with previous/next links (module level on overviews; back to the overview on sub-pages).

Reusable components (all styled in `styles.css`):

| Need | Use |
| --- | --- |
| Diagram | `<div class="fig"><svg viewBox=...>` using classes `bx`, `bxa`, `bxb`, `bxo`, `bxr`, `ln`, `lna`, `lnb`, `t`, `tb`, `th`, `ts`, `tm` |
| Interview answer | `<div class="callout say"><div class="lbl">Say it in an interview</div>…</div>` |
| Common mistake | `<div class="callout trap"><div class="lbl">Common trap</div>…</div>` |
| Ordered process | `<ol class="rail">` (only for real sequences) |
| Comparison table | `<div class="tbl"><table>` |
| Tabs | `<div class="seg" role="tablist">` with `button[aria-selected]` |
| Calculator | `.calc` > `.fields` (labelled inputs) + `.out` (result tiles) |
| Before/after | `.ba` grid with two children |

SVG text inherits theme colours through the classes above. Every `<svg>` needs `role="img"` and a `<title>`.

## Topic tracker rules (important)

The hub's progress is stored in each reader's browser under the localStorage key `de-learning-done-v1`. A topic's id is **group id + its index in that group** (for example `spark7`).

- **Only append** new topics to the end of a group. Inserting or reordering shifts ids and silently corrupts everyone's saved progress.
- To retire a topic, rename it in place rather than deleting it.
- Each topic entry is `[title, link, moduleKey, isOriginal]`. `link` is a path from the repo root, such as `spark/architecture/#memory`; use `0` when no page exists yet.
- When a module page adds a `#mine` checklist, its indices must match the hub's `GROUPS` entries.
- If you ever must change the scheme, bump the key to `-v2` and note it in the PR.

## Content standards

- **Accuracy first.** State defaults with their config names (for example `spark.sql.shuffle.partitions = 200`). When behaviour depends on version, name the version ("on by default since Spark 3.2").
- Label example metrics as examples. Never present invented numbers as benchmarks.
- Prefer Databricks/OSS-neutral explanations and call out platform-specific behaviour explicitly.
- Write plainly: short sentences, active voice, no filler, no emoji.
- Each module should answer, across its pages: what it is, why it matters, how it breaks, how to explain it in an interview.
- Code samples should be runnable PySpark or Spark SQL, with comments only where they add meaning.

## Before opening a PR

```bash
python3 scripts/check.py      # needs Python 3 and Node.js
```

It checks inline JavaScript syntax, that local links and `#anchors` resolve, that pages declare a `<title>`, and that no colour literals appear outside `styles.css`. CI runs the same script on every pull request.

Also open the changed pages in a browser in **both light and dark mode** and at **phone width**.

## PR scope

One topic, one module migration or one fix per PR. Describe what changed and why, and cite a source (Spark docs, Databricks docs, a paper) for any new technical claim.
