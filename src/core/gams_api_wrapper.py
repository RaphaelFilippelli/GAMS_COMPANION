"""
Properly structured GAMS API wrapper following official documentation patterns.
Addresses compatibility issues and implements best practices.
"""
from __future__ import annotations
import os
import sys
import tempfile
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class GamsApiError(Exception):
    """Custom exception for GAMS API issues"""
    pass

class GamsApiWrapper:
    """
    Wrapper for GAMS API that follows documented best practices and handles
    common compatibility issues.
    """
    
    def __init__(self, system_directory: Optional[str] = None, working_directory: Optional[str] = None):
        self.system_directory = system_directory or self._find_gams_system_directory()
        self.working_directory = working_directory
        self._workspace = None
        self._api_validated = False
        
    def _find_gams_system_directory(self) -> str:
        """Find GAMS system directory following documented search order"""
        # Check environment variable first
        if "GAMS_HOME" in os.environ:
            return os.environ["GAMS_HOME"]
            
        # Windows: Check registry (simplified - use common locations)
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
        return r"C:\GAMS\49"
        
    def _validate_api_compatibility(self) -> bool:
        """Validate that the GAMS API is compatible with current environment"""
        try:
            from gams import GamsWorkspace
            
            # Test basic workspace creation
            test_ws = GamsWorkspace(system_directory=self.system_directory)
            
            # Check API version compatibility
            if hasattr(GamsWorkspace, 'api_major_rel_number'):
                api_version = GamsWorkspace.api_major_rel_number
                if api_version < 42:
                    logger.warning(f"Using older API structure (version {api_version})")
                    
            logger.info(f"GAMS API validation successful. System dir: {self.system_directory}")
            return True
            
        except ImportError as e:
            raise GamsApiError(f"GAMS API not available: {e}")
        except Exception as e:
            if "MemoryView" in str(e) or "buffer" in str(e).lower():
                raise GamsApiError(f"GAMS API compatibility issue (likely pandas/numpy version mismatch): {e}")
            raise GamsApiError(f"GAMS API validation failed: {e}")
    
    def get_workspace(self) -> 'GamsWorkspace':
        """Get or create a GamsWorkspace with proper initialization"""
        if not self._api_validated:
            self._validate_api_compatibility()
            self._api_validated = True
            
        if self._workspace is None:
            from gams import GamsWorkspace
            
            kwargs = {"system_directory": self.system_directory}
            if self.working_directory:
                kwargs["working_directory"] = self.working_directory
                
            self._workspace = GamsWorkspace(**kwargs)
            logger.info(f"Created GamsWorkspace: system={self._workspace.system_directory}, working={self._workspace.working_directory}")
            
        return self._workspace
    
    def create_job_from_file(self, file_path: str, job_name: Optional[str] = None) -> 'GamsJob':
        """Create a GamsJob from file with proper error handling"""
        ws = self.get_workspace()
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
    
    def create_options(self, options_dict: Optional[Dict[str, Any]] = None) -> 'GamsOptions':
        """Create GamsOptions with proper option setting"""
        ws = self.get_workspace()
        gams_options = ws.add_options()
        
        if options_dict:
            for key, value in options_dict.items():
                try:
                    # Use proper option setting instead of setattr
                    if hasattr(gams_options, key):
                        setattr(gams_options, key, value)
                    else:
                        logger.warning(f"Unknown GAMS option: {key}")
                except Exception as e:
                    logger.error(f"Failed to set option {key}={value}: {e}")
                    
        return gams_options
    
    def run_job(self, job: 'GamsJob', options_dict: Optional[Dict[str, Any]] = None) -> None:
        """Run a GamsJob with proper options and error handling"""
        try:
            if options_dict:
                options = self.create_options(options_dict)
                job.run(options)
            else:
                job.run()
                
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
    
    def run_gams_file(self, 
                     gams_file: str, 
                     options: Optional[Dict[str, Any]] = None,
                     job_name: Optional[str] = None) -> 'GamsJob':
        """Complete workflow: create job from file and run it"""
        job = self.create_job_from_file(gams_file, job_name)
        self.run_job(job, options)
        return job

class GamsTransferWrapper:
    """
    Wrapper for GAMS Transfer API with proper usage patterns
    """
    
    def __init__(self):
        self._transfer_available = None
        
    def _check_transfer_api(self) -> bool:
        """Check if GAMS Transfer API is available"""
        if self._transfer_available is None:
            try:
                from gams import transfer
                self._transfer_available = True
                logger.info("GAMS Transfer API available")
            except ImportError as e:
                self._transfer_available = False
                logger.error(f"GAMS Transfer API not available: {e}")
                
        return self._transfer_available
    
    def create_workspace(self) -> 'transfer.Container':
        """Create a Transfer workspace (Container)"""
        if not self._check_transfer_api():
            raise GamsApiError("GAMS Transfer API not available")
            
        from gams import transfer
        return transfer.Container()
    
    def load_from_gdx(self, gdx_path: str) -> 'transfer.Container':
        """Load data from GDX file using Transfer API"""
        if not self._check_transfer_api():
            raise GamsApiError("GAMS Transfer API not available")
            
        from gams import transfer
        container = transfer.Container()
        
        try:
            container.read(gdx_path)
            logger.info(f"Successfully loaded GDX: {gdx_path}")
            return container
        except Exception as e:
            raise GamsApiError(f"Failed to load GDX {gdx_path}: {e}")

# Global instances for convenience
_default_api_wrapper = None
_default_transfer_wrapper = None

def get_default_api_wrapper(system_directory: Optional[str] = None) -> GamsApiWrapper:
    """Get the default API wrapper instance"""
    global _default_api_wrapper
    if _default_api_wrapper is None:
        _default_api_wrapper = GamsApiWrapper(system_directory=system_directory)
    return _default_api_wrapper

def get_default_transfer_wrapper() -> GamsTransferWrapper:
    """Get the default Transfer wrapper instance"""
    global _default_transfer_wrapper
    if _default_transfer_wrapper is None:
        _default_transfer_wrapper = GamsTransferWrapper()
    return _default_transfer_wrapper