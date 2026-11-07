import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / "skills" / "find-product-opportunities"


class MetadataTests(unittest.TestCase):
    def test_codex_manifest_declares_skill_only_plugin(self) -> None:
        manifest = json.loads((ROOT / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))

        self.assertEqual(manifest["name"], "indie-product-skills")
        self.assertRegex(manifest["version"], r"^\d+\.\d+\.\d+$")
        self.assertEqual(manifest["author"]["name"], "chess99")
        self.assertEqual(manifest["repository"], "https://github.com/chess99/indie-product-skills")
        self.assertEqual(manifest["license"], "MIT")
        self.assertEqual(manifest["skills"], "./skills/")
        self.assertFalse({"apps", "mcpServers", "hooks"} & set(manifest))

    def test_claude_manifest_matches_plugin_identity(self) -> None:
        codex = json.loads((ROOT / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
        claude = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))

        self.assertEqual(claude["name"], codex["name"])
        self.assertEqual(claude["version"], codex["version"])
        self.assertEqual(claude["skills"], "./skills/")

    def test_skill_has_concrete_trigger_description_and_no_placeholders(self) -> None:
        content = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        frontmatter = content.split("---", 2)[1]

        self.assertIn("name: find-product-opportunities", frontmatter)
        self.assertRegex(frontmatter, r"description: .*(产品机会|product opportunit)")
        self.assertNotRegex(content, r"\b(TODO|TBD)\b|\[TODO:")
        self.assertIn("NO-GO", content)
        self.assertIn("Google Trends", content)

    def test_skill_resources_are_complete_and_one_level_deep(self) -> None:
        expected = {
            "evidence.md",
            "report.md",
            "scoring.md",
            "source-strategy.md",
        }
        references = SKILL / "references"

        self.assertTrue(expected <= {path.name for path in references.glob("*.md")})
        self.assertTrue((SKILL / "assets" / "report-template.md").is_file())
        self.assertTrue((SKILL / "scripts" / "opportunity_radar" / "__main__.py").is_file())

    def test_eval_cases_cover_positive_negative_and_failure_paths(self) -> None:
        evals = json.loads((SKILL / "evals" / "evals.json").read_text(encoding="utf-8"))
        labels = {case["label"] for case in evals["evals"]}

        self.assertTrue({"trigger", "non-trigger", "no-go", "source-failure"} <= labels)
        self.assertGreaterEqual(len(evals["evals"]), 6)

    def test_marketplace_descriptions_do_not_hardcode_skill_counts(self) -> None:
        marketplace = (ROOT / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8")

        self.assertNotRegex(marketplace, r"\b\d+ first-party skills?\b")


if __name__ == "__main__":
    unittest.main()
