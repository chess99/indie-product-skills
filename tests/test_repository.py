import hashlib
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.validate_repository import ROOT, check_manifests, check_plugin_bundle, check_references, check_vendor, run_check


class RepositoryTests(unittest.TestCase):
    def test_packaged_resources_manifests_and_upstream_match(self):
        self.assertEqual(check_manifests(ROOT) + check_references(ROOT) + check_vendor(ROOT), [])

    def test_git_checkout_preserves_locked_vendor_bytes_with_autocrlf(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            vendor = root / "vendor/marketing"
            vendor.mkdir(parents=True)
            files = {"LICENSE": b"Upstream license\n", "guide.md": b"# Upstream guide\r\n"}
            for name, content in files.items():
                (vendor / name).write_bytes(content)
            lock = {
                "commit": "a" * 40, "skills": [],
                "files": {name: hashlib.sha256(content).hexdigest() for name, content in files.items()},
            }
            (root / "vendor/marketing.lock.json").write_text(json.dumps(lock), encoding="utf-8")
            shutil.copyfile(ROOT / ".gitattributes", root / ".gitattributes")

            def git(*args):
                return subprocess.run(
                    ["git", "-c", "core.autocrlf=true", "-c", "core.safecrlf=false", *args],
                    cwd=root, check=True, capture_output=True,
                )

            git("init", "--quiet")
            git("add", ".")
            for name in files:
                (vendor / name).unlink()
            git("checkout-index", "--all", "--force")
            self.assertEqual(check_vendor(root), [])

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

    def test_navigation_detects_links_to_a_renamed_skill(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            skill = root / "skills/web-performance"
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text("# Website performance\n", encoding="utf-8")
            (root / "docs").mkdir()
            (root / "docs/catalog.md").write_text("[Performance](../skills/performance/SKILL.md)\n", encoding="utf-8")
            (root / "README.md").write_text("[Performance](skills/web-performance/SKILL.md)\n", encoding="utf-8")
            self.assertEqual(check_references(root), ["broken reference in docs/catalog.md: ../skills/performance/SKILL.md"])
            (root / "docs/catalog.md").write_text("[Performance](../skills/web-performance/SKILL.md)\n", encoding="utf-8")
            self.assertEqual(check_references(root), [])

    def test_manifest_check_detects_incomplete_plugin_rename(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for name in (".claude-plugin", ".codex-plugin"):
                shutil.copytree(ROOT / name, root / name)
            # Compatibility links are absent in this fixture; keep their baseline diagnostics.
            baseline = check_manifests(root)
            cases = [
                (".claude-plugin/marketplace.json", lambda data: data.update(name="previous-name"), "marketplace identity differs from plugin"),
                (".claude-plugin/marketplace.json", lambda data: data["plugins"][0].update(name="previous-name"), "marketplace must expose the local plugin under its current name"),
                (".claude-plugin/marketplace.json", lambda data: data["plugins"][0].update(source="./old-plugin"), "marketplace must expose the local plugin under its current name"),
                (".codex-plugin/plugin.json", lambda data: data.update(repository="https://example.com/old-repo"), "plugin manifests disagree on repository"),
                (".codex-plugin/plugin.json", lambda data: data.update(homepage="https://example.com/old-repo"), "plugin manifests disagree on homepage"),
            ]
            for name, mutate, expected in cases:
                with self.subTest(name=name, expected=expected):
                    path = root / name
                    original = path.read_text(encoding="utf-8")
                    data = json.loads(original)
                    mutate(data)
                    path.write_text(json.dumps(data), encoding="utf-8")
                    self.assertEqual(check_manifests(root), [expected] + baseline)
                    path.write_text(original, encoding="utf-8")

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
