
import unittest

from personas.profesores import Profesor
from personas.gestion_profesores import Gestion_profesores


class TestProfesores(unittest.TestCase):

    def setUp(self):
        self.gestion = Gestion_profesores()

        self.profesor = Profesor(
            "Carlos Pérez",
            123456,
            35,
            "Ingeniero",
            101,
            "Programación"
        )

    def test_registrar_profesor(self):
        self.gestion.registrar(self.profesor)
        self.assertEqual(len(self.gestion.listar()), 1)

    def test_buscar_profesor(self):
        self.gestion.registrar(self.profesor)

        resultado = self.gestion.buscar_por_documento(123456)

        self.assertEqual(resultado, self.profesor)

    def test_buscar_profesor_inexistente(self):
        resultado = self.gestion.buscar_por_documento(999999)

        self.assertIsNone(resultado)

    def test_listar_profesores(self):
        self.gestion.registrar(self.profesor)

        profesor2 = Profesor(
            "Ana López", 654321, 30,
            "Ingeniera", 102, "Bases de datos"
        )

        self.gestion.registrar(profesor2)

        self.assertEqual(len(self.gestion.listar()), 2)

    def test_documento_duplicado(self):
        self.gestion.registrar(self.profesor)

        with self.assertRaises(ValueError):
            self.gestion.registrar(self.profesor)

    def test_nombre_vacio(self):
        with self.assertRaises(ValueError):
            Profesor(
                "", 123456, 35,
                "Ingeniero", 101, "Programación"
            )

    def test_edad_invalida(self):
        with self.assertRaises(ValueError):
            Profesor(
                "Carlos", 123456, -5,
                "Ingeniero", 101, "Programación"
            )

    def test_profesion_vacia(self):
        with self.assertRaises(ValueError):
            Profesor(
                "Carlos", 123456, 35,
                "", 101, "Programación"
            )


if __name__ == "__main__":
    unittest.main()
