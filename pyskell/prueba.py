import concurrent.futures
import shlex
import os
from typing import Any
from colorama import Fore, Back, Style

class PyskellFunction:
    def __init__(self, name="_", func=lambda x: x, type=(None, None)):
        self.name = name
        self.func = func
        self.type = type
        self.command = ""

    def __call__(self, *args: Any) -> Any:
        return self.func(args[0]) if len(args) > 0 else self.func()
    
    def calleable(self):
        return callable(self.func)
    
    def set_command(self, command):
        self.command = command
    
    def destruct_type(self, _obj):
        self_type, inner_type = _obj.type
        
        if (type(_obj.type[0]) is type and type(_obj.type[1]) is PyskellFunction):
            return f"{self_type.__name__} -> {self.destruct_type(inner_type)}"
        else:
            return _obj.type[0].__name__ + " -> " + _obj.type[1].__name__
    
    def __str__(self):
        return f"{self.name if self.name != '_' else f'({self.command})'} :: {self.destruct_type(self)}"

    def __repr__(self):
        return f"<PyskellFunction: {self.name}>"

# Función factorial (Number -> Number)
def factorial_pyskell(n: int) -> int:
    n = int(n)
    return n * factorial_pyskell(n-1) if n > 1 else 1
factorial = PyskellFunction('factorial', factorial_pyskell, type=(int, int))

# Función doble (Number -> Number)
def doble_pyskell(n):
    n = float(n)
    return n * 2
doble = PyskellFunction('doble', doble_pyskell, type=(float, float))

# Función suma (Number -> Number -> Number)
def suma_pyskell(n: float) -> PyskellFunction:
    def inner_suma_pyskell (m: float) -> float:
        return float(n) + float(m)
    return PyskellFunction(func=inner_suma_pyskell, type=(float,float))
suma = PyskellFunction('suma', suma_pyskell, type=(float, PyskellFunction(type=(float,float))))

# Función upperCase (String -> String)
def upperCase_pyskell(s):
    s = str(s)
    return s.upper()
upperCase = PyskellFunction('upperCase', upperCase_pyskell, type=(str, str))

# Función lowerCase (String -> String)
def lowerCase_pyskell(s):
    s = str(s)
    return s.lower()
lowerCase = PyskellFunction('lowerCase', lowerCase_pyskell, type=(str, str))

# Función length (String -> Number)
def length_pyskell(s):
    s = str(s)
    return len(s)
length = PyskellFunction('length', length_pyskell, type=(str, int))

def sumOf_pyskell(arr):
    if len(arr) == 0:
        return 0
    else:
        return int(arr[0]) + sumOf_pyskell(arr[1:])
sumOf = PyskellFunction('sumOf', sumOf_pyskell, type=(list, int))

def isStrEq_pyskell(s):
    def inner_isStrEq_pyskell(x):
        return s == x
    return PyskellFunction(func=inner_isStrEq_pyskell, type=(str, bool))
isStrEq = PyskellFunction('isStrEq', isStrEq_pyskell, type=(str, PyskellFunction(type=(str, bool))))

def helloWorld_pyskell():
    return "Hello World!"
helloWorld = PyskellFunction('helloWorld', helloWorld_pyskell, type=(str))


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
    
    function = globals().get(function)
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

# ---------- Consola de Pyskell ----------


def apply_args(func, args):
    result = func
    for arg in args:
        result = result(arg)
    return result

def print_c(text, color=Fore.RESET, bg_color=Back.RESET, _end="\n"):
    print(bg_color + color + text + Style.RESET_ALL, end=_end)

# Funcion para limpiar el codigo y hacer todos los try catch de una.
def pyskellRunProccess(function, *args):
    # Get how many args the function needs
    num_args = function.func.__code__.co_argcount if isinstance(function, PyskellFunction) else function.__code__.co_argcount
    # Check if the function needs less args than the ones provided
    if len(args) < num_args:
        # If so, return a function that takes the remaining args
        return function
    try:
        # return function(*args)
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

import re

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
  
def main():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        print("Pyskell v0.1.0. For help type '!h' or 'help'.")
        while True:
            comando = input("> ")
            
              
            # comando_split = shlex.split(comando)  # Utiliza shlex.split para dividir el comando
            # comando_split = otro_split(comando)  # Utiliza shlex.split para dividir el comando
            
            # comando_split = custom_split(comando)
            comando_split = None
            try:
                comando_split = process_command(comando)
            except Exception as e:
                print(f"Error: {e}.")
                continue
            
            
            special_func = special_commands.get(comando_split[0].lower().replace(' ', ''))
            
            if special_func:
                # if not arguments then call special_func() else call special_func(arguments)
                special_func() if len(comando_split[1:]) == 0 else special_func(comando_split[1:])
                continue
            
            # Convertir argumentos que representan listas o tuplas a objetos de Python
            argumentos = [safe_eval(arg) if is_valid_list_or_tuple(arg) else arg for arg in comando_split[1:]]
            funcion_nombre = comando_split[0]
            # Busca la función en el módulo actual por nombre
            funcion = globals().get(funcion_nombre)
            
            if funcion is not None and funcion.calleable():
                funcion.set_command(comando)
                # Usa pyskellRunProccess para llamar a la función con el primer argumento
                resultado = None
                if len(argumentos) == 0:
                    resultado = pyskellRunProccess(funcion)
                else:
                    resultado = pyskellRunProccess(funcion, argumentos[0])
                
                if callable(resultado):  # Si el resultado es una función, aplica los argumentos restantes
                    resultado.set_command(comando)
                    # Aplica los argumentos restantes uno por uno
                    resultado_final = pyskellRunProccess(apply_args, resultado, argumentos[1:])
                    print(resultado_final)
                else:
                    print(resultado)  # Imprimir el resultado si no hay errores
            else:
                print(f"Function '{funcion_nombre}' not recognized or callable.")

if __name__ == "__main__":
    main()
