"""Checks for the bundled report checker (stdlib only)."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "skills/fairverdict/scripts/check_report.py"

GOOD_SHORT = """# Alpha beats Beta for small teams: 87 vs 60

*04 Nov 2026 · AI analysis by Example Model with [FairVerdict](https://msrv.dev/fairverdict/)*

**TL;DR:** Alpha wins on correctness.

> ### 🥇 Alpha
>
> **87 / 100** · Clear · **+27 points** ahead of #2

### The ranking

| # | Option | Score | Payoff → trade-off |
|:---:|---|:---:|---|
| 1 | **Alpha** | **87** | **Correct by default → slower to set up** |
| 2 | Beta | 60 | Quick experiments → more bugs |

**What would change it:** nothing in the tested weightings.

[Proof: public share link not yet provided]
"""


def run(text, *options, scores=None):
    with tempfile.TemporaryDirectory() as temporary:
        report = Path(temporary) / "report.md"
        report.write_text(text, encoding="utf-8")
        command = [sys.executable, str(CHECKER), str(report), *options]
        if scores is not None:
            path = Path(temporary) / "scores.json"
            path.write_text(json.dumps(scores), encoding="utf-8")
            command += ["--scores", str(path)]
        return subprocess.run(command, text=True, capture_output=True)


SCORES = {
    "criteria": [{"name": "Correctness", "weight": 70}, {"name": "Effort", "weight": 30}],
    "scores": {"Alpha": {"Correctness": 9, "Effort": 8}, "Beta": {"Correctness": 6, "Effort": 6}},
}


class CheckReportTests(unittest.TestCase):
    def test_good_report_passes(self):
        result = run(GOOD_SHORT, "--type", "short", scores=SCORES)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("0 error(s), 0 warning(s)", result.stdout)

    def test_leftover_template_field_fails(self):
        result = run(GOOD_SHORT.replace("Quick experiments", "<payoff>"), "--type", "short")
        self.assertEqual(result.returncode, 1)
        self.assertIn("unresolved template field", result.stdout)

    def test_code_is_not_a_template_field(self):
        text = GOOD_SHORT.replace("Alpha wins on correctness.", "Alpha wins; it types `Array<string>` well.")
        self.assertEqual(run(text, "--type", "short").returncode, 0)

    def test_source_list_and_links_fail(self):
        text = GOOD_SHORT.replace("[Proof:", "## Sources\n\n- [Docs](https://example.com/docs)\n\n[Proof:")
        result = run(text, "--type", "short")
        self.assertEqual(result.returncode, 1)
        self.assertIn("sources section", result.stdout)
        self.assertIn("https://example.com/docs", result.stdout)

    def test_proof_line_may_hold_a_supplied_share_link(self):
        text = GOOD_SHORT.replace("[Proof: public share link not yet provided]",
                                  "[Proof: shared chat](https://example.com/share/abc)")
        self.assertEqual(run(text, "--type", "short").returncode, 0)

    def test_missing_proof_line_fails(self):
        result = run(GOOD_SHORT.replace("[Proof: public share link not yet provided]\n", ""), "--type", "short")
        self.assertEqual(result.returncode, 1)
        self.assertIn("proof placeholder", result.stdout)

    def test_configuration_file_name_fails(self):
        text = GOOD_SHORT.replace("Alpha wins on correctness.", "Alpha wins; add it to CLAUDE.md.")
        result = run(text, "--type", "short")
        self.assertEqual(result.returncode, 1)
        self.assertIn("CLAUDE.md", result.stdout)

    def test_broken_table_fails(self):
        text = GOOD_SHORT.replace("| 2 | Beta | 60 | Quick experiments → more bugs |", "| 2 | Beta | 60 |")
        result = run(text, "--type", "short")
        self.assertEqual(result.returncode, 1)
        self.assertIn("3 cells, its header has 4", result.stdout)

    def test_list_glued_to_paragraph_warns(self):
        text = GOOD_SHORT.replace("**What would change it:**", "**Strengths:**\n- fast\n\n**What would change it:**")
        result = run(text, "--type", "short")
        self.assertEqual(result.returncode, 0)
        self.assertIn("blank line before this list", result.stdout)

    def test_post_formatting_that_breaks_on_reddit_warns(self):
        text = GOOD_SHORT.replace("### The ranking", "## The ranking 🚀").replace(
            "| # | Option | Score | Payoff → trade-off |\n|:---:|---|:---:|---|",
            "| # | Option | Score | Payoff | Trade-off |\n|:---:|---|:---:|---|---|").replace(
            "| **Correct by default → slower to set up** |", "| **Correct by default** | slower to set up |").replace(
            "| Quick experiments → more bugs |", "| Quick experiments | more bugs |")
        result = run(text, "--type", "short")
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("use ### for headings", result.stdout)
        self.assertIn("decorative emoji 🚀", result.stdout)
        self.assertIn("5 columns", result.stdout)
        self.assertNotIn("decorative emoji 🥇", result.stdout)

    def test_wrong_score_and_missing_section_warn(self):
        result = run(GOOD_SHORT.replace("**87 / 100**", "**88 / 100**").replace("**87**", "**88**")
                     .replace(": 87 vs 60", ": 88 vs 60"), "--type", "full", scores=SCORES)
        self.assertEqual(result.returncode, 0)
        self.assertIn("'Alpha' scored 87/100", result.stdout)
        self.assertIn("no section heading for 'Beta'", result.stdout)
        self.assertIn("thin for a full report", result.stdout)


if __name__ == "__main__":
    unittest.main()
