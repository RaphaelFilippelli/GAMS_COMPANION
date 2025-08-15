from __future__ import annotations
import hashlib, json
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, Optional
from ulid import ULID  # type: ignore

def _sha256_of_bytes(data: bytes) -> str:
    import hashlib
    h = hashlib.sha256(); h.update(data); return h.hexdigest()

def _sha256_of_file(path: Path) -> str:
    return _sha256_of_bytes(Path(path).read_bytes())

def compute_model_hash(root: str | Path, exclude_dirs: Iterable[str] = ("runs",)) -> str:
    root = Path(root); files = []
    for p in root.rglob("*"):
        if p.is_dir(): continue
        if any(part in exclude_dirs for part in p.parts): continue
        files.append(p)
    files = sorted(files, key=lambda p: str(p.relative_to(root)))
    h = hashlib.sha256()
    for p in files:
        rel = str(p.relative_to(root)).replace("\\","/")
        h.update(rel.encode("utf-8")); h.update(b"\0"); h.update(p.read_bytes()); h.update(b"\0")
    return h.hexdigest()

def build_run_meta(*, work_dir: str, main_file: str, options: Dict[str, str] | None = None, scenario_id: str | None = None, gams_version: str | None = None, patch_path: str | Path | None = None, git_commit: str | None = None) -> Dict[str, str]:
    # Try to create ULID, fallback to UUID if MemoryView error occurs (pandas/numpy compatibility issue)
    try:
        run_id = str(ULID())
    except TypeError as e:
        if "MemoryView" in str(e):
            import uuid
            run_id = str(uuid.uuid4())
        else:
            raise
    meta = {
        "run_id": run_id,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "scenario_id": scenario_id,
        "gams_version": gams_version,
        "model_hash": compute_model_hash(work_dir),
        "patch_hash": _sha256_of_file(Path(patch_path)) if patch_path else None,
        "commit": git_commit,
        "main_file": main_file,
        "options": options or {},
    }
    return meta

def write_run_json(run_dir: str | Path, meta: Dict[str, str]) -> Path:
    run_dir = Path(run_dir); out = run_dir / "run.json"
    out.write_text(json.dumps(meta, indent=2), encoding="utf-8"); return out
