import unittest

from tests.api_rest import BasePruebasAPI

from api.excepciones import (
    DatosInvalidos,
    Conflicto,
    RecursoNoEncontrado
)


class TestCalificacionesAPI(BasePruebasAPI):

    def setUp(self):

        super().setUp()

        registros = (
            (
                "/aprendices",
                {
                    "nombre": "Aprendiz Prueba",
                    "documento": 987654321,
                    "edad": 22,
                    "telefono": "3001234567",
                    "correo": "aprendiz@example.com",
                    "direccion": "Dirección de prueba"
                }
            ),
            (
                "/cursos",
                {
                    "codigo": "CUR-001",
                    "nombre": "Python",
                    "descripcion": "Curso de prueba",
                    "duracion_horas": 48,
                    "modalidad": "complementaria"
                }
            ),
            (
                "/inscripciones",
                {
                    "codigo": "INS-001",
                    "documento_aprendiz": 987654321,
                    "codigo_curso": "CUR-001"
                }
            )
        )

        for ruta, datos in registros:

            respuesta = self.solicitar(
                "POST", ruta, datos
            )

            self.verificar_respuesta(respuesta, 201)

        self.calificacion = {
            "codigo": "NOT-001",
            "codigo_inscripcion": "INS-001",
            "nota": 4.5,
            "fecha": "2026-11-28"
        }

    def registrar_calificacion(self):

        respuesta = self.solicitar(
            "POST",
            "/calificaciones",
            self.calificacion
        )

        self.verificar_respuesta(respuesta, 201)

        return respuesta

    def registrar_tres_notas(
        self,
        notas=(3.0, 4.0, 5.0)
    ):

        for numero, nota in enumerate(notas, start=1):

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

    def cambiar_estado(self, estado):

        respuesta = self.solicitar(
            "PATCH",
            "/inscripciones/INS-001/estado",
            {"estado": estado}
        )

        self.verificar_respuesta(respuesta, 200)

    def test_listar_calificaciones_vacias(self):

        respuesta = self.solicitar(
            "GET", "/calificaciones"
        )

        self.verificar_respuesta(respuesta, 200)

        self.assertEqual(
            respuesta.contenido["datos"], []
        )

    def test_registrar_calificacion(self):

        respuesta = self.registrar_calificacion()

        datos = respuesta.contenido["datos"]

        self.assertEqual(datos["codigo"], "NOT-001")
        self.assertEqual(datos["nota"], 4.5)

        self.assertEqual(
            datos["inscripcion"]["codigo"],
            "INS-001"
        )

    def test_calificacion_location(self):

        respuesta = self.registrar_calificacion()

        self.assertEqual(
            respuesta.encabezados["Location"],
            "/api/v1/calificaciones/NOT-001"
        )

    def test_calificacion_fecha(self):

        respuesta = self.registrar_calificacion()

        self.assertEqual(
            respuesta.contenido["datos"]["fecha"],
            "2026-11-28"
        )

    def test_calificacion_sin_fecha(self):

        from datetime import date

        datos = self.calificacion.copy()

        del datos["fecha"]

        respuesta = self.solicitar(
            "POST", "/calificaciones", datos
        )

        self.verificar_respuesta(respuesta, 201)

        self.assertEqual(
            respuesta.contenido["datos"]["fecha"],
            date.today().isoformat()
        )

    def test_buscar_calificacion(self):

        registrada = self.registrar_calificacion()

        respuesta = self.solicitar(
            "GET", "/calificaciones/NOT-001"
        )

        self.verificar_respuesta(respuesta, 200)

        self.assertEqual(
            respuesta.contenido["datos"],
            registrada.contenido["datos"]
        )

    def test_listar_calificaciones_registradas(self):

        registrada = self.registrar_calificacion()

        respuesta = self.solicitar(
            "GET", "/calificaciones"
        )

        self.verificar_respuesta(respuesta, 200)

        self.assertEqual(
            respuesta.contenido["datos"],
            [registrada.contenido["datos"]]
        )

    def test_calificacion_inexistente(self):

        with self.assertRaises(RecursoNoEncontrado):

            self.solicitar(
                "GET", "/calificaciones/NOT-999"
            )

    def test_calificacion_duplicada(self):

        self.registrar_calificacion()

        with self.assertRaises(Conflicto):

            self.solicitar(
                "POST",
                "/calificaciones",
                self.calificacion
            )

    def test_calificacion_inscripcion_inexistente(self):

        datos = {
            **self.calificacion,
            "codigo_inscripcion": "INS-999"
        }

        with self.assertRaises(RecursoNoEncontrado):

            self.solicitar(
                "POST", "/calificaciones", datos
            )

    def test_calificacion_campos_faltantes(self):

        campos = (
            "codigo",
            "codigo_inscripcion",
            "nota"
        )

        for campo in campos:

            with self.subTest(campo=campo):

                datos = self.calificacion.copy()

                del datos[campo]

                with self.assertRaises(DatosInvalidos):

                    self.solicitar(
                        "POST", "/calificaciones", datos
                    )

    def test_calificacion_campos_desconocidos(self):

        datos = {
            **self.calificacion,
            "extra": True
        }

        with self.assertRaises(DatosInvalidos):

            self.solicitar(
                "POST", "/calificaciones", datos
            )

    def test_calificacion_datos_invalidos(self):

        valores = (
            ("codigo", ""),
            ("codigo_inscripcion", ""),
            ("nota", -1),
            ("nota", 5.01),
            ("nota", 4.123),
            ("nota", True),
            ("nota", "4.5"),
            ("fecha", "2026-02-30")
        )

        for campo, valor in valores:

            with self.subTest(campo=campo):

                datos = {
                    **self.calificacion,
                    campo: valor
                }

                with self.assertRaises(DatosInvalidos):

                    self.solicitar(
                        "POST", "/calificaciones", datos
                    )

    def test_calificaciones_limites_validos(self):

        for numero, nota in enumerate(
            (0.0, 5.0),
            start=1
        ):

            with self.subTest(nota=nota):

                datos = {
                    **self.calificacion,
                    "codigo": f"LIM-{numero}",
                    "nota": nota
                }

                respuesta = self.solicitar(
                    "POST", "/calificaciones", datos
                )

                self.verificar_respuesta(respuesta, 201)

                self.assertEqual(
                    respuesta.contenido["datos"]["nota"],
                    nota
                )

    def test_modificar_calificacion(self):

        self.registrar_calificacion()

        respuesta = self.solicitar(
            "PATCH",
            "/calificaciones/NOT-001",
            {"nota": 5.0}
        )

        self.verificar_respuesta(respuesta, 200)

        self.assertEqual(
            respuesta.contenido["datos"]["nota"],
            5.0
        )

    def test_consultar_calificacion_modificada(self):

        self.registrar_calificacion()

        respuesta = self.solicitar(
            "PATCH",
            "/calificaciones/NOT-001",
            {"nota": 3.5}
        )

        self.verificar_respuesta(respuesta, 200)

        respuesta = self.solicitar(
            "GET", "/calificaciones/NOT-001"
        )

        self.verificar_respuesta(respuesta, 200)

        self.assertEqual(
            respuesta.contenido["datos"]["nota"],
            3.5
        )

    def test_modificar_calificacion_inexistente(self):

        with self.assertRaises(RecursoNoEncontrado):

            self.solicitar(
                "PATCH",
                "/calificaciones/NOT-999",
                {"nota": 4.0}
            )

    def test_modificar_calificacion_invalida(self):

        self.registrar_calificacion()

        valores = (
            {},
            {"nota": -1},
            {"nota": 6},
            {"nota": True},
            {"nota": 4.123},
            {"nota": 4, "extra": True}
        )

        for datos in valores:

            with self.subTest(datos=datos):

                with self.assertRaises(DatosInvalidos):

                    self.solicitar(
                        "PATCH",
                        "/calificaciones/NOT-001",
                        datos
                    )

    def test_registrar_nota_inscripcion_cancelada(self):

        self.cambiar_estado("Cancelada")

        with self.assertRaises(Conflicto):

            self.solicitar(
                "POST",
                "/calificaciones",
                self.calificacion
            )

    def test_registrar_nota_inscripcion_finalizada(self):

        self.registrar_tres_notas()

        self.cambiar_estado("Finalizada")

        datos = {
            **self.calificacion,
            "codigo": "NOT-004"
        }

        with self.assertRaises(Conflicto):

            self.solicitar(
                "POST", "/calificaciones", datos
            )

    def test_modificar_nota_inscripcion_cancelada(self):

        self.registrar_calificacion()

        self.cambiar_estado("Cancelada")

        with self.assertRaises(Conflicto):

            self.solicitar(
                "PATCH",
                "/calificaciones/NOT-001",
                {"nota": 5.0}
            )

    def test_modificar_nota_inscripcion_finalizada(self):

        self.registrar_tres_notas()

        self.cambiar_estado("Finalizada")

        with self.assertRaises(Conflicto):

            self.solicitar(
                "PATCH",
                "/calificaciones/NOT-001",
                {"nota": 5.0}
            )

    def test_recalcular_promedio(self):

        self.registrar_tres_notas()

        respuesta = self.solicitar(
            "PATCH",
            "/calificaciones/NOT-001",
            {"nota": 4.0}
        )

        self.verificar_respuesta(respuesta, 200)

        respuesta = self.solicitar(
            "GET",
            "/inscripciones/INS-001/promedio"
        )

        self.verificar_respuesta(respuesta, 200)

        self.assertEqual(
            respuesta.contenido["datos"]["promedio"],
            4.33
        )

    def test_rendimiento_reprobado(self):

        self.registrar_tres_notas(
            (1.0, 2.0, 3.0)
        )

        respuesta = self.solicitar(
            "GET",
            "/inscripciones/INS-001/rendimiento"
        )

        self.verificar_respuesta(respuesta, 200)

        datos = respuesta.contenido["datos"]

        self.assertEqual(datos["promedio"], 2.0)
        self.assertEqual(datos["estado"], "Reprobado")

    def test_aprobacion_nota_minima(self):

        self.registrar_tres_notas(
            (3.0, 3.0, 3.0)
        )

        respuesta = self.solicitar(
            "GET",
            "/inscripciones/INS-001/rendimiento"
        )

        self.verificar_respuesta(respuesta, 200)

        datos = respuesta.contenido["datos"]

        self.assertEqual(datos["promedio"], 3.0)
        self.assertEqual(datos["estado"], "Aprobado")

    def test_consultar_calificaciones_aprendiz(self):

        self.registrar_tres_notas()

        respuesta = self.solicitar(
            "GET",
            "/aprendices/987654321/calificaciones"
        )

        self.verificar_respuesta(respuesta, 200)

        self.assertEqual(
            len(respuesta.contenido["datos"]), 3
        )

    def test_consultar_calificaciones_curso(self):

        self.registrar_tres_notas()

        respuesta = self.solicitar(
            "GET",
            "/cursos/CUR-001/calificaciones"
        )

        self.verificar_respuesta(respuesta, 200)

        self.assertEqual(
            len(respuesta.contenido["datos"]), 3
        )

    def test_modificacion_invalida_conserva_nota(self):

        self.registrar_calificacion()

        with self.assertRaises(DatosInvalidos):

            self.solicitar(
                "PATCH",
                "/calificaciones/NOT-001",
                {"nota": 10}
            )

        respuesta = self.solicitar(
            "GET", "/calificaciones/NOT-001"
        )

        self.verificar_respuesta(respuesta, 200)

        self.assertEqual(
            respuesta.contenido["datos"]["nota"],
            4.5
        )


if __name__ == "__main__":

    unittest.main()