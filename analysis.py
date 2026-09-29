"""Completa las cuatro funciones. Usa Python 3.11+ sin paquetes externos."""

def tick(lamport, vector, process, incoming=None):
    """Devuelve (nuevo_lamport, nuevo_vector) sin modificar los argumentos.
    process es el índice 0..2. incoming es None o (lamport_remoto, vector_remoto).
    Evento local o envío: suma 1 a Lamport y al componente local del vector.
    Recepción: toma el máximo local/remoto de Lamport y de cada componente
    vectorial; después suma 1 a Lamport y al componente local del vector.
    """
    raise NotImplementedError("tick")

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
        raise NotImplementedError("receive")

def owner(key, nodes, mode):
    """nodes es {nombre:posición}; key y posiciones están en 0..15.
    mode='modulo': usa el orden de inserción y key % len(nodes).
    mode='ring': primer nodo con posición >= key; si no hay, usa la menor posición.
    Rechaza un ring vacío. No modifica nodes.
    """
    raise NotImplementedError("owner")

def compare(keys, frequencies, before, after, mode):
    """Devuelve los campos descritos en EVIDENCE-PACKET.md.
    Usa owner para asignar claves; no fijes resultados de CASES.json en el código.
    """
    raise NotImplementedError("compare")
