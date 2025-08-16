from __future__ import annotations
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import uuid

import duckdb  # type: ignore
import pandas as pd
from ulid import ULID  # type: ignore

def _import_transfer():
    """Import GAMS Transfer API with proper error handling"""
    try:
        from gams import transfer as gt  # type: ignore
        return gt
    except ImportError as e:
        raise ImportError(
            "GAMS Transfer API not available. Ensure GAMS is installed and "
            "gamsapi[transfer] package is available. Install with: "
            "pip install 'gamsapi[transfer]==<GAMS_VERSION>'"
        ) from e

def _tidy_df_from_symbol(sym) -> Tuple[pd.DataFrame, Optional[pd.DataFrame], str]:
    dim = sym.dimension
    key_cols = [f"key{i+1}" for i in range(dim)]
    cls_name = sym.__class__.__name__.lower()
    
    # Get records DataFrame from GAMS Transfer API
    try:
        records_df = sym.records
        if records_df is None or records_df.empty:
            # Return empty DataFrames with appropriate structure
            if "parameter" in cls_name:
                cols = key_cols + ["value"]
                if hasattr(sym, 'records') and not sym.records.empty and 'element_text' in sym.records.columns:
                    cols.append("text")
                return pd.DataFrame(columns=cols), None, "parameter"
            elif "set" in cls_name:
                return pd.DataFrame(columns=key_cols + ["value"]), None, "set"
            elif "variable" in cls_name:
                df_val = pd.DataFrame(columns=key_cols + ["value"])
                df_marg = pd.DataFrame(columns=key_cols + ["marginal"])
                return df_val, df_marg, "variable"
            elif "equation" in cls_name:
                df_val = pd.DataFrame(columns=key_cols + ["value"])
                df_marg = pd.DataFrame(columns=key_cols + ["marginal"])
                return df_val, df_marg, "equation"
            else:
                return pd.DataFrame(columns=key_cols + ["value"]), None, "unknown"
    except Exception:
        # Fallback to empty DataFrames if we can't access records
        if "parameter" in cls_name:
            return pd.DataFrame(columns=key_cols + ["value"]), None, "parameter"
        elif "set" in cls_name:
            return pd.DataFrame(columns=key_cols + ["value"]), None, "set"
        elif "variable" in cls_name:
            df_val = pd.DataFrame(columns=key_cols + ["value"])
            df_marg = pd.DataFrame(columns=key_cols + ["marginal"])
            return df_val, df_marg, "variable"
        elif "equation" in cls_name:
            df_val = pd.DataFrame(columns=key_cols + ["value"])
            df_marg = pd.DataFrame(columns=key_cols + ["marginal"])
            return df_val, df_marg, "equation"
        else:
            return pd.DataFrame(columns=key_cols + ["value"]), None, "unknown"
    
    # Process the records DataFrame based on symbol type
    if "parameter" in cls_name:
        kind = "parameter"
        df_val = records_df.copy()
        
        # Rename dimension columns to key1, key2, etc.
        dim_cols = [col for col in df_val.columns if col not in ['value', 'element_text']]
        for i, col in enumerate(dim_cols[:dim]):
            if col != f"key{i+1}":
                df_val.rename(columns={col: f"key{i+1}"}, inplace=True)
        
        # Add missing key columns
        for i in range(len(dim_cols), dim):
            df_val[f"key{i+1}"] = None
            
        # Rename element_text to text if it exists
        if 'element_text' in df_val.columns:
            df_val.rename(columns={'element_text': 'text'}, inplace=True)
            
        return df_val, None, kind
        
    elif "set" in cls_name:
        kind = "set"
        df_val = records_df.copy()
        
        # For sets, we need to add a value column (sets are binary - 1 means element is in set)
        df_val['value'] = 1.0
        
        # Rename dimension columns to key1, key2, etc.
        dim_cols = [col for col in df_val.columns if col not in ['value', 'element_text']]
        for i, col in enumerate(dim_cols[:dim]):
            if col != f"key{i+1}":
                df_val.rename(columns={col: f"key{i+1}"}, inplace=True)
                
        # Add missing key columns
        for i in range(len(dim_cols), dim):
            df_val[f"key{i+1}"] = None
            
        return df_val, None, kind
        
    elif "variable" in cls_name:
        kind = "variable"
        df = records_df.copy()
        
        # Rename dimension columns to key1, key2, etc.
        dim_cols = [col for col in df.columns if col not in ['level', 'marginal', 'lower', 'upper', 'scale']]
        for i, col in enumerate(dim_cols[:dim]):
            if col != f"key{i+1}":
                df.rename(columns={col: f"key{i+1}"}, inplace=True)
                
        # Add missing key columns
        for i in range(len(dim_cols), dim):
            df[f"key{i+1}"] = None
        
        # Create value DataFrame (level values)
        df_val = df.copy()
        df_val['value'] = df_val.get('level', None)
        value_cols = [f"key{i+1}" for i in range(dim)] + ['value']
        df_val = df_val[value_cols]
        
        # Create marginal DataFrame
        df_marg = df.copy()
        marg_cols = [f"key{i+1}" for i in range(dim)] + ['marginal']
        df_marg = df_marg[marg_cols] if 'marginal' in df_marg.columns else None
        
        return df_val, df_marg, kind
        
    elif "equation" in cls_name:
        kind = "equation"
        df = records_df.copy()
        
        # Rename dimension columns to key1, key2, etc.
        dim_cols = [col for col in df.columns if col not in ['level', 'marginal', 'lower', 'upper', 'scale']]
        for i, col in enumerate(dim_cols[:dim]):
            if col != f"key{i+1}":
                df.rename(columns={col: f"key{i+1}"}, inplace=True)
                
        # Add missing key columns
        for i in range(len(dim_cols), dim):
            df[f"key{i+1}"] = None
        
        # Create value DataFrame (level values)
        df_val = df.copy()
        df_val['value'] = df_val.get('level', None)
        value_cols = [f"key{i+1}" for i in range(dim)] + ['value']
        df_val = df_val[value_cols]
        
        # Create marginal DataFrame
        df_marg = df.copy()
        marg_cols = [f"key{i+1}" for i in range(dim)] + ['marginal']
        df_marg = df_marg[marg_cols] if 'marginal' in df_marg.columns else None
        
        return df_val, df_marg, kind
        
    else:
        # Unknown type - try to extract value column
        kind = "unknown"
        df_val = records_df.copy()
        
        # Rename dimension columns
        dim_cols = [col for col in df_val.columns if col != 'value']
        for i, col in enumerate(dim_cols[:dim]):
            if col != f"key{i+1}":
                df_val.rename(columns={col: f"key{i+1}"}, inplace=True)
                
        # Add missing key columns
        for i in range(len(dim_cols), dim):
            df_val[f"key{i+1}"] = None
            
        # Ensure value column exists
        if 'value' not in df_val.columns:
            df_val['value'] = None
            
        return df_val, None, kind

def read_gdx(gdx_path: str | Path, symbols: Optional[List[str]] = None) -> Dict[str, pd.DataFrame]:
    vals, _, _ = read_gdx_full(gdx_path, symbols)
    return vals

def read_gdx_full(gdx_path: str | Path, symbols: Optional[List[str]] = None) -> Tuple[Dict[str, pd.DataFrame], Dict[str, pd.DataFrame], Dict[str, str]]:
    """Read GDX file using GAMS Transfer API with proper error handling"""
    gt = _import_transfer()
    
    gdx_path = Path(gdx_path)
    if not gdx_path.exists():
        raise FileNotFoundError(f"GDX file not found: {gdx_path}")
    
    try:
        # Use Container (modern Transfer API pattern) instead of Workspace
        container = gt.Container()
        container.read(str(gdx_path))
        
        values: Dict[str, pd.DataFrame] = {}
        marginals: Dict[str, pd.DataFrame] = {}
        kinds: Dict[str, str] = {}
        
        for symbol_name, symbol in container.data.items():
            if symbols and symbol_name not in symbols:
                continue
                
            try:
                df_val, df_marg, kind = _tidy_df_from_symbol(symbol)
                values[symbol_name] = df_val
                kinds[symbol_name] = kind
                if df_marg is not None:
                    marginals[symbol_name] = df_marg
            except Exception as e:
                print(f"Warning: Failed to process symbol '{symbol_name}': {e}")
                continue
                
        return values, marginals, kinds
        
    except Exception as e:
        raise RuntimeError(f"Failed to read GDX file {gdx_path}: {e}") from e

def export_excel(symbol_data: Dict[str, pd.DataFrame], xlsx_out: str | Path, units: Optional[Dict[str, str]] = None, meta: Optional[Dict[str, str]] = None) -> Path:
    import openpyxl  # type: ignore
    import datetime
    xlsx_out = Path(xlsx_out); units = units or {}
    with pd.ExcelWriter(xlsx_out, engine="openpyxl") as writer:
        # Ensure at least one sheet is created to avoid openpyxl error
        if not symbol_data and not meta:
            # Create a default info sheet when no data is available
            info_df = pd.DataFrame([
                ["export_time", datetime.datetime.now().isoformat()],
                ["status", "No symbol data available"],
                ["file", str(xlsx_out)]
            ], columns=["key", "value"])
            info_df.to_excel(writer, sheet_name="info", index=False)
            ws = writer.sheets["info"]; ws.freeze_panes = "A2"
            for col in ws.columns:
                maxlen = max(len(str(c.value)) if c.value is not None else 0 for c in col)
                ws.column_dimensions[col[0].column_letter].width = min(max(12, maxlen + 2), 60)
        
        if meta:
            meta_df = pd.DataFrame(list(meta.items()), columns=["key", "value"])
            meta_df.to_excel(writer, sheet_name="meta", index=False)
            ws = writer.sheets["meta"]; ws.freeze_panes = "A2"
            for col in ws.columns:
                maxlen = max(len(str(c.value)) if c.value is not None else 0 for c in col)
                ws.column_dimensions[col[0].column_letter].width = min(max(12, maxlen + 2), 60)
        for name, df in symbol_data.items():
            df = df.copy()
            key_cols = [c for c in df.columns if c.startswith("key")]
            rest = [c for c in df.columns if c not in key_cols]
            cols = key_cols + [c for c in rest if c.startswith("value")] + [c for c in rest if c == "text"] + [c for c in rest if c not in ("value","text")]
            df = df[cols]
            unit = (units or {}).get(name)
            if unit and "value" in df.columns:
                df.rename(columns={"value": f"value ({unit})"}, inplace=True)
            sheet = name[:31]
            df.to_excel(writer, sheet_name=sheet, index=False)
            ws = writer.sheets[sheet]; ws.freeze_panes = "A2"
            for col in ws.columns:
                maxlen = max(len(str(c.value)) if c.value is not None else 0 for c in col)
                ws.column_dimensions[col[0].column_letter].width = min(max(10, maxlen + 2), 60)
    return xlsx_out

def _register_df(conn: duckdb.DuckDBPyConnection, df: pd.DataFrame) -> str:
    view = f"_df_{uuid.uuid4().hex}"
    conn.register(view, df)
    return view

def to_duckdb(symbol_values: Dict[str, pd.DataFrame], db_path: str | Path, *, symbol_marginals: Optional[Dict[str, pd.DataFrame]] = None, kinds: Optional[Dict[str, str]] = None, run_meta: Optional[Dict[str, str]] = None) -> Path:
    import datetime
    db_path = Path(db_path)
    conn = duckdb.connect(str(db_path))
    run_id = (run_meta or {}).get("run_id") or str(ULID())
    conn.execute("""CREATE TABLE IF NOT EXISTS meta_run (run_id TEXT PRIMARY KEY, timestamp TIMESTAMP, scenario_id TEXT, gams_version TEXT, model_hash TEXT, patch_hash TEXT, commit TEXT);""")
    conn.execute("""CREATE TABLE IF NOT EXISTS symbol_values (run_id TEXT, symbol TEXT, kind TEXT, dim INTEGER, key1 TEXT, key2 TEXT, key3 TEXT, key4 TEXT, key5 TEXT, key6 TEXT, key7 TEXT, value DOUBLE, text TEXT);""")
    conn.execute("""CREATE TABLE IF NOT EXISTS symbol_marginals (run_id TEXT, symbol TEXT, dim INTEGER, key1 TEXT, key2 TEXT, key3 TEXT, key4 TEXT, key5 TEXT, key6 TEXT, key7 TEXT, marginal DOUBLE);""")
    meta_row = {"run_id": run_id, "timestamp": (run_meta or {}).get("timestamp") or datetime.datetime.utcnow(), "scenario_id": (run_meta or {}).get("scenario_id"), "gams_version": (run_meta or {}).get("gams_version"), "model_hash": (run_meta or {}).get("model_hash"), "patch_hash": (run_meta or {}).get("patch_hash"), "commit": (run_meta or {}).get("commit")}
    conn.execute("INSERT OR REPLACE INTO meta_run VALUES (?, ?, ?, ?, ?, ?, ?);", list(meta_row.values()))
    def _normalize(df: pd.DataFrame, value_col: str) -> pd.DataFrame:
        df = df.copy()
        for i in range(7):
            col = f"key{i+1}"
            if col not in df.columns:
                df[col] = None
        cols = [f"key{i+1}" for i in range(7)] + [value_col]
        # Ensure 'text' column exists for values table
        if value_col == "value":
            if "text" not in df.columns:
                df["text"] = None
            cols.append("text")
        return df[cols]
    kinds = kinds or {}
    # Insert values
    for name, df in symbol_values.items():
        dim = sum(c.startswith("key") for c in df.columns)
        kind = kinds.get(name) or "unknown"
        norm = _normalize(df, "value")
        norm.insert(0, "dim", dim); norm.insert(0, "kind", kind); norm.insert(0, "symbol", name); norm.insert(0, "run_id", run_id)
        view = _register_df(conn, norm)
        conn.execute(f"""            INSERT INTO symbol_values
            (run_id, symbol, kind, dim, key1, key2, key3, key4, key5, key6, key7, value, text)
            SELECT run_id, symbol, kind, dim, key1, key2, key3, key4, key5, key6, key7, value, text
            FROM {view}
        """)
    # Insert marginals
    if symbol_marginals:
        for name, df in symbol_marginals.items():
            dim = sum(c.startswith("key") for c in df.columns)
            norm = _normalize(df, "marginal")
            norm.insert(0, "dim", dim); norm.insert(0, "symbol", name); norm.insert(0, "run_id", run_id)
            view = _register_df(conn, norm)
            conn.execute(f"""                INSERT INTO symbol_marginals
                (run_id, symbol, dim, key1, key2, key3, key4, key5, key6, key7, marginal)
                SELECT run_id, symbol, dim, key1, key2, key3, key4, key5, key6, key7, marginal
                FROM {view}
            """)
    conn.close()
    return db_path
