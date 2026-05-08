# ARS Performance Notes for Codex

ARS is a Codex-only skills bundle. Model choice, reasoning effort, and tool permissions are controlled by the local Codex runtime. Use a high-reasoning frontier model for full-pipeline work and a lower-cost model only for narrow mechanical tasks such as citation-format checks.

The full academic pipeline consumes a large amount of context. A single end-to-end run can exceed 200K input tokens plus 100K output tokens depending on paper length, corpus size, and revision rounds.

## Estimated Token Usage by Mode

| Skill / Mode | Input Tokens | Output Tokens |
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

Estimates assume a roughly 15,000-word paper with about 60 references. Actual usage varies with paper length, revision loops, supplied corpus size, and dialogue depth.

## Codex Runtime Guidance

- Prefer a high-reasoning model for `academic-pipeline`, `deep-research full`, `deep-research systematic-review`, `academic-paper full`, and `academic-paper-reviewer full`.
- Use lower-cost settings only for bounded modes such as `citation-check`, `format-convert`, `abstract-only`, or `quick`.
- Keep `shared/`, `scripts/`, and `docs/` accessible from the active workspace; many prompts reference these files by repo-relative path.
- Use `AGENTS.md` as the Codex routing and project-instruction source of truth.

## Codex Agent Notes

The repository exposes selected downstream agent prompts in `agents/` as symlinks to their canonical source files:

- `synthesis_agent`
- `research_architect_agent`
- `report_compiler_agent`

These files are Codex-readable prompt assets, not a separate model-routing layer. The active Codex session decides model and reasoning effort.

## Long-Running Session Management

Full ARS runs are human-in-the-loop and often span hours or days. Every completed stage requires user confirmation before advancing.

When `ARS_PASSPORT_RESET=1` is set, FULL checkpoints can emit Material Passport reset-boundary entries. A later session can resume with:

```text
resume_from_passport=<hash> [stage=<n>] [mode=<m>]
```

The resume command identifies a boundary hash and optional stage/mode overrides. Passport file discovery is handled by the surrounding workspace convention, normally `./passports/<slug>/` or a matching `./material_passport*.yaml`.

Reset is useful when:

- the prior session accumulated large context that the next stage does not need;
- the run is a systematic review with clean stage boundaries;
- a fresh session is cheaper and clearer than carrying all previous dialogue.

Continuation is still better when:

- the whole task is short;
- the user wants a live Socratic branch to stay in context;
- the Material Passport does not capture a key in-session decision.

## Literature Corpus Cost

When the Material Passport carries non-empty `literature_corpus[]`, Phase 1 corpus screening scales with corpus size:

| Corpus size | Step 1 pre-screening per consumer |
|---|---:|
| Empty / absent | 0 |
| ~50 entries | +~3-5K input + ~1-2K output |
| ~200 entries | +~10-15K input + ~3-5K output |
| ~500 entries | +~25-40K input + ~8-12K output |

Large libraries should be trimmed before passport generation when possible.

## Cross-Model Audit Wrapper

`scripts/run_codex_audit.sh` dispatches a separate Codex CLI process for selected audit workflows. It requires:

- authenticated Codex CLI or `OPENAI_API_KEY`;
- `git`, `jq`, and `python3`;
- Bash 4+;
- a working directory inside the ARS repository.

The wrapper writes audit artifacts to its output directory and does not mutate the Material Passport directly. See `docs/design/2026-04-30-ars-v3.6.7-step-6-orchestrator-hooks-spec.md` for the full contract.
