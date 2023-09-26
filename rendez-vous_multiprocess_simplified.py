################################################################################################
# Enunciado:    Implementar el problema de rendez-vous utilizando una barrera.
# Autor: Nicolás Villamonte
# Año: 2023
# Materia: Seminario de Programación Paralela y Concurrente
# Institucion: UNSAM (Universidad Nacional de San Martin)
# Fecha: 25/09/2023
################################################################################################

from threading import Thread, Barrier
import time
import random
from colorama import Fore, Back, Style

def print_c(text, color = Fore.RESET, bg_color = Back.RESET):
    print(bg_color + color + text + Style.RESET_ALL)

def proceso(i):
    print_c(f"Proceso {i}: Inicio de tarea.", color=Fore.GREEN)
    time.sleep(random.randint(1, 10))
    
    print_c(f"Proceso {i}: Llegué a la marca.", bg_color=Back.BLUE)
    barrier.wait()
    
    print_c(f"Proceso {i}: Continuando después del encuentro.", color=Fore.CYAN)

if __name__ == "__main__":
    # Número de procesos
    n = int(input("Ingrese el número de procesos: "))

    # Inicializar una barrera para n hilos
    barrier = Barrier(n)

    # Crear y lanzar los hilos
    threads = [Thread(target=proceso, args=(i,)) for i in range(n)]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    print_c("Finalización de ejecución de hilos.", color=Fore.YELLOW, bg_color=Back.RED)