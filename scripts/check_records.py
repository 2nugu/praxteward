#!/usr/bin/env python3
"""Verify praxteward project records are substantive, consistent, and complete.

Usage: python3 check_records.py <project_root> [--since <git-ref> | --since last]
Reads <project_root>/.praxteward.yaml (keys: index, log, volumes_dir,
coverage_ignore); defaults: docs/INDEX.md, docs/LOG.md, docs/volumes.
"--since last" uses the "Last reconcile:" commit in the index.
Exit 1 if any error is found. Standard library only.
"""
import fnmatch, os, re, subprocess, sys
from collections import Counter

ID_RE = r"[FDCX]-\d{3,}"
REQUIRED_F = ["Status", "Intent", "How", "Alternatives", "Rationale",
              "Verification", "Locators", "Operation", "Limits"]
REQUIRED_D = ["Context", "Options", "Choice", "Evidence", "invalidated_if", "Affects"]
VAGUE = re.compile(r"^(tested|works|done|ok|implemented( as planned)?|n/?a|tbd|-|—)\.?$", re.I)
PLACEHOLDER = re.compile(r"<[^<>\n]+>")


def load_config(root):
    cfg = {"index": "docs/INDEX.md", "log": "docs/LOG.md",
           "volumes_dir": "docs/volumes", "coverage_ignore": []}
    p = os.path.join(root, ".praxteward.yaml")
    if not os.path.exists(p):
        return cfg
    key = None
    for raw in open(p, encoding="utf-8"):
        line = re.sub(r"\s+#.*$", "", raw.rstrip())
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        m = re.match(r"^(\w+):\s*(.*)$", line)
        if m:
            key, val = m.group(1), m.group(2).strip().strip("\"'")
            if key == "coverage_ignore":
                cfg[key] = [v.strip().strip("\"'") for v in val.strip("[]").split(",") if v.strip()]
            else:
                cfg[key] = val
        elif key == "coverage_ignore" and line.strip().startswith("- "):
            cfg[key].append(line.strip()[2:].strip().strip("\"'"))
    return cfg


def table(text, heading):
    m = re.search(rf"^## {re.escape(heading)}.*?$(.*?)(?=^## |\Z)", text, re.M | re.S)
    if not m:
        return []
    lines = [l for l in m.group(1).splitlines() if l.strip().startswith("|")]
    if len(lines) < 2:
        return []
    head = [h.strip() for h in lines[0].strip("|").split("|")]
    return [dict(zip(head, [c.strip() for c in l.strip("|").split("|")])) for l in lines[2:]]


def section(text, heading):
    m = re.search(rf"^## {re.escape(heading)}\s*$(.*?)(?=^## |\Z)", text, re.M | re.S)
    return m.group(1) if m else ""


def records(text):
    """List of (id, fields) for ### F-/D-/C- headings, in file order."""
    out = []
    for m in re.finditer(rf"^### ({ID_RE}) — (.*?)$(.*?)(?=^#{{2,3}} |\Z)", text, re.M | re.S):
        fields, cur = {}, None
        for line in m.group(3).splitlines():
            fm = re.match(r"^- \*\*(.+?):\*\*\s*(.*)$", line)
            if fm:
                cur = fm.group(1)
                fields[cur] = fm.group(2).strip()
            elif cur and line.strip():
                fields[cur] += "\n" + line.strip()
        out.append((m.group(1), fields))
    return out


def first_word(s):
    return s.split()[0].lower() if s and s.split() else ""


def vol_key(v):
    return int(v) if str(v).isdigit() else str(v)


def git_lines(root, *args):
    return subprocess.run(["git", "-C", root, *args], capture_output=True, text=True, check=True).stdout.split("\n")


def main():
    args = sys.argv[1:]
    if not args or args[0].startswith("-"):
        print(__doc__); sys.exit(2)
    root = os.path.abspath(args[0])
    since = args[args.index("--since") + 1] if "--since" in args else None
    cfg = load_config(root)
    errors = []
    idx_path = os.path.join(root, cfg["index"])
    if not os.path.exists(idx_path):
        print(f"ERROR index not found: {cfg['index']} (set 'index' in .praxteward.yaml)"); sys.exit(1)
    idx_dir = os.path.dirname(idx_path)
    index = open(idx_path, encoding="utf-8").read()

    # 1. Volumes registered <-> files present.
    vol_files = {r.get("File", ""): r for r in table(index, "Volumes") if r.get("File")}
    vdir = os.path.join(root, cfg["volumes_dir"])
    for f in sorted(os.listdir(vdir)) if os.path.isdir(vdir) else []:
        if f.endswith(".md"):
            rel = os.path.relpath(os.path.join(vdir, f), idx_dir).replace(os.sep, "/")
            if rel not in vol_files:
                errors.append(f"volume file not in index: {rel}")
    for f in vol_files:
        if not os.path.exists(os.path.join(idx_dir, f)):
            errors.append(f"index lists missing volume: {f}")

    # 2. Parse records; IDs unique across and within files.
    all_recs, rec_vol, vol_text, seen = {}, {}, {}, Counter()
    for f, row in vol_files.items():
        p = os.path.join(idx_dir, f)
        if not os.path.exists(p):
            continue
        t = open(p, encoding="utf-8").read()
        vol = row.get("Vol", f)
        vol_text[vol] = (f, t, row)
        for rid, fields in records(t):
            seen[rid] += 1
            all_recs[rid], rec_vol[rid] = fields, vol
    for rid, n in seen.items():
        if n > 1:
            errors.append(f"duplicate ID {rid} ({n} records)")

    reg = {r["ID"]: r for r in table(index, "Feature registry") if r.get("ID")}
    dec = {r["ID"]: r for r in table(index, "Decisions") if r.get("ID")}
    for rid, f in all_recs.items():
        if rid.startswith("F-"):
            if rid not in reg:
                errors.append(f"{rid} missing from Feature registry")
                continue
            if first_word(reg[rid].get("Status", "")) != first_word(f.get("Status", "")):
                errors.append(f"{rid} registry status '{reg[rid].get('Status')}' != record '{f.get('Status')}'")
            if reg[rid].get("Vol") != rec_vol[rid]:
                errors.append(f"{rid} registry Vol '{reg[rid].get('Vol')}' != record Vol '{rec_vol[rid]}'")
        elif rid.startswith("D-") and rid not in dec:
            errors.append(f"{rid} missing from index Decisions")
    for rid in list(reg) + list(dec):
        if rid not in all_recs:
            errors.append(f"index lists {rid} but no record exists")
    known = set(all_recs) | {r["ID"] for r in table(index, "Deferred") if r.get("ID")}
    for rid, f in all_recs.items():
        for ref in re.findall(ID_RE, " ".join(f.values())):
            if ref not in known:
                errors.append(f"{rid} references unknown {ref}")

    # 3. Substance of records.
    locator_paths = set()
    for rid, f in all_recs.items():
        if rid.startswith("F-"):
            status = f.get("Status", "").lower()
            if status.startswith("superseded") and not re.search(r"F-\d+", f.get("Status", "")):
                errors.append(f"{rid} superseded without successor ID")
            done = status.startswith("done")
            if done:
                for k in REQUIRED_F:
                    v = f.get(k, "").strip()
                    if not v or PLACEHOLDER.search(v) or (k != "Status" and VAGUE.match(v)):
                        errors.append(f"{rid} field '{k}' empty, vague, or placeholder")
                if f.get("Verification") and not re.search(r"`|\d", f["Verification"]):
                    errors.append(f"{rid} Verification lacks a command or observed value")
            locs = re.findall(r"^- `([^`]+)`\s*[—-]\s*(\S.*)$", f.get("Locators", ""), re.M)
            raw = re.findall(r"`([^`]+)`", f.get("Locators", ""))
            if done and not locs:
                errors.append(f"{rid} has no locator with an explanation ('`path::symbol` — what it confirms')")
            if len(raw) > len(locs):
                errors.append(f"{rid} has locators without an explanation")
            for loc in raw:
                path, _, sym = loc.partition("::")
                locator_paths.add(os.path.normpath(path).replace(os.sep, "/"))
                if not (done or status.startswith("active")):
                    continue  # planned/superseded locators may not exist
                fp = os.path.join(root, path)
                if not os.path.exists(fp):
                    errors.append(f"{rid} locator file missing: {path}")
                elif sym and os.path.isfile(fp):
                    src = open(fp, encoding="utf-8", errors="replace").read()
                    if not re.search(rf"(?<![\w]){re.escape(sym.split('.')[-1])}(?![\w])", src):
                        errors.append(f"{rid} locator symbol not found: {loc}")
        elif rid.startswith("D-"):
            for k in REQUIRED_D:
                v = f.get(k, "").strip()
                if not v or PLACEHOLDER.search(v):
                    errors.append(f"{rid} field '{k}' empty or placeholder")

    # 4. Closed volumes account for every open item; carried items appear in the next volume.
    order = sorted(vol_text, key=vol_key)
    for i, vol in enumerate(order):
        fname, t, row = vol_text[vol]
        st = re.search(r"^- \*\*Status:\*\*\s*(\w+)", t, re.M)
        if not ((st and st.group(1).lower() == "closed") or row.get("Status", "").lower() == "closed"):
            continue
        nxt = vol_text[order[i + 1]][1] if i + 1 < len(order) else None
        for line in section(t, "Open items").splitlines():
            if not line.strip().startswith("- ["):
                continue
            if not re.search(r"\b(carried|deferred|dropped)\b", line):
                errors.append(f"{fname}: open item without disposition: {line.strip()}")
            if "carried" in line and nxt is not None:
                for cid in re.findall(ID_RE, line):
                    if cid not in section(nxt, "Carried in"):
                        errors.append(f"{fname}: {cid} marked carried but absent from the next volume's Carried in")
        summ = section(t, "Exit summary")
        if not summ.strip() or PLACEHOLDER.search(summ):
            errors.append(f"{fname}: closed without a completed exit summary")

    # 5. Coverage of changed and untracked files since a ref.
    if since:
        if since == "last":
            m = re.search(r"Last reconcile:\s*`?([0-9a-fA-F]{6,40}|[\w./-]+)`?", index)
            if not m or m.group(1).startswith("<"):
                print("ERROR --since last: no 'Last reconcile:' commit in the index"); sys.exit(1)
            since = m.group(1)
        try:
            changed = git_lines(root, "diff", "--relative", "--name-only", since)
            changed += git_lines(root, "ls-files", "--others", "--exclude-standard")
        except Exception as e:
            print(f"ERROR git failed: {e}"); sys.exit(1)
        log_path = os.path.join(root, cfg["log"])
        log = open(log_path, encoding="utf-8").read() if os.path.exists(log_path) else ""
        record_files = {os.path.normpath(p).replace(os.sep, "/") for p in
                        (cfg["index"], cfg["log"], cfg.get("queue", "")) if p}
        ignore = list(cfg["coverage_ignore"]) + [cfg["volumes_dir"].rstrip("/") + "/*", ".praxteward.yaml"]
        for p in sorted({x.strip() for x in changed if x.strip()}):
            if p in record_files or any(fnmatch.fnmatch(p, g) for g in ignore):
                continue
            if p in locator_paths or re.search(rf"no-record:\s*`?{re.escape(p)}`?", log):
                continue
            errors.append(f"uncovered change since {since}: {p} (add a locator or record, or log 'no-record: {p} — reason')")

    n_f = sum(k.startswith("F-") for k in all_recs)
    n_done = sum(1 for k, f in all_recs.items() if k.startswith("F-") and f.get("Status", "").lower().startswith("done"))
    summary = f"{len(vol_files)} volumes, {n_f} features ({n_done} done), {sum(k.startswith('D-') for k in all_recs)} decisions"
    if errors:
        print("\n".join("ERROR " + e for e in errors)); print(f"FAIL: {len(errors)} errors; {summary}"); sys.exit(1)
    print(f"OK: {summary}")


if __name__ == "__main__":
    main()
