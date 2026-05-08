# Academic Research Skills for Codex

[![Version](https://img.shields.io/badge/version-v3.7.0-blue)](https://github.com/Imbad0202/academic-research-skills-codex/releases/tag/v3.7.0)
[![License: CC BY-NC 4.0](https://img.shields.io/badge/license-CC%20BY--NC%204.0-lightgrey)](https://creativecommons.org/licenses/by-nc/4.0/)

[繁體中文版](README.zh-TW.md)

## Repackaging Notice

This is an unofficial Codex-facing adaptation of Academic Research Skills by [Cheng-I Wu](https://github.com/Imbad0202/).

Original project:
https://github.com/Imbad0202/academic-research-skills

Original license:
[CC BY-NC 4.0](https://github.com/Imbad0202/academic-research-skills/blob/main/LICENSE)

This adaptation is distributed for non-commercial use only.


## Features

- **Deep Research**: 13-agent research workflow with Socratic guided mode, literature review, fact-checking, systematic review, source verification, synthesis, and risk-of-bias checks.
- **Academic Paper**: 12-agent paper writing workflow with planning, drafting, revision, citation checks, disclosure generation, bilingual abstracts, and DOCX (via Pandoc when available).
- **Academic Paper Reviewer**: Multi-perspective review with EIC, methodology, domain, interdisciplinary, and Devil's Advocate review roles.
- **Academic Pipeline**: 10-stage orchestrator that coordinates research, writing, integrity checks, review, revision, final integrity, formatting, and process summary.

## Install

The installable Codex skills are the four top-level skill directories:

- `deep-research`
- `academic-paper`
- `academic-paper-reviewer`
- `academic-pipeline`

The bundle also requires the repo-root support directories `shared/`, `scripts/`, `docs/`, and `MODE_REGISTRY.md`. Do not install the whole repository as one nested skill; that hides the four `SKILL.md` entrypoints.

Use this repository as a local Codex skills bundle:

```bash
git clone https://github.com/Imbad0202/academic-research-skills-codex.git ~/academic-research-skills-codex
```

Then expose the four skill roots to your local Codex skills directory using symlinks or copies, depending on how your Codex install loads skills. Keep the repository itself available because the skills reference root-level `shared/`, `scripts/`, and `docs/` files.

For full setup details, see [docs/SETUP.md](docs/SETUP.md).

## Usage

### Individual Skills

#### Deep Research (7 modes)

```text
"Research the impact of AI on higher education"       -> full mode
"Give me a quick brief on X"                          -> quick mode
"Do a systematic review on X with PRISMA"             -> systematic-review mode
"Guide my research on X"                              -> socratic mode
"Fact-check these claims"                             -> fact-check mode
"Do a literature review on X"                         -> lit-review mode
"Review this paper's research quality"                -> review mode
```

#### Academic Paper (10 modes)

```text
"Write a paper on X"                                  -> full mode
"Guide me through writing a paper"                    -> plan mode
"Build a paper outline"                               -> outline-only mode
"I have a draft, here are reviewer comments"          -> revision mode
"Parse these reviewer comments into a roadmap"        -> revision-coach mode
"Write an abstract for this paper"                    -> abstract-only mode
"Turn this into a literature review paper"            -> lit-review mode
"Convert to LaTeX" / "Convert citations to IEEE"      -> format-convert mode
"Check citations"                                     -> citation-check mode
"Generate an AI disclosure statement for NeurIPS"     -> disclosure mode
```

#### Academic Paper Reviewer (6 modes)

```text
"Review this paper"                                   -> full mode
"Quick assessment of this paper"                      -> quick mode
"Guide me to improve this paper"                      -> guided mode
"Check the methodology"                               -> methodology-focus mode
"Verify the revisions"                                -> re-review mode
"Calibrate this reviewer against my gold set"         -> calibration mode
```

#### Academic Pipeline (Orchestrator)

```text
"I want to write a complete research paper"           -> full pipeline from Stage 1
"I already have a paper, review it"                   -> mid-entry at Stage 2.5
"I received reviewer comments"                        -> mid-entry at Stage 4
"resume_from_passport=<hash>"                         -> resume from a Material Passport reset boundary
```
