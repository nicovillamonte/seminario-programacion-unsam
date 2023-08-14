################################################################################################
# Enunciado:    Se debe desarrollar un programa en Python que simule una carrera de 10 caballos 
#               en la que cada caballo avanza un metro a la vez hasta llegar a 20 metros, 
#               utilizando hilos para representar el avance de cada caballo de forma paralela. 
#               Cada caballo debe correr en un hilo separado, y el primero en llegar a la meta 
#               debe declarar “Gane”, deteniendo los procesos de los demás caballos.
# Autor: Nicolás Villamonte
# Año: 2023
# Materia: Seminario de Programación Paralela y Concurrente
# Institucion: UNSAM (Universidad Nacional de San Martin)
# Fecha: 07/08/2023
################################################################################################

from threading import Thread, Event, Lock
import time
import random

class Caballo(Thread):
    def __init__(self, nombre, evento_ganador, lock_ganador):
        super().__init__()
        self.nombre = nombre
        self.distancia_recorrida = 0
        self.evento_ganador = evento_ganador
        self.lock_ganador = lock_ganador

    def correr(self):
        while self.distancia_recorrida < 20 and not self.evento_ganador.is_set():
            tiempo_espera = random.uniform(0.1, 0.5)  # Un tiempo aleatorio para simular la carrera
            time.sleep(tiempo_espera)
            self.distancia_recorrida += 1

            if self.distancia_recorrida == 20:
                with self.lock_ganador:  # Asegurarse de que solo un hilo pueda entrar en esta sección a la vez
                    if not self.evento_ganador.is_set():  # Verificar nuevamente dentro del lock
                        print(f"{self.nombre} dice: ¡Gané!")
                        self.evento_ganador.set()

    def run(self):
        self.correr()

if __name__ == "__main__":
    cantidad_caballos = 5
    evento_ganador = Event()
    lock_ganador = Lock()  # Lock para garantizar que solo un hilo pueda declarar su victoria a la vez
    caballos = [Caballo(f"Caballo {i + 1}", evento_ganador, lock_ganador) for i in range(cantidad_caballos)]

    print("La carrera se esta ejecutando...")
    for caballo in caballos:
        caballo.start()

    for caballo in caballos:
        caballo.join()

    print("Carrera terminada.")
