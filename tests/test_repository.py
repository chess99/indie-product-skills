import hashlib
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.validate_repository import ROOT, check_manifests, check_plugin_bundle, check_references, check_vendor, run_check


class RepositoryTests(unittest.TestCase):
    def test_packaged_resources_manifests_and_upstream_match(self):
        self.assertEqual(check_manifests(ROOT) + check_references(ROOT) + check_vendor(ROOT), [])

    def test_vendor_check_detects_edits_additions_and_removals(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            vendor = root / "vendor/marketing"
            vendor.mkdir(parents=True)
            (vendor / "original.md").write_text("changed", encoding="utf-8")
            (vendor / "extra.md").write_text("extra", encoding="utf-8")
            lock = {"commit": "a" * 40, "skills": [], "files": {"original.md": hashlib.sha256(b"original").hexdigest(), "missing.md": "a" * 64}}
            (root / "vendor/marketing.lock.json").write_text(json.dumps(lock), encoding="utf-8")
            issues = check_vendor(root)
            self.assertEqual(len(issues), 3)
            for name in ("original.md", "extra.md", "missing.md"):
                self.assertTrue(any(name in issue for issue in issues))

    def test_reference_check_detects_missing_resource(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            skill = root / "skills/example"
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text("[Missing](references/missing.md)\n[Web](https://example.com)", encoding="utf-8")
            self.assertEqual(len(check_references(root)), 1)

    def test_missing_compatibility_patch_is_reported(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            vendor = root / "vendor/marketing"
            vendor.mkdir(parents=True)
            (vendor / "guide.md").write_text("patched", encoding="utf-8")
            lock = {
                "commit": "a" * 40, "skills": [],
                "files": {"guide.md": hashlib.sha256(b"original").hexdigest()},
                "patches": [{"path": "guide.md", "patch": "patches/missing.patch", "sha256": hashlib.sha256(b"patched").hexdigest()}],
            }
            (root / "vendor/marketing.lock.json").write_text(json.dumps(lock), encoding="utf-8")
            self.assertEqual(check_vendor(root), ["untracked compatibility patch: guide.md"])

    def test_plugin_validation_uses_real_skill_files_and_propagates_failure(self):
        def inspect_bundle(command):
            bundle = Path(command[3]).parent.parent
            for skill in (bundle / "skills").iterdir():
                self.assertFalse(skill.is_symlink())
                self.assertTrue((skill / "SKILL.md").is_file())
            return "validator failed" if command[3].endswith("plugin.json") else None

        with patch("scripts.validate_repository.run_check", side_effect=inspect_bundle):
            self.assertEqual(check_plugin_bundle(ROOT, "claude"), ["validator failed"])

    def test_official_validator_failure_is_not_mistaken_for_valid_substring(self):
        with patch("scripts.validate_repository.subprocess.run", return_value=subprocess.CompletedProcess([], 1, "Invalid skill", "")):
            self.assertIsNotNone(run_check(["validator", "example"]))
        with patch("scripts.validate_repository.subprocess.run", side_effect=FileNotFoundError("missing")):
            self.assertIsNotNone(run_check(["missing"]))

    def test_first_party_eval_cases_have_runnable_inputs_and_unique_ids(self):
        for skill in (ROOT / "skills").iterdir():
            if skill.is_symlink():
                continue
            files = list((skill / "evals").glob("*.json"))
            self.assertTrue(files, skill.name)
            for path in files:
                data = json.loads(path.read_text(encoding="utf-8"))
                self.assertEqual(data["skill_name"], skill.name)
                ids = [case["id"] for case in data["evals"]]
                self.assertEqual(len(ids), len(set(ids)))
                for case in data["evals"]:
                    self.assertTrue(case["prompt"].strip())
                    self.assertTrue(case["expected_output"].strip())
                    for name in case.get("files", []):
                        self.assertTrue((skill / name).is_file(), name)


if __name__ == "__main__":
    unittest.main()
