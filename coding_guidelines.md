# Coding Guidelines

- PEP‑8 via **ruff**; 120‑char line limit; full type hints.
- Pure logic in `core/` (no Streamlit imports there).
- Keep functions ≤40 lines; prefer small helpers.
- Tests mirror module paths (`tests/core/test_*.py`).
- Conventional commits: `feat: …`, `fix: …` (reference task ID).
- CI runs **ruff** + **pytest** on Windows & Linux.
