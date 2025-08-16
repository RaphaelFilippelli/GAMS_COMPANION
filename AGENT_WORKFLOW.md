# AGENT_WORKFLOW.md — How to Work on This Repo

## Setup
```bash
python -m venv .venv
# Windows PowerShell
. .venv\Scripts\Activate.ps1
pip install -r requirements.txt
# Point GAMS_HOME to your install (v49+), then:
#   cd %GAMS_HOME%\apifiles\Python\api_31X  (X matches your Python minor)
#   pip install .
pytest -q   # expect 1 skipped without GAMS
```

## Running the app
```bash
streamlit run src/app/main.py
# Sidebar: set Model folder (e.g., toy_model), main.gms, expected results.gdx
```

## Change workflow (small, safe, repeatable)
1. **Create a branch**: `git checkout -b feat/<topic>`
2. **Write/adjust tests** in `tests/` for your change.
3. **Implement** the smallest viable patch.
4. **Run tests**: `pytest -q` and a minimal manual run if relevant.
5. **Open a PR** using the template, summarize exactly what changed.
6. **Wait for review**; respond with follow‑up patches if needed.

## Token/context limits (practical guidance)
- Don’t paste huge files; reference exact paths and only quote the few lines you change.
- Work in **small diffs**; split large refactors into sequenced PRs.
- Persist decisions in repo docs (`docs/`) so new sessions/agents reload context from files, not chat memory.
- When you must inspect long files, summarize sections you rely on and cite line ranges.

## Guardrails checklist before merging
- [ ] Temp‑isolation preserved (no absolute paths in includes or unloads)
- [ ] Excel export leaves at least one sheet
- [ ] DuckDB export inserts via registered views + explicit columns
- [ ] LO handled as CLI arg only when using `gams.exe`
- [ ] `runs/<stamp>/` contains `.lst`, `raw.gdx`, `run.json`, `debug_paths.json`
