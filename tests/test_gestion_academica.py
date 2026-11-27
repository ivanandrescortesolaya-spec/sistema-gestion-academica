import unittest

from gestion_academica import GestionAcademica
from personas.profesores import Profesor
from personas.aprendices import Aprendiz
from cursos.curso import Curso


class TestGestionAcademica(unittest.TestCase):

    def setUp(self):
        self.sistema = GestionAcademica()

        self.profesor = Profesor(
            "Carlos Pérez", 123456, 35,
            "Ingeniero", 101, "Programación"
        )

        self.aprendiz = Aprendiz(
            "Juan Pérez", 654321, 20,
            "3001234567",
            "juan@gmail.com",
            "Calle 10"
        )

        self.curso = Curso(
            "CUR001", "Python",
            "Fundamentos de programación",
            120, "titulada"
        )

    def test_registrar_profesor(self):
        self.assertTrue(
            self.sistema.registrar_profesor(self.profesor)
        )

        self.assertEqual(
            self.sistema.buscar_profesor(123456),
            self.profesor
        )

    def test_registrar_aprendiz(self):
        self.assertTrue(
            self.sistema.registrar_aprendiz(self.aprendiz)
        )

        self.assertEqual(
            self.sistema.buscar_aprendiz(654321),
            self.aprendiz
        )

    def test_registrar_curso(self):
        self.assertTrue(
            self.sistema.registrar_curso(self.curso)
        )

        self.assertEqual(
            self.sistema.buscar_curso("CUR001"),
            self.curso
        )

    def test_asignar_profesor(self):
        self.sistema.registrar_profesor(self.profesor)
        self.sistema.registrar_curso(self.curso)

        self.sistema.asignar_profesor("CUR001", 123456)

        self.assertEqual(
            self.curso.profesor,
            self.profesor
        )

    def test_asignar_profesor_no_registrado(self):
        self.sistema.registrar_curso(self.curso)

        with self.assertRaises(ValueError):
            self.sistema.asignar_profesor("CUR001", 999999)

    def test_asignar_curso_inexistente(self):
        self.sistema.registrar_profesor(self.profesor)

        with self.assertRaises(ValueError):
            self.sistema.asignar_profesor("CUR999", 123456)

    def test_consultar_cursos_profesor(self):
        self.sistema.registrar_profesor(self.profesor)
        self.sistema.registrar_curso(self.curso)

        self.sistema.asignar_profesor("CUR001", 123456)

        self.assertEqual(
            self.sistema.consultar_cursos_profesor(123456),
            [self.curso]
        )

    def test_resumen_vacio(self):
        self.assertEqual(
            self.sistema.obtener_resumen(),
            {
                "profesores": 0,
                "aprendices": 0,
                "cursos": 0,
                "inscripciones": 0,
                "calificaciones": 0
            }
        )

    def test_resumen_academico(self):
        self.sistema.registrar_profesor(self.profesor)
        self.sistema.registrar_aprendiz(self.aprendiz)
        self.sistema.registrar_curso(self.curso)

        self.assertEqual(
            self.sistema.obtener_resumen(),
            {
                "profesores": 1,
                "aprendices": 1,
                "cursos": 1,
                "inscripciones": 0,
                "calificaciones": 0
            }
        )

    def test_profesor_duplicado(self):
        self.sistema.registrar_profesor(self.profesor)

        with self.assertRaises(ValueError):
            self.sistema.registrar_profesor(self.profesor)


if __name__ == "__main__":
    unittest.main()
