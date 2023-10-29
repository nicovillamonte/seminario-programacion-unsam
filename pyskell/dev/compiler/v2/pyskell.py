import pyskell_builder as pbuilder
import sys
import time
from pyskell_execute import run_pll
from pyskell_repl import run_repl
from pyskell_special_commands import clear_screen

DEV_MODE = True

def main():
    if len(sys.argv) > 1:
        file = sys.argv[1]
        
        # If file extension is .pll, build it, else run it
        if file.split('.')[-1] == 'pll':
            print("Building file:", file)
            build_file = pbuilder.build(file=file, print_log=DEV_MODE)
            print("File builded:", build_file)
        else:
            build_file = file
        
        # time.sleep(1)
        # pause
        if DEV_MODE:
            input("Press Enter to continue...")
        
        print(f"\nRunning {build_file}")
        # time.sleep(1)
        clear_screen()
        run_pll(build_file)
    else:
        run_repl()

if __name__ == "__main__":
    main()