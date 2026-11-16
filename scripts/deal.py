#!/usr/bin/env python3
"""Deal a palette, type pairing, and hero layout for a web page from the curated library.

Usage: python3 deal.py --kind <software|gaming|tech|product|service|place> [--lang ko] [--mode light|dark]
                       [--history <file>] [--css <out.css>]
Choices come from assets/web/palettes.json and type.json, filtered by kind. The history file
(default .praxteward/deal-history.json in the current directory) records past deals, and each
new deal takes the least recently used option, so consecutive pages differ without random taste.
Prints the deal, the :root tokens, and the font link. Standard library only.
"""
import json, os, sys, time, urllib.parse

KINDS = ("software", "gaming", "tech", "product", "service", "place")
HERE = os.path.dirname(os.path.abspath(__file__))
LIB = os.path.join(HERE, "..", "assets", "web")


def opt(args, name, default=None):
    if name in args:
        k = args.index(name)
        if k + 1 < len(args):
            return args[k + 1]
        print(__doc__); sys.exit(2)
    return default


def least_recent(options, used):
    order = {u: n for n, u in enumerate(used)}
    return min(options, key=lambda o: (order.get(o["id"], -1), o["id"]))


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")
    args = sys.argv[1:]
    kind, lang, mode = opt(args, "--kind"), opt(args, "--lang"), opt(args, "--mode")
    hist_path = opt(args, "--history", os.path.join(".praxteward", "deal-history.json"))
    css_out = opt(args, "--css")
    if kind not in KINDS or mode not in (None, "light", "dark"):
        print(__doc__); sys.exit(2)
    palettes = json.load(open(os.path.join(LIB, "palettes.json"), encoding="utf-8"))["palettes"]
    library = json.load(open(os.path.join(LIB, "type.json"), encoding="utf-8"))
    history = []
    if os.path.isfile(hist_path):
        try:
            history = json.load(open(hist_path, encoding="utf-8"))
        except ValueError:
            history = []
    used = lambda key: [h[key] for h in history]

    pals = [p for p in palettes if kind in p["kinds"] and (mode is None or p["mode"] == mode)]
    types = [t for t in library["pairings"] if kind in t["kinds"] and (t.get("lang") == "ko") == (lang == "ko")]
    heroes = [h for h in library["heroes"] if kind in h["kinds"]]
    if not (pals and types and heroes):
        print(f"ERROR no library option for kind={kind} mode={mode} lang={lang}"); sys.exit(1)
    pal, typ, hero = least_recent(pals, used("palette")), least_recent(types, used("type")), least_recent(heroes, used("hero"))

    tokens = (":root {\n"
              f"  --bg: {pal['bg']}; --surface: {pal['surface']}; --text: {pal['text']}; --muted: {pal['muted']};\n"
              f"  --accent: {pal['accent']}; --on-accent: {pal['on_accent']}; --line: {pal['line']};\n"
              f"  --font-display: \"{typ['display']}\", {typ['fallback']}; --font-body: \"{typ['body']}\", {typ['fallback']};\n"
              "}\n")
    families = [typ["display"]] + ([typ["body"]] if typ["body"] != typ["display"] else [])
    query = "&".join("family=" + urllib.parse.quote_plus(f) + ":wght@" + typ["weights"] for f in families)
    link = f'<link rel="stylesheet" href="https://fonts.googleapis.com/css2?{query}&display=swap">'
    effects = kind in ("software", "tech", "gaming")
    print(f"kind: {kind}\npalette: {pal['id']} ({pal['mode']})\ntype: {typ['id']} ({typ['display']} / {typ['body']})\n"
          f"hero: {hero['id']}: {hero['note']}\n"
          f"effects allowed: {'yes, at most 4 live WebGL contexts, static fallback on phones and reduced motion' if effects else 'no: photographs, type, and flat color only'}\n")
    print(tokens)
    print(link)
    if css_out:
        with open(css_out, "w", encoding="utf-8") as f:
            f.write(tokens)
    os.makedirs(os.path.dirname(hist_path) or ".", exist_ok=True)
    history.append({"date": time.strftime("%Y-%m-%d"), "kind": kind, "palette": pal["id"], "type": typ["id"], "hero": hero["id"]})
    with open(hist_path, "w", encoding="utf-8") as f:
        json.dump(history[-50:], f, indent=1)


if __name__ == "__main__":
    main()
