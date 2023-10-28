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
    for i 5
        factorial 30
end_paralell
doble ?num
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