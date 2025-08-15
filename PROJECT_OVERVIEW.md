# GAMS‑Companion App — Project Overview

## Purpose
A friendly layer around an existing **GAMS** model so researchers can edit inputs, run scenarios, and export ready‑to‑use results (Excel, DuckDB, plots, reports).

## Components
```
src/
├─ core/ (env.py, model_runner.py, gdx_io.py)
├─ app/  (Streamlit UI)
├─ cli.py (Typer CLI)
tests/
docs/
runs/
```
## Setup (Windows)
1) Install Python 3.12.  
2) Create venv: `python -m venv .venv` → activate.  
3) `pip install -r requirements.txt`.  
4) Ensure `GAMS_HOME` is set (defaults to `C:\GAMS\44`).  
5) UI: `streamlit run src/app/main.py`.

## Workflow
- Tasks live in `tasks_backlog.md`.  
- Follow `agents.md` (or `agents_v2.md`) to work autonomously.
