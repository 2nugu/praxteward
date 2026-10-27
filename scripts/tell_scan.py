#!/usr/bin/env python3
"""Flag mechanical signs of machine-written output in docs and code.

Usage: python3 tell_scan.py <file-or-dir>... [--block-only]
Check IDs match references/output.md. Suppress a Fix finding with a comment
that names the check ID and a reason, on the same or the previous line:
  <!-- tell-ok: T11 statistical term -->      # tell-ok: T21 re-raised by caller
A comment line starting with "tell-ok-file: <id> <reason>" suppresses the check
for the whole file; it is the only way to exempt a Block check, intended for
files that define or test the checks.
Exit codes: 0 clean, 1 findings, 2 usage or read error. Standard library only.
"""
import os, re, sys

TEXT_EXT = (".md", ".markdown", ".txt", ".rst")
CODE_EXT = (".py", ".js", ".ts", ".tsx", ".jsx", ".mjs", ".go", ".rs", ".java", ".c", ".cc", ".cpp",
            ".h", ".hpp", ".cs", ".rb", ".sh", ".kt", ".swift")
SKIP_DIRS = {".git", "node_modules", "dist", "build", "__pycache__", ".venv", "venv", ".idea", ".vscode"}
BLOCK = {"T01", "T02"}

HTML_TAGS = (r"(?:br|hr|img|a|p|div|span|sup|sub|kbd|details|summary|table|thead|tbody|tr|td|th|em|strong|"
             r"b|i|u|code|pre|ul|ol|li|h\d|section|script|style|input|blockquote|mark|small|dl|dt|dd|"
             r"figure|figcaption|video|source|iframe|nav)")
PLACEHOLDER = re.compile(
    rf"(?<!\w)<(?!/?{HTML_TAGS}\b)(?![a-z][a-z0-9+.-]*:)(?![^<>\s]+@)[A-Za-z][^<>\n`]{{2,59}}>"
    r"|\b(TODO|FIXME|TBD)\b|lorem ipsum", re.I)
DONE_CLAIM = re.compile(r"\b(all tests pass(ed)?|fully (tested|verified)|works (perfectly|as expected)|production[- ]ready)\b", re.I)
EVIDENCE = re.compile(r"`[^`]+`|\b\d+ (passed|tests?|checks?|cases?)\b", re.I)
MEASURE = re.compile(r"\d+(\.\d+)?\s*(%|x\b|×|ms\b|s\b|sec|min|h\b|kb|mb|gb|tb|fps|rps|qps|ops|°|배|초|분)", re.I)

PROSE = [
    ("T10", re.compile(r"(^|[.!?]\s+)(great question|certainly!|absolutely!|i hope this helps|let me know if you have|feel free to reach out|happy to help)", re.I)),
    ("T10", re.compile(r"(^|[.!?]\s+|^\s*[-*]\s+)(in conclusion|in summary|to summarize|to sum up|overall|ultimately),", re.I)),
    ("T10", re.compile(r"(결론적으로|요약하자면|정리하자면|도움이 되셨길|궁금한 점이 있으시면|살펴보겠습니다|알아보겠습니다)")),
    ("T11", re.compile(r"\b(delve|delves|delving|tapestry|realm|landscape of|leverag(e|es|ed|ing)|robust|seamless(ly)?|cutting[- ]edge|state[- ]of[- ]the[- ]art|game[- ]chang\w*|pivotal|holistic|synerg\w+|streamlin\w+|empower\w*|elevat(e|es|ed|ing)|unlock(s|ed|ing)?|supercharg\w+|revolutioni[sz]\w*|meticulous(ly)?|intricate|underscore(s|d)?|paramount|testament to|navigat(e|ing) the (complexities|landscape))\b", re.I)),
    ("T11", re.compile(r"(혁신적|획기적|원활한|원활하게|다양한 측면|핵심적인 역할|중요한 역할을 합니다)")),
    ("T12", re.compile(r"\b(it('s| is) (important|worth|crucial) (to note|noting|to remember)|needless to say|it goes without saying|arguably|essentially,|basically,|at the end of the day)\b", re.I)),
    ("T12", re.compile(r"(것이 중요합니다|라고 할 수 있습니다|점에 유의해야 합니다|주목할 만합니다)")),
    ("T13", re.compile(r"\bnot (just|only|merely) [^.;\n]{1,60}?,? but (also )?\b", re.I)),
    ("T13", re.compile(r"\bit('s| is) not [^.;\n]{1,40}?(,|[—–]| -{1,2}) ?it('s| is)\b", re.I)),
    ("T13", re.compile(r"뿐만 아니라")),
    ("T16", re.compile(r"\b(studies|research|experts|many people|some say) (show|shows|suggest|suggests|say|says|agree)\b", re.I)),
    ("T17", re.compile(r"\b(significantly|dramatically|substantially|vastly|greatly|massively) (faster|slower|better|worse|improv\w+|reduc\w+|higher|lower|increas\w+|decreas\w+)\b", re.I)),
]
EMOJI = re.compile("[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U0001F000-\U0001F2FF]")
COMMENT = re.compile(r"^\s*(#|//|--|/\*|\*)\s?(.*)$")
NARRATION = re.compile(r"^(step \d+\b|this (function|method|class|code|block|line)\b|here we\b|now we\b|first,|next,|finally,|then we\b|loop (through|over)\b|we (will|now)\b)", re.I)
BANNER = re.compile(r"^\s*(#|//)\s*[=\-*#~]{6,}\s*$")
BROAD_EXCEPT = re.compile(r"^\s*except\b[^:]*\b(Exception|BaseException)\b[^:]*:\s*(pass|\.\.\.)?\s*(#.*)?$")
FILE_OK = re.compile(r"^\s*(<!--|#|//|/\*|\*)\s*tell-ok-file:\s*(T\d+)\s+(?!-->|\*/)\w", re.M)


def inline_ok(lines, i, cid):
    if cid in BLOCK:
        return False
    for j in (i, i - 1):
        if 0 <= j < len(lines) and re.search(rf"tell-ok:\s*{cid}\s+(?!-->|\*/)\w", lines[j]):
            return True
    return False


def prose_lines(lines):
    """(index, text) of Markdown prose, excluding frontmatter, fenced and indented code,
    HTML comments, tables, and headings. Inline code is removed."""
    fence, comment, prev_blank_or_code = None, False, True
    start = 0
    if lines and lines[0].strip() == "---":
        end = next((k for k in range(1, len(lines)) if lines[k].strip() == "---"), None)
        if end is not None:
            start = end + 1
    for i in range(start, len(lines)):
        l = lines[i]
        s = l.strip()
        if fence:
            m = re.match(r"^\s*(`{3,}|~{3,})\s*$", l)
            if m and m.group(1)[0] == fence[0] and len(m.group(1)) >= len(fence):
                fence = None
            continue
        m = re.match(r"^\s*(`{3,}|~{3,})", l)
        if m:
            fence = m.group(1)
            continue
        if comment:
            if "-->" in l:
                comment = False
            continue
        if s.startswith("<!--"):
            comment = "-->" not in s
            continue
        if re.match(r"^( {4}|\t)", l) and prev_blank_or_code:
            continue
        prev_blank_or_code = not s
        if not s or s.startswith(("|", "#")):
            continue
        yield i, re.sub(r"`[^`]*`", "", l)


def check_text(lines, add):
    words = dashes = bolds = 0
    for i, t in prose_lines(lines):
        m = PLACEHOLDER.search(t)
        if m:
            add("T01", i, m.group(0))
        m = DONE_CLAIM.search(t)
        if m and not EVIDENCE.search(lines[i]):
            add("T02", i, m.group(0))
        for cid, rx in PROSE:
            m = rx.search(t)
            if not m:
                continue
            if cid == "T16" and re.search(r"https?://|\[\d+\]|\]\(", t):
                continue
            if cid == "T17" and MEASURE.search(t):
                continue
            add(cid, i, m.group(0).strip())
        m = EMOJI.search(t)
        if m:
            add("T15", i, m.group(0))
        if not re.match(r"^\s*[-*] `", lines[i]):
            dashes += t.count("—")
        words += len(t.split())
        bolds += len(re.findall(r"\*\*[^*]+\*\*", re.sub(r"^\s*[-*]\s+\*\*[^*]+:\*\*", "", t)))
    if words >= 120 and dashes * 120 / words > 1.0:
        add("T14", 0, f"{dashes} em dashes in {words} prose words")
    if words >= 120 and bolds * 60 / words > 1.0:
        add("T15", 0, f"{bolds} bold spans in {words} prose words")


def check_code(lines, add):
    for i, l in enumerate(lines):
        if BANNER.match(l):
            add("T20", i, l.strip()[:40])
            continue
        m = COMMENT.match(l)
        if m:
            if NARRATION.match(m.group(2)):
                add("T20", i, m.group(2)[:50])
            if re.search(r"\b(TODO|FIXME)\b", m.group(2)):
                add("T01", i, "TODO/FIXME comment")
        if re.match(r"^\s*except\s*:", l):
            add("T21", i, "bare except")
        elif BROAD_EXCEPT.match(l):
            body = re.search(r":\s*(pass|\.\.\.)\s*(#.*)?$", l)
            nxt = next((x.strip() for x in lines[i + 1:] if x.strip() and not x.strip().startswith("#")), "")
            if body or nxt in ("pass", "..."):
                add("T21", i, "exception swallowed")
        if re.search(r"\bcatch\s*(\([^)]*\))?\s*\{\s*\}", l):
            add("T21", i, "empty catch")
        m = EMOJI.search(l)
        if m:
            add("T24", i, m.group(0))


def iter_files(paths):
    for p in paths:
        if not os.path.exists(p):
            print(f"ERROR {p}: not found"); sys.exit(2)
        if os.path.isfile(p):
            yield p
            continue
        for d, dirs, files in os.walk(p):
            dirs[:] = sorted(x for x in dirs if x not in SKIP_DIRS)
            for f in sorted(files):
                if f.lower().endswith(TEXT_EXT + CODE_EXT):
                    yield os.path.join(d, f)


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")
    flags = [a for a in sys.argv[1:] if a.startswith("--")]
    paths = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not paths or set(flags) - {"--block-only"}:
        print(__doc__); sys.exit(2)
    block_only = "--block-only" in flags
    findings = read_errors = 0
    for path in iter_files(paths):
        low = path.lower()
        if not low.endswith(TEXT_EXT + CODE_EXT):
            print(f"SKIP {path}: unsupported type"); continue
        try:
            text = open(path, encoding="utf-8-sig").read()
        except UnicodeDecodeError:
            print(f"ERROR {path}: not UTF-8"); read_errors += 1; continue
        lines = text.splitlines()
        file_ok = {m.group(2) for m in FILE_OK.finditer(text)}
        out = []

        def add(cid, i, what):
            if block_only and cid not in BLOCK:
                return
            if cid in file_ok or inline_ok(lines, i, cid):
                return
            out.append(f"{cid} {path}:{i + 1}: {what}")

        (check_text if low.endswith(TEXT_EXT) else check_code)(lines, add)
        for line in out:
            print(line)
        findings += len(out)
    print(f"{'FAIL' if findings or read_errors else 'OK'}: {findings} findings, {read_errors} unreadable")
    sys.exit(2 if read_errors else 1 if findings else 0)


if __name__ == "__main__":
    main()
