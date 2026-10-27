#!/usr/bin/env python3
"""Consistency check for the praxteward skill package. Standard library only.

Checks frontmatter rules; that packaged Markdown links and file mentions
resolve inside the package; that contract.json agrees with SKILL.md, the
mode procedures, the VOLUME template, check_records.py, and output.md; and
that packaged prose and scripts pass tell_scan.py.
Usage: python3 tools/validate.py [skill_dir]   (exit 1 on any failure)
"""
import ast, json, os, re, subprocess, sys

EXCLUDE_DIRS = {"docs", "evals", "tools", "dist", "__pycache__", "venv", "node_modules"}
EXCLUDE_FILES = {"README.md", "CHANGELOG.md", "Thumbs.db", "desktop.ini"}


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
    if not re.fullmatch(r"[a-z0-9-]{1,64}", name) or re.search(r"claude|anthropic", name):
        errors.append(f"invalid name '{name}'")
    if not desc or len(desc) > 1024 or re.search(r"[<>]", desc):
        errors.append(f"invalid description (len={len(desc)}; no angle brackets)")
    if set(fm) - {"name", "description"}:
        errors.append(f"unexpected frontmatter keys {sorted(set(fm) - {'name', 'description'})}")

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

    contract = json.loads(read("contract.json"))
    for mode, spec in contract["modes"].items():
        if spec["procedure"] not in fileset:
            errors.append(f"{mode}: procedure missing"); continue
        text = read(spec["procedure"])
        found = re.findall(r"^- ([A-Z]\d+)\.", text, flags=re.M)
        if found != spec["steps"]:
            errors.append(f"{mode}: steps {found} != contract {spec['steps']}")
        if not text.startswith(f"# {mode.capitalize()}\n"):
            errors.append(f"{spec['procedure']}: title must be '# {mode.capitalize()}'")
        for s in spec.get("light_steps", []) + spec.get("lookahead_steps", []):
            if s not in spec["steps"]:
                errors.append(f"{mode}: sub-step {s} not in steps")
        if f"**{mode.capitalize()}**" not in body or spec["procedure"] not in body:
            errors.append(f"SKILL.md mode table missing {mode} or its procedure link")
    prefixes = [s[0][0] for s in (m["steps"] for m in contract["modes"].values())]
    if len(prefixes) != len(set(prefixes)):
        errors.append(f"step ID prefixes collide: {prefixes}")

    block = re.search(r"## \d+\. Report.*?```(.*?)```", body, flags=re.S)
    if not block:
        errors.append("SKILL.md report block not found")
    else:
        for field in contract["report"]["required"]:
            if not re.search(rf"\b{field}:", block.group(1)):
                errors.append(f"report field '{field}' missing from SKILL.md")

    for ev, target in contract["events"].items():
        for t in (target if isinstance(target, list) else [target]):
            base = re.sub(r"_(light|lookahead)$", "", t)
            if t not in ("named_mode", "regate", "inspect_read_only") and base not in contract["modes"]:
                errors.append(f"event {ev} maps to unknown mode {t}")

    checker = read(contract["records"]["checker"])
    tmpl = read("assets/templates/VOLUME.md")
    for key, const in (("work_required", "REQUIRED_W"), ("decision_required", "REQUIRED_D")):
        m = re.search(rf"^{const} = (\[.*?\])", checker, re.S | re.M)
        if not m or ast.literal_eval(m.group(1)) != contract["records"][key]:
            errors.append(f"contract records.{key} != {const} in checker")
        for k in contract["records"][key]:
            if f"- **{k}:**" not in tmpl:
                errors.append(f"VOLUME template lacks field {k}")

    card = read("assets/templates/CARD.md")
    m = re.search(r"^REQUIRED_CARD = (\[.*?\])", read(contract["practice"]["checker"]), re.S | re.M)
    if not m or ast.literal_eval(m.group(1)) != contract["practice"]["card_required"]:
        errors.append("contract practice.card_required != REQUIRED_CARD in checker")
    for k in contract["practice"]["card_required"]:
        if f"- **{k}:**" not in card:
            errors.append(f"CARD template lacks field {k}")

    oc = contract["output_checks"]
    defined = re.findall(r"^- (T\d+) ", read("references/output.md"), flags=re.M)
    if defined != oc["block"] + oc["fix"]:
        errors.append(f"output.md checks {defined} != contract")
    targets = [os.path.join(root, f) for f in files
               if (f.endswith(".md") and not f.startswith("assets/templates/")) or f.endswith(".py")]
    r = subprocess.run([sys.executable, os.path.join(root, oc["checker"]), *targets],
                       capture_output=True, encoding="utf-8", errors="replace")
    if r.returncode not in (0, 1) or r.stderr.strip():
        errors.append("tell_scan failed: " + (r.stdout + r.stderr).strip()[-300:])
    elif r.returncode:
        errors += ["tell: " + l for l in r.stdout.splitlines() if re.match(r"T\d+ ", l)]

    return errors, f"{len(contract['modes'])} modes, {len(files)} packaged files, description {len(desc)} chars, SKILL.md body {len(body.split())} words"


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")
    root = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    errs, summary = validate(root)
    print("\n".join("ERROR " + e for e in errs) if errs else "OK: " + summary)
    sys.exit(1 if errs else 0)
