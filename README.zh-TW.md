# Academic Research Skills for Codex

[![Version](https://img.shields.io/badge/version-v3.7.0-blue)](https://github.com/Imbad0202/academic-research-skills-codex/releases/tag/v3.7.0)
[![License: CC BY-NC 4.0](https://img.shields.io/badge/license-CC%20BY--NC%204.0-lightgrey)](https://creativecommons.org/licenses/by-nc/4.0/)

[English](README.md)

## 重新打包聲明

This is an unofficial Codex-facing adaptation of Academic Research Skills by [Cheng-I Wu](https://github.com/Imbad0202/).

Original project:
https://github.com/Imbad0202/academic-research-skills

Original license:
[CC BY-NC 4.0](https://github.com/Imbad0202/academic-research-skills/blob/main/LICENSE)

This adaptation is distributed for non-commercial use only.


## 功能

- **Deep Research**：13-agent 研究流程，包含 Socratic guided mode、文獻回顧、事實查核、系統性回顧、來源驗證、綜整與 bias 檢查。
- **Academic Paper**：12-agent 論文寫作流程，包含規劃、起草、修訂、引用檢查、揭露聲明、雙語摘要，以及 DOCX（Pandoc 可用時）。
- **Academic Paper Reviewer**：多視角審查，包含主編、方法、領域、跨領域與 Devil's Advocate 角色。
- **Academic Pipeline**：10-stage orchestrator，串接研究、寫作、完整性檢查、審查、修訂、最終完整性檢查、格式化與流程摘要。

## 安裝

可安裝的 Codex skills 是四個頂層 skill 目錄：

- `deep-research`
- `academic-paper`
- `academic-paper-reviewer`
- `academic-pipeline`

這個 bundle 也需要 repo 根目錄的 `shared/`、`scripts/`、`docs/` 與 `MODE_REGISTRY.md`。不要把整個 repository 當成單一巢狀 skill 安裝；那會讓四個 `SKILL.md` entrypoint 被埋得太深。

把這個 repository 作為本機 Codex skills bundle 使用：

```bash
git clone https://github.com/Imbad0202/academic-research-skills-codex.git ~/academic-research-skills-codex
```

接著依你的 Codex 安裝方式，把四個 skill root 以 symlink 或 copy 暴露到本機 Codex skills 目錄。請保留 repository 本體，因為 skills 會引用根目錄的 `shared/`、`scripts/` 與 `docs/`。

完整設定請見 [docs/SETUP.zh-TW.md](docs/SETUP.zh-TW.md)。

## 使用方式

### Individual Skills

#### Deep Research（深度研究，7 種模式）

```text
"Research the impact of AI on higher education"       -> full mode
"Give me a quick brief on X"                          -> quick mode
"Do a systematic review on X with PRISMA"             -> systematic-review mode
"Guide my research on X"                              -> socratic mode
"Fact-check these claims"                             -> fact-check mode
"Do a literature review on X"                         -> lit-review mode
"Review this paper's research quality"                -> review mode
```

#### Academic Paper（學術論文撰寫，10 種模式）

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

#### Academic Paper Reviewer（論文審查，6 種模式）

```text
"Review this paper"                                   -> full mode
"Quick assessment of this paper"                      -> quick mode
"Guide me to improve this paper"                      -> guided mode
"Check the methodology"                               -> methodology-focus mode
"Verify the revisions"                                -> re-review mode
"Calibrate this reviewer against my gold set"         -> calibration mode
```

#### Academic Pipeline（全流程調度器）

```text
"I want to write a complete research paper"           -> Stage 1 起跑的完整 pipeline
"I already have a paper, review it"                   -> Stage 2.5 中途進入
"I received reviewer comments"                        -> Stage 4 中途進入
"resume_from_passport=<hash>"                         -> 從 Material Passport reset boundary 恢復
```
