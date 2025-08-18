
"""
GAMS model runner (merged) — v49 Control API patterns + optional scenario support.

- Runs in an isolated temp workspace
- Collects .lst and raw.gdx into runs/<stamp>/
- Optionally applies a Scenario YAML (builds patch.gdx, copies includes, injects $include in temp main)
- Silently ignores LO/LogOption when using the Control API (CLI-only flag)
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
    GamsApiError,
    options_to_cli_args,
)
from .provenance import build_run_meta, write_run_json

# Scenario support is optional; import if present
try:
    from .scenario_merg import apply_scenario_to_temp_workspace  # type: ignore
except Exception:  # pragma: no cover
    apply_scenario_to_temp_workspace = None  # type: ignore


@dataclass
class RunConfig:
    work_dir: str
    gms_file: str
    gdx_out: str
    options: Optional[Dict[str, Any]] = None
    keep_temp: bool = False
    system_directory: Optional[str] = None


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


def _run_job_api(td_path: Path, main_name: str, options: Optional[Dict[str, Any]]) -> None:
    """Run via Control API (preferred)."""
    ws_mgr = GamsWorkspaceManager(system_directory=get_gams_home(), working_directory=str(td_path))
    runner = GamsJobRunner(ws_mgr)
    job = runner.create_job_from_file(str(td_path / main_name))
    if options:
        runner.run_job(job, options)
    else:
        runner.run_job(job)


def _run_job_subprocess(td_path: Path, main_name: str, options: Optional[Dict[str, Any]]) -> None:
    """Fallback: call gams.exe directly (so LO can be passed as CLI)."""
    import subprocess

    gams_exe = Path(get_gams_home()) / "gams.exe"
    if not gams_exe.exists():
        alt = Path(get_gams_home()) / "gams" / "gams.exe"
        if alt.exists():
            gams_exe = alt
    if not gams_exe.exists():
        raise FileNotFoundError(f"GAMS executable not found under {get_gams_home()}")

    args = [str(gams_exe), main_name] + options_to_cli_args(options or {})
    proc = subprocess.run(args, cwd=str(td_path), capture_output=True, text=True, shell=False)
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
    scenario_yaml: Optional[str] = None,
    scenario_id: Optional[str] = None,
    patch_path: Optional[str] = None,
    system_directory: Optional[str] = None,
) -> Path:
    """Primary runner. Applies scenario (if provided) in temp workspace, then runs GAMS."""
    work_dir_p = Path(work_dir).resolve()
    if not work_dir_p.exists():
        raise FileNotFoundError(f"Work dir not found: {work_dir_p}")

    main_name = Path(gms_file).name

    # Temp workspace
    if keep_temp:
        td_path = Path(tempfile.mkdtemp(prefix="gams_run_"))
        cleanup_ctx = None
    else:
        cleanup_ctx = tempfile.TemporaryDirectory(prefix="gams_run_")
        td_path = Path(cleanup_ctx.name)

    # Output dir
    run_stamp = datetime.now().strftime("run_%Y%m%dT%H%M%S")
    out_dir = Path("runs") / run_stamp

    try:
        _copy_tree(work_dir_p, td_path)
        local_main = td_path / main_name
        if not local_main.exists():
            raise FileNotFoundError(f"Main file not found in temp copy: {local_main}")

        # Optional scenario application
        scen_info = None
        if scenario_yaml:
            if apply_scenario_to_temp_workspace is None:
                raise RuntimeError("Scenario support not available (scenario_merg.py missing).")
            scen_info = apply_scenario_to_temp_workspace(td_path, work_dir_p, main_name, scenario_yaml)

        # Run via Control API; fallback to subprocess on compat issues
        try:
            _run_job_api(td_path, main_name, options)
        except Exception as e:
            msg = str(e).lower()
            if any(k in msg for k in ("memoryview", "buffer", "compatibility")):
                _run_job_subprocess(td_path, main_name, options)
            else:
                raise

        # Collect artifacts
        copied = _collect_artifacts(td_path, out_dir, gdx_out)
        if not copied["gdx"]:
            raise RuntimeError(f"Expected GDX not produced: {td_path / gdx_out}")

        # Provenance
        meta = build_run_meta(
            work_dir=str(work_dir_p),
            main_file=main_name,
            options=options or {},
            scenario_id=scenario_id or (scen_info or {}).get("scenario_id"),
            patch_path=patch_path or (str(td_path / "patch.gdx") if (td_path / "patch.gdx").exists() else None),
            gams_version=None,
        )
        write_run_json(out_dir, meta)

        # Debug breadcrumbs
        (out_dir / "debug_paths.json").write_text(
            json.dumps(
                {
                    "work_dir_input": str(work_dir),
                    "gms_file_input": str(gms_file),
                    "work_dir_resolved": str(work_dir_p),
                    "td_path": str(td_path),
                    "local_main": str(local_main),
                    "scenario_yaml": scenario_yaml,
                    "gdx_src": str(td_path / gdx_out),
                    "gdx_dst": copied["gdx"],
                },
                indent=2,
            ),
            encoding="utf-8",
        )

        return Path(copied["gdx"])

    finally:
        if cleanup_ctx is not None:
            try:
                cleanup_ctx.cleanup()
            except Exception:
                pass


def run_gams(
    work_dir: str,
    gms_file: str,
    gdx_out: str,
    options: Optional[Dict[str, Any]] = None,
    keep_temp: bool = False,
    scenario_yaml: Optional[str] = None,
    scenario_id: Optional[str] = None,
    patch_path: Optional[str] = None,
) -> Path:
    """Thin wrapper for compatibility; forwards to run_gams_v49 with scenario support."""
    return run_gams_v49(
        work_dir=work_dir,
        gms_file=gms_file,
        gdx_out=gdx_out,
        options=options,
        keep_temp=keep_temp,
        scenario_yaml=scenario_yaml,
        scenario_id=scenario_id,
        patch_path=patch_path,
    )


def get_run_log_txt(run_dir: str | Path) -> str:
    run_dir = Path(run_dir)
    lst_files = list(run_dir.glob("*.lst"))
    if not lst_files:
        return "(no listing file found)"
    return lst_files[0].read_text(encoding="utf-8", errors="ignore")


def validate_gams_setup() -> bool:
    try:
        return validate_gams_api()
    except Exception as e:
        print(f"GAMS setup validation failed: {e}")
        return False
