# ARS Codex 效能說明

ARS 是 Codex-only skills bundle。模型、reasoning effort 與工具權限由本機 Codex runtime 控制。完整 pipeline 建議使用高推理能力模型；只有 citation-format checks 這類窄範圍機械任務才建議降成本。

完整 academic pipeline 會消耗大量 context。單次 end-to-end run 可能超過 200K input tokens 與 100K output tokens，實際取決於論文字數、corpus 大小與 revision rounds。

## 各模式 Token 估算

| Skill / 模式 | 輸入 Token | 輸出 Token |
|---|---:|---:|
| `deep-research` socratic | ~30K | ~15K |
| `deep-research` full | ~60K | ~30K |
| `deep-research` systematic-review | ~100K | ~50K |
| `academic-paper` plan | ~40K | ~20K |
| `academic-paper` full | ~80K | ~50K |
| `academic-paper-reviewer` full | ~50K | ~30K |
| `academic-paper-reviewer` quick | ~15K | ~8K |
| Full pipeline | ~200K+ | ~100K+ |
| + cross-model verification | +~10K external | +~5K external |

估算基準是約 15,000 字、60 篇 references 的論文。實際用量會隨 paper length、revision loops、corpus size 與 dialogue depth 變動。

## Codex Runtime 建議

- `academic-pipeline`、`deep-research full`、`deep-research systematic-review`、`academic-paper full`、`academic-paper-reviewer full` 建議使用高 reasoning 設定。
- `citation-check`、`format-convert`、`abstract-only`、`quick` 等 bounded modes 可用較低成本設定。
- Active workspace 需要能存取 `shared/`、`scripts/` 與 `docs/`；許多 prompts 會用 repo-relative path 引用這些檔案。
- `AGENTS.md` 是 Codex routing 與 project instruction 的 source of truth。

## Codex Agent Notes

`agents/` 內的 selected downstream agent prompts 是 canonical source files 的 symlink：

- `synthesis_agent`
- `research_architect_agent`
- `report_compiler_agent`

這些是 Codex-readable prompt assets，不是額外的 model-routing layer。實際模型與 reasoning effort 由當前 Codex session 決定。

## 長時間 Session 管理

完整 ARS run 是 human-in-the-loop，常跨數小時到數天。每個 stage 完成後都需要使用者確認才會前進。

設定 `ARS_PASSPORT_RESET=1` 時，FULL checkpoints 可寫入 Material Passport reset-boundary entries。後續 session 可用：

```text
resume_from_passport=<hash> [stage=<n>] [mode=<m>]
```

此命令指定 boundary hash 與選用 stage/mode override。Passport file discovery 由 workspace convention 處理，通常是 `./passports/<slug>/` 或符合 `./material_passport*.yaml` 的檔案。

適合 reset 的情境：

- 前一個 session 累積大量 context，而下一階段不需要；
- systematic review 有清楚 stage boundaries；
- 新 session 比攜帶全部歷史對話更清楚、更省。

適合 continuation 的情境：

- 任務很短；
- 使用者想保留 live Socratic branch；
- Material Passport 沒有捕捉某個重要 in-session decision。

## Literature Corpus 成本

Material Passport 帶有非空 `literature_corpus[]` 時，Phase 1 corpus screening 成本會隨 corpus size 增加：

| Corpus size | 每個 consumer 的 Step 1 pre-screening |
|---|---:|
| Empty / absent | 0 |
| ~50 entries | +~3-5K input + ~1-2K output |
| ~200 entries | +~10-15K input + ~3-5K output |
| ~500 entries | +~25-40K input + ~8-12K output |

大型 library 建議先裁切後再產生 passport。

## Cross-Model Audit Wrapper

`scripts/run_codex_audit.sh` 會為特定 audit workflow dispatch 獨立 Codex CLI process。需求：

- 已登入 Codex CLI 或設定 `OPENAI_API_KEY`；
- `git`、`jq`、`python3`；
- Bash 4+；
- working directory 位於 ARS repository 內。

Wrapper 只寫入 output directory 的 audit artifacts，不會直接修改 Material Passport。完整 contract 見 `docs/design/2026-04-30-ars-v3.6.7-step-6-orchestrator-hooks-spec.md`。
