
import unittest
from typing import Optional

from gestion_academica import GestionAcademica

from personas.profesores import Profesor
from personas.aprendices import Aprendiz
from cursos.curso import Curso
from inscripciones.inscripcion import Inscripcion
from calificaciones.calificacion import Calificacion

from personas.gestion_profesores import (
    IGestionProfesores,
    Gestion_profesores
)

from personas.gestion_aprendices import Gestion_aprendices
from cursos.gestion_cursos import GestionCursos
from inscripciones.gestion_inscripciones import GestionInscripciones
from calificaciones.gestion_calificaciones import GestionCalificaciones

class GestionProfesoresAlternativa:

    def __init__(self):
        self.__profesores: dict[int, Profesor] = {}

    def registrar(self, profesor: Profesor) -> bool:

        if not isinstance(profesor, Profesor):
            raise ValueError(
                "Debes registrar un profesor válido"
            )

        if profesor.documento in self.__profesores:
            raise ValueError(
                "Ya existe un profesor con ese documento"
            )

        self.__profesores[profesor.documento] = profesor
        return True

    def buscar_por_documento(
        self, documento: int
    ) -> Optional[Profesor]:

        return self.__profesores.get(documento)

    def listar(self) -> list[Profesor]:
        return list(self.__profesores.values())


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

    # Metodos auxiliares

    def preparar_inscripcion(self):
        self.sistema.registrar_aprendiz(self.aprendiz)
        self.sistema.registrar_curso(self.curso)
        self.sistema.registrar_inscripcion(self.inscripcion)

    def preparar_calificaciones(self):
        self.preparar_inscripcion()

        self.sistema.registrar_calificacion(
            self.calificacion
        )

        self.sistema.registrar_calificacion(
            Calificacion("N002", self.inscripcion, 3.5)
        )

        self.sistema.registrar_calificacion(
            Calificacion("N003", self.inscripcion, 4.0)
        )

    # Pruebas originales

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

    # Pruebas de integracion de inscripciones

    def test_registrar_inscripcion_valida(self):
        self.sistema.registrar_aprendiz(self.aprendiz)
        self.sistema.registrar_curso(self.curso)

        self.assertTrue(
            self.sistema.registrar_inscripcion(
                self.inscripcion
            )
        )

        self.assertIs(
            self.sistema.buscar_inscripcion("I001"),
            self.inscripcion
        )

    def test_inscripcion_aprendiz_no_registrado(self):
        self.sistema.registrar_curso(self.curso)

        with self.assertRaises(ValueError):
            self.sistema.registrar_inscripcion(
                self.inscripcion
            )

        self.assertEqual(
            self.sistema.listar_inscripciones(), []
        )

    def test_inscripcion_curso_no_registrado(self):
        self.sistema.registrar_aprendiz(self.aprendiz)

        with self.assertRaises(ValueError):
            self.sistema.registrar_inscripcion(
                self.inscripcion
            )

    def test_inscripcion_aprendiz_objeto_distinto(self):
        self.sistema.registrar_aprendiz(self.aprendiz)
        self.sistema.registrar_curso(self.curso)

        otro_aprendiz = Aprendiz(
            "Otro aprendiz", 654321, 22,
            "3101234567",
            "otro@gmail.com",
            "Calle 20"
        )

        inscripcion = Inscripcion(
            "I002",
            otro_aprendiz,
            self.curso
        )

        with self.assertRaises(ValueError):
            self.sistema.registrar_inscripcion(inscripcion)

    def test_inscripcion_curso_objeto_distinto(self):
        self.sistema.registrar_aprendiz(self.aprendiz)
        self.sistema.registrar_curso(self.curso)

        otro_curso = Curso(
            "CUR001",
            "Otro curso",
            "Descripción de prueba",
            80,
            "complementaria"
        )

        inscripcion = Inscripcion(
            "I002",
            self.aprendiz,
            otro_curso
        )

        with self.assertRaises(ValueError):
            self.sistema.registrar_inscripcion(inscripcion)

    def test_inscripcion_duplicada(self):
        self.preparar_inscripcion()

        inscripcion = Inscripcion(
            "I002",
            self.aprendiz,
            self.curso
        )

        with self.assertRaises(ValueError):
            self.sistema.registrar_inscripcion(inscripcion)

    # Pruebas de integracion de calificaciones

    def test_registrar_calificacion_valida(self):
        self.preparar_inscripcion()

        self.assertTrue(
            self.sistema.registrar_calificacion(
                self.calificacion
            )
        )

        self.assertIs(
            self.sistema.buscar_calificacion("N001"),
            self.calificacion
        )

    def test_calificacion_inscripcion_no_registrada(self):
        with self.assertRaises(ValueError):
            self.sistema.registrar_calificacion(
                self.calificacion
            )

        self.assertEqual(
            self.sistema.listar_calificaciones(), []
        )

    def test_calificacion_inscripcion_objeto_distinto(self):
        self.preparar_inscripcion()

        otra_inscripcion = Inscripcion(
            "I001",
            self.aprendiz,
            self.curso
        )

        calificacion = Calificacion(
            "N002",
            otra_inscripcion,
            4.0
        )

        with self.assertRaises(ValueError):
            self.sistema.registrar_calificacion(
                calificacion
            )

    def test_modificar_calificacion(self):
        self.preparar_inscripcion()

        self.sistema.registrar_calificacion(
            self.calificacion
        )

        resultado = self.sistema.modificar_calificacion(
            "N001", 3.8
        )

        self.assertTrue(resultado)
        self.assertEqual(self.calificacion.nota, 3.8)

    def test_consultar_calificaciones_inscripcion(self):
        self.preparar_calificaciones()

        resultado = (
            self.sistema.consultar_calificaciones_inscripcion(
                "I001"
            )
        )

        self.assertEqual(len(resultado), 3)

    def test_calcular_promedio(self):
        self.preparar_calificaciones()

        promedio = self.sistema.calcular_promedio("I001")

        self.assertAlmostEqual(promedio, 4.0, places=2)

    def test_obtener_estado_academico(self):
        self.preparar_calificaciones()

        estado = self.sistema.obtener_estado_academico(
            "I001"
        )

        self.assertEqual(estado, "Aprobado")

    # Pruebas de consultas academicas

    def test_consultar_cursos_aprendiz(self):
        self.preparar_inscripcion()

        resultado = self.sistema.consultar_cursos_aprendiz(
            654321
        )

        self.assertEqual(resultado, [self.curso])

    def test_consultar_aprendices_curso(self):
        self.preparar_inscripcion()

        resultado = self.sistema.consultar_aprendices_curso(
            "CUR001"
        )

        self.assertEqual(resultado, [self.aprendiz])

    def test_consultar_aprendices_profesor(self):
        self.preparar_inscripcion()

        self.sistema.registrar_profesor(self.profesor)

        self.sistema.asignar_profesor(
            "CUR001", 123456
        )

        resultado = (
            self.sistema.consultar_aprendices_profesor(
                123456
            )
        )

        self.assertEqual(len(resultado), 1)

        self.assertIs(
            resultado[0]["curso"],
            self.curso
        )

        self.assertEqual(
            resultado[0]["aprendices"],
            [self.aprendiz]
        )

    def test_rendimiento_aprendiz(self):
        self.preparar_calificaciones()

        resultado = (
            self.sistema.consultar_rendimiento_aprendiz(
                654321
            )
        )

        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0]["promedio"], 4.0)
        self.assertEqual(resultado[0]["estado"], "Aprobado")

    def test_rendimiento_curso(self):
        self.preparar_calificaciones()

        resultado = self.sistema.consultar_rendimiento_curso(
            "CUR001"
        )

        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0]["aprendiz"], "Juan Pérez")
        self.assertEqual(resultado[0]["curso"], "Python")
        self.assertEqual(resultado[0]["promedio"], 4.0)

    def test_rendimiento_sin_calificaciones(self):
        self.preparar_inscripcion()

        resultado = (
            self.sistema.consultar_rendimiento_inscripcion(
                "I001"
            )
        )

        self.assertEqual(resultado["notas"], [])
        self.assertIsNone(resultado["promedio"])
        self.assertEqual(resultado["estado"], "Pendiente")

    def test_resumen_academico_completo(self):
        self.preparar_calificaciones()

        self.sistema.registrar_profesor(self.profesor)

        self.sistema.asignar_profesor(
            "CUR001", 123456
        )

        self.assertEqual(
            self.sistema.obtener_resumen(),
            {
                "profesores": 1,
                "aprendices": 1,
                "cursos": 1,
                "inscripciones": 1,
                "calificaciones": 3
            }
        )

    # Pruebas de ISP y DIP

    def test_inyeccion_gestion_profesores(self):
        gestor = Gestion_profesores()

        sistema = GestionAcademica(
            profesores=gestor
        )

        sistema.registrar_profesor(self.profesor)

        self.assertIs(
            gestor.buscar_por_documento(123456),
            self.profesor
        )

        self.assertEqual(
            sistema.listar_profesores(),
            gestor.listar()
        )

    def test_inyeccion_gestion_aprendices(self):
        gestor = Gestion_aprendices()

        sistema = GestionAcademica(
            aprendices=gestor
        )

        sistema.registrar_aprendiz(self.aprendiz)

        self.assertIs(
            gestor.buscar_documento(654321),
            self.aprendiz
        )

        self.assertEqual(
            sistema.listar_aprendices(),
            gestor.listar()
        )

    def test_inyeccion_gestion_cursos(self):
        gestor = GestionCursos()

        sistema = GestionAcademica(
            cursos=gestor
        )

        sistema.registrar_curso(self.curso)

        self.assertIs(
            gestor.buscar_por_codigo("CUR001"),
            self.curso
        )

        self.assertEqual(
            sistema.listar_cursos(),
            gestor.listar()
        )

    def test_inyeccion_gestion_inscripciones(self):
        gestor = GestionInscripciones()

        sistema = GestionAcademica(
            inscripciones=gestor
        )

        sistema.registrar_aprendiz(self.aprendiz)
        sistema.registrar_curso(self.curso)
        sistema.registrar_inscripcion(self.inscripcion)

        self.assertIs(
            gestor.buscar_por_codigo("I001"),
            self.inscripcion
        )

        self.assertEqual(
            sistema.listar_inscripciones(),
            gestor.listar()
        )

    def test_inyeccion_gestion_calificaciones(self):
        gestor = GestionCalificaciones()

        sistema = GestionAcademica(
            calificaciones=gestor
        )

        sistema.registrar_aprendiz(self.aprendiz)
        sistema.registrar_curso(self.curso)
        sistema.registrar_inscripcion(self.inscripcion)
        sistema.registrar_calificacion(self.calificacion)

        self.assertIs(
            gestor.buscar_por_codigo("N001"),
            self.calificacion
        )

        self.assertEqual(
            sistema.listar_calificaciones(),
            gestor.listar()
        )

    def test_implementacion_alternativa_dip(self):
        gestor: IGestionProfesores = (
            GestionProfesoresAlternativa()
        )

        sistema = GestionAcademica(
            profesores=gestor
        )

        self.assertTrue(
            sistema.registrar_profesor(self.profesor)
        )

        self.assertIs(
            sistema.buscar_profesor(123456),
            self.profesor
        )

        self.assertEqual(
            sistema.listar_profesores(),
            [self.profesor]
        )

        with self.assertRaises(ValueError):
            sistema.registrar_profesor(self.profesor)

    def test_interfaz_segregada_isp(self):
        gestor = GestionProfesoresAlternativa()

        self.assertFalse(
            hasattr(gestor, "mostrar")
        )

        sistema = GestionAcademica(
            profesores=gestor
        )

        sistema.registrar_profesor(self.profesor)
        sistema.registrar_curso(self.curso)

        sistema.asignar_profesor(
            "CUR001", 123456
        )

        self.assertIs(
            self.curso.profesor,
            self.profesor
        )

        self.assertEqual(
            sistema.consultar_cursos_profesor(123456),
            [self.curso]
        )

    def test_independencia_de_instancias(self):
        sistema1 = GestionAcademica()
        sistema2 = GestionAcademica()

        sistema1.registrar_profesor(self.profesor)
        sistema1.registrar_aprendiz(self.aprendiz)
        sistema1.registrar_curso(self.curso)
        sistema1.registrar_inscripcion(self.inscripcion)
        sistema1.registrar_calificacion(self.calificacion)

        self.assertEqual(
            sistema1.obtener_resumen(),
            {
                "profesores": 1,
                "aprendices": 1,
                "cursos": 1,
                "inscripciones": 1,
                "calificaciones": 1
            }
        )

        self.assertEqual(
            sistema2.obtener_resumen(),
            {
                "profesores": 0,
                "aprendices": 0,
                "cursos": 0,
                "inscripciones": 0,
                "calificaciones": 0
            }
        )


if __name__ == "__main__":
    unittest.main()
