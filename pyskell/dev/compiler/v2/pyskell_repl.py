from pyskell_execute import process_command, safe_eval, search_pyskell_function_by_name
from pyskell_utils import is_valid_list_or_tuple, pyskellRunProccess, apply_args
from pyskell_special_commands import special_commands
from pyskell_shared_global import version

def run_repl():
    print(f"Pyskell v{version}. For help type '!h' or 'help'.")
    while True:
        comando = input("> ")
        
        comando_split = None
        try:
            comando_split = process_command(comando)
        except Exception as e:
            print(f"Error: {e}.")
            continue
        
        special_func = special_commands.get(comando_split[0].lower().replace(' ', ''))
        
        if special_func:
            special_func() if len(comando_split[1:]) == 0 else special_func(comando_split[1:])
            continue
        
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