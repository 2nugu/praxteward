#!/usr/bin/env python3
"""Check color pairs for WCAG contrast and color sets for distinguishability.

Usage:
  python3 contrast.py FG BG [FG BG ...] [--min 4.5]
      Contrast ratio per pair (WCAG 2.x). Exit 1 if any pair is below --min.
      Use 4.5 for body text, 3 for large text (24px, or 18.66px bold) and for
      UI boundaries and icons.
  python3 contrast.py --distinct C1 C2 [C3 ...] [--min-de 10]
      Smallest CIEDE2000 difference between any two colors, for normal vision
      and simulated protanopia, deuteranopia, and tritanopia (Machado et al.
      2009, severity 1.0). Exit 1 if any minimum is below --min-de. The default
      of 10 is a working threshold for chart categories, not a standard.
Colors: #rgb or #rrggbb (the # is optional). Exit 2 on bad input.
Standard library only.
"""
import math, re, sys

MACHADO = {
    "protan": ((0.152286, 1.052583, -0.204868), (0.114503, 0.786281, 0.099216), (-0.003882, -0.048116, 1.051998)),
    "deutan": ((0.367322, 0.860646, -0.227968), (0.280085, 0.672501, 0.047413), (-0.011820, 0.042940, 0.968881)),
    "tritan": ((1.255528, -0.076749, -0.178779), (-0.078411, 0.930809, 0.147602), (0.004733, 0.691367, 0.303900)),
}


def parse(s):
    h = s.strip().lstrip("#")
    if re.fullmatch(r"[0-9a-fA-F]{3}", h):
        h = "".join(c * 2 for c in h)
    if not re.fullmatch(r"[0-9a-fA-F]{6}", h):
        raise ValueError(f"not a hex color: {s}")
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def to_linear(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def luminance(rgb):
    r, g, b = (to_linear(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(fg, bg):
    a, b = sorted((luminance(fg), luminance(bg)), reverse=True)
    return (a + 0.05) / (b + 0.05)


def grade(r):
    if r >= 7: return "AAA"
    if r >= 4.5: return "AA"
    if r >= 3: return "AA large text / UI only"
    return "fails"


def lab(lin):
    r, g, b = lin
    x = (0.4124564 * r + 0.3575761 * g + 0.1804375 * b) / 0.95047
    y = 0.2126729 * r + 0.7151522 * g + 0.0721750 * b
    z = (0.0193339 * r + 0.1191920 * g + 0.9503041 * b) / 1.08883
    f = lambda t: t ** (1 / 3) if t > 216 / 24389 else (24389 / 27 * t + 16) / 116
    fx, fy, fz = f(x), f(y), f(z)
    return 116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)


def simulate(lin, kind):
    m = MACHADO[kind]
    return tuple(min(1.0, max(0.0, sum(m[i][j] * lin[j] for j in range(3)))) for i in range(3))


def de2000(l1, l2):
    L1, a1, b1 = l1; L2, a2, b2 = l2
    c1, c2 = math.hypot(a1, b1), math.hypot(a2, b2)
    cm = (c1 + c2) / 2
    g = 0.5 * (1 - math.sqrt(cm ** 7 / (cm ** 7 + 25 ** 7)))
    a1p, a2p = a1 * (1 + g), a2 * (1 + g)
    c1p, c2p = math.hypot(a1p, b1), math.hypot(a2p, b2)
    h1p = math.degrees(math.atan2(b1, a1p)) % 360
    h2p = math.degrees(math.atan2(b2, a2p)) % 360
    dL, dC = L2 - L1, c2p - c1p
    if c1p * c2p == 0:
        dh = 0
    elif abs(h2p - h1p) <= 180:
        dh = h2p - h1p
    else:
        dh = h2p - h1p - 360 if h2p > h1p else h2p - h1p + 360
    dH = 2 * math.sqrt(c1p * c2p) * math.sin(math.radians(dh / 2))
    Lm, cpm = (L1 + L2) / 2, (c1p + c2p) / 2
    if c1p * c2p == 0:
        hm = h1p + h2p
    elif abs(h1p - h2p) <= 180:
        hm = (h1p + h2p) / 2
    else:
        hm = (h1p + h2p + 360) / 2 if h1p + h2p < 360 else (h1p + h2p - 360) / 2
    t = (1 - 0.17 * math.cos(math.radians(hm - 30)) + 0.24 * math.cos(math.radians(2 * hm))
         + 0.32 * math.cos(math.radians(3 * hm + 6)) - 0.20 * math.cos(math.radians(4 * hm - 63)))
    sl = 1 + 0.015 * (Lm - 50) ** 2 / math.sqrt(20 + (Lm - 50) ** 2)
    sc, sh = 1 + 0.045 * cpm, 1 + 0.015 * cpm * t
    rt = (-2 * math.sqrt(cpm ** 7 / (cpm ** 7 + 25 ** 7))
          * math.sin(math.radians(60 * math.exp(-(((hm - 275) / 25) ** 2)))))
    return math.sqrt((dL / sl) ** 2 + (dC / sc) ** 2 + (dH / sh) ** 2 + rt * (dC / sc) * (dH / sh))


def take_option(args, name, default):
    if name in args:
        i = args.index(name)
        value = float(args[i + 1])
        del args[i:i + 2]
        return value
    return default


def main(argv):
    args = list(argv)
    try:
        if args and args[0] == "--distinct":
            limit = take_option(args, "--min-de", 10.0)
            names = args[1:]
            if len(names) < 2:
                raise ValueError("--distinct needs at least two colors")
            lins = [tuple(to_linear(c) for c in parse(n)) for n in names]
            failed = False
            for kind in ("normal", "protan", "deutan", "tritan"):
                labs = [lab(l if kind == "normal" else simulate(l, kind)) for l in lins]
                worst = min(((de2000(labs[i], labs[j]), names[i], names[j])
                             for i in range(len(labs)) for j in range(i + 1, len(labs))))
                ok = worst[0] >= limit
                failed |= not ok
                print(f"{kind:7} min dE2000 {worst[0]:5.1f}  {worst[1]} vs {worst[2]}  {'ok' if ok else 'too close'}")
            return 1 if failed else 0
        limit = take_option(args, "--min", 4.5)
        if not args or len(args) % 2:
            raise ValueError("give colors in FG BG pairs")
        failed = False
        for fg, bg in zip(args[::2], args[1::2]):
            r = ratio(parse(fg), parse(bg))
            failed |= r < limit
            print(f"{fg} on {bg}: {r:.2f}:1  {grade(r)}{'' if r >= limit else f'  below {limit:g}'}")
        return 1 if failed else 0
    except (ValueError, IndexError) as e:
        print(f"error: {e}\n{__doc__}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
