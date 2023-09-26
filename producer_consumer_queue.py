################################################################################################
# Enunciado:    Implementar el problema de productor-consumidor utilizando una cola simple.
# Autor: Nicolás Villamonte
# Año: 2023
# Materia: Seminario de Programación Paralela y Concurrente
# Institucion: UNSAM (Universidad Nacional de San Martin)
# Fecha: 25/09/2023
################################################################################################

from threading import Thread, Semaphore 
from queue import SimpleQueue
from time import sleep
from random import uniform
from colorama import Fore, Back, Style

# Definimos el buffer como una cola simple sin límite de tamaño
buffer = SimpleQueue()

# Función del productor
def productor_fn(id):
    for i in range(10):
        item = f"item-{id}-{i}"
        buffer.put(item)
        print((Fore.RED if id == 1 else Fore.MAGENTA) + f"Productor {id} produjo {item}" + Style.RESET_ALL)
        sleep(uniform(0.1, 0.7))

# Función del consumidor
def consumidor_fn():
    for i in range(20):  # Debe ser igual al doble del rango del productor ya que tenemos 2 productores
        item = buffer.get()
        print( Fore.BLACK + Back.GREEN + f"Consumidor consumió {item}" + Style.RESET_ALL)
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
