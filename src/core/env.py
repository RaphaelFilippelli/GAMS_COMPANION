from __future__ import annotations
import os
from typing import Tuple, Type

DEFAULT_GAMS_HOME = r"C:\GAMS\49"

def get_gams_home() -> str:
    return os.getenv("GAMS_HOME", DEFAULT_GAMS_HOME)

def import_gams_workspace() -> Tuple[Type, str]:
    """Return (GamsWorkspace class, api_module_name).

    Uses the modern GAMS API import pattern following official documentation.
    Raises ImportError with guidance if not found.
    """
    try:
        # Modern API (GAMS 42+): Direct import from gams package
        from gams import GamsWorkspace  # type: ignore
        return GamsWorkspace, "gams"
    except ImportError as e:
        # Try legacy import as fallback
        try:
            from gams.control import GamsWorkspace  # type: ignore
            return GamsWorkspace, "gams.control"
        except ImportError:
            raise ImportError(
                "GAMS Python API not found. Ensure GAMS is installed and gamsapi package is available. "
                f"Current GAMS_HOME: {get_gams_home()}. "
                "Install with: pip install gamsapi[control]==<GAMS_VERSION>"
            ) from e

def validate_gams_api() -> bool:
    """Validate that GAMS API is properly installed and compatible."""
    try:
        GamsWorkspace, api_name = import_gams_workspace()
        
        # Test basic workspace creation
        ws = GamsWorkspace(system_directory=get_gams_home())
        
        # Check version compatibility
        if hasattr(GamsWorkspace, 'api_major_rel_number'):
            version = GamsWorkspace.api_major_rel_number
            if version < 42:
                print(f"Warning: Using older GAMS API version {version}. Consider upgrading.")
        
        print(f"GAMS API validation successful using {api_name}")
        return True
        
    except Exception as e:
        print(f"GAMS API validation failed: {e}")
        if "MemoryView" in str(e) or "buffer" in str(e).lower():
            print("This appears to be a compatibility issue with pandas/numpy versions.")
            print("Try downgrading pandas to 1.5.x and numpy to 1.24.x")
        return False
