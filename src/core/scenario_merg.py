
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional
import re
import yaml  # PyYAML

# We will use the Transfer API via gt.Workspace -> Database to build a small patch GDX.
def _import_transfer():
    try:
        from gams import transfer as gt  # type: ignore
        return gt
    except Exception as e:
        raise ImportError("GAMS Transfer API is not available. Ensure GAMS v49+ Python API is installed.") from e

@dataclass
class Scenario:
    id: str
    description: Optional[str]
    edits: Dict[str, Any]
    meta: Dict[str, Any]

_slug_re = re.compile(r"^[A-Za-z0-9_\-\.]+$")

def load_scenario(path: str | Path) -> Scenario:
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Scenario YAML must be a mapping/object")
    sid = data.get("id")
    if not sid or not isinstance(sid, str) or not _slug_re.match(sid):
        raise ValueError("Scenario 'id' is required and must be slug-safe (letters, numbers, _ - .)")
    edits = data.get("edits") or {}
    if not isinstance(edits, dict):
        raise ValueError("'edits' must be a mapping/object")
    if not any(k in edits for k in ("scalars", "parameters", "sets", "equations")):
        raise ValueError("Scenario must declare at least one of: scalars, parameters, sets, equations")
    # Normalize shapes
    scalars = edits.get("scalars") or []
    if not isinstance(scalars, list):
        raise ValueError("'edits.scalars' must be a list")
    parameters = edits.get("parameters") or []
    if not isinstance(parameters, list):
        raise ValueError("'edits.parameters' must be a list")
    for p in parameters:
        ups = p.get("updates")
        if not isinstance(ups, list):
            raise ValueError("parameter.updates must be a list")
        for u in ups:
            if "key" not in u or "value" not in u:
                raise ValueError("parameter.update requires 'key' and 'value'")
            if not isinstance(u["key"], (list, tuple)):
                raise ValueError("parameter.update.key must be a list/tuple")
    sets_ = edits.get("sets") or []
    if not isinstance(sets_, list):
        raise ValueError("'edits.sets' must be a list")
    for s in sets_:
        if "add" not in s or "remove" not in s or "name" not in s:
            raise ValueError("set edits require 'name', 'add', 'remove'")
        if not isinstance(s["add"], list) or not isinstance(s["remove"], list):
            raise ValueError("set.add and set.remove must be lists")
    eq = edits.get("equations") or {}
    if not isinstance(eq, dict):
        raise ValueError("'equations' must be a mapping/object if present")
    includes = eq.get("includes") or []
    if includes and not isinstance(includes, list):
        raise ValueError("'equations.includes' must be a list")
    scen = Scenario(
        id=sid,
        description=data.get("description"),
        edits={"scalars": scalars, "parameters": parameters, "sets": sets_, "equations": {"includes": includes}},
        meta=data.get("meta") or {},
    )
    return scen

def build_patch_gdx(temp_dir: str | Path, scen: Scenario) -> Path:
    """Create patch.gdx in temp_dir with all symbol edits; returns the path."""
    gt = _import_transfer()
    temp_dir = Path(temp_dir); temp_dir.mkdir(parents=True, exist_ok=True)
    db = gt.Container()  # Transfer Container
    # Scalars -> parameters of dim 0
    for s in scen.edits["scalars"]:
        name = s["name"]; val = s["value"]
        par = gt.Parameter(db, name)
        par.setRecords([val])
    # Parameters -> parameters of inferred dimension
    for p in scen.edits["parameters"]:
        name = p["name"]; ups = p["updates"]
        if ups:
            # Infer dimension from first key
            dim = len(ups[0]["key"])
            domain = [f"*" for _ in range(dim)]  # Use universal domain
            par = gt.Parameter(db, name, domain)
            records_data = []
            for u in ups:
                key = [str(x) for x in u["key"]]
                records_data.append(key + [u["value"]])
            par.setRecords(records_data)
    # Sets -> sets(dim=1) adding only "add" items  
    for s in scen.edits["sets"]:
        name = s["name"]
        add_items = s.get("add") or []
        if add_items:
            st = gt.Set(db, name)
            st.setRecords(add_items)
    patch = temp_dir / "patch.gdx"
    db.write(str(patch))
    return patch

def ensure_autoload_include(temp_main_gms: str | Path, symbols: List[str]) -> Path:
    """Move GDX loading to after declarations and update symbol list."""
    main = Path(temp_main_gms)
    
    # Read the main.gms file
    src = main.read_text(encoding="utf-8", errors="ignore")
    lines = src.splitlines()
    
    # Remove existing GDX loading lines and find where to insert new ones
    out_lines = []
    gdx_lines_removed = False
    
    for line in lines:
        # Remove existing GDX loading lines (before declarations)
        if ("$gdxin" in line or "$load " in line) and not gdx_lines_removed:
            continue
        else:
            out_lines.append(line)
            # Insert GDX loading after parameter declarations (look for "Benefit" parameter as marker)  
            if "Benefit(i)" in line and symbols and not gdx_lines_removed:
                out_lines.append("")
                out_lines.append("* Load scenario overrides from patch.gdx")
                out_lines.append("$onMultiR")
                out_lines.append("$if exist patch.gdx $gdxin patch.gdx")
                symbol_list = ", ".join(symbols)
                out_lines.append(f"$if exist patch.gdx $load {symbol_list}")
                out_lines.append("$if exist patch.gdx $gdxin")
                out_lines.append("$offMulti")
                gdx_lines_removed = True
    
    # Write back the modified main.gms
    main.write_text("\n".join(out_lines) + "\n", encoding="utf-8")
    return main

def apply_scenario_to_temp_workspace(temp_dir: str | Path, model_dir: str | Path, main_gms_name: str, scenario_yaml: str | Path) -> Dict[str, Any]:
    """Apply scenario YAML to the *temp copy*:
       - Build patch.gdx in temp_dir
       - Copy equation includes from model_dir into temp_dir
       - Ensure autoload include is present in temp main.gms
       Returns dict with scenario_id and symbols touched.
    """
    scen = load_scenario(scenario_yaml)
    temp_dir = Path(temp_dir); model_dir = Path(model_dir)
    # Build patch
    patch = build_patch_gdx(temp_dir, scen)
    # Copy any equation include files
    for rel in scen.edits["equations"]["includes"]:
        src = (model_dir / rel).resolve()
        dst = (temp_dir / rel)
        dst.parent.mkdir(parents=True, exist_ok=True)
        if not src.exists():
            raise FileNotFoundError(f"Equation include not found: {src}")
        dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
    # Ensure include in main
    syms: List[str] = []
    syms += [s["name"] for s in scen.edits["scalars"]]
    syms += [p["name"] for p in scen.edits["parameters"]]
    syms += [s["name"] for s in scen.edits["sets"]]
    ensure_autoload_include(Path(temp_dir) / main_gms_name, syms)
    return {"scenario_id": scen.id, "symbols": syms, "patch": str(patch)}
