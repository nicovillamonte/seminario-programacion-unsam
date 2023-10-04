#! EN PROCESO

from snakes.nets import *
import time

# Creamos la red
net = PetriNet('Red')

# Pedimos al usuario que ingrese la cantidad de filósofos
N = int(input("Cantidad de filosofos: "))

# Funcion para crear los filósofos
def createPhilosopher(index):
  p0 = Place(f"pensando{index}", [dot])
  p1 = Place(f"comiendo{index}", [])
  return [p0,p1]


# Creación de los filósofos
filosofos = [createPhilosopher(i) for i in range(N)]
# Creación de los cubiertos
cubiertos = [Place(f"cubierto{i}", [dot]) for i in range(N)]

# Creación de las transiciones
dejar_cubiertos = [Transition(f'tomar_{i}') for i in range(N)]
tomar_cubiertos = [Transition(f'dejar_{i}') for i in range(N)]

# Agregado a la red de los cubiertos
for cubierto in cubiertos:
  net.add_place(cubierto)

# Agregado a la red de los estados de los filosofos
for filosofo in filosofos:
  for estado in filosofo:
    net.add_place(estado)

# Agregado a la red de las transiciones
for grupo_transiciones in [dejar_cubiertos, tomar_cubiertos]:
  for transicion in grupo_transiciones:
    net.add_transition(transicion)

for index, filosofo in enumerate(filosofos):
  index_anterior = (index - 1) if index - 1 >= 0 else N - 1
  
  # Agregar inputs y outputs de la tansicion de tomar cubiertos del filósofo
  net.add_input(str(cubiertos[index]), str(tomar_cubiertos[index]), Value(dot))
  net.add_input(str(cubiertos[index_anterior]), str(tomar_cubiertos[index]), Value(dot))
  net.add_input(str(filosofo[0]), str(tomar_cubiertos[index]), Value(dot))
  net.add_output(str(filosofo[1]), str(tomar_cubiertos[index]), Value(dot))
  
  # Agregar inputs y outputs de la tansicion de dejar cubiertos del filósofo
  net.add_input(str(filosofo[1]), str(dejar_cubiertos[index]), Value(dot))
  net.add_output(str(cubiertos[index]), str(dejar_cubiertos[index]), Value(dot))
  net.add_output(str(cubiertos[index_anterior]), str(dejar_cubiertos[index]), Value(dot))
  net.add_output(str(filosofo[0]), str(dejar_cubiertos[index]), Value(dot))
  
# Imprimir en tiempo real una simulación de las transiciones
for i in range(N):
    trans = str(tomar_cubiertos[i])
    modes = net.transition(trans).modes()
    if trans in [t.name for t in net.transition()]:
        if modes:
            net.transition(trans).fire(modes[0])

    os.system('cls' if os.name == 'nt' else 'clear')

    # Mostrar el estado de los cubiertos
    for i in range(N):
        print(f"Fork{i}", net.place(str(cubiertos[i])).tokens)

    # Mostrar el estado de los filósofos
    for i, (pensando, comiendo) in enumerate(filosofos):
        estado = "comiendo" if net.place(str(comiendo)).tokens else "pensando"
        print(f"Filósofo{i} está {estado}")

    time.sleep(2)


# Print forks
os.system('cls' if os.name == 'nt' else 'clear')    # Limpiar la pantalla
for i in range(N):
  print(f"Fork{i}", net.place(str(cubiertos[i])).tokens)
  