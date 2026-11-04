# FairVerdict · Which Claude Code prompt helps most?

*04 Nov 2026 · AI analysis by Claude Opus 5.5 with [FairVerdict](https://msrv.dev/fairverdict/) · Default effort*

**The goal:** better correctness and less rework in everyday coding. Session prompts and standing instructions share one ranking.

**Disclosure:** Claude is evaluating its own maker’s product: Anthropic’s Claude Code.

> ## 🥇 Verify before done
>
> **88 / 100** · Clear winner · **+12 points** ahead of #2
>
> Make completion depend on a check Claude can run. Direct evidence of success addresses a recurring failure: declaring an untested fix finished.
>
> **Copy this prompt**
>
> “When you're done, run the tests/build and show me the exact command and its output. Don't tell me it works, show me.”

**Catch:** a useful check must exist. Green tests can mislead if they were weakened—pair this with #4.

### The shortlist

| Rank | Approach | Score /100 | Payoff → trade-off |
|:---:|---|---:|---|
| 2 | **Plan before coding** | **76** | Approve the approach before edits; catch wrong assumptions early. Adds friction to small tasks; dropped from the cited Nov 2026 best-practices page. |
| 3 | **Surgical changes** | **72** | Keep edits focused and diffs reviewable. Following standing instructions is not guaranteed; excessive restraint can block useful abstractions. |
| 4 | **Root cause, no shortcuts** | **71*** | Fix the cause; never weaken tests or silence errors. Advisory only; **0/3 supporting facts confirmed from primary sources**. |
| 5 | **Fresh-context review** | **69** | A separate reviewer checks the diff against the spec. Can catch blind spots, but false findings waste tokens and encourage over-engineering. |

*\* Low evidence confidence. “Not found” does not mean “disproved.”*

### Why this verdict holds

**Verify** beats **Plan** on quality impact, breadth, efficiency and durability. Plan leads on control and ease.

**94%** of simulations won · **No tested single reweighting** changes #1 · **Only 3 points** separate #3–5

For loosely specified new features, excluding breadth brings **Interview me first** into a tie for #5.

---

**Evidence check** · 8 candidates from official guidance, community advice and recurring issues; setup-only and superseded context-saving advice excluded · 24 facts checked by 8 independent verifiers · **16 confirmed / 0 contradicted / 8 not found**. The rubric was fixed before scoring; an outdated source was caught and 3 candidates were adjusted.

[Proof: public share link not yet provided]
