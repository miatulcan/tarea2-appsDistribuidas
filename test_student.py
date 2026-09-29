"""Sustituye el ejemplo por tus pruebas; ejecuta python3 -m unittest -v."""
import unittest
import analysis

class MyTests(unittest.TestCase):
    def test_example_local_event(self):
        self.assertEqual(analysis.tick(0,[0,0,0],2),(1,[0,0,1]))

# Añade casos propios de reloj, entrega y asignación con resultados calculados
# independientemente. No copies la función evaluada para obtener el esperado.
