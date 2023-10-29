# Bugs a arreglar

Importantes:
- Arreglar asignaciones cuando se intenta ejecutar directo el archivo rpll.

Futuros:
- Arreglar espaciado de tabulacion (Actualmente solo acepta 4)
- Hacer que se puedan hacer fors adentro de fors.
- Cuando se ejecuta con carpetas internas no funciona.

## Bug 1: Asignaciones a funciones con parametros no devuelven lo que deberian

```
res = suma ?num ?num2
factorial res
```

`res` si ingreso 1 y 1 deberia ser 2, y es 13. Pero si hago lo siguiente

```
res = suma 1 1
facotorial res
```

Entonces funciona correctamente.