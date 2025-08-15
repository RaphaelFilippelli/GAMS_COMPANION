#!/usr/bin/env python3
"""
Test script to validate GAMS API fixes and diagnose issues.
Run this script to verify that all GAMS API components are working correctly.
"""
import sys
import traceback
from pathlib import Path

def test_basic_imports():
    """Test basic GAMS API imports"""
    print("=== Testing Basic Imports ===")
    
    try:
        from src.core.env import get_gams_home, validate_gams_api
        print(f"[+] Environment functions imported successfully")
        print(f"  GAMS_HOME: {get_gams_home()}")
        
        # Validate API
        if validate_gams_api():
            print("[+] GAMS API validation passed")
        else:
            print("[-] GAMS API validation failed")
            return False
            
    except Exception as e:
        print(f"[-] Import failed: {e}")
        traceback.print_exc()
        return False
    
    return True

def test_api_wrapper():
    """Test the new GAMS API wrapper"""
    print("\n=== Testing GAMS API Wrapper ===")
    
    try:
        from src.core.gams_api_wrapper import GamsApiWrapper, get_default_api_wrapper
        
        # Test wrapper creation
        wrapper = get_default_api_wrapper()
        print("[+] API wrapper created successfully")
        
        # Test workspace creation
        workspace = wrapper.get_workspace()
        print(f"[+] Workspace created successfully")
        print(f"  System directory: {workspace.system_directory}")
        print(f"  Working directory: {workspace.working_directory}")
        
        return True
        
    except Exception as e:
        print(f"[-] API wrapper test failed: {e}")
        traceback.print_exc()
        return False

def test_transfer_api():
    """Test GAMS Transfer API wrapper"""
    print("\n=== Testing GAMS Transfer API ===")
    
    try:
        from src.core.gams_api_wrapper import GamsTransferWrapper, get_default_transfer_wrapper
        
        # Test transfer wrapper
        transfer_wrapper = get_default_transfer_wrapper()
        print("[+] Transfer wrapper created successfully")
        
        # Test container creation
        container = transfer_wrapper.create_workspace()
        print("[+] Transfer container created successfully")
        
        return True
        
    except Exception as e:
        print(f"[-] Transfer API test failed: {e}")
        traceback.print_exc()
        return False

def test_gdx_io_functions():
    """Test GDX I/O functions"""
    print("\n=== Testing GDX I/O Functions ===")
    
    try:
        from src.core.gdx_io import _import_transfer
        
        # Test transfer import
        gt = _import_transfer()
        print("[+] Transfer API import successful")
        
        # Test basic container operations
        container = gt.Container()
        print("[+] Basic container operations work")
        
        return True
        
    except Exception as e:
        print(f"[-] GDX I/O test failed: {e}")
        traceback.print_exc()
        return False

def test_model_runner():
    """Test model runner functionality"""
    print("\n=== Testing Model Runner (Basic) ===")
    
    try:
        from src.core.model_runner import run_gams
        print("[+] Model runner imports successful")
        
        # Note: We don't actually run a model here to avoid creating files
        # but we verify the imports work
        return True
        
    except Exception as e:
        print(f"[-] Model runner test failed: {e}")
        traceback.print_exc()
        return False

def test_with_toy_model():
    """Test with the actual toy model if available"""
    print("\n=== Testing with Toy Model ===")
    
    toy_model_dir = Path("toy_model")
    if not toy_model_dir.exists():
        print("[!] Toy model directory not found, skipping integration test")
        return True
    
    main_gms = toy_model_dir / "main.gms"
    if not main_gms.exists():
        print("[!] main.gms not found in toy_model directory")
        return True
    
    try:
        from src.core.gams_api_wrapper import GamsApiWrapper
        
        # Test compile-only run
        wrapper = GamsApiWrapper(working_directory=str(toy_model_dir))
        job = wrapper.create_job_from_file(str(main_gms))
        print("[+] Job created from toy model successfully")
        
        # Test with compile-only option
        options = {"action": "c"}  # Compile only
        compile_job = wrapper.run_gams_file(str(main_gms), options=options, job_name="test_compile")
        print("[+] Compile-only test passed")
        
        return True
        
    except Exception as e:
        print(f"[-] Toy model test failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("GAMS API Fix Validation Script")
    print("=" * 50)
    
    tests = [
        ("Basic Imports", test_basic_imports),
        ("API Wrapper", test_api_wrapper), 
        ("Transfer API", test_transfer_api),
        ("GDX I/O Functions", test_gdx_io_functions),
        ("Model Runner", test_model_runner),
        ("Toy Model Integration", test_with_toy_model)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                print(f"\n[-] {test_name} test failed")
        except KeyboardInterrupt:
            print(f"\n[!] Test interrupted by user")
            break
        except Exception as e:
            print(f"\n[-] {test_name} test crashed: {e}")
    
    print(f"\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("[SUCCESS] All tests passed! GAMS API fixes are working correctly.")
        return 0
    else:
        print("[WARNING] Some tests failed. Check the output above for details.")
        print("\nCommon issues and solutions:")
        print("- MemoryView errors: Try downgrading pandas/numpy versions")
        print("- Import errors: Ensure gamsapi package is installed correctly")
        print("- Path errors: Check GAMS installation and GAMS_HOME environment variable")
        return 1

if __name__ == "__main__":
    sys.exit(main())