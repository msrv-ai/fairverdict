# Full article

The full report is a complete article that could be published as it is on a blog, a docs site, Medium, dev.to or GitHub. Its structure follows the comparison articles that rank and get read — roundups such as Zapier's "best X apps", LogRocket's library guides, Engadget's buying guides and the leading "X vs Y" pieces — and the review guidance search engines publish:

- the answer and named picks before the body;
- a table to scan;
- the method stated before the candidates: how many were compared, on what, with what evidence;
- one block per candidate, with the same fields every time, so each one stands on its own;
- the alternatives that were considered;
- "choose X if …" rules;
- an FAQ and a short bottom line.

It also fills the gaps that even good roundups leave: a score that means something, an explicit verdict, a "skip it if" for every candidate, and a robustness check.

Write it in the user's language, including headings. Address the reader as "you". The voice is a knowledgeable colleague: concrete, plain, no hype. Numbers and named evidence beat adjectives.

## Length

About **2,000–3,000 words for five candidates, tables included**, less for fewer. Spend words on the evidence and the differences that decide the choice; a section that has nothing to say is shortened, not padded. Never write to a word count.

## Section by section

- **Headline (H1)** — built from the frame, with the year; with the number of candidates when it's a ranking. Formulas (translate):
  - "The best <unit> for <job> in <year>: <N> compared"
  - "<N> <unit> for <job>, scored and ranked (<year>)"
  - head-to-head: "<A> vs <B> for <job> (<year>): <short verdict>"
  - switch: "Should you switch from <A> to <B>? <short verdict>"

  No "ultimate", no exaggeration, and no question the article doesn't answer.
- **Byline** — one italic line: date, the model actually running the analysis, the FairVerdict link, the number of candidates and criteria. When a follow-up revises the article, add an italic update line under it saying what changed and why; never refresh the date without a change.
- **Lede** — two to four sentences. Open with the reader's problem and the scale of the comparison, or with what changed this year (a release, a price or license change), taken from the research. Then give the answer. Never open with a definition of the category, a history lesson or "it depends".
- **Verdict callout** — the blockquote with the winner, the score out of 100, verdict strength, the lead over #2 and the main reason. It is the article's TL;DR.
- **Quick picks** — the overall winner plus at most three "best if …" picks, in the "<candidate> — best for <X>" form roundups open with. Each pick comes from the computed results — a candidate that wins when one criterion counts double or is dropped, or that leads one criterion by 2+ points — or from a verified fact ("the only one with a free self-hosted edition"). Never from reputation. Skip the list when no other candidate wins anything.
- **At a glance** — one table: rank, candidate, score /100, best for, main trade-off. Add a price or license column only when cost or licensing is a criterion or a must-have. Every eligible candidate is in it; disqualified candidates go under it, each with the must-have it failed.
- **What we compared** — the frame, written for the reader: the decision and the unit, including any reframing ("React is a library, so the real choice is …"); what counted as a contender and what was out of scope; how the candidates were chosen (named by the user, or by which adoption signals); and the assumptions.
- **How we scored** — a table of criteria with their weight and what 10/10 means. Then the must-haves and one short paragraph on method:
  - the rubric was fixed before research, and every candidate got the same research;
  - the key facts were checked by independent verifiers (say so if they weren't);
  - this is an analysis of published evidence — docs, release notes, benchmarks, surveys, issue trackers — not hands-on testing.
- **The ranking** — one H3 block per candidate, in rank order, using the candidate block below. This is the body of the article.
- **Also considered** — the notable options that didn't make the cut, each with a few words on why. Leave it out when there were none.
- **Scores by criterion** — the 0–10 matrix printed by the scoring script, with `*` marking low confidence. Then, in two to four sentences, the gap drivers: the criteria that put #1 ahead of #2, by how many weighted points, and where #2 wins instead.
- **How to choose** — "If <priority or situation>, pick <candidate>", one line per realistic situation. Draw them from the computed alternative weightings, the must-haves and the criterion leaders. This is where a reader whose priorities differ from the default finds their answer.
- **How solid is this verdict?** — cover:
  - the simulation share;
  - which tested weightings change the winner, or that none did;
  - places whose order is uncertain;
  - the fact-check counts as the verifiers returned them — confirmed, contradicted, not found, and not checked if any — and any fact the analysis settled itself afterwards;
  - any score the fact-check or the bias audit changed, and any change made after the totals were visible, with the totals before and after.

  "Not found" doesn't mean "disproved".
- **FAQ** — three to six questions a reader is likely to ask next, each as an H3 and answered in one to three sentences from the research: is it still maintained, what does it cost, how hard is migrating, does it support <platform>, which one is easiest to learn. Leave out a question the evidence can't answer.
- **Bottom line** — one short paragraph: who should pick the winner, who should pick something else, and the one condition that would change the verdict. No new facts.
- **Signature** — a horizontal rule, then one italic line as the last line: the report was made with AI, and FairVerdict by msrv was used for objective analysis, with its two links. Translate the sentences; keep "FairVerdict by msrv" and the links as they are.

Emoji stay out of the article body, as in editorial roundups: the 🥇 in the callout and ⛔ for a disqualified candidate are the only ones.

## Candidate block

```markdown
### <rank>. <candidate> — <score>/100<, best for <scenario> — only when the computed results support it>

*<One-line verdict: what it is best at, and the price you pay for it.>*

**Key facts:** <current version(s) and release date> · <license or pricing> · <platforms or deployment> · <one maintenance or adoption signal>

<Two to four sentences on why it ranks here, with the evidence behind its strongest and weakest criterion scores, and what changed in its latest versions if that matters for the choice.>

**Strengths**

- <strength, with its evidence>
- <a second only if real>

**Limitations**

- <limitation, with its evidence>
- <a second only if real>

**Best for:** <who or what situation> · **Skip it if:** <who or what situation>
```

- Every block has the same fields in the same order, so readers can compare blocks and jump straight to one.
- Key facts come from primary sources checked during the research or the fact-check — release notes, the repository, the package registry, official pricing — never from memory. Leave out anything unconfirmed rather than guess. For a closed-source candidate, use its pricing and platform facts.
- One to three strengths and one to three limitations, each with a concrete fact, number or kind of source ("in the 2026 developer survey", "per its release notes"). Never invent one for symmetry.
- When a score rests on thin evidence, say so in the block: "Evidence is thin on <criterion>; treat that score as provisional."
- The winner's block may point back to the callout instead of repeating it, but still lists its limitations.
- A disqualified candidate gets a two-line block: ⛔, the must-have it failed, and what it would need to qualify.

## Template — ranking

```markdown
# <Headline>

*<date> · AI analysis by <actual model> with [FairVerdict](https://msrv.dev/fairverdict/) · <N> candidates · <K> criteria*

<Lede: the reader's problem or what changed this year, the scale of the comparison, the answer.>

<Only if relevant: **Disclosure:** <actual provider relationship>.>
<Only for an unattended run: **Defaults used:** <what was assumed>.>

> ## 🥇 <winner>
>
> **<score> / 100** · <Clear | With caveats> · **+<lead> points** ahead of <#2>
>
> <Main advantage and the concrete evidence behind it; one or two sentences.>
>
> <Only when the winner is a prompt or procedure: **Use it:** <ready-to-use prompt or action>>

**Quick picks**

- **Best overall:** <winner> — <reason in a few words>
- **Best if <priority> matters most:** <candidate> — <reason>

## At a glance

| Rank | <Unit> | Score /100 | Best for | Main trade-off |
|:---:|---|:---:|---|---|
| 1 | **<winner>** | **<score>** | <scenario> | <limitation> |
| 2 | **<candidate>** | <score> | <scenario> | <limitation> |
| 3 | **<candidate>** | <score>* | <scenario> | <limitation> |

<Only if any: *\* Thin evidence; see that candidate's section.*>
<Only if any: ⛔ **<candidate>** — disqualified: <failed must-have>.>

## What we compared

<The decision and the unit in one or two sentences, including any reframing.>

- **In scope:** <what qualified as a contender>
- **Out of scope:** <adjacent categories or options left out, and why>
- **How the candidates were chosen:** <named by you | by <adoption signals>>
- **Assumptions:** <the frame's assumptions, such as a small team starting fresh>

## How we scored

| Criterion | Weight | What 10/10 means |
|---|:---:|---|
| <criterion> | <w>% | <anchor> |

**Must-haves:** <list, or "none">.

<Method in one short paragraph: rubric fixed before research; same research for every candidate; key facts checked by independent verifiers; an analysis of published evidence, not hands-on testing.>

## The ranking

<One candidate block per candidate, in rank order.>

## Also considered

- **<option>** — <why it didn't make the cut>

## Scores by criterion

<The score matrix from the scoring script, with translated headings.>

<Gap drivers: what puts #1 ahead of #2, in weighted points, and where #2 wins instead.>

## How to choose

- **If <priority or situation>:** <candidate> — <why, in a few words>
- **If <priority or situation>:** <candidate> — <why>

## How solid is this verdict?

<Simulation share for the winner and the runner-up; which tested weightings change #1, or none; uncertain places.>

**Fact-check:** <N> facts checked <independently | by the analysis itself> · **<n> confirmed · <n> contradicted · <n> not found**<, <n> not checked><; settled afterwards by the analysis: <facts>> · <corrections made>.

## FAQ

### <Question?>

<Answer in one to three sentences.>

## Bottom line

<Who should pick the winner, who should pick something else, and the one condition that would change the verdict.>

---

*This report was made with AI. [FairVerdict](https://msrv.dev/fairverdict/) by [msrv](https://msrv.dev) was used for objective analysis.*
```

## Variant — head-to-head

Two candidates read better as rounds than as a ranking. In "What we compared", add one sentence on what each candidate is. Replace "At a glance", "The ranking" and "Scores by criterion" with:

```markdown
## At a glance

| | **<A>** | **<B>** |
|---|---|---|
| Score /100 | **<score>** | <score> |
| Best for | <scenario> | <scenario> |
| Biggest strength | <strength> | <strength> |
| Biggest limitation | <limitation> | <limitation> |
| Current version | <version, date> | <version, date> |
| License / pricing | <fact> | <fact> |

## Round by round

### <Criterion> (<weight>%) — <A | B | Tie>: <the finding in a few words>

<Two to four sentences of evidence. End with the scores: **<A> <score> · <B> <score>**.>

<One round per criterion, highest weight first.>

## The scorecard

<The score matrix from the scoring script, then the gap drivers in two or three sentences.>
```

"How to choose" becomes "**Choose <A> if …**" and "**Choose <B> if …**", two to four bullets each. Keep the other sections.

## Variant — switch

For "should we move from <current> to <alternative>?", use the head-to-head variant, or the ranking for several alternatives with the current option marked "(current)". Then:

- The callout's headline is the decision — "Switch to <B>", "Stay on <A>" or "Switch only if <condition>" — with both scores.
- Add **What the move costs** after "What we compared": the evidence behind the switching-cost scores, covering migration work, retraining and lock-in.
- "How to choose" becomes "**Switch if …**" and "**Stay if …**".

## Variant — too close to call

- Replace the callout with `## Too close to call: <A> · <B>`, both scores and the priority that decides between them.
- No 🥇, no "winner" language, no forced first place. The two leaders share rank "1–2" in the tables and in their block headings, and neither row is bold.
- Quick picks become "**Pick <A> if …**" and "**Pick <B> if …**".
- The headline says the race is close and keeps the year and the count: "The best <unit> for <job> in <year>: <A> and <B> too close to call (<N> compared)", or for two candidates "<A> vs <B> for <job> (<year>): too close to call — what decides it".
- The bottom line names the deciding priority.
