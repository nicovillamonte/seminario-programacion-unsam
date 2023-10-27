# Vamos a hacer un convertidor de archivo.pll -> archivo.rpll
# pll -> PyskeLL
# rpll -> Runable PyskeLL

import sys

def read_file(file):
    lines = []
    with open(file, 'r') as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            lines[i] = line.replace('\n', '').replace('    ','\t')
    return lines

def main():
    file = sys.argv[1]
    lines = read_file(file)
    
    print(lines)
    for i in lines:
        print(i)

if __name__ == "__main__":
    main()