import os
import unittest

from uuid import uuid4
from datetime import date

from persistencia import ConfiguracionBD, ConexionMySQL
from persistencia.fabrica import crear_sistema_mysql

from personas.profesores import Profesor
from personas.aprendices import Aprendiz
from cursos.curso import Curso
from inscripciones.inscripcion import Inscripcion
from calificaciones.calificacion import Calificacion


class BaseIntegracion(unittest.TestCase):

    def setUp(self):
        if os.getenv("RUN_MYSQL_TESTS") != "1":
            self.skipTest("Pruebas MySQL no habilitadas")

        self.config = ConfiguracionBD.desde_entorno(pruebas=True)
        self.conexion = ConexionMySQL(self.config)

        with self.conexion.transaccion() as cn:
            cursor = cn.cursor()
            try:
                cursor.execute("SELECT DATABASE(), CURRENT_USER()")
                fila = cursor.fetchone()

                if not isinstance(fila, (tuple, list)):
                    self.fail("MySQL no devolvió una fila válida")

                if len(fila) != 2:
                    self.fail("Respuesta inesperada de MySQL")

                base, usuario = fila

                if not isinstance(base, str):
                    self.fail("Nombre de base de datos inválido")

                if not isinstance(usuario, str):
                    self.fail("Usuario de base de datos inválido")

                self.assertEqual(
                    base, "sistema_gestion_academica_test"
                )

                self.assertEqual(
                    usuario.split("@")[0], "academic_test_user"
                )
            finally:
                cursor.close()

        self.sistema = crear_sistema_mysql(pruebas=True)

        self.uid = uuid4().hex[:16]
        numero = uuid4().int % 1000000000

        self.doc_profesor = 840000000000 + numero
        self.doc_aprendiz = 850000000000 + numero
        self.codigo_profesor = 2000000000 + numero

        self.codigo_curso = "C-" + self.uid
        self.codigo_inscripcion = "I-" + self.uid

        self.fecha = date(2025, 1, 15)

        self.profesor = Profesor(
            "Profesor Prueba",
            self.doc_profesor,
            35,
            "Ingeniero",
            self.codigo_profesor,
            "Python"
        )

        self.aprendiz = Aprendiz(
            "Aprendiz Prueba",
            self.doc_aprendiz,
            22,
            "3001234567",
            "prueba@example.com",
            "Dirección de prueba"
        )

        self.curso = Curso(
            self.codigo_curso,
            "Python",
            "Curso de integración",
            48,
            "complementaria"
        )

        self.profesor_creado = False
        self.aprendiz_creado = False
        self.curso_creado = False
        self.inscripcion_creada = False
        self.notas_creadas: list[str] = []

        self.addCleanup(self.limpiar)

    def preparar_profesor(self):
        self.profesor_creado = self.sistema.registrar_profesor(
            self.profesor
        )
        self.assertTrue(self.profesor_creado)

    def preparar_aprendiz(self):
        self.aprendiz_creado = self.sistema.registrar_aprendiz(
            self.aprendiz
        )
        self.assertTrue(self.aprendiz_creado)

    def preparar_curso(self):
        self.curso_creado = self.sistema.registrar_curso(
            self.curso
        )
        self.assertTrue(self.curso_creado)

    def preparar_inscripcion(self):
        self.preparar_aprendiz()
        self.preparar_curso()

        self.inscripcion = Inscripcion(
            self.codigo_inscripcion,
            self.aprendiz,
            self.curso,
            fecha_inscripcion=self.fecha
        )

        self.inscripcion_creada = (
            self.sistema.registrar_inscripcion(self.inscripcion)
        )

        self.assertTrue(self.inscripcion_creada)

    def registrar_nota(self, numero, nota):
        codigo = f"N{numero}-{self.uid}"

        inscripcion = self.sistema.buscar_inscripcion(
            self.codigo_inscripcion
        )

        assert inscripcion is not None, (
            "No se encontró la inscripción de prueba"
        )

        calificacion = Calificacion(
            codigo,
            inscripcion,
            nota,
            fecha=self.fecha
        )

        resultado = self.sistema.registrar_calificacion(
            calificacion
        )

        if resultado:
            self.notas_creadas.append(codigo)

        self.assertTrue(resultado)

        return codigo

    def preparar_calificaciones(self):
        self.preparar_inscripcion()

        for numero, nota in enumerate([3.0, 4.0, 5.0], 1):
            self.registrar_nota(numero, nota)

    def limpiar(self):
        with self.conexion.transaccion() as cn:
            cursor = cn.cursor()

            try:
                for codigo in self.notas_creadas:
                    cursor.execute(
                        "DELETE FROM calificacion WHERE codigo = %s",
                        (codigo,)
                    )

                if self.inscripcion_creada:
                    cursor.execute(
                        "DELETE FROM inscripcion WHERE codigo = %s",
                        (self.codigo_inscripcion,)
                    )

                if self.curso_creado:
                    cursor.execute(
                        "DELETE FROM curso WHERE codigo = %s",
                        (self.codigo_curso,)
                    )

                if self.aprendiz_creado:
                    cursor.execute("""
                        DELETE a FROM aprendiz a
                        INNER JOIN persona p
                            ON p.id_persona = a.id_persona
                        WHERE p.documento = %s
                    """, (str(self.doc_aprendiz),))

                    cursor.execute(
                        "DELETE FROM persona WHERE documento = %s",
                        (str(self.doc_aprendiz),)
                    )

                if self.profesor_creado:
                    cursor.execute("""
                        DELETE pr FROM profesor pr
                        INNER JOIN persona p
                            ON p.id_persona = pr.id_persona
                        WHERE p.documento = %s
                    """, (str(self.doc_profesor),))

                    cursor.execute(
                        "DELETE FROM persona WHERE documento = %s",
                        (str(self.doc_profesor),)
                    )

            finally:
                cursor.close()
