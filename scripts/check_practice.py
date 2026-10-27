#!/usr/bin/env python3
"""Validate a praxteward practice directory and list cards due for review.

Usage: python3 check_practice.py <practice-dir> [--today YYYY-MM-DD]
The directory holds INDEX.md and cards/<ID>.md. Exit 1 on errors; cards due
for review are listed but are not errors. Standard library only.
"""
import datetime, os, re, sys

REQUIRED_CARD = ["Version", "Status", "Kind", "Scope", "Task type", "Objective", "Applies when", "Not when",
                 "Decision factors", "Procedure", "Verification", "Assumptions", "Review triggers",
                 "Simpler alternative", "Transfer", "Automation", "Evidence", "History"]
STATUSES = ("candidate", "trial", "standard", "deprecated")
KINDS = ("method", "craft", "check", "automation")
PLACEHOLDER = re.compile(r"(?<![\w<])<[a-z][^<>\n=]{1,60}>(?!>)|YYYY-MM-DD|YYYYMMDD")
OUTCOMES = ("met", "partial", "missed")


def table_rows(text):
    """Rows of the first Markdown table only."""
    lines = []
    for l in text.splitlines():
        if l.strip().startswith("|"):
            lines.append(l)
        elif lines:
            break
    if len(lines) < 2:
        return []
    head = [h.strip() for h in lines[0].strip("|").split("|")]
    return [dict(zip(head, [c.strip() for c in l.strip("|").split("|")])) for l in lines[2:]]


def card_fields(text):
    fields, cur = {}, None
    for line in text.splitlines():
        m = re.match(r"^- \*\*(.+?):\*\*\s*(.*)$", line)
        if m:
            cur = m.group(1)
            fields[cur] = m.group(2).strip()
        elif cur and line.strip():
            fields[cur] += "\n" + line.strip()
    return fields


def items(value):
    return [re.sub(r"^([-*]|\d+\.)\s+", "", l).strip() for l in value.splitlines() if re.match(r"^([-*]|\d+\.)\s+", l.strip())]


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")
    args = sys.argv[1:]
    if not args or args[0].startswith("-"):
        print(__doc__); sys.exit(2)
    root = args[0]
    try:
        today = datetime.date.fromisoformat(args[args.index("--today") + 1]) if "--today" in args else datetime.date.today()
    except (IndexError, ValueError):
        print("ERROR --today needs YYYY-MM-DD"); sys.exit(2)
    idx = os.path.join(root, "INDEX.md")
    if not os.path.exists(idx):
        print(f"ERROR {idx}: not found"); sys.exit(2)
    errors, due = [], []
    rows = {r["ID"]: r for r in table_rows(open(idx, encoding="utf-8-sig").read()) if r.get("ID")}
    cdir = os.path.join(root, "cards")
    files = {f[:-3] for f in os.listdir(cdir) if re.fullmatch(r"P-\d{3,}\.md", f)} if os.path.isdir(cdir) else set()
    index_text = open(idx, encoding="utf-8-sig").read()
    if not re.search(r"^Last distill:\s*\d{4}-\d{2}-\d{2}", index_text, re.M):
        errors.append("INDEX.md: missing 'Last distill: YYYY-MM-DD'")
    for cid in sorted(files - set(rows)):
        errors.append(f"{cid}: card file not in INDEX")
    for cid in sorted(set(rows) - files):
        errors.append(f"{cid}: INDEX row has no cards/{cid}.md")

    for cid in sorted(files & set(rows)):
        text = open(os.path.join(cdir, cid + ".md"), encoding="utf-8-sig").read()
        if not re.match(rf"^# {re.escape(cid)} — \S", text):
            errors.append(f"{cid}: title must be '# {cid} — <title>'")
        f = card_fields(text)
        for k in REQUIRED_CARD:
            v = f.get(k, "").strip()
            if not v:
                errors.append(f"{cid}: field '{k}' empty")
            elif PLACEHOLDER.search(v) and not (k == "Review triggers" and "review_by" in v and not re.search(r"<[^<>\n]+>", v)):
                errors.append(f"{cid}: field '{k}' has placeholder text")
        status = f.get("Status", "").split()[0].lower() if f.get("Status") else ""
        if status not in STATUSES:
            errors.append(f"{cid}: Status '{f.get('Status')}' not in {STATUSES}")
        row = rows[cid]
        for col, val in (("Status", status), ("Kind", f.get("Kind", "")), ("Scope", f.get("Scope", "")), ("Task type", f.get("Task type", ""))):
            if row.get(col, "").strip().lower() != val.strip().lower():
                errors.append(f"{cid}: INDEX {col} '{row.get(col)}' != card '{val}'")
        if f.get("Kind", "") not in KINDS:
            errors.append(f"{cid}: Kind must be one of {KINDS}")
        if not re.fullmatch(r"general|general \(staged\)|project:[\w.-]+", f.get("Scope", "")):
            errors.append(f"{cid}: Scope must be 'general', 'general (staged)', or 'project:<name>'")
        if not re.fullmatch(r"\d+\.\d+", f.get("Version", "")):
            errors.append(f"{cid}: Version must look like 1.0")
        assumptions = items(f.get("Assumptions", ""))
        if any(" — " not in a for a in assumptions):
            errors.append(f"{cid}: every assumption needs ' — <how to check it>'")
        if f.get("Transfer") and f["Transfer"].count("→") < 3:
            errors.append(f"{cid}: Transfer must be cause → conditions → mechanism → verification")
        evidence = [e.rsplit(" — ", 2) for e in items(f.get("Evidence", ""))]
        if any(len(e) != 3 or e[1].strip() not in OUTCOMES or "/" not in e[0] or not e[2].strip().startswith("E-") for e in evidence):
            errors.append(f"{cid}: Evidence lines must be '<project>/<deliverable> — met|partial|missed — E-id'")
        m = re.search(r"review_by:\s*(\d{4}-\d{2}-\d{2})", f.get("Review triggers", ""))
        review = None
        if m:
            try:
                review = datetime.date.fromisoformat(m.group(1))
            except ValueError:
                errors.append(f"{cid}: review_by {m.group(1)} is not a valid date")
        else:
            errors.append(f"{cid}: Review triggers lacks review_by: YYYY-MM-DD")
        if m and row.get("Review by", "").strip() != m.group(1):
            errors.append(f"{cid}: INDEX Review by '{row.get('Review by')}' != card '{m.group(1)}'")
        if review and status != "deprecated" and review <= today:
            due.append(f"{cid}: review_by {m.group(1)} passed")
        if status == "trial" and len(evidence) < 2:
            errors.append(f"{cid}: trial needs two or more evidence lines (has {len(evidence)})")
        if status == "standard":
            met = {e[0].strip().lower() for e in evidence if len(e) == 3 and e[1].strip() == "met"}
            if len(met) < 2:
                errors.append(f"{cid}: standard needs 'met' evidence from 2+ distinct project/deliverable pairs (has {len(met)})")
            if re.search(r"—\s*untested\s*$", f.get("Simpler alternative", ""), re.I):
                errors.append(f"{cid}: standard needs the simpler alternative addressed, not 'untested'")
            if not assumptions:
                errors.append(f"{cid}: standard needs at least one assumption with a check")
        if status == "deprecated" and (not f.get("Replacement", "").strip() or "deprecat" not in f.get("History", "").lower()):
            errors.append(f"{cid}: deprecated card needs a Replacement field and a History line with the reason")
        missed = sum(1 for e in evidence if len(e) == 3 and e[1].strip() == "missed")
        if status in ("trial", "standard") and missed >= 2:
            due.append(f"{cid}: {missed} missed outcomes recorded")

    for d in due:
        print("DUE " + d)
    for e in errors:
        print("ERROR " + e)
    print(f"{'FAIL' if errors else 'OK'}: {len(files)} cards, {len(errors)} errors, {len(due)} due")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
