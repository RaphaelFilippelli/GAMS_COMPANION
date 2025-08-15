# Agents 2.0 — Autonomous Workflow Manual

This upgrades `agents.md` with a multi‑agent flow so Codex can operate more independently.

## Roles
1. **Planner** — reads backlog + specs, writes a concrete plan with subtasks and acceptance criteria.
2. **Implementer** — writes/edits code and tests to satisfy the plan.
3. **Reviewer** — runs lint/tests, does static review, and proposes fixes.
4. **Runner** — executes end‑to‑end smoke tests via CLI and publishes artifacts in `runs/`.
5. **Documenter** — updates docs and changelog, ensures examples stay correct.

Each cycle must start with **Planner** and end with **Runner** → **Documenter**.

## Process (per task)
1. Planner reads specs and creates a file `./.agent/plan_<task>.md` with:
   - scope, design notes, edge cases
   - *explicit acceptance criteria* and *definition of done*
2. Implementer commits code + tests.
3. Reviewer runs: `ruff check .` and `pytest -q` and updates the plan file with the status.
4. Runner executes: `python -m gams_helper run-scenario --dry-run`, then a real run, and stores artifacts.
5. Documenter updates relevant docs and closes the task in `tasks_backlog.md`.

## Guardrails
- **Always** open `agents.md`, `agents_v2.md`, and related specs before acting.
- Do not push code that fails CI or reduces test coverage for core modules.
- Keep feature flags behind config to avoid breaking user workflows.
