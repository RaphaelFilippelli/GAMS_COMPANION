from __future__ import annotations
import streamlit as st
from pathlib import Path
import sys
import time
from datetime import datetime
sys.path.append(str(Path(__file__).parent.parent))

from core.model_runner_merg import run_gams
from core.gdx_io_merg import read_gdx_transfer, read_gdx_transfer_full, export_excel
from core.async_runner import start_async_run, get_run_status, get_run_logs
from core.provenance_integration import load_provenance_from_run_dir, create_excel_metadata

st.set_page_config(page_title="GAMS Companion", layout="wide")

# Initialize session state
if "current_run_id" not in st.session_state:
    st.session_state.current_run_id = None
if "page" not in st.session_state:
    st.session_state.page = "run"

# Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to:", ["Run Model", "Live Log", "Results"], 
                       index=["Run Model", "Live Log", "Results"].index(
                           {"run": "Run Model", "log": "Live Log", "results": "Results"}.get(st.session_state.page, "Run Model")
                       ))

# Update page state
page_map = {"Run Model": "run", "Live Log": "log", "Results": "results"}
st.session_state.page = page_map[page]

st.title("GAMS Companion — Async MVP")
st.write("Async execution with live logs and results")


def show_run_page():
    """Show the model run configuration page"""
    st.header("Run Model")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        work_dir = st.text_input("Model folder", value=str(Path("toy_model").resolve()))
        gms_file = st.text_input("Main .gms file", value="main.gms")
        gdx_out = st.text_input("Output GDX", value="results.gdx")
        lo = st.number_input("Log option (Lo)", value=2, step=1)
        
        col_run, col_sync = st.columns([1, 1])
        
        with col_run:
            if st.button("🚀 Run GAMS (Async)", type="primary"):
                try:
                    run_id, status = start_async_run(
                        work_dir=work_dir,
                        gms_file=gms_file,
                        gdx_out=gdx_out,
                        options={"Lo": int(lo)}
                    )
                    st.session_state.current_run_id = run_id
                    st.session_state.page = "log"  # Switch to log page
                    st.success(f"Started run {run_id}")
                    st.rerun()
                except Exception as e:
                    st.error(f"Failed to start run: {e}")
        
        with col_sync:
            if st.button("⏱️ Run GAMS (Sync)"):
                with st.spinner("Running GAMS…"):
                    try:
                        gdx = run_gams(work_dir, gms_file, gdx_out, options={"Lo": int(lo)})
                        st.success(f"Run OK → {gdx}")
                        st.session_state["last_gdx"] = str(gdx)
                    except Exception as e:
                        st.error(f"Run failed: {e}")
    
    with col2:
        st.subheader("Current Status")
        if st.session_state.current_run_id:
            status = get_run_status(st.session_state.current_run_id)
            if status:
                status_color = {
                    "pending": "🟡",
                    "running": "🔵", 
                    "completed": "🟢",
                    "failed": "🔴"
                }.get(status.status, "⚪")
                
                st.write(f"**Run ID:** {status.run_id}")
                st.write(f"**Status:** {status_color} {status.status.upper()}")
                if status.start_time:
                    st.write(f"**Started:** {status.start_time.strftime('%H:%M:%S')}")
                if status.end_time:
                    st.write(f"**Ended:** {status.end_time.strftime('%H:%M:%S')}")
                if status.error:
                    st.error(f"Error: {status.error}")
                    
                if status.status in ["running", "completed"]:
                    if st.button("📊 View Logs"):
                        st.session_state.page = "log"
                        st.rerun()
                        
                if status.status == "completed":
                    if st.button("📈 View Results"):
                        st.session_state.page = "results"
                        st.rerun()
        else:
            st.write("No active run")
    
    # Legacy sync results
    if "last_gdx" in st.session_state:
        st.subheader("Export Results (Sync Run)")
        gdx = st.session_state["last_gdx"]
        
        # Load data for units configuration
        try:
            sync_data = read_gdx_transfer(gdx)
            sync_numeric_symbols = [name for name, df in sync_data.items() if len(df) > 0 and 'value' in df.columns]
            
            # Units input for sync run
            sync_units = {}
            if sync_numeric_symbols:
                with st.expander("Configure Units for Sync Export", expanded=False):
                    for symbol in sync_numeric_symbols[:3]:  # Limit to 3 for sync
                        unit_input = st.text_input(
                            f"Units for '{symbol}':",
                            placeholder="e.g., MW, $/MWh",
                            key=f"sync_unit_{symbol}"
                        )
                        if unit_input.strip():
                            sync_units[symbol] = unit_input.strip()
            
            if st.button("Export Excel"):
                with st.spinner("Reading GDX and exporting to Excel..."):
                    xlsx = Path(gdx).with_suffix(".xlsx")
                    # Create comprehensive metadata for sync run
                    sync_meta = {
                        "export_type": "sync_run",
                        "source_gdx": Path(gdx).name,
                        "export_timestamp": datetime.now().isoformat(),
                        "units_applied": ", ".join(f"{k}={v}" for k, v in sync_units.items()) if sync_units else "None",
                        "symbols_count": len(sync_data),
                        "symbols_with_data": sum(1 for df in sync_data.values() if len(df) > 0)
                    }
                    
                    export_excel(
                        symbol_data=sync_data, 
                        xlsx_out=xlsx,
                        units=sync_units if sync_units else None,
                        meta=sync_meta
                    )
                    
                    # Count symbols with actual data
                    total_symbols = len(sync_data)
                    symbols_with_data = sum(1 for df in sync_data.values() if len(df) > 0)
                    
                    success_msg = f"Excel exported with {symbols_with_data}/{total_symbols} symbols containing data."
                    if sync_units:
                        success_msg += f" Units applied to: {', '.join(sync_units.keys())}"
                    
                    if symbols_with_data > 0:
                        st.success(success_msg)
                    else:
                        st.warning(f"Excel exported, but all {total_symbols} symbols are empty. This may be because the model was compiled but not solved, or the symbols contain no data.")
                    
                    with open(xlsx, "rb") as f:
                        st.download_button("Download Excel", data=f, file_name=xlsx.name)
        
        except Exception as e:
            st.error(f"Failed to load GDX data: {e}")
            if st.button("Export Excel (Fallback)"):
                # Fallback without units
                with st.spinner("Exporting without units..."):
                    data = read_gdx_transfer(gdx)
                    xlsx = Path(gdx).with_suffix(".xlsx")
                    export_excel(data, xlsx)
                    
                    with open(xlsx, "rb") as f:
                        st.download_button("Download Excel", data=f, file_name=xlsx.name)


def show_log_page():
    """Show live log streaming page"""
    st.header("Live Log")
    
    if not st.session_state.current_run_id:
        st.warning("No active run. Please start a run from the Run Model page.")
        return
        
    run_id = st.session_state.current_run_id
    status = get_run_status(run_id)
    
    if not status:
        st.error(f"Run {run_id} not found")
        return
    
    # Status display
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        status_color = {
            "pending": "🟡",
            "running": "🔵", 
            "completed": "🟢",
            "failed": "🔴"
        }.get(status.status, "⚪")
        st.metric("Status", f"{status_color} {status.status.upper()}")
        
    with col2:
        if status.start_time:
            if status.end_time:
                duration = status.end_time - status.start_time
                st.metric("Duration", f"{duration.total_seconds():.1f}s")
            else:
                duration = time.time() - status.start_time.timestamp()
                st.metric("Duration", f"{duration:.1f}s")
                
    with col3:
        if st.button("🔄 Refresh"):
            st.rerun()
    
    # Auto-refresh for running jobs
    if status.status == "running":
        time.sleep(1)
        st.rerun()
    
    # Log display
    st.subheader("Execution Log")
    logs = get_run_logs(run_id)
    
    if logs:
        # Show logs in a text area
        log_text = "\n".join(logs)
        st.text_area("Logs", value=log_text, height=400, disabled=True)
        
        # Show last few lines prominently
        if len(logs) > 5:
            st.subheader("Recent Output")
            recent_logs = logs[-5:]
            for line in recent_logs:
                if "error" in line.lower() or "failed" in line.lower():
                    st.error(line)
                elif "warning" in line.lower():
                    st.warning(line)
                elif "completed" in line.lower() or "success" in line.lower():
                    st.success(line)
                else:
                    st.code(line)
    else:
        st.info("No logs available yet...")
    
    # Navigation
    if status.status == "completed":
        if st.button("📈 View Results →"):
            st.session_state.page = "results"
            st.rerun()


def show_results_page():
    """Show results and export page"""
    st.header("Results")
    
    if not st.session_state.current_run_id:
        st.warning("No active run. Please start a run from the Run Model page.")
        return
        
    run_id = st.session_state.current_run_id
    status = get_run_status(run_id)
    
    if not status:
        st.error(f"Run {run_id} not found")
        return
        
    if status.status != "completed":
        st.warning(f"Run is {status.status}. Results only available for completed runs.")
        if status.status == "running":
            if st.button("📊 View Live Log"):
                st.session_state.page = "log"
                st.rerun()
        return
    
    if not status.output_gdx:
        st.error("No output GDX file found")
        return
    
    # Run summary
    st.subheader("Run Summary")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Run ID", run_id)
    with col2:
        duration = status.end_time - status.start_time if status.end_time and status.start_time else None
        if duration:
            st.metric("Duration", f"{duration.total_seconds():.1f}s")
    with col3:
        st.metric("Output GDX", status.output_gdx.name)
    
    # Provenance information
    if status.run_dir:
        from core.provenance_integration import get_provenance_summary
        provenance_info = get_provenance_summary(status.run_dir)
        
        if "status" not in provenance_info:  # Has valid provenance data
            with st.expander("📋 Provenance Information", expanded=False):
                st.write("**Model Reproducibility Information:**")
                
                col1, col2 = st.columns(2)
                with col1:
                    for key in ["Run ID", "Timestamp", "Main File"]:
                        if key in provenance_info:
                            st.write(f"**{key}:** {provenance_info[key]}")
                
                with col2:
                    for key in ["Model Hash", "Options", "Scenario"]:
                        if key in provenance_info:
                            st.write(f"**{key}:** {provenance_info[key]}")
                
                st.info("💡 This provenance data is automatically included in Excel exports for full reproducibility.")
    
    # Load and display data
    st.subheader("Symbol Data")
    try:
        with st.spinner("Loading GDX data..."):
            # Load full data including kinds and marginals for proper export
            data, marginals, kinds = read_gdx_transfer_full(str(status.output_gdx))
            
        if data:
            # Summary stats
            total_symbols = len(data)
            symbols_with_data = sum(1 for df in data.values() if len(df) > 0)
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Symbols", total_symbols)
            with col2:
                st.metric("Symbols with Data", symbols_with_data)
            
            # Export options
            st.subheader("Export Options")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Units configuration
                st.subheader("Excel Export Options")
                
                # Get symbols that could have units
                numeric_symbols = [name for name, df in data.items() if len(df) > 0 and 'value' in df.columns]
                
                if numeric_symbols:
                    with st.expander("Configure Units (Optional)", expanded=False):
                        st.write("Add units to value columns in Excel export:")
                        units = {}
                        
                        # Create unit inputs for up to 5 symbols (to avoid UI clutter)
                        for symbol in numeric_symbols[:5]:
                            unit_input = st.text_input(
                                f"Units for '{symbol}':",
                                placeholder="e.g., MW, $/MWh, kg/day",
                                key=f"unit_{symbol}"
                            )
                            if unit_input.strip():
                                units[symbol] = unit_input.strip()
                        
                        if len(numeric_symbols) > 5:
                            st.info(f"Showing first 5 symbols. {len(numeric_symbols) - 5} more symbols available.")
                else:
                    units = {}
                
                if st.button("📊 Export to Excel"):
                    with st.spinner("Exporting to Excel..."):
                        xlsx = status.output_gdx.with_suffix(".xlsx")
                        
                        # Load provenance data and create comprehensive metadata
                        provenance_data = load_provenance_from_run_dir(status.run_dir) if status.run_dir else None
                        duration = (status.end_time - status.start_time).total_seconds() if status.end_time and status.start_time else None
                        
                        full_meta = create_excel_metadata(
                            provenance_data=provenance_data,
                            run_id=run_id,
                            gdx_file=status.output_gdx.name,
                            units=units,
                            symbols_count=len(data),
                            symbols_with_data=symbols_with_data,
                            duration_seconds=duration
                        )
                        
                        # Export with comprehensive metadata
                        export_excel(
                            symbol_data=data, 
                            xlsx_out=xlsx,
                            units=units if units else None,
                            meta=full_meta
                        )
                        
                        with open(xlsx, "rb") as f:
                            st.download_button(
                                "📥 Download Excel", 
                                data=f.read(), 
                                file_name=xlsx.name,
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                            )
                        
                        success_msg = f"Excel exported with {symbols_with_data}/{total_symbols} symbols containing data."
                        if units:
                            success_msg += f" Units applied to: {', '.join(units.keys())}"
                        
                        if symbols_with_data > 0:
                            st.success(success_msg)
                        else:
                            st.warning(f"Excel exported, but all {total_symbols} symbols are empty.")
            
            with col2:
                if st.button("🗃️ Export to DuckDB"):
                    with st.spinner("Exporting to DuckDB..."):
                        try:
                            from core.gdx_io_merg import to_duckdb
                            db_path = status.output_gdx.with_suffix(".duckdb")
                            # Pass all required parameters to avoid MemoryView errors
                            to_duckdb(
                                symbol_values=data, 
                                db_path=db_path,
                                symbol_marginals=marginals,
                                kinds=kinds,
                                run_meta={"run_id": run_id, "timestamp": status.start_time.isoformat() if status.start_time else None}
                            )
                            st.success(f"Data exported to {db_path}")
                        except Exception as e:
                            st.error(f"DuckDB export failed: {e}")
                            # Provide fallback information
                            st.info("This may be due to pandas/numpy version compatibility. Try upgrading: pip install 'pandas>=2.0' 'numpy>=1.24'")
            
            # Show data preview
            st.subheader("Data Preview")
            
            if symbols_with_data > 0:
                # Select symbol to preview
                symbols_with_data_list = [name for name, df in data.items() if len(df) > 0]
                selected_symbol = st.selectbox("Select symbol to preview:", symbols_with_data_list)
                
                if selected_symbol:
                    df = data[selected_symbol]
                    st.write(f"**{selected_symbol}** ({len(df)} rows)")
                    st.dataframe(df, use_container_width=True)
            else:
                st.info("No symbols contain data to preview.")
        else:
            st.warning("No data found in GDX file")
            
    except Exception as e:
        st.error(f"Failed to load results: {e}")


# Page routing
if st.session_state.page == "run":
    show_run_page()
elif st.session_state.page == "log":
    show_log_page()
elif st.session_state.page == "results":
    show_results_page()

st.caption("Tip: use the bundled toy model to validate your setup.")