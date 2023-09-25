# Importando la biblioteca para trabajar con hilos y tiempo
from threading import Thread, Semaphore
import time
from colorama import Fore, Back, Style

# Inicializamos los semáforos para los dos procesos
sem1 = Semaphore(0)
sem2 = Semaphore(0)

def print_c(text, color = Fore.RESET, bg_color = Back.RESET):
  print(bg_color + color + text + Style.RESET_ALL)

def proceso1():
  print_c("Proceso 1: Inicio de tarea.", color=Fore.GREEN)
  time.sleep(2)  # Simular un retardo
  
  # Alcanzar la marca en el código
  print_c("Proceso 1: Llegué a la marca.", bg_color=Back.BLUE)
  sem2.release()  # Señal al segundo proceso que ya he llegado
  sem1.acquire()  # Esperar a que el segundo proceso llegue
  
  print_c("Proceso 1: Continuando después del encuentro.", color=Fore.GREEN)
  time.sleep(1)  # Simular un retardo adicional

def proceso2():
  print_c("Proceso 2: Inicio de tarea.", color=Fore.CYAN)
  time.sleep(1)  # Simular un retardo
  
  # Alcanzar la marca en el código
  print_c("Proceso 2: Llegué a la marca.", bg_color=Back.BLUE)
  sem1.release()  # Señal al primer proceso que ya he llegado
  sem2.acquire()  # Esperar a que el primer proceso llegue
  
  print_c("Proceso 2: Continuando después del encuentro.", color=Fore.CYAN)
  time.sleep(1)  # Simular un retardo adicional

# Crear y lanzar los hilos
hilo1 = Thread(target=proceso1)
hilo2 = Thread(target=proceso2)

hilo1.start()
hilo2.start()

hilo1.join()
hilo2.join()
print_c("Finalización de ejecución de hilos.", color=Fore.YELLOW, bg_color=Back.RED)