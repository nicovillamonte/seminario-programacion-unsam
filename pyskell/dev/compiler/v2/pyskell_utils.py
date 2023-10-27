from pyskell_functions import pyskell_exported_functions
from pyskell_types import PyskellFunction
from colorama import Fore, Back, Style

def search_pyskell_function_by_name(name):
    funcion = None
    for f in pyskell_exported_functions:
        if f.name == name:
            funcion = f
            break
    return funcion

def is_valid_list_or_tuple(s):
    return (s.startswith('[') and s.endswith(']')) or (s.startswith('(') and s.endswith(')'))

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
        return f"Error: {e}."
        # print(f"\n Error Name: {type(e).__name__}")
        
def apply_args(func, args):
    result = func
    for arg in args:
        result = result(arg)
    return result

def print_c(text, color=Fore.RESET, bg_color=Back.RESET, _end="\n"):
    print(bg_color + color + text + Style.RESET_ALL, end=_end)
    

def safe_eval(s):
    try:
        return eval(s, {"__builtins__": None}, {})
    except Exception:
        return s