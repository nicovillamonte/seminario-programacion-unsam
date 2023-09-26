################################################################################################
# Enunciado:    Implementar el problema de rendez-vous para múltiples procesos con semáforos.
# Autor: Nicolás Villamonte
# Año: 2023
# Materia: Seminario de Programación Paralela y Concurrente
# Institucion: UNSAM (Universidad Nacional de San Martin)
# Fecha: 25/09/2023
################################################################################################

# Importando la biblioteca para trabajar con hilos y tiempo
from threading import Thread, Semaphore
import time
import random
from colorama import Fore, Back, Style

def print_c(text, color = Fore.RESET, bg_color = Back.RESET):
    print(bg_color + color + text + Style.RESET_ALL)

def proceso(i):
    print_c(f"Proceso {i}: Inicio de tarea.", color=Fore.GREEN)
    # Simular un retardo random entre 1 y 10 segundos
    time.sleep(random.randint(1, 10))
    
    # Alcanzar la marca en el código
    print_c(f"Proceso {i}: Llegué a la marca.", bg_color=Back.BLUE)
    
    # Notificar a todos los demás procesos
    for j in range(n):
        if i != j:
            sems[j].release()
    
    # Esperar a que todos los demás procesos lleguen
    for j in range(n):
        if i != j:
            sems[i].acquire()
    
    print_c(f"Proceso {i}: Continuando después del encuentro.", color=Fore.CYAN)
    time.sleep(1)  # Simular un retardo adicional
    
if __name__ == "__main__":
    # Número de procesos
    n = int(input("Ingrese el número de procesos: "))
    
    # Creación de n semáforos
    sems = [Semaphore(0) for _ in range(n)]

    # Crear y lanzar los hilos
    hilos = [Thread(target=proceso, args=(i,)) for i in range(n)]

    for hilo in hilos:
        hilo.start()

    for hilo in hilos:
        hilo.join()

    print_c("Finalización de ejecución de hilos.", color=Fore.YELLOW, bg_color=Back.RED)