# TODO - Pyskell

Proximo a hacer
- [X] Mejorar el codigo para que en vez de comentarlo tenga una lista de comandos ya corridos en paralelo para que no se vuelvan a correr.
- [ ] Hacer que los archivos de dist temporales se eliminen al terminar de ejecutar el programa.
- [ ] Hacer la keyword concurrent para concurrencia.
- [ ] Ver si pasar estas keywords solo a mayuscula
- [ ] Poder ponerle nombre a `parallel` y `concurrent` y hacer un `wait nombre` para esperar a que termine antes de avanzar. (semaforos)

Orden de prioridad:
- [Manejo de archivos](#manejo-de-archivos)
- [Paralelismo por secciones](#paralelismo-por-secciones)
- [Agregar semaforos](#agregar-semaforos)

Sin prioridad:
- [Asignacion parcial](#asignacion-parcial)

Otros:
- No imprimir las lineas de asignacion al menos que se active el flag `--print-assigns`
- Hacer un help de como utilizar el comando pyskell
- Agregarle al `for` los parametros de `step` y `start` o `in` para recorrer una lista
- Concurrencia. Ademas del bloque PARALELL, agregarle un bloque CONCURRENT, lo unico que cambiaria en la implementacion es el uso de Threads en vez de Proccess.

## Manejo de archivos

- [ ] Listo

Poder cargar archivos excell con un comando `load`, obtener y modificar sus celdas.

Otra opcion es cargar el archivo con load para todo un bloque de codigo, y que se pueda acceder y modificar en la misma linea que se hace una operacion, por ejemplo.

```
load archivo.xlsx
factorial 2 <=> A1
```

Tambien que se pueda utilizar la propia celda como parametro de una funcion, por ejemplo.

```
load archivo.xlsx
facorial _/2 <=> A1
```

el simbolo `_` representa el valor de la celda actual, y el simbolo `<=>` representa que el resultado de la operacion se guarde en la celda. Es un ida y vuelta.

Tambien deberia ser posible utilizar el valor de alguna celda, pero sin modificarla, por ejemplo.

```
load archivo.xlsx
variable = factorial _ => A1
```

Otra cosa que se deberia poder hacer es recorrer las filas y columnas de un archivo, por ejemplo.

```
load archivo.xlsx

for i 10
    for j 10
        factorial _ <=> i.j
```

Siendo i la letra y j el numero de la columna. Pero internamente el numero se convierte en la letra.

## Paralelismo por secciones

- [ ] Listo

```
suma ?num ?num2
paralell
    doble 3
    for i 5
        factorial 30
end_paralell
doble ?num
```

La idea es que esto se separe en el builder.
Por el momento al hacer build de un programa, las lineas agrupadas quedan asi:

```
doble 2
for i 5
    doble i+1
    doble i-1
factoial 3
```
->
```
['doble 2', ('for i 5', ['doble i+1', 'doble i-1']), 'factorial 3']
```

Lo que despues se sigue procesando, pero por ahora queremos centrarnos en agregar otro formato a ese agrupamiento para los bloques de paralelismo, para lo que vamos usar un objeto esta vez, de tipo `PyskellParalellCode`: 

```
doble 2
paralell
    doble 3
    for i 3
        doble i+1
end_paralell
factoial 3
```
->
```
['doble 2', PyskellParalellCode('doble 3',('for i 3', ['doble i+1'])), 'factorial 3']
```

Lo que deberia convertirse a algo asi en el `expanded lines`:

```
['doble 2', PyskellParalellCode('doble 3', 'doble 1', 'doble 2', 'doble 3'), 'factorial 3']
```

### PyskellParalellCode

Va a poder recibir una lista de strings, puede ser modificado externamente para su procesamiento y cambiar su lista de comandos. Tambien va a poder mostrar su lista de comandos para que sean ejecutados externamente. Este objeto se encarga de encapsular estos datos y no de ejecutarlos ni modificarlos.

### Otra opcion

Otra opcion para esta solucion es no complicarnos tanto por el momento con clases y responsabilidades. Sino que se haga de la misma forma que se hizo el for. Entonces en vez de esto

```
['doble 2', PyskellParalellCode('doble 3',('for i 3', ['doble i+1'])), 'factorial 3']
```

Tendriamos esto

```
['doble 2', ('PARALELL', ['doble 3', ('for i 3', ['doble i+1'])]), 'factorial 3']
```

Teniendo en cuenta siempre que se comienza con un PARALELL y se termina con un END_PARALELL.

```
doble 2
PARALELL
    doble 3
    for i 3
        doble i+1
END_PARALELL
factoial 3
```

Luego, teniendo en cuenta que el builder solamente se encarga de agrupar las lineas, el agrupamiento quedaria asi para pasarlo al archivo .rpll y que luego el executer lo interprete:

```
['doble 2',  '__p', 'doble 3', 'doble 3', 'doble 1', 'doble 2', 'doble 3', '__ep', 'factorial 3']
```


### Guardado en el rpll

Si tenemos un codigo asi

```
doble 2
paralell
    doble 3
    for i 3
        doble i+1
factorial 3
```

Vamos a tener esto en el group

```
['doble 2', ('paralell', ['doble 3', ('for i 3', ['doble i+1'])]), 'factorial 3']
```

De alguna manera, esto tiene que ser guardado en el rpll, para que luego el executer lo interprete. La idea es que se guarde asi:

```
doble 2
$id$:pl
doble 3
doble 1
doble 2
doble 3
$id$;pl
factorial 3
```

El `id` representa un hash unico que es atribuido tanto a su inicio como su final, para que el executer sepa que es un bloque de paralelismo. El `:pl` representa que es un bloque de paralelismo, y el `;pl` representa el final del bloque de paralelismo.

### Bloques de paralelismo anidados

```
doble 2
paralell
    paralell
        doble 3
        doble 4
    paralell
        doble 1
        doble 176
factorial 3
```

Algo asi deberia ser posible. Lo que haria que ambos paralell se ejecuten en paralelo y, a su vez, estos creen otro paralelismo para ejecutar sus comandos. Lo que haria que cuando uno de los dos procesos termine, el otro deba esperarlo para seguir por fuera del paralell.

## Agregar semaforos

```
doble 2
hola = suma 3 3
paralell
    paralell
        doble 3
        sem nombreSemaforo
            hola = 3
        doble 4
    paralell
        doble 1
        sem nombreSemaforo
            hola = 4
        doble 176
factorial 3
```



## Asignacion parcial

- [ ] Listo

```
res = suma ?num
res 5
```

Y que `res 5` devuelva `num+5` (o sea, que se pueda usar como una funcion), ya que en realidad las asignaciones son funciones.

Esto incluye que si yo tengo esto

```
res = suma 3 54
res
```

Devuelva `57`.

## Agregarle al `for` los parametros de `step` y `start`

Todavia no es seguro como se quiere realizar, por el momento el for solo acepta dos parametros, nombre de la variable y cantidad de iteraciones.

```
for i 5
    ...
```