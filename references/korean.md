# Korean prose

<!-- tell-ok-file: T10 the taxonomy quotes the patterns it removes -->
<!-- tell-ok-file: T11 the taxonomy quotes the patterns it removes -->
<!-- tell-ok-file: T12 the taxonomy quotes the patterns it removes -->
<!-- tell-ok-file: T13 the taxonomy quotes the patterns it removes -->
<!-- tell-ok-file: T14 the taxonomy quotes the patterns it removes -->
<!-- tell-ok-file: T30 the taxonomy quotes the patterns it removes -->
<!-- tell-ok-file: T31 the taxonomy quotes the patterns it removes -->
<!-- tell-ok-file: T32 the taxonomy quotes the patterns it removes -->
<!-- tell-ok-file: T33 the taxonomy quotes the patterns it removes -->

Use whenever writing Korean, and for `praxteward humanize`: revising Korean so it reads as written by a native writer of that genre. Generated Korean reads as foreign for two kinds of reasons. Older and smaller models carry English sentence structure over (번역투). Current large models write grammatical Korean but follow chatbot and template conventions: an empathy formula before the answer, bold labels with colons, symmetric "A가 아니라 B", one polite ending repeated for a whole page, and an aphorism as the last line. The first kind is easy to scan for; the second needs a reader. This file is the single source for the Korean pattern IDs. `scripts/ko_scan.py` detects the patterns marked `scan`, and output checks T30 to T33 enforce a subset on every Korean deliverable.

## Commands

| Request | Run |
|---|---|
| "AI 티 안 나게 다듬어줘", "윤문해줘", `praxteward humanize` | Full procedure |
| "고치지 말고 AI 흔적만 찾아줘", `praxteward humanize scan` | Steps 1 to 4, then report spans, severity, score, and route without editing |
| "1000자로 맞춰줘", `length=N` | Full procedure; step 8 holds the length within ±5% |
| "이 글 말투로", `voice=<sample>` | Full procedure; step 5 matches the sample's rhythm, endings, and speech level |
| `genre=<genre>` or a genre named in the request | Sets the genre profile (below) |
| "가볍게" / "꼼꼼하게", `strict` | Force the light or heavy route |

## Four rules

1. Meaning stays fixed. Facts, claims, claim strength, numbers, proper nouns, direct quotations, and the hedges on uncertain findings are preserved exactly. A hedge may change form, never strength or polarity.
2. Edit only flagged spans and the sentences the native read marks. A sentence nobody flagged stays as written.
3. Keep the genre. A column stays a column and a report stays a report; the speech level stays one level throughout.
4. Do not over-edit. Above 30% of characters changed, re-check each change against the request; at 50%, stop and show the diff unless the operator asked for a full rewrite.

Never add content to fill a gap, and never insert a new stock phrase while removing an old one.

## Procedure

1. Save the original unchanged.
2. Name the genre and the reader: report, column, essay, news, academic, legal, medical, policy, marketing, chat answer, social post, email, or fiction. The genre decides what is a convention and what is a tell (profiles below).
3. Scan: `python3 <skill-dir>/scripts/ko_scan.py <file> --genre <genre>`. It lists spans by severity, rhythm metrics, a weighted score per 1000 characters, and a route: light (under 5), standard (5 to 15), heavy (above 15). Treat the score as a ranking of where to look, not a verdict (see Calibration).
4. Native read. Read the whole text aloud in your head as a Korean reader of that genre and mark every sentence a native writer would not have produced, using the playbook below. This step finds what the scan cannot: rhythm, register, chatbot structure, and empty sentences. With subagents available on a standard or heavy route, also give a delegate only the text and this question: "한국어 원어민 독자로서, 이 글에서 번역문이나 기계가 쓴 글처럼 읽히는 문장을 모두 짚고 이유를 한 줄씩 적어 달라." Merge its marks with yours; drop marks you cannot explain.
5. Rewrite by route. Light: fix S1 spans and marked sentences in one pass. Standard: list target spans first, then rewrite only those. Heavy: as standard, section by section, then one pass for transitions and terminology. With a voice sample, run `ko_scan.py <draft> --voice <sample>` and move sentence length, its variation, comma share, joined-clause share, and endings toward the sample.
6. Audit: ask once more "what still makes this read as machine-written or translated?" and check: no S1 span remains; no new stock phrase; every number, name, and quotation intact; hedges keep their strength; one speech level; sentence and paragraph lengths uneven where the content allows; the first sentence carries content; the last sentence is a fact, a decision, or a next step rather than an aphorism.
7. Gate: `ko_scan.py <revised> --base <original> --genre <genre>` reports change rate, lost numbers, lost quotations, stock phrases introduced, whether every contrast pair (C-8) was wiped out (keep one), score gain, and a grade. Restore any lost number or quotation.
8. Grade and deliver. A: no S1, at most two S2, score improved 70% or more, nothing introduced. B: no S1, at most four S2, improved 50% or more. C: one or two S1, or two over-editing signals: one more targeted pass. D: three or more S1, a lost number or quotation, or a change rate of 50% or more: hand back for human review with the diff. Report the grade, change rate, and the substantive changes; with `length=N`, also characters with and without spaces.

When writing Korean from scratch rather than revising, apply the playbook while drafting and run steps 3, 4, and 6 on the draft before delivery.

## Genre profiles

`--genre` turns off patterns that are the genre's own convention.

| Genre | Conventions kept |
|---|---|
| legal, medical, policy | Hedges and possibility forms (A-10, G-1, G-2, I-5, K-13); formal nouns in legal text |
| academic | Section headings and "X: Y" titles, parenthetical citations, nominal style |
| news | Paragraphs of one or two sentences; "~것으로 나타났다" attributions |
| fiction | Pronouns including "그녀", mixed speech levels in dialogue, reflective and intensifying adverbs |
| essay | Reflective endings in literary essays |
| chat | Headings and short sections; bullets downgraded to S3 |
| slides | Label lines, bullets, bold labels, "X : Y" titles, and uniform short lines, in decks and 개조식 reports |

Genre also sets the speech level: reports, news, columns, and academic text use 해라체 (-다); notices, emails, and service answers use 합쇼체, with 해요체 only where the brand or the operator uses it; social posts and personal blogs may use 해요체 throughout. Mixing 합쇼체 and 해요체 in one formal piece is a tell (E-7b). 개조식 (lines ending in a noun or in -함, -음, -임, -됨) is the native form of Korean review decks and of institutional reports and official documents written that way; keep one ending for the whole deck or document and do not mix it with -다 sentences. Scan these with `--genre slides`.

## Native writing playbook

These are the habits that separate native Korean from generated Korean. Each line gives the generated form, then a native form. The examples are illustrations, not templates to paste.

**Sentence core**
- Predicate first in importance. Korean carries meaning in the verb; English carries it in nouns. "효율성 향상을 위한 프로세스 개선이 필요합니다" → "일하는 순서를 바꾸면 더 빨라집니다."
- Drop the subject and pronouns when context supplies them. "그는 회의에 늦었다. 그는 사과했다." → "그는 회의에 늦었다. 들어오자마자 사과했다."
- Use the active voice and a real agent. "결정이 내려졌다" → "운영위원회가 결정했다."
- Replace light verbs with the verb itself: "분석을 진행했다" → "분석했다", "회의를 실시했다" → "회의했다".
- English "have" and "one of the most" do not carry over: "높은 확장성을 가지고 있다" → "확장하기 쉽다"; "가장 중요한 요소 중 하나" → "중요한 요소다" or the actual rank.
- "가능하다" is not "can": "예약하는 것이 가능합니다" → "예약할 수 있습니다".

**Connection and rhythm**
- Join clauses with connective endings rather than sentence-initial connectives: "비가 왔다. 그리고 경기가 취소됐다." → "비가 와서 경기가 취소됐다."
- Vary endings and length. A page of "~습니다." in a row, or every sentence 30 to 40 characters, reads as generated. Mix a short sentence after a long one; let one paragraph be a single sentence when it carries one point.
- A comma after a connective ending ("-고,", "-며,") or after a topic particle ("이 문제는,") is usually unnecessary in Korean; remove it unless the sentence is ambiguous without it.
- Keep one speech level. Do not slide between "~합니다" and "~해요" in one piece.

**Structure**
- Start with the content. Delete announcements ("이 글에서는 ~을 정리해 보겠습니다"), empathy formulas ("그렇게 느끼셨다면 이미 중요한 첫걸음을 내디디신 거예요"), and "결론부터 말하면".
- End with a fact, a decision, or a next step. Delete aphoristic closers ("그것이야말로 ~의 첫걸음일지도 모릅니다", "~만으로도 충분합니다", "~할 때다") and closing offers ("원하시면 알려 주세요").
- Use prose for reasoning. Bullets, bold labels with colons ("**소진**: ~"), and numbered bold headings belong to reference material and to 개조식 decks and reports, not to columns, essays, or short answers.
- Use asymmetry. One "A가 아니라 B" per piece at most; replace symmetric pairs ("장점만 있는 것도, 단점만 있는 것도 아니다", "정부는 ~해야 하고, 의료계는 ~해야 한다") with the specific claim.
- Avoid comma lists of four abstract nouns ("치솟는 집값, 불안정한 일자리, 길어진 노동시간, ~"). Keep the one or two that matter and say what they do.

**Vocabulary**
- Prefer native and everyday words over Sino-Korean nominalizations where the register allows: "활용하다" → "쓰다", "진행하다" → the actual verb, "~적인 측면에서" → drop it.
- Cut stock modifiers: "다양한", "효과적으로", "지속적으로", "적극적으로", "체계적으로", "매우".
- Replace column clichés ("낯설지 않은 풍경", "현주소", "민낯", "숙제로 남았다", "기로에 섰다", "물꼬를 텄다") with the concrete fact.
- Keep English only for standard terms; gloss a term in parentheses once, not every time.

## Taxonomy

Severity: S1 is a strong signal alone and is removed first; S2 matters when it repeats (thresholds below); S3 matters only together with other patterns or in the genre named. No single pattern proves machine authorship. `scan` marks patterns `ko_scan.py` detects; the rest are found in the native read.

### A. Translationese

| ID | Pattern | Sev | Flag when | Fix |
|---|---|---|---|---|
| A-1 | "~에 대해(서)" | S2 | scan: 3 in one paragraph | Direct object |
| A-2 | "~를 통해(서)" | S2 | scan: 3 in one paragraph | Some to "~로", "~해서" |
| A-3 | "~에 있어(서)", "~에게 있어", "~하는 데 있어" | S2 | scan: any | "~에서", "~하는 데", "~에게" |
| A-4 | "~라는 점에서" | S2 | scan: 3 in the document | "~서", "~라는 이유로" |
| A-5 | "~와 관련하여", "~에 관해" | S3 | scan: any | "~에", "~의", "~을" |
| A-6 | "~에 기반하여", "~을 바탕으로" | S2 | scan: 3 in the document | "~로", "~을 보고" |
| A-7 | "~를 가지고 있다" | S2 | scan: any | "~가 있다", predicate adjective |
| A-7a | "의미를 가진다", "관심을 가지다" | S3 | scan: any | "뜻이 있다", "관심이 있다" |
| A-8 | Double passive ("되어진다", "보여지다", "쓰여지다") | S1 | scan: any | Active or single passive |
| A-9 | Agent passive ("~에 의해 ~되었다") | S2 | scan: any | Agent as subject |
| A-10 | "~할 수 있다" repeated | S2 | scan: 4 in the document | Vary the form; never turn it into a certainty |
| A-11 | "~을 위해", "~기 위해" | S2 | scan: 3 in one paragraph | "~려고", "~도록", or omit |
| A-12 | "만들어지다", "이루어지다" | S3 | scan: any | Active verb |
| A-13 | Nouns stacked without particles | S2 | read | Restore particles |
| A-14 | Sentence-initial "그리고" after a full stop | S2 | scan: 3 in the document | Connective ending |
| A-15 | Abstract subject with "보여준다/제공한다" | S2 | scan: any | Concrete subject; "~덕분에", "~에 따르면" |
| A-16 | Pronouns ("그는", "그것은", "이것은") where Korean drops them | S3 | scan: 5 in the document; read each | No antecedent in the last two sentences, restore the noun; one, drop it; two or more, repeat the noun phrase |
| A-16a | "그녀" | S1 | scan: any, except fiction | Name or noun phrase, or omit |
| A-18 | Left-stacked modifiers before a noun | S2 | read: three or more words of modifier | Split the sentence |
| A-19 | Stacked particles ("에서의", "으로의", "와의") | S2 | scan: 4 in the document | Rewrite as a clause |
| A-20 | Passive progressive ("~되고 있다") | S2 | scan: 3 in one paragraph | Some to a plain statement |
| A-21 | "단순한 X를 넘어 Y" | S2 | scan: any | "X만이 아니라 Y다" |
| A-22 | "명확하다/분명하다" as evaluation | S3 | scan: any | State the claim |
| A-23 | "발판을 마련하다", "지평을 열다" | S2 | scan: any in an outlook | The actual content |
| A-24 | "더 이상 ~않다" | S2 | scan: 2 in the document | "이제" |
| A-25 | "~에 위치한" | S3 | scan: any | "~에 있는" |
| A-26 | "~로 구성되어 있다" | S2 | scan: 2 in the document | "~로 되어 있다" or list |
| A-27 | "~를 포함한" | S2 | scan: 3 in the document | "~까지", "~와" |

### B. English terms

| ID | Pattern | Sev | Flag when | Fix |
|---|---|---|---|---|
| B-1 | The same term glossed in English parentheses every time | S2 | scan: second gloss | Gloss only the first use |
| B-2 | Promotional loanwords ("인사이트", "솔루션", "시너지", "니즈") | S2 | scan: 3 in the document | Korean words; keep standard technical terms |
| B-3 | English quotations pasted in | S2 | read | Translate and cite |

### C. Structure

| ID | Pattern | Sev | Flag when | Fix |
|---|---|---|---|---|
| C-1 | "첫째, 둘째, 셋째" | S2 | scan: 3 in the document | Fold in or vary |
| C-2 | Bullet blocks in prose genres | S2 (S3 in chat, report) | scan: 4 in a row | Prose |
| C-3 | Template headings (서론, 결론, 장점, 단점, 마치며) | S2 | scan: 2 headings | Name the content, or remove |
| C-4 | Every paragraph opens with its summary | S2 | read | Open some with a case or a quotation |
| C-5 | Emoji in lists, headings, emphasis | S1 | scan in headings; T15 in prose | Remove outside social posts |
| C-6 | A heading over every short block | S2 | scan: under 120 characters of prose per heading | Fewer headings |
| C-7 | "먼저, 반면, 결국" sequence | S2 | scan | Remove two |
| C-8 | Symmetric contrast ("A가 아니라 B", "A도, B도 아니다", "A인가, B인가") | S1 | scan: 2 in the document | Keep one; make the rest specific; never remove all |
| C-9 | "1) 2) 3)" inside prose | S2 | scan: any | Fold in |
| C-10 | "X: Y" headings | S2 | scan: 2 headings | One noun phrase |
| C-11 | Comma after a connective ending ("-고,", "-지만,") | S3 | scan: more than one per 90 characters | Remove the comma |
| C-12 | Share of sentences with a comma | S3 | scan: over 70% | Shorter sentences |
| C-13 | Comma after a topic or subject particle ("이 문제는,") | S2, S1 at 4+ | scan: 2 in the document | Remove the comma |
| C-14 | Comma after a sentence-initial connective ("또한,", "따라서,") | S2 | scan: 3 in the document | Remove the comma or the connective |

### D. Stock phrases

None of these may be introduced while revising.

| ID | Pattern | Sev | Flag when | Fix |
|---|---|---|---|---|
| D-1 | Wrap-up markers ("결론적으로", "따라서", "이를 통해", "요컨대") | S1 | scan: 4 combined | Keep one or two |
| D-2 | Significance inflation ("시사하는 바가 크다", "주목할 만하다") | S1 | scan: any | The concrete conclusion |
| D-3 | List openers ("세 가지로 나눌 수 있다", "다음과 같습니다:") | S1 | scan: any | Remove the opener |
| D-4 | Hype ("혁신적", "획기적", "압도적") | S1 | scan: 3 in the document | Numbers and facts |
| D-5 | Personified abstract subject ("데이터가 말해준다") | S2 | scan: any | The actual agent |
| D-6 | "~할 때다", "시점이다" endings | S2 | scan: any | A concrete verb |
| D-7 | "X에서 Y로", "X를 넘어 Y로" (also in headings) | S2 | scan: 2 in the text, or any heading | Say it directly |
| D-8 | Cleft ("필요한 것은 ~이다", "중요한 것은 ~이다") | S2 | scan: any | Subject and predicate directly |
| D-9 | "~로 이어진다", "직결된다", "귀결된다" | S2 | scan: 2 in the document | The concrete causal path |
| D-10 | "~하는 이유다" | S2 | scan: any | Forward statement |
| D-11 | "향후", "앞으로" openers in the last 30% | S2 | scan | Real date or condition, or remove |
| D-12 | Empty caveat signs ("과제도 남아 있다") | S2 | scan: any | The actual issue |
| D-13 | Reflective adverbs closing an essay ("어쩌면", "비로소") | S2 | scan: last 30% | Concrete statement |
| D-14 | Generated metaphors and column clichés ("여정", "나침반", "현주소", "민낯", "숙제로 남", "기로에 서") | S2 | scan: 2 in the document | Say it literally; keep at most one |
| D-15 | Chatbot residue ("좋은 질문입니다", "살펴보겠습니다", "정리해 드리겠습니다") | S1 | scan: any | Remove |

### E. Rhythm

| ID | Pattern | Sev | Flag when | Fix |
|---|---|---|---|---|
| E-1 | Uniform sentence length | S2 | scan: 8+ sentences, variation under 0.35, under 5% at 100+ characters | Mix short and long |
| E-2 | One ending repeated | S2 | scan: 4 in a row (6 for plain past "~었다") | Vary endings |
| E-3 | Every paragraph three or four sentences | S2 | scan: 4+ paragraphs | Mix lengths |
| E-4 | Clauses never joined | S2 | scan: under 15% of 8+ sentences | Join with connective endings |
| E-5 | Long comma segments | S3 | scan: over 12 words on average | Split |
| E-7 | 해라체 mixed with polite levels | S2 | scan: 2+ of each | One level |
| E-7b | 합쇼체 mixed with 해요체 | S2 in formal genres, S3 otherwise | scan: 2+ of each | One level |

### F to J. Modifiers, hedging, connectives, formal nouns, decoration

| ID | Pattern | Sev | Flag when | Fix |
|---|---|---|---|---|
| F-1 | Intensifiers ("매우", "정말", "상당히") | S2 | scan: more than one per 300 characters | Remove most |
| F-2 | Synonym doubling ("중요하고 핵심적인", "효율적이고 효과적인") | S2 | scan: any | Keep one |
| F-4 | "-적", "-성", "-화" nominalization | S2 | scan: 13 in the document | Verb or adjective root |
| F-5 | "~적 N ~적" chains | S2 | scan: 2 in the document | Verb phrases |
| F-7 | Generic policy verbs ("강화", "확대", "고도화", "최적화") | S2 | scan: 5 in the document | The concrete action |
| G-1 | Repeated "~로 보인다" | S2 | scan: 3 in the document | Vary the form, keep the strength |
| G-2 | Stacked hedges ("~할 수 있을 것으로 보인다") | S2 | scan: any | One hedge, same certainty |
| H-1 | Sentence-initial "또한", "따라서", "즉", "나아가" | S2 | scan: 3 in one paragraph | Remove about half there |
| H-2 | "하지만" and "그러나" both repeated | S2 | scan | Remove half or more |
| H-3 | Meta openers ("이는", "이처럼") | S2 | scan: 3 in one paragraph | Go straight to the statement |
| H-4 | "즉," | S2 | scan: 3 in the document | Omit |
| I-1 | "~것이다" endings | S2 | scan: 3 in one paragraph | Direct statements |
| I-2 | "~는 점이다", "~바이다" | S2 | scan: 3 in the document | "X는 ~다" |
| I-3 | "~라는 것이다", "~라는 뜻이다" | S2 | scan: 3 in the document | End with "~다" |
| I-4 | Paragraphs ending in "~해야 한다" | S2 | scan: 2 paragraphs | Move the obligation earlier; keep the mood |
| I-5 | "~이 필요하다" | S2 | scan: 3 in the document | Concrete subject and verb |
| I-6 | "~능력" chains | S2 | scan: 3 in the document | Verb forms |
| J-1 | Scattered bold | S2 | scan: 3+ spans, over one per 150 characters | Remove most |
| J-2 | Quotation marks for emphasis | S3 | scan: over five short quoted words | Real quotations only |
| J-3 | Em dashes | S2 | scan: 3 in the document | Comma, parentheses, or a new sentence |
| J-4 | Parenthetical asides | S3 | scan: more than one per 100 characters | Fold in or remove |

### K. Generative Korean

Patterns of current chat models, added from Praxteward's own comparison of model output with human text.

| ID | Pattern | Sev | Flag when | Fix |
|---|---|---|---|---|
| K-1 | "가장 ~ 중 하나" | S1 | scan: any | "손꼽히는", "대표적인", or the rank |
| K-2 | "~하는 것이 가능하다" | S1 | scan: any | "~할 수 있다" |
| K-3 | Light verbs ("~를 진행하다", "수행하다", "실시하다") | S2 | scan: 2 in the document | The verb itself |
| K-4 | "역할을 하다", "중요한 역할" | S2 | scan: any | What it does |
| K-5 | "~에 초점을 맞추다", "~에 주목하다" | S2 | scan: 2 in the document | A plain verb |
| K-6 | "~로 인해" | S2 | scan: 3 in the document | "~로", "~때문에" |
| K-7 | "이러한", "이와 같은", "해당" | S2 | scan: 4 in the document | Drop or "이" |
| K-8 | Stock adverbs ("효과적으로", "지속적으로", "적극적으로", "다양한") | S2 | scan: 5 in the document | Drop or name the method |
| K-9 | Service tone ("여러분", "~해 보세요", "하시길 권합니다", "~하는 것이 좋습니다") | S2 | scan: 2 in the document | Plain statements |
| K-10 | "만약" before a conditional | S2 | scan: 2 in the document | Drop "만약" |
| K-11 | "~의 ~의 ~의" | S2 | scan: any | One "의", rest as a clause |
| K-12 | Double approximation ("약 30% 정도") | S2 | scan: any | One of them |
| K-13 | Future "~할 것입니다" repeated | S2 | scan: 3 in the document | Present tense |
| K-14 | "~하는 경향이 있다", "~할 가치가 있다", "~에도 불구하고" | S2 | scan: 2 in the document | Direct forms |
| K-15 | "~지 않을 수 없다", "~하는 중이다" | S3 | scan: 2 in the document | Direct forms |
| K-16 | "~에 대한 이해/고민/논의" | S2 | scan: 3 in the document | Verb: "~을 이해하다" |
| K-17 | "~할 수 있도록" | S2 | scan: 3 in the document | "~하게", or omit |
| K-18 | Exclamation marks after formal endings | S2 | scan: 2 in the document | Remove |
| K-20 | Nearly every paragraph one sentence | S2 | scan: 80% of 4+ paragraphs | Join paragraphs |
| K-21 | Aphoristic last line ("~일지도 모릅니다", "~야말로", "첫걸음", "답이다") | S2 | scan: last sentence | A fact, decision, or next step |
| K-22 | Comma lists of four or more short items, repeated | S2 | scan: 2 sentences | Keep the one or two that matter |
| K-23 | Announcing the piece ("이 글에서는 ~을 정리해 보겠습니다") | S1 | scan: any | Remove; start with the content |
| K-24 | "어떻게 ~하느냐에 따라 결과가 달라진다" | S1 | scan: any | The actual condition and result |
| K-25 | Closing offer ("원하시면 ~ 알려 주세요") | S1 | scan: any | Remove |
| K-26 | "~것만으로도" | S2 | scan: 2 in the document | Direct statement |
| K-27 | Empathy and validation formulas ("그 자체로 이미 첫걸음", "~해도 괜찮습니다", "자연스러운 감정입니다") | S2 | scan: any | Remove, or one sentence of specific acknowledgment |
| K-28 | "결론부터 말하면," "요약하면," | S3 | scan: any | Give the conclusion |
| K-29 | "잊어서는 안 된다", "가볍게 넘길 일이 아니다" | S2 | scan: any | The actual consequence |
| K-30 | Balanced appeals ("양측 모두", "머리를 맞대야") | S2 | scan: any | Who does what |
| K-31 | Bold label with colon at line start ("**소진**: ~") | S2 (S3 in chat, report) | scan: 2 in the document | A sentence |
| K-32 | One-sentence acknowledgment of the question before the answer | S2 | read | Start with the answer |

Diagnostic signs with no fix of their own (read): an opening with no time anchor; quotations from unnamed sources (never invent one; flag them); no people in a narrative; no stake from the writer; every claim balanced by a counterclaim.

## Calibration

Measured on 2026-11-07 with `ko_scan.py` defaults (genre general). Human text: 247 chunks of about 900 characters from 10 Korean Wikipedia articles, and 22 random Korean Wikinews articles. Generated text: 40 pieces of 600 to 1000 characters, one per request (blog, report, column, service answer, product copy, essay, policy summary, email, social post, news, notice, review, abstract, and others), from three current Claude models, written in their default style by agents that did not know the patterns. 16 pieces were used to tune the patterns; 24 were held out, of which 5 were read while adding K-27 to K-30, so held-out figures are somewhat optimistic.

| Set | Median score | Score 5 or more | Score 10 or more |
|---|---|---|---|
| Human, encyclopedia | 0.5 | 8% | 0% |
| Human, news | 0.0 | 0% | 0% |
| Generated, held out | 5.4 | 62% | 12% |

Re-run with `python3 evals/korean/calibrate.py` from the repository (it downloads the human text). Patterns that separated best: E-2 (one ending repeated), E-1 (uniform length), J-1 (bold), E-7b (mixed polite levels), K-9 (service tone), C-2 and C-3 (bullets and template headings), D-8 (cleft). Classic translationese (A-3, A-8, D-2) was frequent in human encyclopedia text, which is often translated, and absent from current models; those patterns remain because they are style faults in any Korean, not because they identify a model. Commas after connective endings (C-11) were equally common in both and were downgraded to S3.

## Limits

A low score does not mean the text reads as native; current models write grammatical Korean whose foreignness is mostly structural and needs the native read in step 4. The scan finds form, not truth: it does not check facts or add sources. Thresholds come from a small corpus of encyclopedia and news text; columns, essays, and social posts by people were not measured, so expect more false positives there and read every span before editing.
