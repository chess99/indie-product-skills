#!/usr/bin/env python3
"""Local workspace helpers for the link-ops skill."""

from __future__ import annotations

import argparse
import csv
import json
import math
import re
import sys
from pathlib import Path
from typing import Iterable
from urllib.parse import urlparse, urlsplit, urlunsplit

SCHEMA_VERSION = 1

SCORE_WEIGHTS = {
    "topic_relevance": 25,
    "editorial_selectivity": 20,
    "page_quality": 15,
    "click_likelihood": 15,
    "unique_domain": 10,
    "placement_quality": 10,
    "durability": 5,
}

RISK_PENALTIES = {0: 0, 1: 0, 2: 10, 3: 25, 4: 50, 5: 75}

PROSPECT_FIELDS = [
    "source_domain",
    "source_url",
    "target_url",
    "competitor",
    "anchor_text",
    "link_category",
    "page_title",
    "page_language",
    "import_source",
    "authority_metric",
    "estimated_traffic",
    *SCORE_WEIGHTS.keys(),
    "spam_risk",
    "opportunity_score",
    "score_status",
    "recommended_action",
    "contact_name",
    "contact_email",
    "status",
    "notes",
]

CHANNEL_FIELDS = [
    "channel",
    "category",
    "url",
    "topic",
    "submission_type",
    "relationship",
    "status",
    "last_verified",
    "quality_notes",
    "wins",
    "failures",
]

OUTREACH_FIELDS = [
    "source_url",
    "contact_name",
    "contact_email",
    "status",
    "subject",
    "last_action",
    "next_action",
    "notes",
]

ALIASES = {
    "source_url": {
        "source_url",
        "source",
        "url_from",
        "referring_page",
        "referring_page_url",
        "referring_url",
        "page_url",
    },
    "source_domain": {"source_domain", "referring_domain", "domain"},
    "target_url": {"target_url", "target", "url_to", "linked_url", "destination_url"},
    "anchor_text": {"anchor_text", "anchor", "link_text"},
    "page_title": {"page_title", "referring_page_title", "title"},
    "authority_metric": {"authority_metric", "domain_rating", "domain_authority", "authority_score"},
    "estimated_traffic": {"estimated_traffic", "organic_traffic", "page_traffic", "traffic"},
    "link_category": {"link_category", "category", "type"},
}


class LinkOpsError(ValueError):
    """A user-correctable workspace or input error."""


def normalize_header(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    return value.strip("_")


def valid_http_url(value: str) -> bool:
    try:
        parsed = urlparse(value)
    except ValueError:
        return False
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def domain_from_url(value: str) -> str:
    if not valid_http_url(value):
        return ""
    host = (urlparse(value).hostname or "").lower()
    return host[4:] if host.startswith("www.") else host


def blank_row(fields: Iterable[str]) -> dict[str, str]:
    return {field: "" for field in fields}


def write_csv(path: Path, fieldnames: list[str], rows: Iterable[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def _lookup_value(row: dict[str, str], canonical: str) -> str:
    normalized = {normalize_header(key): (value or "").strip() for key, value in row.items() if key}
    if canonical in normalized:
        return normalized[canonical]
    for alias in sorted(ALIASES.get(canonical, set())):
        if alias in normalized:
            return normalized[alias]
    return ""


def canonicalize_row(
    row: dict[str, str],
    *,
    import_source: str = "",
    competitor: str = "",
) -> dict[str, str]:
    result = blank_row(PROSPECT_FIELDS)
    for field in PROSPECT_FIELDS:
        result[field] = _lookup_value(row, field)
    if import_source:
        result["import_source"] = import_source
    if competitor:
        result["competitor"] = competitor
    if not result["source_domain"]:
        result["source_domain"] = domain_from_url(result["source_url"])
    return result


def prospect_key(row: dict[str, str]) -> tuple[str, str, str]:
    def normalize_url(value: str) -> str:
        value = value.strip()
        try:
            parts = urlsplit(value)
            return urlunsplit((parts.scheme.lower(), parts.netloc.lower(), parts.path or "/", parts.query, ""))
        except ValueError:
            return value

    return (
        normalize_url(row.get("source_url", "")),
        normalize_url(row.get("target_url", "")),
        row.get("competitor", "").strip().lower(),
    )


def init_workspace(output: Path, *, site: str = "", name: str = "") -> None:
    if output.exists() and any(output.iterdir()):
        raise LinkOpsError(f"output directory is not empty: {output}")
    output.mkdir(parents=True, exist_ok=True)
    brief = {
        "schema_version": SCHEMA_VERSION,
        "site": site,
        "name": name,
        "goal": "",
        "target_pages": [],
        "competitors": [],
        "constraints": [],
    }
    (output / "brief.json").write_text(
        json.dumps(brief, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    write_csv(output / "prospects.csv", PROSPECT_FIELDS, [])
    write_csv(output / "channels.csv", CHANNEL_FIELDS, [])
    write_csv(output / "outreach.csv", OUTREACH_FIELDS, [])


def import_csv(
    run: Path,
    input_path: Path,
    *,
    import_source: str = "",
    competitor: str = "",
) -> tuple[int, int]:
    prospects_path = run / "prospects.csv"
    if not prospects_path.is_file():
        raise LinkOpsError("prospects.csv is missing; run init first")
    existing = read_csv(prospects_path)
    incoming = [
        canonicalize_row(row, import_source=import_source, competitor=competitor)
        for row in read_csv(input_path)
    ]

    seen = {prospect_key(row) for row in existing if row.get("source_url", "").strip()}
    added = 0
    skipped = 0
    for row in incoming:
        if not row["source_url"]:
            skipped += 1
            continue
        key = prospect_key(row)
        if key in seen:
            skipped += 1
            continue
        existing.append(row)
        seen.add(key)
        added += 1

    write_csv(prospects_path, PROSPECT_FIELDS, existing)
    return added, skipped


def _parse_score(value: str, field: str) -> float:
    try:
        score = float(value)
    except ValueError as exc:
        raise LinkOpsError(f"{field} must be a number from 0 to 5: {value!r}") from exc
    if not math.isfinite(score) or score < 0 or score > 5:
        raise LinkOpsError(f"{field} must be from 0 to 5: {value!r}")
    if field == "spam_risk" and not score.is_integer():
        raise LinkOpsError("spam_risk must be an integer from 0 to 5")
    return score


def _format_score(value: float) -> str:
    return f"{value:.1f}"


def score_row(row: dict[str, str]) -> dict[str, str]:
    result = {field: row.get(field, "") for field in PROSPECT_FIELDS}
    required = [*SCORE_WEIGHTS.keys(), "spam_risk"]
    if any(not result[field].strip() for field in required):
        result["opportunity_score"] = ""
        result["score_status"] = "incomplete"
        result["recommended_action"] = ""
        return result

    values = {field: _parse_score(result[field], field) for field in SCORE_WEIGHTS}
    spam_risk = _parse_score(result["spam_risk"], "spam_risk")
    base = sum(values[field] / 5 * weight for field, weight in SCORE_WEIGHTS.items())
    risk_index = int(round(spam_risk))
    final = max(0.0, base - RISK_PENALTIES[risk_index])

    result["opportunity_score"] = _format_score(final)
    result["score_status"] = "complete"
    if spam_risk >= 4:
        result["recommended_action"] = "reject"
    elif final >= 75:
        result["recommended_action"] = "priority"
    elif final >= 55:
        result["recommended_action"] = "consider"
    else:
        result["recommended_action"] = "low"
    return result


def score_workspace(run: Path) -> int:
    path = run / "prospects.csv"
    if not path.is_file():
        raise LinkOpsError("prospects.csv is missing; run init first")
    rows = read_csv(path)
    scored = [score_row(row) for row in rows]
    write_csv(path, PROSPECT_FIELDS, scored)
    return sum(row["score_status"] == "complete" for row in scored)


def validate_workspace(run: Path) -> list[dict[str, object]]:
    issues: list[dict[str, object]] = []
    required_files = {
        "brief.json": None,
        "prospects.csv": PROSPECT_FIELDS,
        "channels.csv": CHANNEL_FIELDS,
        "outreach.csv": OUTREACH_FIELDS,
    }
    for filename in required_files:
        if not (run / filename).is_file():
            issues.append(
                {"severity": "error", "code": "missing-file", "file": filename, "message": "required file is missing"}
            )

    prospects_path = run / "prospects.csv"
    if not prospects_path.is_file():
        return issues

    with prospects_path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        headers = reader.fieldnames or []
        missing = [field for field in PROSPECT_FIELDS if field not in headers]
        for field in missing:
            issues.append(
                {"severity": "error", "code": "missing-column", "file": "prospects.csv", "field": field, "message": "required column is missing"}
            )
        rows = list(reader)

    seen: set[tuple[str, str, str]] = set()
    score_fields = [*SCORE_WEIGHTS.keys(), "spam_risk"]
    for index, row in enumerate(rows, start=2):
        source_url = (row.get("source_url") or "").strip()
        target_url = (row.get("target_url") or "").strip()
        if source_url and not valid_http_url(source_url):
            issues.append(
                {"severity": "error", "code": "invalid-url", "file": "prospects.csv", "row": index, "field": "source_url", "message": source_url}
            )
        if target_url and not valid_http_url(target_url):
            issues.append(
                {"severity": "error", "code": "invalid-url", "file": "prospects.csv", "row": index, "field": "target_url", "message": target_url}
            )
        key = prospect_key(row)
        if source_url:
            if key in seen:
                issues.append(
                    {"severity": "error", "code": "duplicate-prospect", "file": "prospects.csv", "row": index, "message": "duplicate source/target/competitor"}
                )
            seen.add(key)

        for field in score_fields:
            value = (row.get(field) or "").strip()
            if not value:
                continue
            try:
                _parse_score(value, field)
            except LinkOpsError as exc:
                issues.append(
                    {"severity": "error", "code": "invalid-score", "file": "prospects.csv", "row": index, "field": field, "message": str(exc)}
                )

    return issues


def _print_validation(issues: list[dict[str, object]], output_format: str) -> None:
    if output_format == "json":
        print(json.dumps({"issues": issues}, ensure_ascii=False, indent=2))
        return
    if not issues:
        print("link-ops workspace is valid")
        return
    for issue in issues:
        location = f"{issue.get('file', '')}"
        if issue.get("row"):
            location += f":{issue['row']}"
        field = f" [{issue['field']}]" if issue.get("field") else ""
        print(f"{issue['severity']}: {issue['code']}: {location}{field}: {issue['message']}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Local data helpers for the link-ops skill")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="create a link-ops workspace")
    init_parser.add_argument("--output", required=True, type=Path)
    init_parser.add_argument("--site", default="")
    init_parser.add_argument("--name", default="")

    import_parser = subparsers.add_parser("import", help="normalize and append a backlink CSV export")
    import_parser.add_argument("--run", required=True, type=Path)
    import_parser.add_argument("--input", required=True, type=Path)
    import_parser.add_argument("--source", default="")
    import_parser.add_argument("--competitor", default="")

    score_parser = subparsers.add_parser("score", help="calculate opportunity scores for complete rows")
    score_parser.add_argument("--run", required=True, type=Path)

    validate_parser = subparsers.add_parser("validate", help="validate workspace files and prospect data")
    validate_parser.add_argument("--run", required=True, type=Path)
    validate_parser.add_argument("--format", choices=("text", "json"), default="text")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "init":
            init_workspace(args.output, site=args.site, name=args.name)
            print(f"initialized {args.output}")
            return 0
        if args.command == "import":
            added, skipped = import_csv(
                args.run,
                args.input,
                import_source=args.source,
                competitor=args.competitor,
            )
            print(f"added={added} skipped={skipped}")
            return 0
        if args.command == "score":
            scored = score_workspace(args.run)
            print(f"scored={scored}")
            return 0
        if args.command == "validate":
            issues = validate_workspace(args.run)
            _print_validation(issues, args.format)
            return 1 if any(issue["severity"] == "error" for issue in issues) else 0
    except (OSError, LinkOpsError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    parser.error("unknown command")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
