import json
import unittest

from threading import Thread
from urllib.request import Request, urlopen
from urllib.error import HTTPError

from tests.api_rest import BasePruebasAPI
from api.servidor import crear_servidor


class BasePruebasHTTP(BasePruebasAPI):

    def setUp(self):

        super().setUp()

        self.servidor = crear_servidor(
            self.enrutador,
            puerto=0
        )

        self.hilo = Thread(
            target=self.servidor.serve_forever,
            kwargs={"poll_interval": 0.01},
            daemon=True
        )

        self.hilo.start()

        self.addCleanup(self.detener_servidor)

        puerto = self.servidor.server_address[1]

        self.url_base = (
            f"http://127.0.0.1:{puerto}/api/v1"
        )

    def detener_servidor(self):

        self.servidor.shutdown()

        self.servidor.server_close()

        self.hilo.join(timeout=5)

    def solicitar_http(
        self,
        metodo,
        ruta,
        datos=None,
        cuerpo=None,
        encabezados=None
    ):

        cabeceras = {
            "Accept": "application/json"
        }

        if datos is not None:

            cuerpo = json.dumps(
                datos,
                ensure_ascii=False
            ).encode("utf-8")

        if cuerpo is not None:

            cabeceras["Content-Type"] = (
                "application/json"
            )

        if encabezados:

            cabeceras.update(encabezados)

        solicitud = Request(
            url=f"{self.url_base}{ruta}",
            data=cuerpo,
            headers=cabeceras,
            method=metodo
        )

        try:

            with urlopen(
                solicitud,
                timeout=5
            ) as respuesta:

                return self.procesar_respuesta_http(
                    respuesta
                )

        except HTTPError as error:

            with error:

                return self.procesar_respuesta_http(
                    error
                )

    def procesar_respuesta_http(self, respuesta):

        cuerpo = respuesta.read()

        contenido = (
            json.loads(cuerpo.decode("utf-8"))
            if cuerpo
            else None
        )

        encabezados = {
            clave.lower(): valor
            for clave, valor
            in respuesta.headers.items()
        }

        return (
            respuesta.code,
            contenido,
            encabezados
        )

    def verificar_http(
        self,
        respuesta,
        estado,
        exito=True
    ):

        codigo, contenido, encabezados = respuesta

        self.assertEqual(codigo, estado)

        self.assertIsInstance(contenido, dict)

        self.assertEqual(
            contenido["exito"],
            exito
        )

        self.assertIn("mensaje", contenido)

        self.assertIn("datos", contenido)

        self.assertIn(
            "application/json",
            encabezados["content-type"]
        )

        return contenido["datos"]


class TestServidorHTTP(BasePruebasHTTP):

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
            "descripcion": "Curso de prueba",
            "duracion_horas": 48,
            "modalidad": "complementaria"
        }

    def registrar_profesor(self):

        respuesta = self.solicitar_http(
            "POST",
            "/profesores",
            self.profesor
        )

        self.verificar_http(respuesta, 201)

        return respuesta

    def preparar_inscripcion(self):

        registros = (
            ("/profesores", self.profesor),
            ("/aprendices", self.aprendiz),
            ("/cursos", self.curso),
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

    def registrar_calificaciones(self):

        for numero, nota in enumerate(
            (3.0, 4.0, 5.0),
            start=1
        ):

            respuesta = self.solicitar_http(
                "POST",
                "/calificaciones",
                {
                    "codigo": f"NOT-00{numero}",
                    "codigo_inscripcion": "INS-001",
                    "nota": nota
                }
            )

            self.verificar_http(respuesta, 201)

    def test_servidor_operativo(self):

        respuesta = self.solicitar_http(
            "GET", "/salud"
        )

        datos = self.verificar_http(
            respuesta, 200
        )

        self.assertEqual(
            datos["estado"],
            "operativo"
        )

    def test_version_api(self):

        respuesta = self.solicitar_http(
            "GET", "/salud"
        )

        datos = self.verificar_http(
            respuesta, 200
        )

        self.assertEqual(datos["version"], "v1")

    def test_cantidad_endpoints(self):

        self.assertEqual(
            self.enrutador.cantidad_rutas,
            34
        )

    def test_content_type_json(self):

        respuesta = self.solicitar_http(
            "GET", "/salud"
        )

        self.assertIn(
            "application/json",
            respuesta[2]["content-type"]
        )

    def test_codificacion_utf8(self):

        respuesta = self.solicitar_http(
            "GET", "/salud"
        )

        self.assertIn(
            "utf-8",
            respuesta[2]["content-type"].lower()
        )

    def test_content_length(self):

        solicitud = Request(
            f"{self.url_base}/salud"
        )

        with urlopen(
            solicitud,
            timeout=5
        ) as respuesta:

            cuerpo = respuesta.read()

            longitud = int(
                respuesta.headers["Content-Length"]
            )

            self.assertEqual(
                longitud,
                len(cuerpo)
            )

    def test_cache_control(self):

        respuesta = self.solicitar_http(
            "GET", "/salud"
        )

        self.assertEqual(
            respuesta[2]["cache-control"],
            "no-store"
        )

    def test_encabezado_nosniff(self):

        respuesta = self.solicitar_http(
            "GET", "/salud"
        )

        self.assertEqual(
            respuesta[2]["x-content-type-options"],
            "nosniff"
        )

    def test_connection_close(self):

        respuesta = self.solicitar_http(
            "GET", "/salud"
        )

        self.assertEqual(
            respuesta[2]["connection"].lower(),
            "close"
        )

    def test_listar_profesores_http(self):

        respuesta = self.solicitar_http(
            "GET", "/profesores"
        )

        datos = self.verificar_http(
            respuesta, 200
        )

        self.assertEqual(datos, [])

    def test_registrar_profesor_http(self):

        respuesta = self.registrar_profesor()

        self.assertEqual(
            respuesta[1]["datos"],
            self.profesor
        )

    def test_location_profesor_http(self):

        respuesta = self.registrar_profesor()

        self.assertEqual(
            respuesta[2]["location"],
            "/api/v1/profesores/123456789"
        )

    def test_buscar_profesor_http(self):

        self.registrar_profesor()

        respuesta = self.solicitar_http(
            "GET", "/profesores/123456789"
        )

        datos = self.verificar_http(
            respuesta, 200
        )

        self.assertEqual(
            datos,
            self.profesor
        )

    def test_registrar_aprendiz_http(self):

        respuesta = self.solicitar_http(
            "POST",
            "/aprendices",
            self.aprendiz
        )

        datos = self.verificar_http(
            respuesta, 201
        )

        self.assertEqual(
            datos,
            self.aprendiz
        )

    def test_registrar_curso_http(self):

        respuesta = self.solicitar_http(
            "POST",
            "/cursos",
            self.curso
        )

        datos = self.verificar_http(
            respuesta, 201
        )

        self.assertEqual(
            datos["codigo"],
            "CUR-001"
        )

        self.assertIsNone(datos["profesor"])

    def test_asignar_profesor_http_put(self):

        self.preparar_inscripcion()

        respuesta = self.solicitar_http(
            "PUT",
            "/cursos/CUR-001/profesor",
            {"documento": 123456789}
        )

        datos = self.verificar_http(
            respuesta, 200
        )

        self.assertEqual(
            datos["profesor"],
            self.profesor
        )

    def test_registrar_inscripcion_http(self):

        self.preparar_inscripcion()

        respuesta = self.solicitar_http(
            "GET",
            "/inscripciones/INS-001"
        )

        datos = self.verificar_http(
            respuesta, 200
        )

        self.assertEqual(
            datos["estado"],
            "Activa"
        )

    def test_registrar_calificaciones_http(self):

        self.preparar_inscripcion()

        self.registrar_calificaciones()

        respuesta = self.solicitar_http(
            "GET",
            "/calificaciones"
        )

        datos = self.verificar_http(
            respuesta, 200
        )

        self.assertEqual(len(datos), 3)

    def test_consultar_promedio_http(self):

        self.preparar_inscripcion()

        self.registrar_calificaciones()

        respuesta = self.solicitar_http(
            "GET",
            "/inscripciones/INS-001/promedio"
        )

        datos = self.verificar_http(
            respuesta, 200
        )

        self.assertEqual(
            datos["promedio"],
            4.0
        )

    def test_modificar_calificacion_http_patch(self):

        self.preparar_inscripcion()

        self.registrar_calificaciones()

        respuesta = self.solicitar_http(
            "PATCH",
            "/calificaciones/NOT-001",
            {"nota": 4.0}
        )

        datos = self.verificar_http(
            respuesta, 200
        )

        self.assertEqual(datos["nota"], 4.0)

    def test_recalcular_promedio_http(self):

        self.preparar_inscripcion()

        self.registrar_calificaciones()

        respuesta = self.solicitar_http(
            "PATCH",
            "/calificaciones/NOT-001",
            {"nota": 4.0}
        )

        self.verificar_http(respuesta, 200)

        respuesta = self.solicitar_http(
            "GET",
            "/inscripciones/INS-001/promedio"
        )

        datos = self.verificar_http(
            respuesta, 200
        )

        self.assertEqual(
            datos["promedio"],
            4.33
        )

    def test_finalizar_inscripcion_http(self):

        self.preparar_inscripcion()

        self.registrar_calificaciones()

        respuesta = self.solicitar_http(
            "PATCH",
            "/inscripciones/INS-001/estado",
            {"estado": "Finalizada"}
        )

        datos = self.verificar_http(
            respuesta, 200
        )

        self.assertEqual(
            datos["estado"],
            "Finalizada"
        )

    def test_resumen_academico_http(self):

        self.preparar_inscripcion()

        self.registrar_calificaciones()

        respuesta = self.solicitar_http(
            "GET",
            "/reportes/resumen"
        )

        datos = self.verificar_http(
            respuesta, 200
        )

        self.assertEqual(
            datos,
            {
                "profesores": 1,
                "aprendices": 1,
                "cursos": 1,
                "inscripciones": 1,
                "calificaciones": 3
            }
        )

    def test_reporte_calificaciones_http(self):

        self.preparar_inscripcion()

        self.registrar_calificaciones()

        respuesta = self.solicitar_http(
            "GET",
            "/reportes/calificaciones"
        )

        datos = self.verificar_http(
            respuesta, 200
        )

        self.assertIsInstance(
            datos["reporte"],
            str
        )

        self.assertTrue(
            datos["reporte"].strip()
        )

    def test_ruta_con_barra_final_http(self):

        respuesta = self.solicitar_http(
            "GET", "/salud/"
        )

        self.verificar_http(respuesta, 200)

    def test_ruta_con_consulta_http(self):

        respuesta = self.solicitar_http(
            "GET", "/profesores?pagina=1"
        )

        self.verificar_http(respuesta, 200)


if __name__ == "__main__":

    unittest.main()