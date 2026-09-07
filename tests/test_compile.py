import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class CompileScriptTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.project = Path(self.tmp.name)
        (self.project / "docs").mkdir()

    def tearDown(self):
        self.tmp.cleanup()

    def run_compile(self, *args):
        return subprocess.run(
            [sys.executable, str(ROOT / "scripts/loom/compile.py"), *args],
            cwd=self.project, text=True, capture_output=True)

    def write_config(self, text):
        (self.project / "docs/loom.yaml").write_text(text, encoding="utf-8")

    def paths(self):
        return sorted(path.relative_to(self.project).as_posix()
                      for path in self.project.rglob("*"))

    def test_empty_engine_values_with_trailing_comments_fail_closed(self):
        self.write_config(
            "engine:\n"
            "  name: \"\"            # spec-kit | kiro | openspec | bmad | claude-code | ...\n"
            "  constitution: \"\"    # e.g. .specify/memory/constitution.md | .kiro/steering/product.md | AGENTS.md\n"
            "  spec_dir: \"\"        # e.g. .specify/specs — per-epic seed specs land here\n")
        before = self.paths()

        for args in ((), ("--check",)):
            result = self.run_compile(*args)
            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertIn("ERROR: no engine configured", result.stderr)
            self.assertEqual(self.paths(), before)

    def test_hash_inside_quoted_engine_paths_is_preserved(self):
        epic = self.project / "docs/roadmap/epics/epic-hash/epic.md"
        epic.parent.mkdir(parents=True)
        epic.write_text(
            "---\nid: epic-hash\nstatus: approved\n---\n# Hash paths\n",
            encoding="utf-8")
        self.write_config(
            "engine:\n"
            "  name: \"fixture#engine\" # trailing comment\n"
            "  constitution: \"compiled/#constitution.md\" # trailing comment\n"
            "  spec_dir: 'compiled/#specs' # trailing comment\n")

        result = self.run_compile("--epic", "epic-hash")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.project / "compiled/#constitution.md").is_file())
        self.assertTrue((self.project / "compiled/#specs/epic-hash.md").is_file())
        compiled_files = sorted(
            path.relative_to(self.project).as_posix()
            for path in (self.project / "compiled").rglob("*")
            if path.is_file())
        self.assertEqual(compiled_files, [
            "compiled/#constitution.md",
            "compiled/#specs/epic-hash.md",
        ])

        check = self.run_compile("--check", "--epic", "epic-hash")
        self.assertEqual(check.returncode, 0, check.stderr)
        self.assertIn("GATE PASSED", check.stdout)


if __name__ == "__main__":
    unittest.main()
