import sys
import re
from sympy import sympify
import os
import time
from multiprocessing import Process
import shlex
from colorama import Fore, Back, Style
from pyskell_types import PyskellFunction
from pyskell_functions import pyskell_exported_functions

def read_file(file):
    lines = []
    with open(file, 'r') as f:
        for line in f:
            lines.append(line.rstrip())
    return lines

def group_lines(lines):
    grouped_lines = []
    parent_line = None
    
    for line in lines:
        stripped_line = line.strip()
        
        is_indented = line.startswith('\t') or line.startswith('    ')
        
        if not is_indented:
            if parent_line:
                grouped_lines.append(parent_line)
            
            parent_line = (stripped_line, [])
        else:
            if parent_line:
                parent_line[1].append(stripped_line)
    
    if parent_line:
        grouped_lines.append(parent_line)
    
    flattened_grouped_lines = []
    for item in grouped_lines:
        if isinstance(item, tuple):
            if item[1]:
                flattened_grouped_lines.append(item)
            else:
                flattened_grouped_lines.append(item[0])
        else:
            flattened_grouped_lines.append(item)
            
    return flattened_grouped_lines

def handle_for_loop_with_complex_evaluation(grouped_lines):
    expanded_lines = []
    
    for item in grouped_lines:
        if isinstance(item, tuple):
            command, block = item
            if command.startswith("for"):
                _, var_name, repeat_count = command.split()
                repeat_count = int(repeat_count)
                
                regex = re.compile(r'\b' + re.escape(var_name) + r'\b')
                
                for i in range(repeat_count):
                    expanded_block = []
                    for line in block:
                        # Replace the variable name in each line with its value
                        replaced_line = regex.sub(str(i), line)
                        
                        # Identify and evaluate expressions
                        try:
                            evaluated_line = ' '.join([str(eval(comp)) if any(op in comp for op in ['+', '-', '*', '/', '%', '(', ')']) else comp for comp in replaced_line.split()])
                        except:
                            evaluated_line = replaced_line  # If evaluation fails, keep the original line
                        
                        # Remove trailing ".0" if any
                        cleaned_line = evaluated_line.replace(".0 ", " ").replace(".0", "")
                        
                        expanded_block.append(cleaned_line)
                    
                    expanded_lines.extend(expanded_block)
            else:
                pass
        else:
            expanded_lines.append(item)
            
    return expanded_lines

def handle_for_loop_with_cleaning(grouped_lines):
    expanded_lines = handle_for_loop_with_complex_evaluation(grouped_lines)
    
    # Remove empty lines and lines starting with "--"
    cleaned_lines = [line for line in expanded_lines if line.strip() and not line.startswith("--")]
    
    return cleaned_lines

def generate_rpll(file, expanded_lines):
    file_name = file.replace('.pll','.rpll').replace('.\\','')
    # si la carpeta dist no existe, crearla
    try:
        os.stat('dist')
    except:
        os.mkdir('dist')
    
    with open(f"dist/{file_name}", 'w+') as f:
        for i, line in enumerate(expanded_lines):
            f.write(line + '\n') if i + 1 != len(expanded_lines) else f.write(line)
    
    return f"./dist/{file_name}"

def separe_rpll_and_calculable_lines(expanded_lines):
    rpll_lines = []
    calculable_lines = []
    for line in expanded_lines:
        if not '=' in line:
            rpll_lines.append(line)
        else:
            calculable_lines.append(line)
    return rpll_lines, calculable_lines

def throw_duplicates(elements):
    new_elements = []
    seen = set()  # Para llevar un registro de los nombres que ya hemos visto

    for element in elements:
        name = element["name"]
        if name not in seen:
            seen.add(name)
            new_elements.append(element)

    return new_elements

def get_variable(hash):
    global variables
    
    return variables[[variable["hash"] for variable in variables].index(hash)]

def print_if(condition, message, *args):
    if condition:
        print(message, *args)

def build(file, print_log=False):
    global variables
    
    lines = read_file(file)
    
    grouped_lines = group_lines(lines)
    print_if(print_log, 'grouped_lines: ', grouped_lines)
    expanded_lines = handle_for_loop_with_complex_evaluation(grouped_lines)
    expanded_lines = handle_for_loop_with_cleaning(expanded_lines)
    # Remove empty lines
    print_if(print_log, 'expanded_lines: ', expanded_lines)
    
    # print_if(print_log, "\ncodigo")
    # for i in expanded_lines:
    #     print_if(print_log, i)
    
    rpll_lines, calculable_lines = separe_rpll_and_calculable_lines(expanded_lines)
    
    print_if(print_log, 'rpll_lines: ', rpll_lines)
    print_if(print_log, 'calculable_lines: ', calculable_lines)
    
    variables = []  # Usamos una lista en lugar de un conjunto
    for i in calculable_lines:
        [left_side, _] = i.split('=')
        variables.append({
            "name": left_side.strip(),
            "value": None,
            "hash": f"%{str(abs(hash(f'{left_side.strip()}')))}%"
        })

    print_if(print_log, 'variables: ', throw_duplicates(variables))
    
    # replace all variables in expanded_lines with their hashes
    for i, line in enumerate(expanded_lines):
        for variable in variables:
            if variable["name"] in line:
                expanded_lines[i] = line.replace(variable["name"], variable["hash"])
    
        
    return generate_rpll(file, expanded_lines)

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
        return f"Error: {e}."
        # print(f"\n Error Name: {type(e).__name__}")

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

def is_pll_function(command):
    comando_split = None
    try:
        comando_split = process_command(command)
        print("SPLIT", comando_split)
    except Exception as e:
        print("LA CONCHA DE TU MADRE")
        print(f"Error SPLITEANDO: {e}.")
        return "continue"
    
    special_func = special_commands.get(comando_split[0].lower().replace(' ', ''))
    
    if special_func:
        return False
    
    funcion_nombre = comando_split[0]
    
    funcion = search_pyskell_function_by_name(funcion_nombre)
    
    if funcion:
        return True
    return False

def handle_assignation(command):
    global variables
    
    command_split = command.split('=')
    variable_hash = command_split[0].strip()
    variable_to_assign = get_variable(variable_hash)
    command = command_split[1].strip()
    variable_value = run_command(command, True) if is_pll_function(command_split[1].strip()) else safe_eval(command_split[1].strip())

    variable_to_assign["value"] = variable_value
    name = variable_to_assign["name"]
    
    print(f"{name} :: {type(variable_value).__name__} = {variable_value}")

def replace_variables_in_command(command):
    global variables
    if not len(variables) > 0:
        return command
    
    comando = ""
    for variable in variables:
        comando = command.replace(variable["hash"], str(variable["value"]))
        print("comando reemplazado", comando)

    return comando

def run_command(comando, with_return=False):
    if '=' in comando:
        return handle_assignation(comando)
    
    comando = replace_variables_in_command(comando)
    
    comando_split = None
    try:
        comando_split = process_command(comando)
    except Exception as e:
        print("LA CONCHA DE TU MADRE")
        print(f"Error SPLITEANDO: {e}.")
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
            if with_return:
                return resultado_final
            else:
                print(resultado_final)
        else:
            if with_return:
                return resultado
            else:
                print(resultado)
    else:
        if with_return:
            return None
        else:
            print(f"Function '{funcion_nombre}' not recognized or callable.")
    

def run_pll(file):
    lines = []
    with open(file, 'r') as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            lines[i] = line.replace('\n', '')
    
    for comando in lines:
        run_command(comando)
    
def remove_dist(file):
    # Remove build_file
    os.remove(file)
    # Remove dist folder if empty
    try:
        os.rmdir('dist')
    except OSError:
        pass

def main():
    global variables
    
    file = sys.argv[1]
    build_file = build(file=file, print_log=False)
    
    run_pll(build_file)
    # remove_dist(build_file)
    
    

if __name__ == "__main__":
    main()
