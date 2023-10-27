import os
from colorama import Fore, Style
from pyskell_utils import *
from pyskell_execute import pyskellRunProccess, apply_args, process_command

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')    

def show_help():
    commands = {
        '!c | clear': 'Clear the terminal screen.',
        '!h | help': 'Show help.',
        '!q | exit': 'Exit Pyskell.'
    }
    print("Available commands:")
    for cmd, desc in commands.items():
        print(f"\t{Fore.GREEN}{cmd}{Style.RESET_ALL}: {desc}")
        

def return_type_pyskell(function):
    # print("function[1:]", function[1:])
    function_name, arguments = function[0], function[1:]
    
    command_string = f"{function_name} {' '.join(arguments)}"
    
    comando_split = None
    try:
        comando_split = process_command(command_string)
    except Exception as e:
        print(f"Error: {e}.")
        return
    
    arguments = [safe_eval(arg) if is_valid_list_or_tuple(arg) else arg for arg in comando_split[1:]]
    function_name = comando_split[0]
    
    function = search_pyskell_function_by_name(function_name)
    
    if function is not None and function.calleable():
        function.set_command(command_string)
        # Usa pyskellRunProccess para llamar a la función con el primer argumento
        resultado = None
        if len(arguments) == 0:
            resultado = pyskellRunProccess(function)
        else:
            resultado = pyskellRunProccess(function, arguments[0])
        
        if callable(resultado):  # Si el resultado es una función, aplica los argumentos restantes
            resultado.set_command(command_string)
            # Aplica los argumentos restantes uno por uno
            resultado_final = pyskellRunProccess(apply_args, resultado, arguments[1:])
            print(resultado_final.__str__() if isinstance(resultado_final, PyskellFunction) else f"({command_string}) :: {type(resultado_final).__name__}" )
        else:
            print(f"({command_string}) ::", resultado.__str__() if isinstance(resultado, PyskellFunction) else type(resultado).__name__)
    else:
        print(f"Function '{function_name}' not recognized or callable.")
    

special_commands = {
    '!c': clear_screen,
    'clear': clear_screen,
    '!h': show_help,
    'help': show_help,
    'ftype': return_type_pyskell,
    '!q': lambda: [clear_screen(), exit()],
    'exit': lambda: [clear_screen(), exit()]
}