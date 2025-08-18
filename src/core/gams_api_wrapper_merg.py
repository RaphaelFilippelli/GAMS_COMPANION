"""
GAMS API wrapper following official GAMS Python API v49 documentation patterns.
Merged version combining best practices from gams_api_wrapper.py and gams_api_wrapper_v49.py.
Implements best practices from Control API documentation.
"""
from __future__ import annotations
import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional, Union
import logging

logger = logging.getLogger(__name__)

class GamsApiError(Exception):
    """Custom exception for GAMS API issues"""
    pass

def _is_lo_key(k: str) -> bool:
    return str(k).lower() in ("lo", "logoption", "log")

def options_to_cli_args(options: Optional[Dict[str, Any]]) -> list[str]:
    """
    Build command-line args for gams.exe from a Python dict.
    Special-cases LogOption/LO to ensure the canonical 'LO=<int>' form.
    """
    args: list[str] = []
    if not options:
        return args
    for k, v in options.items():
        if _is_lo_key(k):
            args.append(f"LO={v}")
        else:
            args.append(f"{k}={v}")
    return args

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

            # Informational (some builds expose this constant)
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
    """

    def __init__(self, workspace_manager: GamsWorkspaceManager):
        self.workspace_manager = workspace_manager

    def create_job_from_file(self, file_path: str, job_name: Optional[str] = None) -> 'GamsJob':
        """
        Create GamsJob from file following documented pattern.
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

        NOTE: LO/LogOption is a command-line parameter only. We deliberately
        ignore any 'Lo'/'lo'/'logoption' keys here to avoid "Unknown GAMS option" warnings.
        """
        ws = self.workspace_manager.get_workspace()
        gams_options = ws.add_options()

        if options_dict:
            for key, value in options_dict.items():
                # Skip LO/LogOption: not a GamsOptions attribute
                if _is_lo_key(key):
                    logger.debug("Ignoring LO/LogOption in GamsOptions (CLI-only parameter).")
                    continue
                try:
                    str_value = str(value)
                    if hasattr(gams_options, key):
                        setattr(gams_options, key, str_value)
                    elif hasattr(gams_options, 'defines') and isinstance(gams_options.defines, dict):
                        # Only use defines for explicit macro definitions, not for unknown options
                        logger.warning(f"Unknown GAMS option: {key} (not setting as define)")
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
        """
        try:
            run_kwargs = {}
            if options:
                if isinstance(options, dict):
                    run_kwargs['gams_options'] = self.create_options(options)
                else:
                    run_kwargs['gams_options'] = options
            if databases:
                run_kwargs['databases'] = databases if isinstance(databases, list) else [databases]
            if checkpoint:
                run_kwargs['checkpoint'] = checkpoint
            if output:
                run_kwargs['output'] = output
            job.run(**run_kwargs)
            logger.info(f"Job completed successfully: {job.name}")
        except Exception as e:
            error_info = {
                "job_name": getattr(job, "name", "(unknown)"),
                "working_dir": getattr(getattr(job, "workspace", None), "working_directory", "(unknown)"),
                "system_dir": getattr(getattr(job, "workspace", None), "system_directory", "(unknown)"),
                "error": str(e)
            }
            raise GamsApiError(f"Job execution failed: {e}. Info: {error_info}")


class GamsDatabaseManager:
    """
    GAMS database management following Control API documentation.
    """

    def __init__(self, workspace_manager: GamsWorkspaceManager):
        self.workspace_manager = workspace_manager

    def create_database(self, name: Optional[str] = None) -> 'GamsDatabase':
        ws = self.workspace_manager.get_workspace()
        return ws.add_database(name) if name else ws.add_database()

    def create_database_from_gdx(self, gdx_path: str) -> 'GamsDatabase':
        ws = self.workspace_manager.get_workspace()
        gdx_path = Path(gdx_path)
        if not gdx_path.exists():
            raise FileNotFoundError(f"GDX file not found: {gdx_path}")
        try:
            return ws.add_database_from_gdx(str(gdx_path))
        except Exception as e:
            raise GamsApiError(f"Failed to create database from GDX {gdx_path}: {e}")


class GamsCheckpointManager:
    """GAMS checkpoint management following documented patterns."""
    def __init__(self, workspace_manager: GamsWorkspaceManager):
        self.workspace_manager = workspace_manager
    def create_checkpoint(self, name: Optional[str] = None) -> 'GamsCheckpoint':
        ws = self.workspace_manager.get_workspace()
        return ws.add_checkpoint(name) if name else ws.add_checkpoint()


# Legacy compatibility wrapper
class GamsApiWrapper:
    """
    Legacy compatibility wrapper that provides the same interface as the original GamsApiWrapper.
    """
    def __init__(self, system_directory: Optional[str] = None, working_directory: Optional[str] = None):
        self.workspace_manager = GamsWorkspaceManager(system_directory, working_directory)
        self.job_runner = GamsJobRunner(self.workspace_manager)
        self.system_directory = self.workspace_manager.system_directory
        self.working_directory = working_directory

    def get_workspace(self) -> 'GamsWorkspace':
        return self.workspace_manager.get_workspace()
    def create_job_from_file(self, file_path: str, job_name: Optional[str] = None) -> 'GamsJob':
        return self.job_runner.create_job_from_file(file_path, job_name)
    def create_options(self, options_dict: Optional[Dict[str, Any]] = None) -> 'GamsOptions':
        return self.job_runner.create_options(options_dict)
    def run_job(self, job: 'GamsJob', options_dict: Optional[Dict[str, Any]] = None) -> None:
        self.job_runner.run_job(job, options_dict)
    def run_gams_file(self, gams_file: str, options: Optional[Dict[str, Any]] = None, job_name: Optional[str] = None) -> 'GamsJob':
        job = self.create_job_from_file(gams_file, job_name)
        self.run_job(job, options)
        return job


def create_workspace(system_directory: Optional[str] = None, working_directory: Optional[str] = None) -> GamsWorkspaceManager:
    """Create workspace manager following GAMS Python API v49 best practices."""
    return GamsWorkspaceManager(system_directory, working_directory)

def run_gams_model(gams_file: str, options: Optional[Dict[str, Any]] = None, system_directory: Optional[str] = None, working_directory: Optional[str] = None) -> 'GamsJob':
    """Complete workflow to run GAMS model following documented patterns."""
    workspace_mgr = create_workspace(system_directory, working_directory)
    job_runner = GamsJobRunner(workspace_mgr)
    job = job_runner.create_job_from_file(gams_file)
    job_runner.run_job(job, options)
    return job

def get_default_api_wrapper(system_directory: Optional[str] = None) -> GamsApiWrapper:
    """Get the default API wrapper instance (legacy compatibility)."""
    return GamsApiWrapper(system_directory=system_directory)


class GamsTransferWrapper:
    """
    Legacy compatibility wrapper for Transfer API functionality.
    Note: For new code, use gdx_io_merg.py.
    """
    def __init__(self):
        self._transfer_available = None
    def _check_transfer_api(self) -> bool:
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
        if not self._check_transfer_api():
            raise GamsApiError("GAMS Transfer API not available")
        from gams import transfer
        return transfer.Container()
    def load_from_gdx(self, gdx_path: str) -> 'transfer.Container':
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
def get_default_transfer_wrapper() -> GamsTransferWrapper:
    """Get the default Transfer wrapper instance (legacy compatibility)"""
    return GamsTransferWrapper()
