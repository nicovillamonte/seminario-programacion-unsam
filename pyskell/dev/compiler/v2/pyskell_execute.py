from pyskell_types import PyskellFunction
from pyskell_utils import *
# from pyskell_special_commands import special_commands
import re
import shlex
from pyskell_shared_global import variables
# from pyskell_builder import handle_line_evaluation

# variables = []

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

def is_pll_function(command):
    from pyskell_special_commands import special_commands
    comando_split = None
    try:
        comando_split = process_command(command)
    except Exception as e:
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

def get_variable(hash):
    # global variables
    
    return variables[[variable["hash"] for variable in variables].index(hash)] if hash in [variable["hash"] for variable in variables] else None

def handle_assignation(command):
    command_split = command.split('=')
    variable_hash = command_split[0].strip()
    variable_to_assign = get_variable(variable_hash)
    command = command_split[1].strip()
    variable_value = run_command(command, True) if is_pll_function(command_split[1].strip()) else safe_eval(command_split[1].strip())

    variable_to_assign["value"] = variable_value
    name = variable_to_assign["name"]
    
    print(f"{name} :: {type(variable_value).__name__} = {variable_value}")

# def replace_variables_in_command(command):
#     if not len(variables) > 0:
#         return command
    
#     comando = command
    
#     for variable in variables:
#         comando = comando.replace(variable["hash"], str(variable["value"])) if variable["hash"] in comando else comando

#     return comando

def replace_variables_in_command(command):
    if not len(variables) > 0:
        return command, False
    
    comando = command
    replaced = False
    
    for variable in variables:
        if variable["hash"] in comando:
            comando = comando.replace(variable["hash"], str(variable["value"]))
            replaced = True

    return comando, replaced

def evaluate_arithmetic_expressions(command):
    command, _ = command
    command_split = command.split(' ')
    try:
        return f"{command_split[0]} {str(eval(command_split[1]))}"
    except:
        return command

def run_command(comando, with_return=False):
    from pyskell_special_commands import special_commands
    
    if '=' in comando:
        return handle_assignation(comando)
    
    comando = replace_variables_in_command(comando)
    
    comando, _ = replace_variables_in_command(comando)
    
    comando = evaluate_arithmetic_expressions(comando)
    
    comando_split = None
    try:
        comando_split = process_command(comando)
    except Exception as e:
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
        # print("Running:", comando)
        run_command(comando)