# Craft

<!-- tell-ok-file: T01 rule text names the placeholder pattern it forbids -->

Read before producing anything a person will read, see, run, or present. Plan records the experience frame; Execute applies the artifact rules; Integrate runs the generic-feel review.

## Experience frame (Plan L1)

| Question | Example answer |
|---|---|
| Who receives it, and what do they already know? | Lab PI, knows the method, has not seen the last two weeks of data |
| In what situation? | Reads on a phone between meetings; presents it to a committee; runs it at 2 a.m. during an outage |
| What must they understand, decide, or do afterwards? | Approve the second experiment; restart the service safely |
| First contact: what do they see in the first five seconds? | The decision needed and the one number behind it |
| Use: how do they act on it? | A command to copy; a table to compare; a figure to cite |
| Recovery: what happens when it fails or they disagree? | Error says what to check next; the rejected option and its evidence are one link away |

Shape the deliverable from these answers, not from a template.

## Solution selection

Before planning production, trace the affected flow from inputs to the receiver's outcome. Then choose the first sufficient approach:

1. Build nothing the need does not require: name in one line the features, options, and flexibility left out. When part of the request itself looks unjustified by the goal, say so before building.
2. Keep the artifact as it is when it already meets the criteria; explain the evidence.
3. Reuse or adjust an existing project capability, component, analysis, or source passage that fits the need.
4. Use a platform feature, standard tool, or installed dependency that fits the project's conventions.
5. Create only the missing part. New dependencies, layers, settings, and deliverables need a requirement the earlier options cannot meet.

Readability, correctness, and upkeep decide between sufficient options. Existing material must still fit the current need; reuse is not a reason to preserve a defect. Never remove required input checks, data-loss protection, security, accessibility, or scientific validity to reduce work. Use only the plan units and delegates the task needs; retain required records and checks.

## Reduce the path

Count the steps from first contact to the outcome: clicks, fields, pages, commands, or slides before the decision. Then cut.

- Remove each step whose removal loses nothing; merge steps that always happen together.
- Ask only for what cannot be inferred or defaulted. Defaults fit the most frequent receiver.
- Undo beats confirmation for reversible actions. Confirm only what cannot be undone, and name the consequence.
- Feedback and the next action appear where attention already is, at the point of action.
- Advanced options, details, and appendices sit one step away. What most receivers need is never hidden there.
- One way to do one thing. Keep a parallel path only when a distinct group of receivers needs it.

## Specificity

- Swap test: a sentence, slide, section, chart, or component that could move to another project unchanged is generic. Replace it with this project's names, numbers, cases, and constraints, or cut it.
- Content decides structure. A section exists because the reader needs it, not because such documents usually have one. No intro that restates the title, no summary that repeats the body.
- Real material over invented: real data, screenshots, quotes from sources, actual error messages. Missing material is labelled `to confirm: <what>`; it is never filled with plausible fiction.
- Decide for the reader when they need a decision: recommend one option, give the reason and the condition that would change it, then show the rest briefly.
- Uneven is honest. Three equal bullets, matching paragraph lengths, and a heading over every two sentences signal a template. Let the material set the shape: one strong point can stand alone; a hard point gets more space.
- One name per concept across the whole deliverable, taken from the reader's or the domain's vocabulary.

## Form

Settle form in Plan, on the first unit. The genre (what the deliverable is for and who receives it) sets structure and sentence form; the medium sets layout and the check; the convention is the accepted way of writing that genre. Take the convention from the first source that has one: the operator's or the receiving organization's template or kit, a practice card, the project's earlier deliverables, then common practice. A kit already in use is followed as given.

Most genres have one obvious form: a paper is prose, a guide is numbered steps. Decide explicitly where conventions compete:

| Deliverable | Competing conventions | Default |
|---|---|---|
| Report for a decision | Prose, or 개조식 with one ending throughout | Prose, unless the receiving organization writes 개조식 |
| Review deck (results, progress, funding or panel review) | Label lines under noun titles, each result with its baseline and condition; or claim titles | Label 개조식 for Korean institutional reviews |
| Talk (conference, seminar, pitch) | Claim titles that alone tell the argument, about thirty words of body each | Assertion-evidence |

The wrong convention is a form error even when every sentence is good. A convention the operator corrects twice becomes a craft card.

| Medium | Layout and density | Check |
|---|---|---|
| Document (docx, PDF, Markdown, print) | Paged; numbered figures and tables with takeaway captions; figures survive grayscale printing; detail in appendices | Rendered pages: breaks, captions, references |
| Slide deck (pptx, HTML deck on a fixed stage) | One message per slide; one smallest type size for the whole deck, set for the room; spoken detail in speaker notes | Rendered slides: overflow, wrapping, smallest type |
| Responsive page (HTML report, dashboard) | Answer in the first view; evidence one step away in folded details or filters; a print view | Renders at the widths in [design](design.md) section 7, without motion, and in print |

When the same material goes out in several forms (a paper, a deck, a page), write its core once: claims, numbers with their conditions, sources, and one name per concept. Derive each form from that core and check that numbers and terms match across forms. In a project with records, the records are the core and [Compile](../modes/compile.md) does the deriving.

## Artifact rules

Apply the principles in [design](design.md) to anything a person perceives or operates, including documents, command-line tools, and APIs. For visual deliverables (slides, pages, interfaces, figures, diagrams, formatted documents), also apply its rules on priority, reduction, boundaries, overlays, color, type, and finish.

**Prose.** One idea per paragraph, with a concrete example or number. Headings only where a reader navigates. Tables for comparisons across the same attributes. Figure and table captions state the takeaway, not the topic.

**Slides.** Whatever the convention, one visual grid, type scale, and sentence ending for the whole deck. When text overflows, cut words or split the slide; never shrink the type or drop a required item. No decorative stock images or icons that carry no information. End with the decision, the ask, or the next step, not "Thank you" or "Questions?".

**Data visuals.** Choose the chart for the question (change over time, comparison, distribution, relationship). Label lines and bars directly instead of using a distant legend. Show units and scales; start bar axes at zero. Color carries meaning, never decoration; no 3D, shadows, or gradients.

**Interfaces and web pages.** The primary action is obvious within five seconds. Mockups use realistic content, never lorem ipsum or placeholder metrics. Design the empty, loading, error, and long-content states. Text contrast meets WCAG AA. Avoid the default pattern of a hero, three feature cards, and a call to action unless the content calls for it; derive the layout from what the user does first.

**Code.** Judge growth by independent concepts, execution paths, dependencies, and places a rule must be updated; line count is supporting evidence. Before adding a path, find the existing owner of that behavior. Consolidate rules that must agree, preserving genuinely different contracts. Complete a replacement by removing superseded implementations, temporary adapters, unused imports introduced by the change, and obsolete branches within scope, after checking consumers including configuration and dynamic references. Keep boundaries that protect correctness or make responsibilities clear; do not merge unrelated jobs or compress code for a smaller diff. Explain necessary growth in the existing Rationale or reply. Levels, shortcuts, review, and audit: [lean](lean.md). Flag unrelated cleanup separately. Names follow the domain; errors explain recovery; comments explain reasons.

**Replies.** Answer first, then reasons. Match the operator's language and register. End with what was skipped or left unchecked and any risk the operator must know, in one or two lines; omit it when nothing was. No closing offers of further help unless a specific next step is worth naming.

## Generic-feel review (Integrate G5, Compile P7)

1. Read the deliverable as the receiver from the experience frame, in their situation.
2. Mark every part that fails the swap test, every invented or unlabelled filler, and every structure that exists because of habit.
3. Run `tell_scan.py` on the files for wording signals and judge each per [output checks](output.md). For visual deliverables, run the design review in [design](design.md) on the rendered output.
4. Independent review, when the deliverable is high-stakes or signals remain after your own pass: give a delegate only the deliverable, the experience frame, the form line (genre, medium, convention), and the remaining signals. It rules on each signal (defect or convention, with a reason) and marks where the receiver would get stuck or where the text reads as generic. Apply its rulings; drop marks it cannot explain. Without subagents, do this as a separate pass and say the review was not independent.
5. Fix what was found. When the same fix recurs across tasks, record an episode with `signal=repeat`; it may become a craft card for that task type.
