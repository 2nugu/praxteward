#!/usr/bin/env python3
"""Measure ko_scan.py on human-written and generated Korean.

Usage: python3 evals/korean/calibrate.py [--ids] [--cache <dir>]
Downloads human text once (Korean Wikipedia articles and random Korean Wikinews
articles, via the public MediaWiki API) into the cache directory, default
evals/korean/.cache, then scores 900-character chunks of it against the generated
samples in tune/ and heldout/. --ids adds the share of texts each pattern flags.
Wikinews pages are random, so the news figures vary slightly between caches.
"""
import collections, glob, json, os, sys, time, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "scripts"))
import ko_scan  # noqa: E402

WIKI = ["김치", "서울특별시", "세종", "한글", "비빔밥", "부산광역시", "경복궁", "독도", "태권도", "한국전쟁", "제주도", "김구", "고려"]
UA = {"User-Agent": "praxteward-calibration/1.0"}


def fetch(url, path):
    if not os.path.exists(path):
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=30) as r, open(path, "wb") as f:
            f.write(r.read())
        time.sleep(0.5)
    with open(path, encoding="utf-8") as f:
        return [p.get("extract", "") for p in json.load(f).get("query", {}).get("pages", {}).values()]


def chunks(text, size=900):
    cur = ""
    for p in [p.strip() for p in text.split("\n") if len(p.strip()) > 40]:
        cur += p + "\n\n"
        if len(cur) >= size:
            yield cur
            cur = ""


def stats(name, texts):
    ids, scores = collections.Counter(), []
    for t in texts:
        lines = t.splitlines()
        rows = [(i, l) for i, l in enumerate(lines) if l.strip()]
        found, m = ko_scan.diagnose(lines, rows)
        scores.append(ko_scan.score(found, m)[0])
        ids.update({f["id"] for f in found})
    scores.sort()
    n = len(scores) or 1
    q = lambda p: scores[min(len(scores) - 1, int(len(scores) * p))] if scores else 0
    print(f"{name:12} n={len(scores):3} median {q(.5):5} p90 {q(.9):5} | score>=5 {sum(s >= 5 for s in scores) / n:4.0%} "
          f">=10 {sum(s >= 10 for s in scores) / n:4.0%} >=15 {sum(s >= 15 for s in scores) / n:4.0%}")
    return ids, n


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")
    args = sys.argv[1:]
    cache = args[args.index("--cache") + 1] if "--cache" in args else os.path.join(HERE, ".cache")
    os.makedirs(cache, exist_ok=True)
    wiki, news = [], []
    for t in WIKI:
        url = ("https://ko.wikipedia.org/w/api.php?action=query&prop=extracts&explaintext=1&format=json&titles="
               + urllib.parse.quote(t))
        for e in fetch(url, os.path.join(cache, f"wiki-{t}.json")):
            wiki += list(chunks(e))
    for i in range(25):
        url = ("https://ko.wikinews.org/w/api.php?action=query&generator=random&grnnamespace=0&grnlimit=1"
               "&prop=extracts&explaintext=1&format=json")
        news += [e for e in fetch(url, os.path.join(cache, f"news-{i}.json")) if len(e) > 400]
    read = lambda d: [open(f, encoding="utf-8").read() for f in sorted(glob.glob(os.path.join(HERE, d, "*.md")))]
    sets = {"human-wiki": wiki, "human-news": news, "gen-tune": read("tune"), "gen-heldout": read("heldout")}
    res = {k: stats(k, v) for k, v in sets.items()}
    if "--ids" in args:
        print("id      " + " ".join(f"{k:>12}" for k in res))
        for i in sorted(set().union(*[r[0] for r in res.values()]), key=lambda i: -res["gen-heldout"][0][i]):
            print(f"{i:7} " + " ".join(f"{r[0][i] / r[1]:12.0%}" for r in res.values()))


if __name__ == "__main__":
    main()
