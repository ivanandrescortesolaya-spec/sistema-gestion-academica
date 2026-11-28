import unittest

from tests.api_rest import BasePruebasAPI

from api.excepciones import (
    DatosInvalidos,
    Conflicto,
    RecursoNoEncontrado
)


class TestProfesoresAPI(BasePruebasAPI):

    def setUp(self):

        super().setUp()

        self.profesor = {
            "nombre": "Profesor Prueba",
            "documento": 123456789,
            "edad": 35,
            "profesion": "Ingeniero",
            "codigo": 1001,
            "especialidad": "Python"
        }

    def registrar_profesor(self):

        respuesta = self.solicitar(
            "POST",
            "/profesores",
            self.profesor
        )

        self.verificar_respuesta(respuesta, 201)

        return respuesta

    def test_listar_profesores_vacio(self):

        respuesta = self.solicitar(
            "GET", "/profesores"
        )

        self.verificar_respuesta(respuesta, 200)

        self.assertEqual(
            respuesta.contenido["datos"], []
        )

    def test_registrar_profesor(self):

        respuesta = self.registrar_profesor()

        self.assertEqual(
            respuesta.contenido["datos"],
            self.profesor
        )

    def test_registrar_profesor_location(self):

        respuesta = self.registrar_profesor()

        self.assertEqual(
            respuesta.encabezados["Location"],
            "/api/v1/profesores/123456789"
        )

    def test_buscar_profesor(self):

        self.registrar_profesor()

        respuesta = self.solicitar(
            "GET",
            "/profesores/123456789"
        )

        self.verificar_respuesta(respuesta, 200)

        self.assertEqual(
            respuesta.contenido["datos"],
            self.profesor
        )

    def test_listar_profesores_registrados(self):

        self.registrar_profesor()

        respuesta = self.solicitar(
            "GET", "/profesores"
        )

        self.verificar_respuesta(respuesta, 200)

        self.assertEqual(
            respuesta.contenido["datos"],
            [self.profesor]
        )

    def test_profesor_duplicado(self):

        self.registrar_profesor()

        with self.assertRaises(Conflicto):

            self.solicitar(
                "POST",
                "/profesores",
                self.profesor
            )

    def test_profesor_inexistente(self):

        with self.assertRaises(RecursoNoEncontrado):

            self.solicitar(
                "GET",
                "/profesores/999999999"
            )

    def test_profesor_campos_faltantes(self):

        for campo in self.profesor:

            with self.subTest(campo=campo):

                datos = self.profesor.copy()

                del datos[campo]

                with self.assertRaises(DatosInvalidos):

                    self.solicitar(
                        "POST",
                        "/profesores",
                        datos
                    )

    def test_profesor_campos_desconocidos(self):

        datos = {
            **self.profesor,
            "campo_extra": True
        }

        with self.assertRaises(DatosInvalidos):

            self.solicitar(
                "POST",
                "/profesores",
                datos
            )

    def test_profesor_datos_invalidos(self):

        valores = (
            ("nombre", ""),
            ("documento", 0),
            ("edad", -1),
            ("profesion", ""),
            ("codigo", 0),
            ("especialidad", "")
        )

        for campo, valor in valores:

            with self.subTest(campo=campo):

                datos = {
                    **self.profesor,
                    campo: valor
                }

                with self.assertRaises(DatosInvalidos):

                    self.solicitar(
                        "POST",
                        "/profesores",
                        datos
                    )

    def test_buscar_documento_invalido(self):

        with self.assertRaises(DatosInvalidos):

            self.solicitar(
                "GET",
                "/profesores/ABC"
            )

    def test_consultar_cursos_sin_asignacion(self):

        self.registrar_profesor()

        respuesta = self.solicitar(
            "GET",
            "/profesores/123456789/cursos"
        )

        self.verificar_respuesta(respuesta, 200)

        self.assertEqual(
            respuesta.contenido["datos"], []
        )

    def test_consultar_cursos_asignados(self):

        self.registrar_profesor()

        respuesta = self.solicitar(
            "POST",
            "/cursos",
            {
                "codigo": "CUR-001",
                "nombre": "Python",
                "descripcion": "Curso de prueba",
                "duracion_horas": 48,
                "modalidad": "complementaria"
            }
        )

        self.verificar_respuesta(respuesta, 201)

        respuesta = self.solicitar(
            "PUT",
            "/cursos/CUR-001/profesor",
            {"documento": 123456789}
        )

        self.verificar_respuesta(respuesta, 200)

        respuesta = self.solicitar(
            "GET",
            "/profesores/123456789/cursos"
        )

        self.verificar_respuesta(respuesta, 200)

        cursos = respuesta.contenido["datos"]

        self.assertEqual(len(cursos), 1)

        self.assertEqual(
            cursos[0]["codigo"],
            "CUR-001"
        )

    def test_consultar_aprendices_sin_cursos(self):

        self.registrar_profesor()

        respuesta = self.solicitar(
            "GET",
            "/profesores/123456789/aprendices"
        )

        self.verificar_respuesta(respuesta, 200)

        self.assertEqual(
            respuesta.contenido["datos"], []
        )

    def test_consultar_relaciones_profesor_inexistente(self):

        for relacion in ("cursos", "aprendices"):

            with self.subTest(relacion=relacion):

                with self.assertRaises(RecursoNoEncontrado):

                    self.solicitar(
                        "GET",
                        f"/profesores/999999999/{relacion}"
                    )


if __name__ == "__main__":

    unittest.main()