import sys
import re
from sympy import sympify

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


def main():
    file = sys.argv[1]
    lines = read_file(file)
    
    grouped_lines = group_lines(lines)
    print('grouped_lines: ', grouped_lines)
    expanded_lines = handle_for_loop_with_complex_evaluation(grouped_lines)
    print('expanded_lines: ', expanded_lines)
    
    print("\ncodigo")
    for i in expanded_lines:
        print(i)

if __name__ == "__main__":
    main()
