import sys

def read_file(file):
    lines = []
    with open(file, 'r') as f:
        for line in f:
            lines.append(line.rstrip())
    return lines

def group_lines(lines):
    grouped_lines = []
    parent_line = None  # To hold the current parent line (e.g., "for i 3")
    
    for line in lines:
        stripped_line = line.strip()
        
        # Check for indentation (using '\t' for detecting indented lines)
        is_indented = line.startswith('\t') or line.startswith('    ')  # considering both tab and four spaces as indentation
        
        if not is_indented:
            # If there is a previous parent line, append it to the grouped_lines
            if parent_line:
                grouped_lines.append(parent_line)
            
            # Check if the next line(s) are indented to decide whether this line should be a parent line
            parent_line = (stripped_line, [])
        else:
            # Append the indented line to the current parent line's block
            if parent_line:
                parent_line[1].append(stripped_line)
    
    # Append the last parent line if it's not empty
    if parent_line:
        grouped_lines.append(parent_line)
    
    # Flatten the grouped_lines to remove empty blocks
    flattened_grouped_lines = []
    for item in grouped_lines:
        if isinstance(item, tuple):
            if item[1]:  # only append parent lines that have a block
                flattened_grouped_lines.append(item)
            else:
                flattened_grouped_lines.append(item[0])
        else:
            flattened_grouped_lines.append(item)
            
    return flattened_grouped_lines

def main():
    file = sys.argv[1]
    lines = read_file(file)
    
    grouped_lines = group_lines(lines)
    
    print(grouped_lines)

if __name__ == "__main__":
    main()