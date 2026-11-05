# Short post

The short report is a post: a verdict that reads well on Reddit, in any Markdown viewer, and in a minute. Its structure follows the comparison posts that earn the most upvotes on Reddit, Hacker News and dev.to — "tested so you don't have to" results, "same thing in N stacks: the numbers", switch stories. Those posts share a pattern:

- the verdict and the scale sit in the title;
- the opening lines establish credibility instead of summarising;
- each option gets a compact block or table row, with the winner in bold and a number behind every claim;
- the method is a short paragraph after the results;
- a "who should pick what" line;
- often one specific question at the end.

What they avoid matters as much: a marketing voice, decorative emoji, wide tables, one heading per option, and generic claims without numbers. All of these read as SEO or AI filler and get ignored.

Write it in the user's language. Plain, specific, a little dry: the numbers do the persuading. No hype words, no greeting, no sign-off.

## Length

**300–500 words for five candidates, table included**, less for fewer. Don't pad a smaller comparison.

## Rules

- **Headline (H1)** — the title of the post, carrying the verdict and the scale, built from the frame. On Reddit it goes in the title field. Concrete numbers, no clickbait, no "surprising" or "beats everything". Formulas (translate):
  - ranking: "<winner> is the best <unit> for <job>: <N> options scored on <K> criteria"
  - head-to-head: "<A> vs <B> for <job>: <winner> wins <score> to <score>"
  - switch: "Should you switch from <A> to <B>? <Switch | Stay> — <score> vs <score>"
  - too close to call: "<A> vs <B> for <job>: too close to call, <score> to <score> (<N> options scored)"
- **Byline** — one italic line: the date and the model actually running the analysis. No link here: on Reddit a post that opens with a link to its maker's site reads as promotion, so the links wait for the signature at the end.
- **Opening** — one or two sentences that establish credibility, the way strong posts open with how long the author ran the tools:
  - how many options were compared, on how many criteria, fixed before any research;
  - how many key facts were checked;
  - what "best" means here, with the main assumption.

  Don't summarise the verdict; the title and the callout do that.
- **Verdict callout** — the blockquote with the winner, the score out of 100, verdict strength, the lead, and the evidence behind it with at least one number. It is the visual centre of the post.
- **Catch** — the winner's most important limitation, in one line.
- **The ranking** — one table, four columns at most so it reads on a phone: rank, option, score, payoff → trade-off. Bold the winner's row; leave the other rows plain. Give every payoff and trade-off a concrete number or fact where the research has one. `*` marks thin evidence, explained in one line under the table. Disqualified candidates go under the table with ⛔ and the must-have they failed.
- **Why it wins** — two or three bullets, one per gap driver, each with its evidence and its weighted points.
- **Who should pick what** — the default pick, then the computed alternatives as "<candidate> if <priority> matters most", then the robustness result: the simulation share, or that no tested weighting changes #1. Never invent a flip.
- **How it was judged** — the method, after the results, in one compact paragraph:
  - who chose the candidates, and the notable options left out;
  - the criteria with their weights;
  - that the rubric was fixed before research;
  - the fact-check counts as the verifiers returned them, and any fact settled afterwards.
- **Discussion question** — only when the user is posting for an audience: one specific question that asks for experience the analysis couldn't measure ("Shipped one of these to production? Where did it hurt?"). Never "Thoughts?".
- **Edit line** — when a follow-up revises the post, add "**Edit:** <what changed and why>" right under the byline, so readers see what moved.
- **Signature** — the last line, in italics: the report was made with AI, and FairVerdict by msrv was used for objective analysis, with its two links. Translate the sentences; keep "FairVerdict by msrv" and the links as they are. These are the post's only links, and the line doubles as its AI disclosure.

## Markdown that survives Reddit

- Below the H1, use `###` for every heading: `#` and `##` render oversized on Reddit.
- Put a blank line before and after every table and list. Single line breaks are ignored, so separate lines with blank lines.
- Never put a blank line inside a table.
- Use `-` bullets. Nest them one level at most. Never interrupt a numbered list with a paragraph, because the numbering restarts.
- No fenced code blocks, which break on old Reddit. Put a prompt in quotes, or indent it by four spaces.
- No HTML, images, footnotes or task lists.
- Emoji: the 🥇 in the callout, and ⛔ for a disqualified candidate. Nothing else.

## Template — ranking

```markdown
# <Headline>

*<date> · AI analysis by <actual model>*

<Opening: <N> <unit> scored on <K> criteria fixed before any research, <M> key facts checked; "best" here means <goal, main assumption>.>

<Only if relevant: **Disclosure:** <actual provider relationship>.>
<Only for an unattended run: **Defaults used:** <what was assumed>.>

> ### 🥇 <winner>
>
> **<score> / 100** · <Clear | With caveats> · **+<lead> points** ahead of <#2>
>
> <Main advantage and the concrete evidence behind it, with at least one number; one or two sentences.>
>
> <Only when the winner is a prompt or procedure: **Use it:** "<ready-to-use prompt or action>">

**Catch:** <the winner's most important limitation>.

### The ranking

| # | <Unit> | Score | Payoff → trade-off |
|:---:|---|:---:|---|
| 1 | **<winner>** | **<score>** | **<payoff with a number> → <trade-off>** |
| 2 | <candidate> | <score> | <payoff> → <trade-off> |
| 3 | <candidate> | <score>* | <payoff> → <trade-off> |

<Only if any: *\* Thin evidence; treat as provisional.*>

<Only if any: ⛔ **<candidate>** — disqualified: <failed must-have>.>

### Why <winner> wins

- **<criterion>** (+<points> weighted): <evidence with a number>
- **<criterion>** (+<points>): <evidence>

### Who should pick what

- **<winner>** — <who it suits: the default pick>
- **<candidate>** — if <priority> matters most
- <**<N>%** of 5,000 simulations go to <winner> · <no tested weighting changes #1 | which weighting does>>

---

**How it was judged:** <N> <unit> <named by you | chosen by <signals>><; left out: <option> (<reason>)> · <criterion> <w>% · <criterion> <w>% · … · rubric fixed before research · <n> facts checked<, independently>: **<n> confirmed · <n> contradicted · <n> not found**<, <n> not checked><; settled afterwards: <fact>><; corrections: <what changed and why>, <#1> <total before> → <total after>>.

<Only when posting for an audience: **<Discussion question>**>

*This report was made with AI. [FairVerdict](https://msrv.dev/fairverdict/) by [msrv](https://msrv.dev) was used for objective analysis.*
```

## Variant — head-to-head

For exactly two candidates, replace "The ranking" with a scorecard by criterion, highest weight first. Bold the higher score in each row:

```markdown
### Round by round

| Criterion (weight) | <A> | <B> | Edge |
|---|:---:|:---:|---|
| <criterion> (<w>%) | **<score>** | <score> | <A>: <evidence in a few words> |
| **Total /100** | **<score>** | <score> | <lead> points |
```

"Why <winner> wins" then names the two or three rounds that decided it, and "Who should pick what" says who should still pick the other one.

## Variant — switch

- The headline and the callout lead with the decision — "**Switch to <B>**", "**Stay on <A>**" or "**Switch only if <condition>**" — with both scores.
- The scorecard includes the switching-cost criterion.
- "Who should pick what" becomes "Who should switch, who should stay".

## Variant — too close to call

- The callout becomes `### Too close to call: <A> · <B>`, with both scores and the priority that decides between them.
- No 🥇 and no "winner" language. The two leaders share rank "1–2" in the table, and neither row is bold.
- The catch gives each leader's main limitation in one line.
- Rename "Why <winner> wins" to "What decides between them".
- "Who should pick what" splits on the deciding priority.

## Other platforms

When the user names a destination other than Reddit or a Markdown site, keep the same order and adapt:

- **No tables (X, LinkedIn, Telegram, Hacker News)** — replace each table with ranked lines: "1. <candidate> — <score>/100 — <payoff> → <trade-off>".
- **No bold either (X, LinkedIn, Hacker News)** — write plain text and keep the line breaks. In the signature, put each link as a bare URL after its name.
- **X thread** — the headline and the callout make the first post, then one post per candidate of at most 280 characters, then a last post with the method, the question and the signature.
- **LinkedIn** — the verdict must fit in the first two lines, before the "see more" cut. One idea per line.
- **Hacker News** — plain paragraphs, no emoji. The title states the finding without hype, caps or exclamation marks.
