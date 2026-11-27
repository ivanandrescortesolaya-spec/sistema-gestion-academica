import unittest

from personas.aprendices import Aprendiz
from cursos.curso import Curso
from inscripciones.inscripcion import Inscripcion
from inscripciones.gestion_inscripciones import GestionInscripciones


class TestGestionInscripciones(unittest.TestCase):

    def setUp(self):
        self.aprendiz = Aprendiz(
            "Carlos",
            123456,
            20,
            "3001234567",
            "carlos@gmail.com",
            "Neiva"
        )

        self.curso = Curso(
            "C001",
            "Programacion",
            "Desarrollo de software",
            400,
            "titulada"
        )

        self.inscripcion = Inscripcion(
            "I001",
            self.aprendiz,
            self.curso
        )

        self.gestion = GestionInscripciones()

    def test_registrar_inscripcion(self):
        resultado = self.gestion.registrar(self.inscripcion)
        self.assertTrue(resultado)

    def test_buscar_por_codigo(self):
        self.gestion.registrar(self.inscripcion)

        resultado = self.gestion.buscar_por_codigo("I001")

        self.assertEqual(resultado.codigo, "I001")

    def test_no_registrar_codigo_duplicado(self):
        self.gestion.registrar(self.inscripcion)

        with self.assertRaises(ValueError):
            self.gestion.registrar(self.inscripcion)

    def test_listar_inscripciones(self):
        self.gestion.registrar(self.inscripcion)

        resultado = self.gestion.listar()

        self.assertEqual(len(resultado), 1)

    def test_buscar_por_aprendiz(self):
        self.gestion.registrar(self.inscripcion)

        resultado = self.gestion.buscar_por_aprendiz(123456)

        self.assertEqual(len(resultado), 1)

    def test_buscar_por_curso(self):
        self.gestion.registrar(self.inscripcion)

        resultado = self.gestion.buscar_por_curso("C001")

        self.assertEqual(len(resultado), 1)

    def test_cancelar_inscripcion(self):
        self.inscripcion.cancelar()

        self.assertEqual(self.inscripcion.estado, "Cancelada")

    def test_finalizar_inscripcion(self):
        self.inscripcion.finalizar()

        self.assertEqual(self.inscripcion.estado, "Finalizada")


if __name__ == "__main__":
    unittest.main()
