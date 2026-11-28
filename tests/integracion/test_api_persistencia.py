
from threading import Thread

from tests.integracion.test_api_mysql import (
    BaseIntegracionAPI
)

from persistencia.fabrica import crear_sistema_mysql

from api.rutas import crear_enrutador
from api.servidor import crear_servidor


class TestAPIPersistencia(BaseIntegracionAPI):

    def reiniciar_servidor(self):

        self.detener_servidor()

        self.sistema = crear_sistema_mysql(
            pruebas=True
        )

        self.enrutador = crear_enrutador(
            self.sistema
        )

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

        puerto = self.servidor.server_address[1]

        self.url_base = (
            f"http://127.0.0.1:{puerto}/api/v1"
        )

    def test_profesor_persistente(self):

        anterior = self.registrar_profesor_api()

        self.reiniciar_servidor()

        respuesta = self.solicitar_http(
            "GET",
            f"/profesores/{self.doc_profesor}"
        )

        actual = self.verificar_http(
            respuesta,
            200
        )

        self.assertEqual(actual, anterior)

    def test_aprendiz_persistente(self):

        anterior = self.registrar_aprendiz_api()

        self.reiniciar_servidor()

        respuesta = self.solicitar_http(
            "GET",
            f"/aprendices/{self.doc_aprendiz}"
        )

        actual = self.verificar_http(
            respuesta,
            200
        )

        self.assertEqual(actual, anterior)

    def test_curso_persistente(self):

        anterior = self.registrar_curso_api()

        self.reiniciar_servidor()

        respuesta = self.solicitar_http(
            "GET",
            f"/cursos/{self.codigo_curso}"
        )

        actual = self.verificar_http(
            respuesta,
            200
        )

        self.assertEqual(actual, anterior)

    def test_asignacion_profesor_persistente(self):

        self.registrar_profesor_api()

        self.registrar_curso_api()

        self.asignar_profesor_api()

        self.reiniciar_servidor()

        respuesta = self.solicitar_http(
            "GET",
            f"/cursos/{self.codigo_curso}"
        )

        datos = self.verificar_http(
            respuesta,
            200
        )

        self.assertEqual(
            datos["profesor"]["documento"],
            self.doc_profesor
        )

    def test_inscripcion_persistente(self):

        self.preparar_inscripcion_api()

        self.reiniciar_servidor()

        respuesta = self.solicitar_http(
            "GET",
            f"/inscripciones/{self.codigo_inscripcion}"
        )

        datos = self.verificar_http(
            respuesta,
            200
        )

        self.assertEqual(
            datos["codigo"],
            self.codigo_inscripcion
        )

        self.assertEqual(
            datos["aprendiz"]["documento"],
            self.doc_aprendiz
        )

        self.assertEqual(
            datos["curso"]["codigo"],
            self.codigo_curso
        )

        self.assertEqual(
            datos["fecha_inscripcion"],
            self.fecha.isoformat()
        )

    def test_calificaciones_persistentes(self):

        self.preparar_calificaciones_api()

        self.reiniciar_servidor()

        respuesta = self.solicitar_http(
            "GET",
            f"/inscripciones/{self.codigo_inscripcion}/calificaciones"
        )

        datos = self.verificar_http(
            respuesta,
            200
        )

        self.assertEqual(len(datos), 3)

        self.assertEqual(
            sorted(nota["nota"] for nota in datos),
            [3.0, 4.0, 5.0]
        )

        self.assertEqual(
            sorted(nota["codigo"] for nota in datos),
            sorted(self.notas_creadas)
        )

    def test_modificacion_nota_persistente(self):

        self.preparar_calificaciones_api()

        codigo = self.notas_creadas[0]

        respuesta = self.solicitar_http(
            "PATCH",
            f"/calificaciones/{codigo}",
            {"nota": 4.5}
        )

        self.verificar_http(respuesta, 200)

        self.reiniciar_servidor()

        respuesta = self.solicitar_http(
            "GET",
            f"/calificaciones/{codigo}"
        )

        datos = self.verificar_http(
            respuesta,
            200
        )

        self.assertEqual(datos["nota"], 4.5)

    def test_promedio_persistente(self):

        self.preparar_calificaciones_api()

        respuesta = self.solicitar_http(
            "GET",
            f"/inscripciones/{self.codigo_inscripcion}/promedio"
        )

        anterior = self.verificar_http(
            respuesta,
            200
        )

        self.reiniciar_servidor()

        respuesta = self.solicitar_http(
            "GET",
            f"/inscripciones/{self.codigo_inscripcion}/promedio"
        )

        actual = self.verificar_http(
            respuesta,
            200
        )

        self.assertEqual(actual, anterior)

        self.assertEqual(
            actual["promedio"],
            4.0
        )

    def test_estado_finalizado_persistente(self):

        self.preparar_calificaciones_api()

        respuesta = self.solicitar_http(
            "PATCH",
            f"/inscripciones/{self.codigo_inscripcion}/estado",
            {"estado": "Finalizada"}
        )

        self.verificar_http(respuesta, 200)

        self.reiniciar_servidor()

        respuesta = self.solicitar_http(
            "GET",
            f"/inscripciones/{self.codigo_inscripcion}"
        )

        datos = self.verificar_http(
            respuesta,
            200
        )

        self.assertEqual(
            datos["estado"],
            "Finalizada"
        )

    def test_estado_cancelado_persistente(self):

        self.preparar_inscripcion_api()

        respuesta = self.solicitar_http(
            "PATCH",
            f"/inscripciones/{self.codigo_inscripcion}/estado",
            {"estado": "Cancelada"}
        )

        self.verificar_http(respuesta, 200)

        self.reiniciar_servidor()

        respuesta = self.solicitar_http(
            "GET",
            f"/inscripciones/{self.codigo_inscripcion}"
        )

        datos = self.verificar_http(
            respuesta,
            200
        )

        self.assertEqual(
            datos["estado"],
            "Cancelada"
        )

    def test_restriccion_calificacion_persistente(self):

        self.preparar_calificaciones_api()

        codigo = self.notas_creadas[0]

        respuesta = self.solicitar_http(
            "PATCH",
            f"/inscripciones/{self.codigo_inscripcion}/estado",
            {"estado": "Finalizada"}
        )

        self.verificar_http(respuesta, 200)

        self.reiniciar_servidor()

        respuesta = self.solicitar_http(
            "PATCH",
            f"/calificaciones/{codigo}",
            {"nota": 5.0}
        )

        self.verificar_http(
            respuesta,
            409,
            False
        )

        respuesta = self.solicitar_http(
            "GET",
            f"/calificaciones/{codigo}"
        )

        datos = self.verificar_http(
            respuesta,
            200
        )

        self.assertEqual(datos["nota"], 3.0)

    def test_duplicado_persistente(self):

        self.registrar_profesor_api()

        self.reiniciar_servidor()

        respuesta = self.solicitar_http(
            "POST",
            "/profesores",
            self.datos_profesor
        )

        self.verificar_http(
            respuesta,
            409,
            False
        )

    def test_reporte_persistente(self):

        self.preparar_calificaciones_api()

        self.reiniciar_servidor()

        respuesta = self.solicitar_http(
            "GET",
            "/reportes/calificaciones"
        )

        datos = self.verificar_http(
            respuesta,
            200
        )

        for codigo in self.notas_creadas:

            self.assertIn(
                codigo,
                datos["reporte"]
            )

    def test_resumen_persistente(self):

        self.registrar_profesor_api()

        self.preparar_calificaciones_api()

        respuesta = self.solicitar_http(
            "GET",
            "/reportes/resumen"
        )

        anterior = self.verificar_http(
            respuesta,
            200
        )

        self.reiniciar_servidor()

        respuesta = self.solicitar_http(
            "GET",
            "/reportes/resumen"
        )

        actual = self.verificar_http(
            respuesta,
            200
        )

        self.assertEqual(actual, anterior)

    def test_servidor_operativo_despues_reinicio(self):

        self.reiniciar_servidor()

        respuesta = self.solicitar_http(
            "GET",
            "/salud"
        )

        datos = self.verificar_http(
            respuesta,
            200
        )

        self.assertEqual(
            datos["estado"],
            "operativo"
        )

        self.assertEqual(
            self.enrutador.cantidad_rutas,
            34
        )
