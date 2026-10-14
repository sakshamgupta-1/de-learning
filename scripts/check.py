#!/usr/bin/env python3
"""Validate the DE Learning site. Run from the repo root: python3 scripts/check.py

Checks:
  1. Inline <script> blocks parse (uses `node --check`; skipped with a warning if Node is missing)
  2. Local links resolve to existing files, and #anchors to existing ids
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
pages = sorted(f for f in os.listdir(ROOT) if f.endswith(".html"))
errors = []
warnings = []


def ids_in(html):
    return set(re.findall(r'\bid="([^"]+)"', html))


texts = {p: open(os.path.join(ROOT, p), encoding="utf-8").read() for p in pages}
ids = {p: ids_in(t) for p, t in texts.items()}
node = shutil.which("node")
if not node:
    warnings.append("Node.js not found: skipped JavaScript syntax check")

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

    # 2. links (static hrefs, plus page.html#id strings inside scripts)
    targets = set(re.findall(r'href="([^"]+)"', html))
    targets |= set(re.findall(r'["\']([a-z0-9-]+\.html(?:#[A-Za-z0-9_.~-]+)?)["\']', html))
    for href in targets:
        if re.match(r"^(https?:|mailto:|tel:|data:|javascript:)", href) or "${" in href:
            continue
        path, _, frag = href.partition("#")
        target_page = path or page
        if path and not os.path.exists(os.path.join(ROOT, path)):
            errors.append(f"{page}: link to missing file '{href}'")
            continue
        if frag and target_page in ids and frag not in ids[target_page]:
            # ids created at runtime by scripts (scenario panels) are allowed if referenced in that page's script
            if f'"{frag}"' not in texts.get(target_page, ""):
                errors.append(f"{page}: anchor '#{frag}' not found in {target_page}")

    # 3. colour literals outside styles.css
    body_no_svg_ids = re.sub(r'url\(#[^)]+\)', "", html)
    for m in re.finditer(r'#[0-9a-fA-F]{3,8}\b(?=[;\s"\'),])|\brgba?\(|\bhsla?\(', body_no_svg_ids):
        ctx = body_no_svg_ids[max(0, m.start() - 12): m.end() + 4]
        if "href=" in ctx or "url(" in ctx:
            continue
        errors.append(f"{page}: colour literal near '{ctx.strip()}' (use a styles.css token)")
        break

# Hub tracker links: page constants in index.html (A, E, O, T) + "#id"
hub = texts.get("index.html", "")
consts = dict(re.findall(r'\b([A-Z])="([a-z0-9-]+\.html)"', hub))
for const, frag in re.findall(r'\b([A-Z])\+"#([A-Za-z0-9_-]+)"', hub):
    page = consts.get(const)
    if not page:
        errors.append(f"index.html: unknown page constant {const}")
    elif frag not in ids.get(page, set()) and f'"{frag}"' not in texts.get(page, ""):
        errors.append(f"index.html: tracker link {page}#{frag} has no matching id")

for w in warnings:
    print("WARN ", w)
for e in errors:
    print("ERROR", e)
print(f"\nChecked {len(pages)} pages: {len(errors)} error(s), {len(warnings)} warning(s)")
sys.exit(1 if errors else 0)
