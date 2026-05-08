#!/usr/bin/env python3
"""Validate the Codex-only ARS bundle shape."""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path


SKILLS = (
    "deep-research",
    "academic-paper",
    "academic-paper-reviewer",
    "academic-pipeline",
)

REQUIRED_ROOTS = ("shared", "scripts", "docs")
FORBIDDEN_PATHS = (
    ".claude",
    ".claude-plugin",
    "hooks/hooks.json",
)
FORBIDDEN_ACTIVE_TEXT = (
    ".claude-plugin",
    ".claude/skills",
    "${CLAUDE_PLUGIN_ROOT}",
    "ANTHROPIC_API_KEY",
    "claude --dangerously-skip-permissions",
    "curl -fsSL https://claude.ai/install.sh",
    "irm https://claude.ai/install.ps1",
)

ACTIVE_TEXT_PATHS = (
    "AGENTS.md",
    "README.md",
    "README.zh-TW.md",
    "MODE_REGISTRY.md",
    "docs/SETUP.md",
    "docs/SETUP.zh-TW.md",
    "docs/PERFORMANCE.md",
    "docs/PERFORMANCE.zh-TW.md",
    "docs/ARCHITECTURE.md",
    ".github/workflows/spec-consistency.yml",
)


def _is_symlink_ok(path: Path) -> bool:
    target = os.readlink(path)
    resolved = (path.parent / target).resolve()
    return resolved.exists()


def check(root: Path) -> list[str]:
    errors: list[str] = []

    for name in SKILLS:
        skill_md = root / name / "SKILL.md"
        if not skill_md.is_file():
            errors.append(f"{skill_md}: missing installable Codex skill entry")

    for rel in REQUIRED_ROOTS:
        if not (root / rel).is_dir():
            errors.append(f"{rel}/: required shared support directory is missing")

    for rel in FORBIDDEN_PATHS:
        if (root / rel).exists():
            errors.append(f"{rel}: Claude-only packaging surface must be removed")

    for link_dir in ("skills", "agents"):
        base = root / link_dir
        if not base.exists():
            continue
        for child in sorted(base.iterdir()):
            if child.is_symlink() and not _is_symlink_ok(child):
                errors.append(f"{child}: symlink target does not resolve")

    for rel in ACTIVE_TEXT_PATHS:
        path = root / rel
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for forbidden in FORBIDDEN_ACTIVE_TEXT:
            if forbidden in text:
                errors.append(f"{rel}: forbidden active Codex-only text {forbidden!r}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--path",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="Repository root to validate.",
    )
    args = parser.parse_args()

    errors = check(args.path)
    if errors:
        print("Codex packaging check failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Codex packaging check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
