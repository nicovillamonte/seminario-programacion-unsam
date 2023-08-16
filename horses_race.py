################################################################################################
# Enunciado:    Implementar una "carrera de caballos" usando threads, donde cada "caballo" es un 
#               Thread o bien un objeto de una clase que sea sub clase de Thread, y contendrá una
#               posición dada por un número entero. El ciclo de vida de este objeto es incrementar 
#               la posición en variados instantes de tiempo, mientras no haya llegado a la meta, 
#               la cual es simplemente un entero prefijado. Una vez que un caballo llegue a la meta, 
#               se debe informar en pantalla cuál fue el ganador, luego de lo cual los demás caballos 
#               no deberán seguir corriendo. Imprimir durante todo el ciclo las posiciones de los 
#               caballos, o bien de alguna manera el camino que va recorriendo cada uno (usando 
#               símbolos Ascii). El programa podría producir un ganador disitnto cada vez que se corra. 
#               Opcionalmente, extender el funcionamiento a un array de n caballos, donde n puede ser 
#               un parámetro.
# Autor: Nicolás Villamonte
# Año: 2023
# Materia: Seminario de Programación Paralela y Concurrente
# Institucion: UNSAM (Universidad Nacional de San Martin)
# Fecha: 07/08/2023
################################################################################################

from threading import Thread, Event, Lock
from typing import List
import time
import random
import os

class Caballo(Thread):
    def __init__(self, nombre: str, evento_ganador: Event, lock_ganador: Lock) -> None:
        super().__init__()
        self.nombre = nombre
        self.distancia_recorrida = 0
        self.evento_ganador = evento_ganador
        self.lock_ganador = lock_ganador
        self.ganador = False

    def correr(self) -> None:
        while not self.evento_ganador.is_set():
            tiempo_espera = random.uniform(0.1, 0.5)  # Un tiempo aleatorio para simular la carrera
            time.sleep(tiempo_espera)
            self.distancia_recorrida += 1
            
            with print_lock:
                print_positions()

            if self.distancia_recorrida == distancia_carrera:
                with self.lock_ganador:  # Asegurarse de que solo un hilo pueda entrar en esta sección a la vez
                    if not self.evento_ganador.is_set():  # Verificar nuevamente dentro del lock
                        self.ganador = True
                        self.evento_ganador.set()

    def run(self):
        self.correr()
        

def print_positions():
    """Imprime las posiciones de los caballos en el transcurso de la carrera."""
    
    os.system('cls' if os.name == 'nt' else 'clear')    # Limpiar la pantalla
    
    print(f"Carrera de {len(caballos)} caballos por {distancia_carrera} metros:\n\n")                   # Titulo de la carrera
    for caballo in caballos:
        print("■" * caballo.distancia_recorrida + caballo.nombre)
    print("\n" + "═" * (distancia_carrera + 10))

if __name__ == "__main__":
    global distancia_carrera, caballos, print_lock
    cantidad_caballos = int(input("Cantidad de caballos: "))
    distancia_carrera = int(input("Distancia de la carrera: "))
    
    evento_ganador = Event()
    lock_ganador = Lock()  # Lock para garantizar que solo un hilo pueda declarar su victoria a la vez
    print_lock = Lock()
    caballos: List[Caballo] = [Caballo(f"Caballo {i + 1}", evento_ganador, lock_ganador) for i in range(cantidad_caballos)]

    print("La carrera se esta ejecutando...")
    for caballo in caballos:
        caballo.start()

    for caballo in caballos:
        caballo.join()

    print("Carrera terminada.")
    
    print("\nResultados:")
    caballo_ganador: Caballo = next((caballo for caballo in caballos if caballo.ganador), None)
    print(f"1° lugar: {caballo_ganador.nombre} ¡GANADOR! 🥇")
    caballos_ordenados: List[Caballo] = sorted(caballos, key=lambda caballo: caballo.distancia_recorrida, reverse=True)
    i: int = 1
    for _, caballo in enumerate(caballos_ordenados):
        if not caballo.ganador:
            print(f"{i+1}° lugar: {caballo.nombre}")
            i += 1
