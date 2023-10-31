import pyskell_builder as pbuilder
import pyskell_execute as pexecuter
import sys
import time
from pyskell_repl import run_repl
from pyskell_special_commands import clear_screen
from pyskell_shared_global import DEV_MODE
from pyskell_utils import print_if_debug

def main():
    if len(sys.argv) > 1:
        file = sys.argv[1]
        
        # If file extension is .pll, build it, else run it
        if file.split('.')[-1] == 'pll':
            print_if_debug("Building file:", file)
            build_file = pbuilder.build(file=file, print_log=DEV_MODE)
            print_if_debug("File builded:", build_file)
        else:
            build_file = file
        
        input("Press Enter to continue...") if DEV_MODE else None
        
        print_if_debug(f"\nRunning {build_file}")
        clear_screen()
        pexecuter.run_pll(build_file)
    else:
        run_repl()

if __name__ == "__main__":
    main()