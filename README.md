# FairVerdict

FairVerdict is a portable AI plugin for "which option is best?" questions about frameworks, technologies, libraries, languages, apps, tools, services and products. It works with Codex, ChatGPT environments that support custom plugins, and Claude. Ask a question, name the candidates or let it pick them, and choose a short or full report. You get a scored verdict: a 0–100 score for every option, its strengths and limitations, why the winner wins, and a check of how robust the result is.

Impartial here doesn't mean that every option gets a prize. If the evidence shows a clear winner, FairVerdict says so plainly. What makes the verdict impartial is the procedure it follows every time.

## How it stays impartial

- **The yardstick comes first.** Criteria and weights are fixed before any research or scoring and shown in the report. Changing them later means a full rescore, never a tweak after the fact.
- **Equal effort for every candidate.** Each option gets the same research, with the same queries, including explicit searches for its limitations and known problems. Evidence beats reputation, and independent measurements beat vendor marketing.
- **Anchored scoring.** Scores are given one criterion at a time across all candidates, on a 0–10 scale with fixed meanings and a confidence level for each score.
- **Independent fact-check.** After scoring, fast verifier subagents check the facts each score rests on against what the candidate's public repository publishes, or its official docs for closed-source products. Verifiers never see the scores or the ranking, so they have nothing to confirm.
- **A bias audit before the verdict.** Order effects, name swaps, popularity, familiarity, outdated reputations, invented "balance" and conflicts of interest are checked and corrected.
- **No user history.** The verdict uses only the context you state in the current conversation. FairVerdict doesn't consult memory or past chats to infer your preferences.
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

- **Short** — a compact decision brief: a prominent winner callout, a small comparison table with each candidate's score, strength and limitation, the decisive reasons, what would change the verdict, and a brief fact-check and robustness summary.
- **Full** — a complete article: how the contenders were chosen, the criteria with their weights and what 10/10 means, results with simulation shares, a section per candidate with strengths, limitations, "best for" and "avoid if", why the winner wins, and the robustness and fact check.

Both use clear Markdown hierarchy, restrained emphasis, and a short attribution naming the model that produced the analysis. They retain important uncertainties and conflicts of interest. Reports have no Sources section or configuration filenames; evidence is still researched and checked during the analysis. A proof-link placeholder lets you add a public share link if your environment supports sharing chats.

**The complete report is saved first as a Markdown file**, such as `fairverdict-desktop-mcp-gateways-2026-11-04.md`. The chat reply is only a 3–5-line summary, at most 90 words, with the winner, the main caveat, and a link or download for the file. It does not repeat the report. Local environments save it in the working folder; hosted environments use their supported file-download mechanism. If file tools are unavailable, FairVerdict explains that limitation and provides the report in chat.

See the [short-report design example](examples/claude-code-prompts.md), reformatted from a supplied analysis. Its scores and claims illustrate the layout; they were not re-researched for this example.

## Speed

A short report takes a few minutes and a full one about a quarter of an hour. Research runs in parallel within a fixed budget per candidate, the fact-check verifiers run at the same time on a fast model, and the scoring script ships with the skill instead of being written on the fly.

## What it runs

- **Web search and page fetches** for research, when your environment provides them. Without web access, the verdict says it relies on the model's training data and flags what may be outdated.
- **A small Python scoring script**, bundled with the skill at `skills/fairverdict/scripts/judge_score.py`, when code execution is available. It uses only the Python standard library, reads one local JSON file of scores, prints the results and makes no network calls. It computes the weighted totals, the criteria that separate first from second place, the winner under alternative weightings, and the simulation. Without code execution, the arithmetic is done by hand and the simulation is skipped.
- **Verifier subagents**, when your environment can launch them: one per candidate, on a fast model. For open-source candidates they read what the project publishes about itself — README, architecture and docs files, tech stack, releases — through the GitHub API or repository pages; they don't download or read source code. Closed-source candidates are checked against their official docs. Without subagents, the main session runs the same checks itself and the report says so.
- **Only task output files:** the report and a temporary scoring-input file. FairVerdict doesn't read or write memory, chat history or unrelated project files, and the plugin adds no data collection.

## Install

### Codex: local checkout

From the root of this checkout, register its local marketplace and install the plugin:

```bash
codex plugin marketplace add .
codex plugin add fairverdict@fairverdict
```

In the Codex desktop app, use the **Plugins** selector to select FairVerdict for your chat. Ask a which-is-best question and specify the candidates and report type, or explicitly ask to use FairVerdict.

This installs from files on your machine. It does not publish the plugin or install it into your ChatGPT account. The repository includes `.agents/plugins/marketplace.json` and `.codex-plugin/plugin.json` for this local workflow. See the [official OpenAI plugin build guide](https://developers.openai.com/plugins/build/plugins).

### ChatGPT Work / web: private plugin

ChatGPT Work and web use account-backed plugins; adding a local Codex marketplace does not make a plugin available there. Build the portable package from this checkout:

```bash
python3 scripts/package_plugin.py
```

The result is `dist/fairverdict-1.1.4.zip`. In an environment where Plugin Creator is available, give it this ZIP and ask it to create a private FairVerdict plugin in your account or workspace. Availability and installation depend on that environment's supported plugin tools and your account access. This package is prepared for private import; it has not been published to a public plugin directory.

The ZIP contains a root `plugin.json`, the skill, and its Python scoring script. For the supported conversion and packaging conventions, see the [official Claude-plugin import guide](https://developers.openai.com/plugins/guides/submit-claude-plugin).

### Claude Code

From this checkout:

```bash
claude plugin marketplace add .
claude plugin install fairverdict@fairverdict
```

To install a published repository version instead, use `claude plugin marketplace add msrv-ai/fairverdict` for the first command. That version may differ from your local checkout.

Then ask a which-is-best question, or invoke the skill directly with `/fairverdict:fairverdict`. Claude Code prefixes plugin skills with the plugin name, which is why the name appears twice.

### Claude apps

The skill lives in `skills/fairverdict`, together with its scoring script. If your Claude app supports custom skills, zip that folder and upload it through the app's custom-skill settings, then invoke `/fairverdict` or ask a which-is-best question. This skill-only archive is separate from the portable plugin ZIP above.

## Troubleshooting

- **It asked questions instead of judging.** Name the candidates (or write "pick them yourself") and the report type ("short report") in your first message, and it goes straight to work.
- **There's no Markdown file to open or download.** Update an older installed copy; installed copies do not necessarily refresh when the repository changes. In Claude Code, run `claude plugin marketplace update fairverdict`, then `claude plugin update fairverdict@fairverdict`. In the Claude apps, upload the latest `skills/fairverdict` folder as a custom-skill ZIP in place of the old copy. For other hosts, refresh or reimport the plugin through the installation flow above.
- **A score looks wrong.** Ask why that score was given. FairVerdict re-checks the evidence and changes the score only if the evidence supports it, then recalculates and shows what moved.
- **There's no simulation in the report.** Code execution wasn't available, so the totals were calculated by hand.
- **Recent releases are missing.** Web search wasn't available, so the verdict relies on training data. The report says so.
- **You want different priorities.** Say which weights to change. The whole comparison is rescored from scratch, never adjusted after the fact.
- **You want the other report type.** Ask for it: the same research and scores are reused.
- **The chat reply is short.** The complete report is in the linked Markdown file; the chat contains only the summary.
- **The proof line is a placeholder.** Add a public share link if your environment supports it. FairVerdict never invents a link or publishes the chat for you.
- **It works in Codex but is missing in ChatGPT.** A local marketplace is installed on your machine. Work/web need a separate account-backed private-plugin installation.

## License

MIT, see [LICENSE](LICENSE).
