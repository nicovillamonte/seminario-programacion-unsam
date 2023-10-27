import sys
import re
from sympy import sympify
import os
from hashlib import blake2b

def read_file(file):
    lines = []
    with open(file, 'r') as f:
        for line in f:
            lines.append(line.rstrip())
    return lines

def group_lines(lines):
    grouped_lines = []
    parent_line = None
    
    for line in lines:
        stripped_line = line.strip()
        
        is_indented = line.startswith('\t') or line.startswith('    ')
        
        if not is_indented:
            if parent_line:
                grouped_lines.append(parent_line)
            
            parent_line = (stripped_line, [])
        else:
            if parent_line:
                parent_line[1].append(stripped_line)
    
    if parent_line:
        grouped_lines.append(parent_line)
    
    flattened_grouped_lines = []
    for item in grouped_lines:
        if isinstance(item, tuple):
            if item[1]:
                flattened_grouped_lines.append(item)
            else:
                flattened_grouped_lines.append(item[0])
        else:
            flattened_grouped_lines.append(item)
            
    return flattened_grouped_lines

def handle_for_loop_with_complex_evaluation(grouped_lines):
    expanded_lines = []
    
    for item in grouped_lines:
        if isinstance(item, tuple):
            command, block = item
            if command.startswith("for"):
                _, var_name, repeat_count = command.split()
                repeat_count = int(repeat_count)
                
                regex = re.compile(r'\b' + re.escape(var_name) + r'\b')
                
                for i in range(repeat_count):
                    expanded_block = []
                    for line in block:
                        # Replace the variable name in each line with its value
                        replaced_line = regex.sub(str(i), line)
                        
                        # Identify and evaluate expressions
                        try:
                            evaluated_line = ' '.join([str(eval(comp)) if any(op in comp for op in ['+', '-', '*', '/', '%', '(', ')']) else comp for comp in replaced_line.split()])
                        except:
                            evaluated_line = replaced_line  # If evaluation fails, keep the original line
                        
                        # Remove trailing ".0" if any
                        cleaned_line = evaluated_line.replace(".0 ", " ").replace(".0", "")
                        
                        expanded_block.append(cleaned_line)
                    
                    expanded_lines.extend(expanded_block)
            else:
                pass
        else:
            expanded_lines.append(item)
            
    return expanded_lines

def handle_for_loop_with_cleaning(grouped_lines):
    expanded_lines = handle_for_loop_with_complex_evaluation(grouped_lines)
    
    # Remove empty lines and lines starting with "--"
    cleaned_lines = [line for line in expanded_lines if line.strip() and not line.startswith("--")]
    
    return cleaned_lines

def generate_rpll(file, expanded_lines):
    file_name = file.replace('.pll','.rpll').replace('.\\','')
    # si la carpeta dist no existe, crearla
    try:
        os.stat('dist')
    except:
        os.mkdir('dist')
    
    with open(f"dist/{file_name}", 'w+') as f:
        for i, line in enumerate(expanded_lines):
            f.write(line + '\n') if i + 1 != len(expanded_lines) else f.write(line)

def separe_rpll_and_calculable_lines(expanded_lines):
    rpll_lines = []
    calculable_lines = []
    for line in expanded_lines:
        if not '=' in line:
            rpll_lines.append(line)
        else:
            calculable_lines.append(line)
    return rpll_lines, calculable_lines

def throw_duplicates(elements):
    new_elements = []
    seen = set()  # Para llevar un registro de los nombres que ya hemos visto

    for element in elements:
        name = element["name"]
        if name not in seen:
            seen.add(name)
            new_elements.append(element)

    return new_elements

def get_variable(hash):
    global variables
    
    return variables[[variable["hash"] for variable in variables].index(hash)]
    

def main():
    global variables
    
    file = sys.argv[1]
    lines = read_file(file)
    
    grouped_lines = group_lines(lines)
    print('grouped_lines: ', grouped_lines)
    expanded_lines = handle_for_loop_with_complex_evaluation(grouped_lines)
    expanded_lines = handle_for_loop_with_cleaning(expanded_lines)
    # Remove empty lines
    print('expanded_lines: ', expanded_lines)
    
    # print("\ncodigo")
    # for i in expanded_lines:
    #     print(i)
    
    rpll_lines, calculable_lines = separe_rpll_and_calculable_lines(expanded_lines)
    
    print('rpll_lines: ', rpll_lines)
    print('calculable_lines: ', calculable_lines)
    
    variables = []  # Usamos una lista en lugar de un conjunto
    for i in calculable_lines:
        [left_side, _] = i.split('=')
        variables.append({
            "name": left_side.strip(),
            "value": None,
            "hash": f"%{str(abs(hash(f'{left_side.strip()}')))}%"
        })

    print('variables: ', throw_duplicates(variables))
    
    # replace all variables in expanded_lines with their hashes
    for i, line in enumerate(expanded_lines):
        for variable in variables:
            if variable["name"] in line:
                expanded_lines[i] = line.replace(variable["name"], variable["hash"])
    
        
    generate_rpll(file, expanded_lines)

if __name__ == "__main__":
    main()
