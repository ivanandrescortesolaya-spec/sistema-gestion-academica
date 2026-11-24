
import unittest

from personas.aprendices import Aprendiz
from personas.gestion_aprendices import Gestion_aprendices


class TestAprendices(unittest.TestCase):

    def setUp(self):
        self.gestion = Gestion_aprendices()

        self.aprendiz = Aprendiz(
            "Juan Pérez",
            123456,
            20,
            "3001234567",
            "juan@gmail.com",
            "Calle 10"
        )

    def test_registrar_aprendiz(self):
        self.assertTrue(self.gestion.registrar(self.aprendiz))
        self.assertEqual(len(self.gestion.listar()), 1)

    def test_buscar_aprendiz(self):
        self.gestion.registrar(self.aprendiz)

        resultado = self.gestion.buscar_documento(123456)

        self.assertEqual(resultado, self.aprendiz)

    def test_buscar_aprendiz_inexistente(self):
        self.assertIsNone(
            self.gestion.buscar_documento(999999)
        )

    def test_listar_aprendices(self):
        self.gestion.registrar(self.aprendiz)

        aprendiz2 = Aprendiz(
            "Ana López",
            654321,
            22,
            "3101234567",
            "ana@gmail.com",
            "Calle 20"
        )

        self.gestion.registrar(aprendiz2)

        self.assertEqual(len(self.gestion.listar()), 2)

    def test_listar_sin_aprendices(self):
        self.assertEqual(self.gestion.listar(), [])

    def test_documento_duplicado(self):
        self.gestion.registrar(self.aprendiz)

        with self.assertRaises(ValueError):
            self.gestion.registrar(self.aprendiz)

        self.assertEqual(len(self.gestion.listar()), 1)

    def test_telefono_invalido(self):
        with self.assertRaises(ValueError):
            self.aprendiz.telefono = "abcdef"

    def test_telefono_vacio(self):
        with self.assertRaises(ValueError):
            self.aprendiz.telefono = ""

    def test_correo_invalido(self):
        with self.assertRaises(ValueError):
            self.aprendiz.correo = "correo_invalido"

    def test_direccion_vacia(self):
        with self.assertRaises(ValueError):
            self.aprendiz.direccion = ""

    def test_obtener_rol(self):
        self.assertEqual(
            self.aprendiz.obtener_rol(),
            "Aprendiz"
        )

    def test_mostrar_informacion(self):
        informacion = self.aprendiz.mostrar_informacion()

        self.assertIn("Juan Pérez", informacion)
        self.assertIn("3001234567", informacion)
        self.assertIn("juan@gmail.com", informacion)


if __name__ == "__main__":
    unittest.main()
