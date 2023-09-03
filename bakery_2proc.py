################################################################################################
# Enunciado:    Implementar el algoritmo de Bakery para N procesos.
# Autor: Nicolás Villamonte
# Año: 2023
# Materia: Seminario de Programación Paralela y Concurrente
# Institucion: UNSAM (Universidad Nacional de San Martin)
# Fecha: 03/09/2023
################################################################################################


from threading import Thread

np, nq = 0, 0  # type: (int, int)


def process_p():
    # Proccess p code for bakery algorithm
    
    global np, nq
    
    print("p: non-critical section")
    for i in range(1000000):
        pass
    
    np = nq + 1
    
    while not (nq == 0 or np <= nq):
        pass
    
    print("p: critical section")
    
    np = 0
    

def process_q():
    # Proccess q code for bakery algorithm
    
    global np, nq
    
    print("q: non-critical section")
    for i in range(1000000):
        pass
    
    nq = np + 1
    
    while not (np == 0 or nq < np):
        pass
    
    print("q: critical section")
    
    nq = 0
    

if __name__ == "__main__":
    # Creamos los Threads
    p_thread = Thread(target=process_p)
    q_thread = Thread(target=process_q)
    
    # Comenzamos los Threads
    p_thread.start()
    q_thread.start()