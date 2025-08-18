import sys
from pathlib import Path
import streamlit as st
import yaml
from datetime import datetime
import time

# Ensure repo root on sys.path
ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.async_runner import start_async_run, get_run_status, get_async_runner

st.set_page_config(page_title="Batch Scenarios", layout="wide")
st.title("🔄 Batch Scenarios")

# Initialize session state for batch runs
if "batch_runs" not in st.session_state:
    st.session_state.batch_runs = []
if "scenario_selection" not in st.session_state:
    st.session_state.scenario_selection = []
if "widget_counter" not in st.session_state:
    st.session_state.widget_counter = 0

# Configuration section
st.header("Configuration")

col1, col2 = st.columns([2, 1])

with col1:
    # Model configuration
    st.subheader("Model Settings")
    work_dir = st.text_input("Model folder", value=str(ROOT / "toy_model"))
    gms_file = st.text_input("Main .gms file", value="main.gms")
    gdx_out = st.text_input("Output GDX", value="results.gdx")
    lo = st.number_input("Log option (Lo)", value=2, step=1)

with col2:
    # Scenario folder selection
    st.subheader("Scenario Selection")
    scenario_folder = st.text_input("Scenario folder", value=str(ROOT / "scenarios"))
    
    # Auto-refresh scenarios when folder changes
    if st.button("🔄 Refresh scenarios"):
        st.session_state.selected_scenarios = []

# Discover and list scenarios
def load_scenarios(folder_path: str) -> list[dict]:
    """Load scenario files from folder and extract metadata"""
    scenarios = []
    folder = Path(folder_path)
    
    if not folder.exists() or not folder.is_dir():
        return scenarios
    
    for yaml_file in sorted(folder.glob("*.yaml")):
        try:
            with open(yaml_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                
            scenario_info = {
                "file_path": str(yaml_file),
                "file_name": yaml_file.name,
                "id": data.get("id", yaml_file.stem),
                "description": data.get("description", ""),
                "author": data.get("meta", {}).get("author", ""),
                "edits_count": len(data.get("edits", {}).get("scalars", []) + 
                                data.get("edits", {}).get("parameters", []) + 
                                data.get("edits", {}).get("sets", []))
            }
            scenarios.append(scenario_info)
        except Exception as e:
            st.warning(f"Could not load {yaml_file.name}: {e}")
    
    return scenarios

scenarios = load_scenarios(scenario_folder)

if scenarios:
    st.header("Available Scenarios")
    
    # Create DataFrame for better display
    scenario_df = st.data_editor(
        scenarios,
        column_config={
            "file_path": None,  # Hide full path
            "file_name": st.column_config.TextColumn("File", width="medium"),
            "id": st.column_config.TextColumn("Scenario ID", width="medium"), 
            "description": st.column_config.TextColumn("Description", width="large"),
            "author": st.column_config.TextColumn("Author", width="small"),
            "edits_count": st.column_config.NumberColumn("Edits", width="small")
        },
        use_container_width=True,
        key="scenarios_table",
        on_change=None,
        disabled=["file_name", "id", "description", "author", "edits_count"]
    )
    
    # Selection controls
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col2:
        select_all = st.button("Select All")
        if select_all:
            st.session_state.scenario_selection = list(range(len(scenarios)))
            st.session_state.widget_counter += 1
            st.rerun()
    
    with col3:
        clear_all = st.button("Clear All")
        if clear_all:
            st.session_state.scenario_selection = []
            st.session_state.widget_counter += 1
            st.rerun()
    
    with col1:
        # Multi-select for scenarios with dynamic key to force recreation
        selected_indices = st.multiselect(
            "Select scenarios to run:",
            options=range(len(scenarios)),
            default=st.session_state.scenario_selection,
            format_func=lambda i: f"{scenarios[i]['file_name']} ({scenarios[i]['id']})",
            key=f"scenario_selector_{st.session_state.widget_counter}"
        )
        
        # Update session state with current selection
        st.session_state.scenario_selection = selected_indices
    
    # Run scenarios section
    if selected_indices:
        st.subheader(f"Run {len(selected_indices)} Selected Scenarios")
        
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("🚀 Run Selected (Async)", type="primary"):
                try:
                    new_runs = []
                    for idx in selected_indices:
                        scenario = scenarios[idx]
                        run_id = f"batch_{int(time.time() * 1000)}_{scenario['id']}"
                        
                        # Start async run
                        _, status = start_async_run(
                            work_dir=work_dir,
                            gms_file=gms_file,
                            gdx_out=gdx_out,
                            options={"Lo": int(lo)},
                            run_id=run_id,
                            scenario_yaml=scenario['file_path']
                        )
                        
                        # Track in session state
                        run_info = {
                            "run_id": run_id,
                            "scenario_id": scenario['id'],
                            "scenario_file": scenario['file_name'],
                            "started_at": datetime.now(),
                            "status": "pending"
                        }
                        new_runs.append(run_info)
                    
                    # Add to session state
                    st.session_state.batch_runs.extend(new_runs)
                    st.success(f"Started {len(new_runs)} async runs")
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Failed to start batch runs: {e}")
        
        with col2:
            if st.button("⏱️ Run Selected (Sync)"):
                st.warning("Sync batch runs not implemented yet. Use async mode.")

else:
    if Path(scenario_folder).exists():
        st.info(f"No .yaml files found in {scenario_folder}")
    else:
        st.warning(f"Scenario folder not found: {scenario_folder}")

# Batch run status section
if st.session_state.batch_runs:
    st.header("Batch Run Status")
    
    # Auto-refresh controls
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        if st.button("🔄 Refresh Status"):
            st.rerun()
    
    with col2:
        auto_refresh = st.checkbox("Auto refresh (5s)", value=False)
    
    with col3:
        if st.button("🗑️ Clear Completed Runs"):
            # Remove completed/failed runs
            st.session_state.batch_runs = [
                run for run in st.session_state.batch_runs 
                if get_run_status(run["run_id"]) and 
                get_run_status(run["run_id"]).status not in ["completed", "failed"]
            ]
            st.rerun()
    
    # Update run statuses
    for run_info in st.session_state.batch_runs:
        status = get_run_status(run_info["run_id"])
        if status:
            run_info["status"] = status.status
            run_info["run_dir"] = str(status.run_dir) if status.run_dir else ""
            if status.end_time:
                run_info["duration"] = (status.end_time - status.start_time).total_seconds() if status.start_time else 0
            run_info["error"] = status.error or ""
    
    # Display runs table
    runs_data = []
    for run_info in st.session_state.batch_runs:
        status_emoji = {
            "pending": "🟡",
            "running": "🔵", 
            "completed": "🟢",
            "failed": "🔴"
        }.get(run_info["status"], "⚪")
        
        row = {
            "Scenario": run_info["scenario_id"],
            "File": run_info["scenario_file"],
            "Status": f"{status_emoji} {run_info['status'].upper()}",
            "Run ID": run_info["run_id"][:12] + "...",  # Truncate for display
            "Started": run_info["started_at"].strftime("%H:%M:%S"),
            "Duration": f"{run_info.get('duration', 0):.1f}s" if run_info.get('duration') else "-",
            "Run Dir": Path(run_info.get('run_dir', '')).name if run_info.get('run_dir') else "",
            "Error": run_info.get('error', '')[:50] + "..." if len(run_info.get('error', '')) > 50 else run_info.get('error', '')
        }
        runs_data.append(row)
    
    if runs_data:
        st.dataframe(
            runs_data,
            use_container_width=True,
            column_config={
                "Status": st.column_config.TextColumn("Status", width="small"),
                "Run ID": st.column_config.TextColumn("Run ID", width="medium"),
                "Started": st.column_config.TextColumn("Started", width="small"),
                "Duration": st.column_config.TextColumn("Duration", width="small"),
                "Run Dir": st.column_config.TextColumn("Run Dir", width="medium"),
                "Error": st.column_config.TextColumn("Error", width="large")
            }
        )
        
        # Quick links section
        st.subheader("Quick Actions")
        
        # Get completed runs for comparison
        completed_runs = [
            run for run in st.session_state.batch_runs 
            if run["status"] == "completed" and run.get("run_dir")
        ]
        
        if len(completed_runs) >= 2:
            col1, col2, col3 = st.columns([1, 1, 1])
            
            with col1:
                # Pre-select last two completed runs for comparison
                last_two = completed_runs[-2:]
                run_a_name = Path(last_two[0]["run_dir"]).name
                run_b_name = Path(last_two[1]["run_dir"]).name
                
                if st.button("🔍 Compare Last Two Runs"):
                    st.session_state["compare_run_a"] = run_a_name
                    st.session_state["compare_run_b"] = run_b_name
                    st.switch_page("pages/20_Compare_Runs.py")
            
            with col2:
                # Link to compare page without pre-selection
                if st.button("🔍 Compare Runs"):
                    # Clear any previous selections
                    if "compare_run_a" in st.session_state:
                        del st.session_state["compare_run_a"]
                    if "compare_run_b" in st.session_state:
                        del st.session_state["compare_run_b"]
                    st.switch_page("pages/20_Compare_Runs.py")
            
            with col3:
                # Export results summary
                if st.button("📊 Export Summary"):
                    summary_data = []
                    for run in completed_runs:
                        summary_data.append({
                            "scenario_id": run["scenario_id"],
                            "run_id": run["run_id"],
                            "run_dir": run["run_dir"],
                            "duration": run.get("duration", 0),
                            "status": run["status"]
                        })
                    
                    import json
                    summary_json = json.dumps(summary_data, indent=2, default=str)
                    st.download_button(
                        "Download Summary JSON",
                        data=summary_json,
                        file_name=f"batch_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json"
                    )
        else:
            st.info("At least 2 completed runs needed for comparison links.")
    
    # Auto-refresh logic
    if auto_refresh:
        time.sleep(5)
        st.rerun()

# Instructions
with st.expander("ℹ️ How to use", expanded=False):
    st.markdown("""
    ## Batch Scenarios Workflow
    
    1. **Configure Model**: Set model folder, main .gms file, and output settings
    2. **Select Scenarios**: Choose scenario folder and select which .yaml files to run
    3. **Run Batch**: Click "Run Selected (Async)" to start all scenarios concurrently
    4. **Monitor Progress**: Watch the status table update in real-time
    5. **Compare Results**: Use quick links to compare completed runs
    
    ## Features
    
    - **Async Execution**: All scenarios run in parallel for better performance
    - **Live Status**: Real-time updates of run progress and completion
    - **Error Tracking**: See which runs failed and why
    - **Quick Compare**: Direct links to compare completed runs
    - **Export Summary**: Download batch results as JSON
    
    ## Tips
    
    - Use auto-refresh to monitor long-running batches
    - Clear completed runs to reduce clutter
    - Check the Compare page for detailed result analysis
    """)