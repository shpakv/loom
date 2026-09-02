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
        (self.project / "custom/changes").mkdir(parents=True)
        (self.project / "docs/loom.yaml").write_text(
            "version: 0.11\nscripts_version: 0.14.0\n"
            "paths:\n  docs: custom/docs\n  changes: custom/changes\n  product: custom/product\n  roadmap: custom/roadmap\n  epics: custom/roadmap/epics\n"
            "statuses:\n  documents: [draft, in-review, approved, superseded]\n"
            "  changes: [captured, triaged, accepted, in-progress, applied, rejected, superseded]\n",
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

    def write_adr(self, name="ADR-use-postgres-for-billing", **fields):
        defaults = {
            "id": "ADR-use-postgres-for-billing",
            "status": "accepted", "reversibility": "one-way",
            "decision_mode": "recommend", "evidence_level": "reasoned",
            "confidence": "low", "authority": "product-owner",
            "risk_accepted_by": "product-owner",
            "revisit_when": "load exceeds 1000 requests per second",
            "decided": "2026-09-02", "updated": "2026-09-02",
        }
        defaults.update(fields)
        front = "\n".join(f"{key}: {value}" for key, value in defaults.items())
        body = """# ADR: Use Postgres for billing

Status: accepted · reversibility: one-way · evidence: reasoned · confidence: low

## Context
The choice is framed by DRV-billing-volume and QS-billing-reliability.

## Recommendation
Use Postgres because the operational fit is strongest.

## Evidence
Question, method, observations, interpretation, limitations and provenance are
recorded here; no experiment code is stored in Loom.

## Unknowns
Peak behavior remains uncertain.

## Residual risk
The choice may need migration if load grows faster than expected.

## Research decision
The project accepts this risk now because the decision is time-sensitive.

## Decision
Accepted by the authority.
"""
        (self.project / "custom/docs" / f"{name}.md").write_text(
            f"---\n{front}\n---\n{body}", encoding="utf-8")

    def test_weak_one_way_decision_can_pass_with_explicit_risk(self):
        self.write_adr()
        result = self.run_script("adr_scan.py", "--gate", "custom/docs")
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_weak_one_way_decision_fails_when_risk_is_hidden(self):
        self.write_adr(risk_accepted_by="null", revisit_when="[]")
        result = self.run_script("adr_scan.py", "--gate", "custom/docs")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("weak evidence", result.stderr)

    def test_all_decision_modes_and_evidence_levels_are_supported(self):
        modes = ("delegated", "recommend", "confirm", "record-only")
        levels = ("none", "reasoned", "reported", "observed", "measured")
        for index, mode in enumerate(modes):
            for level in levels:
                name = f"ADR-use-billing-option-{index}-{level}"
                self.write_adr(
                    name=name, id=name, decision_mode=mode,
                    evidence_level=level, confidence="medium",
                    policy_override="true" if mode == "delegated" else "null",
                    override_reason="project policy permits delegation" if mode == "delegated" else "null")
        result = self.run_script("adr_scan.py", "--gate", "custom/docs")
        self.assertEqual(result.returncode, 0, result.stderr)

    def write_change(self, status="captured", extra=""):
        (self.project / "custom/changes/CHG-retention-window.md").write_text(
            "---\n"
            "id: CHG-retention-window\n"
            f"status: {status}\n"
            "owner: human\nsource: customer\nreceived: 2026-09-02\n"
            "confidence: confirmed\nclassification: customer-change\n"
            "route: requirements\naffects: [BR-retention-window]\n"
            "decision: approved\ndecided_by: product-owner\ndecided_at: 2026-09-02\n"
            "applied_documents: []\nrevalidated_documents: []\n"
            "superseded_by: null\nupdated: 2026-09-02\n---\n"
            "# Change: Retention window\n\n## Original input\n\nCustomer changed the retention window.\n"
            f"{extra}", encoding="utf-8")

    def test_change_scan_accepts_captured_record_and_rejects_incomplete_applied(self):
        self.write_change()
        result = self.run_script("change_scan.py", "--gate")
        self.assertEqual(result.returncode, 0, result.stderr)

        self.write_change("applied")
        result = self.run_script("change_scan.py", "--gate")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("applied status requires non-empty", result.stdout)

    def test_impact_scan_reports_direct_blocked_and_transitive_review_consumers(self):
        (self.project / "custom/docs/RULES.md").write_text(
            "---\nid: rules\nstatus: approved\n---\n"
            "# Rules\n\n| BR-retention-window | Retention is bounded | product owner |\n",
            encoding="utf-8")
        (self.project / "custom/docs/epic-retention.md").write_text(
            "---\nid: epic-retention\nstatus: approved\n---\n"
            "# Retention\n\nThe epic follows BR-retention-window.\n",
            encoding="utf-8")
        (self.project / "custom/docs/TASK-retention-review.md").write_text(
            "---\nid: TASK-retention-review\nstatus: draft\n---\n"
            "# Task\n\nThis task follows epic-retention.\n",
            encoding="utf-8")
        result = self.run_script("impact_scan.py", "--id", "BR-retention-window", "--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(len(report["direct"]), 1)
        self.assertEqual(report["direct"][0]["state"], "blocked")
        self.assertEqual(len(report["transitive"]), 1)
        self.assertEqual(report["transitive"][0]["state"], "needs-review")


if __name__ == "__main__":
    unittest.main()
