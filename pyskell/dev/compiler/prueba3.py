import sys

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

def handle_for_loop(grouped_lines):
    expanded_lines = []
    
    for item in grouped_lines:
        if isinstance(item, tuple):
            command, block = item
            if command.startswith("for"):
                _, var_name, repeat_count = command.split()
                repeat_count = int(repeat_count)
                
                for _ in range(repeat_count):
                    expanded_lines.extend(block)
            else:
                # Handle other tuple cases (if any) here
                pass
        else:
            expanded_lines.append(item)
            
    return expanded_lines

def main():
    file = sys.argv[1]
    lines = read_file(file)
    
    grouped_lines = group_lines(lines)
    print('grouped_lines: ', grouped_lines)
    expanded_lines = handle_for_loop(grouped_lines)   
    print('expanded_lines: ', expanded_lines)
    
    
    print("\ncodigo")
    for i in expanded_lines:
        print(i)

if __name__ == "__main__":
    main()
