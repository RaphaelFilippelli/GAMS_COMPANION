from pathlib import Path
import pandas as pd
import duckdb
from src.core.gdx_io import to_duckdb

def test_to_duckdb_schema(tmp_path: Path):
    values = {"Foo": pd.DataFrame([{"key1":"A","value":1.0},{"key1":"B","value":2.0}])}
    marginals = {"Baz": pd.DataFrame([{"key1":"A","marginal":0.5}])}
    kinds = {"Foo":"parameter","Baz":"equation"}
    db = tmp_path / "out.duckdb"
    to_duckdb(values, db, symbol_marginals=marginals, kinds=kinds, run_meta={"run_id":"R1"})
    con = duckdb.connect(str(db))
    assert con.execute("select count(*) from symbol_values").fetchone()[0] == 2
    assert con.execute("select count(*) from symbol_marginals").fetchone()[0] == 1
    assert con.execute("select count(*) from meta_run").fetchone()[0] == 1
    con.close()
