"""Opportunity scoring with explicit, reviewable ranking overrides."""

from __future__ import annotations

from copy import deepcopy
from numbers import Real
from typing import Any


SCORE_WEIGHTS: dict[str, int] = {
    "pain_severity": 20,
    "demand_evidence": 15,
    "willingness_to_pay": 15,
    "competition_gap": 15,
    "distribution_access": 10,
    "builder_fit": 15,
    "retention_potential": 5,
    "operational_safety": 5,
}


def _weighted_score(candidate: dict[str, Any]) -> float:
    scores = candidate.get("scores")
    if not isinstance(scores, dict) or set(scores) != set(SCORE_WEIGHTS):
        raise ValueError(f"candidate {candidate.get('id', '<unknown>')} has invalid score dimensions")

    total = 0.0
    for dimension, weight in SCORE_WEIGHTS.items():
        value = scores[dimension]
        if isinstance(value, bool) or not isinstance(value, Real) or not 0 <= value <= 5:
            raise ValueError(
                f"candidate {candidate.get('id', '<unknown>')} score {dimension} must be between 0 and 5"
            )
        total += float(value) / 5 * weight
    return round(total, 1)


def score_candidates(document: dict[str, Any]) -> dict[str, Any]:
    """Calculate weighted scores, base ranks, and justified final ranks."""

    result = deepcopy(document)
    candidates = result.get("candidates")
    if not isinstance(candidates, list):
        raise ValueError("candidates must be a list")

    seen_ids: set[str] = set()
    for candidate in candidates:
        if not isinstance(candidate, dict) or not isinstance(candidate.get("id"), str) or not candidate["id"].strip():
            raise ValueError("each candidate must be an object with an id")
        if candidate["id"] in seen_ids:
            raise ValueError("candidate ids must be unique")
        seen_ids.add(candidate["id"])
        candidate["weighted_score"] = _weighted_score(candidate)

    candidates.sort(key=lambda item: -item["weighted_score"])
    for rank, candidate in enumerate(candidates, start=1):
        candidate["base_rank"] = rank

    overrides: list[tuple[int, dict[str, Any]]] = []
    used_targets: set[int] = set()
    for candidate in candidates:
        override = candidate.get("rank_override")
        if override is None:
            continue
        if not isinstance(override, dict):
            raise ValueError("rank_override must be an object")
        target = override.get("target_rank")
        reason = override.get("reason")
        if not isinstance(target, int) or isinstance(target, bool) or not 1 <= target <= len(candidates):
            raise ValueError("rank_override target_rank is outside the candidate range")
        if not isinstance(reason, str) or not reason.strip():
            raise ValueError("rank_override requires a non-empty reason")
        if target in used_targets:
            raise ValueError("rank_override target_rank values must be unique")
        used_targets.add(target)
        overrides.append((target, candidate))

    for target, candidate in sorted(overrides, key=lambda item: item[0]):
        candidates.remove(candidate)
        candidates.insert(target - 1, candidate)

    for rank, candidate in enumerate(candidates, start=1):
        candidate["final_rank"] = rank
    return result
