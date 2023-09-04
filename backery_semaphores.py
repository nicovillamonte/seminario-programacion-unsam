from threading import Thread, Semaphore

sem = Semaphore()

def semaphored_section(i):
    "Define una funcion para el algoritmo de bakery en el proceso i con semaforos"
    
    print(f"{i}: non-critical section")
    for _ in range(1000000):
        pass
    
    sem.acquire()
    
    print(f"{i}: critical section")
    
    sem.release()

if __name__ == "__main__":
    global n_proc, turn
    n_proc = int(input("Number of threads: "))
    turn = [0] * n_proc
    
    # Creacion de threads
    threads = [Thread(target=semaphored_section, args=(i,)) for i in range(n_proc)]
    
    # Ejecucion de todos los threads
    for thread in threads:
        thread.start()