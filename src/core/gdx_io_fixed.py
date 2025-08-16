"""
Properly structured GDX I/O following GAMS Python API v49 documentation.
Separates Control API and Transfer API usage correctly.
"""
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


def _import_control():
    """Import GAMS Control API with proper error handling"""
    try:
        from gams import GamsWorkspace  # type: ignore
        return GamsWorkspace
    except ImportError as e:
        raise ImportError(
            "GAMS Control API not available. Ensure GAMS is installed and "
            "gamsapi[control] package is available."
        ) from e


def _tidy_df_from_transfer_symbol(symbol) -> Tuple[pd.DataFrame, Optional[pd.DataFrame], str]:
    """Convert Transfer API symbol to tidy DataFrame format"""
    # Transfer API symbols have .records as pandas DataFrame already
    records = symbol.records
    dim = symbol.dimension
    key_cols = [f"key{i+1}" for i in range(dim)]
    
    if hasattr(symbol, 'type'):
        symbol_type = symbol.type.lower()
    else:
        symbol_type = type(symbol).__name__.lower()
    
    if "parameter" in symbol_type:
        kind = "parameter"
        # Records already in correct format for Transfer API
        df_val = records.copy()
        # Rename domain columns to key1, key2, etc.
        domain_cols = [col for col in df_val.columns if col not in ['value', 'text']]
        rename_dict = {col: f"key{i+1}" for i, col in enumerate(domain_cols)}
        df_val.rename(columns=rename_dict, inplace=True)
        return df_val, None, kind
        
    elif "set" in symbol_type:
        kind = "set"
        df_val = records.copy()
        # Add value column for sets
        df_val['value'] = 1.0
        # Rename domain columns
        domain_cols = [col for col in df_val.columns if col not in ['value', 'element_text']]
        rename_dict = {col: f"key{i+1}" for i, col in enumerate(domain_cols)}
        df_val.rename(columns=rename_dict, inplace=True)
        return df_val, None, kind
        
    elif "variable" in symbol_type:
        kind = "variable"
        df_val = records.copy()
        # Separate value and marginal
        df_marg = df_val.copy()
        # Rename domain columns
        domain_cols = [col for col in df_val.columns if col not in ['level', 'marginal', 'lower', 'upper', 'scale']]
        rename_dict = {col: f"key{i+1}" for i, col in enumerate(domain_cols)}
        df_val.rename(columns=rename_dict, inplace=True)
        df_marg.rename(columns=rename_dict, inplace=True)
        
        # Set value column to level for variables
        if 'level' in df_val.columns:
            df_val['value'] = df_val['level']
        else:
            df_val['value'] = 0.0
            
        return df_val, df_marg, kind
        
    elif "equation" in symbol_type:
        kind = "equation"
        df_val = records.copy()
        df_marg = df_val.copy()
        # Rename domain columns
        domain_cols = [col for col in df_val.columns if col not in ['level', 'marginal', 'lower', 'upper', 'scale']]
        rename_dict = {col: f"key{i+1}" for i, col in enumerate(domain_cols)}
        df_val.rename(columns=rename_dict, inplace=True)
        df_marg.rename(columns=rename_dict, inplace=True)
        
        # Set value column to level for equations
        if 'level' in df_val.columns:
            df_val['value'] = df_val['level']
        else:
            df_val['value'] = 0.0
            
        return df_val, df_marg, kind
        
    else:
        kind = "unknown"
        df_val = records.copy()
        if 'value' not in df_val.columns:
            df_val['value'] = 0.0
        # Rename domain columns
        domain_cols = [col for col in df_val.columns if col != 'value']
        rename_dict = {col: f"key{i+1}" for i, col in enumerate(domain_cols)}
        df_val.rename(columns=rename_dict, inplace=True)
        return df_val, None, kind


def read_gdx_transfer(gdx_path: str | Path, symbols: Optional[List[str]] = None) -> Dict[str, pd.DataFrame]:
    """
    Read GDX file using GAMS Transfer API (recommended for data operations).
    
    This is the proper way to read GDX files for data manipulation according to
    GAMS Python API v49 documentation.
    """
    vals, _, _ = read_gdx_transfer_full(gdx_path, symbols)
    return vals


def read_gdx_transfer_full(gdx_path: str | Path, symbols: Optional[List[str]] = None) -> Tuple[Dict[str, pd.DataFrame], Dict[str, pd.DataFrame], Dict[str, str]]:
    """
    Read GDX file using GAMS Transfer API with full symbol information.
    
    Following GAMS Python API v49 documentation patterns.
    """
    gt = _import_transfer()
    
    gdx_path = Path(gdx_path)
    if not gdx_path.exists():
        raise FileNotFoundError(f"GDX file not found: {gdx_path}")
    
    try:
        # Use Container - this is the correct Transfer API pattern
        container = gt.Container(str(gdx_path))
        
        values: Dict[str, pd.DataFrame] = {}
        marginals: Dict[str, pd.DataFrame] = {}
        kinds: Dict[str, str] = {}
        
        # Iterate through symbols in container
        for symbol_name, symbol in container.data.items():
            if symbols and symbol_name not in symbols:
                continue
                
            try:
                df_val, df_marg, kind = _tidy_df_from_transfer_symbol(symbol)
                values[symbol_name] = df_val
                kinds[symbol_name] = kind
                if df_marg is not None:
                    marginals[symbol_name] = df_marg
            except Exception as e:
                print(f"Warning: Failed to process symbol '{symbol_name}': {e}")
                continue
                
        return values, marginals, kinds
        
    except Exception as e:
        raise RuntimeError(f"Failed to read GDX file {gdx_path} using Transfer API: {e}") from e


def read_gdx_control(gdx_path: str | Path, symbols: Optional[List[str]] = None, system_directory: Optional[str] = None) -> Dict[str, pd.DataFrame]:
    """
    Read GDX file using GAMS Control API (for integration with GAMS execution).
    
    Use this when you need to integrate with GamsWorkspace/GamsJob workflows.
    """
    vals, _, _ = read_gdx_control_full(gdx_path, symbols, system_directory)
    return vals


def read_gdx_control_full(gdx_path: str | Path, symbols: Optional[List[str]] = None, system_directory: Optional[str] = None) -> Tuple[Dict[str, pd.DataFrame], Dict[str, pd.DataFrame], Dict[str, str]]:
    """
    Read GDX file using GAMS Control API with full symbol information.
    
    Following GAMS Python API v49 Control API patterns.
    """
    GamsWorkspace = _import_control()
    
    gdx_path = Path(gdx_path)
    if not gdx_path.exists():
        raise FileNotFoundError(f"GDX file not found: {gdx_path}")
    
    try:
        # Create workspace with proper system directory
        kwargs = {}
        if system_directory:
            kwargs["system_directory"] = system_directory
        ws = GamsWorkspace(**kwargs)
        
        # Use Control API pattern
        db = ws.add_database_from_gdx(str(gdx_path))
        
        values: Dict[str, pd.DataFrame] = {}
        marginals: Dict[str, pd.DataFrame] = {}
        kinds: Dict[str, str] = {}
        
        # Iterate through symbols in database
        for symbol in db:
            symbol_name = symbol.name
            if symbols and symbol_name not in symbols:
                continue
                
            try:
                df_val, df_marg, kind = _tidy_df_from_control_symbol(symbol)
                values[symbol_name] = df_val
                kinds[symbol_name] = kind
                if df_marg is not None:
                    marginals[symbol_name] = df_marg
            except Exception as e:
                print(f"Warning: Failed to process symbol '{symbol_name}': {e}")
                continue
                
        return values, marginals, kinds
        
    except Exception as e:
        raise RuntimeError(f"Failed to read GDX file {gdx_path} using Control API: {e}") from e


def _tidy_df_from_control_symbol(symbol) -> Tuple[pd.DataFrame, Optional[pd.DataFrame], str]:
    """Convert Control API symbol to tidy DataFrame format"""
    # This is the original logic but properly structured
    dim = symbol.dimension
    key_cols = [f"key{i+1}" for i in range(dim)]
    
    def keys_dict(rec):
        return {f"key{i+1}": rec.keys[i] for i in range(dim)}
    
    rows_val = []
    rows_marg = []
    cls_name = symbol.__class__.__name__.lower()
    
    if "parameter" in cls_name:
        kind = "parameter"
        has_text = hasattr(next(iter(symbol)), "text") if len(symbol) else False
        for rec in symbol:
            d = keys_dict(rec)
            d["value"] = getattr(rec, "value", None)
            if has_text:
                d["text"] = getattr(rec, "text", None)
            rows_val.append(d)
        df_val = pd.DataFrame(rows_val) if rows_val else pd.DataFrame(columns=key_cols + ["value"] + (["text"] if has_text else []))
        return df_val, None, kind
        
    if "set" in cls_name:
        kind = "set"
        for rec in symbol:
            d = keys_dict(rec)
            d["value"] = 1.0
            rows_val.append(d)
        df_val = pd.DataFrame(rows_val) if rows_val else pd.DataFrame(columns=key_cols + ["value"])
        return df_val, None, kind
        
    if "variable" in cls_name:
        kind = "variable"
        for rec in symbol:
            d = keys_dict(rec)
            d["value"] = getattr(rec, "level", None)
            rows_val.append(d)
            rows_marg.append({**d, "marginal": getattr(rec, "marginal", None)})
        df_val = pd.DataFrame(rows_val) if rows_val else pd.DataFrame(columns=key_cols + ["value"])
        df_marg = pd.DataFrame(rows_marg) if rows_marg else None
        return df_val, df_marg, kind
        
    if "equation" in cls_name:
        kind = "equation"
        for rec in symbol:
            d = keys_dict(rec)
            d["value"] = getattr(rec, "level", None)
            rows_val.append(d)
            rows_marg.append({**d, "marginal": getattr(rec, "marginal", None)})
        df_val = pd.DataFrame(rows_val) if rows_val else pd.DataFrame(columns=key_cols + ["value"])
        df_marg = pd.DataFrame(rows_marg) if rows_marg else None
        return df_val, df_marg, kind
        
    kind = "unknown"
    for rec in symbol:
        d = keys_dict(rec)
        d["value"] = getattr(rec, "value", None)
        rows_val.append(d)
    df_val = pd.DataFrame(rows_val) if rows_val else pd.DataFrame(columns=key_cols + ["value"])
    return df_val, None, kind


# Legacy compatibility - use Transfer API by default (recommended)
def read_gdx(gdx_path: str | Path, symbols: Optional[List[str]] = None) -> Dict[str, pd.DataFrame]:
    """
    Legacy compatibility function - uses Transfer API by default.
    
    For new code, use read_gdx_transfer() or read_gdx_control() explicitly.
    """
    return read_gdx_transfer(gdx_path, symbols)


def read_gdx_full(gdx_path: str | Path, symbols: Optional[List[str]] = None) -> Tuple[Dict[str, pd.DataFrame], Dict[str, pd.DataFrame], Dict[str, str]]:
    """
    Legacy compatibility function - uses Transfer API by default.
    
    For new code, use read_gdx_transfer_full() or read_gdx_control_full() explicitly.
    """
    return read_gdx_transfer_full(gdx_path, symbols)


# Keep existing export functions unchanged
def export_excel(symbol_data: Dict[str, pd.DataFrame], xlsx_out: str | Path, units: Optional[Dict[str, str]] = None, meta: Optional[Dict[str, str]] = None) -> Path:
    import openpyxl  # type: ignore
    xlsx_out = Path(xlsx_out)
    units = units or {}
    with pd.ExcelWriter(xlsx_out, engine="openpyxl") as writer:
        if meta:
            meta_df = pd.DataFrame(list(meta.items()), columns=["key", "value"])
            meta_df.to_excel(writer, sheet_name="meta", index=False)
            ws = writer.sheets["meta"]
            ws.freeze_panes = "A2"
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
            ws = writer.sheets[sheet]
            ws.freeze_panes = "A2"
            for col in ws.columns:
                maxlen = max(len(str(c.value)) if c.value is not None else 0 for c in col)
                ws.column_dimensions[col[0].column_letter].width = min(max(10, maxlen + 2), 60)
    return xlsx_out


def _register_df(conn: duckdb.DuckDBPyConnection, df: pd.DataFrame) -> str:
    view = f"_df_{uuid.uuid4().hex}"
    try:
        conn.register(view, df)
        return view
    except Exception as e:
        # Handle MemoryView compatibility issues
        if "memoryview" in str(e).lower() or "buffer" in str(e).lower():
            # Fallback: create a copy with compatible dtypes
            df_copy = df.copy()
            # Convert object columns to string to avoid memory view issues
            for col in df_copy.columns:
                if df_copy[col].dtype == 'object':
                    df_copy[col] = df_copy[col].astype(str)
            conn.register(view, df_copy)
            return view
        else:
            raise


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
        norm.insert(0, "dim", dim)
        norm.insert(0, "kind", kind)
        norm.insert(0, "symbol", name)
        norm.insert(0, "run_id", run_id)
        view = _register_df(conn, norm)
        conn.execute(f"""
            INSERT INTO symbol_values
            (run_id, symbol, kind, dim, key1, key2, key3, key4, key5, key6, key7, value, text)
            SELECT run_id, symbol, kind, dim, key1, key2, key3, key4, key5, key6, key7, value, text
            FROM {view}
        """)
    
    # Insert marginals
    if symbol_marginals:
        for name, df in symbol_marginals.items():
            dim = sum(c.startswith("key") for c in df.columns)
            norm = _normalize(df, "marginal")
            norm.insert(0, "dim", dim)
            norm.insert(0, "symbol", name)
            norm.insert(0, "run_id", run_id)
            view = _register_df(conn, norm)
            conn.execute(f"""
                INSERT INTO symbol_marginals
                (run_id, symbol, dim, key1, key2, key3, key4, key5, key6, key7, marginal)
                SELECT run_id, symbol, dim, key1, key2, key3, key4, key5, key6, key7, marginal
                FROM {view}
            """)
    
    conn.close()
    return db_path