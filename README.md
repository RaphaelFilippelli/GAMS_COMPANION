# GAMS‑Companion App (Starter Kit)

This is a minimal, testable scaffold to run/edit a GAMS model, convert outputs, and generate publication‑ready artefacts.

## Quick start (Windows)
```powershell
# from repo root
python -m venv .venv
. .venv\Scripts\Activate.ps1
pip install -r requirements.txt

# ensure GAMS is installed and GAMS_HOME is set (defaults to C:\GAMS\44)
$env:GAMS_HOME = "C:\GAMS\44"

# run UI
streamlit run src/app/main.py
```

## CLI
```bash
python -m src.cli --help
```

See `docs/PROJECT_OVERVIEW.md` and `docs/agents.md` to orient yourself.
