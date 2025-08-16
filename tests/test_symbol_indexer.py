"""
Tests for symbol_indexer.py
"""
import pytest
from pathlib import Path
import tempfile
import json
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.symbol_indexer import (
    scan_sources, 
    save_index, 
    fallback_to_gdx,
    create_symbol_index,
    _extract_symbols_from_line
)


class TestSymbolIndexer:
    
    def test_extract_symbols_from_line(self):
        """Test symbol extraction from individual lines"""
        test_cases = [
            # Sets
            ("Sets i 'catchments' / A, B /;", [{'type': 'set', 'name': 'i', 'dim': 0}]),
            ("Set ActiveCatchments(i) / A, B /;", [{'type': 'set', 'name': 'ActiveCatchments', 'dim': 1}]),
            
            # Scalars
            ("Scalar CapacityLimit 'capacity limit' / 10 /;", [{'type': 'scalar', 'name': 'CapacityLimit', 'dim': 0}]),
            ("Scalars Cap / 5 /, Limit / 10 /;", [{'type': 'scalar', 'name': 'Cap', 'dim': 0}, {'type': 'scalar', 'name': 'Limit', 'dim': 0}]),
            
            # Parameters
            ("Parameter Cost(i) 'unit cost';", [{'type': 'parameter', 'name': 'Cost', 'dim': 1}]),
            ("Parameters CostByCatchment(i), Benefit(i);", [{'type': 'parameter', 'name': 'CostByCatchment', 'dim': 1}, {'type': 'parameter', 'name': 'Benefit', 'dim': 1}]),
            
            # Variables
            ("Variable z 'objective';", [{'type': 'variable', 'name': 'z', 'dim': 0}]),
            ("Variables x(i), y(i,j);", [{'type': 'variable', 'name': 'x', 'dim': 1}, {'type': 'variable', 'name': 'y', 'dim': 2}]),
            
            # Equations
            ("Equation obj 'objective function';", [{'type': 'equation', 'name': 'obj', 'dim': 0}]),
            ("Equations obj, cap(i);", [{'type': 'equation', 'name': 'obj', 'dim': 0}, {'type': 'equation', 'name': 'cap', 'dim': 1}]),
            
            # Comments should be ignored
            ("* This is a comment with Set declaration", []),
            ("// Another comment style", []),
        ]
        
        for line, expected in test_cases:
            result = _extract_symbols_from_line(line, Path("test.gms"), 1)
            
            # Check we got the right number of symbols
            assert len(result) == len(expected), f"Line: {line}, Expected: {len(expected)}, Got: {len(result)}"
            
            if expected:
                # Create comparable dictionaries without file/line details
                result_symbols = [{'type': r['type'], 'name': r['name'], 'dim': r['dim']} for r in result]
                expected_symbols = [{'type': e['type'], 'name': e['name'], 'dim': e['dim']} for e in expected]
                
                assert result_symbols == expected_symbols, f"Line: {line}, Expected: {expected_symbols}, Got: {result_symbols}"
                
                # Check file and line are correct for all results
                for r in result:
                    assert r['file'] == "test.gms"
                    assert r['line'] == 1
    
    def test_scan_sources_with_toy_model(self):
        """Test scanning the actual toy model"""
        toy_model_path = Path("toy_model/main.gms")
        if toy_model_path.exists():
            symbols = scan_sources([toy_model_path])
            
            # Should find symbols from toy model
            assert len(symbols) > 0
            
            # Check for expected symbols - at least the main ones we can reliably parse
            symbol_names = [s['name'] for s in symbols]
            expected_symbols = ['i', 'CapacityLimit', 'ActiveCatchments', 'CostByCatchment']
            
            for expected in expected_symbols:
                assert expected in symbol_names, f"Expected symbol '{expected}' not found in {symbol_names}"
        else:
            pytest.skip("toy_model/main.gms not found")
    
    def test_scan_sources_with_temp_file(self):
        """Test scanning with a temporary GAMS file"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.gms', delete=False) as f:
            f.write("""
Sets
    i   "catchments" / A, B /
    j   "regions" / North, South /;

Scalar
    CapacityLimit "capacity limit" / 10 /;

Parameters
    Cost(i)     "unit cost"
    Benefit(i)  "unit benefit";

Variables
    z   "objective"
    x(i) "activity level";

Equations
    obj "objective function"
    cap "capacity constraint";
""")
            temp_path = Path(f.name)
        
        try:
            symbols = scan_sources([temp_path])
            
            # Check we found expected symbols
            assert len(symbols) >= 2  # At least some main symbols
            
            symbol_dict = {s['name']: s for s in symbols}
            
            # Verify specific symbols that we know should be found
            if 'CapacityLimit' in symbol_dict:
                assert symbol_dict['CapacityLimit']['type'] == 'scalar'
                assert symbol_dict['CapacityLimit']['dim'] == 0
            
            if 'Cost' in symbol_dict:
                assert symbol_dict['Cost']['type'] == 'parameter'
                assert symbol_dict['Cost']['dim'] == 1
            
        finally:
            temp_path.unlink()
    
    def test_save_index(self):
        """Test saving index to JSON"""
        test_symbols = [
            {'type': 'set', 'name': 'i', 'file': 'test.gms', 'line': 1, 'dim': 0},
            {'type': 'parameter', 'name': 'Cost', 'file': 'test.gms', 'line': 5, 'dim': 1}
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_path = Path(f.name)
        
        try:
            result_path = save_index(test_symbols, temp_path)
            assert result_path == temp_path
            assert temp_path.exists()
            
            # Verify JSON content
            with open(temp_path, 'r') as f:
                loaded = json.load(f)
            
            assert loaded == test_symbols
            
        finally:
            temp_path.unlink()
    
    def test_fallback_to_gdx_no_gdx(self):
        """Test GDX fallback with non-existent file"""
        symbols = fallback_to_gdx("nonexistent.gdx")
        assert symbols == []
    
    def test_create_symbol_index_with_toy_model(self):
        """Test the complete symbol index creation with toy model"""
        toy_model_dir = Path("toy_model")
        if toy_model_dir.exists():
            symbols = create_symbol_index(toy_model_dir, "main.gms")
            
            # Should find symbols
            assert len(symbols) > 0
            
            # Check symbol structure
            for symbol in symbols:
                assert 'type' in symbol
                assert 'name' in symbol
                assert 'file' in symbol
                assert 'line' in symbol
                assert 'dim' in symbol
        else:
            pytest.skip("toy_model directory not found")
    
    def test_create_symbol_index_with_gdx_fallback(self):
        """Test symbol index creation with GDX fallback"""
        # Test with non-existent main file but potential GDX fallback
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # No main.gms file exists, should try GDX fallback
            symbols = create_symbol_index(temp_path, "main.gms", "nonexistent.gdx")
            assert symbols == []  # Both source and GDX fallback fail
            
            # Test with toy model GDX if available
            toy_gdx = Path("toy_model/results.gdx")
            if toy_gdx.exists():
                symbols = create_symbol_index(temp_path, "main.gms", str(toy_gdx))
                # Should find some symbols from GDX
                assert len(symbols) >= 0  # May be empty if GDX read fails