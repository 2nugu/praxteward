# Web pages

Use for `praxteward web` and any company, product, or event website or landing page. The aim is a page that looks designed for this business, not assembled from the generic generated landing page. Taste is set by constraints and a curated library, then checked in a real browser. The general rules in [design](design.md) still apply; this file adds the build kit and the house rules. An existing brand or design system takes precedence over the library.

Kit: `assets/web/starter.html`, `assets/web/system.css`, `assets/web/palettes.json`, `assets/web/type.json`, `scripts/deal.py`, `scripts/page_check.py`.

## House rules (these override the rest of this file)

1. No caption or description under any image, render, or visual. Licence credits go in one expandable footer line.
2. Every visual renders at 1440, 1024, 768, and 390 px. No empty grounds or broken effects.
3. One section per screen: the hero stands alone on the first screen, and each section is one or two screens tall at 1440 by 900.
4. Left and right content edges are equal; every block sits on the same wrap lines. The navigation stays fixed.
5. Small responses to the pointer: linked cards lift 2 px, photos zoom slightly, buttons step on hover and press on click; card loops cycle in 2.5 to 4 seconds. No tilt, carousels, or timed tabs.
6. Real photographs, and more of them, with strong backgrounds, heroes, and type.
7. Real full-color icons of known products where products are named, and small diagram visuals in cards.
8. Shader effects, 3D, scroll scenes, and ambient motion only for technical subjects (software, developer tools, AI, hardware, fintech, gaming). A cafe, bakery, guesthouse, clinic, or shop gets photographs, type, and flat color.
9. Contacts stay generic: street and district only, no house numbers, postcodes, coordinates, registration numbers, or real-format phone numbers; email addresses use `.example`.

## Kinds

| Kind | Examples | Lead with | Effects |
|---|---|---|---|
| software | SaaS, developer tool, app | Real product UI, node-and-line diagrams, lit feature cards | Allowed, at most four live WebGL contexts, static fallback on phones and reduced motion |
| tech | AI, hardware, fintech, infrastructure | Product shots, diagrams, data | Allowed, same limits |
| gaming | Game, studio, esports | Key art, gameplay frames | Allowed, same limits |
| product | Physical goods, consumer brand | Large product photographs, in three sections at most | None |
| service | Agency, clinic, school, consultancy | People and work photographs, type | None |
| place | Cafe, hotel, shop, venue | Place photographs, type, flat color | None |

## Run

1. Read the brief: the kind, what is sold, the buyer, the one main action, and the real material available (photos, UI captures, logos, facts, prices, hours). List what is missing as `to confirm`.
2. Write all copy first. The h1 names the category and the buyer; one hard fact (a number, a place, a date, a result) appears on the first screen; every button pairs a verb with an object; at most two hero actions; headings name things.
3. Plan by screens: record the kind, then one line per section with its idea, picture type, and screen count. On technical pages, note where the effect goes and its static fallback.
4. Deal, do not pick by taste: `python3 <skill-dir>/scripts/deal.py --kind <kind> [--lang ko] [--mode light|dark]`. It returns a palette, type pairing, and hero layout from the library for that kind, the least recently used in the project's deal history, so pages differ from one another. Use its tokens and font link as given. Never use violet or lavender anywhere in the page's own design (accent, ground, gradient, effect, or tint).
5. Build from `assets/web/starter.html` and `assets/web/system.css`: paste the dealt tokens, keep only the dealt hero variant, use the system's classes and tokens, and replace every `[[...]]` marker with the copy from step 2. Paste real UI captures with the client's names. Add a scene or effect only when the kind allows it.
6. Check and look: `python3 <skill-dir>/scripts/page_check.py <page.html> --kind <kind> --render <shots-dir>`. Fix every FAIL and re-run. Without Playwright, take screenshots at the four widths with the host's browser tool. Look at every screenshot yourself: first screen, edges, broken images, crowding at 390 px.
7. Report: the kind, the deal, the check results, what went unchecked, every assumed price, hour, or address, the assets the client must supply, and each stand-in image or text.

## Checklist

- First screen: says what is sold, for whom, with one hard fact; the hero fills the screen and holds its main button.
- Edges: every block on the wrap lines; no sideways scroll at any width.
- Restraint by kind: effects, grain, scenes, and moments only on technical pages.
- Motion: buttons and linked cards respond to the pointer; loops run 2.5 to 4 seconds; anything longer than 5 seconds has a pause control; reduced motion stops everything without hiding content; nothing reveals itself on scroll.
- Performance: no more than four live WebGL contexts; images sized and compressed; no layout shift from images without dimensions.
- Copy: headings name things, buttons pair a verb with an object, no invented reviews, quotes, customers, or figures.

## Never

- A card, row, or tile that animates on scroll, including reveals, fade-ins, parallax, and random blinking.
- Stock photographs presented as the client's own product, people, or place; a product page that never shows the product.
- A drawn imitation of a real logo; invented reviews, quotes, customers, or figures.
- Violet or lavender in the page's own design.
- Reproducing a reference site's code, copy, pictures, or signature effect.
- Editing the kit's `assets/web/` files or `scripts/` to clear a check. Report the conflict instead.
