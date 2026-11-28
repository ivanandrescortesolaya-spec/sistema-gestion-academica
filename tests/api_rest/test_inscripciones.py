import unittest

from tests.api_rest import BasePruebasAPI

from api.excepciones import (
    DatosInvalidos,
    Conflicto,
    RecursoNoEncontrado
)


class TestInscripcionesAPI(BasePruebasAPI):

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

        self.curso = {
            "codigo": "CUR-001",
            "nombre": "Python",
            "descripcion": "Curso de programación",
            "duracion_horas": 48,
            "modalidad": "complementaria"
        }

        self.inscripcion = {
            "codigo": "INS-001",
            "documento_aprendiz": 987654321,
            "codigo_curso": "CUR-001",
            "fecha_inscripcion": "2026-11-28"
        }

        respuesta = self.solicitar(
            "POST", "/aprendices", self.aprendiz
        )

        self.verificar_respuesta(respuesta, 201)

        respuesta = self.solicitar(
            "POST", "/cursos", self.curso
        )

        self.verificar_respuesta(respuesta, 201)

    def registrar_inscripcion(self):

        respuesta = self.solicitar(
            "POST",
            "/inscripciones",
            self.inscripcion
        )

        self.verificar_respuesta(respuesta, 201)

        return respuesta

    def registrar_calificaciones(self):

        for numero, nota in enumerate(
            (3.0, 4.0, 5.0),
            start=1
        ):

            respuesta = self.solicitar(
                "POST",
                "/calificaciones",
                {
                    "codigo": f"NOT-00{numero}",
                    "codigo_inscripcion": "INS-001",
                    "nota": nota
                }
            )

            self.verificar_respuesta(respuesta, 201)

    def test_listar_inscripciones_vacias(self):

        respuesta = self.solicitar(
            "GET", "/inscripciones"
        )

        self.verificar_respuesta(respuesta, 200)

        self.assertEqual(
            respuesta.contenido["datos"], []
        )

    def test_registrar_inscripcion(self):

        respuesta = self.registrar_inscripcion()

        datos = respuesta.contenido["datos"]

        self.assertEqual(datos["codigo"], "INS-001")
        self.assertEqual(datos["estado"], "Activa")

        self.assertEqual(
            datos["aprendiz"]["documento"],
            987654321
        )

        self.assertEqual(
            datos["curso"]["codigo"],
            "CUR-001"
        )

    def test_inscripcion_location(self):

        respuesta = self.registrar_inscripcion()

        self.assertEqual(
            respuesta.encabezados["Location"],
            "/api/v1/inscripciones/INS-001"
        )

    def test_inscripcion_fecha(self):

        respuesta = self.registrar_inscripcion()

        self.assertEqual(
            respuesta.contenido["datos"]["fecha_inscripcion"],
            "2026-11-28"
        )

    def test_inscripcion_sin_fecha(self):

        from datetime import date

        datos = self.inscripcion.copy()

        del datos["fecha_inscripcion"]

        respuesta = self.solicitar(
            "POST", "/inscripciones", datos
        )

        self.verificar_respuesta(respuesta, 201)

        self.assertEqual(
            respuesta.contenido["datos"]["fecha_inscripcion"],
            date.today().isoformat()
        )

    def test_buscar_inscripcion(self):

        registrada = self.registrar_inscripcion()

        respuesta = self.solicitar(
            "GET", "/inscripciones/INS-001"
        )

        self.verificar_respuesta(respuesta, 200)

        self.assertEqual(
            respuesta.contenido["datos"],
            registrada.contenido["datos"]
        )

    def test_listar_inscripciones_registradas(self):

        registrada = self.registrar_inscripcion()

        respuesta = self.solicitar(
            "GET", "/inscripciones"
        )

        self.verificar_respuesta(respuesta, 200)

        self.assertEqual(
            respuesta.contenido["datos"],
            [registrada.contenido["datos"]]
        )

    def test_inscripcion_inexistente(self):

        with self.assertRaises(RecursoNoEncontrado):

            self.solicitar(
                "GET", "/inscripciones/INS-999"
            )

    def test_codigo_inscripcion_duplicado(self):

        self.registrar_inscripcion()

        with self.assertRaises(Conflicto):

            self.solicitar(
                "POST",
                "/inscripciones",
                self.inscripcion
            )

    def test_aprendiz_curso_duplicado(self):

        self.registrar_inscripcion()

        datos = {
            **self.inscripcion,
            "codigo": "INS-002"
        }

        with self.assertRaises(Conflicto):

            self.solicitar(
                "POST", "/inscripciones", datos
            )

    def test_inscribir_aprendiz_inexistente(self):

        datos = {
            **self.inscripcion,
            "documento_aprendiz": 999999999
        }

        with self.assertRaises(RecursoNoEncontrado):

            self.solicitar(
                "POST", "/inscripciones", datos
            )

    def test_inscribir_curso_inexistente(self):

        datos = {
            **self.inscripcion,
            "codigo_curso": "CUR-999"
        }

        with self.assertRaises(RecursoNoEncontrado):

            self.solicitar(
                "POST", "/inscripciones", datos
            )

    def test_inscripcion_campos_faltantes(self):

        campos = (
            "codigo",
            "documento_aprendiz",
            "codigo_curso"
        )

        for campo in campos:

            with self.subTest(campo=campo):

                datos = self.inscripcion.copy()

                del datos[campo]

                with self.assertRaises(DatosInvalidos):

                    self.solicitar(
                        "POST", "/inscripciones", datos
                    )

    def test_inscripcion_campos_desconocidos(self):

        datos = {
            **self.inscripcion,
            "extra": True
        }

        with self.assertRaises(DatosInvalidos):

            self.solicitar(
                "POST", "/inscripciones", datos
            )

    def test_inscripcion_datos_invalidos(self):

        valores = (
            ("codigo", ""),
            ("documento_aprendiz", 0),
            ("codigo_curso", ""),
            ("fecha_inscripcion", "28/11/2026")
        )

        for campo, valor in valores:

            with self.subTest(campo=campo):

                datos = {
                    **self.inscripcion,
                    campo: valor
                }

                with self.assertRaises(DatosInvalidos):

                    self.solicitar(
                        "POST", "/inscripciones", datos
                    )

    def test_cancelar_inscripcion(self):

        self.registrar_inscripcion()

        respuesta = self.solicitar(
            "PATCH",
            "/inscripciones/INS-001/estado",
            {"estado": "Cancelada"}
        )

        self.verificar_respuesta(respuesta, 200)

        self.assertEqual(
            respuesta.contenido["datos"]["estado"],
            "Cancelada"
        )

    def test_finalizar_inscripcion(self):

        self.registrar_inscripcion()

        self.registrar_calificaciones()

        respuesta = self.solicitar(
            "PATCH",
            "/inscripciones/INS-001/estado",
            {"estado": "Finalizada"}
        )

        self.verificar_respuesta(respuesta, 200)

        self.assertEqual(
            respuesta.contenido["datos"]["estado"],
            "Finalizada"
        )

    def test_cambiar_estado_invalido(self):

        self.registrar_inscripcion()

        for estado in ("Activa", "Pendiente", ""):

            with self.subTest(estado=estado):

                with self.assertRaises(DatosInvalidos):

                    self.solicitar(
                        "PATCH",
                        "/inscripciones/INS-001/estado",
                        {"estado": estado}
                    )

    def test_cambiar_estado_inscripcion_cancelada(self):

        self.registrar_inscripcion()

        respuesta = self.solicitar(
            "PATCH",
            "/inscripciones/INS-001/estado",
            {"estado": "Cancelada"}
        )

        self.verificar_respuesta(respuesta, 200)

        with self.assertRaises(Conflicto):

            self.solicitar(
                "PATCH",
                "/inscripciones/INS-001/estado",
                {"estado": "Finalizada"}
            )

    def test_consultar_calificaciones_vacias(self):

        self.registrar_inscripcion()

        respuesta = self.solicitar(
            "GET",
            "/inscripciones/INS-001/calificaciones"
        )

        self.verificar_respuesta(respuesta, 200)

        self.assertEqual(
            respuesta.contenido["datos"], []
        )

    def test_consultar_calificaciones_registradas(self):

        self.registrar_inscripcion()

        self.registrar_calificaciones()

        respuesta = self.solicitar(
            "GET",
            "/inscripciones/INS-001/calificaciones"
        )

        self.verificar_respuesta(respuesta, 200)

        datos = respuesta.contenido["datos"]

        self.assertEqual(len(datos), 3)

        self.assertEqual(
            sorted(nota["nota"] for nota in datos),
            [3.0, 4.0, 5.0]
        )

    def test_promedio_insuficientes_calificaciones(self):

        self.registrar_inscripcion()

        with self.assertRaises(DatosInvalidos):

            self.solicitar(
                "GET",
                "/inscripciones/INS-001/promedio"
            )

    def test_calcular_promedio(self):

        self.registrar_inscripcion()

        self.registrar_calificaciones()

        respuesta = self.solicitar(
            "GET",
            "/inscripciones/INS-001/promedio"
        )

        self.verificar_respuesta(respuesta, 200)

        self.assertEqual(
            respuesta.contenido["datos"]["promedio"],
            4.0
        )

    def test_rendimiento_pendiente(self):

        self.registrar_inscripcion()

        respuesta = self.solicitar(
            "GET",
            "/inscripciones/INS-001/rendimiento"
        )

        self.verificar_respuesta(respuesta, 200)

        datos = respuesta.contenido["datos"]

        self.assertEqual(datos["estado"], "Pendiente")
        self.assertIsNone(datos["promedio"])

    def test_rendimiento_aprobado(self):

        self.registrar_inscripcion()

        self.registrar_calificaciones()

        respuesta = self.solicitar(
            "GET",
            "/inscripciones/INS-001/rendimiento"
        )

        self.verificar_respuesta(respuesta, 200)

        datos = respuesta.contenido["datos"]

        self.assertEqual(datos["promedio"], 4.0)
        self.assertEqual(datos["estado"], "Aprobado")

    def test_relaciones_inscripcion_inexistente(self):

        relaciones = (
            "calificaciones",
            "rendimiento",
            "promedio"
        )

        for relacion in relaciones:

            with self.subTest(relacion=relacion):

                with self.assertRaises(RecursoNoEncontrado):

                    self.solicitar(
                        "GET",
                        f"/inscripciones/INS-999/{relacion}"
                    )


if __name__ == "__main__":

    unittest.main()