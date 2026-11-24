
import unittest

from cursos.curso import Curso
from cursos.gestion_cursos import GestionCursos
from personas.profesores import Profesor


class TestCursos(unittest.TestCase):

    def setUp(self):
        self.gestion = GestionCursos()

        self.profesor = Profesor(
            "Carlos Pérez",
            123456,
            35,
            "Ingeniero",
            101,
            "Programación"
        )

        self.curso = Curso(
            "CUR001",
            "Programación Python",
            "Fundamentos de programación",
            120,
            "titulada"
        )

    def test_registrar_curso(self):
        self.assertTrue(self.gestion.registrar(self.curso))
        self.assertEqual(len(self.gestion.listar()), 1)

    def test_buscar_curso(self):
        self.gestion.registrar(self.curso)

        resultado = self.gestion.buscar_por_codigo("CUR001")

        self.assertEqual(resultado, self.curso)

    def test_buscar_curso_inexistente(self):
        self.assertIsNone(
            self.gestion.buscar_por_codigo("CUR999")
        )

    def test_listar_cursos(self):
        self.gestion.registrar(self.curso)

        curso2 = Curso(
            "CUR002",
            "Bases de datos",
            "Fundamentos de SQL",
            80,
            "complementaria"
        )

        self.gestion.registrar(curso2)

        self.assertEqual(len(self.gestion.listar()), 2)

    def test_listar_sin_cursos(self):
        self.assertEqual(self.gestion.listar(), [])

    def test_codigo_duplicado(self):
        self.gestion.registrar(self.curso)

        curso2 = Curso(
            "CUR001",
            "Bases de datos",
            "Fundamentos de SQL",
            80,
            "complementaria"
        )

        with self.assertRaises(ValueError):
            self.gestion.registrar(curso2)

        self.assertEqual(len(self.gestion.listar()), 1)

    def test_codigo_vacio(self):
        with self.assertRaises(ValueError):
            self.curso.codigo = ""

    def test_nombre_vacio(self):
        with self.assertRaises(ValueError):
            self.curso.nombre = ""

    def test_descripcion_vacia(self):
        with self.assertRaises(ValueError):
            self.curso.descripcion = ""

    def test_duracion_negativa(self):
        with self.assertRaises(ValueError):
            self.curso.duracion_horas = -10

    def test_duracion_cero(self):
        with self.assertRaises(ValueError):
            self.curso.duracion_horas = 0

    def test_modalidad_invalida(self):
        with self.assertRaises(ValueError):
            self.curso.modalidad = "virtual"

    def test_modalidad_titulada(self):
        self.assertEqual(self.curso.modalidad, "titulada")

    def test_modalidad_complementaria(self):
        self.curso.modalidad = "complementaria"

        self.assertEqual(
            self.curso.modalidad,
            "complementaria"
        )

    def test_curso_sin_profesor(self):
        self.assertIsNone(self.curso.profesor)

    def test_asignar_profesor(self):
        self.gestion.registrar(self.curso)

        self.assertTrue(
            self.gestion.asignar_profesor(
                "CUR001", self.profesor
            )
        )

        self.assertEqual(
            self.curso.profesor,
            self.profesor
        )

    def test_asignar_profesor_curso_inexistente(self):
        with self.assertRaises(ValueError):
            self.gestion.asignar_profesor(
                "CUR999", self.profesor
            )

    def test_buscar_por_profesor(self):
        self.gestion.registrar(self.curso)

        self.gestion.asignar_profesor(
            "CUR001", self.profesor
        )

        resultado = self.gestion.buscar_por_profesor(123456)

        self.assertEqual(resultado, [self.curso])

    def test_buscar_profesor_sin_cursos(self):
        self.gestion.registrar(self.curso)

        resultado = self.gestion.buscar_por_profesor(999999)

        self.assertEqual(resultado, [])

    def test_mostrar_informacion(self):
        self.curso.asignar_profesor(self.profesor)

        informacion = self.curso.mostrar_informacion()

        self.assertIn("CUR001", informacion)
        self.assertIn("Programación Python", informacion)
        self.assertIn("120 horas", informacion)
        self.assertIn("Carlos Pérez", informacion)


if __name__ == "__main__":
    unittest.main()
