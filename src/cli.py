from __future__ import annotations
import shutil
import tempfile
from pathlib import Path
import typer
from rich import print
from pydantic import BaseModel
from typing import Optional, Dict, Any

from .core.model_runner import run_gams
from .core.gdx_io import read_gdx, export_excel
from .core.patch_builder import build_patch_gdx, get_patch_info
from .core.equation_injector import inject_equation_includes
from .core.provenance import generate_run_id, create_run_json, write_run_json

app = typer.Typer(help="GAMS Helper CLI")


class Scenario(BaseModel):
    id: str
    description: str | None = None
    model: Dict[str, Any]
    gams: Dict[str, Any] = {}
    edits: Dict[str, Any] = {}
    equations: list[Dict[str, str]] = []
    notes: str | None = None


@app.command()
def run_scenario(file: Path, out: Path = Path("runs"), dry_run: bool = typer.Option(False, help="Compile only")) -> None:
    """Run a scenario YAML with full patch and equation injection support."""
    import yaml  # lazy import
    
    # Validate scenario file exists
    if not file.exists():
        print(f"[red]Error:[/red] Scenario file not found: {file}")
        raise typer.Exit(4)
    
    # Load and validate scenario
    try:
        sc = Scenario.model_validate(yaml.safe_load(file.read_text(encoding="utf-8")))
    except Exception as e:
        print(f"[red]Error:[/red] Invalid scenario YAML: {e}")
        raise typer.Exit(4)
    
    # Resolve paths
    scenario_dir = file.parent.resolve()
    model_dir = Path(sc.model["work_dir"]).resolve()
    if not model_dir.is_absolute():
        model_dir = scenario_dir / sc.model["work_dir"]
    
    # Validate model directory
    if not model_dir.exists():
        print(f"[red]Error:[/red] Model directory not found: {model_dir}")
        raise typer.Exit(4)
    
    main_file = sc.model["main_file"]
    if not (model_dir / main_file).exists():
        print(f"[red]Error:[/red] Main GAMS file not found: {model_dir / main_file}")
        raise typer.Exit(4)
    
    # Generate run ID and create output directory
    run_id = generate_run_id()
    run_dir = out / f"run_{run_id}"
    run_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"[blue]Starting run:[/blue] {run_id}")
    print(f"[blue]Scenario:[/blue] {sc.id} - {sc.description or 'No description'}")
    print(f"[blue]Output:[/blue] {run_dir}")
    
    try:
        # Create temporary working directory
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_model_dir = Path(temp_dir) / "model"
            
            # Copy model to temp directory
            print("[yellow]Copying model to temporary workspace...[/yellow]")
            shutil.copytree(model_dir, temp_model_dir)
            
            
            
            patch_info = None
            
            # Build patch.gdx if there are edits
            if sc.edits:
                print("[yellow]Building patch.gdx from scenario edits...[/yellow]")
                patch_path = temp_model_dir / "patch.gdx"
                build_patch_gdx(sc.edits, scenario_dir, patch_path)
                patch_info = get_patch_info(patch_path)
                
                # Skip patch loading setup - original main.gms already has correct loading
                # setup_patch_loading(temp_model_dir, patch_path, main_file)
                print(f"[green]Patch built:[/green] {len(patch_info['symbols'])} symbols")
            
            # Inject equation includes
            if sc.equations:
                print("[yellow]Injecting equation includes...[/yellow]")
                # Copy equation files to temp model directory
                for eq_spec in sc.equations:
                    if 'file' in eq_spec:
                        eq_file = eq_spec['file']
                        src_path = scenario_dir / eq_file
                        dst_path = temp_model_dir / eq_file
                        
                        if not src_path.exists():
                            print(f"[red]Error:[/red] Equation file not found: {src_path}")
                            raise typer.Exit(4)
                        
                        dst_path.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(src_path, dst_path)
                
                inject_equation_includes(temp_model_dir, sc.equations, main_file)
                print(f"[green]Injected:[/green] {len(sc.equations)} equation includes")
            
            # Prepare GAMS options
            gams_options = sc.gams.get("options", {})
            if dry_run:
                # Set compile-only mode
                gams_options["action"] = "c"  # Compile only
                print("[yellow]Running in dry-run mode (compile only)...[/yellow]")
            else:
                print("[yellow]Running GAMS solve...[/yellow]")
            
            # Run GAMS
            try:
                gdx_path = run_gams(
                    str(temp_model_dir), 
                    main_file, 
                    gdx_out="results.gdx",
                    run_output_dir=run_dir,
                    options=gams_options
                )
                print("[green]GAMS completed successfully[/green]")
                
                # Export to Excel if not in dry-run mode
                if not dry_run:
                    print("[yellow]Exporting results to Excel...[/yellow]")
                    try:
                        symbol_data = read_gdx(gdx_path)
                        if symbol_data:
                            excel_path = run_dir / f"{run_id}_results.xlsx"
                            export_excel(symbol_data, excel_path)
                            print(f"[green]Excel export saved to:[/green] {excel_path}")
                        else:
                            print("[yellow]No symbols found in GDX for Excel export[/yellow]")
                    except Exception as e:
                        print(f"[yellow]Excel export failed:[/yellow] {e}")
                        # Continue execution - Excel export is optional
                
                # The GDX is already in the correct run directory
                
            except Exception as e:
                print(f"[red]GAMS execution failed:[/red] {e}")
                # Try to copy any log files for debugging
                log_files = list(temp_model_dir.glob("*.lst"))
                if log_files:
                    shutil.copy2(log_files[0], run_dir / "error.lst")
                    print(f"[yellow]Error log saved to:[/yellow] {run_dir / 'error.lst'}")
                raise typer.Exit(2 if "compile" in str(e).lower() else 3)
            
            # Generate provenance information
            print("[yellow]Creating provenance record...[/yellow]")
            run_data = create_run_json(
                run_id=run_id,
                scenario_id=sc.id,
                model_dir=model_dir,  # Original model directory
                main_file=main_file,
                gams_options=gams_options,
                patch_info=patch_info
            )
            
            write_run_json(run_data, run_dir)
            
            # Export results if not dry-run
            if not dry_run and gdx_path.exists():
                print("[yellow]Exporting results to Excel...[/yellow]")
                try:
                    sym = read_gdx(gdx_path)
                    excel_path = run_dir / f"{sc.id}_results.xlsx"
                    export_excel(sym, excel_path)
                    print(f"[green]Excel export completed:[/green] {excel_path}")
                except Exception as e:
                    print(f"[yellow]Excel export failed:[/yellow] {e}")
                    # Don't fail the entire run for export issues
            
    except typer.Exit:
        raise  # Re-raise typer exits
    except Exception as e:
        print(f"[red]Unexpected error:[/red] {e}")
        raise typer.Exit(4)
    
    print("[green]Run completed successfully![/green]")
    print(f"[blue]Run ID:[/blue] {run_id}")
    print(f"[blue]Output directory:[/blue] {run_dir}")
    
    if sc.notes:
        print(f"[blue]Notes:[/blue] {sc.notes}")


@app.command()
def export(gdx: Path, excel: Optional[Path] = None) -> None:
    """Re-export a GDX to Excel."""
    sym = read_gdx(gdx)
    excel = excel or gdx.with_suffix(".xlsx")
    export_excel(sym, excel)
    print(f"[green]Exported[/green] → {excel}")


if __name__ == "__main__":
    app()
