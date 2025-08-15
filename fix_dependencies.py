#!/usr/bin/env python3
"""
Script to fix common dependency issues with GAMS API.
This script will check and fix pandas/numpy version compatibility issues.
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, description):
    """Run a command and return success status"""
    print(f"Running: {description}")
    print(f"Command: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"✓ Success: {description}")
        if result.stdout:
            print(f"  Output: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed: {description}")
        print(f"  Error: {e.stderr.strip()}")
        return False

def check_current_versions():
    """Check current versions of key packages"""
    print("=== Current Package Versions ===")
    
    packages = ["pandas", "numpy", "gamsapi", "duckdb"]
    
    for package in packages:
        try:
            result = subprocess.run([sys.executable, "-c", f"import {package}; print({package}.__version__)"], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print(f"{package}: {result.stdout.strip()}")
            else:
                print(f"{package}: not installed")
        except Exception as e:
            print(f"{package}: error checking version - {e}")

def fix_pandas_numpy_versions():
    """Fix pandas and numpy versions for GAMS API compatibility"""
    print("\n=== Fixing pandas/numpy versions ===")
    
    # Recommended compatible versions
    compatible_versions = {
        "pandas": "1.5.3",
        "numpy": "1.24.3"
    }
    
    success = True
    
    for package, version in compatible_versions.items():
        if not run_command([
            sys.executable, "-m", "pip", "install", f"{package}=={version}", "--force-reinstall"
        ], f"Installing {package} {version}"):
            success = False
    
    return success

def verify_gams_api():
    """Verify GAMS API is working after fixes"""
    print("\n=== Verifying GAMS API ===")
    
    test_code = """
try:
    import gams
    print('GAMS import successful')
    
    ws = gams.GamsWorkspace(system_directory='C:/GAMS/49')
    print('GamsWorkspace created successfully')
    
    print('✓ GAMS API is working correctly')
except Exception as e:
    print(f'✗ GAMS API test failed: {e}')
    if 'MemoryView' in str(e) or 'buffer' in str(e).lower():
        print('This appears to be a compatibility issue')
    exit(1)
"""
    
    try:
        result = subprocess.run([sys.executable, "-c", test_code], 
                              capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print(result.stdout)
            return True
        else:
            print(f"GAMS API test failed:")
            print(result.stderr)
            return False
    except subprocess.TimeoutExpired:
        print("GAMS API test timed out")
        return False

def main():
    """Main function to fix dependencies"""
    print("GAMS API Dependency Fix Script")
    print("=" * 40)
    
    # Check current versions
    check_current_versions()
    
    # Ask user if they want to proceed
    print(f"\nThis script will:")
    print(f"1. Install pandas==1.5.3 (compatible with GAMS API)")
    print(f"2. Install numpy==1.24.3 (compatible with GAMS API)")
    print(f"3. Verify GAMS API functionality")
    
    response = input(f"\nProceed? (y/N): ").strip().lower()
    if response != 'y':
        print("Aborted by user")
        return 1
    
    # Fix versions
    if fix_pandas_numpy_versions():
        print("✓ Dependency versions updated successfully")
    else:
        print("✗ Failed to update some dependencies")
        return 1
    
    # Verify GAMS API
    if verify_gams_api():
        print("\n🎉 GAMS API is now working correctly!")
        print("\nYou can now run: python test_gams_api_fixes.py")
        return 0
    else:
        print("\n⚠ GAMS API still has issues after dependency fixes")
        print("\nNext steps:")
        print("1. Check GAMS installation")
        print("2. Verify GAMS_HOME environment variable")
        print("3. Ensure gamsapi package matches your GAMS version")
        return 1

if __name__ == "__main__":
    sys.exit(main())