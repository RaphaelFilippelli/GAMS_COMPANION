# Streamlit MVP — Specification

## Goals
- **Edit → Run → Excel** in ≤3 clicks.

## Pages
- **Home**: description, links to docs.
- **Edit & Run**: symbol selector, inputs, "Run GAMS", live log tail.
- **Results**: Download Excel, quick Plotly charts, report preview stub.

## Widgets
- Scalar/0‑d parameter → number input.
- Set → multi‑select.
- Equation → read‑only (editing in v2).
- "Run GAMS" → calls `run_gams()` in a background thread, shows spinner.

## Deployment
- Local: `streamlit run src/app/main.py`.
