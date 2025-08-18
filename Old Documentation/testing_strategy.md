# Testing Strategy

## Pyramid
- **Unit** (fast): core utilities (`gdx_io`, parsers).
- **Integration** (medium): `run -> gdx -> export` with a tiny toy model.
- **Golden** (slow): compare outputs vs. known-good artifacts (hash or tolerance).

## Key Tests
1. **Round‑trip**: write_gdx → read_gdx preserves values & UEL order.
2. **Patch overlay**: scenario edits override only targeted symbols.
3. **Compilation**: `--dry-run` compiles without solve (use `$exit` pre-solve).
4. **Results schema**: all expected tables/columns exist; non-empty after a run.
5. **Regression**: load previous `runs/<id>/raw.gdx` and ensure metrics unchanged.

## Tooling
- `pytest -q` + `coverage` (fail under 90% for `core/`).
- Property-based tests for random UELs with `hypothesis` (optional).
