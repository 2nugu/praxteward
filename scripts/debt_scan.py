#!/usr/bin/env python3
"""Collect `shortcut:` comments into a debt ledger. Standard library only.

Usage: python3 debt_scan.py <file-or-dir>... [--strict]
Comment form: shortcut: <the limit>, <when to upgrade>
Prints a Markdown table of location, limit, and upgrade trigger. With --strict,
exit 1 when a shortcut has no upgrade trigger. Exit 2 on usage errors.
"""
import os, re, sys

CODE_EXT = (".py", ".js", ".ts", ".tsx", ".jsx", ".mjs", ".cjs", ".go", ".rs", ".java", ".c", ".cc", ".cpp",
            ".h", ".hpp", ".cs", ".rb", ".sh", ".kt", ".swift", ".php", ".css", ".scss", ".html", ".vue", ".svelte",
            ".sql", ".yaml", ".yml", ".toml")
SKIP_DIRS = {".git", "node_modules", "dist", "build", "__pycache__", ".venv", "venv", ".idea", ".vscode", "vendor"}
MARK = re.compile(r"(?:#|//|/\*|<!--|--|\*)\s*shortcut:\s*(.+?)\s*(?:\*/|-->)?\s*$")


def files(paths):
    for p in paths:
        if os.path.isfile(p):
            yield p
        else:
            for d, dirs, names in os.walk(p):
                dirs[:] = sorted(x for x in dirs if x not in SKIP_DIRS)
                for n in sorted(names):
                    if n.lower().endswith(CODE_EXT):
                        yield os.path.join(d, n)


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")
    strict = "--strict" in sys.argv[1:]
    paths = [a for a in sys.argv[1:] if a != "--strict"]
    if not paths or any(a.startswith("--") for a in paths):
        print(__doc__); sys.exit(2)
    for p in paths:
        if not os.path.exists(p):
            print(f"ERROR {p}: not found"); sys.exit(2)
    rows, missing = [], 0
    for path in files(paths):
        try:
            lines = open(path, encoding="utf-8-sig").read().splitlines()
        except (UnicodeDecodeError, OSError):
            continue
        for i, line in enumerate(lines, 1):
            m = MARK.search(line)
            if not m:
                continue
            limit, _, trigger = m.group(1).partition(",")
            trigger = trigger.strip()
            if not trigger:
                missing += 1
            rows.append((f"{path}:{i}", limit.strip(), trigger or "MISSING: add when to upgrade"))
    print("| Location | Limit | Upgrade when |\n|---|---|---|")
    for r in rows:
        print("| " + " | ".join(x.replace("|", "\\|") for x in r) + " |")
    print(f"\n{len(rows)} shortcuts, {missing} without an upgrade trigger")
    sys.exit(1 if strict and missing else 0)


if __name__ == "__main__":
    main()
