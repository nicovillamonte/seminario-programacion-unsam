# Introducción

En este documento se abordará de manera exhaustiva el proceso integral de diseño y construcción de una Red de Petri destinada a resolver el problema clásico de los filósofos comensales. 

Este problema propone una situación en la que cinco filósofos se encuentran sentados en una mesa circular, donde cada uno piensa profundamente y, ocasionalmente, interrumpe sus reflexiones para alcanzar los tenedores que se encuentran a su izquierda y derecha con el objetivo de degustar el platillo que tienen frente a sí. La complejidad surge al requerir que cada filósofo necesite ambos tenedores para comer, lo que lleva a la necesidad de establecer un protocolo que evite situaciones de bloqueo y hambruna.

Las simulaciones se realizarán con la página https://petri.hp102.ru/pnet.html

[**Desarrollo**](#desarrollo)

1. [Primer Versión](#primer-versión)
    1. [Características de los Filósofos](#características-de-los-filósofos)
    2. [Un sólo filósofo](#un-sólo-filósofo)
    3. [Dos filósofos](#dos-filósofos)
2. [Segunda Versión](#segunda-versión)
    1. [Nuevos Filósofos](#nuevos-filósofos)
    2. [Segunda versión con 1 filósofo](#segunda-versión-con-1-filósofo)
    3. [2 filósofos sin DeadLock](#2-filósofos-sin-deadlock)
3. [Solución final](#solución-final)

# Desarrollo

Conforme se mencionó anteriormente, adoptaremos un enfoque progresivo para resolver el problema de los filósofos comensales. Iniciaremos simplificando el problema con el objetivo de, gradualmente, alcanzar una solución robusta y funcional sin enfrentar dificultades abrumadoras en el proceso.

Principalmente, consideraremos que los filósofos comensales piensan mientras se encuentran esperando el primer cubierto. Por lo tanto, las tareas que desempeñarán serán las siguientes: agarrar el cubierto derecho, agarrar el cubierto izquierdo, comer, y posteriormente, volver a dejar los cubiertos sobre la mesa. No nos preocuparemos por el momento por los bloqueos.

Esta simplificación permite una aproximación inicial más manejable al problema, facilitando la estructuración y análisis de la Red de Petri en las etapas iniciales de desarrollo. A medida que progresamos, iremos incrementando la complejidad para abordar el problema en su totalidad, permitiendo así una comprensión y solución sistemáticas y bien fundamentadas del desafío presentado por los filósofos comensales.

## Primer Versión

### Características de los Filósofos

Propondremos una solución inicial al problema de los filósofos comensales en su versión simplificada, utilizando Redes de Petri. Para ello, es crucial entender la función de los elementos constituyentes de la red, tales como los *lugares* (places), las *transiciones* y los *tokens*. Por lo tanto, estableceremos una serie de reglas antes de proceder con la elaboración de la red:
- Los **filósofos** estarán representados por todos sus estados posibles, los cuales serán delineados mediante *lugares* en la Red de Petri. En este escenario, un filósofo puede encontrarse en uno de los tres estados siguientes:
    - Posee el cubierto derecho (Posee CD)
    - Posee ambos cubiertos y puede comer. (Comiendo)
    - Ha concluido su comida y ha regresado los cubiertos a la mesa y/o está esperando los cubiertos para comer, lo que le da tiempo de pensar. (Pensando)
- Dada la simplificación del problema, donde se omite el estado de reflexión de los filósofos, el estado inicial se define como aquel en el que los filósofos ya han comido y han dejado los cubiertos en la mesa. Consecuentemente, se situará un token en el lugar que representa este estado. 
- Los **cubiertos** también serán representados por *lugares* en la red. Inicialmente, cada cubierto contará con un token, indicando que dicho recurso se encuentra disponible sobre la mesa para ser tomado por los filósofos.
- Las **acciones**, tales como tomar un cubierto, dejar un cubierto, y comer, serán representadas mediante las *transiciones*. Todas estas acciones son ejecutadas por los filósofos, mientras que los cubiertos solo se ven afectados por las mismas.

### Un sólo filósofo

Ahora, examinaremos cómo se representaría un solo filósofo en esta red:

<div align="center" id="img-1">
  <img src="https://github.com/nicovillamonte/seminario-programacion-unsam/assets/64659720/96362c82-e194-46d0-8c2f-a6aea0a8e024" alt="1  Diagramas de Petri-1 filo dl simple"  />
</div>

A continuación, asignaremos los cubiertos a este filósofo para evitar que coma con las manos:

<div align="center" id="img-2">
  <img src="https://github.com/nicovillamonte/seminario-programacion-unsam/assets/64659720/f1144324-ad28-4fc5-9a98-f8300febe6e7" alt="2  Diagramas de Petri-1 filo dl simple con cubiertos"  />
</div>

La simulación se ve de esta manera:

<div align="center" id="gif-1">
  <img src="https://github.com/nicovillamonte/seminario-programacion-unsam/assets/64659720/3a8db7c1-ded9-40c5-bd4b-08ab12dbfc0e" alt="Gif Diagramas de Petri-1 filo dl simple con cubiertos"  />
</div>


### Dos filósofos

Una vez tenemos un filósofo con sus cubiertos funcionando, vamos a hacer el intento de agregar un filósofo más a la red que deba utilizar los mismos cubiertos que el anterior, en donde comienza el hecho de compartir los cubiertos o los recursos si hablamos del sistema en sí.

<div align="center" id="img-3">
  <img src="https://github.com/nicovillamonte/seminario-programacion-unsam/assets/64659720/02d91269-876c-4095-a31e-300cabf65163" alt="3  Diagramas de Petri-2 filo dl simple con cubiertos"  />
</div>

Vamos a ver como se ejecuta la simulación de esta red de Petri con 2 filósofos.

------------------------------------GIF DE SEGUNDA SIMULACIÓN

En este contexto, nos podemos encontrar con la situación en la que un filósofo toma uno de los cubiertos mientras el otro filósofo toma el cubierto restante, resultando en una circunstancia donde ambos filósofos permanecen en espera del cubierto que tiene el otro y, por ende, se hallan incapaces de comer. Esta condición de espera mutua conduce a un estancamiento, donde ninguno de los filósofos puede avanzar hacia el siguiente estado de la operación. Acabamos de producir un **DeadLock**.

Por lo tanto, ahora vamos a hacer otra versión en la que solucionaremos este problema.

## Segunda Versión

Necesitaremos modificar la interacción entre los filósofos y los cubiertos. Una idea inicial podría ser que, antes de que el filósofo tome uno de los cubiertos, verifique la disponibilidad del otro cubierto. Si ambos están disponibles, entonces bloquearía ambos cubiertos para los otros filósofos, asegurando que estén disponibles cuando decida tomarlos, evitando así su uso por otros filósofos.

En términos de las Redes de Petri, esto se traduce en demostrar que, si ambos cubiertos están disponibles, el filósofo los toma simultáneamente. Esta modificación en la lógica de interacción introduce una coordinación más efectiva entre los filósofos, minimizando el riesgo de caer en condiciones de Deadlock y promoviendo un flujo operativo más fluido en la red.

### Nuevos Filósofos

Por lo tanto, vamos a tomar a los filósofos con las siguientes propiedades:
- Sus estados, representados por *lugares*, se reducirán a los siguientes:
    - **Pensando**: Estado en el que el filósofo esta esperando la disponibilidad de los cubiertos o pensando antes de querer tomarlos.
    - **Comiendo**: Estado en el que pudo tomar los dos cubiertos y comer, una vez en este estado ya estará listo para tomar la transición en la que deba dejar ambos cubiertos y volver a pensar
- Las *transiciones* por las que va a pasar serán:
    - **Tomar cubiertos**: Acción en la que toma ambos cubiertos a la vez solamente si ambos se encuentran disponibles y la que transicionará al filósofo a su estado de comer.
    - **Dejar cubiertos**: Acción en la que el filósofo ya haya comido y quiera dejar los cubiertos en su lugar para seguir pensando.

### Segunda versión con 1 filósofo

El estado del filósofo comenzará cuando el filósofo este pensando o esperando que los cubiertos se encuentren disponibles, cuando eso sea así, el mismo va a transicionar al estado en el que estará comiendo y, finalmente, dejará los cubiertos y se pondrá a pensar nuevamente cuando termine de comer.

<div align="center" id="img-4">
  <img src="https://github.com/nicovillamonte/seminario-programacion-unsam/assets/64659720/3e0a3535-b183-4eee-965d-ba9fd5086d15" alt="4  Diagramas de Petri-1 filo correcto"  />
</div>

Ahora podemos añadirle, al único filósofo que tenemos, dos cubiertos para que pueda comer, lo que nos quedaría de la siguiente manera:

<div align="center" id="img-5">
  <img src="https://github.com/nicovillamonte/seminario-programacion-unsam/assets/64659720/0464078b-e685-49ee-98c8-984a43a0cfe6" alt="5  Diagramas de Petri-1 filo correcto con cubiertos"  />
</div>

Esta vez, cuando el filósofo deje de pensar o esperar y quiera tomar los cubiertos, va a tomarlos los dos al mismo tiempo solamente si están ambos disponibles, luego comerá y dejará los dos cubiertos nuevamente para volver a pensar y repetir el bucle constantemente.


------------------------------------GIF DE TERCERA SIMULACIÓN

### 2 filósofos sin DeadLock

A esta última solución le vamos a agregar otro filósofo como hicimos previamente con la anterior posible solución para ver si se produce algún problema cuando los recursos se comienzan a compartir.

<div align="center" id="img-6">
  <img src="https://github.com/nicovillamonte/seminario-programacion-unsam/assets/64659720/a107ec61-0f8f-4ef5-b9c3-22ff37dc57cd" alt="6  Diagramas de Petri-2 filo correcto con cubiertos"  />
</div>

Cuya simulación podría verse de la siguiente manera:

------------------------------------GIF DE CUARTA SIMULACIÓN

> IMPORTANTE: Se logra ver que solo uno de los filósofos llega a comer, esto no se debe a un error en la Red de Petri, sino que se debe al software que se esta utilizando para simularla, ya que cuando debe decidir entre dos _lugares_ de la red elige el que tiene valor más bajo en su etiqueta. Se puede ver cómo funcionaría agregando un _token_ a los cubiertos.

## Solución final

La solución anterior funcionó perfectamente con dos comensales, por lo que ya tenemos el visto bueno para confeccionar la Red de Petri que solucione el problema en su totalidad con los 5 filósofos incluídos en la misma. La solución es la siguiente:

<div align="center" id="img-7">
  <img src="https://github.com/nicovillamonte/seminario-programacion-unsam/assets/64659720/2a9f5fcc-96c7-4f20-b3ab-dd313b566a27" alt="7  Diagramas de Petri-Solucion Completa"  />
</div>

La cual responde al siguiente esquema:

<div align="center" id="img-8">
  <img src="https://github.com/nicovillamonte/seminario-programacion-unsam/assets/64659720/c5b48171-d050-40a2-9fe0-82c5b3ff729d" alt="Esquema"  />
</div>

















