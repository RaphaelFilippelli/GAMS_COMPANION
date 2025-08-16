"""
Async GAMS model runner for Streamlit integration.
Provides non-blocking execution with live log streaming.
"""
from __future__ import annotations
import asyncio
import json
import queue
import threading
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional, Callable, AsyncGenerator

from .model_runner_merg import run_gams_v49, get_run_log_txt


@dataclass
class RunStatus:
    """Status of an async GAMS run"""
    run_id: str
    status: str  # pending, running, completed, failed
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    output_gdx: Optional[Path] = None
    run_dir: Optional[Path] = None
    error: Optional[str] = None
    log_lines: list = None
    
    def __post_init__(self):
        if self.log_lines is None:
            self.log_lines = []


class AsyncGamsRunner:
    """
    Async GAMS runner with live log streaming capability.
    
    Following architecture patterns:
    - Uses run_gams_v49 for actual execution
    - Provides non-blocking execution via threading
    - Streams logs via queue mechanism
    - Maintains run status for UI integration
    """
    
    def __init__(self):
        self._runs: Dict[str, RunStatus] = {}
        self._log_queues: Dict[str, queue.Queue] = {}
        
    def start_run(
        self,
        run_id: str,
        work_dir: str,
        gms_file: str,
        gdx_out: str,
        options: Optional[Dict[str, Any]] = None,
        keep_temp: bool = False,
        scenario_id: Optional[str] = None,
        patch_path: Optional[str] = None,
    ) -> RunStatus:
        """
        Start an async GAMS run.
        
        Returns immediately with run status tracking object.
        """
        if run_id in self._runs:
            raise ValueError(f"Run {run_id} already exists")
            
        # Create run status
        status = RunStatus(
            run_id=run_id,
            status="pending",
            start_time=datetime.now()
        )
        self._runs[run_id] = status
        self._log_queues[run_id] = queue.Queue()
        
        # Start background thread
        thread = threading.Thread(
            target=self._run_thread,
            args=(run_id, work_dir, gms_file, gdx_out, options, keep_temp, scenario_id, patch_path),
            daemon=True
        )
        thread.start()
        
        return status
    
    def _run_thread(
        self,
        run_id: str,
        work_dir: str,
        gms_file: str,
        gdx_out: str,
        options: Optional[Dict[str, Any]],
        keep_temp: bool,
        scenario_id: Optional[str],
        patch_path: Optional[str],
    ):
        """Background thread that executes the GAMS run"""
        status = self._runs[run_id]
        log_queue = self._log_queues[run_id]
        
        try:
            status.status = "running"
            log_queue.put("Starting GAMS execution...")
            
            # Run GAMS using existing v49 runner
            output_gdx = run_gams_v49(
                work_dir=work_dir,
                gms_file=gms_file,
                gdx_out=gdx_out,
                options=options,
                keep_temp=keep_temp,
                scenario_id=scenario_id,
                patch_path=patch_path,
            )
            
            # Find the run directory
            run_dir = output_gdx.parent
            status.run_dir = run_dir
            status.output_gdx = output_gdx
            
            # Read log file and stream it
            log_content = get_run_log_txt(run_dir)
            if log_content and log_content != "(no listing file found)":
                # Split into lines and add to queue
                for line in log_content.split('\n'):
                    log_queue.put(line)
                    status.log_lines.append(line)
            
            status.status = "completed"
            status.end_time = datetime.now()
            log_queue.put("GAMS execution completed successfully")
            
        except Exception as e:
            status.status = "failed"
            status.end_time = datetime.now()
            status.error = str(e)
            log_queue.put(f"GAMS execution failed: {e}")
        
        finally:
            # Signal end of logs
            log_queue.put(None)
    
    def get_status(self, run_id: str) -> Optional[RunStatus]:
        """Get current status of a run"""
        return self._runs.get(run_id)
    
    def get_log_stream(self, run_id: str) -> AsyncGenerator[str, None]:
        """
        Get async generator for live log streaming.
        
        Yields log lines as they become available.
        """
        async def _stream():
            if run_id not in self._log_queues:
                return
                
            log_queue = self._log_queues[run_id]
            
            while True:
                try:
                    # Non-blocking queue get
                    line = log_queue.get_nowait()
                    if line is None:  # End signal
                        break
                    yield line
                except queue.Empty:
                    # Wait a bit and try again
                    await asyncio.sleep(0.1)
                    continue
        
        return _stream()
    
    def get_all_logs(self, run_id: str) -> list[str]:
        """Get all accumulated log lines for a run"""
        status = self.get_status(run_id)
        return status.log_lines if status else []
    
    def cleanup_run(self, run_id: str) -> None:
        """Clean up run data"""
        self._runs.pop(run_id, None)
        self._log_queues.pop(run_id, None)
    
    def list_runs(self) -> Dict[str, RunStatus]:
        """List all runs"""
        return self._runs.copy()


# Global instance for Streamlit session sharing
_global_runner: Optional[AsyncGamsRunner] = None


def get_async_runner() -> AsyncGamsRunner:
    """Get or create global async runner instance"""
    global _global_runner
    if _global_runner is None:
        _global_runner = AsyncGamsRunner()
    return _global_runner


# Convenience functions for Streamlit integration
def start_async_run(
    work_dir: str,
    gms_file: str,
    gdx_out: str,
    options: Optional[Dict[str, Any]] = None,
    run_id: Optional[str] = None,
) -> tuple[str, RunStatus]:
    """
    Start an async GAMS run.
    
    Returns (run_id, status) tuple.
    """
    if run_id is None:
        run_id = f"run_{int(time.time() * 1000)}"
    
    runner = get_async_runner()
    status = runner.start_run(
        run_id=run_id,
        work_dir=work_dir,
        gms_file=gms_file,
        gdx_out=gdx_out,
        options=options
    )
    
    return run_id, status


def get_run_status(run_id: str) -> Optional[RunStatus]:
    """Get status of a run"""
    runner = get_async_runner()
    return runner.get_status(run_id)


def get_run_logs(run_id: str) -> list[str]:
    """Get all logs for a run"""
    runner = get_async_runner()
    return runner.get_all_logs(run_id)