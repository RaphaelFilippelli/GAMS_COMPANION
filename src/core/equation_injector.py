from __future__ import annotations
from pathlib import Path
from typing import List, Dict

def inject_equation_includes(model_dir: Path, equations: List[Dict[str, str]], main_file: str) -> None:
    """
    Simple equation injection that adds equation names to the Equations section.
    """
    main_gms_path = model_dir / main_file
    if not main_gms_path.exists():
        raise FileNotFoundError(f"Main GAMS file not found: {main_gms_path}")
    
    if not equations:
        return
    
    # Extract equation names from include files
    equation_names = []
    for eq_spec in equations:
        if 'file' in eq_spec:
            include_file = eq_spec['file']
            include_path = model_dir / include_file
            
            if not include_path.exists():
                raise FileNotFoundError(f"Include file not found: {include_path}")
            
            # Read and parse equation names
            include_content = include_path.read_text(encoding='utf-8')
            for line in include_content.split('\n'):
                line = line.strip()
                if '..' in line and not line.startswith('*'):
                    eq_name = line.split('..')[0].strip()
                    if eq_name:
                        equation_names.append(eq_name)
                        print(f"Found equation: {eq_name}")
    
    if not equation_names:
        return
    
    print(f"Injecting equations: {equation_names}")
    
    # Read main file
    content = main_gms_path.read_text(encoding='utf-8')
    lines = content.split('\n')
    
    # Find the specific line with the semicolon that ends equation declarations
    # Look for: cap "capacity constraint";
    for i, line in enumerate(lines):
        if (';' in line and 
            '"' in line and 
            'constraint' in line.lower()):
            
            print(f"Found equations section end at line {i}: {line.strip()}")
            
            # Get indentation from this line
            indent = ''
            for char in line:
                if char in ' \t':
                    indent += char
                else:
                    break
            
            # Insert equation names before the semicolon line  
            for eq_name in reversed(equation_names):  # Reverse to maintain order
                new_line = f'{indent}{eq_name}'
                lines.insert(i, new_line)
                print(f"Inserted: '{new_line}'")
            
            print(f"Successfully added {len(equation_names)} equations")
            break
    
    # Write back
    new_content = '\n'.join(lines)
    main_gms_path.write_text(new_content, encoding='utf-8')

def inject_equation_includes_BACKUP(model_dir: Path, equations: List[Dict[str, str]], main_file: str) -> None:
    """
    Inject equation include statements into a GAMS model.
    
    This modifies the main GAMS file in-place to:
    1. Add equation names to the Equations declaration section
    2. Add $include statements before the first equation definition
    
    Args:
        model_dir: Path to the model directory (should be temp copy)
        equations: List of equation specifications from scenario
        main_file: Name of the main GAMS file
    """
    main_gms_path = model_dir / main_file
    if not main_gms_path.exists():
        raise FileNotFoundError(f"Main GAMS file not found: {main_gms_path}")
    
    if not equations:
        return  # Nothing to inject
    
    # Read the main file
    content = main_gms_path.read_text(encoding='utf-8')
    
    # Extract equation names from include files
    equation_names = []
    include_statements = []
    
    for eq_spec in equations:
        if 'file' in eq_spec:
            include_file = eq_spec['file']
            # Ensure the include file exists (relative to model dir)
            include_path = model_dir / include_file
            if not include_path.exists():
                raise FileNotFoundError(f"Include file not found: {include_path}")
            
            # Add include statement
            include_statements.append(f"$include {include_file}")
            
            # Read the include file to extract equation names
            include_content = include_path.read_text(encoding='utf-8')
            for line in include_content.split('\n'):
                line = line.strip()
                if '..' in line and not line.startswith('*'):
                    # Extract equation name (before '..')
                    eq_name = line.split('..')[0].strip()
                    if eq_name:
                        equation_names.append(eq_name)
                        print(f"Found equation: {eq_name}")
    
    print(f"Total equation names to inject: {equation_names}")
    
    if not equation_names and not include_statements:
        return
    
    lines = content.split('\n')
    new_lines = []
    equations_section_modified = False
    includes_injected = False
    
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip().lower()
        
        # Check if this line starts the Equations section
        if 'equations' == stripped or stripped.startswith('equations ') or 'equations' in stripped:
            # Add the Equations header
            new_lines.append(line)
            i += 1
            
            # Process all lines in the equations section until we hit semicolon
            while i < len(lines):
                next_line = lines[i]
                
                # If this line contains a semicolon, add our equations before it
                if ';' in next_line and not equations_section_modified:
                    # Add our equation names before the semicolon
                    if equation_names:
                        # Get indentation from existing equations
                        indent = '    '  # Default
                        # Look at previous equation declaration lines for indentation
                        for j in range(len(new_lines) - 1, -1, -1):
                            prev_line = new_lines[j]
                            prev_stripped = prev_line.strip()
                            if prev_stripped and '"' in prev_stripped and not prev_stripped.lower().startswith('equation'):
                                # This looks like an equation declaration, match its indentation
                                indent = ''
                                for char in prev_line:
                                    if char in ' \t':
                                        indent += char
                                    else:
                                        break
                                break
                        
                        # Add each equation name on its own line
                        for eq_name in equation_names:
                            new_lines.append(f"{indent}{eq_name}")
                    
                    equations_section_modified = True
                
                # Add the current line (including the semicolon line)
                new_lines.append(next_line)
                i += 1
                
                # If we just processed the semicolon line, we're done with equations section
                if ';' in next_line:
                    break
        
        # Check if this is the first equation definition (contains '..')
        elif '..' in stripped and not stripped.startswith('*') and include_statements and not includes_injected:
            # Inject include statements before first equation definition
            new_lines.append("")
            new_lines.append("* === Injected equation includes ===")
            new_lines.extend(include_statements)
            new_lines.append("* === End injected includes ===")
            new_lines.append("")
            new_lines.append(line)
            includes_injected = True
            i += 1
        
        # Skip any existing conditional includes for the same files
        elif stripped.startswith('$if exist') and include_statements:
            # Check if this is an include for one of our files
            skip_line = False
            for eq_spec in equations:
                if 'file' in eq_spec:
                    include_file = eq_spec['file']
                    if include_file in line:
                        skip_line = True
                        break
            
            if not skip_line:
                new_lines.append(line)
            i += 1
        else:
            # Regular line
            new_lines.append(line)
            i += 1
    
    # Write back the modified content
    new_content = '\n'.join(new_lines)
    main_gms_path.write_text(new_content, encoding='utf-8')

def _find_injection_point(content: str) -> int | None:
    """
    Find the best place to inject equation includes in GAMS code.
    
    Strategy:
    1. Look for the end of equation declarations section 
    2. Before the first equation definition (equation.. )
    3. If neither found, return None (will append to end)
    
    Args:
        content: The GAMS file content
        
    Returns:
        Character position to inject, or None if no good spot found
    """
    lines = content.split('\n')
    
    # Look for the end of Equations section
    equation_declarations_end = None
    equation_definition_start = None
    
    for i, line in enumerate(lines):
        stripped = line.strip().lower()
        
        # Skip comments and empty lines
        if not stripped or stripped.startswith('*'):
            continue
        
        # Look for equations declaration section
        if any(keyword in stripped for keyword in ['equation', 'equations']):
            # Find the end of this section (look for semicolon)
            for j in range(i + 1, len(lines)):
                next_line = lines[j].strip()
                if next_line and not next_line.startswith('*'):
                    if ';' in next_line:
                        equation_declarations_end = sum(len(lines[k]) + 1 for k in range(j + 1))
                        break
        
        # Look for first equation definition (contains '..' )
        if '..' in stripped and not stripped.startswith('*'):
            equation_definition_start = sum(len(lines[k]) + 1 for k in range(i))
            break
    
    # Return the best injection point
    if equation_declarations_end is not None:
        return equation_declarations_end
    elif equation_definition_start is not None:
        return equation_definition_start
    else:
        return None

def setup_patch_loading(model_dir: Path, patch_gdx_path: Path, main_file: str) -> None:
    """
    Modify the main GAMS file to load the patch.gdx at startup.
    
    This adds the necessary GAMS code to load patch.gdx before other declarations.
    
    Args:
        model_dir: Path to the model directory (should be temp copy)
        patch_gdx_path: Path to the patch.gdx file
        main_file: Name of the main GAMS file
    """
    main_gms_path = model_dir / main_file
    if not main_gms_path.exists():
        raise FileNotFoundError(f"Main GAMS file not found: {main_gms_path}")
    
    content = main_gms_path.read_text(encoding='utf-8')
    
    # Calculate relative path from model to patch
    try:
        rel_patch_path = Path(patch_gdx_path).relative_to(model_dir)
    except ValueError:
        # If not relative, use absolute path
        rel_patch_path = Path(patch_gdx_path)
    
    # Convert to forward slashes for GAMS
    patch_path_str = str(rel_patch_path).replace('\\', '/')
    
    # Create the patch loading code
    patch_code = f"""
* === Auto-generated patch loading ===
$if exist {patch_path_str} $gdxin {patch_path_str}
$if exist {patch_path_str} $load
$if exist {patch_path_str} $gdxin
* === End patch loading ===

"""
    
    # Add the patch loading code at the beginning, after any initial comments
    lines = content.split('\n')
    insert_pos = 0
    
    # Skip initial comment block
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped and not stripped.startswith('*') and not stripped.startswith('$'):
            insert_pos = i
            break
    
    # Insert the patch loading code
    lines.insert(insert_pos, patch_code)
    new_content = '\n'.join(lines)
    
    main_gms_path.write_text(new_content, encoding='utf-8')