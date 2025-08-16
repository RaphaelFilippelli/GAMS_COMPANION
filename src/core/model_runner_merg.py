"""
GAMS model runner following official GAMS Python API v49 documentation patterns.
Merged version combining best practices from model_runner.py and model_runner_v49.py.
Implements proper Control API usage as documented.
"""
from __future__ import annotations
import json
import os
import shutil
import tempfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

from .env import get_gams_home, validate_gams_api
from .gams_api_wrapper_merg import (
    GamsWorkspaceManager,
    GamsJobRunner, 
    GamsDatabaseManager,
    GamsApiError
)
from .provenance import build_run_meta, write_run_json


@dataclass
class RunConfig:
    """Configuration for GAMS model runs following documented patterns"""
    work_dir: str
    gms_file: str
    gdx_out: str
    options: Optional[Dict[str, Any]] = None
    keep_temp: bool = False
    system_directory: Optional[str] = None


def _copy_tree(src: Path, dst: Path) -> None:
    """Copy directory tree efficiently"""
    for p in src.rglob("*"):
        rel = p.relative_to(src)
        target = dst / rel
        if p.is_dir():
            target.mkdir(parents=True, exist_ok=True)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, target)


def _collect_artifacts(td_path: Path, out_dir: Path, gdx_out: str) -> dict:
    """Collect run artifacts (listings, GDX files) following documented patterns"""
    out_dir.mkdir(parents=True, exist_ok=True)
    copied = {"lst": None, "gdx": None}
    
    # Find listing files
    lst_candidates = sorted(td_path.glob("*.lst"), key=lambda p: p.stat().st_mtime, reverse=True)
    if lst_candidates:
        lst_dst = out_dir / lst_candidates[0].name
        shutil.copy2(lst_candidates[0], lst_dst)
        copied["lst"] = str(lst_dst)
    
    # Find GDX output
    gdx_src = td_path / gdx_out
    if gdx_src.exists():
        gdx_dst = out_dir / "raw.gdx"
        shutil.copy2(gdx_src, gdx_dst)
        copied["gdx"] = str(gdx_dst)
    
    return copied


def _run_gams_job_documented_pattern(
    workspace_mgr: GamsWorkspaceManager,
    job_runner: GamsJobRunner,
    td_path: Path, 
    main_name: str, 
    options: Optional[Dict[str, Any]]
) -> None:
    """
    Run GAMS job following documented Control API patterns.
    
    This implements the exact patterns shown in the documentation:
    1. Create workspace with proper directories
    2. Create job from file
    3. Set options using documented methods
    4. Run job with proper error handling
    """
    try:
        # Create job from file (documented pattern)
        main_file = td_path / main_name
        job = job_runner.create_job_from_file(str(main_file))
        
        # Run job with options (documented pattern)
        if options:
            # Use documented options handling
            job_runner.run_job(job, options)
        else:
            job_runner.run_job(job)
            
        print(f"GAMS job completed successfully: {job.name}")
        
    except GamsApiError as e:
        # Re-raise with context
        raise RuntimeError(f"GAMS job execution failed: {e}") from e
    except Exception as e:
        # Handle unexpected errors
        raise RuntimeError(f"Unexpected error during GAMS execution: {e}") from e


def _run_via_subprocess_fallback(td_path: Path, main_name: str, options: Optional[Dict[str, Any]]) -> None:
    """
    Fallback: run GAMS by calling gams.exe directly.
    Used when API fails due to compatibility issues.
    """
    import subprocess
    
    gams_exe = Path(get_gams_home()) / "gams.exe"
    if not gams_exe.exists():
        alt = Path(get_gams_home()) / "gams" / "gams.exe"
        gams_exe = alt if alt.exists() else gams_exe
    if not gams_exe.exists():
        raise FileNotFoundError(f"GAMS executable not found under {get_gams_home()}")

    args = [str(gams_exe), main_name]
    for k, v in (options or {}).items():
        args.append(f"{k}={v}")

    proc = subprocess.run(
        args,
        cwd=str(td_path),
        capture_output=True,
        text=True,
        shell=False,
    )
    (td_path / "_gams_stdout.txt").write_text(proc.stdout or "", encoding="utf-8")
    (td_path / "_gams_stderr.txt").write_text(proc.stderr or "", encoding="utf-8")

    if proc.returncode != 0:
        raise RuntimeError(f"gams.exe returned {proc.returncode}. See _gams_stderr.txt and listing (.lst).")


def run_gams_v49(
    work_dir: str,
    gms_file: str,
    gdx_out: str,
    options: Optional[Dict[str, Any]] = None,
    keep_temp: bool = False,
    scenario_id: Optional[str] = None,
    patch_path: Optional[str] = None,
    system_directory: Optional[str] = None,
) -> Path:
    """
    Run GAMS following official Python API v49 documentation patterns.
    
    This function implements the recommended approach from the documentation:
    1. Proper workspace management with system_directory
    2. Isolated temporary workspace
    3. Control API patterns for job execution
    4. Proper error handling and fallbacks
    5. Artifact collection and provenance tracking
    
    Args:
        work_dir: Directory containing GAMS model files
        gms_file: Main GAMS file to run
        gdx_out: Expected output GDX file name
        options: GAMS options dictionary
        keep_temp: Whether to keep temporary files for debugging
        scenario_id: Optional scenario identifier for tracking
        patch_path: Optional path to patch file
        system_directory: Optional GAMS system directory override
        
    Returns:
        Path: Path to output GDX file
        
    Raises:
        FileNotFoundError: If input files are not found
        RuntimeError: If GAMS execution fails
        GamsApiError: If API-specific issues occur
    """
    # Validate inputs
    work_dir_p = Path(work_dir).resolve()
    if not work_dir_p.exists():
        raise FileNotFoundError(f"Work dir not found: {work_dir_p}")

    main_name = Path(gms_file).name
    
    # Create isolated temporary workspace (documented best practice)
    if keep_temp:
        td_path = Path(tempfile.mkdtemp(prefix="gams_run_"))
        cleanup = False
    else:
        td = tempfile.TemporaryDirectory(prefix="gams_run_")
        td_path = Path(td.name)
        cleanup = True

    # Create output directory with timestamp
    run_stamp = datetime.now().strftime("run_%Y%m%dT%H%M%S")
    out_dir = Path("runs") / run_stamp

    try:
        # Copy model files to isolated workspace
        _copy_tree(work_dir_p, td_path)
        local_main = td_path / main_name
        if not local_main.exists():
            raise FileNotFoundError(f"Main file not found in temp copy: {local_main}")

        # Determine system directory
        sys_dir = system_directory or get_gams_home()
        
        # Create workspace manager following documented patterns
        workspace_mgr = GamsWorkspaceManager(
            system_directory=sys_dir,
            working_directory=str(td_path)
        )
        
        # Create job runner
        job_runner = GamsJobRunner(workspace_mgr)
        
        try:
            # Run using documented Control API patterns
            _run_gams_job_documented_pattern(
                workspace_mgr, 
                job_runner, 
                td_path, 
                main_name, 
                options
            )
            
        except Exception as e:
            msg = str(e)
            
            # Check for known compatibility issues (documented issue)
            if any(keyword in msg.lower() for keyword in ["memoryview", "buffer", "compatibility"]):
                print(f"Warning: GAMS API compatibility issue detected: {msg}")
                print("Falling back to direct GAMS executable (documented fallback pattern)...")
                
                try:
                    _run_via_subprocess_fallback(td_path, main_name, options or {})
                except Exception as e2:
                    copied = _collect_artifacts(td_path, out_dir, gdx_out)
                    error_details = {
                        "primary_error": msg,
                        "fallback_error": str(e2),
                        "system_directory": sys_dir,
                        "working_directory": str(td_path),
                        "recommendation": "Check pandas/numpy versions. Try: pip install 'pandas==1.5.3' 'numpy==1.24.3'"
                    }
                    (out_dir / "error.json").write_text(json.dumps(error_details, indent=2), encoding="utf-8")
                    raise RuntimeError(f"GAMS run failed via API and executable fallback. See artifacts in {out_dir} (listing: {copied.get('lst')})")
            else:
                # Other errors
                copied = _collect_artifacts(td_path, out_dir, gdx_out)
                error_details = {
                    "error": msg,
                    "system_directory": sys_dir,
                    "working_directory": str(td_path),
                }
                (out_dir / "error.json").write_text(json.dumps(error_details, indent=2), encoding="utf-8")
                raise RuntimeError(f"GAMS run failed. See artifacts in {out_dir} (listing: {copied.get('lst')})")

        # Collect output artifacts
        copied = _collect_artifacts(td_path, out_dir, gdx_out)
        if not copied["gdx"]:
            raise RuntimeError(f"Expected GDX not produced: {td_path / gdx_out}")

        # Build provenance metadata
        meta = build_run_meta(
            work_dir=str(work_dir_p),
            main_file=main_name,
            options=options or {},
            scenario_id=scenario_id,
            patch_path=patch_path,
            gams_version=None,  # Could be extracted from workspace if needed
        )
        write_run_json(out_dir, meta)

        # Write debug information
        (out_dir / "debug_paths.json").write_text(json.dumps({
            "work_dir_input": str(work_dir),
            "gms_file_input": str(gms_file),
            "work_dir_resolved": str(work_dir_p),
            "td_path": str(td_path),
            "local_main": str(local_main),
            "gdx_src": str(td_path / gdx_out),
            "gdx_dst": copied["gdx"],
            "system_directory": sys_dir,
        }, indent=2), encoding="utf-8")

        print(f"GAMS run completed successfully. Output: {copied['gdx']}")
        return Path(copied["gdx"])
        
    finally:
        # Cleanup temporary directory
        if cleanup:
            try:
                td.cleanup()
            except Exception:
                pass


# Primary interface - uses v49 patterns by default
def run_gams(
    work_dir: str,
    gms_file: str,
    gdx_out: str,
    options: Optional[Dict[str, Any]] = None,
    keep_temp: bool = False,
    scenario_id: Optional[str] = None,
    patch_path: Optional[str] = None,
) -> Path:
    """
    Run GAMS model with v49 API patterns.
    
    This is the primary interface that should be used by all consumers.
    Provides backward compatibility with the original run_gams interface.
    """
    return run_gams_v49(
        work_dir=work_dir,
        gms_file=gms_file,
        gdx_out=gdx_out,
        options=options,
        keep_temp=keep_temp,
        scenario_id=scenario_id,
        patch_path=patch_path,
    )


def get_run_log_txt(run_dir: str | Path) -> str:
    """Get run log text from listing file"""
    run_dir = Path(run_dir)
    lst_files = list(run_dir.glob("*.lst"))
    if not lst_files:
        return "(no listing file found)"
    return lst_files[0].read_text(encoding="utf-8", errors="ignore")


def validate_gams_setup() -> bool:
    """
    Validate GAMS setup following documentation patterns.
    
    Returns:
        bool: True if GAMS is properly configured
    """
    try:
        # Use our validation function
        return validate_gams_api()
    except Exception as e:
        print(f"GAMS setup validation failed: {e}")
        return False


def create_gams_workspace_for_gdx(system_directory: Optional[str] = None) -> GamsWorkspaceManager:
    """
    Create workspace specifically for GDX operations.
    
    For Control API GDX operations (when you need integration with GamsJob).
    For pure data operations, use Transfer API instead.
    """
    return GamsWorkspaceManager(system_directory or get_gams_home())