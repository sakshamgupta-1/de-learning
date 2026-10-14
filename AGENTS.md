# Guide for AI agents (and humans) editing DE Learning

Read this whole file before changing anything. It describes how the site is built and the rules that keep it consistent.

## What this project is

A static, dependency-free study site for data engineering interview prep. Readers are experienced engineers preparing for Lead Data Engineer / Data Architect interviews. Content must be **technically correct, concise and interview-oriented**.

## Hard constraints

- **No build step, no frameworks, no package manager.** Plain HTML, one shared `styles.css`, and inline `<script>` per page.
- **No new external hosts.** Fonts come from Google Fonts only. Don't add CDNs, analytics, trackers, iframes or remote images. Embed images as inline SVG.
- **Every page is self-contained** apart from `styles.css` and links to sibling pages.
- **Works offline and from `file://`.** No `fetch()` of local files.
- **Light and dark themes.** Use only the CSS tokens defined in `:root` in `styles.css` (`--bg`, `--fg`, `--accent`, `--blue`, `--ok`, `--warn`, `--bad`, and their `-soft` variants). Never hard-code a colour in a page or an SVG.
- **Phone width (~400 px) must work.** Wide diagrams and tables go inside `.fig` / `.tbl` containers, which scroll horizontally on their own.

## File layout

```
index.html                hub + topic tracker (topic data lives in the GROUPS array)
spark-*.html              Spark Core learning path, modules 1–4
styles.css                shared tokens + components
scripts/check.py          validation run in CI
```

New learning paths use the prefix pattern `<area>-<module>.html`, for example `streaming-output-modes.html`.

## Page skeleton

Copy an existing module page (for example `spark-execution.html`) as the starting point. Every module page has:

1. `<header class="top">` with the module nav. Update the nav on **every page in the path** when adding a page.
2. Eyebrow (`Spark Core · Module N of M`), `h1`, `.lede`, and a `.toc` row of in-page anchor links.
3. Content `<section id="...">` blocks. Section ids are linked from `index.html`, so **don't rename existing ids**.
4. A `Check yourself` section (`.qa` with `<details>` items).
5. A `Mark this module's topics` block (`#mine`) driven by the page script.
6. `<nav class="next">` with previous/next links.

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
- Each topic entry is `[title, link, moduleKey, isOriginal]`. `link` is `page.html#section-id`; use `0` when no page exists yet.
- When a module page adds a `#mine` checklist, its indices must match the hub's `GROUPS` entries.
- If you ever must change the scheme, bump the key to `-v2` and note it in the PR.

## Content standards

- **Accuracy first.** State defaults with their config names (for example `spark.sql.shuffle.partitions = 200`). When behaviour depends on version, name the version ("on by default since Spark 3.2").
- Label example metrics as examples. Never present invented numbers as benchmarks.
- Prefer Databricks/OSS-neutral explanations and call out platform-specific behaviour explicitly.
- Write plainly: short sentences, active voice, no filler, no emoji.
- Each concept should answer: what it is, why it matters, how it breaks, how to explain it in an interview.
- Code samples should be runnable PySpark or Spark SQL, with comments only where they add meaning.

## Before opening a PR

```bash
python3 scripts/check.py      # needs Python 3 and Node.js
```

It checks inline JavaScript syntax, that local links and `#anchors` resolve, that pages declare a `<title>`, and that no colour literals appear outside `styles.css`. CI runs the same script on every pull request.

Also open the changed pages in a browser in **both light and dark mode** and at **phone width**.

## PR scope

One topic or one fix per PR. Describe what changed and why, and cite a source (Spark docs, Databricks docs, a paper) for any new technical claim.
