
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

    # Pruebas originales

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

    # Pruebas de validacion y encapsulamiento

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

    # Pruebas de modificacion de calificaciones

    def test_modificar_calificacion(self):
        self.gestion.registrar(self.calificacion)

        resultado = self.gestion.modificar_calificacion(
            "N001", 3.8
        )

        self.assertTrue(resultado)
        self.assertEqual(self.calificacion.nota, 3.8)

    def test_modificar_calificacion_inexistente(self):
        with self.assertRaises(ValueError):
            self.gestion.modificar_calificacion("N999", 4.0)

    def test_modificar_nota_invalida(self):
        self.gestion.registrar(self.calificacion)

        with self.assertRaises(ValueError):
            self.gestion.modificar_calificacion("N001", 6.0)

        self.assertEqual(self.calificacion.nota, 4.5)

    # Pruebas de busqueda por inscripcion

    def test_buscar_por_inscripcion(self):
        self.gestion.registrar(self.calificacion)

        resultado = self.gestion.buscar_por_inscripcion("I001")

        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0].codigo, "N001")

    def test_buscar_inscripcion_sin_calificaciones(self):
        resultado = self.gestion.buscar_por_inscripcion("I999")

        self.assertEqual(resultado, [])

    # Pruebas de promedios

    def test_calcular_promedio(self):
        self.gestion.registrar(self.calificacion)

        self.gestion.registrar(
            Calificacion("N002", self.inscripcion, 3.5)
        )

        self.gestion.registrar(
            Calificacion("N003", self.inscripcion, 4.0)
        )

        promedio = self.gestion.calcular_promedio("I001")

        self.assertAlmostEqual(promedio, 4.0, places=2)

    def test_promedio_con_menos_de_tres_notas(self):
        self.gestion.registrar(self.calificacion)

        with self.assertRaises(ValueError):
            self.gestion.calcular_promedio("I001")

    # Pruebas de estados academicos

    def test_estado_aprobado(self):
        for codigo in ["N001", "N002", "N003"]:
            self.gestion.registrar(
                Calificacion(codigo, self.inscripcion, 4.0)
            )

        estado = self.gestion.obtener_estado_academico("I001")

        self.assertEqual(estado, "Aprobado")

    def test_estado_reprobado(self):
        for codigo in ["N001", "N002", "N003"]:
            self.gestion.registrar(
                Calificacion(codigo, self.inscripcion, 2.5)
            )

        estado = self.gestion.obtener_estado_academico("I001")

        self.assertEqual(estado, "Reprobado")

    def test_aprobacion_con_nota_minima(self):
        for codigo in ["N001", "N002", "N003"]:
            self.gestion.registrar(
                Calificacion(codigo, self.inscripcion, 3.0)
            )

        estado = self.gestion.obtener_estado_academico("I001")

        self.assertEqual(estado, "Aprobado")

    # Pruebas de rendimiento academico

    def test_rendimiento_pendiente(self):
        self.gestion.registrar(self.calificacion)

        resultado = self.gestion.consultar_rendimiento("I001")

        self.assertEqual(resultado["estado"], "Pendiente")
        self.assertIsNone(resultado["promedio"])

    def test_rendimiento_completo(self):
        self.gestion.registrar(self.calificacion)

        self.gestion.registrar(
            Calificacion("N002", self.inscripcion, 4.0)
        )

        self.gestion.registrar(
            Calificacion("N003", self.inscripcion, 4.0)
        )

        resultado = self.gestion.consultar_rendimiento("I001")

        self.assertEqual(resultado["aprendiz"], "Carlos")
        self.assertEqual(resultado["curso"], "Programacion")
        self.assertEqual(resultado["promedio"], 4.17)
        self.assertEqual(resultado["estado"], "Aprobado")
        self.assertEqual(len(resultado["notas"]), 3)

    def test_rendimiento_sin_calificaciones(self):
        with self.assertRaises(ValueError):
            self.gestion.consultar_rendimiento("I001")

    def test_promedio_independiente_por_inscripcion(self):
        otro_curso = Curso(
            "C002",
            "Bases de datos",
            "Fundamentos de SQL",
            100,
            "complementaria"
        )

        otra_inscripcion = Inscripcion(
            "I002",
            self.aprendiz,
            otro_curso
        )

        for codigo in ["N001", "N002", "N003"]:
            self.gestion.registrar(
                Calificacion(codigo, self.inscripcion, 4.0)
            )

        self.gestion.registrar(
            Calificacion("N004", otra_inscripcion, 1.0)
        )

        promedio = self.gestion.calcular_promedio("I001")

        self.assertEqual(promedio, 4.0)

    def test_registrar_mas_de_tres_calificaciones(self):
        for codigo in ["N001", "N002", "N003", "N004"]:
            self.gestion.registrar(
                Calificacion(codigo, self.inscripcion, 4.0)
            )

        resultado = self.gestion.buscar_por_inscripcion("I001")

        self.assertEqual(len(resultado), 4)
        self.assertEqual(
            self.gestion.calcular_promedio("I001"),
            4.0
        )


if __name__ == "__main__":
    unittest.main()
