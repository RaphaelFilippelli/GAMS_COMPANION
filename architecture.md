# Project Architecture

```
gams‑helper/
├─ src/
│  ├─ core/               # pure‑python logic
│  │  ├─ env.py
│  │  ├─ model_runner.py
│  │  ├─ gdx_io.py
│  │  └─ __init__.py
│  ├─ app/                # Streamlit UI
│  │  └─ main.py
│  ├─ cli.py              # Typer CLI
│  └─ __init__.py
├─ tests/                 # pytest suites
├─ runs/                  # generated results (git‑ignored)
├─ docs/                  # these markdown docs
├─ requirements.txt
└─ README.md
```

## Data Flow
1) **Edit** → UI/CLI builds a **patch.gdx** from scenario edits.  
2) **Run** → `model_runner.run_gams()` compiles/solves in a temp copy.  
3) **Export** → `gdx_io` → DuckDB + Excel + plots/reports.
