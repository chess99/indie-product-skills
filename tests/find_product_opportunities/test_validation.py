import json
import tempfile
import unittest
from pathlib import Path

from opportunity_radar.scoring import SCORE_WEIGHTS, score_candidates
from opportunity_radar.validation import validate_run


def evidence(evidence_id: str, family: str, *, direction: str = "support") -> dict[str, str]:
    return {
        "id": evidence_id,
        "source_url": f"https://example.com/{evidence_id.lower()}",
        "source_title": f"Source {evidence_id}",
        "collected_at": "2026-07-17T09:00:00+00:00",
        "source_type": "public-web",
        "signal_family": family,
        "direction": direction,
        "claim": f"Claim {evidence_id}",
        "excerpt": f"Excerpt {evidence_id}",
        "reliability": "medium",
        "limitations": "Directional public evidence only.",
    }


def finalist(candidate_id: str, evidence_ids: list[str], *, recommended: bool = False) -> dict[str, object]:
    return {
        "id": candidate_id,
        "name": candidate_id,
        "target_user": "Independent developers",
        "problem": "A recurring and costly workflow problem",
        "scores": {dimension: 3 for dimension in SCORE_WEIGHTS},
        "evidence_ids": evidence_ids,
        "counterevidence_checks": [
            {
                "source_url": "https://example.com/counter-check",
                "checked_at": "2026-07-17T09:30:00+00:00",
                "finding": "No fatal counter-signal found; switching costs remain a risk.",
            }
        ],
        "confidence": "medium",
        "status": "finalist",
        "recommended": recommended,
    }


class ValidateRunTests(unittest.TestCase):
    def write_run(
        self,
        root: Path,
        evidence_rows: list[dict[str, str]],
        candidates: dict[str, object],
        report: str,
    ) -> None:
        (root / "brief.json").write_text(
            json.dumps({"schema_version": 1, "goal": "Find a product opportunity"}),
            encoding="utf-8",
        )
        (root / "evidence.jsonl").write_text(
            "".join(json.dumps(row) + "\n" for row in evidence_rows), encoding="utf-8"
        )
        (root / "candidates.json").write_text(json.dumps(candidates), encoding="utf-8")
        (root / "report.md").write_text(report, encoding="utf-8")

    def test_accepts_three_traceable_finalists_and_one_recommendation(self) -> None:
        rows = [
            evidence("E001", "search-trend"),
            evidence("E002", "community-pain"),
            evidence("E003", "commercial-proof"),
            evidence("E004", "search-trend"),
            evidence("E005", "community-pain"),
            evidence("E006", "competitor-gap"),
            evidence("E007", "search-trend"),
            evidence("E008", "commercial-proof"),
            evidence("E009", "distribution"),
        ]
        document = score_candidates(
            {
                "schema_version": 1,
                "decision": "recommendation",
                "candidates": [
                    finalist("one", ["E001", "E002", "E003"], recommended=True),
                    finalist("two", ["E004", "E005", "E006"]),
                    finalist("three", ["E007", "E008", "E009"]),
                ],
            }
        )
        report = "# Report\n" + " ".join(f"[E{i:03d}]" for i in range(1, 10))

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.write_run(root, rows, document, report)

            self.assertEqual(validate_run(root), [])

    def test_reports_duplicate_evidence_and_broken_references(self) -> None:
        rows = [evidence("E001", "search-trend"), evidence("E001", "community-pain")]
        document = {
            "schema_version": 1,
            "decision": "recommendation",
            "candidates": [finalist("one", ["E404"], recommended=True)],
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.write_run(root, rows, document, "# Report\n[E999]")

            codes = {issue.code for issue in validate_run(root)}

        self.assertIn("duplicate-evidence-id", codes)
        self.assertIn("broken-candidate-reference", codes)
        self.assertIn("broken-report-reference", codes)

    def test_rejects_finalist_without_signal_diversity_or_counter_check(self) -> None:
        rows = [evidence("E001", "search-trend"), evidence("E002", "search-trend")]
        item = finalist("one", ["E001", "E002"], recommended=True)
        item["counterevidence_checks"] = []
        document = {"schema_version": 1, "decision": "recommendation", "candidates": [item]}

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.write_run(root, rows, document, "# Report\n[E001] [E002]")

            codes = {issue.code for issue in validate_run(root)}

        self.assertIn("finalist-signal-diversity", codes)
        self.assertIn("missing-counterevidence-check", codes)
        self.assertNotIn("finalist-count", codes)

    def test_accepts_one_or_two_supported_finalists(self) -> None:
        rows = [evidence("E001", "search-trend"), evidence("E002", "community-pain"), evidence("E003", "commercial-proof")]
        for count in (1, 2):
            with self.subTest(count=count), tempfile.TemporaryDirectory() as temp_dir:
                root = Path(temp_dir)
                candidates = [finalist(str(i), ["E001", "E002", "E003"], recommended=i == 0) for i in range(count)]
                self.write_run(root, rows, score_candidates({"decision": "recommendation", "candidates": candidates}), "[E001] [E002] [E003]")
                self.assertEqual(validate_run(root), [])

    def test_support_gate_excludes_context_counter_low_quality_and_same_origin(self) -> None:
        for scenario in ("context", "counter", "low", "same-url", "syndicated"):
            rows = [evidence("E001", "search-trend"), evidence("E002", "community-pain"), evidence("E003", "commercial-proof")]
            if scenario in ("context", "counter"):
                rows[2]["direction"] = scenario
            elif scenario == "low":
                rows[2]["reliability"] = "low"
            elif scenario == "same-url":
                rows[2]["source_url"] = rows[0]["source_url"] + "#section"
            else:
                rows[0]["source_group"] = rows[2]["source_group"] = "one-original-study"
            with self.subTest(scenario=scenario), tempfile.TemporaryDirectory() as temp_dir:
                root = Path(temp_dir)
                doc = score_candidates({"decision": "recommendation", "candidates": [finalist("one", ["E001", "E002", "E003"], recommended=True)]})
                self.write_run(root, rows, doc, "[E001] [E002] [E003]")
                self.assertIn("finalist-signal-diversity", {i.code for i in validate_run(root)})

    def test_needs_validation_is_distinct_from_recommendation_and_no_go(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.write_run(root, [], {"decision": "needs-validation", "candidates": []}, "NEEDS-VALIDATION: source unavailable; test buyer demand next.")
            self.assertEqual(validate_run(root), [])

    def test_rejects_hidden_recommendations_in_non_finalists(self) -> None:
        item = finalist("one", [], recommended=True)
        item["status"] = "pending"
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.write_run(root, [], score_candidates({"decision": "needs-validation", "candidates": [item]}), "NEEDS-VALIDATION")
            codes = {i.code for i in validate_run(root)}
            self.assertIn("recommendation-status", codes)
            self.assertIn("no-go-recommendation", codes)

    def test_malformed_evidence_references_produce_issues_without_crashing(self) -> None:
        for ids in ([{}], None):
            item = finalist("one", ids, recommended=True)
            with self.subTest(ids=ids), tempfile.TemporaryDirectory() as temp_dir:
                root = Path(temp_dir)
                self.write_run(root, [], score_candidates({"decision": "recommendation", "candidates": [item]}), "Report")
                self.assertIn("invalid-evidence-references", {i.code for i in validate_run(root)})

    def test_recommendation_requires_at_least_one_and_at_most_three_finalists(self) -> None:
        for count in (0, 4):
            with self.subTest(count=count), tempfile.TemporaryDirectory() as temp_dir:
                root = Path(temp_dir)
                items = [finalist(str(i), [], recommended=i == 0) for i in range(count)]
                self.write_run(root, [], score_candidates({"decision": "recommendation", "candidates": items}), "Report")
                self.assertIn("finalist-count", {i.code for i in validate_run(root)})

    def test_accepts_explicit_no_go_without_fabricating_finalists(self) -> None:
        document = {"schema_version": 1, "decision": "no-go", "candidates": []}

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.write_run(root, [], document, "# Report\n\n结论：NO-GO\n")

            self.assertEqual(validate_run(root), [])

    def test_rejects_unresolved_report_placeholder(self) -> None:
        document = {"schema_version": 1, "decision": "no-go", "candidates": []}

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.write_run(root, [], document, "# Report\n\n结论：NO-GO\n\n得分：待评分脚本写回\n")

            codes = {issue.code for issue in validate_run(root)}

        self.assertIn("unresolved-report-placeholder", codes)

    def test_high_confidence_is_invalid_when_counter_evidence_conflicts(self) -> None:
        rows = [
            evidence("E001", "search-trend"),
            evidence("E002", "community-pain"),
            evidence("E003", "commercial-proof", direction="counter"),
        ]
        item = finalist("one", ["E001", "E002", "E003"], recommended=True)
        item["confidence"] = "high"
        document = {"schema_version": 1, "decision": "recommendation", "candidates": [item]}

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.write_run(root, rows, document, "# Report\n[E001] [E002] [E003]")

            codes = {issue.code for issue in validate_run(root)}

        self.assertIn("confidence-conflict", codes)

    def test_rejects_invalid_or_unscored_candidate_data(self) -> None:
        rows = [
            evidence("E001", "search-trend"),
            evidence("E002", "community-pain"),
            evidence("E003", "commercial-proof"),
        ]
        item = finalist("one", ["E001", "E002", "E003"], recommended=True)
        del item["scores"]["operational_safety"]
        document = {"schema_version": 1, "decision": "recommendation", "candidates": [item]}

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.write_run(root, rows, document, "# Report\n[E001] [E002] [E003]")

            codes = {issue.code for issue in validate_run(root)}

        self.assertIn("invalid-candidate-score", codes)


if __name__ == "__main__":
    unittest.main()
