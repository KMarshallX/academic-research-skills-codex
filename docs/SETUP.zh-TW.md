# ARS Codex 設定

Academic Research Skills 是 Codex-only skills bundle。若只需要 Markdown 輸出，最低需求是可用的本機 Codex 環境，以及這個 repository 的完整 checkout。

## 最小可行設定

1. 依你的本機 Codex distribution 安裝並登入 Codex。
2. 如果你的 Codex 設定使用 API key，請確認 `OPENAI_API_KEY` 可用。
3. Clone 這個 repository：

```bash
git clone https://github.com/Imbad0202/academic-research-skills-codex.git ~/academic-research-skills-codex
```

4. 依你的 Codex skills 目錄設定，用 symlink 或 copy 暴露四個 skill roots：

```text
deep-research/SKILL.md
academic-paper/SKILL.md
academic-paper-reviewer/SKILL.md
academic-pipeline/SKILL.md
```

請保留 repository 根目錄。Skills 會引用 `shared/`、`scripts/`、`docs/` 與 `MODE_REGISTRY.md`。

## 安裝形狀

Codex 透過 `SKILL.md` entrypoint 探索 skills。這個 repo 包含四個獨立 skills，不是一個巢狀 skill：

- `deep-research`
- `academic-paper`
- `academic-paper-reviewer`
- `academic-pipeline`

不要把整個 repository 當成單一 skill name 底下的巢狀資料夾。應直接暴露四個 skill root，同時保留 root-level support files。

## Symlink 安裝

單機使用且希望 `git pull` 更新時，使用 symlink：

```bash
git clone https://github.com/Imbad0202/academic-research-skills-codex.git ~/academic-research-skills-codex
mkdir -p <codex-skills-dir>
ln -s ~/academic-research-skills-codex/deep-research <codex-skills-dir>/deep-research
ln -s ~/academic-research-skills-codex/academic-paper <codex-skills-dir>/academic-paper
ln -s ~/academic-research-skills-codex/academic-paper-reviewer <codex-skills-dir>/academic-paper-reviewer
ln -s ~/academic-research-skills-codex/academic-pipeline <codex-skills-dir>/academic-pipeline
```

如果你的 skills 目錄會跨機器同步，請使用 copy，因為絕對路徑 symlink 可能失效。

## Copy 安裝

如果 symlink 不適用，使用 copies：

```bash
git clone https://github.com/Imbad0202/academic-research-skills-codex.git ~/academic-research-skills-codex
mkdir -p <codex-skills-dir>
cp -R ~/academic-research-skills-codex/deep-research <codex-skills-dir>/deep-research
cp -R ~/academic-research-skills-codex/academic-paper <codex-skills-dir>/academic-paper
cp -R ~/academic-research-skills-codex/academic-paper-reviewer <codex-skills-dir>/academic-paper-reviewer
cp -R ~/academic-research-skills-codex/academic-pipeline <codex-skills-dir>/academic-pipeline
```

Copy 安裝仍建議保留完整 repo clone，供 shared references、validators、adapters 與 docs 使用。若你的 Codex runtime 無法從 copied skill folders 解析 repo-root references，請改用 symlink 或完整 workspace checkout。

## 選用 DOCX 輸出

若要直接產出 `.docx`，需要安裝 [Pandoc](https://pandoc.org/)。如果沒有 Pandoc，formatter 會退回 Markdown 加 DOCX 轉換說明。

```bash
# macOS
brew install pandoc

# Linux (Debian/Ubuntu)
sudo apt-get install pandoc

# Windows
# 從 https://pandoc.org/installing.html 下載
```

直接產出 `.docx` 需要 Pandoc，PDF 需要 `tectonic`。

## 選用 LaTeX / PDF 輸出

PDF 輸出需要 [tectonic](https://tectonic-typesetting.github.io/) 與適當字型：

- Times New Roman
- Source Han Serif TC VF / Noto Serif TC
- Courier New

Markdown 輸出與 DOCX 轉換說明不需要這些工具。

## Material Passport Corpus Adapters

選用的 Material Passport `literature_corpus[]` 欄位可在 ARS session 前用 `scripts/adapters/` 的 reference adapters 產生：

```bash
pip install -r requirements-dev.txt
python scripts/adapters/folder_scan.py --input /path/to/pdfs --passport passport.yaml --rejection-log rejection_log.yaml
python scripts/adapters/zotero.py --input my-zotero-export.json --passport passport.yaml --rejection-log rejection_log.yaml
python scripts/adapters/obsidian.py --input ~/Obsidian/LitNotes --passport passport.yaml --rejection-log rejection_log.yaml
```

Adapter contract 請見 [../academic-pipeline/references/adapters/overview.md](../academic-pipeline/references/adapters/overview.md)。

## 選用環境旗標

所有 flags 預設關閉：

| Flag | 用途 |
|---|---|
| `ARS_CROSS_MODEL` | 在本機 runtime 已設定時啟用選用 cross-model verification。 |
| `ARS_SOCRATIC_READING_PROBE=1` | 啟用 Socratic reading-check probe layer。 |
| `ARS_PASSPORT_RESET=1` | 在 FULL checkpoints 寫入 Material Passport reset-boundary entries。 |
| `ARS_CROSS_MODEL_SAMPLE_INTERVAL` | advisory cross-model integrity checks 的 sampling interval。 |

## 驗證

Packaging 變更後執行：

```bash
python3 scripts/check_codex_packaging.py
python3 scripts/check_version_consistency.py
python3 scripts/check_spec_consistency.py
python3 scripts/check_data_access_level.py
python3 scripts/check_task_type.py
```
