# Tarea 2: Entrega causal y asignación de perfiles

## Ejecutar

Los comandos utilizados fueron:

```bash
python check_contract.py
python run_cases.py
python -m unittest -v
```

## Resultado y decisión

Los límites establecidos son cambiar el owner de como máximo 3 claves y mantener una carga máxima de 16.

En la muestra inicial, después de añadir D, el método `modulo` cambia el owner de 4 claves y alcanza una carga máxima de 11. Por lo tanto, no cumple el límite de claves movidas.

El método `ring` cambia el owner de 2 claves y alcanza una carga máxima de 9. Por lo tanto, es el único método que cumple simultáneamente ambos límites en la muestra inicial.

Cuando la frecuencia de la clave 10 aumenta de 8 a 20, `modulo` continúa cambiando 4 claves y su carga máxima aumenta a 23. `ring` continúa cambiando solamente 2 claves, pero su carga máxima aumenta a 21. Por lo tanto, con la clave 10 más solicitada ninguno de los dos métodos cumple simultáneamente los dos límites.

Después de añadir D, `modulo` requiere 8 saltos de consulta en total, mientras que `ring` requiere 17. En `modulo`, el cliente calcula directamente el propietario y cada una de las 8 claves requiere un salto. En `ring`, cada consulta comienza en el nodo de menor posición y puede requerir avances adicionales hasta llegar al propietario. Los saltos se cuentan una vez por clave y no se multiplican por su frecuencia.

## Límite

Calcular el nuevo owner de una clave únicamente determina qué nodo debería ser responsable del perfil según la regla de asignación. Esto no demuestra que el perfil haya sido transferido físicamente al nuevo nodo.

La implementación no realiza migración de perfiles, transferencia de datos, persistencia ni coordinación entre nodos. Por lo tanto, un cambio de owner representa una nueva asignación calculada, no evidencia de que los datos ya se hayan movido.