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

## Specificity

- Swap test: a sentence, slide, section, chart, or component that could move to another project unchanged is generic. Replace it with this project's names, numbers, cases, and constraints, or cut it.
- Content decides structure. A section exists because the reader needs it, not because such documents usually have one. No intro that restates the title, no summary that repeats the body.
- Real material over invented: real data, screenshots, quotes from sources, actual error messages. Missing material is labelled `to confirm: <what>`; it is never filled with plausible fiction.
- Decide for the reader when they need a decision: recommend one option, give the reason and the condition that would change it, then show the rest briefly.
- Uneven is honest. Three equal bullets, matching paragraph lengths, and a heading over every two sentences signal a template. Let the material set the shape: one strong point can stand alone; a hard point gets more space.
- One name per concept across the whole deliverable, taken from the reader's or the domain's vocabulary.

## Artifact rules

**Writing and reports.** Put the answer or decision in the first lines. One idea per paragraph, with a concrete example or number. Headings only where a reader navigates. Tables for comparisons across the same attributes. Figure and table captions state the takeaway, not the topic.

**Slides.** Each slide title is a full claim; the titles alone tell the argument. Under the title, only the evidence for that claim: a figure, a number, a short quote. About thirty words of body at most. No decorative stock images or icons that carry no information. One visual grid and type scale for the whole deck. End with the decision or ask, not "Thank you" or "Questions?".

**Documents for use (guides, runbooks, READMEs).** Start with what the reader is trying to do. Steps are numbered, each with the command or action and how to tell it worked. Failure paths are written next to the step where they happen.

**Data visuals.** Choose the chart for the question (change over time, comparison, distribution, relationship). Label lines and bars directly instead of using a distant legend. Show units and scales; start bar axes at zero. Color carries meaning, never decoration; no 3D, shadows, or gradients.

**Interfaces and web pages.** The primary action is obvious within five seconds. Mockups use realistic content, never lorem ipsum or placeholder metrics. Design the empty, loading, error, and long-content states. Text contrast meets WCAG AA. Avoid the default pattern of a hero, three feature cards, and a call to action unless the content calls for it; derive the layout from what the user does first.

**Code.** Names come from the problem domain. Structure follows the problem, not a framework template; no layers, interfaces, or options without a current need. Error messages say what failed and what to do next. Comments explain why, not what.

**Replies.** Answer first, then reasons. Match the operator's language and register. No closing offers of further help unless a specific next step is worth naming.

## Generic-feel review (Integrate G5, Compile P7)

1. Read the deliverable as the receiver from the experience frame, in their situation.
2. Mark every part that fails the swap test, every invented or unlabelled filler, and every structure that exists because of habit.
3. Run `tell_scan.py` on the files for wording tells.
4. For a high-stakes deliverable with subagents available, give a delegate only the deliverable and the experience frame, and ask where it reads as generic or where the receiver would get stuck.
5. Fix what was found. When the same fix recurs across tasks, record an episode with `signal=repeat`; it may become a craft card for that task type.
