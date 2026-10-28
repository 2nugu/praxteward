# Design

The principles below apply to anything a person perceives or operates: documents, slides, pages, interfaces, figures, forms, command-line tools, and APIs. Sections 1 to 7 turn them into rules for visual deliverables (slides, pages, interfaces, figures, diagrams, formatted documents). Execute ranks each view (section 1) before laying it out and applies sections 2 to 6; Integrate checks section 7 and runs the design review on the rendered output. Existing brand or design-system rules take precedence; apply these inside them.

## Principles

When two principles conflict, the receiver's goal from the experience frame in [craft](craft.md) decides, and the trade-off is stated.

**Perception**

| Principle | Rule | Check |
|---|---|---|
| Purpose first | Form follows what the receiver must understand or do; every element serves that or goes. | Name the element's job in one clause. |
| Hierarchy | Importance is visible: the most important thing is seen, read, or reached first. | Squint test; first line or first screen holds the primary. |
| Contrast | Different things look clearly different; similar things look the same. A small difference reads as a mistake. | No near-miss sizes, colors, or alignments. |
| Proximity | Things that belong together sit together (Gestalt grouping). | Gap inside a group is about half the gap between groups or less. |
| Alignment | Every element lines up with something else; edges and baselines are shared. | No element sits on a line of its own. |
| Repetition | The same meaning gets the same form everywhere in the deliverable. | One style per role: heading, label, button, status, chart series. |
| Restraint | Less, but better (Rams): nothing that adds no information or function. | The removal pass in section 2. |

**Use**

| Principle | Rule | Check |
|---|---|---|
| Signifiers | What can be acted on looks actionable, and what cannot does not (Norman). | A first-time receiver can point to every action. |
| Feedback | Every action shows a result where attention is, within about 0.1 s for direct manipulation and with progress for anything over about 1 s. | Each action has a visible or printed outcome. |
| Mapping | Controls sit near and resemble what they affect; order follows the task. | Control order matches task order. |
| Constraints and forgiveness | Make errors hard to make and easy to undo; messages say what happened and what to do next. | Try the likely wrong input; check the result and the message. |
| Recognition over recall | Show options, current state, and context instead of making the receiver remember them (Nielsen). | No step needs information from an earlier screen or page that is no longer visible. |
| Familiarity | Follow the conventions receivers already know from similar work unless breaking them gains more than it costs. | Deviations from convention are listed with their reason. |

**Effort and access**

| Principle | Rule | Check |
|---|---|---|
| Fewer choices | Decision time grows with the number of options (Hick-Hyman); offer a default and few visible choices. | Count options per decision; default marked. |
| Reachable targets | Frequent and important targets are large and close (Fitts); destructive ones are apart. | Primary action largest and nearest; delete away from save. |
| Access for all | Works with keyboard, screen readers, color-vision deficiency, small screens, and low bandwidth. | Contrast and distinctness measured (section 5); keyboard path tried. |

## 1. Priority

- Rank the content of each view (screen, slide, page, figure) by what the receiver needs first, taken from the experience frame in [craft](craft.md): one primary, up to two secondary, the rest supporting. A view with two primaries has none.
- Show rank with as few cues as possible. Cues, in order of preference: position (first in reading order), size, weight, contrast, color. One or two cues per level are enough; putting all of them on one element adds noise and does not raise its rank.
- At most three levels of emphasis per view. When a fourth seems necessary, split the view or merge two levels.
- Squint test: blur the view or shrink it to a quarter. The primary must be the first thing seen. If it is not, change the rank cues before adding anything.

## 2. Reduction

- Removal pass, before any polishing: for each element, name what the receiver loses without it. If the answer is nothing, or something already shown elsewhere, remove it. Finishing work spent on an element that is later cut is waste.
- One cue per meaning. A group is shown by space, or a tint, or a line; never several at once. A status is color plus one label or icon, not color, icon, label, and badge together.
- One statement per fact. A subtitle does not repeat the title; a chart with direct labels has no legend; an icon beside a label that says the same thing goes, unless it is the scan target in a dense list.
- One place per action in a view. A second entry point stays only when the flow or measured use needs it.
- No decoration without information: stock images, ornamental icons, dividers between blocks that space already separates, shadows on flat content, gradients that encode nothing.

## 3. Grouping and boundaries

- Separate with space first. Related items sit closer to each other than to anything else; the gap inside a group is about half the gap between groups, or less.
- Escalate only when space is not enough, in this order: space, tint, line, container. Lines suit dense tables and long lists. Containers suit items that move, get selected, or act as one unit.
- No container inside a container of the same kind (a card in a card, a box in a box). Turn the inner level into space or a heading.
- Align to one grid. Shared edges do the work of boxes: every element starts on a column or baseline that something else also uses.
- When borders are used: one width, one low-contrast neutral color, one radius family across the deliverable.

## 4. Layers and overlays

- An overlay (modal, popover, sheet, toast, scrim over an image) is justified only for a decision that blocks progress, a transient confirmation, or a short detail tied to one spot. Everything else stays in the page.
- A modal never covers the information needed to answer it. For reversible actions, offer undo instead of a confirmation dialog; confirm only what cannot be undone, and name the consequence in the dialog.
- Use a fixed elevation scale (page, raised, overlay, top), one shadow or tint per level, and the same look for the same level everywhere.
- Text over an image or video gets a scrim or solid band; check its contrast against both the darkest and the lightest region behind it.
- Toasts and banners never cover the primary action and never stack. Show one at a time, the most severe first.

## 5. Color

- Assign roles before values. Neutral surfaces and text take most of the area. One accent marks the primary action or the key data series. Status colors (error, warning, success, info) are used for status only.
- A color keeps one meaning across the whole deliverable. Red that means "error" on one slide does not mean "region B" on the next.
- Saturation is a budget. Saturated color goes only where attention should land; large areas stay low in saturation.
- Contrast: body text at least 4.5:1 against its background; large text (24px, or 18.66px bold), UI boundaries, and meaningful icons at least 3:1. Measure with `python3 <skill-dir>/scripts/contrast.py FG BG`; do not judge by eye.
- Data color follows the data: one hue from light to dark for sequential values, two hues around a neutral midpoint for diverging values, at most about six hues for categories before the rest become "other".
- Categories must stay distinguishable with color-vision deficiency: check with `contrast.py --distinct C1 C2 ...`, and add a label, position, or shape so meaning never rests on hue alone. Red and green of similar lightness are the most common failure.
- With a dark mode, measure every pair again there.

## 6. Type and spacing

- One type family, two at most with a distinct role each. A size scale of four to six steps and two weights; no size outside the scale.
- Body lines of 45 to 75 characters; line height about 1.4 to 1.6 for body text, tighter for headings.
- Spacing from one scale (multiples of 4 or 8 px, or the slide or page equivalent); no one-off values.
- Numbers in tables are right-aligned, in tabular figures, with one number of decimals per column. Units go in the column header, not in every cell.

## 7. Finish

Check in the real medium at real size: export the PDF, render the slides, screenshot the page at phone and desktop widths. Source code is not evidence of how a thing looks.

- Edges: everything meant to align does, including icon optical centers and baselines across columns.
- Consistency: one radius family, one border weight, one capitalization style for labels and buttons, one date and number format.
- States: hover, visible focus, pressed, disabled, empty, loading, error, very long content, very short content.
- Text: no single orphaned word on a title or button; truncated text has a way to see the rest; nothing overflows at the narrowest supported width.
- Images and figures: sharp at display size, cropped on purpose, axes and units present, nothing clipped by the export.

## Design review (Integrate G5, Compile P7)

Run after the generic-feel review in [craft](craft.md), on the rendered output.

1. Squint test passes in every view.
2. Removal pass is done: each remaining element has a named loss if removed; list what was cut in the unit's record or report.
3. No meaning carries redundant cues; no same-kind containers are nested.
4. `contrast.py` passes for every text and UI pair in every mode; `--distinct` passes for categorical colors, or the colors are paired with labels.
5. The finish checks in section 7 pass.
6. A fix that recurs across tasks becomes an episode with `signal=repeat`, the start of a craft card for that artifact type.
