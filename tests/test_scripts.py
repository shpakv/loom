import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ScriptFixtures(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.project = Path(self.tmp.name)
        (self.project / "docs/roadmap/epics").mkdir(parents=True)
        (self.project / "custom/product").mkdir(parents=True)
        (self.project / "docs/loom.yaml").write_text(
            "version: 0.11\nscripts_version: 0.14.0\n"
            "paths:\n  docs: custom/docs\n  product: custom/product\n  roadmap: custom/roadmap\n  epics: custom/roadmap/epics\n"
            "statuses:\n  documents: [draft, in-review, approved, superseded]\n",
            encoding="utf-8")
        (self.project / "custom/docs").mkdir()
        (self.project / "custom/roadmap/epics").mkdir(parents=True)

    def tearDown(self):
        self.tmp.cleanup()

    def run_script(self, name, *args):
        return subprocess.run(
            [sys.executable, str(ROOT / "scripts/loom" / name), *args],
            cwd=self.project, text=True, capture_output=True)

    def test_index_uses_configured_docs_and_print_does_not_write(self):
        (self.project / "custom/docs/VISION.md").write_text(
            "---\nid: vision\nstatus: draft\nupdated: today\n---\n# Vision\n",
            encoding="utf-8")
        result = self.run_script("index_gen.py", "--print")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("custom/docs/VISION.md", result.stdout)
        self.assertFalse((self.project / "custom/docs/INDEX.md").exists())

    def test_missing_target_fails_closed(self):
        result = self.run_script("oq_scan.py", "missing")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("does not exist", result.stderr)

    def test_roadmap_rejects_multiple_approved_epics(self):
        for slug in ("epic-one", "epic-two"):
            path = self.project / "custom/roadmap/epics" / slug
            path.mkdir()
            (path / "epic.md").write_text(
                f"---\nid: {slug}\nstatus: approved\n---\n# {slug}\n",
                encoding="utf-8")
        result = self.run_script("roadmap_gen.py", "--gate")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("more than one approved epic", result.stderr)


if __name__ == "__main__":
    unittest.main()
