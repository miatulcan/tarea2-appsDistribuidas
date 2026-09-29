import unittest
import analysis


class MyTests(unittest.TestCase):

    def test_recepcion_fusiona_vector_antes_de_incrementar(self):
        # Proceso 1 recibe un vector cuyo componente 1 es mayor que el local.
        # Primero debe fusionar:
        # max([1,4,0], [3,10,2]) = [3,10,2]
        # y solo después incrementar el componente del receptor:
        # [3,11,2]
        result = analysis.tick(
            5,
            [1, 4, 0],
            1,
            (12, [3, 10, 2])
        )

        self.assertEqual(result, (13, [3, 11, 2]))

    def test_entrega_espera_dependencia_y_no_repite(self):
        inbox = analysis.CausalInbox()

        # Este mensaje del proceso 2 depende de que ya se haya
        # entregado un mensaje del proceso 1.
        waiting = {
            "id": "espera",
            "sender": 2,
            "seq": 0,
            "deps": [0, 1, 0]
        }

        dependency = {
            "id": "base",
            "sender": 1,
            "seq": 0,
            "deps": [0, 0, 0]
        }

        # Todavía falta la dependencia: no se puede entregar.
        self.assertEqual(inbox.receive(waiting), [])
        self.assertEqual(inbox.delivered, [0, 0, 0])

        # Al llegar la dependencia, se entrega primero "base".
        # Después se vuelve a revisar el buffer y ya se puede
        # entregar "espera".
        self.assertEqual(
            inbox.receive(dependency),
            ["base", "espera"]
        )
        self.assertEqual(inbox.delivered, [0, 1, 1])

        # Una copia repetida no debe entregarse de nuevo ni
        # modificar el contador.
        self.assertEqual(inbox.receive(waiting), [])
        self.assertEqual(inbox.delivered, [0, 1, 1])

    def test_carga_incluye_frecuencia_de_clave_solicitada(self):
        keys = [3, 5, 11]
        frequencies = {
            3: 2,
            5: 17,
            11: 1
        }

        before = {
            "X": 1,
            "Y": 6
        }

        after = {
            "X": 1,
            "Y": 6,
            "Z": 12
        }

        result = analysis.compare(
            keys,
            frequencies,
            before,
            after,
            "ring"
        )

        # Después del cambio:
        # 3 -> Y  (2 solicitudes)
        # 5 -> Y  (17 solicitudes)
        # 11 -> Z (1 solicitud)
        #
        # Por tanto:
        # X = 0, Y = 19, Z = 1
        self.assertEqual(
            result["load_after"],
            {"X": 0, "Y": 19, "Z": 1}
        )


if __name__ == "__main__":
    unittest.main()