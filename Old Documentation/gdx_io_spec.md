# gdx_io.py — Specification

## read_gdx(path, symbols=None) → dict[str, DataFrame]
- Loads all symbols (or only those listed).
- Returns tidy DataFrames with columns: key1..keyN, value, text (if present).

## export_excel(symbol_data, xlsx_out, units: dict[str,str]|None)
- One worksheet per symbol; sheet name = symbol (≤31 chars).
- Freeze the header row; auto‑fit column widths.
- If `units` provided, append " (unit)" to header row of `value` column.

## to_duckdb(symbol_data, db_path)
- Store each DataFrame as a table in DuckDB with tidy columns.

### Tests
- Round‑trip: write → read retains values/UELs.
- Covers: scalar, 1‑d parameter, 2‑d parameter, set, variable.
