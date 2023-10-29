# TODO - Pyskell

Orden de prioridad:
- [Paralelismo por secciones](#paralelismo-por-secciones)

Sin prioridad:
- [Asignacion parcial](#asignacion-parcial)

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

## Asignacion parcial

- [ ] Listo

```
res = suma ?num
res 5
```

Y que `res 5` devuelva `num+5` (o sea, que se pueda usar como una funcion), ya que en realidad las asignaciones son funciones.

## Agregarle al `for` los parametros de `step` y `start`

Todavia no es seguro como se quiere realizar, por el momento el for solo acepta dos parametros, nombre de la variable y cantidad de iteraciones.

```
for i 5
    ...
```