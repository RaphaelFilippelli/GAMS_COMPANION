from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import yaml  # PyYAML
import re

try:
    from gams import transfer as gt  # type: ignore
except Exception as e:
    gt = None  # We'll raise a helpful error when trying to build the patch

@dataclass
class ScenarioEdits:
    scalars: List[Dict[str, Any]]
    parameters: List[Dict[str, Any]]
    sets: List[Dict[str, Any]]
    equations_includes: List[str]

@dataclass
class Scenario:
    id: str
    description: Optional[str]
    edits: ScenarioEdits
    meta: Dict[str, Any]

_SCALAR_KEYS = {"name", "value"}
_PARAM_KEYS = {"name", "updates"}
_SET_KEYS   = {"name", "add", "remove"}

def load_yaml(path: str | Path) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def _slug_ok(s: str) -> bool:
    return re.fullmatch(r"[A-Za-z0-9_\-\.]+", s) is not None

def validate_scenario(data: Dict[str, Any]) -> Scenario:
    if not isinstance(data, dict): raise ValueError("Scenario YAML must be a mapping")
    sid = data.get("id")
    if not sid or not isinstance(sid, str) or not _slug_ok(sid):
        raise ValueError("Scenario 'id' is required and must be slug-safe (letters, numbers, _ - .)")
    edits = data.get("edits") or {}
    if not isinstance(edits, dict):
        raise ValueError("'edits' must be a mapping")
    any_section = any(k in edits for k in ("scalars","parameters","sets","equations"))
    if not any_section:
        raise ValueError("Scenario must declare at least one of: scalars, parameters, sets, equations")
    scalars = edits.get("scalars") or []
    if not isinstance(scalars, list): raise ValueError("'edits.scalars' must be a list")
    for s in scalars:
        if not _SCALAR_KEYS.issubset(s.keys()): raise ValueError(f"Scalar requires keys {sorted(_SCALAR_KEYS)}; got {s}")
    parameters = edits.get("parameters") or []
    if not isinstance(parameters, list): raise ValueError("'edits.parameters' must be a list")
    for p in parameters:
        if not _PARAM_KEYS.issubset(p.keys()): raise ValueError(f"Parameter requires keys {sorted(_PARAM_KEYS)}; got {p}")
        ups = p["updates"]
        if not isinstance(ups, list): raise ValueError("parameter.updates must be a list")
        for u in ups:
            if "key" not in u or "value" not in u: raise ValueError(f"parameter.update entries require 'key' and 'value'; got {u}")
            if not isinstance(u["key"], (list, tuple)): raise ValueError("parameter.update.key must be a list/tuple")
    sets_ = edits.get("sets") or []
    if not isinstance(sets_, list): raise ValueError("'edits.sets' must be a list")
    for s in sets_:
        if not _SET_KEYS.issubset(s.keys()): raise ValueError(f"Set requires keys {sorted(_SET_KEYS)}; got {s}")
        if not isinstance(s["add"], list) or not isinstance(s["remove"], list):
            raise ValueError("set.add and set.remove must be lists")
    eq = edits.get("equations") or {}
    includes = eq.get("includes") or []
    if includes and not isinstance(includes, list): raise ValueError("'equations.includes' must be a list")
    scen = Scenario(
        id=sid,
        description=data.get("description"),
        edits=ScenarioEdits(scalars, parameters, sets_, includes),
        meta=data.get("meta") or {}
    )
    return scen

def _ensure_transfer():
    global gt
    if gt is None:
        raise ImportError("GAMS Transfer API not available. Ensure GAMS v49+ API is installed in this environment.")

def build_patch_gdx(out_dir: str | Path, scen: Scenario) -> Path:
    \"\"\"Create patch.gdx with symbols declared in the scenario.\"\"\"
    _ensure_transfer()
    out = Path(out_dir); out.mkdir(parents=True, exist_ok=True)
    db = gt.Container()
    # scalars
    for s in scen.edits.scalars:
        p = gt.Parameter(db, s["name"])
        p.setRecords([s["value"]])
    # parameters
    for p in scen.edits.parameters:
        name = p["name"]; updates = p["updates"]
        if updates:
            # Infer dimension from first key
            dim = len(updates[0]["key"])
            domain = [f"*" for _ in range(dim)]  # Use universal domain
            par = gt.Parameter(db, name, domain)
            records_data = []
            for u in updates:
                key = [str(x) for x in u["key"]]
                records_data.append(key + [u["value"]])
            par.setRecords(records_data)
    # sets
    for s in scen.edits.sets:
        name = s["name"]; to_add = s.get("add") or []; to_remove = set(s.get("remove") or [])
        if to_add:
            st = gt.Set(db, name)
            filtered_add = [str(el) for el in to_add if el not in to_remove]
            if filtered_add:
                st.setRecords(filtered_add)
    patch = out / "patch.gdx"
    db.write(str(patch))
    return patch

def ensure_autoload_include(temp_main_gms: str | Path, symbols: List[str]) -> Path:
    \"\"\"Ensure temp main.gms includes an autoload include that loads our patch.gdx for given symbols.\"\"\"
    main = Path(temp_main_gms)
    inc_path = main.parent / "autoload_patch.inc"
    load_lines = []
    load_lines.append("$if exist patch.gdx $gdxin patch.gdx")
    # Load sets/parameters/scalars by name (GAMS figures out type from db)
    for name in symbols:
        load_lines.append(f"$load {name}")
    inc_body = "* Auto-generated by scenario.apply\n" + "\n".join(load_lines) + "\n"
    inc_path.write_text(inc_body, encoding="utf-8")

    src = main.read_text(encoding="utf-8")
    if "$include autoload_patch.inc" not in src and "$include  autoload_patch.inc" not in src:
        # Insert near top, after first line
        lines = src.splitlines()
        insert_at = 1 if lines else 0
        lines.insert(insert_at, "$include autoload_patch.inc")
        main.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return inc_path

def apply_scenario_to_temp_dir(temp_dir: str | Path, model_dir: str | Path, main_gms_name: str, scenario_yaml: str | Path) -> dict:
    \"\"\"Apply a scenario to the *temp* workspace before running GAMS.
    - Writes patch.gdx in temp_dir
    - Copies includes (if any) into temp_dir preserving rel paths
    - Ensures autoload include is present in temp main.gms
    - Returns dict with scenario_id and symbols touched
    \"\"\"
    data = load_yaml(scenario_yaml)
    scen = validate_scenario(data)
    temp_dir = Path(temp_dir); model_dir = Path(model_dir)
    # Build patch
    patch = build_patch_gdx(temp_dir, scen)
    # Copy equation includes
    for inc_rel in scen.edits.equations_includes:
        src = (model_dir / inc_rel).resolve()
        dst = (temp_dir / inc_rel)
        dst.parent.mkdir(parents=True, exist_ok=True)
        if not src.exists():
            raise FileNotFoundError(f"Equation include not found: {src}")
        dst.write_text(src.read_text(encoding='utf-8'), encoding='utf-8')
    # Ensure autoload include in temp main
    symbols = []
    symbols += [s["name"] for s in scen.edits.scalars]
    symbols += [p["name"] for p in scen.edits.parameters]
    symbols += [s["name"] for s in scen.edits.sets]
    ensure_autoload_include(temp_dir / main_gms_name, symbols)
    return {"scenario_id": scen.id, "symbols": symbols}
