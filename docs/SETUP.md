# ARS Setup for Codex

Academic Research Skills is a Codex-only skills bundle. If you only need Markdown output, the minimum setup is a working local Codex environment plus this repository on disk.

## Minimum Viable Setup

1. Install and authenticate Codex according to your local Codex distribution.
2. Make sure `OPENAI_API_KEY` is available if your Codex setup uses API-key authentication.
3. Clone this repository:

```bash
git clone https://github.com/Imbad0202/academic-research-skills-codex.git ~/academic-research-skills-codex
```

4. Expose the four skill roots to your local Codex skills directory by symlink or copy:

```text
deep-research/SKILL.md
academic-paper/SKILL.md
academic-paper-reviewer/SKILL.md
academic-pipeline/SKILL.md
```

Keep the repository root available. The skills reference shared repo-root assets under `shared/`, `scripts/`, `docs/`, and `MODE_REGISTRY.md`.

## Install Shape

Codex discovers skills by their `SKILL.md` entrypoints. This repo contains four separate skills, not one nested skill:

- `deep-research`
- `academic-paper`
- `academic-paper-reviewer`
- `academic-pipeline`

Do not install the whole repository as one nested folder such as `academic-research-skills-codex/deep-research/SKILL.md` under a single skill name. Install or expose each skill root directly, while preserving access to the root-level support files.

## Symlink Install

Use symlinks if you work on one machine and want updates by pulling the repo:

```bash
git clone https://github.com/Imbad0202/academic-research-skills-codex.git ~/academic-research-skills-codex
mkdir -p <codex-skills-dir>
ln -s ~/academic-research-skills-codex/deep-research <codex-skills-dir>/deep-research
ln -s ~/academic-research-skills-codex/academic-paper <codex-skills-dir>/academic-paper
ln -s ~/academic-research-skills-codex/academic-paper-reviewer <codex-skills-dir>/academic-paper-reviewer
ln -s ~/academic-research-skills-codex/academic-pipeline <codex-skills-dir>/academic-pipeline
```

If your skills directory syncs across machines, use copies instead because absolute symlinks may break.

## Copy Install

Use copies if your local Codex skills directory syncs across machines or symlinks are not supported:

```bash
git clone https://github.com/Imbad0202/academic-research-skills-codex.git ~/academic-research-skills-codex
mkdir -p <codex-skills-dir>
cp -R ~/academic-research-skills-codex/deep-research <codex-skills-dir>/deep-research
cp -R ~/academic-research-skills-codex/academic-paper <codex-skills-dir>/academic-paper
cp -R ~/academic-research-skills-codex/academic-paper-reviewer <codex-skills-dir>/academic-paper-reviewer
cp -R ~/academic-research-skills-codex/academic-pipeline <codex-skills-dir>/academic-pipeline
```

For copy installs, also keep a clone of the full repo available for shared references, validators, adapters, and docs. If your Codex runtime cannot resolve repo-root references from copied skill folders, prefer symlinks or a full workspace checkout.

## Optional DOCX Output

Direct `.docx` generation uses [Pandoc](https://pandoc.org/). If Pandoc is unavailable, the formatter falls back to Markdown plus DOCX conversion instructions.

```bash
# macOS
brew install pandoc

# Linux (Debian/Ubuntu)
sudo apt-get install pandoc

# Windows
# Download from https://pandoc.org/installing.html
```

Direct `.docx` generation requires Pandoc, and PDF generation requires `tectonic`.

## Optional LaTeX / PDF Output

PDF output requires [tectonic](https://tectonic-typesetting.github.io/) and suitable fonts:

- Times New Roman
- Source Han Serif TC VF / Noto Serif TC
- Courier New

Markdown output and DOCX conversion instructions work without this.

## Material Passport Corpus Adapters

The optional Material Passport `literature_corpus[]` field can be populated before an ARS session with reference adapters under `scripts/adapters/`:

```bash
pip install -r requirements-dev.txt
python scripts/adapters/folder_scan.py --input /path/to/pdfs --passport passport.yaml --rejection-log rejection_log.yaml
python scripts/adapters/zotero.py --input my-zotero-export.json --passport passport.yaml --rejection-log rejection_log.yaml
python scripts/adapters/obsidian.py --input ~/Obsidian/LitNotes --passport passport.yaml --rejection-log rejection_log.yaml
```

See [../academic-pipeline/references/adapters/overview.md](../academic-pipeline/references/adapters/overview.md) for the adapter contract.

## Optional Environment Flags

All flags default to off:

| Flag | Purpose |
|---|---|
| `ARS_CROSS_MODEL` | Enables optional cross-model verification where configured by the local runtime. |
| `ARS_SOCRATIC_READING_PROBE=1` | Activates the Socratic reading-check probe layer. |
| `ARS_PASSPORT_RESET=1` | Emits Material Passport reset-boundary entries at FULL checkpoints. |
| `ARS_CROSS_MODEL_SAMPLE_INTERVAL` | Sampling interval for advisory cross-model integrity checks. |

## Validation

Run these checks after packaging changes:

```bash
python3 scripts/check_codex_packaging.py
python3 scripts/check_version_consistency.py
python3 scripts/check_spec_consistency.py
python3 scripts/check_data_access_level.py
python3 scripts/check_task_type.py
```
