# Datos y contratos de Tarea 2

`CASES.json` contiene entradas, no respuestas. `run_cases.py` las procesa con
tu código e imprime los resultados. No necesitas editarlo ni copiar su salida.

## Relojes

En `CASES.json`, los eventos `c*`, `a*` y `b*` ocurren en C, A y B,
respectivamente. Sus índices son 0, 1 y 2. En un evento local o envío,
incrementa el reloj Lamport y el componente propio del vector. Al recibir,
el nuevo Lamport es `max(local, remoto) + 1`: primero toma el máximo de cada
componente vectorial y después incrementa el componente del receptor. La
firma de `tick` indica cómo se recibe el estado remoto.

La lista respeta el orden de cada proceso y de envío/recepción. No establece
un orden total entre procesos. `received` indica el evento que envió el
mensaje, o `null` si no hubo recepción. Las siguientes medidas son solo
ejemplos para interpretar la historia: no son campos de `CASES.json` ni debes
calcularlas. Aunque la hora de pared marque `c3=10:00:00.020` y
`b1=09:59:59.900`, el mensaje establece `c3→b1`. La duración monotónica de
`c1→c6` dentro de C es 160 ms; no restes relojes de máquinas distintas.

## Admisión y entrega

`id` identifica el mensaje: todas sus copias tienen el mismo `id`. `sender`
es 0, 1 o 2; `seq` empieza en 0 para cada emisor. Acepta solo la primera
copia. Si llega otra con el mismo `id`, no cambies `seen` ni `delivered`.
Las llegadas ya están dadas; no implementes reenvíos ni fiabilidad de red.

El vector de `tick` y el contador `delivered` pertenecen a entradas distintas.
`delivered[p]` cuenta los mensajes ya entregados del proceso `p`. `deps[p]`
indica cuántos mensajes de `p` deben haberse entregado antes de este.
Entrega un mensaje solo si `seq == delivered[sender]` y, para todo `p`,
`deps[p] <= delivered[p]`. Después incrementa `delivered[sender]`.

Revisa el buffer hasta que no haya más mensajes listos. En cada recorrido,
empieza por el que llegó primero. Si dos mensajes independientes están listos,
este orden solo resuelve el empate: no crea una relación causal. Si falta una
dependencia, deja el mensaje en el buffer.

## Asignación y medida

`frequencies[i]` es el número de solicitudes para `keys[i]`. Las claves
enteras ya son los valores de hash, entre 0 y 15: no calcules otro hash.
En modo `modulo`, usa el orden de inserción de los nodos y
`key % número_de_nodos`. En modo `ring`, el owner es el primer nodo cuya
posición es `>= key`; si no existe, vuelve al nodo de menor posición.

`compare` recibe `frequencies` como diccionario clave→solicitudes y devuelve:

- `before` y `after`: diccionarios clave→owner;
- `moved`: claves cuyo owner cambia, en el orden de `keys`;
- `load_before` y `load_after`: solicitudes por nodo, incluidos los nodos con cero;
- `hops`: saltos totales de la **petición de consulta**, una vez por clave,
  después del cambio. No cuenta la respuesta del propietario al cliente.

En `modulo`, el cliente calcula el owner y le envía la consulta directamente:
un salto por clave. En `ring`, el cliente no tiene el mapa: envía la consulta
al nodo de menor posición (A en la muestra), lo que cuesta un salto. Cada
avance al siguiente nodo suma otro. Si el owner es A, la consulta termina allí
en un salto, incluso si A es el sucesor por retorno circular. No multipliques los saltos
por la frecuencia: esta solo sirve para calcular la carga.

Compara la asignación antes y después de añadir D. El método elegido debe
cambiar el owner de a lo sumo tres claves y dejar una carga máxima de 16. Después cambia
solo `f(10)` a 20 y compara otra vez. Cada clave representa un perfil:
`compare` calcula su nuevo owner, pero no mueve el perfil ni coordina cambios
entre nodos.
