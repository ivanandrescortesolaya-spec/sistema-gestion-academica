import unittest

from tests.api_rest.test_servidor import (
    BasePruebasHTTP
)

from api.respuestas import respuesta_exitosa

from persistencia.excepciones import (
    ErrorConexion,
    ErrorIntegridad,
    ErrorOperacion
)


class TestErroresHTTP(BasePruebasHTTP):

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

    def verificar_error(self, respuesta, estado):

        datos = self.verificar_http(
            respuesta,
            estado,
            exito=False
        )

        self.assertIsNone(datos)

        self.assertTrue(
            respuesta[1]["mensaje"]
        )

    def registrar_profesor(self):

        respuesta = self.solicitar_http(
            "POST",
            "/profesores",
            self.profesor
        )

        self.verificar_http(respuesta, 201)

    def preparar_inscripcion(self):

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

            respuesta = self.solicitar_http(
                "POST", ruta, datos
            )

            self.verificar_http(respuesta, 201)

    def registrar_error_simulado(self, error):

        def controlador(parametros, datos):

            raise error

        self.enrutador.registrar(
            "GET",
            "/api/v1/error-simulado",
            controlador
        )

    # HTTP 400

    def test_json_mal_formado(self):

        respuesta = self.solicitar_http(
            "POST",
            "/profesores",
            cuerpo=b'{"nombre":'
        )

        self.verificar_error(respuesta, 400)

    def test_json_lista(self):

        respuesta = self.solicitar_http(
            "POST",
            "/profesores",
            cuerpo=b'["Python", "Java"]'
        )

        self.verificar_error(respuesta, 400)

    def test_json_nulo(self):

        respuesta = self.solicitar_http(
            "POST",
            "/profesores",
            cuerpo=b"null"
        )

        self.verificar_error(respuesta, 400)

    def test_json_valor_escalar(self):

        for cuerpo in (
            b"123",
            b"true",
            b'"Python"'
        ):

            with self.subTest(cuerpo=cuerpo):

                respuesta = self.solicitar_http(
                    "POST",
                    "/profesores",
                    cuerpo=cuerpo
                )

                self.verificar_error(
                    respuesta, 400
                )

    def test_json_campos_duplicados(self):

        respuesta = self.solicitar_http(
            "POST",
            "/profesores",
            cuerpo=(
                b'{"nombre":"Uno",'
                b'"nombre":"Dos"}'
            )
        )

        self.verificar_error(respuesta, 400)

    def test_json_constantes_no_permitidas(self):

        valores = (
            b'{"nota":NaN}',
            b'{"nota":Infinity}',
            b'{"nota":-Infinity}'
        )

        for cuerpo in valores:

            with self.subTest(cuerpo=cuerpo):

                respuesta = self.solicitar_http(
                    "POST",
                    "/calificaciones",
                    cuerpo=cuerpo
                )

                self.verificar_error(
                    respuesta, 400
                )

    def test_json_utf8_invalido(self):

        respuesta = self.solicitar_http(
            "POST",
            "/profesores",
            cuerpo=b'{"nombre":"\xff"}'
        )

        self.verificar_error(respuesta, 400)

    def test_solicitud_post_sin_cuerpo(self):

        respuesta = self.solicitar_http(
            "POST",
            "/profesores"
        )

        self.verificar_error(respuesta, 400)

    def test_solicitud_put_sin_cuerpo(self):

        respuesta = self.solicitar_http(
            "PUT",
            "/cursos/CUR-001/profesor"
        )

        self.verificar_error(respuesta, 400)

    def test_solicitud_patch_sin_cuerpo(self):

        respuesta = self.solicitar_http(
            "PATCH",
            "/calificaciones/NOT-001"
        )

        self.verificar_error(respuesta, 400)

    def test_solicitud_get_con_cuerpo(self):

        respuesta = self.solicitar_http(
            "GET",
            "/profesores",
            datos={"nombre": "Python"}
        )

        self.verificar_error(respuesta, 400)

    # HTTP 404

    def test_ruta_inexistente(self):

        respuesta = self.solicitar_http(
            "GET",
            "/ruta-inexistente"
        )

        self.verificar_error(respuesta, 404)

    def test_recursos_inexistentes(self):

        rutas = (
            "/profesores/999999999",
            "/aprendices/999999999",
            "/cursos/CUR-999",
            "/inscripciones/INS-999",
            "/calificaciones/NOT-999"
        )

        for ruta in rutas:

            with self.subTest(ruta=ruta):

                respuesta = self.solicitar_http(
                    "GET", ruta
                )

                self.verificar_error(
                    respuesta, 404
                )

    # HTTP 405

    def test_metodo_no_permitido(self):

        respuesta = self.solicitar_http(
            "DELETE",
            "/profesores"
        )

        self.verificar_error(respuesta, 405)

    def test_encabezado_allow(self):

        respuesta = self.solicitar_http(
            "DELETE",
            "/profesores"
        )

        self.verificar_error(respuesta, 405)

        metodos = {
            metodo.strip()
            for metodo
            in respuesta[2]["allow"].split(",")
        }

        self.assertEqual(
            metodos,
            {"GET", "POST"}
        )

    def test_metodo_options_no_permitido(self):

        respuesta = self.solicitar_http(
            "OPTIONS",
            "/profesores"
        )

        self.verificar_error(respuesta, 405)

    def test_metodo_head_sin_cuerpo(self):

        respuesta = self.solicitar_http(
            "HEAD",
            "/profesores"
        )

        self.assertEqual(
            respuesta[0],
            405
        )

        self.assertIsNone(respuesta[1])

        self.assertIn(
            "allow",
            respuesta[2]
        )

    # HTTP 409

    def test_profesor_duplicado(self):

        self.registrar_profesor()

        respuesta = self.solicitar_http(
            "POST",
            "/profesores",
            self.profesor
        )

        self.verificar_error(respuesta, 409)

    def test_inscripcion_duplicada(self):

        self.preparar_inscripcion()

        respuesta = self.solicitar_http(
            "POST",
            "/inscripciones",
            {
                "codigo": "INS-002",
                "documento_aprendiz": 987654321,
                "codigo_curso": "CUR-001"
            }
        )

        self.verificar_error(respuesta, 409)

    def test_calificacion_inscripcion_cancelada(self):

        self.preparar_inscripcion()

        respuesta = self.solicitar_http(
            "PATCH",
            "/inscripciones/INS-001/estado",
            {"estado": "Cancelada"}
        )

        self.verificar_http(respuesta, 200)

        respuesta = self.solicitar_http(
            "POST",
            "/calificaciones",
            {
                "codigo": "NOT-001",
                "codigo_inscripcion": "INS-001",
                "nota": 4.0
            }
        )

        self.verificar_error(respuesta, 409)

    def test_error_integridad_simulado(self):

        self.registrar_error_simulado(
            ErrorIntegridad(
                "Detalle interno de integridad"
            )
        )

        respuesta = self.solicitar_http(
            "GET",
            "/error-simulado"
        )

        self.verificar_error(respuesta, 409)

        self.assertNotIn(
            "Detalle interno de integridad",
            respuesta[1]["mensaje"]
        )

    # HTTP 413

    def test_contenido_demasiado_grande(self):

        cuerpo = b"x" * (1024 * 1024 + 1)

        respuesta = self.solicitar_http(
            "POST",
            "/profesores",
            cuerpo=cuerpo
        )

        self.verificar_error(respuesta, 413)

    # HTTP 415

    def test_formato_texto_no_permitido(self):

        respuesta = self.solicitar_http(
            "POST",
            "/profesores",
            cuerpo=b"Texto de prueba",
            encabezados={
                "Content-Type": "text/plain"
            }
        )

        self.verificar_error(respuesta, 415)

    def test_formato_xml_no_permitido(self):

        respuesta = self.solicitar_http(
            "POST",
            "/profesores",
            cuerpo=b"<profesor>Prueba</profesor>",
            encabezados={
                "Content-Type": "application/xml"
            }
        )

        self.verificar_error(respuesta, 415)

    # HTTP 422

    def test_campos_obligatorios_faltantes(self):

        respuesta = self.solicitar_http(
            "POST",
            "/profesores",
            {"nombre": "Profesor"}
        )

        self.verificar_error(respuesta, 422)

    def test_campos_desconocidos(self):

        respuesta = self.solicitar_http(
            "POST",
            "/profesores",
            {
                **self.profesor,
                "extra": True
            }
        )

        self.verificar_error(respuesta, 422)

    def test_documento_invalido(self):

        respuesta = self.solicitar_http(
            "GET",
            "/profesores/ABC"
        )

        self.verificar_error(respuesta, 422)

    def test_calificacion_fuera_rango(self):

        self.preparar_inscripcion()

        respuesta = self.solicitar_http(
            "POST",
            "/calificaciones",
            {
                "codigo": "NOT-001",
                "codigo_inscripcion": "INS-001",
                "nota": 6.0
            }
        )

        self.verificar_error(respuesta, 422)

    def test_promedio_sin_calificaciones(self):

        self.preparar_inscripcion()

        respuesta = self.solicitar_http(
            "GET",
            "/inscripciones/INS-001/promedio"
        )

        self.verificar_error(respuesta, 422)

    # HTTP 500

    def test_error_interno_simulado(self):

        self.registrar_error_simulado(
            RuntimeError(
                "Detalle interno reservado"
            )
        )

        respuesta = self.solicitar_http(
            "GET",
            "/error-simulado"
        )

        self.verificar_error(respuesta, 500)

        self.assertNotIn(
            "Detalle interno reservado",
            respuesta[1]["mensaje"]
        )

    def test_error_persistencia_simulado(self):

        self.registrar_error_simulado(
            ErrorOperacion(
                "Detalle SQL reservado"
            )
        )

        respuesta = self.solicitar_http(
            "GET",
            "/error-simulado"
        )

        self.verificar_error(respuesta, 500)

        self.assertNotIn(
            "Detalle SQL reservado",
            respuesta[1]["mensaje"]
        )

    def test_error_serializacion_json(self):

        def controlador(parametros, datos):

            return respuesta_exitosa(
                {"objeto": object()}
            )

        self.enrutador.registrar(
            "GET",
            "/api/v1/error-serializacion",
            controlador
        )

        respuesta = self.solicitar_http(
            "GET",
            "/error-serializacion"
        )

        self.verificar_error(respuesta, 500)

    # HTTP 503

    def test_servicio_no_disponible(self):

        self.registrar_error_simulado(
            ErrorConexion(
                "Detalle de conexión reservado"
            )
        )

        respuesta = self.solicitar_http(
            "GET",
            "/error-simulado"
        )

        self.verificar_error(respuesta, 503)

        self.assertNotIn(
            "Detalle de conexión reservado",
            respuesta[1]["mensaje"]
        )

    # HTTP 408

    def test_tiempo_espera_agotado_simulado(self):

        self.registrar_error_simulado(
            TimeoutError(
                "Tiempo de espera agotado"
            )
        )

        respuesta = self.solicitar_http(
            "GET",
            "/error-simulado"
        )

        self.verificar_error(respuesta, 408)

    # Recuperación del servidor

    def test_servidor_continua_despues_error(self):

        self.registrar_error_simulado(
            RuntimeError("Error simulado")
        )

        respuesta = self.solicitar_http(
            "GET",
            "/error-simulado"
        )

        self.verificar_error(respuesta, 500)

        respuesta = self.solicitar_http(
            "GET",
            "/salud"
        )

        self.verificar_http(respuesta, 200)

    def test_error_no_registra_profesor(self):

        respuesta = self.solicitar_http(
            "POST",
            "/profesores",
            {"nombre": "Incompleto"}
        )

        self.verificar_error(respuesta, 422)

        respuesta = self.solicitar_http(
            "GET",
            "/profesores"
        )

        datos = self.verificar_http(
            respuesta, 200
        )

        self.assertEqual(datos, [])


if __name__ == "__main__":

    unittest.main()