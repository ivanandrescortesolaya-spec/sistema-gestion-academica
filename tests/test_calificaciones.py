import unittest

from personas.aprendices import Aprendiz
from cursos.curso import Curso
from inscripciones.inscripcion import Inscripcion
from calificaciones.calificacion import Calificacion
from calificaciones.gestion_calificaciones import GestionCalificaciones


class TestGestionCalificaciones(unittest.TestCase):

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

        self.calificacion = Calificacion(
            "N001",
            self.inscripcion,
            85
        )

        self.gestion = GestionCalificaciones()

    def test_registrar_calificacion(self):
        resultado = self.gestion.registrar(self.calificacion)
        self.assertTrue(resultado)

    def test_buscar_por_codigo(self):
        self.gestion.registrar(self.calificacion)

        resultado = self.gestion.buscar_por_codigo("N001")

        self.assertEqual(resultado.codigo, "N001")

    def test_no_registrar_codigo_duplicado(self):
        self.gestion.registrar(self.calificacion)

        with self.assertRaises(ValueError):
            self.gestion.registrar(self.calificacion)

    def test_listar_calificaciones(self):
        self.gestion.registrar(self.calificacion)

        resultado = self.gestion.listar()

        self.assertEqual(len(resultado), 1)

    def test_buscar_por_aprendiz(self):
        self.gestion.registrar(self.calificacion)

        resultado = self.gestion.buscar_por_aprendiz(123456)

        self.assertEqual(len(resultado), 1)

    def test_buscar_por_curso(self):
        self.gestion.registrar(self.calificacion)

        resultado = self.gestion.buscar_por_curso("C001")

        self.assertEqual(len(resultado), 1)

    def test_rechazar_nota_mayor_a_100(self):
        with self.assertRaises(ValueError):
            Calificacion("N002", self.inscripcion, 120)

    def test_rechazar_nota_menor_a_0(self):
        with self.assertRaises(ValueError):
            Calificacion("N003", self.inscripcion, -10)


if __name__ == "__main__":
    unittest.main()
