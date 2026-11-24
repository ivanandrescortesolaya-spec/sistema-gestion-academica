
import unittest
from unittest.mock import patch
from io import StringIO

from gestion_academica import GestionAcademica
from main import (
    main,
    mostrar_menu,
    menu_profesores,
    menu_aprendices,
    menu_cursos
)


class TestMain(unittest.TestCase):

    def setUp(self):
        self.sistema = GestionAcademica()

    def test_mostrar_menu(self):
        with patch("sys.stdout", new_callable=StringIO) as salida:
            mostrar_menu()

        self.assertIn(
            "SISTEMA DE GESTIÓN ACADÉMICA",
            salida.getvalue()
        )

    def test_salir_programa(self):
        with patch("builtins.input", side_effect=["0"]):
            with patch("sys.stdout", new_callable=StringIO) as salida:
                main()

        self.assertIn(
            "Gracias por utilizar el sistema",
            salida.getvalue()
        )

    def test_opcion_invalida(self):
        with patch("builtins.input", side_effect=["99", "0"]):
            with patch("sys.stdout", new_callable=StringIO) as salida:
                main()

        self.assertIn("Opción inválida", salida.getvalue())

    def test_registrar_profesor(self):
        datos = [
            "1",
            "Carlos Pérez",
            "123456",
            "35",
            "Ingeniero",
            "101",
            "Programación",
            "0"
        ]

        with patch("builtins.input", side_effect=datos):
            with patch("sys.stdout", new_callable=StringIO):
                menu_profesores(self.sistema)

        self.assertIsNotNone(
            self.sistema.buscar_profesor(123456)
        )

    def test_registrar_aprendiz(self):
        datos = [
            "1",
            "Juan Pérez",
            "654321",
            "20",
            "3101234567",
            "juan@gmail.com",
            "Calle 15",
            "0"
        ]

        with patch("builtins.input", side_effect=datos):
            with patch("sys.stdout", new_callable=StringIO):
                menu_aprendices(self.sistema)

        self.assertIsNotNone(
            self.sistema.buscar_aprendiz(654321)
        )

    def test_registrar_curso(self):
        datos = [
            "1",
            "CUR001",
            "Python",
            "Fundamentos de programación",
            "120",
            "titulada",
            "0"
        ]

        with patch("builtins.input", side_effect=datos):
            with patch("sys.stdout", new_callable=StringIO):
                menu_cursos(self.sistema)

        self.assertIsNotNone(
            self.sistema.buscar_curso("CUR001")
        )

    def test_documento_invalido(self):
        datos = ["2", "abc", "0"]

        with patch("builtins.input", side_effect=datos):
            with patch("sys.stdout", new_callable=StringIO) as salida:
                menu_profesores(self.sistema)

        self.assertIn("Error:", salida.getvalue())

    def test_resumen_academico(self):
        with patch("builtins.input", side_effect=["6", "0"]):
            with patch("sys.stdout", new_callable=StringIO) as salida:
                main()

        resultado = salida.getvalue()

        self.assertIn("Profesores: 0", resultado)
        self.assertIn("Aprendices: 0", resultado)
        self.assertIn("Cursos: 0", resultado)


if __name__ == "__main__":
    unittest.main()
