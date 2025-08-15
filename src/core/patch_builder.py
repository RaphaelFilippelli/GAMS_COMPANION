from __future__ import annotations
import pandas as pd
from pathlib import Path
from typing import Dict, Any

def _import_transfer():
    """Import GAMS Transfer API with error handling."""
    try:
        from gams import transfer as gt  # type: ignore
        return gt
    except Exception as e:
        raise ImportError("GAMS Transfer API not available. Ensure a recent GAMS is installed.") from e

def build_patch_gdx(edits: Dict[str, Any], scenario_dir: Path, output_path: str | Path) -> Path:
    """
    Build a patch.gdx file from scenario edits.
    
    Args:
        edits: Dictionary containing scalars, parameters, and sets edits
        scenario_dir: Directory where the scenario file is located (for relative CSV paths)
        output_path: Path where to write the patch.gdx file
    
    Returns:
        Path to the created patch.gdx file
    """
    gt = _import_transfer()
    output_path = Path(output_path)
    
    database = gt.Container()
    
    # First, create any sets that will be needed as domains
    created_sets = {}
    
    # Process sets first so they can be used as domains
    if "sets" in edits:
        for set_name, set_edits in edits["sets"].items():
            if "add" in set_edits and set_edits["add"]:
                # Create the set
                gams_set = gt.Set(database, set_name)
                # Set records as simple list of strings
                gams_set.setRecords(set_edits["add"])
                created_sets[set_name] = gams_set
                print(f"Created set {set_name} with {len(set_edits['add'])} elements")
    
    # Process scalars (0-dimensional parameters)
    if "scalars" in edits:
        for scalar_name, value in edits["scalars"].items():
            scalar = gt.Parameter(database, scalar_name)
            scalar.setRecords([value])
    
    # Process parameters (including CSV files)
    if "parameters" in edits:
        for param_name, param_data in edits["parameters"].items():
            if isinstance(param_data, str) and param_data.endswith('.csv'):
                # Load CSV parameter properly
                csv_path = scenario_dir / param_data
                if not csv_path.exists():
                    raise FileNotFoundError(f"CSV file not found: {csv_path}")
                
                df = pd.read_csv(csv_path)
                
                # Determine parameter structure
                if 'value' in df.columns:
                    # Standard format: key columns + value column
                    value_col = 'value'
                    key_cols = [col for col in df.columns if col != 'value' and col != 'text']
                else:
                    # Assume last column is value
                    value_col = df.columns[-1]
                    key_cols = list(df.columns[:-1])
                
                if len(key_cols) == 0:
                    # Scalar parameter from CSV
                    param = gt.Parameter(database, param_name)
                    param.setRecords([df[value_col].iloc[0]])
                else:
                    # Multi-dimensional parameter
                    # For toy model compatibility, create sets with standard names
                    domains = []
                    set_names = ['i', 'j', 'k', 'l']  # Standard GAMS set names
                    
                    for i, key_col in enumerate(key_cols):
                        set_name = set_names[i] if i < len(set_names) else f"set{i}"
                        
                        if set_name not in created_sets:
                            # Create set from CSV data
                            unique_values = df[key_col].unique().tolist()
                            implicit_set = gt.Set(database, set_name)
                            implicit_set.setRecords(unique_values)
                            created_sets[set_name] = implicit_set
                            print(f"Created set {set_name} with values: {unique_values}")
                        domains.append(created_sets[set_name])
                    
                    # Create parameter with proper domains
                    param = gt.Parameter(database, param_name, domain=domains)
                    
                    # Format data for setRecords - must match domain order
                    records_data = []
                    for _, row in df.iterrows():
                        record = tuple(str(row[col]) for col in key_cols) + (row[value_col],)
                        records_data.append(record)
                    
                    param.setRecords(records_data)
                    print(f"Created parameter {param_name} with {len(records_data)} records")
            else:
                # Direct parameter value (scalar)
                param = gt.Parameter(database, param_name)
                param.setRecords([param_data])
    
    # Write the patch.gdx
    database.write(str(output_path))
    return output_path

def get_patch_info(patch_path: Path) -> Dict[str, Any]:
    """
    Get information about symbols in a patch.gdx file.
    
    Args:
        patch_path: Path to the patch.gdx file
    
    Returns:
        Dictionary with patch information including symbol list and hash
    """
    gt = _import_transfer()
    
    database = gt.Container()
    database.read(str(patch_path))
    
    symbols = []
    for symbol_name in database.data.keys():
        symbols.append(symbol_name)
    
    # Calculate hash of the patch file
    import hashlib
    with open(patch_path, 'rb') as f:
        patch_hash = hashlib.sha256(f.read()).hexdigest()
    
    return {
        "symbols": sorted(symbols),
        "hash": patch_hash
    }