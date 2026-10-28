"""Structural validation for evidence-backed Opportunity Radar runs."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit, urlunsplit

from .scoring import score_candidates


EVIDENCE_FIELDS = {
    "id",
    "source_url",
    "source_title",
    "collected_at",
    "source_type",
    "signal_family",
    "direction",
    "claim",
    "excerpt",
    "reliability",
    "limitations",
}
CANDIDATE_FIELDS = {
    "id",
    "name",
    "target_user",
    "problem",
    "scores",
    "evidence_ids",
    "confidence",
    "status",
}
CITATION_PATTERN = re.compile(r"\[(E\d{3,})\]")
REPORT_PLACEHOLDER_PATTERN = re.compile(
    r"待评分脚本写回|待补充|\b(?:TBD|TODO)\b|RECOMMENDATION\s*/\s*(?:NEEDS-VALIDATION\s*/\s*)?NO-GO",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class ValidationIssue:
    code: str
    message: str


def _issue(issues: list[ValidationIssue], code: str, message: str) -> None:
    issues.append(ValidationIssue(code, message))


def _independent_support_count(rows: list[dict[str, Any]]) -> int:
    """Match distinct support families to distinct declared original sources.

    A source group identifies a shared original (including syndicated articles).
    Without one, identical URLs are deduplicated, ignoring fragments only.
    This checks declared provenance, not the truth of the underlying evidence.
    """
    sources: dict[str, set[str]] = {}
    for row in rows:
        if row.get("direction") != "support" or row.get("reliability") == "low":
            continue
        family = row.get("signal_family")
        url = row.get("source_url")
        if not isinstance(family, str) or not family.strip() or not isinstance(url, str):
            continue
        try:
            parts = urlsplit(url)
            if parts.scheme not in {"http", "https"} or not parts.hostname:
                continue
        except ValueError:
            continue
        group = row.get("source_group") or urlunsplit(
            (parts.scheme.lower(), parts.netloc.lower(), parts.path or "/", parts.query, "")
        )
        if isinstance(group, str):
            sources.setdefault(group, set()).add(family)

    matched: dict[str, str] = {}

    def assign(source: str, visited: set[str]) -> bool:
        for family in sorted(sources[source]):
            if family in visited:
                continue
            visited.add(family)
            if family not in matched or assign(matched[family], visited):
                matched[family] = source
                return True
        return False

    return sum(assign(source, set()) for source in sources)


def _load_evidence(path: Path, issues: list[ValidationIssue]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        _issue(issues, "missing-file", "evidence.jsonl is missing")
        return rows

    for line_number, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as error:
            _issue(issues, "invalid-evidence-json", f"line {line_number}: {error.msg}")
            continue
        if not isinstance(row, dict):
            _issue(issues, "invalid-evidence-record", f"line {line_number} is not an object")
            continue
        missing = sorted(EVIDENCE_FIELDS - set(row))
        if missing:
            _issue(
                issues,
                "missing-evidence-field",
                f"line {line_number} is missing: {', '.join(missing)}",
            )
        if row.get("direction") not in ("support", "counter", "context"):
            _issue(issues, "invalid-evidence-direction", f"line {line_number} has invalid direction")
        if row.get("reliability") not in ("low", "medium", "high"):
            _issue(issues, "invalid-evidence-reliability", f"line {line_number} has invalid reliability")
        for field in EVIDENCE_FIELDS:
            if field in row and (not isinstance(row[field], str) or not row[field].strip()):
                _issue(issues, "invalid-evidence-field", f"line {line_number}: {field} must be non-empty text")
        if "source_group" in row and (not isinstance(row["source_group"], str) or not row["source_group"].strip()):
            _issue(issues, "invalid-source-group", f"line {line_number} has invalid source_group")
        rows.append(row)
    return rows


def _load_json(path: Path, issues: list[ValidationIssue]) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        _issue(issues, "missing-file", f"{path.name} is missing")
        return {}
    except json.JSONDecodeError as error:
        _issue(issues, "invalid-json", f"{path.name}: {error.msg}")
        return {}
    if not isinstance(value, dict):
        _issue(issues, "invalid-json-root", f"{path.name} must contain an object")
        return {}
    return value


def validate_run(run_path: Path) -> list[ValidationIssue]:
    """Return all structural and traceability issues in a saved research run."""

    root = Path(run_path)
    issues: list[ValidationIssue] = []
    _load_json(root / "brief.json", issues)
    rows = _load_evidence(root / "evidence.jsonl", issues)
    document = _load_json(root / "candidates.json", issues)
    try:
        report = (root / "report.md").read_text(encoding="utf-8")
    except FileNotFoundError:
        _issue(issues, "missing-file", "report.md is missing")
        report = ""

    placeholder = REPORT_PLACEHOLDER_PATTERN.search(report)
    if placeholder:
        _issue(
            issues,
            "unresolved-report-placeholder",
            f"report contains unresolved placeholder: {placeholder.group(0)}",
        )

    evidence_by_id: dict[str, dict[str, Any]] = {}
    for row in rows:
        evidence_id = row.get("id")
        if not isinstance(evidence_id, str) or not re.fullmatch(r"E\d{3,}", evidence_id):
            _issue(issues, "invalid-evidence-id", f"invalid evidence id: {evidence_id!r}")
            continue
        if evidence_id in evidence_by_id:
            _issue(issues, "duplicate-evidence-id", f"duplicate evidence id: {evidence_id}")
        else:
            evidence_by_id[evidence_id] = row

    candidates = document.get("candidates", [])
    if not isinstance(candidates, list):
        _issue(issues, "invalid-candidates", "candidates must be a list")
        candidates = []

    try:
        expected_document = score_candidates(document)
    except ValueError as error:
        _issue(issues, "invalid-candidate-score", str(error))
        expected_document = {"candidates": []}
    expected_by_id = {candidate["id"]: candidate for candidate in expected_document.get("candidates", [])}

    finalists: list[dict[str, Any]] = []
    recommended: list[dict[str, Any]] = []
    for candidate in candidates:
        if not isinstance(candidate, dict):
            _issue(issues, "invalid-candidate", "candidate must be an object")
            continue
        candidate_id = candidate.get("id", "<unknown>")
        expected = expected_by_id.get(candidate_id) if isinstance(candidate_id, str) else None
        if expected is not None and any(
            candidate.get(field) != expected.get(field)
            for field in ("weighted_score", "base_rank", "final_rank")
        ):
            _issue(
                issues,
                "stale-candidate-score",
                f"candidate {candidate_id} must be processed by the score command",
            )
        missing = sorted(CANDIDATE_FIELDS - set(candidate))
        if missing:
            _issue(
                issues,
                "missing-candidate-field",
                f"candidate {candidate_id} is missing: {', '.join(missing)}",
            )
        evidence_ids = candidate.get("evidence_ids", [])
        if not isinstance(evidence_ids, list):
            _issue(
                issues,
                "invalid-evidence-references",
                f"candidate {candidate_id} evidence_ids must be a list",
            )
            evidence_ids = []
        referenced_rows = []
        for evidence_id in evidence_ids:
            if not isinstance(evidence_id, str):
                _issue(issues, "invalid-evidence-references", f"candidate {candidate_id} has a non-string evidence id")
                continue
            row = evidence_by_id.get(evidence_id)
            if row is None:
                _issue(
                    issues,
                    "broken-candidate-reference",
                    f"candidate {candidate_id} references missing {evidence_id}",
                )
            else:
                referenced_rows.append(row)

        if candidate.get("status") == "finalist":
            finalists.append(candidate)
            support_count = _independent_support_count(referenced_rows)
            if support_count < 3:
                _issue(
                    issues,
                    "finalist-signal-diversity",
                    f"finalist {candidate_id} has {support_count} independent support families",
                )
            checks = candidate.get("counterevidence_checks")
            if not isinstance(checks, list) or not checks or any(
                not isinstance(check, dict) or any(
                    not isinstance(check.get(field), str) or not check[field].strip()
                    for field in ("source_url", "checked_at", "finding")
                ) for check in checks
            ):
                _issue(
                    issues,
                    "missing-counterevidence-check",
                    f"finalist {candidate_id} has no recorded counterevidence check",
                )
            if candidate.get("confidence") == "high" and any(
                row.get("direction") == "counter" for row in referenced_rows
            ):
                _issue(
                    issues,
                    "confidence-conflict",
                    f"finalist {candidate_id} cannot be high confidence with counter evidence",
                )
            if candidate.get("confidence") not in ("medium", "high"):
                _issue(issues, "finalist-confidence", f"finalist {candidate_id} needs medium or high confidence")
        if candidate.get("recommended") is True:
            recommended.append(candidate)
            if candidate.get("status") != "finalist":
                _issue(issues, "recommendation-status", f"recommended candidate {candidate_id} must be a finalist")

    report_ids = set(CITATION_PATTERN.findall(report))
    for evidence_id in report_ids:
        if evidence_id not in evidence_by_id:
            _issue(issues, "broken-report-reference", f"report references missing {evidence_id}")
    for candidate in finalists:
        ids = candidate.get("evidence_ids", [])
        for evidence_id in ids if isinstance(ids, list) else []:
            if isinstance(evidence_id, str) and evidence_id in evidence_by_id and evidence_id not in report_ids:
                _issue(
                    issues,
                    "missing-report-citation",
                    f"report does not cite {evidence_id} used by finalist {candidate.get('id')}",
                )

    decision = document.get("decision")
    if decision == "recommendation":
        if not 1 <= len(finalists) <= 3:
            _issue(
                issues,
                "finalist-count",
                f"recommendation requires 1–3 finalists, found {len(finalists)}",
            )
        if len(recommended) != 1:
            _issue(
                issues,
                "recommendation-count",
                f"recommendation requires 1 primary choice, found {len(recommended)}",
            )
    elif decision in ("no-go", "needs-validation"):
        if recommended:
            _issue(issues, "no-go-recommendation", f"{decision} runs cannot contain a primary recommendation")
        if finalists:
            _issue(issues, "non-recommendation-finalists", f"{decision} runs use pending/rejected candidates, not finalists")
        if decision.upper() not in report.upper():
            _issue(issues, "missing-decision-marker", f"report must state {decision.upper()}")
    else:
        _issue(issues, "invalid-decision", "decision must be recommendation, needs-validation or no-go")

    return issues
