from pyskell_types import PyskellFunction
from pyskell_utils import *
from multiprocessing import Process
# from pyskell_special_commands import special_commands
import re
import shlex
from pyskell_shared_global import variables, variables_inputs
# from pyskell_builder import handle_line_evaluation
# from pyskell_shared_global import DEV_MODE
from pyskell_utils import print_if_debug

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
    block_size = 0
    
    print_if_debug("searching for id:", id, "in:", loaded_program)
    
    start_line, end_line = None, None
    
    for line in loaded_program:
        start_match = re.match(rf'_\${id}\$:.*', line)
        end_match = re.match(rf'_\${id}\$;.*', line)
        
        # print_if_debug("Match start:", start_match, "Match end:", end_match)
        if start_match:
            start_line = line
            block_started = True
            continue
        
        if end_match:
            end_line = line
            break
        
        if block_started:
            command_block.append(line)
            block_size += 1
            
    # return [command_block if block_started and end_match else None, block_size]
    
    full_block = [start_line] + command_block + [end_line]

    return {
        "inner": (command_block, block_size),
        "full": (full_block, len(full_block)),
    } if block_started and end_match else None
    

def run_parallel_block(block):
    # print_if_debug("Vengo a correr un bloque paralelo con el bloque", block)
    # Create a new thread (Proccess) for each command 
    
    # Detectar si se abre un bloque
    # Si es asi obtener el bloque entero y mandarlo a run_parallel_block recursivamente
    # Sino crear un Thread para cada comando
    code = []
    proccesses_to_wait = []
    i = 0
    
    while i < len(block):
        print_if_debug(f"Estoy en el index {i} con el comando {block[i]}")
        command = block[i]
        if command.startswith('_$'):
            id = obtain_id_from_prebuild_command(command)
            # print_if_debug("Id obtenido:", id)
            block_prebuild = get_block_from_prebuild_command(id)
            print_if_debug("Bloque obtenido:", block)
            # _, size = block_prebuild.get("inner")
            full_block, size = block_prebuild.get("full")
            
            # print("----------FULL BLOCK", full_block)
            # get_inner_block_from_prebuild_command
            # get_block_from_prebuild_command(id).get("inner")
            
            # Hacer el tema de los procesos aca.
            print_if_debug("Mandando a ejecutar bloque:", full_block, size)
            file_name = f"./dist/temp-{id}.rpll"
            with open(file_name, 'w+') as f:
                f.writelines([line + '\n' for line in full_block])
            block_proccess = Process(target=run_pll,args=(file_name,None,))
            # print("EMPEZANDO EJECUCION DEL PROCESO DLE BLOQUE")
            proccesses_to_wait.append(block_proccess)
            block_proccess.start()
            # run_parallel_block(block)
            i += size
        else:
            code.append(command)
            i += 1
    # for command in block:
    #     if command.startswith('_$'):
    #         id = obtain_id_from_prebuild_command(command)
    #         block, size = get_block_from_prebuild_command(id)
    #         run_parallel_block(block)
            
    #         # TODO: Falta que se saltee todo el bloque al seguir con el for.
    #     else:
    #         code.append(command)
    
    command_proccesses = [
        Process(target=run_command, args=(command,)) for command in code if not command.startswith('--')
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
    # print("Se que es un BLOQUE PARALELO")
    global loaded_program
    global pyskell_pc
    
    prebuild_command_id = obtain_id_from_prebuild_command(command)
    
    # print("Tengo el ID:", prebuild_command_id)
    
    line_index = loaded_program.index(command)
    
    # print("Estoy en la linea:", line_index+1)
    
    parallel_block = []
    
    new_loaded_program = loaded_program
    # new_loaded_program[line_index] = "-- " + new_loaded_program[line_index]
    for i, line in enumerate(loaded_program[line_index+1:]):
        # new_loaded_program[line_index+i+1] = "-- " + new_loaded_program[line_index+i+1]
        if obtain_id_from_prebuild_command(line) == prebuild_command_id:
            break
        else:
            parallel_block.append(line)
    # print("New loaded program: ", new_loaded_program)
    # print("Parallel block: ", parallel_block)
    
    loaded_program = new_loaded_program
    
    run_parallel_block(parallel_block)
    pyskell_pc += len(parallel_block)

def handle_prebuild_command(command):
    regex = re.compile(r"[:;][a-zA-Z]+$")
    match = regex.search(command)
    
    # print("MATCHEO O NO MATCHEO:", match)
    
    if match:
        if match.group(0).startswith(';'):
            # print("Empieza con ;")
            return "continue"
        # print("No empieza con ;")
        
        prebuild_commands = {
            ':pl': handle_parallel_block
        }
        prebuild_commands.get(match.group(0), lambda: None)(command)
    else:
        return "continue"

def run_command(comando, with_return=False):
    from pyskell_special_commands import special_commands
    
    if comando.startswith('_$'): # if starts with _$ it is a prebuild command like PARALLEL, CONCURRENT, etc.
        # print("ES un prebuild command:", comando)
        handle_prebuild_command(comando)
        return "continue"
    
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
            
            
def load_program(file):
    program = []
    
    with open(file, 'r') as f:
        program = f.readlines()
        for i, line in enumerate(program):
            program[i] = line.replace('\n', '')
    
    return program

def run_pll(file=None, program=None, principal=True):
    # print("args:", file, program)
    global loaded_program
    
    #TODO: Puedo hacer un PC (Program Counter) global y que ejecute segun ese PC en vez de un for.
    global pyskell_pc
    
    print_if_debug("RUNNING PROGRAM", file, program)
    
    # if program is not None:
    #     print("Se ejecuta el programa", program)
    
    if program is None and file is not None and principal:
        loaded_program = load_program(file)
        program = loaded_program
    elif program is None and file is None:
        return "Error."
        
    # print("PROGRAM TO USE:", program)
    # print("LENGTH:", len(program))
    pyskell_pc = 0
    
    while pyskell_pc < len(program):
    # for index_command in range(len(program)):
        # print("Voy por el index:", index_command)
        try:
            comando = program[pyskell_pc]
            # print("LLEGUE ACA1")
            regex = re.compile(r"[;][a-zA-Z]+$")
            # print("LLEGUE ACA2")
            # match = regex.search(command)
            if not comando.startswith('--') and not regex.search(comando):
                # print("LLEGUE ACA3")
                # print("comando a ejecutar", comando)
                run_command(comando)
                # print("LLEGUE ACA4")
        except:
            return "Error."
        pyskell_pc += 1