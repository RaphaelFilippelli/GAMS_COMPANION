from __future__ import annotations
import json
import os
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

from .env import get_gams_home, import_gams_workspace, validate_gams_api
from .gams_api_wrapper import GamsApiWrapper, GamsApiError
from .provenance import build_run_meta, write_run_json


@dataclass
class RunConfig:
    work_dir: str
    gms_file: str
    gdx_out: str
    options: Optional[Dict[str, Any]] = None
    keep_temp: bool = False


def _copy_tree(src: Path, dst: Path) -> None:
    for p in src.rglob("*"):
        rel = p.relative_to(src)
        target = dst / rel
        if p.is_dir():
            target.mkdir(parents=True, exist_ok=True)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, target)


def _collect_artifacts(td_path: Path, out_dir: Path, gdx_out: str) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    copied = {"lst": None, "gdx": None}
    lst_candidates = sorted(td_path.glob("*.lst"), key=lambda p: p.stat().st_mtime, reverse=True)
    if lst_candidates:
        lst_dst = out_dir / lst_candidates[0].name
        shutil.copy2(lst_candidates[0], lst_dst)
        copied["lst"] = str(lst_dst)
    gdx_src = td_path / gdx_out
    if gdx_src.exists():
        gdx_dst = out_dir / "raw.gdx"
        shutil.copy2(gdx_src, gdx_dst)
        copied["gdx"] = str(gdx_dst)
    return copied


def _run_via_api(td_path: Path, main_name: str, options: Dict[str, Any] | None) -> None:
    """Run GAMS using the Python API with proper wrapper. Raises on error."""
    old_cwd = Path.cwd()
    try:
        os.chdir(td_path)
        
        # Use the new wrapper for better compatibility
        api_wrapper = GamsApiWrapper(
            system_directory=get_gams_home(),
            working_directory=str(td_path)
        )
        
        # Run the job using the wrapper
        job = api_wrapper.run_gams_file(
            gams_file=str(td_path / main_name),
            options=options
        )
        
    except GamsApiError as e:
        # Re-raise GamsApiError with additional context
        raise RuntimeError(f"GAMS API execution failed: {e}") from e
    except Exception as e:
        # Handle unexpected errors
        raise RuntimeError(f"Unexpected error during GAMS execution: {e}") from e
    finally:
        try:
            os.chdir(old_cwd)
        except Exception:
            pass


def _run_via_exe(td_path: Path, main_name: str, options: Dict[str, Any] | None) -> None:
    """Fallback: run GAMS by calling the gams.exe directly."""
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


def run_gams(
    work_dir: str,
    gms_file: str,
    gdx_out: str,
    options: Optional[Dict[str, Any]] = None,
    keep_temp: bool = False,
    scenario_id: Optional[str] = None,
    patch_path: Optional[str] = None,
) -> Path:
    """Run GAMS in an isolated temp workspace and return path to the result GDX.

    Prefers the Python API but falls back to gams.exe when the API crashes
    (e.g. MemoryView.init buffer errors due to binary mismatch).
    """
    work_dir_p = Path(work_dir).resolve()
    if not work_dir_p.exists():
        raise FileNotFoundError(f"Work dir not found: {work_dir_p}")

    main_name = Path(gms_file).name

    if keep_temp:
        td_path = Path(tempfile.mkdtemp(prefix="gams_run_"))
        cleanup = False
    else:
        td = tempfile.TemporaryDirectory(prefix="gams_run_")
        td_path = Path(td.name)
        cleanup = True

    run_stamp = datetime.now().strftime("run_%Y%m%dT%H%M%S")
    out_dir = Path("runs") / run_stamp

    try:
        _copy_tree(work_dir_p, td_path)
        local_main = td_path / main_name
        if not local_main.exists():
            raise FileNotFoundError(f"Main file not found in temp copy: {local_main}")

        try:
            _run_via_api(td_path, main_name, options or {})
        except Exception as e:
            msg = str(e)
            
            # Check for known compatibility issues
            if any(keyword in msg.lower() for keyword in ["memoryview", "buffer", "compatibility"]):
                print(f"Warning: GAMS API compatibility issue detected: {msg}")
                print("Falling back to direct GAMS executable...")
                try:
                    _run_via_exe(td_path, main_name, options or {})
                except Exception as e2:
                    copied = _collect_artifacts(td_path, out_dir, gdx_out)
                    error_details = {
                        "primary_error": msg,
                        "fallback_error": str(e2),
                        "recommendation": "Check pandas/numpy versions. Try: pip install 'pandas==1.5.3' 'numpy==1.24.3'"
                    }
                    (out_dir / "error.json").write_text(json.dumps(error_details, indent=2), encoding="utf-8")
                    raise RuntimeError(f"GAMS run failed via API and EXE fallback. See artifacts in {out_dir} (listing: {copied.get('lst')})") from e2
            else:
                copied = _collect_artifacts(td_path, out_dir, gdx_out)
                (out_dir / "error.json").write_text(json.dumps({"error": msg}, indent=2), encoding="utf-8")
                raise RuntimeError(f"GAMS run failed. See artifacts in {out_dir} (listing: {copied.get('lst')})") from e

        copied = _collect_artifacts(td_path, out_dir, gdx_out)
        if not copied["gdx"]:
            raise RuntimeError(f"Expected GDX not produced: {td_path / gdx_out}")

        meta = build_run_meta(
            work_dir=str(work_dir_p),
            main_file=main_name,
            options=options or {},
            scenario_id=scenario_id,
            patch_path=patch_path,
            gams_version=None,
        )
        write_run_json(out_dir, meta)

        (out_dir / "debug_paths.json").write_text(json.dumps({
            "work_dir_input": str(work_dir),
            "gms_file_input": str(gms_file),
            "work_dir_resolved": str(work_dir_p),
            "td_path": str(td_path),
            "local_main": str(local_main),
            "gdx_src": str(td_path / gdx_out),
            "gdx_dst": copied["gdx"],
        }, indent=2), encoding="utf-8")

        return Path(copied["gdx"])
    finally:
        if cleanup:
            try:
                td.cleanup()
            except Exception:
                pass


def get_run_log_txt(run_dir: str | Path) -> str:
    run_dir = Path(run_dir)
    lst_files = list(run_dir.glob("*.lst"))
    if not lst_files:
        return "(no listing file found)"
    return lst_files[0].read_text(encoding="utf-8", errors="ignore")
