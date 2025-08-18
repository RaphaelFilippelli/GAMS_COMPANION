# KPI Schema (v1)

Each KPI request has:
- `name`: output column name
- `symbol`: the symbol in results (as in `symbol_values.symbol` or GDX)
- `where` (optional): filters on `key1..key7` (string or list of strings)
- `agg` (optional): `sum` (default) or `mean`

Example:
```yaml
kpis:
  - name: TotalObjective
    symbol: obj
    agg: sum
  - name: Cost_2025
    symbol: cost
    where: { key2: "2025" }
  - name: Flow_A_to_B
    symbol: flow
    where: { key1: "A", key2: "B" }
```