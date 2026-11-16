#!/usr/bin/env python3
"""Check a built web page against references/web.md. Standard library only; rendering is optional.

Usage: python3 page_check.py <page.html> --kind <software|gaming|tech|product|service|place> [--render <shots-dir>]
Static checks read the HTML, inline styles and scripts, and local stylesheets and scripts it links.
--render needs Playwright for Python with Chromium installed; it screenshots 1440, 1024, 768, and 390 px
widths and checks horizontal overflow, broken images, and equal content edges. Without it, rendering is
reported as not checked. Prints PASS, WARN, or FAIL per rule; exit 1 on any FAIL, 2 on usage errors.
"""
import colorsys, os, re, sys
from html.parser import HTMLParser

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import contrast  # noqa: E402

KINDS = ("software", "gaming", "tech", "product", "service", "place")
EFFECT_KINDS = ("software", "gaming", "tech")
WIDTHS = (1440, 1024, 768, 390)


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tags, self.text, self.styles, self.scripts, self.links = [], [], [], [], []
        self._in = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        self.tags.append((tag, a))
        if tag in ("style", "script"):
            self._in = tag
            if tag == "script" and a.get("src"):
                self.links.append(("script", a["src"]))
        if tag == "link" and "stylesheet" in (a.get("rel") or ""):
            self.links.append(("style", a.get("href", "")))
        if a.get("style"):
            self.styles.append(a["style"])

    def handle_endtag(self, tag):
        if tag == self._in:
            self._in = None

    def handle_data(self, data):
        if self._in == "style":
            self.styles.append(data)
        elif self._in == "script":
            self.scripts.append(data)
        elif data.strip():
            self.text.append(data.strip())


def hex_colors(css):
    for m in re.finditer(r"#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b", css):
        h = m.group(1)
        h = "".join(c * 2 for c in h) if len(h) == 3 else h
        yield m.group(0), tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    for m in re.finditer(r"rgba?\(\s*(\d+)[ ,]+(\d+)[ ,]+(\d+)", css):
        yield m.group(0), tuple(int(m.group(i)) / 255 for i in (1, 2, 3))
    for m in re.finditer(r"hsla?\(\s*(\d+(?:\.\d+)?)(?:deg)?[ ,]+(\d+(?:\.\d+)?)%[ ,]+(\d+(?:\.\d+)?)%", css):
        r, g, b = colorsys.hls_to_rgb(float(m.group(1)) / 360, float(m.group(3)) / 100, float(m.group(2)) / 100)
        yield m.group(0), (r, g, b)


def violet(rgb):
    h, l, s = colorsys.rgb_to_hls(*rgb)
    return 255 <= h * 360 <= 300 and s >= 0.25 and 0.12 <= l <= 0.92


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")
    args = sys.argv[1:]
    def opt(name):
        if name in args:
            k = args.index(name)
            return args[k + 1] if k + 1 < len(args) else ""
        return None
    kind, shots = opt("--kind"), opt("--render")
    files = [a for i, a in enumerate(args) if not a.startswith("--") and (i == 0 or args[i - 1] not in ("--kind", "--render"))]
    if len(files) != 1 or kind not in KINDS or shots == "":
        print(__doc__); sys.exit(2)
    path = files[0]
    if not os.path.isfile(path):
        print(f"ERROR {path}: not found"); sys.exit(2)
    html = open(path, encoding="utf-8-sig").read()
    page = Page(); page.feed(html)
    base = os.path.dirname(os.path.abspath(path))
    for kind_, href in page.links:
        local = os.path.join(base, href.split("?")[0])
        if not re.match(r"^(https?:)?//", href) and os.path.isfile(local):
            (page.styles if kind_ == "style" else page.scripts).append(open(local, encoding="utf-8-sig").read())
    css, js, text = "\n".join(page.styles), "\n".join(page.scripts), "\n".join(page.text)
    code = css + "\n" + js + "\n" + html
    results = []
    def rule(level, name, detail=""):
        results.append((level, name, detail))

    metas = [a for t, a in page.tags if t == "meta"]
    rule("PASS" if any(a.get("name") == "viewport" for a in metas) else "FAIL", "viewport meta")
    root = next((a for t, a in page.tags if t == "html"), {})
    rule("PASS" if root.get("lang") and "[[" not in root.get("lang") else "WARN", "html lang")
    markers = re.findall(r"\[\[[^\]]{0,60}\]\]|lorem ipsum|\bTODO\b|Your Company|John Doe|Jane Doe|example text", html, re.I)
    rule("FAIL" if markers else "PASS", "no placeholder or template text", ", ".join(sorted(set(markers))[:5]))
    h1 = sum(t == "h1" for t, _ in page.tags)
    rule("PASS" if h1 >= 1 else "FAIL", "h1 present", f"{h1} found")

    imgs = [a for t, a in page.tags if t == "img"]
    no_alt = [a.get("src", "?") for a in imgs if "alt" not in a]
    rule("FAIL" if no_alt else "PASS", "every image has alt text", ", ".join(no_alt[:3]))
    no_size = [a.get("src", "?") for a in imgs if not (a.get("width") and a.get("height"))]
    rule("WARN" if no_size else "PASS", "images declare width and height (no layout shift)", ", ".join(no_size[:3]))
    captions = sum(t == "figcaption" for t, _ in page.tags) + sum(1 for t, a in page.tags if re.search(r"\bcaption\b", a.get("class") or ""))
    rule("FAIL" if captions else "PASS", "no captions under images", f"{captions} found")

    bad = sorted({s for s, rgb in hex_colors(css) if violet(rgb)})
    rule("FAIL" if bad else "PASS", "no violet or lavender in the page's own colors", ", ".join(bad[:5]))

    libs = sorted({m.group(0) for m in re.finditer(r"data-aos|\baos(?:\.min)?\.(?:js|css)|ScrollTrigger|scrollreveal|animation-timeline\s*:\s*view|wow\.js|\bsal\.js", code, re.I)})
    rule("FAIL" if libs else "PASS", "nothing animates on scroll", ", ".join(libs))
    if "IntersectionObserver" in js:
        rule("WARN", "IntersectionObserver in use", "confirm it only loads or plays media and never reveals content")
    carousel = re.findall(r"swiper|slick|owl-carousel|glide\.js|splide|vanilla-tilt|tilt\.js|\bcarousel\b", code, re.I)
    rule("FAIL" if carousel else "PASS", "no carousels, tilt, or timed tabs", ", ".join(sorted({c.lower() for c in carousel})[:4]))
    webgl = len(re.findall(r"getContext\(\s*['\"](webgl2?|experimental-webgl)['\"]", js)) + len(re.findall(r"new\s+(THREE\.)?WebGLRenderer", js))
    if kind not in EFFECT_KINDS:
        rule("FAIL" if webgl else "PASS", f"no WebGL or shaders on a {kind} page", f"{webgl} contexts")
    else:
        rule("FAIL" if webgl > 4 else "PASS", "at most 4 live WebGL contexts", f"{webgl} found")
    moving = re.search(r"@keyframes|\banimation\s*:|\btransition\s*:|requestAnimationFrame", code)
    rule("FAIL" if moving and "prefers-reduced-motion" not in code else "PASS", "reduced motion respected")
    rule("PASS" if re.search(r"\.nav[^{]*\{[^}]*position\s*:\s*(fixed|sticky)", css) or re.search(r"position\s*:\s*(fixed|sticky)", css) else "WARN", "navigation stays fixed")

    hero = re.search(r"<section[^>]*class=\"[^\"]*hero[^\"]*\"[^>]*>(.*?)</section>", html, re.S | re.I)
    if hero:
        n = len(re.findall(r"class=\"[^\"]*\bbtn\b", hero.group(1)))
        rule("WARN" if n > 2 else "PASS", "at most two hero actions", f"{n} found")
        heroes = len(re.findall(r"<section[^>]*class=\"[^\"]*\bhero\b", html, re.I))
        rule("FAIL" if heroes > 1 else "PASS", "one hero variant kept", f"{heroes} found")
    phones = re.findall(r"tel:\+?\d|\b0\d{1,2}[-. ]\d{3,4}[-. ]\d{4}\b|\(\d{3}\)\s?\d{3}-\d{4}|\+\d{1,3}[ -]\d{2,4}[ -]\d{3,4}", html)
    emails = [e for e in re.findall(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+", html) if not e.endswith(".example")]
    rule("WARN" if phones or emails else "PASS", "contacts generic (.example, no real-format numbers)", ", ".join((phones + emails)[:4]))
    stock = re.search(r"unsplash|pexels|pixabay|shutterstock|istock", html, re.I)
    credit = re.search(r"<footer.*?(credit|사진|photo)", html, re.S | re.I)
    rule("WARN" if stock and not credit else "PASS", "library photos credited in one footer line")

    tokens = dict(re.findall(r"--(bg|surface|text|muted|accent|on-accent)\s*:\s*(#[0-9a-fA-F]{3,6})", css))
    pairs = [("text", "bg", 4.5), ("muted", "bg", 4.5), ("text", "surface", 4.5), ("on-accent", "accent", 4.5)]
    low = [f"{a}/{b} {contrast.ratio(contrast.parse(tokens[a]), contrast.parse(tokens[b])):.2f}"
           for a, b, need in pairs if a in tokens and b in tokens
           and contrast.ratio(contrast.parse(tokens[a]), contrast.parse(tokens[b])) < need]
    rule("FAIL" if low else "PASS" if tokens else "WARN", "token contrast at least 4.5:1", ", ".join(low) or ("" if tokens else "no tokens found"))

    if shots is None:
        rule("WARN", "rendered at 1440, 1024, 768, 390 px", "not checked: run with --render <dir>, or screenshot with the host's browser tool")
    else:
        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            rule("WARN", "rendered at 1440, 1024, 768, 390 px", "not checked: Playwright for Python is not installed")
        else:
            os.makedirs(shots, exist_ok=True)
            with sync_playwright() as p:
                browser = p.chromium.launch()
                for w in WIDTHS:
                    pg = browser.new_page(viewport={"width": w, "height": 900})
                    pg.goto("file://" + os.path.abspath(path).replace(os.sep, "/"))
                    pg.wait_for_load_state("networkidle")
                    info = pg.evaluate("""() => {
                      const over = document.documentElement.scrollWidth > innerWidth + 1;
                      const broken = [...document.images].filter(i => i.complete && i.naturalWidth === 0).map(i => i.src);
                      const edges = [...document.querySelectorAll('.wrap')].map(e => {
                        const r = e.getBoundingClientRect(), cs = getComputedStyle(e);
                        return [Math.round(r.left + parseFloat(cs.paddingLeft)), Math.round(innerWidth - r.right + parseFloat(cs.paddingRight))];
                      });
                      const uneven = edges.filter(([l, r]) => Math.abs(l - r) > 2).length;
                      return {over, broken, uneven};
                    }""")
                    pg.screenshot(path=os.path.join(shots, f"page-{w}.png"), full_page=True)
                    rule("FAIL" if info["over"] else "PASS", f"{w}px: no horizontal scroll")
                    rule("FAIL" if info["broken"] else "PASS", f"{w}px: every image loads", ", ".join(info["broken"][:3]))
                    rule("FAIL" if info["uneven"] else "PASS", f"{w}px: equal left and right content edges", f"{info['uneven']} uneven blocks")
                    pg.close()
                browser.close()
            rule("PASS", "screenshots written", shots + " (look at each one before delivery)")

    for level, name, detail in results:
        print(f"{level} {name}" + (f": {detail}" if detail else ""))
    fails = sum(r[0] == "FAIL" for r in results)
    print(f"{'FAIL' if fails else 'OK'}: {fails} fail, {sum(r[0] == 'WARN' for r in results)} warn, {sum(r[0] == 'PASS' for r in results)} pass")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
