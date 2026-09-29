"""Completa las cuatro funciones. Usa Python 3.11+ sin paquetes externos."""

def tick(lamport, vector, process, incoming=None):
    """Devuelve (nuevo_lamport, nuevo_vector) sin modificar los argumentos.
    process es el índice 0..2. incoming es None o (lamport_remoto, vector_remoto).
    Evento local o envío: suma 1 a Lamport y al componente local del vector.
    Recepción: toma el máximo local/remoto de Lamport y de cada componente
    vectorial; después suma 1 a Lamport y al componente local del vector.
    """
    new_vector = list(vector)

    if incoming is None:
        new_lamport = lamport + 1
        new_vector[process] += 1
    else:
        remote_lamport, remote_vector = incoming

        new_lamport = max(lamport, remote_lamport) + 1

        new_vector = [
            max(local, remote)
            for local, remote in zip(vector, remote_vector)
        ]

        new_vector[process] += 1

    return new_lamport, new_vector


class CausalInbox:
    def __init__(self):
        self.seen = set()
        self.delivered = [0, 0, 0]
        self.buffer = []

    def receive(self, message):
        """Acepta la primera copia y devuelve los id entregados en esta llamada.
        message={id,sender,seq,deps}; sender=0..2 y seq empieza en 0.
        Un id repetido no cambia el estado.
        Listo: seq==delivered[sender] y cada deps[p]<=delivered[p].
        Al entregar, incrementa delivered[sender]. Revisa el buffer de nuevo,
        desde la entrada más antigua, hasta que no haya más mensajes listos.
        """
        message_id = message["id"]

        # Una copia repetida no cambia ningún estado.
        if message_id in self.seen:
            return []

        # Aceptamos solamente la primera copia.
        self.seen.add(message_id)
        self.buffer.append(message)

        delivered_now = []

        # Seguimos recorriendo el buffer mientras alguna entrega sea posible.
        while True:
            delivered_one = False

            # Se revisa desde el mensaje que llegó primero.
            for i, buffered_message in enumerate(self.buffer):
                sender = buffered_message["sender"]
                seq = buffered_message["seq"]
                deps = buffered_message["deps"]

                correct_sequence = (
                    seq == self.delivered[sender]
                )

                dependencies_satisfied = all(
                    deps[p] <= self.delivered[p]
                    for p in range(len(self.delivered))
                )

                if correct_sequence and dependencies_satisfied:
                    delivered_message = self.buffer.pop(i)

                    self.delivered[sender] += 1
                    delivered_now.append(delivered_message["id"])

                    # Como cambió delivered, debemos volver a revisar
                    # desde el inicio del buffer.
                    delivered_one = True
                    break

            if not delivered_one:
                break

        return delivered_now


def owner(key, nodes, mode):
    """nodes es {nombre:posición}; key y posiciones están en 0..15.
    mode='modulo': usa el orden de inserción y key % len(nodes).
    mode='ring': primer nodo con posición >= key; si no hay, usa la menor posición.
    Rechaza un ring vacío. No modifica nodes.
    """
    if not nodes:
        raise ValueError("nodes no puede estar vacío")

    if mode == "modulo":
        node_names = list(nodes.keys())
        return node_names[key % len(node_names)]

    if mode == "ring":
        ordered_nodes = sorted(nodes.items(), key=lambda item: item[1])

        for name, position in ordered_nodes:
            if position >= key:
                return name

        # Retorno circular al nodo de menor posición.
        return ordered_nodes[0][0]

    raise ValueError(f"Modo desconocido: {mode}")


def compare(keys, frequencies, before, after, mode):
    """Devuelve los campos descritos en EVIDENCE-PACKET.md.
    Usa owner para asignar claves; no fijes resultados de CASES.json en el código.
    """
    owners_before = {
        key: owner(key, before, mode)
        for key in keys
    }

    owners_after = {
        key: owner(key, after, mode)
        for key in keys
    }

    # Debe conservar el orden original de keys.
    moved = [
        key
        for key in keys
        if owners_before[key] != owners_after[key]
    ]

    # Incluimos incluso nodos con carga cero.
    load_before = {
        node: 0
        for node in before
    }

    load_after = {
        node: 0
        for node in after
    }

    for key in keys:
        frequency = frequencies[key]

        load_before[owners_before[key]] += frequency
        load_after[owners_after[key]] += frequency

    # Los saltos se calculan una vez por clave, no por frecuencia.
    if mode == "modulo":
        hops = len(keys)

    elif mode == "ring":
        ordered_nodes = sorted(after.items(), key=lambda item: item[1])
        entry_node = ordered_nodes[0][0]

        hops = 0

        for key in keys:
            key_owner = owners_after[key]

            # Cliente -> nodo de menor posición.
            key_hops = 1

            if key_owner != entry_node:
                owner_index = next(
                    i
                    for i, (name, _) in enumerate(ordered_nodes)
                    if name == key_owner
                )

                # Cada avance por el ring suma un salto.
                key_hops += owner_index

            hops += key_hops

    else:
        raise ValueError(f"Modo desconocido: {mode}")

    return {
        "before": owners_before,
        "after": owners_after,
        "moved": moved,
        "load_before": load_before,
        "load_after": load_after,
        "hops": hops,
    }