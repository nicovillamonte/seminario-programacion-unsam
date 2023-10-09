################################################################################################
# Enunciado:    Mediante una red de petri clásica, se debe modelar el problema de los filósofos
#               comensales. Se debe simular la situación en la que N filósofos se sientan alrededor
#               de una mesa y tienen N cubiertos para comer. Cada filósofo alterna entre pensar y
#               comer, y para comer debe tomar los dos cubiertos que tiene a su lado. Si un filósofo
#               no puede tomar ambos cubiertos, entonces no puede comer y debe volver a pensar.
#               Cuando un filósofo termina de comer, debe dejar los cubiertos sobre la mesa y volver
#               a pensar. El programa debe terminar cuando todos los filósofos hayan comido al menos
#               3 veces.
# Autor: Nicolás Villamonte
# Año: 2023
# Materia: Seminario de Programación Paralela y Concurrente
# Institucion: UNSAM (Universidad Nacional de San Martin)
# Fecha: 09/10/2023
################################################################################################

from snakes.nets import PetriNet, Place, Transition, dot, Value
from threading import Thread, Lock
from colorama import Fore, Back, Style
import os
import time
import random

output_lock = Lock()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_c(text, color = Fore.RESET, bg_color = Back.RESET):
    print(bg_color + color + text + Style.RESET_ALL)

class PhilosopherState:
    THINKING = "pensando"
    EATING = "comiendo"

class Philosopher(Thread):
    def __init__(self, id, petri_net, initial_state=PhilosopherState.THINKING):
        super().__init__()
        self.id = id
        self.initial_state = initial_state
        self.petri_net = petri_net
        self.eats = 0
        self.create_places_and_transitions()

    def create_places_and_transitions(self):
        self.thinking_place = self.create_place(PhilosopherState.THINKING)
        self.eating_place = self.create_place(PhilosopherState.EATING)
        self.take_forks_trans = self.create_transition(f"take_forks_{self.id}")
        self.put_forks_trans = self.create_transition(f"put_forks_{self.id}")

    def create_place(self, state):
        place_name = f"{state}_{self.id}"
        initial_token = [dot] if self.initial_state == state else []
        place = Place(place_name, initial_token)
        self.petri_net.add_place(place)
        return place

    def create_transition(self, name):
        transition = Transition(name)
        self.petri_net.add_transition(transition)
        return transition

    def run(self):
        self.eats = 0
        while self.eats < 3:
            self.execute_transition(self.take_forks_trans)
            self.show_status()
            self.execute_transition(self.put_forks_trans, eats = True)
            self.show_status()

    def execute_transition(self, transition, eats = False):
        modes = transition.modes()
        if modes:
            transition.fire(modes[0])
            if eats:
                self.eats += 1

    def show_status(self):
        print_status(self.petri_net, philosophers, forks)
        time.sleep(random.uniform(1, 5))

def print_status(petri_net, philosophers, forks):
    with output_lock:
        clear_screen()
        
        print_c("Cubiertos:")
        for i, fork in enumerate(forks):
            print_c(f"Cubierto {i+1} " + str(fork.tokens), color=Fore.GREEN if fork.tokens else Fore.RED)

        print_c("\nFilosofos:")
        for i, philosopher in enumerate(philosophers):
            state = "satisfecho" if philosopher.eats >= 3 else petri_net.place(f"{PhilosopherState.EATING}_{i}").tokens and PhilosopherState.EATING or PhilosopherState.THINKING
            print_c(f"Filósofo {i+1} está {state}", color=Fore.GREEN if state == "satisfecho" else (Fore.CYAN if state == PhilosopherState.THINKING else Fore.YELLOW))

def create_fork(id, petri_net):
    place = Place(f"cubierto_{id}", [dot])
    petri_net.add_place(place)
    return place

if __name__ == "__main__":
    N = int(input("Cantidad de filosofos: "))
    petri_net = PetriNet('Red')
    philosophers = [Philosopher(i, petri_net) for i in range(N)]
    forks = [create_fork(i, petri_net) for i in range(N)]

    for i, philosopher in enumerate(philosophers):
        prev = (i - 1) if i - 1 >= 0 else N - 1
        petri_net.add_input(forks[i].name, philosopher.take_forks_trans.name, Value(dot))
        petri_net.add_input(forks[prev].name, philosopher.take_forks_trans.name, Value(dot))
        petri_net.add_input(philosopher.thinking_place.name, philosopher.take_forks_trans.name, Value(dot))
        petri_net.add_output(philosopher.eating_place.name, philosopher.take_forks_trans.name, Value(dot))

        petri_net.add_input(philosopher.eating_place.name, philosopher.put_forks_trans.name, Value(dot))
        petri_net.add_output(forks[i].name, philosopher.put_forks_trans.name, Value(dot))
        petri_net.add_output(forks[prev].name, philosopher.put_forks_trans.name, Value(dot))
        petri_net.add_output(philosopher.thinking_place.name, philosopher.put_forks_trans.name, Value(dot))
    
    print_status(petri_net, philosophers, forks)
    time.sleep(2)

    for philosopher in philosophers:
        philosopher.start()

    for philosopher in philosophers:
        philosopher.join()

    print_status(petri_net, philosophers, forks)
    print_c("Todos los filósofos están satisfechos", color=Fore.RED, bg_color=Back.YELLOW)
