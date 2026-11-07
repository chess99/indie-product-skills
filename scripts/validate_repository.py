#!/usr/bin/env python3
"""Check packaged resources and upstream integrity; optionally run official CLIs."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]


def check_vendor(root: Path) -> list[str]:
    issues = []
    lock = json.loads((root / "vendor/marketing.lock.json").read_text(encoding="utf-8"))
    vendor = root / "vendor/marketing"
    actual = {
        path.relative_to(vendor).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in vendor.rglob("*") if path.is_file()
    }
    expected = dict(lock["files"])
    for patch in lock.get("patches", []):
        if patch["path"] not in expected or not (root / patch["patch"]).is_file():
            issues.append(f"untracked compatibility patch: {patch['path']}")
        expected[patch["path"]] = patch["sha256"]
    for name in sorted(actual.keys() | expected.keys()):
        if actual.get(name) != expected.get(name):
            issues.append(f"upstream file differs from lock: {name}")
    if not re.fullmatch(r"[0-9a-f]{40}", lock["commit"]):
        issues.append("upstream commit must be a full SHA")
    for name in lock["skills"]:
        entry = root / "skills" / name
        if not entry.is_symlink() or entry.resolve() != (vendor / name).resolve():
            issues.append(f"upstream entry must reference vendor: {name}")
        if not (entry / "SKILL.md").is_file():
            issues.append(f"missing upstream skill: {name}")
    return issues


def check_references(root: Path) -> list[str]:
    issues = []
    paths = [path for path in (root / "README.md", root / "AGENTS.md") if path.is_file()]
    paths.extend((root / "docs").rglob("*.md"))
    for skill in sorted((root / "skills").iterdir()):
        if not (skill / "SKILL.md").is_file():
            issues.append(f"missing skill entrypoint: {skill.name}")
            continue
        if skill.is_symlink():
            continue  # Upstream templates may contain illustrative Markdown links.
        paths.extend(skill.rglob("*.md"))
    for path in paths:
        text = path.read_text(encoding="utf-8")
        for target in re.findall(r"\]\(([^\s)]+)\)", text):
            if target.startswith(("https:", "http:", "#", "mailto:")):
                continue
            target = unquote(target.split("#", 1)[0])
            if not (path.parent / target).exists():
                issues.append(f"broken reference in {path.relative_to(root).as_posix()}: {target}")
    return issues


def check_manifests(root: Path) -> list[str]:
    issues = []
    claude = json.loads((root / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))
    codex = json.loads((root / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
    market = json.loads((root / ".claude-plugin/marketplace.json").read_text(encoding="utf-8"))
    for field in ("name", "version", "skills", "repository", "homepage"):
        if claude[field] != codex[field]:
            issues.append(f"plugin manifests disagree on {field}")
    if market["name"] != claude["name"]:
        issues.append("marketplace identity differs from plugin")
    entries = market["plugins"]
    if len(entries) != 1 or entries[0]["name"] != claude["name"] or entries[0]["source"] != "./":
        issues.append("marketplace must expose the local plugin under its current name")
    if market["metadata"]["version"] != claude["version"]:
        issues.append("marketplace version differs from plugin")
    for name in (".claude/skills", ".agents/skills", ".catpaw/skills", "CLAUDE.md"):
        path = root / name
        target = root / ("AGENTS.md" if name == "CLAUDE.md" else "skills")
        if not path.is_symlink() or path.resolve() != target.resolve():
            issues.append(f"compatibility entry must link to canonical source: {name}")
    return issues


def run_check(command: list[str]) -> str | None:
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=120)
    except (OSError, subprocess.TimeoutExpired) as error:
        return f"{command[0]}: {error}"
    if result.returncode:
        return f"{' '.join(command)}\n{result.stdout}{result.stderr}"
    return None


def check_plugin_bundle(root: Path, claude: str) -> list[str]:
    """Validate a disposable, dereferenced install tree; never edit canonical links."""
    issues = []
    with tempfile.TemporaryDirectory(prefix="indie-product-plugin-") as temp:
        bundle = Path(temp)
        shutil.copytree(root / "skills", bundle / "skills", symlinks=False)
        shutil.copytree(root / ".claude-plugin", bundle / ".claude-plugin")
        shutil.copyfile(root / "README.md", bundle / "README.md")
        for name in ("plugin.json", "marketplace.json"):
            error = run_check([claude, "plugin", "validate", str(bundle / ".claude-plugin" / name), "--strict"])
            if error:
                issues.append(error)
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skills-ref", help="official skills-ref executable")
    parser.add_argument("--claude", help="Claude CLI executable for plugin manifest validation")
    args = parser.parse_args()
    issues = check_vendor(ROOT) + check_references(ROOT) + check_manifests(ROOT)
    skills = sorted((ROOT / "skills").iterdir())
    if args.skills_ref:
        for skill in skills:
            error = run_check([args.skills_ref, "validate", str(skill.resolve())])
            if error:
                issues.append(error)
    if args.claude:
        issues.extend(check_plugin_bundle(ROOT, args.claude))
    for issue in issues:
        print(issue)
    print(f"{len(skills)} skills; {len(issues)} validation issues")
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
