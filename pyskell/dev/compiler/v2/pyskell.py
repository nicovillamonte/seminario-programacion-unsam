import pyskell_builder as pbuilder
import sys
from pyskell_execute import run_pll
from pyskell_repl import run_repl

def main():
    if len(sys.argv) > 1:
        file = sys.argv[1]
        build_file = pbuilder.build(file=file, print_log=False)
        
        print("File builded:", build_file)
        
        print(f"Running {build_file}")
        run_pll(build_file)
    else:
        run_repl()

if __name__ == "__main__":
    main()