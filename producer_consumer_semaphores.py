################################################################################################
# Enunciado:    Implementar el problema de productor-consumidor utilizando semáforos.
# Autor: Nicolás Villamonte
# Año: 2023
# Materia: Seminario de Programación Paralela y Concurrente
# Institucion: UNSAM (Universidad Nacional de San Martin)
# Fecha: 25/09/2023
################################################################################################

from threading import Thread, Semaphore 
from time import sleep
from random import uniform
from colorama import Fore, Back, Style

# Inicializamos el buffer como una lista vacía
buffer = []

# Inicializamos el semáforo de acceso al buffer
buffer_access = Semaphore(1)

# Inicializamos el semáforo para indicar que el buffer no está vacío
notEmpty = Semaphore(0)

# Función del productor
def productor_fn(id):
    for i in range(10): # Vamos a producir 10 items por cada productor
        item = f"item-{id}-{i}"
        
        # Adquirir el semáforo antes de acceder al buffer
        buffer_access.acquire()
        
        buffer.append(item)
        print((Fore.RED if id == 1 else Fore.MAGENTA) + f"Productor {id} produjo {item}" + Style.RESET_ALL)
        
        # Señalamos que el buffer no está vacío
        notEmpty.release()
        
        # Liberar el semáforo después de acceder al buffer
        buffer_access.release()
        
        sleep(uniform(0.1, 0.7))

# Función del consumidor
def consumidor_fn():
    for i in range(20):  # Debe ser igual al doble del rango del productor ya que tenemos 2 productores
        # Esperamos hasta que el buffer no esté vacío
        notEmpty.acquire()
        
        # Adquirir el semáforo antes de acceder al buffer
        buffer_access.acquire()
        
        item = buffer.pop(0)
        print( Fore.BLACK + Back.GREEN + f"Consumidor consumió {item}" + Style.RESET_ALL)
        
        # Liberar el semáforo después de acceder al buffer
        buffer_access.release()
        
        sleep(uniform(0.2, 0.6))

if __name__ == "__main__":
    # Creamos threads para los productores y el consumidor
    productor1 = Thread(target=productor_fn, args=(1,))
    productor2 = Thread(target=productor_fn, args=(2,))
    consumidor = Thread(target=consumidor_fn)

    # Iniciamos los threads
    productor1.start()
    productor2.start()
    consumidor.start()

    # Esperamos a que todos los threads terminen
    productor1.join()
    productor2.join()
    consumidor.join()