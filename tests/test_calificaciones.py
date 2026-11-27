
import unittest
from datetime import date

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
            4.5
        )

        self.gestion = GestionCalificaciones()

    # Pruebas originales corregidas

    def test_registrar_calificacion(self):
        resultado = self.gestion.registrar(self.calificacion)
        self.assertTrue(resultado)

    def test_buscar_por_codigo(self):
        self.gestion.registrar(self.calificacion)
        resultado = self.gestion.buscar_por_codigo("N001")

        assert resultado is not None

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

    def test_rechazar_nota_mayor_a_5(self):
        with self.assertRaises(ValueError):
            Calificacion("N002", self.inscripcion, 5.1)

    def test_rechazar_nota_menor_a_0(self):
        with self.assertRaises(ValueError):
            Calificacion("N003", self.inscripcion, -0.1)

    # Nuevas pruebas de validacion

    def test_aceptar_nota_minima(self):
        calificacion = Calificacion(
            "N002", self.inscripcion, 0.0
        )
        self.assertEqual(calificacion.nota, 0.0)

    def test_aceptar_nota_maxima(self):
        calificacion = Calificacion(
            "N002", self.inscripcion, 5.0
        )
        self.assertEqual(calificacion.nota, 5.0)

    def test_rechazar_nota_texto(self):
        with self.assertRaises(ValueError):
            Calificacion("N002", self.inscripcion, "4.5")  # pyright: ignore[reportArgumentType]

    def test_rechazar_nota_booleana(self):
        with self.assertRaises(ValueError):
            Calificacion("N002", self.inscripcion, True)

    def test_codigo_vacio(self):
        with self.assertRaises(ValueError):
            Calificacion("", self.inscripcion, 4.0)

    def test_inscripcion_invalida(self):
        with self.assertRaises(ValueError):
            Calificacion("N002", None, 4.0)  # pyright: ignore[reportArgumentType]

    def test_fecha_calificacion(self):
        self.assertEqual(
            self.calificacion.fecha,
            date.today()
        )

    def test_proteger_fecha(self):
        with self.assertRaises(AttributeError):
            setattr(
                self.calificacion,
                "fecha",
                date(2000, 1, 1)
            )


if __name__ == "__main__":
    unittest.main()
