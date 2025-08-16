from pathlib import Path
import pandas as pd
from src.core.gdx_io_merg import export_excel

def test_export_excel_with_meta_and_units(tmp_path: Path):
    values = {
        "Foo": pd.DataFrame([{"key1":"A","value":1.23},{"key1":"B","value":4.56}]),
        "Bar": pd.DataFrame([{"key1":"A","key2":"X","value":7.89}]),
    }
    out = tmp_path / "out.xlsx"
    export_excel(values, out, units={"Foo":"kg"}, meta={"run_id":"TEST123","note":"hello"})
    assert out.exists()
