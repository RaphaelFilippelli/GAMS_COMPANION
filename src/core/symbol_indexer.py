"""
Symbol indexer for GAMS source files with GDX fallback.
Follows spec in symbol_indexer_spec.md.
"""
from __future__ import annotations
from pathlib import Path
from typing import Dict, List, Optional, Union
import re
import json

try:
    from .gdx_io_merg import read_gdx_transfer_full
except ImportError:
    # Fallback for testing
    def read_gdx_transfer_full(*args, **kwargs):
        return {}, {}, {}


def scan_sources(files: List[Union[str, Path]]) -> List[Dict]:
    """
    Scan GAMS source files for symbol declarations.
    
    Args:
        files: List of GAMS source files to scan
        
    Returns:
        List of symbol dictionaries with {type, name, file, line, dim}
    """
    symbols = []
    processed_files = set()
    
    for file_path in files:
        symbols.extend(_scan_file(Path(file_path), processed_files, depth=0))
    
    return symbols


def _scan_file(file_path: Path, processed_files: set, depth: int = 0) -> List[Dict]:
    """
    Recursively scan a single GAMS file and its includes.
    
    Args:
        file_path: Path to GAMS file
        processed_files: Set of already processed files to avoid cycles
        depth: Current include depth (max 3)
        
    Returns:
        List of symbol dictionaries
    """
    if depth > 3 or file_path in processed_files or not file_path.exists():
        return []
    
    processed_files.add(file_path)
    symbols = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except (UnicodeDecodeError, OSError):
        return []
    
    # Split into lines for processing
    lines = content.splitlines()
    
    # Track multi-line symbol declarations
    current_declaration = None
    declaration_start_line = 0
    
    for line_num, line in enumerate(lines, 1):
        line_stripped = line.strip()
        
        # Skip comments
        if line_stripped.startswith('*') or line_stripped.startswith('//'):
            continue
            
        # Process includes
        include_match = re.search(r'\$include\s+["\']?([^"\';\s]+)["\']?', line, re.IGNORECASE)
        if include_match:
            include_file = file_path.parent / include_match.group(1)
            symbols.extend(_scan_file(include_file, processed_files, depth + 1))
            continue
        
        # Check if this line starts a new symbol declaration
        new_declaration = _detect_symbol_declaration_start(line)
        if new_declaration:
            # If we have a pending declaration, process it
            if current_declaration:
                symbols.extend(_process_multi_line_declaration(current_declaration, file_path, declaration_start_line))
            
            # Start new declaration
            current_declaration = {'type': new_declaration, 'lines': [line], 'complete': ';' in line}
            declaration_start_line = line_num
        elif current_declaration:
            # Continue existing declaration
            current_declaration['lines'].append(line)
            if ';' in line:
                current_declaration['complete'] = True
        
        # If declaration is complete, process it
        if current_declaration and current_declaration['complete']:
            symbols.extend(_process_multi_line_declaration(current_declaration, file_path, declaration_start_line))
            current_declaration = None
        
        # Also try single-line processing for simple cases
        symbols.extend(_extract_symbols_from_line(line, file_path, line_num))
    
    # Process any remaining declaration
    if current_declaration:
        symbols.extend(_process_multi_line_declaration(current_declaration, file_path, declaration_start_line))
    
    return symbols


def _detect_symbol_declaration_start(line: str) -> Optional[str]:
    """Detect if a line starts a symbol declaration block."""
    line_lower = line.lower().strip()
    
    if re.match(r'\bsets?\s*$', line_lower):
        return 'set'
    elif re.match(r'\bset\s*$', line_lower):
        return 'set' 
    elif re.match(r'\bscalars?\s*$', line_lower):
        return 'scalar'
    elif re.match(r'\bscalar\s*$', line_lower):
        return 'scalar'
    elif re.match(r'\bparameters?\s*$', line_lower):
        return 'parameter'
    elif re.match(r'\bparameter\s*$', line_lower):
        return 'parameter'
    elif re.match(r'\bvariables?\s*$', line_lower):
        return 'variable'
    elif re.match(r'\bvariable\s*$', line_lower):
        return 'variable'
    elif re.match(r'\bequations?\s*$', line_lower):
        return 'equation'
    elif re.match(r'\bequation\s*$', line_lower):
        return 'equation'
    
    return None


def _process_multi_line_declaration(declaration: Dict, file_path: Path, start_line: int) -> List[Dict]:
    """Process a multi-line symbol declaration."""
    symbols = []
    symbol_type = declaration['type']
    
    # Join all lines and extract symbols
    full_text = ' '.join(declaration['lines'])
    
    # Remove the keyword from the beginning
    patterns = [
        r'\bsets?\s*',
        r'\bset\s*', 
        r'\bscalars?\s*',
        r'\bscalar\s*',
        r'\bparameters?\s*',
        r'\bparameter\s*',
        r'\bvariables?\s*',
        r'\bvariable\s*',
        r'\bequations?\s*',
        r'\bequation\s*'
    ]
    
    for pattern in patterns:
        full_text = re.sub(pattern, '', full_text, flags=re.IGNORECASE)
    
    # Parse symbols from the remaining text
    parsed_symbols = _parse_symbol_declarations(full_text, symbol_type)
    
    for name, dim in parsed_symbols:
        symbols.append({
            'type': symbol_type,
            'name': name,
            'file': str(file_path),
            'line': start_line,
            'dim': dim
        })
    
    return symbols


def _extract_symbols_from_line(line: str, file_path: Path, line_num: int) -> List[Dict]:
    """
    Extract symbol declarations from a single line of GAMS code.
    """
    symbols = []
    line_lower = line.lower().strip()
    
    # Skip comments
    if line_lower.startswith('*') or line_lower.startswith('//'):
        return symbols
    
    # Define patterns for each symbol type
    patterns = {
        'set': [r'\bsets?\s+', r'\bset\s+'],
        'scalar': [r'\bscalars?\s+', r'\bscalar\s+'],
        'parameter': [r'\bparameters?\s+', r'\bparameter\s+'],
        'variable': [r'\bvariables?\s+', r'\bvariable\s+'],
        'equation': [r'\bequations?\s+', r'\bequation\s+']
    }
    
    for symbol_type, type_patterns in patterns.items():
        for pattern in type_patterns:
            match = re.search(pattern + r'(.+)', line, re.IGNORECASE)
            if match:
                # Extract everything after the keyword
                symbols_text = match.group(1)
                
                # Parse symbols from this text
                parsed_symbols = _parse_symbol_declarations(symbols_text, symbol_type)
                
                for name, dim in parsed_symbols:
                    symbols.append({
                        'type': symbol_type,
                        'name': name,
                        'file': str(file_path),
                        'line': line_num,
                        'dim': dim
                    })
                
                # Only match first pattern found
                return symbols
    
    return symbols


def _parse_symbol_declarations(text: str, symbol_type: str) -> List[tuple]:
    """
    Parse symbol declarations from text after the keyword.
    Returns list of (name, dimension) tuples.
    """
    symbols = []
    
    # First split by newlines to handle multi-line declarations
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    for line in lines:
        # Skip empty lines and comments
        if not line or line.startswith('*') or line.startswith('//'):
            continue
            
        # Remove quoted strings and value assignments
        clean_line = re.sub(r"'[^']*'", '', line)
        clean_line = re.sub(r'"[^"]*"', '', clean_line)
        clean_line = re.sub(r'/[^/]*/', '', clean_line)
        clean_line = re.sub(r';.*$', '', clean_line)
        
        # Split by commas but respect parentheses
        parts = _split_respecting_parens(clean_line, ',')
        
        for part in parts:
            part = part.strip()
            if not part:
                continue
                
            # Extract name and dimensions
            if '(' in part:
                name = part.split('(')[0].strip()
                dims_part = part.split('(')[1].split(')')[0]
                # Count dimensions
                dim = len([d.strip() for d in dims_part.split(',') if d.strip()]) if dims_part.strip() else 0
            else:
                name = part.strip()
                dim = 0
            
            # Validate name
            if re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', name):
                symbols.append((name, dim))
    
    return symbols


def _split_respecting_parens(text: str, delimiter: str) -> List[str]:
    """Split text by delimiter but respect parentheses nesting."""
    parts = []
    current = ""
    paren_count = 0
    
    for char in text:
        if char == '(':
            paren_count += 1
        elif char == ')':
            paren_count -= 1
        elif char == delimiter and paren_count == 0:
            if current.strip():
                parts.append(current.strip())
            current = ""
            continue
        
        current += char
    
    if current.strip():
        parts.append(current.strip())
    
    return parts


def save_index(index: List[Dict], path: Union[str, Path]) -> Path:
    """
    Save symbol index as pretty JSON.
    
    Args:
        index: List of symbol dictionaries
        path: Output path for JSON file
        
    Returns:
        Path to saved file
    """
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=2, ensure_ascii=False)
    
    return output_path


def fallback_to_gdx(gdx_path: Union[str, Path]) -> List[Dict]:
    """
    Fallback to extract symbol information from GDX file.
    
    Args:
        gdx_path: Path to GDX file
        
    Returns:
        List of symbol dictionaries extracted from GDX
    """
    try:
        # Read symbols, marginals, and kinds from GDX
        symbol_data, marginals, kinds = read_gdx_transfer_full(str(gdx_path))
        
        symbols = []
        for name, df in symbol_data.items():
            # Determine symbol type from kinds mapping or infer from data
            symbol_type = kinds.get(name, 'parameter').lower()
            
            # Determine dimensionality from DataFrame structure
            # Value columns are typically named 'value', 'level', 'marginal', etc.
            value_cols = ['value', 'level', 'marginal', 'lower', 'upper', 'scale']
            key_cols = [col for col in df.columns if col not in value_cols and col != 'text']
            dim = len(key_cols)
            
            symbols.append({
                'type': symbol_type,
                'name': name,
                'file': str(gdx_path),
                'line': 0,  # No line number for GDX symbols
                'dim': dim
            })
        
        return symbols
        
    except Exception:
        # If GDX reading fails, return empty list
        return []


def create_symbol_index(model_dir: Union[str, Path], main_file: str = "main.gms", 
                       gdx_fallback: Optional[Union[str, Path]] = None) -> List[Dict]:
    """
    Create comprehensive symbol index for a GAMS model.
    
    Args:
        model_dir: Directory containing GAMS model
        main_file: Main GAMS file to start scanning from
        gdx_fallback: Optional GDX file to use as fallback source
        
    Returns:
        List of symbol dictionaries
    """
    model_path = Path(model_dir)
    main_path = model_path / main_file
    
    # Try to scan source files first
    if main_path.exists():
        symbols = scan_sources([main_path])
        if symbols:
            return symbols
    
    # Fallback to GDX if source scanning failed or found no symbols
    if gdx_fallback:
        gdx_path = Path(gdx_fallback)
        if not gdx_path.is_absolute():
            gdx_path = model_path / gdx_path
        return fallback_to_gdx(gdx_path)
    
    return []