from threading import Thread
from colorama import Fore, Back, Style

# Variable compartida para determinar el turno
turn = 1

def process_p():
    global turn
    
    for _ in range(5):      # No hacemos un loop infinito para que el programa termine
        print("p: non-critical section")
        while turn != 1:    # Esperamos a que sea el turno de p, cuando turn == 1
            pass
        print(Fore.BLACK + Back.GREEN + "p: critical section" + Style.RESET_ALL)
        turn = 2

def process_q():
    global turn
    
    for _ in range(5):
        print("q: non-critical section")
        while turn != 2:    # Esperamos a que sea el turno de q, cuando turn == 2
            pass
        print(Fore.BLACK + Back.YELLOW + "q: critical section" + Style.RESET_ALL)
        turn = 1
        

if __name__ == "__main__":
    thread_p = Thread(target=process_p)
    thread_q = Thread(target=process_q)

    # Iniciar threads
    thread_p.start()
    thread_q.start()
