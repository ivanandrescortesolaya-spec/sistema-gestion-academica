
import unittest
from unittest.mock import patch
from io import StringIO

from gestion_academica import GestionAcademica
from personas.profesores import Profesor
from personas.aprendices import Aprendiz
from cursos.curso import Curso
from inscripciones.inscripcion import Inscripcion
from calificaciones.calificacion import Calificacion

from main import (
    main,
    mostrar_menu,
    menu_profesores,
    menu_aprendices,
    menu_cursos,
    menu_inscripciones,
    menu_calificaciones,
    menu_reportes
)


class TestMain(unittest.TestCase):

    def setUp(self):
        self.sistema = GestionAcademica()

        self.profesor = Profesor(
            "Carlos Pérez",
            123456,
            35,
            "Ingeniero",
            101,
            "Programación"
        )

        self.aprendiz = Aprendiz(
            "Juan Pérez",
            654321,
            20,
            "3101234567",
            "juan@gmail.com",
            "Calle 15"
        )

        self.curso = Curso(
            "CUR001",
            "Python",
            "Fundamentos de programación",
            120,
            "titulada"
        )

        self.inscripcion = Inscripcion(
            "I001",
            self.aprendiz,
            self.curso
        )

    # Funciones auxiliares

    def ejecutar_menu(self, funcion, datos):
        with patch("builtins.input", side_effect=datos):
            with patch("sys.stdout", new_callable=StringIO) as salida:
                funcion(self.sistema)

        return salida.getvalue()

    def preparar_registros(self):
        self.sistema.registrar_profesor(self.profesor)
        self.sistema.registrar_aprendiz(self.aprendiz)
        self.sistema.registrar_curso(self.curso)

    def preparar_inscripcion(self):
        self.preparar_registros()
        self.sistema.registrar_inscripcion(self.inscripcion)

    def preparar_calificaciones(self):
        self.preparar_inscripcion()

        notas = [
            ("N001", 4.5),
            ("N002", 3.5),
            ("N003", 4.0)
        ]

        for codigo, nota in notas:
            calificacion = Calificacion(
                codigo,
                self.inscripcion,
                nota
            )

            self.sistema.registrar_calificacion(calificacion)

    # Pruebas del menu principal

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

    def test_resumen_academico(self):
        datos = ["6", "1", "0", "0"]

        with patch("builtins.input", side_effect=datos):
            with patch("sys.stdout", new_callable=StringIO) as salida:
                main()

        resultado = salida.getvalue()

        self.assertIn("Profesores: 0", resultado)
        self.assertIn("Aprendices: 0", resultado)
        self.assertIn("Cursos: 0", resultado)
        self.assertIn("Inscripciones: 0", resultado)
        self.assertIn("Calificaciones: 0", resultado)

    def test_acceder_menu_inscripciones(self):
        with patch("builtins.input", side_effect=["4", "0", "0"]):
            with patch("sys.stdout", new_callable=StringIO) as salida:
                main()

        self.assertIn(
            "GESTIÓN DE INSCRIPCIONES",
            salida.getvalue()
        )

    def test_acceder_menu_calificaciones(self):
        with patch("builtins.input", side_effect=["5", "0", "0"]):
            with patch("sys.stdout", new_callable=StringIO) as salida:
                main()

        self.assertIn(
            "GESTIÓN DE CALIFICACIONES",
            salida.getvalue()
        )

    def test_acceder_menu_reportes(self):
        with patch("builtins.input", side_effect=["6", "0", "0"]):
            with patch("sys.stdout", new_callable=StringIO) as salida:
                main()

        self.assertIn(
            "REPORTES ACADÉMICOS",
            salida.getvalue()
        )

    # Pruebas de profesores

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

        self.ejecutar_menu(menu_profesores, datos)

        self.assertIsNotNone(
            self.sistema.buscar_profesor(123456)
        )

    def test_documento_invalido(self):
        datos = ["2", "abc", "0"]

        resultado = self.ejecutar_menu(
            menu_profesores,
            datos
        )

        self.assertIn("Error:", resultado)

    def test_consultar_cursos_profesor(self):
        self.preparar_registros()

        self.sistema.asignar_profesor(
            "CUR001",
            123456
        )

        resultado = self.ejecutar_menu(
            menu_profesores,
            ["4", "123456", "0"]
        )

        self.assertIn("Python", resultado)
        self.assertIn("CUR001", resultado)

    def test_consultar_aprendices_profesor(self):
        self.preparar_inscripcion()

        self.sistema.asignar_profesor(
            "CUR001",
            123456
        )

        resultado = self.ejecutar_menu(
            menu_profesores,
            ["5", "123456", "0"]
        )

        self.assertIn("Python", resultado)
        self.assertIn("Juan Pérez", resultado)

    # Pruebas de aprendices

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

        self.ejecutar_menu(menu_aprendices, datos)

        self.assertIsNotNone(
            self.sistema.buscar_aprendiz(654321)
        )

    def test_consultar_cursos_aprendiz(self):
        self.preparar_inscripcion()

        resultado = self.ejecutar_menu(
            menu_aprendices,
            ["4", "654321", "0"]
        )

        self.assertIn("Python", resultado)
        self.assertIn("CUR001", resultado)

    # Pruebas de cursos

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

        self.ejecutar_menu(menu_cursos, datos)

        self.assertIsNotNone(
            self.sistema.buscar_curso("CUR001")
        )

    def test_asignar_profesor_curso(self):
        self.preparar_registros()

        resultado = self.ejecutar_menu(
            menu_cursos,
            ["4", "CUR001", "123456", "0"]
        )

        self.assertIs(
            self.curso.profesor,
            self.profesor
        )

        self.assertIn(
            "Profesor asignado correctamente",
            resultado
        )

    def test_consultar_aprendices_curso(self):
        self.preparar_inscripcion()

        resultado = self.ejecutar_menu(
            menu_cursos,
            ["5", "CUR001", "0"]
        )

        self.assertIn("Juan Pérez", resultado)
        self.assertIn("654321", resultado)

    # Pruebas de inscripciones

    def test_registrar_inscripcion(self):
        self.preparar_registros()

        resultado = self.ejecutar_menu(
            menu_inscripciones,
            ["1", "I001", "654321", "CUR001", "0"]
        )

        self.assertIsNotNone(
            self.sistema.buscar_inscripcion("I001")
        )

        self.assertIn(
            "Inscripción registrada correctamente",
            resultado
        )

    def test_inscripcion_duplicada(self):
        self.preparar_inscripcion()

        resultado = self.ejecutar_menu(
            menu_inscripciones,
            ["1", "I002", "654321", "CUR001", "0"]
        )

        self.assertIn("Error:", resultado)

        self.assertEqual(
            len(self.sistema.listar_inscripciones()),
            1
        )

    def test_inscripcion_aprendiz_inexistente(self):
        self.preparar_registros()

        resultado = self.ejecutar_menu(
            menu_inscripciones,
            ["1", "I001", "999999", "CUR001", "0"]
        )

        self.assertIn(
            "El aprendiz no está registrado",
            resultado
        )

        self.assertEqual(
            len(self.sistema.listar_inscripciones()),
            0
        )

    def test_inscripcion_curso_inexistente(self):
        self.preparar_registros()

        resultado = self.ejecutar_menu(
            menu_inscripciones,
            ["1", "I001", "654321", "CUR999", "0"]
        )

        self.assertIn(
            "El curso no está registrado",
            resultado
        )

        self.assertEqual(
            len(self.sistema.listar_inscripciones()),
            0
        )

    def test_buscar_inscripcion(self):
        self.preparar_inscripcion()

        resultado = self.ejecutar_menu(
            menu_inscripciones,
            ["2", "I001", "0"]
        )

        self.assertIn("I001", resultado)
        self.assertIn("Juan Pérez", resultado)
        self.assertIn("Python", resultado)

    def test_cancelar_inscripcion(self):
        self.preparar_inscripcion()

        resultado = self.ejecutar_menu(
            menu_inscripciones,
            ["6", "I001", "0"]
        )

        self.assertEqual(
            self.inscripcion.estado,
            "Cancelada"
        )

        self.assertIn(
            "Inscripción cancelada correctamente",
            resultado
        )

    def test_finalizar_inscripcion(self):
        self.preparar_inscripcion()

        resultado = self.ejecutar_menu(
            menu_inscripciones,
            ["7", "I001", "0"]
        )

        self.assertEqual(
            self.inscripcion.estado,
            "Finalizada"
        )

        self.assertIn(
            "Inscripción finalizada correctamente",
            resultado
        )

    # Pruebas de calificaciones

    def test_registrar_calificacion(self):
        self.preparar_inscripcion()

        resultado = self.ejecutar_menu(
            menu_calificaciones,
            ["1", "N001", "I001", "4.5", "0"]
        )

        calificacion = self.sistema.buscar_calificacion("N001")

        assert calificacion is not None

        self.assertEqual(calificacion.nota, 4.5)

        self.assertIn(
            "Calificación registrada correctamente",
            resultado
        )

    def test_calificacion_inscripcion_inexistente(self):
        resultado = self.ejecutar_menu(
            menu_calificaciones,
            ["1", "N001", "I999", "0"]
        )

        self.assertIn(
            "La inscripción no existe",
            resultado
        )

        self.assertEqual(
            len(self.sistema.listar_calificaciones()),
            0
        )

    def test_calificacion_duplicada(self):
        self.preparar_calificaciones()

        resultado = self.ejecutar_menu(
            menu_calificaciones,
            ["1", "N001", "I001", "3.0", "0"]
        )

        self.assertIn(
            "La calificación ya existe",
            resultado
        )

        self.assertEqual(
            len(self.sistema.listar_calificaciones()),
            3
        )

    def test_calificacion_fuera_de_rango(self):
        self.preparar_inscripcion()

        resultado = self.ejecutar_menu(
            menu_calificaciones,
            ["1", "N001", "I001", "5.5", "0"]
        )

        self.assertIn("Error:", resultado)

        self.assertEqual(
            len(self.sistema.listar_calificaciones()),
            0
        )

    def test_modificar_calificacion(self):
        self.preparar_calificaciones()

        resultado = self.ejecutar_menu(
            menu_calificaciones,
            ["4", "N002", "5.0", "0"]
        )

        calificacion = self.sistema.buscar_calificacion("N002")

        assert calificacion is not None

        self.assertEqual(calificacion.nota, 5.0)

        self.assertIn(
            "Calificación modificada correctamente",
            resultado
        )

    def test_consultar_calificaciones_aprendiz(self):
        self.preparar_calificaciones()

        resultado = self.ejecutar_menu(
            menu_calificaciones,
            ["6", "654321", "0"]
        )

        self.assertIn("N001", resultado)
        self.assertIn("N002", resultado)
        self.assertIn("N003", resultado)

    def test_consultar_promedio(self):
        self.preparar_calificaciones()

        resultado = self.ejecutar_menu(
            menu_calificaciones,
            ["8", "I001", "0"]
        )

        self.assertIn("Promedio: 4.00", resultado)
        self.assertIn("Estado: Aprobado", resultado)

    def test_promedio_pendiente(self):
        self.preparar_inscripcion()

        self.sistema.registrar_calificacion(
            Calificacion(
                "N001",
                self.inscripcion,
                4.5
            )
        )

        resultado = self.ejecutar_menu(
            menu_calificaciones,
            ["8", "I001", "0"]
        )

        self.assertIn("Promedio: Pendiente", resultado)
        self.assertIn("Estado: Pendiente", resultado)

    def test_recalcular_promedio(self):
        self.preparar_calificaciones()

        resultado = self.ejecutar_menu(
            menu_calificaciones,
            ["4", "N002", "5.0", "8", "I001", "0"]
        )

        self.assertIn("Promedio: 4.50", resultado)
        self.assertIn("Estado: Aprobado", resultado)

    # Pruebas de reportes

    def test_resumen_academico_completo(self):
        self.preparar_calificaciones()

        resultado = self.ejecutar_menu(
            menu_reportes,
            ["1", "0"]
        )

        self.assertIn("Profesores: 1", resultado)
        self.assertIn("Aprendices: 1", resultado)
        self.assertIn("Cursos: 1", resultado)
        self.assertIn("Inscripciones: 1", resultado)
        self.assertIn("Calificaciones: 3", resultado)

    def test_reporte_general_calificaciones(self):
        self.preparar_calificaciones()

        resultado = self.ejecutar_menu(
            menu_reportes,
            ["2", "0"]
        )

        self.assertIn(
            "REPORTE DE CALIFICACIONES",
            resultado
        )

        self.assertIn(
            "Total de calificaciones: 3",
            resultado
        )

        self.assertIn(
            "Promedio general: 4.00",
            resultado
        )

    def test_reporte_rendimiento_aprendiz(self):
        self.preparar_calificaciones()

        resultado = self.ejecutar_menu(
            menu_reportes,
            ["3", "654321", "0"]
        )

        self.assertIn("Juan Pérez", resultado)
        self.assertIn("Promedio: 4.00", resultado)
        self.assertIn("Estado: Aprobado", resultado)

    def test_reporte_rendimiento_curso(self):
        self.preparar_calificaciones()

        resultado = self.ejecutar_menu(
            menu_reportes,
            ["4", "CUR001", "0"]
        )

        self.assertIn("Python", resultado)
        self.assertIn("Juan Pérez", resultado)
        self.assertIn("Promedio: 4.00", resultado)


if __name__ == "__main__":
    unittest.main()
