################################################################################################
# Enunciado:    Implementar el algoritmo de Bakery para dos procesos.
# Autor: Nicolás Villamonte
# Año: 2023
# Materia: Seminario de Programación Paralela y Concurrente
# Institucion: UNSAM (Universidad Nacional de San Martin)
# Fecha: 03/09/2023
################################################################################################

from threading import Thread
from colorama import Fore, Back, Style
import random

def bakery_algorithm(i):
    "Define una funcion para el algoritmo de bakery en el proceso i"
    
    global n_proc, turn
    
    for _ in range(random.randint(1, 10000000)):
        pass
    print(f"{i}: non-critical section")
    
    turn[i] = 1 + max(turn)
    
    for j in range(n_proc):
        if j == i:
            continue
        while turn[j] != 0 and (turn[i] > turn[j] or (turn[i] == turn[j] and i > j)):
            pass
    
    print(Fore.BLACK + Back.RED + f"{i}: critical section" + Style.RESET_ALL)
    
    turn[i] = 0
    

if __name__ == "__main__":
    global n_proc, turn
    n_proc = int(input("Number of threads: "))
    turn = [0] * n_proc
    
    # Creacion de threads
    threads = [Thread(target=bakery_algorithm, args=(i,)) for i in range(n_proc)]
    
    # Ejecucion de todos los threads
    for thread in threads:
        thread.start()