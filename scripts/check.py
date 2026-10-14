#!/usr/bin/env python3
"""Validate the DE Learning site. Run from the repo root: python3 scripts/check.py

Checks every .html page in the repo (including area/module folders):
  1. Inline <script> blocks parse (uses `node --check`; skipped with a warning if Node is missing)
  2. Local links resolve to existing files or folders, and #anchors to existing ids
  3. Every page has a <title>
  4. No colour literals (#hex, rgb(), hsl()) in pages; colours belong in styles.css tokens
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {".git", ".github", "scripts", "node_modules"}

pages = []
for dirpath, dirnames, filenames in os.walk(ROOT):
    dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS and not d.startswith("."))
    for f in sorted(filenames):
        if f.endswith(".html"):
            pages.append(os.path.relpath(os.path.join(dirpath, f), ROOT).replace(os.sep, "/"))

errors = []
warnings = []
texts = {p: open(os.path.join(ROOT, p), encoding="utf-8").read() for p in pages}
ids = {p: set(re.findall(r'\bid="([^"]+)"', t)) for p, t in texts.items()}
node = shutil.which("node")
if not node:
    warnings.append("Node.js not found: skipped JavaScript syntax check")


def resolve(from_page, path):
    """Resolve a relative link from a page to a repo-relative page path, or None if missing."""
    target = os.path.normpath(os.path.join(os.path.dirname(from_page), path)).replace(os.sep, "/")
    full = os.path.join(ROOT, target)
    if os.path.isdir(full):
        target = "index.html" if target == "." else target + "/index.html"
        full = os.path.join(ROOT, target)
    return target if os.path.exists(full) else None


def anchor_ok(target_page, frag):
    # ids may also be created at runtime by a page script (e.g. scenario panels) if named in that script
    return frag in ids.get(target_page, set()) or f'"{frag}"' in texts.get(target_page, "")


for page, html in texts.items():
    if not re.search(r"<title>[^<]+</title>", html):
        errors.append(f"{page}: missing <title>")

    # 1. script syntax
    if node:
        for i, js in enumerate(re.findall(r"<script>(.*?)</script>", html, re.S)):
            with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as fh:
                fh.write(js)
                tmp = fh.name
            res = subprocess.run([node, "--check", tmp], capture_output=True, text=True)
            os.unlink(tmp)
            if res.returncode:
                msg = res.stderr.strip().splitlines()[-1] if res.stderr.strip() else "syntax error"
                errors.append(f"{page}: inline script #{i + 1}: {msg}")

    # 2. links: static hrefs, plus "page.html#id" strings inside scripts
    #    (strings joined to a prefix with + are built at runtime and skipped)
    targets = set(re.findall(r'href="([^"]+)"', html))
    targets |= set(re.findall(r'(?<!\+)["\']((?:\.\./|[a-z0-9-]+/)*[a-z0-9-]+\.html(?:#[A-Za-z0-9_.~-]+)?)["\']', html))
    for href in targets:
        if re.match(r"^(https?:|mailto:|tel:|data:|javascript:)", href) or "${" in href:
            continue
        path, _, frag = href.partition("#")
        if path:
            target_page = resolve(page, path)
            if not target_page:
                errors.append(f"{page}: link to missing file '{href}'")
                continue
        else:
            target_page = page
        if frag and not anchor_ok(target_page, frag):
            errors.append(f"{page}: anchor '#{frag}' not found in {target_page}")

    # 4. colour literals outside styles.css
    cleaned = re.sub(r"url\(#[^)]+\)", "", html)
    for m in re.finditer(r'#[0-9a-fA-F]{3,8}\b(?=[;\s"\'),])|\brgba?\(|\bhsla?\(', cleaned):
        ctx = cleaned[max(0, m.start() - 12): m.end() + 4]
        if "href=" in ctx or "url(" in ctx:
            continue
        errors.append(f"{page}: colour literal near '{ctx.strip()}' (use a styles.css token)")
        break

# Hub tracker links: page constants in index.html (e.g. A="spark-architecture.html") + "#id"
hub = texts.get("index.html", "")
consts = dict(re.findall(r'\b([A-Z])="([^"]+?\.html|[^"]+/)"', hub))
for const, frag in re.findall(r'\b([A-Z])\+"#([A-Za-z0-9_-]+)"', hub):
    path = consts.get(const)
    target_page = resolve("index.html", path) if path else None
    if not target_page:
        errors.append(f"index.html: tracker constant {const} points to a missing page")
    elif not anchor_ok(target_page, frag):
        errors.append(f"index.html: tracker link {path}#{frag} has no matching id")

for w in warnings:
    print("WARN ", w)
for e in errors:
    print("ERROR", e)
print(f"\nChecked {len(pages)} pages: {len(errors)} error(s), {len(warnings)} warning(s)")
sys.exit(1 if errors else 0)
