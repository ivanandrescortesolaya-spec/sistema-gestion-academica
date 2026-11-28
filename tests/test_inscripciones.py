
import unittest
from datetime import date

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

    # Pruebas originales

    def test_registrar_inscripcion(self):
        resultado = self.gestion.registrar(self.inscripcion)
        self.assertTrue(resultado)

    def test_buscar_por_codigo(self):
        self.gestion.registrar(self.inscripcion)
        resultado = self.gestion.buscar_por_codigo("I001")

        assert resultado is not None

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

    # Nuevas pruebas de validacion

    def test_inscripcion_duplicada_aprendiz_curso(self):
        self.gestion.registrar(self.inscripcion)

        duplicada = Inscripcion(
            "I002",
            self.aprendiz,
            self.curso
        )

        with self.assertRaises(ValueError):
            self.gestion.registrar(duplicada)

        self.assertEqual(len(self.gestion.listar()), 1)

    def test_aprendiz_en_varios_cursos(self):
        segundo_curso = Curso(
            "C002",
            "Bases de datos",
            "Fundamentos de SQL",
            100,
            "complementaria"
        )

        segunda_inscripcion = Inscripcion(
            "I002",
            self.aprendiz,
            segundo_curso
        )

        self.gestion.registrar(self.inscripcion)
        self.gestion.registrar(segunda_inscripcion)

        resultado = self.gestion.buscar_por_aprendiz(123456)
        self.assertEqual(len(resultado), 2)

    def test_curso_con_varios_aprendices(self):
        segundo_aprendiz = Aprendiz(
            "Maria",
            654321,
            22,
            "3101234567",
            "maria@gmail.com",
            "Neiva"
        )

        segunda_inscripcion = Inscripcion(
            "I002",
            segundo_aprendiz,
            self.curso
        )

        self.gestion.registrar(self.inscripcion)
        self.gestion.registrar(segunda_inscripcion)

        resultado = self.gestion.buscar_por_curso("C001")
        self.assertEqual(len(resultado), 2)

    def test_fecha_inscripcion(self):
        self.assertEqual(
            self.inscripcion.fecha_inscripcion,
            date.today()
        )

    def test_estado_inicial(self):
        self.assertEqual(self.inscripcion.estado, "Activa")

    def test_codigo_vacio(self):
        with self.assertRaises(ValueError):
            Inscripcion("", self.aprendiz, self.curso)

    def test_codigo_con_espacios(self):
        with self.assertRaises(ValueError):
            Inscripcion("   ", self.aprendiz, self.curso)

    def test_codigo_tipo_invalido(self):
        with self.assertRaises(ValueError):
            Inscripcion(123, self.aprendiz, self.curso) # pyright: ignore[reportArgumentType]

    def test_aprendiz_invalido(self):
        with self.assertRaises(ValueError):
            Inscripcion("I002", None, self.curso) # pyright: ignore[reportArgumentType]

    def test_curso_invalido(self):
        with self.assertRaises(ValueError):
            Inscripcion("I002", self.aprendiz, None) # pyright: ignore[reportArgumentType]

    def test_proteger_estado(self):
        with self.assertRaises(AttributeError):
            setattr(self.inscripcion, "estado", "Invalido")

    def test_proteger_fecha_inscripcion(self):
        with self.assertRaises(AttributeError):
            setattr(
                self.inscripcion,
                "fecha_inscripcion",
                date(2000, 1, 1)
            )


if __name__ == "__main__":
    unittest.main()
