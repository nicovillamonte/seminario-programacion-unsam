import sys

import concurrent.futures
import shlex
import os
import re
from colorama import Fore, Back, Style
import time
# from threading import Thread
from multiprocessing import Process


from pyskell_types import PyskellFunction
from pyskell_functions import pyskell_exported_functions

# ---------- Comandos Especiales ----------
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
    function, arguments = function[0], function[1:]
    
    function = search_pyskell_function_by_name(function)
    command_string = f"{function.name} {' '.join(arguments)}"
    
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
        print(f"Function '{function}' not recognized or callable.")
    

special_commands = {
    '!c': clear_screen,
    'clear': clear_screen,
    '!h': show_help,
    'help': show_help,
    'ftype': return_type_pyskell,
    '!q': lambda: [clear_screen(), exit()],
    'exit': lambda: [clear_screen(), exit()]
}

#------------------------------------------------

def apply_args(func, args):
    result = func
    for arg in args:
        result = result(arg)
    return result

def print_c(text, color=Fore.RESET, bg_color=Back.RESET, _end="\n"):
    print(bg_color + color + text + Style.RESET_ALL, end=_end)

# Funcion para limpiar el codigo y hacer todos los try catch de una.
def pyskellRunProccess(function, *args):
    num_args = function.func.__code__.co_argcount if isinstance(function, PyskellFunction) else function.__code__.co_argcount
    
    if len(args) < num_args:
        return function
    try:
        return function(*args)
    except ValueError:
        return "Error: uno o más argumentos no son números válidos."
    except Exception as e:
        return f"Error: {e}.\n Error Name: {type(e).__name__}"

def is_valid_list_or_tuple(s):
    return (s.startswith('[') and s.endswith(']')) or (s.startswith('(') and s.endswith(')'))

def safe_eval(s):
    try:
        return eval(s, {"__builtins__": None}, {})
    except Exception:
        return s

def custom_split(s):
    if s is None:
          import warnings
          warnings.warn("Passing None for 's' to shlex.split() is deprecated.",
                        DeprecationWarning, stacklevel=2)
    args = []
    current_arg = ""
    bracket_count = 0
    for char in s:
        if char in "[(":
            bracket_count += 1
        elif char in "])":
            bracket_count -= 1
        if bracket_count > 0 or char not in " ,":
            current_arg += char
        elif current_arg:
            args.append(current_arg)
            current_arg = ""
    if current_arg:
        args.append(current_arg)  # añadir el último argumento si hay alguno
    return args

def process_command(command):
    # Patrón regex para identificar listas y tuplas en la cadena de comando
    pattern = re.compile(r'(\[.*?\]|\(.*?\))')
    # Buscar todas las listas y tuplas en la cadena de comando
    lists_and_tuples = pattern.findall(command)
    # Reemplazar las listas y tuplas encontradas en la cadena de comando con placeholders
    for i, lt in enumerate(lists_and_tuples):
        command = command.replace(lt, f'__PLACEHOLDER{i}__')
    # Dividir la cadena de comando en argumentos
    args = shlex.split(command)
    # Reemplazar los placeholders en los argumentos con las listas y tuplas originales
    for i, lt in enumerate(lists_and_tuples):
        placeholder = f'__PLACEHOLDER{i}__'
        args = [arg.replace(placeholder, lt) for arg in args]
    return args

def search_pyskell_function_by_name(name):
    funcion = None
    for f in pyskell_exported_functions:
        if f.name == name:
            funcion = f
            break
    return funcion

def run_command(comando):
    comando_split = None
    try:
        comando_split = process_command(comando)
    except Exception as e:
        print(f"Error: {e}.")
        return "continue"
    
    special_func = special_commands.get(comando_split[0].lower().replace(' ', ''))
    
    if special_func:
        special_func() if len(comando_split[1:]) == 0 else special_func(comando_split[1:])
        return "continue"
    
    # Convertir argumentos que representan listas o tuplas a objetos de Python
    argumentos = [safe_eval(arg) if is_valid_list_or_tuple(arg) else arg for arg in comando_split[1:]]
    
    funcion_nombre = comando_split[0]
    
    funcion = search_pyskell_function_by_name(funcion_nombre)
    
    if funcion is not None and funcion.calleable():
        funcion.set_command(comando)
        
        resultado = None
        if len(argumentos) == 0:
            resultado = pyskellRunProccess(funcion)
        else:
            resultado = pyskellRunProccess(funcion, argumentos[0])
        
        if callable(resultado):
            resultado.set_command(comando)
            resultado_final = pyskellRunProccess(apply_args, resultado, argumentos[1:])
            print(resultado_final)
        else:
            print(resultado)
    else:
        print(f"Function '{funcion_nombre}' not recognized or callable.")


def main():
    file = sys.argv[1]
    
    lines = []
    with open(file, 'r') as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            lines[i] = line.replace('\n', '')

    results = []
    for activated_hilo in [False, True]:
        
        print(f"Hilos {'activados' if activated_hilo else 'desactivados'}...")
    
        start = time.time()
        
        
        if(not activated_hilo):
            for comando in lines:
                run_command(comando)
        else:
            hilos = [Process(target=run_command, args=(comando,)) for comando in lines]
            
            for hilo in hilos:
                hilo.start()
            
            for hilo in hilos:
                hilo.join()
        
        end = time.time()
        results.append(end - start)
        print(round(end - start,6), "seconds")
        print("End succesfully.")
        time.sleep(5)
        
    print("Resultados: ")
    print("Con hilos: ", results[0])
    print("Sin hilos: ", results[1])

if __name__ == "__main__":
  
  main()