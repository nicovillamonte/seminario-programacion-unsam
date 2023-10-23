import concurrent.futures
import shlex
import os
from colorama import Fore, Back, Style



# Función factorial (Number -> Number)
def factorial(n):
    n = int(n)
    return n * factorial(n-1) if n > 1 else 1

# Función doble (Number -> Number)
def doble(n):
    n = int(n)
    return n * 2

# Función suma (Number -> Number -> Number)
def suma(n):
    n = int(n)
    return lambda m: n + int(m)

# Función upperCase (String -> String)
def upperCase(s):
    s = str(s)
    return s.upper()

# Función length (String -> Number)
def length(s):
    s = str(s)
    return len(s)

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

special_commands = {
    '!c': clear_screen,
    'clear': clear_screen,
    '!h': show_help,
    'help': show_help,
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
    try:
        return function(*args)
    except ValueError:
        return "Error: uno o más argumentos no son números válidos."
    except Exception as e:
        return f"Error: {e}.\n Error Name: {type(e).__name__}"

def main():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        print("Pyskell v0.1.0. For help type '!h' or 'help'.")
        while True:
            comando = input("> ")
            special_func = special_commands.get(comando.lower().replace(' ', ''))
            if special_func:
                special_func()
                continue
            comando_split = shlex.split(comando)  # Utiliza shlex.split para dividir el comando
            if len(comando_split) >= 2:
                funcion_nombre = comando_split[0]
                argumentos = comando_split[1:]
                # Busca la función en el módulo actual por nombre
                funcion = globals().get(funcion_nombre)
                if funcion is not None and callable(funcion):
                    # Usa pyskellRunProccess para llamar a la función con el primer argumento
                    resultado = pyskellRunProccess(funcion, argumentos[0])
                    if callable(resultado):  # Si el resultado es una función, aplica los argumentos restantes
                        # Aplica los argumentos restantes uno por uno
                        resultado_final = pyskellRunProccess(apply_args, resultado, argumentos[1:])
                        print(resultado_final)
                    else:
                        print(resultado)  # Imprimir el resultado si no hay errores
                else:
                    print(f"Function '{funcion_nombre}' not recognized or callable.")
            else:
                print(f"Unrecognized command.")

if __name__ == "__main__":
    main()