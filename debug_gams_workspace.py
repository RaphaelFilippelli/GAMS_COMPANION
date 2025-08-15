#!/usr/bin/env python3
"""
Debug script to test GAMS workspace isolation
"""
import tempfile
import shutil
from pathlib import Path
from src.core.env import get_gams_home, import_gams_workspace

def test_workspace_isolation():
    GamsWorkspace, _ = import_gams_workspace()
    
    # Create temp directory
    with tempfile.TemporaryDirectory() as td:
        td_p = Path(td)
        print(f"Temp directory: {td_p}")
        
        # Copy toy_model to temp
        for p in Path('toy_model').rglob('*'):
            rel = p.relative_to(Path('toy_model'))
            target = td_p / rel
            if p.is_dir():
                target.mkdir(parents=True, exist_ok=True)
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(p, target)
        
        print(f"Files in temp: {list(td_p.iterdir())}")
        
        # Create workspace with explicit working directory
        ws = GamsWorkspace(working_directory=str(td_p), system_directory=get_gams_home())
        print(f"Workspace working dir: {ws.working_directory}")
        print(f"Workspace system dir: {ws.system_directory}")
        
        # Create job from temp file
        temp_main = td_p / "main.gms"
        job = ws.add_job_from_file(str(temp_main))
        
        print(f"Job working dir: {job.workspace.working_directory}")
        print(f"Job name: {job.name}")
        
        # Try to run with compile-only option
        try:
            gopt = ws.add_options()
            gopt.action = "c"  # Compile only
            job.run(gopt)
            print("Job completed successfully")
        except Exception as e:
            print(f"Job failed: {e}")
            
            # Check listing file
            lst_files = list(td_p.glob("*.lst"))
            if lst_files:
                print(f"Listing file: {lst_files[0]}")
                content = lst_files[0].read_text(encoding='utf-8', errors='ignore')
                print("=== LISTING CONTENT ===")
                print(content[:2000])  # First 2000 chars
            else:
                print("No listing file found")

if __name__ == "__main__":
    test_workspace_isolation()