#!/usr/bin/env python3
"""Consistency check for the praxteward skill package. Standard library only.

Checks frontmatter against the Agent Skills specification; that packaged
Markdown links and file mentions resolve inside the package; that the mode
tables in SKILL.md, the mode procedures, the templates, and the checkers'
required fields agree; that the plugin manifests parse and name the skill;
and that packaged prose and scripts pass tell_scan.py.
Usage: python3 tools/validate.py [skill_dir]   (exit 1 on any failure)
"""
import ast, hashlib, json, os, re, subprocess, sys

EXCLUDE_DIRS = {"docs", "evals", "tools", "dist", "__pycache__", "venv", "node_modules"}
EXCLUDE_FILES = {"README.md", "CHANGELOG.md", "Thumbs.db", "desktop.ini"}
# agentskills.io/specification: name and description are required, the rest optional
FRONTMATTER_KEYS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
REPORT_FIELDS = ["mode", "role", "status", "objective", "evidence", "state_delta", "unknowns", "records", "next"]


def packaged_files(root):
    """Relative paths of files that belong in the installable skill."""
    out = []
    for d, dirs, files in os.walk(root):
        dirs[:] = sorted(x for x in dirs if x not in EXCLUDE_DIRS and not x.startswith("."))
        for f in sorted(files):
            rel = os.path.relpath(os.path.join(d, f), root).replace(os.sep, "/")
            if rel in EXCLUDE_FILES or f in EXCLUDE_FILES or f.startswith(".") or f.endswith((".pyc", ".zip")):
                continue
            out.append(rel)
    return out


def frontmatter(text):
    """Parse simple YAML frontmatter: scalars, quoted scalars, block scalars (| >), indented continuations."""
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        return {}, text
    fields, key = {}, None
    for line in m.group(1).split("\n"):
        km = re.match(r"^([\w-]+):\s*(.*)$", line)
        if km:
            key, val = km.group(1), km.group(2).strip()
            fields[key] = "" if val in ("|", ">", "|-", ">-") else val
        elif key and line.startswith((" ", "\t")):
            fields[key] = (fields[key] + " " + line.strip()).strip()
    for k, v in fields.items():
        if len(v) >= 2 and v[0] == v[-1] and v[0] in "'\"":
            fields[k] = v[1:-1]
    return fields, m.group(2)


def validate(root):
    errors = []
    read = lambda rel: open(os.path.join(root, rel), encoding="utf-8-sig").read()
    files = packaged_files(root)
    fileset = set(files)

    skill = read("SKILL.md")
    fm, body = frontmatter(skill)
    name, desc = fm.get("name", ""), fm.get("description", "")
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name) or len(name) > 64 or re.search(r"claude|anthropic", name):
        errors.append(f"invalid name '{name}'")
    if not desc or len(desc) > 1024 or re.search(r"[<>]", desc):
        errors.append(f"invalid description (len={len(desc)}; no angle brackets)")
    if set(fm) - FRONTMATTER_KEYS:
        errors.append(f"unexpected frontmatter keys {sorted(set(fm) - FRONTMATTER_KEYS)}")
    if len(fm.get("compatibility", "")) > 500:
        errors.append("compatibility exceeds 500 characters")
    lines = skill.count("\n")
    if lines > 500:
        errors.append(f"SKILL.md has {lines} lines; the Agent Skills specification recommends under 500")

    for rel in files:
        if not rel.endswith((".md", ".json")):
            continue
        base, text = os.path.dirname(rel), read(rel)
        for link in re.findall(r"\]\(([^)#\s]+)", text):
            if link.startswith(("http://", "https://")):
                continue
            target = os.path.normpath(os.path.join(base, link)).replace(os.sep, "/")
            if target not in fileset:
                errors.append(f"{rel}: link to missing or unpackaged file {link}")
        for m in re.findall(r"\b((?:references|modes|scripts|assets|agents)/[\w./-]+\.\w+)", text):
            if m not in fileset:
                errors.append(f"{rel}: mentions missing or unpackaged file {m}")

    modes = re.findall(r"\*\*(\w+)\*\* \|.*?\]\((modes/\w+\.md)\)", body)
    linked = {rel for _, rel in modes}
    for rel in sorted(f for f in fileset if f.startswith("modes/")):
        if rel not in linked:
            errors.append(f"{rel}: not linked from a SKILL.md mode table")
    prefixes = []
    for mode, rel in modes:
        if rel not in fileset:
            errors.append(f"{mode}: procedure {rel} missing"); continue
        text = read(rel)
        if not text.startswith(f"# {mode}\n"):
            errors.append(f"{rel}: title must be '# {mode}'")
        steps = re.findall(r"^- ([A-Z])(\d+)\.", text, flags=re.M)
        if not steps or len({s[0] for s in steps}) != 1 or [int(s[1]) for s in steps] != list(range(1, len(steps) + 1)):
            errors.append(f"{rel}: steps must share one letter and count from 1")
        prefixes += [s[0] for s in steps[:1]]
    if len(prefixes) != len(set(prefixes)):
        errors.append(f"step ID prefixes collide: {prefixes}")

    block = re.search(r"## \d+\. Report.*?```(.*?)```", body, flags=re.S)
    for field in REPORT_FIELDS:
        if not block or not re.search(rf"\b{field}:", block.group(1)):
            errors.append(f"report field '{field}' missing from SKILL.md report block")

    for script, const, tmpl in (("scripts/check_records.py", "REQUIRED_W", "assets/templates/VOLUME.md"),
                                ("scripts/check_records.py", "REQUIRED_D", "assets/templates/VOLUME.md"),
                                ("scripts/check_practice.py", "REQUIRED_CARD", "assets/templates/CARD.md")):
        m = re.search(rf"^{const} = (\[.*?\])", read(script), re.S | re.M)
        if not m:
            errors.append(f"{script}: {const} not found"); continue
        text = read(tmpl)
        for k in ast.literal_eval(m.group(1)):
            if f"- **{k}:**" not in text:
                errors.append(f"{tmpl} lacks field {k} required by {script}")

    defined = re.findall(r"^- (T\d+) ", read("references/output.md"), flags=re.M)
    if defined != sorted(set(defined)):
        errors.append(f"output.md check IDs must be unique and ascending: {defined}")
    targets = [os.path.join(root, f) for f in files
               if (f.endswith(".md") and not f.startswith("assets/templates/")) or f.endswith(".py")]
    r = subprocess.run([sys.executable, os.path.join(root, "scripts/tell_scan.py"), *targets],
                       capture_output=True, encoding="utf-8", errors="replace")
    if r.returncode not in (0, 1) or r.stderr.strip():
        errors.append("tell_scan failed: " + (r.stdout + r.stderr).strip()[-300:])
    elif r.returncode:
        errors += ["tell: " + l for l in r.stdout.splitlines() if re.match(r"T\d+ ", l)]

    if os.path.isdir(os.path.join(root, ".claude-plugin")):
        try:
            plugin = json.loads(read(".claude-plugin/plugin.json"))
            market = json.loads(read(".claude-plugin/marketplace.json"))
            if plugin.get("name") != name or [p.get("name") for p in market.get("plugins", [])] != [name]:
                errors.append("plugin.json and marketplace.json must name the skill")
            if not re.fullmatch(r"\d+\.\d+\.\d+", plugin.get("version", "")):
                errors.append("plugin.json version must be MAJOR.MINOR.PATCH")
        except (OSError, ValueError) as e:
            errors.append(f"plugin manifest unreadable: {e}")

    digest = hashlib.sha256()
    for rel in files:
        with open(os.path.join(root, rel), "rb") as source:
            data = source.read()
        digest.update(rel.encode("utf-8") + b"\0" + len(data).to_bytes(8, "big") + data)
    return errors, f"{len(modes)} modes, {len(files)} packaged files, description {len(desc)} chars, SKILL.md {lines} lines and {len(body.split())} body words, package-sha256 {digest.hexdigest()}"


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")
    root = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    errs, summary = validate(root)
    print("\n".join("ERROR " + e for e in errs) if errs else "OK: " + summary)
    sys.exit(1 if errs else 0)
