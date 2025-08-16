"""
GAMS API wrapper following official GAMS Python API v49 documentation patterns.
Implements best practices from Control API documentation.
"""
from __future__ import annotations
import os
import sys
import tempfile
from pathlib import Path
from typing import Dict, Any, Optional, Union
import logging

logger = logging.getLogger(__name__)

class GamsApiError(Exception):
    """Custom exception for GAMS API issues"""
    pass

class GamsWorkspaceManager:
    """
    Proper GamsWorkspace management following GAMS Python API v49 documentation.
    
    Key documentation principles implemented:
    1. Always specify system_directory when possible
    2. Manage working directories properly to avoid conflicts  
    3. Handle thread safety (workspace is thread-safe, but objects are not)
    4. Follow Control API patterns exactly as documented
    """
    
    def __init__(self, system_directory: Optional[str] = None, working_directory: Optional[str] = None, debug_level: Optional[int] = None):
        """
        Initialize workspace manager following documented patterns.
        
        Args:
            system_directory: Path to GAMS system directory. If None, auto-detected per documentation.
            working_directory: Working directory for workspace. If None, uses temporary directory.
            debug_level: GAMS debug level (0-4)
        """
        self.system_directory = system_directory or self._find_gams_system_directory()
        self.working_directory = working_directory
        self.debug_level = debug_level
        self._workspace = None
        self._validated = False
        
    def _find_gams_system_directory(self) -> str:
        """
        Find GAMS system directory following documented search order.
        
        Per documentation:
        - Windows: Try to find a system directory in the Windows registry
        - Linux: Try PATH first, then LD_LIBRARY_PATH  
        - macOS: Try PATH first, then DYLD_LIBRARY_PATH
        """
        # Check environment variable first (user override)
        if "GAMS_HOME" in os.environ:
            gams_home = os.environ["GAMS_HOME"]
            if Path(gams_home).exists():
                return gams_home
        
        # Let GAMS API auto-detect (recommended approach)
        try:
            from gams import GamsWorkspace
            temp_ws = GamsWorkspace()
            return temp_ws.system_directory
        except Exception:
            pass
        
        # Fallback to common Windows locations
        if sys.platform.startswith('win'):
            common_locations = [
                r"C:\GAMS\49",
                r"C:\GAMS\50", 
                r"C:\Program Files\GAMS\49",
                r"C:\Program Files\GAMS\50"
            ]
            for location in common_locations:
                if Path(location).exists():
                    return location
                    
        # Default fallback
        raise GamsApiError("Could not find GAMS installation. Please set GAMS_HOME environment variable.")
        
    def _validate_gams_api(self) -> None:
        """Validate GAMS API availability and compatibility"""
        try:
            from gams import GamsWorkspace
            
            # Test workspace creation with our settings
            kwargs = {"system_directory": self.system_directory}
            if self.working_directory:
                kwargs["working_directory"] = self.working_directory
            if self.debug_level is not None:
                kwargs["debug"] = self.debug_level
                
            test_ws = GamsWorkspace(**kwargs)
            
            # Check API version compatibility
            if hasattr(GamsWorkspace, 'api_major_rel_number'):
                api_version = GamsWorkspace.api_major_rel_number
                if api_version < 42:
                    logger.warning(f"Using older API structure (version {api_version}). Consider upgrading.")
                    
            logger.info(f"GAMS API validation successful. System: {test_ws.system_directory}, Working: {test_ws.working_directory}")
            self._validated = True
            
        except ImportError as e:
            raise GamsApiError(f"GAMS API not available: {e}")
        except Exception as e:
            if any(keyword in str(e).lower() for keyword in ["memoryview", "buffer", "compatibility"]):
                raise GamsApiError(f"GAMS API compatibility issue (pandas/numpy version mismatch): {e}")
            raise GamsApiError(f"GAMS API validation failed: {e}")
    
    def get_workspace(self) -> 'GamsWorkspace':
        """
        Get or create GamsWorkspace following documented best practices.
        
        Returns:
            GamsWorkspace: Properly configured workspace
        """
        if not self._validated:
            self._validate_gams_api()
            
        if self._workspace is None:
            from gams import GamsWorkspace
            
            kwargs = {"system_directory": self.system_directory}
            if self.working_directory:
                kwargs["working_directory"] = self.working_directory
            if self.debug_level is not None:
                kwargs["debug"] = self.debug_level
                
            self._workspace = GamsWorkspace(**kwargs)
            logger.info(f"Created GamsWorkspace: system={self._workspace.system_directory}, working={self._workspace.working_directory}")
            
        return self._workspace


class GamsJobRunner:
    """
    GAMS job execution following Control API documentation patterns.
    
    Implements documented patterns for:
    - Creating jobs from files/strings
    - Setting options properly  
    - Running jobs with databases
    - Handling checkpoints
    """
    
    def __init__(self, workspace_manager: GamsWorkspaceManager):
        self.workspace_manager = workspace_manager
        
    def create_job_from_file(self, file_path: str, job_name: Optional[str] = None) -> 'GamsJob':
        """
        Create GamsJob from file following documented pattern.
        
        Args:
            file_path: Path to .gms file
            job_name: Optional job name
            
        Returns:
            GamsJob: Configured job ready to run
        """
        ws = self.workspace_manager.get_workspace()
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"GAMS file not found: {file_path}")
            
        try:
            if job_name:
                return ws.add_job_from_file(str(file_path), job_name=job_name)
            else:
                return ws.add_job_from_file(str(file_path))
        except Exception as e:
            raise GamsApiError(f"Failed to create job from {file_path}: {e}")
    
    def create_job_from_string(self, gams_code: str, job_name: Optional[str] = None, checkpoint: Optional['GamsCheckpoint'] = None) -> 'GamsJob':
        """
        Create GamsJob from string following documented pattern.
        
        Args:
            gams_code: GAMS code as string
            job_name: Optional job name
            checkpoint: Optional checkpoint to initialize from
            
        Returns:
            GamsJob: Configured job ready to run
        """
        ws = self.workspace_manager.get_workspace()
        
        try:
            if checkpoint:
                if job_name:
                    return ws.add_job_from_string(gams_code, checkpoint, job_name)
                else:
                    return ws.add_job_from_string(gams_code, checkpoint)
            else:
                if job_name:
                    return ws.add_job_from_string(gams_code, job_name=job_name)
                else:
                    return ws.add_job_from_string(gams_code)
        except Exception as e:
            raise GamsApiError(f"Failed to create job from string: {e}")
    
    def create_options(self, options_dict: Optional[Dict[str, Any]] = None) -> 'GamsOptions':
        """
        Create GamsOptions following documented patterns.
        
        Args:
            options_dict: Dictionary of option name -> value
            
        Returns:
            GamsOptions: Configured options object
        """
        ws = self.workspace_manager.get_workspace()
        gams_options = ws.add_options()
        
        if options_dict:
            for key, value in options_dict.items():
                try:
                    # Use proper documented option setting
                    # Convert value to string as GAMS options expect string values
                    str_value = str(value)
                    if hasattr(gams_options, key):
                        setattr(gams_options, key, str_value)
                    elif hasattr(gams_options, 'defines') and isinstance(gams_options.defines, dict):
                        # For define variables, use defines dictionary
                        gams_options.defines[key] = str_value
                    else:
                        logger.warning(f"Unknown GAMS option: {key}")
                except Exception as e:
                    logger.error(f"Failed to set option {key}={value}: {e}")
                    
        return gams_options
    
    def run_job(self, job: 'GamsJob', options: Optional[Union[Dict[str, Any], 'GamsOptions']] = None, 
                databases: Optional[Union['GamsDatabase', list]] = None, 
                checkpoint: Optional['GamsCheckpoint'] = None,
                output: Optional[Any] = None) -> None:
        """
        Run GamsJob following documented patterns.
        
        Args:
            job: GamsJob to run
            options: Options dict or GamsOptions object
            databases: Database(s) to pass to job
            checkpoint: Checkpoint to save state to
            output: Output stream for log
        """
        try:
            # Prepare arguments following documented signature
            run_kwargs = {}
            
            # Handle options
            if options:
                if isinstance(options, dict):
                    run_kwargs['gams_options'] = self.create_options(options)
                else:
                    run_kwargs['gams_options'] = options
            
            # Handle databases
            if databases:
                if isinstance(databases, list):
                    run_kwargs['databases'] = databases
                else:
                    run_kwargs['databases'] = databases
            
            # Handle checkpoint
            if checkpoint:
                run_kwargs['checkpoint'] = checkpoint
                
            # Handle output
            if output:
                run_kwargs['output'] = output
            
            # Run job with proper arguments
            job.run(**run_kwargs)
            
            logger.info(f"Job completed successfully: {job.name}")
            
        except Exception as e:
            # Collect diagnostic information
            error_info = {
                "job_name": job.name,
                "working_dir": job.workspace.working_directory,
                "system_dir": job.workspace.system_directory,
                "error": str(e)
            }
            
            raise GamsApiError(f"Job execution failed: {e}. Info: {error_info}")


class GamsDatabaseManager:
    """
    GAMS database management following Control API documentation.
    
    Implements documented patterns for:
    - Creating databases
    - Reading from GDX
    - Adding symbols properly
    """
    
    def __init__(self, workspace_manager: GamsWorkspaceManager):
        self.workspace_manager = workspace_manager
        
    def create_database(self, name: Optional[str] = None) -> 'GamsDatabase':
        """Create empty database following documented pattern"""
        ws = self.workspace_manager.get_workspace()
        if name:
            return ws.add_database(name)
        else:
            return ws.add_database()
    
    def create_database_from_gdx(self, gdx_path: str) -> 'GamsDatabase':
        """Create database from GDX following documented pattern"""
        ws = self.workspace_manager.get_workspace()
        gdx_path = Path(gdx_path)
        
        if not gdx_path.exists():
            raise FileNotFoundError(f"GDX file not found: {gdx_path}")
            
        try:
            return ws.add_database_from_gdx(str(gdx_path))
        except Exception as e:
            raise GamsApiError(f"Failed to create database from GDX {gdx_path}: {e}")


class GamsCheckpointManager:
    """
    GAMS checkpoint management following documented patterns.
    
    For efficient repeated solving and model instances.
    """
    
    def __init__(self, workspace_manager: GamsWorkspaceManager):
        self.workspace_manager = workspace_manager
        
    def create_checkpoint(self, name: Optional[str] = None) -> 'GamsCheckpoint':
        """Create checkpoint following documented pattern"""
        ws = self.workspace_manager.get_workspace()
        if name:
            return ws.add_checkpoint(name)
        else:
            return ws.add_checkpoint()


# Convenience functions following documented patterns
def create_workspace(system_directory: Optional[str] = None, working_directory: Optional[str] = None) -> GamsWorkspaceManager:
    """
    Create workspace manager following GAMS Python API v49 best practices.
    
    Args:
        system_directory: Path to GAMS installation
        working_directory: Working directory for temporary files
        
    Returns:
        GamsWorkspaceManager: Configured workspace manager
    """
    return GamsWorkspaceManager(system_directory, working_directory)


def run_gams_model(gams_file: str, 
                  options: Optional[Dict[str, Any]] = None,
                  system_directory: Optional[str] = None,
                  working_directory: Optional[str] = None) -> 'GamsJob':
    """
    Complete workflow to run GAMS model following documented patterns.
    
    Args:
        gams_file: Path to .gms file
        options: GAMS options dictionary
        system_directory: GAMS installation path
        working_directory: Working directory
        
    Returns:
        GamsJob: Completed job with results
    """
    # Create workspace manager
    workspace_mgr = create_workspace(system_directory, working_directory)
    
    # Create job runner
    job_runner = GamsJobRunner(workspace_mgr)
    
    # Create and run job
    job = job_runner.create_job_from_file(gams_file)
    job_runner.run_job(job, options)
    
    return job