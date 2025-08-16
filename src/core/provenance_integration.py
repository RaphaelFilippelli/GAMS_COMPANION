"""
Provenance integration utilities for T-004 implementation.
Connects provenance JSON generation with Excel metadata embedding.
"""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Any

from .provenance import build_run_meta, write_run_json


def load_provenance_from_run_dir(run_dir: Path) -> Optional[Dict[str, Any]]:
    """
    Load provenance data from run.json in the specified directory.
    
    Args:
        run_dir: Directory containing run.json file
        
    Returns:
        Dictionary with provenance data or None if not found/readable
    """
    run_json_path = run_dir / "run.json"
    
    if not run_json_path.exists():
        return None
        
    try:
        return json.loads(run_json_path.read_text(encoding="utf-8"))
    except Exception:
        return None


def create_excel_metadata(
    provenance_data: Optional[Dict[str, Any]] = None,
    run_id: Optional[str] = None,
    gdx_file: Optional[str] = None,
    units: Optional[Dict[str, str]] = None,
    symbols_count: Optional[int] = None,
    symbols_with_data: Optional[int] = None,
    duration_seconds: Optional[float] = None,
    additional_meta: Optional[Dict[str, Any]] = None
) -> Dict[str, str]:
    """
    Create comprehensive metadata dictionary for Excel export.
    
    Combines provenance data from run.json with UI/export specific metadata.
    
    Args:
        provenance_data: Data loaded from run.json
        run_id: UI run identifier
        gdx_file: Name of GDX file
        units: Units applied to symbols
        symbols_count: Total number of symbols
        symbols_with_data: Number of symbols with actual data
        duration_seconds: Run duration in seconds
        additional_meta: Any additional metadata fields
        
    Returns:
        Dictionary suitable for Excel metadata sheet
    """
    meta = {}
    
    # Add provenance data with prefix for clarity
    if provenance_data:
        meta.update({
            "provenance_run_id": provenance_data.get("run_id"),
            "provenance_timestamp": provenance_data.get("timestamp"),
            "model_hash": provenance_data.get("model_hash"),
            "main_file": provenance_data.get("main_file"),
            "gams_options": str(provenance_data.get("options", {})),
            "scenario_id": provenance_data.get("scenario_id") or "None",
            "patch_hash": provenance_data.get("patch_hash") or "None",
            "git_commit": provenance_data.get("commit") or "None",
            "gams_version": provenance_data.get("gams_version") or "None"
        })
    
    # Add UI/export specific metadata
    if run_id:
        meta["ui_run_id"] = run_id
    
    if gdx_file:
        meta["gdx_file"] = gdx_file
        
    if units:
        meta["units_applied"] = ", ".join(f"{k}={v}" for k, v in units.items())
    else:
        meta["units_applied"] = "None"
        
    if symbols_count is not None:
        meta["symbols_count"] = str(symbols_count)
        
    if symbols_with_data is not None:
        meta["symbols_with_data"] = str(symbols_with_data)
        
    if duration_seconds is not None:
        meta["duration_seconds"] = f"{duration_seconds:.1f}"
    
    # Always include export timestamp
    meta["export_timestamp"] = datetime.now().isoformat()
    
    # Add any additional metadata
    if additional_meta:
        meta.update({k: str(v) for k, v in additional_meta.items()})
    
    return meta


def enhance_excel_with_provenance(
    excel_export_func,
    run_dir: Optional[Path] = None,
    **kwargs
) -> Path:
    """
    Wrapper around excel export function that automatically includes provenance data.
    
    Args:
        excel_export_func: Function to call for Excel export (export_excel)
        run_dir: Directory containing run.json (optional)
        **kwargs: Arguments passed to excel_export_func
        
    Returns:
        Path to created Excel file
    """
    # Load provenance data if run_dir provided
    provenance_data = None
    if run_dir:
        provenance_data = load_provenance_from_run_dir(run_dir)
    
    # Get existing meta or create new
    existing_meta = kwargs.get("meta", {})
    
    # Create enhanced metadata
    enhanced_meta = create_excel_metadata(
        provenance_data=provenance_data,
        additional_meta=existing_meta
    )
    
    # Update kwargs with enhanced metadata
    kwargs["meta"] = enhanced_meta
    
    # Call the export function
    return excel_export_func(**kwargs)


def get_provenance_summary(run_dir: Path) -> Dict[str, str]:
    """
    Get a summary of provenance information for display purposes.
    
    Args:
        run_dir: Directory containing run.json
        
    Returns:
        Dictionary with formatted provenance summary
    """
    provenance_data = load_provenance_from_run_dir(run_dir)
    
    if not provenance_data:
        return {"status": "No provenance data available"}
    
    summary = {
        "Run ID": provenance_data.get("run_id", "Unknown"),
        "Timestamp": provenance_data.get("timestamp", "Unknown"),
        "Model Hash": provenance_data.get("model_hash", "Unknown")[:16] + "..." if provenance_data.get("model_hash") else "Unknown",
        "Main File": provenance_data.get("main_file", "Unknown"),
        "Options": str(provenance_data.get("options", {})),
        "Scenario": provenance_data.get("scenario_id") or "None"
    }
    
    return summary


def create_provenance_for_sync_run(
    work_dir: str,
    main_file: str,
    options: Optional[Dict[str, Any]] = None,
    output_dir: Optional[Path] = None
) -> Optional[Dict[str, Any]]:
    """
    Create provenance data for sync runs that don't automatically generate run.json.
    
    Args:
        work_dir: Model working directory
        main_file: Main GAMS file
        options: GAMS options used
        output_dir: Directory to write run.json (optional)
        
    Returns:
        Provenance metadata dictionary
    """
    try:
        meta = build_run_meta(
            work_dir=work_dir,
            main_file=main_file,
            options=options or {},
            scenario_id="sync_run"
        )
        
        if output_dir:
            write_run_json(output_dir, meta)
        
        return meta
        
    except Exception:
        return None