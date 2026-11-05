# FairVerdict

FairVerdict is a portable AI plugin for "which option is best?" questions about frameworks, technologies, libraries, languages, apps, tools, services and products. It works with Codex, ChatGPT environments that support custom plugins, and Claude. Ask a question, name the candidates or let it pick them, and choose a short post or a full article. You get a scored verdict: a 0–100 score for every option, its strengths and limitations, why the winner wins, and a check of how robust the result is.

Impartial here doesn't mean that every option gets a prize. If the evidence shows a clear winner, FairVerdict says so plainly. What makes the verdict impartial is the procedure it follows every time.

## How it stays impartial

- **It reads the question before anything else.** Before it asks or searches anything, FairVerdict works out what exactly is being compared:
  - the decision behind your question;
  - the kind of option that competes, so it doesn't rank a library against a framework built on it;
  - the shape of the comparison: a ranking, a head-to-head or a should-we-switch decision;
  - what "best" means, and what is in and out of scope.

  The questions it asks, the criteria, the candidates and the report's headline all come from that frame.
- **The yardstick comes first.** Criteria and weights are fixed before any research or scoring and shown in the report. Changing them later means a full rescore, never a tweak after the fact.
- **Equal effort for every candidate.** Each option gets the same research, with the same queries, including explicit searches for its limitations and known problems. Evidence beats reputation, and independent measurements beat vendor marketing.
- **Anchored scoring.** Scores are given one criterion at a time across all candidates, on a 0–10 scale with fixed meanings and a confidence level for each score.
- **Independent fact-check.** After scoring, fast verifier subagents check the facts each score rests on against what the candidate's public repository publishes, or its official docs for closed-source products. Verifiers never see the scores or the ranking, so they have nothing to confirm.
- **A bias audit before any totals.** Order effects, popularity, familiarity, outdated reputations, invented "balance" and conflicts of interest are checked and corrected while the scores are still blind to who is winning. Once the totals are visible, a score changes only for a reason that doesn't depend on them, such as the name-swap check on the two closest candidates, and the report shows the totals before and after.
- **No user history.** The verdict uses only the context you state in the current conversation. FairVerdict doesn't consult memory or past chats to infer your preferences.
- **A robustness check.** The winner is re-tested under alternative weightings and 5,000 simulations with jittered weights and scores. Results that are too close are reported as "too close to call" instead of forcing a winner.

## Example prompts

- "Which framework is fastest for building mobile apps? Take Flutter plus the four most popular alternatives. Write it as a Reddit post."
- "PostgreSQL vs MySQL vs MongoDB for a multi-tenant SaaS backend with heavy reporting. Which is best?"
- "Pick the best static site generator for a documentation site: Docusaurus, Astro Starlight, MkDocs Material or VitePress. I need a full article."
- "Should we move our CI from Jenkins to GitHub Actions? Full article."
- "Shopify, WooCommerce or Wix for a small online store: which is best?"

Ask in any language: FairVerdict talks to you and writes the verdict in the language of your question.

Before it starts, FairVerdict asks whatever your message leaves open, as a multiple-choice question: which candidates to compare (type your own list, mix it with its picks, or let it pick the top ones) and which report you want. The question names what it understood you to be comparing, so you can correct a misreading. It adds at most one more question, only when the answer would change the verdict: an ambiguity in the question ("fast to build with, or fast at runtime?") or a fact about your situation. Nothing is researched or suggested before you answer. When your message settles everything, it states in one line how it read the question and goes straight to work.

## What you get

You choose the report:

- **Short post** — a 300–500-word post modeled on the most-upvoted comparison posts on Reddit, Hacker News and dev.to:
  - a headline that carries the verdict and the scale;
  - an opening that says how many options, criteria and checked facts are behind it;
  - the verdict callout and the winner's catch;
  - a ranking table of at most four columns, with the winner in bold and a number behind every claim;
  - why the winner wins and who should pick what;
  - the method in a few lines after the results, ending with the FairVerdict link; the top carries only the AI attribution, because Reddit readers treat a post that opens with a link to its maker's site as promotion.

  It renders in Reddit's Markdown editor, on GitHub and in any Markdown viewer. To post it on Reddit, put the headline in the title field and paste the rest into the editor's Markdown mode. For X, LinkedIn, Telegram or Hacker News it switches to ranked lines.
- **Full article** — a publishable article with the structure of the most-read "best X" roundups and "X vs Y" comparisons:
  - a headline with the year, a lede with the answer, the verdict callout and quick picks;
  - an at-a-glance table;
  - what was compared and how it was scored, stated before the candidates;
  - one block per candidate with the same fields every time: key facts, strengths, limitations, "best for", "skip it if";
  - the options also considered, scores by criterion, and a "how to choose" guide;
  - the robustness and fact check, an FAQ and a bottom line.

  Two-way comparisons are written round by round, criterion by criterion. Should-we-switch questions lead with "switch" or "stay" and count the cost of moving.

Every pick, "best for" and "what would change it" comes from the computed scores or a verified fact, never from reputation. Both reports keep important uncertainties and conflicts of interest and name the model that produced the analysis. The only emoji are the medal in the verdict callout and ⛔ for a disqualified option. Reports have no Sources section or configuration filenames; evidence is still researched and checked during the analysis. A proof-link placeholder lets you add a public share link if your environment supports sharing chats.

**The complete report is saved first as a Markdown file**, such as `fairverdict-desktop-mcp-gateways-2026-11-04.md`. The chat reply is only a 3–5-line summary, at most 90 words, with the winner, the main caveat, and a link or download for the file. It does not repeat the report. Local environments save it in the working folder; hosted environments use their supported file-download mechanism. If file tools are unavailable, FairVerdict explains that limitation and provides the report in chat.

See both formats from one test run of the skill on 5 November 2026, comparing Flutter and the four most popular alternatives for building mobile apps fast: the [full article](examples/mobile-frameworks-full-article.md) and the [Reddit post](examples/mobile-frameworks-reddit-post.md). The run ended too close to call, so they also show how FairVerdict reports a near-tie. Their facts are as researched in that run and are not kept up to date.

## Speed

A short report takes a few minutes and a full one about a quarter of an hour. Research runs in parallel within a fixed budget per candidate, the fact-check verifiers run at the same time on a fast model, and the scoring script ships with the skill instead of being written on the fly.

## What it runs

- **Web search and page fetches** for research, when your environment provides them. Without web access, the verdict says it relies on the model's training data and flags what may be outdated.
- **A small Python scoring script**, bundled with the skill at `skills/fairverdict/scripts/judge_score.py`, when code execution is available. It uses only the Python standard library, reads one local JSON file of scores, prints the results and makes no network calls. It computes the weighted totals, the criteria that separate first from second place, the winner under alternative weightings, and the simulation. Without code execution, the arithmetic is done by hand and the simulation is skipped.
- **Verifier subagents**, when your environment can launch them: one per candidate, on a fast model. For open-source candidates they read what the project publishes about itself — README, architecture and docs files, tech stack, releases — through the GitHub API or repository pages; they don't download or read source code. Closed-source candidates are checked against their official docs. Without subagents, the main session runs the same checks itself and the report says so.
- **A report checker**, bundled at `skills/fairverdict/scripts/check_report.py`, run on the finished file when code execution is available. It flags problems for the model to fix before you see the report:
  - template fields left unfilled, broken tables and formatting that breaks on Reddit;
  - stray links, a sources section or configuration filenames;
  - a missing verdict callout or proof line;
  - candidates or scores missing from the report.

  Like the scorer, it uses only the standard library, reads only the files it is given and makes no network calls.
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

The result is `dist/fairverdict-1.2.1.zip`. In an environment where Plugin Creator is available, give it this ZIP and ask it to create a private FairVerdict plugin in your account or workspace. Availability and installation depend on that environment's supported plugin tools and your account access. This package is prepared for private import; it has not been published to a public plugin directory.

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
