
# LLM KPI FEASIBILITY (short note)

**Feasible** with a pipeline:
1) Parse `*.gms` symbols/equations to a structured graph.
2) Inspect latest run (`raw.gdx`/`results.duckdb`) to see populated symbols & dims.
3) Heuristics + prompt LLM with the structured context to propose KPIs (objective(s), flows, costs, emissions, binding constraints via marginals).
4) Human confirm → persist `docs/kpis.yaml`.

Caveats: large models (prompt size), ambiguous names, hidden objectives in includes. Mitigate with chunked parsing and a validation pass.
