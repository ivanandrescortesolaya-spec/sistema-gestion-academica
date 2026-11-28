import unittest

from tests.api_rest import BasePruebasAPI

from api.excepciones import (
    DatosInvalidos,
    Conflicto,
    RecursoNoEncontrado
)


class TestAprendicesAPI(BasePruebasAPI):

    def setUp(self):

        super().setUp()

        self.aprendiz = {
            "nombre": "Aprendiz Prueba",
            "documento": 987654321,
            "edad": 22,
            "telefono": "3001234567",
            "correo": "aprendiz@example.com",
            "direccion": "Dirección de prueba"
        }

    def registrar_aprendiz(self):

        respuesta = self.solicitar(
            "POST",
            "/aprendices",
            self.aprendiz
        )

        self.verificar_respuesta(respuesta, 201)

        return respuesta

    def test_listar_aprendices_vacio(self):

        respuesta = self.solicitar(
            "GET", "/aprendices"
        )

        self.verificar_respuesta(respuesta, 200)

        self.assertEqual(
            respuesta.contenido["datos"], []
        )

    def test_registrar_aprendiz(self):

        respuesta = self.registrar_aprendiz()

        self.assertEqual(
            respuesta.contenido["datos"],
            self.aprendiz
        )

    def test_registrar_aprendiz_location(self):

        respuesta = self.registrar_aprendiz()

        self.assertEqual(
            respuesta.encabezados["Location"],
            "/api/v1/aprendices/987654321"
        )

    def test_buscar_aprendiz(self):

        self.registrar_aprendiz()

        respuesta = self.solicitar(
            "GET",
            "/aprendices/987654321"
        )

        self.verificar_respuesta(respuesta, 200)

        self.assertEqual(
            respuesta.contenido["datos"],
            self.aprendiz
        )

    def test_listar_aprendices_registrados(self):

        self.registrar_aprendiz()

        respuesta = self.solicitar(
            "GET", "/aprendices"
        )

        self.verificar_respuesta(respuesta, 200)

        self.assertEqual(
            respuesta.contenido["datos"],
            [self.aprendiz]
        )

    def test_aprendiz_duplicado(self):

        self.registrar_aprendiz()

        with self.assertRaises(Conflicto):

            self.solicitar(
                "POST",
                "/aprendices",
                self.aprendiz
            )

    def test_aprendiz_inexistente(self):

        with self.assertRaises(RecursoNoEncontrado):

            self.solicitar(
                "GET",
                "/aprendices/999999999"
            )

    def test_aprendiz_campos_faltantes(self):

        for campo in self.aprendiz:

            with self.subTest(campo=campo):

                datos = self.aprendiz.copy()

                del datos[campo]

                with self.assertRaises(DatosInvalidos):

                    self.solicitar(
                        "POST",
                        "/aprendices",
                        datos
                    )

    def test_aprendiz_campos_desconocidos(self):

        datos = {
            **self.aprendiz,
            "campo_extra": True
        }

        with self.assertRaises(DatosInvalidos):

            self.solicitar(
                "POST",
                "/aprendices",
                datos
            )

    def test_aprendiz_datos_invalidos(self):

        valores = (
            ("nombre", ""),
            ("documento", -1),
            ("edad", -1),
            ("telefono", "ABC"),
            ("correo", "correo-invalido"),
            ("direccion", "")
        )

        for campo, valor in valores:

            with self.subTest(campo=campo):

                datos = {
                    **self.aprendiz,
                    campo: valor
                }

                with self.assertRaises(DatosInvalidos):

                    self.solicitar(
                        "POST",
                        "/aprendices",
                        datos
                    )

    def test_aprendiz_documento_invalido(self):

        with self.assertRaises(DatosInvalidos):

            self.solicitar(
                "GET",
                "/aprendices/ABC"
            )

    def test_consultar_cursos_vacios(self):

        self.registrar_aprendiz()

        respuesta = self.solicitar(
            "GET",
            "/aprendices/987654321/cursos"
        )

        self.verificar_respuesta(respuesta, 200)

        self.assertEqual(
            respuesta.contenido["datos"], []
        )

    def test_consultar_inscripciones_vacias(self):

        self.registrar_aprendiz()

        respuesta = self.solicitar(
            "GET",
            "/aprendices/987654321/inscripciones"
        )

        self.verificar_respuesta(respuesta, 200)

        self.assertEqual(
            respuesta.contenido["datos"], []
        )

    def test_consultar_calificaciones_vacias(self):

        self.registrar_aprendiz()

        respuesta = self.solicitar(
            "GET",
            "/aprendices/987654321/calificaciones"
        )

        self.verificar_respuesta(respuesta, 200)

        self.assertEqual(
            respuesta.contenido["datos"], []
        )

    def test_consultar_rendimiento_vacio(self):

        self.registrar_aprendiz()

        respuesta = self.solicitar(
            "GET",
            "/aprendices/987654321/rendimiento"
        )

        self.verificar_respuesta(respuesta, 200)

        self.assertEqual(
            respuesta.contenido["datos"], []
        )

    def test_consultar_relaciones_aprendiz_inexistente(self):

        relaciones = (
            "cursos",
            "inscripciones",
            "calificaciones",
            "rendimiento"
        )

        for relacion in relaciones:

            with self.subTest(relacion=relacion):

                with self.assertRaises(RecursoNoEncontrado):

                    self.solicitar(
                        "GET",
                        f"/aprendices/999999999/{relacion}"
                    )

    def test_consultar_curso_inscrito(self):

        self.registrar_aprendiz()

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
            "POST",
            "/inscripciones",
            {
                "codigo": "INS-001",
                "documento_aprendiz": 987654321,
                "codigo_curso": "CUR-001"
            }
        )

        self.verificar_respuesta(respuesta, 201)

        respuesta = self.solicitar(
            "GET",
            "/aprendices/987654321/cursos"
        )

        self.verificar_respuesta(respuesta, 200)

        cursos = respuesta.contenido["datos"]

        self.assertEqual(len(cursos), 1)

        self.assertEqual(
            cursos[0]["codigo"],
            "CUR-001"
        )


if __name__ == "__main__":

    unittest.main()