################################################################################################
# Enunciado:    Implementar el algoritmo de Bakery para dos procesos haciendo uso de los 
#               semaforos.
# Autor: Nicolás Villamonte
# Año: 2023
# Materia: Seminario de Programación Paralela y Concurrente
# Institucion: UNSAM (Universidad Nacional de San Martin)
# Fecha: 03/09/2023
################################################################################################

from threading import Thread, Semaphore
from colorama import Fore, Back, Style

sem = Semaphore()

def semaphored_section(i):
    "Define una funcion para el algoritmo de bakery en el proceso i con semaforos"
    
    for _ in range(1000000):
        pass
    print(f"{i}: non-critical section")
    
    sem.acquire()
    
    print(Fore.BLACK + Back.RED + f"{i}: critical section" + Style.RESET_ALL)
    
    sem.release()

if __name__ == "__main__":
    global n_proc
    n_proc = int(input("Number of threads: "))
    
    # Creacion de threads
    threads = [Thread(target=semaphored_section, args=(i,)) for i in range(n_proc)]
    
    # Ejecucion de todos los threads
    for thread in threads:
        thread.start()
