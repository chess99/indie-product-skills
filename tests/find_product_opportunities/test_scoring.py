import unittest

from opportunity_radar.scoring import SCORE_WEIGHTS, score_candidates


def candidate(candidate_id: str, score: float, **extra: object) -> dict[str, object]:
    value: dict[str, object] = {
        "id": candidate_id,
        "name": candidate_id,
        "scores": {dimension: score for dimension in SCORE_WEIGHTS},
    }
    value.update(extra)
    return value


class ScoreCandidatesTests(unittest.TestCase):
    def test_rejects_duplicate_or_unusable_candidate_ids(self) -> None:
        for items in ([candidate("same", 2), candidate("same", 4)], [candidate([], 3)], [candidate(" ", 3)]):
            with self.subTest(items=items), self.assertRaises(ValueError):
                score_candidates({"candidates": items})

    def test_converts_dimension_scores_to_weighted_hundred_point_total(self) -> None:
        document = {
            "schema_version": 1,
            "candidates": [candidate("maximum", 5), candidate("minimum", 0)],
        }

        scored = score_candidates(document)

        self.assertEqual(scored["candidates"][0]["weighted_score"], 100.0)
        self.assertEqual(scored["candidates"][1]["weighted_score"], 0.0)
        self.assertEqual(scored["candidates"][0]["base_rank"], 1)
        self.assertEqual(scored["candidates"][0]["final_rank"], 1)

    def test_uses_declared_weights_and_rounds_to_one_decimal(self) -> None:
        scores = {dimension: 0 for dimension in SCORE_WEIGHTS}
        scores["pain_severity"] = 4
        scores["demand_evidence"] = 3
        document = {
            "schema_version": 1,
            "candidates": [{"id": "weighted", "name": "Weighted", "scores": scores}],
        }

        scored = score_candidates(document)

        self.assertEqual(scored["candidates"][0]["weighted_score"], 25.0)

    def test_rejects_missing_unknown_and_out_of_range_scores(self) -> None:
        missing = candidate("missing", 3)
        del missing["scores"]["retention_potential"]
        unknown = candidate("unknown", 3)
        unknown["scores"]["virality"] = 5
        out_of_range = candidate("range", 3)
        out_of_range["scores"]["pain_severity"] = 6

        for invalid in (missing, unknown, out_of_range):
            with self.subTest(candidate=invalid["id"]):
                with self.assertRaises(ValueError):
                    score_candidates({"schema_version": 1, "candidates": [invalid]})

    def test_applies_explained_rank_override_after_formula_sort(self) -> None:
        document = {
            "schema_version": 1,
            "candidates": [
                candidate("strong", 5),
                candidate(
                    "lower",
                    3,
                    rank_override={
                        "target_rank": 1,
                        "reason": "Stronger first-party payment evidence than the aggregate score captures.",
                    },
                ),
            ],
        }

        scored = score_candidates(document)

        self.assertEqual([item["id"] for item in scored["candidates"]], ["lower", "strong"])
        self.assertEqual(scored["candidates"][0]["base_rank"], 2)
        self.assertEqual(scored["candidates"][0]["final_rank"], 1)

    def test_rejects_rank_override_without_a_reason(self) -> None:
        document = {
            "schema_version": 1,
            "candidates": [
                candidate("a", 5),
                candidate("b", 3, rank_override={"target_rank": 1, "reason": "  "}),
            ],
        }

        with self.assertRaisesRegex(ValueError, "reason"):
            score_candidates(document)


if __name__ == "__main__":
    unittest.main()
