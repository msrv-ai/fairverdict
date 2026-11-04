"""Distribution checks for the portable plugin archive (stdlib only)."""

import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("package_plugin", ROOT / "scripts/package_plugin.py")
packager = importlib.util.module_from_spec(spec)
spec.loader.exec_module(packager)


class PluginPackageTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.work = Path(self.temporary.name)
        self.source = self.work / "source"
        shutil.copytree(ROOT, self.source, ignore=shutil.ignore_patterns(".git", "dist", "__pycache__", ".idea"))

    def test_archive_is_reproducible_and_contains_only_runtime_files(self):
        (self.source / ".env").write_text("FAKE_TEST_SECRET=never-package-this\n")
        cache = self.source / "skills/fairverdict/scripts/__pycache__"
        cache.mkdir()
        (cache / "judge_score.cpython-313.pyc").write_bytes(b"unwanted cache")
        first = packager.build(self.source, self.work / "first")
        second = packager.build(self.source, self.work / "second")
        self.assertEqual(first.read_bytes(), second.read_bytes())
        with zipfile.ZipFile(first) as archive:
            names = archive.namelist()
            self.assertTrue(all(name.startswith("fairverdict/") for name in names))
            for path in ("plugin.json", ".codex-plugin/plugin.json", ".claude-plugin/plugin.json", "LICENSE",
                         "skills/fairverdict/SKILL.md", "skills/fairverdict/scripts/judge_score.py",
                         "skills/fairverdict/scripts/check_report.py", "skills/fairverdict/references/short-post.md",
                         "skills/fairverdict/references/full-article.md", "assets/icon.png"):
                self.assertIn(f"fairverdict/{path}", names)
            for name in names:
                self.assertNotIn("marketplace", name)
                self.assertNotIn("__pycache__", name)
                self.assertNotIn(".env", name)
                self.assertNotIn("tests/", name)
                self.assertNotIn("README.md", name)

    def test_extracted_scorer_works_outside_repository(self):
        package = packager.build(self.source, self.work / "output")
        extracted = self.work / "extracted"
        with zipfile.ZipFile(package) as archive:
            archive.extractall(extracted)
        scores = self.work / "scores.json"
        scores.write_text(json.dumps({
            "criteria": [{"name": "Correctness", "weight": 70}, {"name": "Effort", "weight": 30}],
            "scores": {"Alpha": {"Correctness": 9, "Effort": 8}, "Beta": {"Correctness": 6, "Effort": 6}}
        }))
        result = subprocess.run([sys.executable, str(extracted / "fairverdict/skills/fairverdict/scripts/judge_score.py"),
                                 str(scores)], cwd=self.work, text=True, capture_output=True, check=True)
        self.assertIn("Alpha", result.stdout)
        self.assertIn("87", result.stdout)

    def test_mismatched_versions_are_rejected(self):
        path = self.source / ".codex-plugin/plugin.json"
        value = json.loads(path.read_text())
        value["version"] = "0.0.0"
        path.write_text(json.dumps(value))
        with self.assertRaisesRegex(ValueError, "name/version differ"):
            packager.build(self.source, self.work / "output")

    def test_linked_component_is_rejected(self):
        target = self.work / "outside.md"
        target.write_text("private content")
        (self.source / "skills/fairverdict/linked.md").symlink_to(target)
        with self.assertRaisesRegex(ValueError, "symlinks cannot be packaged"):
            packager.build(self.source, self.work / "output")


if __name__ == "__main__":
    unittest.main()
