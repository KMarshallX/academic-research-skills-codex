"""Unit tests for check_codex_packaging.py."""
from __future__ import annotations

import subprocess
import textwrap
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from scripts._test_helpers import run_script

SCRIPT = Path(__file__).resolve().parent / "check_codex_packaging.py"


def _run(root: Path) -> subprocess.CompletedProcess:
    return run_script(SCRIPT, "--path", str(root))


def _write_minimal_bundle(root: Path) -> None:
    for name in (
        "deep-research",
        "academic-paper",
        "academic-paper-reviewer",
        "academic-pipeline",
    ):
        skill_dir = root / name
        skill_dir.mkdir(parents=True)
        (skill_dir / "SKILL.md").write_text(f"# {name}\n", encoding="utf-8")

    for dirname in ("shared", "scripts", "docs"):
        (root / dirname).mkdir(exist_ok=True)

    for rel in (
        "AGENTS.md",
        "README.md",
        "README.zh-TW.md",
        "MODE_REGISTRY.md",
        "docs/SETUP.md",
        "docs/SETUP.zh-TW.md",
        "docs/PERFORMANCE.md",
        "docs/PERFORMANCE.zh-TW.md",
        "docs/ARCHITECTURE.md",
    ):
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("Codex bundle fixture\n", encoding="utf-8")


class TestCodexPackaging(unittest.TestCase):
    def test_minimal_bundle_passes(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_minimal_bundle(root)
            result = _run(root)
            self.assertEqual(
                result.returncode, 0,
                msg=f"stdout={result.stdout!r} stderr={result.stderr!r}",
            )

    def test_forbidden_claude_surface_fails(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_minimal_bundle(root)
            (root / ".claude-plugin").mkdir()
            result = _run(root)
            self.assertEqual(result.returncode, 1)
            self.assertIn(".claude-plugin", result.stdout)

    def test_forbidden_active_text_fails(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_minimal_bundle(root)
            (root / "docs" / "SETUP.md").write_text(
                "Install with ANTHROPIC_API_KEY\n",
                encoding="utf-8",
            )
            result = _run(root)
            self.assertEqual(result.returncode, 1)
            self.assertIn("ANTHROPIC_API_KEY", result.stdout)

    def test_broken_symlink_fails(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_minimal_bundle(root)
            links = root / "skills"
            links.mkdir()
            (links / "deep-research").symlink_to("../missing")
            result = _run(root)
            self.assertEqual(result.returncode, 1)
            self.assertIn("symlink target", result.stdout)

    def test_missing_skill_fails(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_minimal_bundle(root)
            for child in (root / "academic-paper").iterdir():
                child.unlink()
            (root / "academic-paper").rmdir()
            result = _run(root)
            self.assertEqual(result.returncode, 1)
            self.assertIn("academic-paper", result.stdout)


if __name__ == "__main__":
    unittest.main()
