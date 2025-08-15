# symbol_indexer.py — Specification

## scan_sources(files) → list[dict]
- Detect declarations of `SET(S)`, `SCALAR(S)`, `PARAMETER(S)`, `VARIABLE(S)`, `EQUATION(S)` (case‑insensitive).
- Skip lines starting with `*` or `//`.
- Follow `$include` up to depth 3 (avoid leaving project root).
- Return dictionaries: `{type, name, file, line, dim}`.

## save_index(index, path) → Path
- Save as pretty JSON.
