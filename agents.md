# Agents — Operating Manual  (read me first)

Welcome, Codex/Claude 👋 You are the lead engineer(s) on the **GAMS‑Companion App**.

Your job is to read the docs below, pick tasks from *tasks_backlog.md*, write code and tests, and keep the build green.

## Documentation map
| Purpose | File |
|--------|------|
| System architecture & layout | architecture.md |
| How we talk to GAMS (run, read/write GDX) | gams_integration.md |
| I/O specs for GDX helper | gdx_io_spec.md |
| Specs for model runner | model_runner_spec.md |
| Specs for symbol indexer | symbol_indexer_spec.md |
| MVP Streamlit UI spec | ui_mvp_spec.md |
| Coding conventions & CI rules | coding_guidelines.md |
| Task backlog & priorities | tasks_backlog.md |

## Workflow
1. Open this file and all linked specs above.
2. Pick the top‑priority OPEN task in *tasks_backlog.md*.
3. Implement code under **`src/`**; tests under **`tests/`**.
4. Run `ruff check .` and `pytest -q` locally.
5. When all pass, mark the task **DONE** in *tasks_backlog.md* and commit.

## Environment
- `GAMS_HOME` (default: `C:\GAMS\44`) — override in `.env` if needed.
- `APP_DATA` default: `./runs`.
- `PYTHONPATH` includes `./src` (activate your venv).

## Regeneration
If any spec changes, re‑read it before continuing work.
