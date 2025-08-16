"""
Tests for async GAMS runner functionality.
"""
import pytest
import tempfile
import time
from pathlib import Path

from src.core.async_runner import AsyncGamsRunner, RunStatus, start_async_run, get_run_status


class TestAsyncGamsRunner:
    """Test async GAMS runner functionality"""
    
    def setup_method(self):
        """Setup for each test"""
        self.runner = AsyncGamsRunner()
    
    def test_run_status_creation(self):
        """Test RunStatus creation and properties"""
        status = RunStatus(
            run_id="test_run",
            status="pending"
        )
        
        assert status.run_id == "test_run"
        assert status.status == "pending"
        assert status.log_lines == []
        assert status.start_time is None
        assert status.end_time is None
        assert status.output_gdx is None
        assert status.error is None
    
    def test_runner_initialization(self):
        """Test runner initialization"""
        assert len(self.runner._runs) == 0
        assert len(self.runner._log_queues) == 0
    
    def test_start_run_creates_status(self):
        """Test that starting a run creates proper status"""
        # Use a simple test case that should fail quickly
        status = self.runner.start_run(
            run_id="test_001",
            work_dir="nonexistent_dir",
            gms_file="nonexistent.gms", 
            gdx_out="test.gdx"
        )
        
        assert status.run_id == "test_001"
        assert status.status in ["pending", "running"]  # May transition quickly
        assert status.start_time is not None
        
        # Check that run is tracked
        assert "test_001" in self.runner._runs
        assert "test_001" in self.runner._log_queues
    
    def test_duplicate_run_id_raises_error(self):
        """Test that duplicate run IDs raise an error"""
        self.runner.start_run(
            run_id="duplicate",
            work_dir="test",
            gms_file="test.gms",
            gdx_out="test.gdx"
        )
        
        with pytest.raises(ValueError, match="Run duplicate already exists"):
            self.runner.start_run(
                run_id="duplicate",
                work_dir="test",
                gms_file="test.gms", 
                gdx_out="test.gdx"
            )
    
    def test_get_status(self):
        """Test getting run status"""
        # Non-existent run
        assert self.runner.get_status("nonexistent") is None
        
        # Create a run
        status = self.runner.start_run(
            run_id="status_test",
            work_dir="test",
            gms_file="test.gms",
            gdx_out="test.gdx"
        )
        
        # Get status
        retrieved = self.runner.get_status("status_test")
        assert retrieved is not None
        assert retrieved.run_id == "status_test"
        assert retrieved.status in ["pending", "running", "failed"]  # May transition quickly
    
    def test_get_all_logs_empty(self):
        """Test getting logs for run with no logs"""
        status = self.runner.start_run(
            run_id="log_test",
            work_dir="test",
            gms_file="test.gms",
            gdx_out="test.gdx"
        )
        
        logs = self.runner.get_all_logs("log_test")
        assert logs == []
    
    def test_cleanup_run(self):
        """Test cleaning up run data"""
        self.runner.start_run(
            run_id="cleanup_test",
            work_dir="test",
            gms_file="test.gms",
            gdx_out="test.gdx"
        )
        
        assert "cleanup_test" in self.runner._runs
        assert "cleanup_test" in self.runner._log_queues
        
        self.runner.cleanup_run("cleanup_test")
        
        assert "cleanup_test" not in self.runner._runs
        assert "cleanup_test" not in self.runner._log_queues
    
    def test_list_runs(self):
        """Test listing all runs"""
        # Empty initially
        runs = self.runner.list_runs()
        assert len(runs) == 0
        
        # Add some runs
        self.runner.start_run("run1", "test", "test.gms", "test.gdx")
        self.runner.start_run("run2", "test", "test.gms", "test.gdx")
        
        runs = self.runner.list_runs()
        assert len(runs) == 2
        assert "run1" in runs
        assert "run2" in runs
    
    @pytest.mark.skipif(
        not Path("toy_model").exists(),
        reason="toy_model directory not found - skipping integration test"
    )
    def test_successful_run_integration(self):
        """Integration test with toy model (if available)"""
        status = self.runner.start_run(
            run_id="integration_test",
            work_dir="toy_model",
            gms_file="main.gms",
            gdx_out="results.gdx",
            options={"Lo": 2}
        )
        
        assert status.status in ["pending", "running"]  # May transition quickly
        
        # Wait for completion (with timeout)
        max_wait = 30  # 30 seconds max
        start_time = time.time()
        
        while time.time() - start_time < max_wait:
            status = self.runner.get_status("integration_test")
            if status.status in ["completed", "failed"]:
                break
            time.sleep(0.5)
        
        # Check final status
        final_status = self.runner.get_status("integration_test")
        assert final_status.status in ["completed", "failed"]
        assert final_status.end_time is not None
        
        if final_status.status == "completed":
            assert final_status.output_gdx is not None
            assert final_status.output_gdx.exists()
            
        # Check logs were captured
        logs = self.runner.get_all_logs("integration_test")
        assert len(logs) > 0


class TestConvenienceFunctions:
    """Test convenience functions for Streamlit integration"""
    
    def test_start_async_run_generates_id(self):
        """Test that start_async_run generates ID when not provided"""
        run_id, status = start_async_run(
            work_dir="test",
            gms_file="test.gms", 
            gdx_out="test.gdx"
        )
        
        assert run_id.startswith("run_")
        assert status.run_id == run_id
    
    def test_start_async_run_uses_provided_id(self):
        """Test that start_async_run uses provided ID"""
        run_id, status = start_async_run(
            work_dir="test",
            gms_file="test.gms",
            gdx_out="test.gdx",
            run_id="custom_id"
        )
        
        assert run_id == "custom_id"
        assert status.run_id == "custom_id"
    
    def test_get_run_status_function(self):
        """Test get_run_status convenience function"""
        # Non-existent run
        assert get_run_status("nonexistent") is None
        
        # Create run
        run_id, _ = start_async_run(
            work_dir="test",
            gms_file="test.gms",
            gdx_out="test.gdx"
        )
        
        # Get status
        status = get_run_status(run_id)
        assert status is not None
        assert status.run_id == run_id


class TestRunStatusDataclass:
    """Test RunStatus dataclass functionality"""
    
    def test_default_log_lines(self):
        """Test that log_lines defaults to empty list"""
        status = RunStatus(run_id="test", status="pending")
        assert status.log_lines == []
        assert isinstance(status.log_lines, list)
    
    def test_log_lines_provided(self):
        """Test that provided log_lines are preserved"""
        logs = ["line1", "line2"]
        status = RunStatus(run_id="test", status="pending", log_lines=logs)
        assert status.log_lines == logs
    
    def test_status_transitions(self):
        """Test typical status transitions"""
        status = RunStatus(run_id="test", status="pending")
        
        # Simulate status transitions
        status.status = "running"
        assert status.status == "running"
        
        status.status = "completed"
        assert status.status == "completed"
        
        status.status = "failed"
        assert status.status == "failed"