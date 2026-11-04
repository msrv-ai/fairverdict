# FairVerdict

FairVerdict turns Claude into an impartial judge for "which option is best?" questions about frameworks, technologies, libraries, languages, apps, tools, services and products. Ask a question, name the candidates or let it pick the most widely adopted ones, choose a short or a full report, and get a scored verdict: a 0–100 score for every option, its pros and cons, a summary of why the winner wins, and a check of how robust that result is.

Impartial here doesn't mean that every option gets a prize. If the evidence shows a clear winner, FairVerdict says so plainly. What makes the verdict impartial is the procedure it follows every time.

## How it stays impartial

- **The yardstick comes first.** Criteria and weights are fixed before any research or scoring and shown in the report. Changing them later means a full rescore, never a tweak after the fact.
- **Equal effort for every candidate.** Each option gets the same research, with the same queries, including explicit searches for its limitations and known problems. Evidence beats reputation, and independent measurements beat vendor marketing.
- **Anchored scoring.** Scores are given one criterion at a time across all candidates, on a 0–10 scale with fixed meanings and a confidence level for each score.
- **Independent fact-check.** After scoring, fast verifier subagents check the facts each score rests on against what the candidate's public repository publishes, or its official docs for closed-source products. Verifiers never see the scores or the ranking, so they have nothing to confirm.
- **A bias audit before the verdict.** Order effects, name swaps, popularity, familiarity, outdated reputations, invented "balance" and conflicts of interest are checked and corrected.
- **No user history.** The verdict depends only on what you say in the current conversation. FairVerdict doesn't read memory or past chats, so the same question with the same stated context gets the same answer for anyone.
- **A robustness check.** The winner is re-tested under alternative weightings and 5,000 simulations with jittered weights and scores. Results that are too close are reported as "too close to call" instead of forcing a winner.

## Example prompts

- "Which framework is fastest for building mobile apps? Take Flutter plus the four most popular alternatives. Short report."
- "PostgreSQL vs MySQL vs MongoDB for a multi-tenant SaaS backend with heavy reporting. Which is best?"
- "Pick the best static site generator for a documentation site: Docusaurus, Astro Starlight, MkDocs Material or VitePress. I need a full article."
- "Shopify, WooCommerce or Wix for a small online store: which is best?"

Ask in any language: FairVerdict talks to you and writes the verdict in the language of your question.

Before it starts, FairVerdict asks whatever your message leaves open, as a multiple-choice question: which candidates to compare (type your own list, mix it with its picks, or let it pick the top ones) and which report you want. It adds at most one question about your situation, and only when the answer would change the verdict. Nothing is researched or suggested before you answer.

## What you get

You choose the report:

- **Short** — a Reddit-style post that fits on one screen: the winner and its score, a leaderboard, the score matrix, two pros and two cons per candidate, why the winner wins, what would change the verdict, how it was judged, and the key sources.
- **Full** — a complete article: how the contenders were chosen, the criteria with their weights and what 10/10 means, the results with simulation shares, a section per candidate with pros, cons, "best for" and "avoid if", why the winner wins, robustness and fact check, and sources with dates.

Both start with a line naming the AI model that produced the analysis with FairVerdict. Both end with a line reserved for the proof link: the public link to the chat that produced the report, which you create with Share → Anyone with the link.

## Speed

A short report takes a few minutes and a full one about a quarter of an hour. Research runs in parallel within a fixed budget per candidate, the fact-check verifiers run at the same time on a fast model, and the scoring script ships with the skill instead of being written on the fly.

## What it runs

- **Web search and page fetches** for research, when your Claude environment provides them. Without web access, the verdict says it relies on the model's training data and flags what may be outdated.
- **A small Python scoring script**, bundled with the skill at `skills/judge/scripts/judge_score.py`, when code execution is available. It uses only the Python standard library, reads one local JSON file of scores, prints the results and makes no network calls. It computes the weighted totals, the criteria that separate first from second place, the winner under alternative weightings, and the simulation. Without code execution, the arithmetic is done by hand and the simulation is skipped.
- **Verifier subagents**, when your environment can launch them: one per candidate, on a fast model. For open-source candidates they read what the project publishes about itself — README, architecture and docs files, tech stack, releases — through the GitHub API or repository pages; they don't download or read source code. Closed-source candidates are checked against their official docs. Without subagents, the main session runs the same checks itself and the report says so.
- Nothing else. FairVerdict doesn't read or write memory, chat history or your project files, and it collects no data.

## Install

### Claude Code

```bash
claude plugin marketplace add msrv-ai/fairverdict
claude plugin install fairverdict@fairverdict
```

Then ask a which-is-best question, or invoke the skill directly with `/fairverdict:judge`.

### Claude apps

The skill lives in `skills/judge`, together with its scoring script. You can zip that folder and upload it as a custom skill in Claude's settings under Capabilities → Skills.

## Troubleshooting

- **It asked questions instead of judging.** Name the candidates (or write "pick them yourself") and the report type ("short report") in your first message, and it goes straight to work.
- **A score looks wrong.** Ask why that score was given. FairVerdict re-checks the evidence and changes the score only if the evidence supports it, then recalculates and shows what moved.
- **There's no simulation in the report.** Code execution wasn't available, so the totals were calculated by hand.
- **Recent releases are missing.** Web search wasn't available, so the verdict relies on training data. The report says so.
- **You want different priorities.** Say which weights to change. The whole comparison is rescored from scratch, never adjusted after the fact.
- **You want the other report type.** Ask for it: the same research and scores are reused.
- **The proof line is a placeholder.** That's by design: only you can publish the chat. Share the chat with "Anyone with the link", copy the link and paste it in place of the placeholder.

## License

MIT, see [LICENSE](LICENSE).
