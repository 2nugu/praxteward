#!/usr/bin/env python3
"""Build the installable skill zip (claude.ai upload, Claude API, release asset).

Usage: python3 tools/package.py [out.zip]     default: dist/praxteward.zip
Runs validate.py first and packages exactly the files it validates.
"""
import os, sys, zipfile

here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here)
from validate import packaged_files, validate  # noqa: E402

root = os.path.dirname(here)
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")
out = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(root, "dist", "praxteward.zip"))
errs, summary = validate(root)
if errs:
    print("\n".join("ERROR " + e for e in errs)); sys.exit("validation failed; not packaging")
if not os.path.exists(os.path.join(root, "LICENSE")):
    print("WARNING: LICENSE missing. Fine for a personal install; add it before a public release.")
files = packaged_files(root)
os.makedirs(os.path.dirname(out), exist_ok=True)
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
    for rel in files:
        z.write(os.path.join(root, rel), "praxteward/" + rel)
print(f"OK: {summary}\nwrote {out} ({len(files)} files)")
