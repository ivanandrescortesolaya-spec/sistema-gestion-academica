import unittest

from tests.api_rest import BasePruebasAPI

from api.excepciones import (
    DatosInvalidos,
    Conflicto,
    RecursoNoEncontrado
)


class TestCursosAPI(BasePruebasAPI):

    def setUp(self):

        super().setUp()

        self.curso = {
            "codigo": "CUR-001",
            "nombre": "Python",
            "descripcion": "Curso de programación",
            "duracion_horas": 48,
            "modalidad": "complementaria"
        }

        self.profesor = {
            "nombre": "Profesor Prueba",
            "documento": 123456789,
            "edad": 35,
            "profesion": "Ingeniero",
            "codigo": 1001,
            "especialidad": "Python"
        }

    def registrar_curso(self):

        respuesta = self.solicitar(
            "POST",
            "/cursos",
            self.curso
        )

        self.verificar_respuesta(respuesta, 201)

        return respuesta

    def registrar_profesor(self):

        respuesta = self.solicitar(
            "POST",
            "/profesores",
            self.profesor
        )

        self.verificar_respuesta(respuesta, 201)

        return respuesta

    def test_listar_cursos_vacio(self):

        respuesta = self.solicitar(
            "GET", "/cursos"
        )

        self.verificar_respuesta(respuesta, 200)

        self.assertEqual(
            respuesta.contenido["datos"], []
        )

    def test_registrar_curso(self):

        respuesta = self.registrar_curso()

        esperado = {
            **self.curso,
            "profesor": None
        }

        self.assertEqual(
            respuesta.contenido["datos"],
            esperado
        )

    def test_registrar_curso_location(self):

        respuesta = self.registrar_curso()

        self.assertEqual(
            respuesta.encabezados["Location"],
            "/api/v1/cursos/CUR-001"
        )

    def test_buscar_curso(self):

        self.registrar_curso()

        respuesta = self.solicitar(
            "GET",
            "/cursos/CUR-001"
        )

        self.verificar_respuesta(respuesta, 200)

        self.assertEqual(
            respuesta.contenido["datos"],
            {**self.curso, "profesor": None}
        )

    def test_listar_cursos_registrados(self):

        self.registrar_curso()

        respuesta = self.solicitar(
            "GET", "/cursos"
        )

        self.verificar_respuesta(respuesta, 200)

        self.assertEqual(
            respuesta.contenido["datos"],
            [{**self.curso, "profesor": None}]
        )

    def test_curso_duplicado(self):

        self.registrar_curso()

        with self.assertRaises(Conflicto):

            self.solicitar(
                "POST",
                "/cursos",
                self.curso
            )

    def test_curso_inexistente(self):

        with self.assertRaises(RecursoNoEncontrado):

            self.solicitar(
                "GET",
                "/cursos/CUR-999"
            )

    def test_curso_campos_faltantes(self):

        for campo in self.curso:

            with self.subTest(campo=campo):

                datos = self.curso.copy()

                del datos[campo]

                with self.assertRaises(DatosInvalidos):

                    self.solicitar(
                        "POST",
                        "/cursos",
                        datos
                    )

    def test_curso_campos_desconocidos(self):

        datos = {
            **self.curso,
            "campo_extra": True
        }

        with self.assertRaises(DatosInvalidos):

            self.solicitar(
                "POST",
                "/cursos",
                datos
            )

    def test_curso_datos_invalidos(self):

        valores = (
            ("codigo", ""),
            ("nombre", ""),
            ("descripcion", ""),
            ("duracion_horas", 0),
            ("duracion_horas", -1),
            ("modalidad", "virtual")
        )

        for campo, valor in valores:

            with self.subTest(campo=campo):

                datos = {
                    **self.curso,
                    campo: valor
                }

                with self.assertRaises(DatosInvalidos):

                    self.solicitar(
                        "POST",
                        "/cursos",
                        datos
                    )

    def test_registrar_curso_titulado(self):

        datos = {
            **self.curso,
            "modalidad": "titulada"
        }

        respuesta = self.solicitar(
            "POST",
            "/cursos",
            datos
        )

        self.verificar_respuesta(respuesta, 201)

        self.assertEqual(
            respuesta.contenido["datos"]["modalidad"],
            "titulada"
        )

    def test_normalizar_modalidad(self):

        datos = {
            **self.curso,
            "modalidad": " COMPLEMENTARIA "
        }

        respuesta = self.solicitar(
            "POST",
            "/cursos",
            datos
        )

        self.verificar_respuesta(respuesta, 201)

        self.assertEqual(
            respuesta.contenido["datos"]["modalidad"],
            "complementaria"
        )

    def test_asignar_profesor(self):

        self.registrar_curso()

        self.registrar_profesor()

        respuesta = self.solicitar(
            "PUT",
            "/cursos/CUR-001/profesor",
            {"documento": 123456789}
        )

        self.verificar_respuesta(respuesta, 200)

        self.assertEqual(
            respuesta.contenido["datos"]["profesor"],
            self.profesor
        )

    def test_consultar_profesor_asignado(self):

        self.registrar_curso()

        self.registrar_profesor()

        respuesta = self.solicitar(
            "PUT",
            "/cursos/CUR-001/profesor",
            {"documento": 123456789}
        )

        self.verificar_respuesta(respuesta, 200)

        respuesta = self.solicitar(
            "GET",
            "/cursos/CUR-001"
        )

        self.verificar_respuesta(respuesta, 200)

        self.assertEqual(
            respuesta.contenido["datos"]["profesor"],
            self.profesor
        )

    def test_asignar_profesor_inexistente(self):

        self.registrar_curso()

        with self.assertRaises(RecursoNoEncontrado):

            self.solicitar(
                "PUT",
                "/cursos/CUR-001/profesor",
                {"documento": 999999999}
            )

    def test_asignar_profesor_curso_inexistente(self):

        self.registrar_profesor()

        with self.assertRaises(RecursoNoEncontrado):

            self.solicitar(
                "PUT",
                "/cursos/CUR-999/profesor",
                {"documento": 123456789}
            )

    def test_asignar_profesor_datos_invalidos(self):

        self.registrar_curso()

        valores = (
            {},
            {"documento": 0},
            {"documento": "ABC"},
            {"documento": 123, "extra": True}
        )

        for datos in valores:

            with self.subTest(datos=datos):

                with self.assertRaises(DatosInvalidos):

                    self.solicitar(
                        "PUT",
                        "/cursos/CUR-001/profesor",
                        datos
                    )

    def test_consultar_aprendices_vacios(self):

        self.registrar_curso()

        respuesta = self.solicitar(
            "GET",
            "/cursos/CUR-001/aprendices"
        )

        self.verificar_respuesta(respuesta, 200)

        self.assertEqual(
            respuesta.contenido["datos"], []
        )

    def test_consultar_inscripciones_vacias(self):

        self.registrar_curso()

        respuesta = self.solicitar(
            "GET",
            "/cursos/CUR-001/inscripciones"
        )

        self.verificar_respuesta(respuesta, 200)

        self.assertEqual(
            respuesta.contenido["datos"], []
        )

    def test_consultar_calificaciones_vacias(self):

        self.registrar_curso()

        respuesta = self.solicitar(
            "GET",
            "/cursos/CUR-001/calificaciones"
        )

        self.verificar_respuesta(respuesta, 200)

        self.assertEqual(
            respuesta.contenido["datos"], []
        )

    def test_consultar_rendimiento_vacio(self):

        self.registrar_curso()

        respuesta = self.solicitar(
            "GET",
            "/cursos/CUR-001/rendimiento"
        )

        self.verificar_respuesta(respuesta, 200)

        self.assertEqual(
            respuesta.contenido["datos"], []
        )

    def test_consultar_relaciones_curso_inexistente(self):

        relaciones = (
            "aprendices",
            "inscripciones",
            "calificaciones",
            "rendimiento"
        )

        for relacion in relaciones:

            with self.subTest(relacion=relacion):

                with self.assertRaises(RecursoNoEncontrado):

                    self.solicitar(
                        "GET",
                        f"/cursos/CUR-999/{relacion}"
                    )


if __name__ == "__main__":

    unittest.main()