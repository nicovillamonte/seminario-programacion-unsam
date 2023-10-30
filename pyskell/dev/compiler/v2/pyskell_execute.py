from pyskell_types import PyskellFunction
from pyskell_utils import *
from multiprocessing import Process
# from pyskell_special_commands import special_commands
import re
import shlex
from pyskell_shared_global import variables, variables_inputs
# from pyskell_builder import handle_line_evaluation

# variables = []
loaded_program = []

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
    command_split[0], command_split[1] = command_split[0], ' '.join(command_split[1:])
    try:
        if any(op in command_split[1] for op in ['+', '-', '*', '/', '%', '(', ')']):
            return f"{command_split[0]} {str(eval(command_split[1]))}"
        else: return command
    except:
        return command

def tokenize_command_with_incognit(command):
    tokens = []
    in_quotes = False
    current_token = []
    for char in command:
        if char == '"':
            in_quotes = not in_quotes
            current_token.append(char)
        elif char == ' ':
            if in_quotes:
                current_token.append(char)
            else:
                tokens.append(''.join(current_token))
                current_token = []
        else:
            current_token.append(char)
    if current_token:
        tokens.append(''.join(current_token))
    return tokens

def obtain_id_from_prebuild_command(command):
    regex = re.compile(r"[_$][a-zA-Z0-9]+[$][:;]")
    match = regex.search(command)
    if match:
        id = match.group(0)
        id = id[1:][:-2]
        return id
    return False

def get_block_from_prebuild_command(id):
    global loaded_program
    command_block = []
    block_started = False
    
    for line in loaded_program:
        start_match = re.match(rf'_\${id}\$:.*', line)
        
        end_match = re.match(rf'_\${id}\$;.*', line)
        if start_match:
            block_started = True
            continue
        
        if end_match:
            break
        
        if block_started:
            command_block.append(line)
            
    return command_block if block_started and end_match else None
    

def run_parallel_block(block):
    # Create a new thread (Proccess) for each command 
    
    # Detectar si se abre un bloque
    # Si es asi obtener el bloque entero y mandarlo a run_parallel_block recursivamente
    # Sino crear un Thread para cada comando
    code = []
    for command in block:
        if command.startswith('_$'):
            id = obtain_id_from_prebuild_command(command)
            block = get_block_from_prebuild_command(id)
            run_parallel_block(block)
            # TODO: Falta que se saltee todo el bloque al seguir con el for.
        else:
            code.append(command)
    
    command_proccesses = [
        Process(target=run_command, args=(command,)) for command in block if not command.startswith('--')
    ]
    
    # TODO: Hacer los procesos de los bloques que tienen como target en vez de run_command a run_pll con el nuevo programa (bloque)
    # command_proccesses.extend([ Process()])
    
    # Start all the threads (Proccesses)
    for proccess in command_proccesses:
        proccess.start()
    
    # Wait for all the threads (Proccesses) to finish
    for proccess in command_proccesses:
        proccess.join()

def handle_parallel_block(command):
    global loaded_program
    
    prebuild_command_id = obtain_id_from_prebuild_command(command)
    
    line_index = loaded_program.index(command)
    
    parallel_block = []
    
    new_loaded_program = loaded_program
    new_loaded_program[line_index] = "-- " + new_loaded_program[line_index]
    for i, line in enumerate(loaded_program[line_index+1:]):
        new_loaded_program[line_index+i+1] = "-- " + new_loaded_program[line_index+i+1]
        if obtain_id_from_prebuild_command(line) == prebuild_command_id:
            break
        else:
            parallel_block.append(line)
    
    loaded_program = new_loaded_program
    
    run_parallel_block(parallel_block)

def handle_prebuild_command(command):
    regex = re.compile(r"[:;][a-zA-Z]+$")
    match = regex.search(command)
    if match:
        if match.group(0).startswith(';'):
            return None
        
        prebuild_commands = {
            ':pl': handle_parallel_block
        }
        prebuild_commands.get(match.group(0), lambda: None)(command)
    else:
        return None
    
    

def run_command(comando, with_return=False):
    from pyskell_special_commands import special_commands
    
    if comando.startswith('_$'): # if starts with _$ it is a prebuild command like PARALLEL, CONCURRENT, etc.
        return handle_prebuild_command(comando)
    
    # Separar el comando en tokens, teniendo en cuenta las comillas
    incogint_tokenated = tokenize_command_with_incognit(comando)
    
    for incognit in incogint_tokenated:
        if incognit.startswith('?'):
            prompt = incognit[1:][1:-1] if incognit[1:].startswith('"') else incognit[1:]
            prompt = (prompt if len(prompt.strip()) > 0 else "?") + (":" if not incognit[1:].startswith('"') else "")
            
            # if exists prompt in variables_inputs then use it, else ask for input
            user_input = None
            for variable_input in variables_inputs:
                if variable_input["prompt"] == prompt:
                    user_input = variable_input["value"]
                    break
            if user_input is None:
                user_input = input(prompt + ' ')
            
            comando = comando.replace(incognit, user_input)
    
            # Save variable for later replacement
            variables_inputs.append({"prompt": prompt, "value": user_input})
    
    if '=' in comando:
        return handle_assignation(comando)
    
    # Si tiene variables, de formato %...% las reemplaza por su valor
    are_variables = re.compile(r'%.*?%')
    if are_variables.search(comando):
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

def run_pll(file, program=[]):
    global loaded_program
    
    if len(program) > 0:
        with open(file, 'r') as f:
            loaded_program = f.readlines()
            for i, line in enumerate(loaded_program):
                loaded_program[i] = line.replace('\n', '')
    else:
        loaded_program = program
    
    for index_command in range(len(loaded_program)):
        try:
            comando = loaded_program[index_command]
            if not comando.startswith('--'):
                run_command(comando)
        except:
            return "Error."