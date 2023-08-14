################################################################################################
# Enunciado:    Se debe desarrollar un programa en Python que simule la tirada de una cantidad 
#               N de dados al mismo tiempo de forma paralela utilizando hilos. Cada dado debe 
#               ser tirado en un hilo separado, y una vez que todos los dados hayan sido tirados, 
#               se debe sumar el resultado obtenido en cada dado e imprimirlo. Si la suma de los 
#               resultados es menor a 15, entonces se debe volver a tirar los dados, repitiendo 
#               el proceso hasta que la suma sea mayor o igual a 15.
# Autor: Nicolás Villamonte
# Año: 2023
# Materia: Seminario de Programación Paralela y Concurrente
# Institucion: UNSAM (Universidad Nacional de San Martin)
# Fecha: 14/08/2023
################################################################################################

from threading import Thread
import random

def tirar_dado(resultado):
    # Simula tirar un dado y almacena el resultado en la lista
    dado = random.randint(1, 6)
    resultado.append(dado)

N = 5  # Número de dados

# Realiza la tirada de dados en paralelo hasta que la suma sea >= 15
while True:
    resultado = []
    dados = []

    # Crea y comienza los dados para tirar los dados
    for i in range(N):
        dado = Thread(target=tirar_dado, args=(resultado,))
        dados.append(dado)
        dado.start()

    # Espera a que todos los dados terminen
    for dado in dados:
        dado.join()

    suma = sum(resultado)
    print(f"Resultado de la tirada: {resultado} - Suma: {suma}")

    # Si la suma es >= 15, termina el bucle
    if suma >= 15:
        print("La suma es mayor o igual a 15, terminando el programa.")
        break