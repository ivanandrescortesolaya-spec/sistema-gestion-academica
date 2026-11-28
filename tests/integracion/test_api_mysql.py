
import json

from threading import Thread
from urllib.request import Request, urlopen
from urllib.error import HTTPError

from tests.integracion import BaseIntegracion

from api.rutas import crear_enrutador
from api.servidor import crear_servidor


class BaseIntegracionAPI(BaseIntegracion):

    def setUp(self):

        super().setUp()

        self.enrutador = crear_enrutador(self.sistema)

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

        self.datos_profesor = {
            "nombre": self.profesor.nombre,
            "documento": self.doc_profesor,
            "edad": self.profesor.edad,
            "profesion": self.profesor.profesion,
            "codigo": self.codigo_profesor,
            "especialidad": self.profesor.especialidad
        }

        self.datos_aprendiz = {
            "nombre": self.aprendiz.nombre,
            "documento": self.doc_aprendiz,
            "edad": self.aprendiz.edad,
            "telefono": self.aprendiz.telefono,
            "correo": self.aprendiz.correo,
            "direccion": self.aprendiz.direccion
        }

        self.datos_curso = {
            "codigo": self.codigo_curso,
            "nombre": self.curso.nombre,
            "descripcion": self.curso.descripcion,
            "duracion_horas": self.curso.duracion_horas,
            "modalidad": self.curso.modalidad
        }

        self.datos_inscripcion = {
            "codigo": self.codigo_inscripcion,
            "documento_aprendiz": self.doc_aprendiz,
            "codigo_curso": self.codigo_curso,
            "fecha_inscripcion": self.fecha.isoformat()
        }

    def detener_servidor(self):

        self.servidor.shutdown()

        self.servidor.server_close()

        self.hilo.join(timeout=5)

    def solicitar_http(
        self,
        metodo: str,
        ruta: str,
        datos: dict | None = None
    ) -> tuple[int, dict, dict[str, str]]:

        encabezados = {
            "Accept": "application/json"
        }

        cuerpo = None

        if datos is not None:

            cuerpo = json.dumps(
                datos,
                ensure_ascii=False
            ).encode("utf-8")

            encabezados["Content-Type"] = (
                "application/json"
            )

        solicitud = Request(
            url=f"{self.url_base}{ruta}",
            data=cuerpo,
            headers=encabezados,
            method=metodo
        )

        try:

            with urlopen(
                solicitud,
                timeout=30
            ) as respuesta:

                codigo = respuesta.code

                contenido = json.loads(
                    respuesta.read().decode("utf-8")
                )

                cabeceras = {
                    clave.lower(): valor
                    for clave, valor
                    in respuesta.headers.items()
                }

        except HTTPError as error:

            with error:

                codigo = error.code

                contenido = json.loads(
                    error.read().decode("utf-8")
                )

                cabeceras = {
                    clave.lower(): valor
                    for clave, valor
                    in error.headers.items()
                }

        assert isinstance(contenido, dict), (
            "La API no devolvió un objeto JSON"
        )

        return codigo, contenido, cabeceras

    def verificar_http(
        self,
        respuesta: tuple[int, dict, dict[str, str]],
        estado: int,
        exito: bool = True
    ):

        codigo, contenido, encabezados = respuesta

        self.assertEqual(codigo, estado)

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

    def registrar_profesor_api(self):

        respuesta = self.solicitar_http(
            "POST",
            "/profesores",
            self.datos_profesor
        )

        if respuesta[0] == 201:
            self.profesor_creado = True

        return self.verificar_http(respuesta, 201)

    def registrar_aprendiz_api(self):

        respuesta = self.solicitar_http(
            "POST",
            "/aprendices",
            self.datos_aprendiz
        )

        if respuesta[0] == 201:
            self.aprendiz_creado = True

        return self.verificar_http(respuesta, 201)

    def registrar_curso_api(self):

        respuesta = self.solicitar_http(
            "POST",
            "/cursos",
            self.datos_curso
        )

        if respuesta[0] == 201:
            self.curso_creado = True

        return self.verificar_http(respuesta, 201)

    def asignar_profesor_api(self):

        respuesta = self.solicitar_http(
            "PUT",
            f"/cursos/{self.codigo_curso}/profesor",
            {"documento": self.doc_profesor}
        )

        return self.verificar_http(respuesta, 200)

    def registrar_inscripcion_api(self):

        respuesta = self.solicitar_http(
            "POST",
            "/inscripciones",
            self.datos_inscripcion
        )

        if respuesta[0] == 201:
            self.inscripcion_creada = True

        return self.verificar_http(respuesta, 201)

    def registrar_calificacion_api(
        self,
        numero: int,
        nota: float
    ) -> str:

        codigo = f"N{numero}-{self.uid}"

        respuesta = self.solicitar_http(
            "POST",
            "/calificaciones",
            {
                "codigo": codigo,
                "codigo_inscripcion": (
                    self.codigo_inscripcion
                ),
                "nota": nota,
                "fecha": self.fecha.isoformat()
            }
        )

        if respuesta[0] == 201:
            self.notas_creadas.append(codigo)

        self.verificar_http(respuesta, 201)

        return codigo

    def preparar_inscripcion_api(self):

        self.registrar_aprendiz_api()

        self.registrar_curso_api()

        self.registrar_inscripcion_api()

    def preparar_calificaciones_api(self):

        self.preparar_inscripcion_api()

        for numero, nota in enumerate(
            [3.0, 4.0, 5.0],
            1
        ):

            self.registrar_calificacion_api(
                numero,
                nota
            )


class TestAPIMySQL(BaseIntegracionAPI):

    def test_base_datos_aislada(self):

        self.assertEqual(
            self.config.base_datos,
            "sistema_gestion_academica_test"
        )

        self.assertEqual(
            self.config.usuario,
            "academic_test_user"
        )

    def test_servidor_operativo(self):

        respuesta = self.solicitar_http(
            "GET",
            "/salud"
        )

        datos = self.verificar_http(respuesta, 200)

        self.assertEqual(
            datos["estado"],
            "operativo"
        )

    def test_cantidad_endpoints(self):

        self.assertEqual(
            self.enrutador.cantidad_rutas,
            34
        )

    def test_registrar_profesor_mysql(self):

        datos = self.registrar_profesor_api()

        self.assertEqual(
            datos["documento"],
            self.doc_profesor
        )

        profesor = self.sistema.buscar_profesor(
            self.doc_profesor
        )

        assert profesor is not None

        self.assertEqual(
            profesor.codigo,
            self.codigo_profesor
        )

    def test_buscar_profesor_mysql(self):

        self.registrar_profesor_api()

        respuesta = self.solicitar_http(
            "GET",
            f"/profesores/{self.doc_profesor}"
        )

        datos = self.verificar_http(respuesta, 200)

        self.assertEqual(
            datos,
            self.datos_profesor
        )

    def test_listar_profesores_mysql(self):

        self.registrar_profesor_api()

        respuesta = self.solicitar_http(
            "GET",
            "/profesores"
        )

        datos = self.verificar_http(respuesta, 200)

        self.assertTrue(
            any(
                profesor["documento"] == self.doc_profesor
                for profesor in datos
            )
        )

    def test_profesor_duplicado_mysql(self):

        self.registrar_profesor_api()

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

    def test_registrar_aprendiz_mysql(self):

        datos = self.registrar_aprendiz_api()

        self.assertEqual(
            datos["documento"],
            self.doc_aprendiz
        )

        aprendiz = self.sistema.buscar_aprendiz(
            self.doc_aprendiz
        )

        assert aprendiz is not None

        self.assertEqual(
            aprendiz.correo,
            self.datos_aprendiz["correo"]
        )

    def test_buscar_aprendiz_mysql(self):

        self.registrar_aprendiz_api()

        respuesta = self.solicitar_http(
            "GET",
            f"/aprendices/{self.doc_aprendiz}"
        )

        datos = self.verificar_http(respuesta, 200)

        self.assertEqual(
            datos,
            self.datos_aprendiz
        )

    def test_aprendiz_duplicado_mysql(self):

        self.registrar_aprendiz_api()

        respuesta = self.solicitar_http(
            "POST",
            "/aprendices",
            self.datos_aprendiz
        )

        self.verificar_http(respuesta, 409, False)

    def test_registrar_curso_mysql(self):

        datos = self.registrar_curso_api()

        self.assertEqual(
            datos["codigo"],
            self.codigo_curso
        )

        curso = self.sistema.buscar_curso(
            self.codigo_curso
        )

        assert curso is not None

        self.assertEqual(
            curso.duracion_horas,
            48
        )

    def test_buscar_curso_mysql(self):

        self.registrar_curso_api()

        respuesta = self.solicitar_http(
            "GET",
            f"/cursos/{self.codigo_curso}"
        )

        datos = self.verificar_http(respuesta, 200)

        self.assertEqual(
            datos["codigo"],
            self.codigo_curso
        )

    def test_curso_duplicado_mysql(self):

        self.registrar_curso_api()

        respuesta = self.solicitar_http(
            "POST",
            "/cursos",
            self.datos_curso
        )

        self.verificar_http(respuesta, 409, False)

    def test_asignar_profesor_mysql(self):

        self.registrar_profesor_api()

        self.registrar_curso_api()

        datos = self.asignar_profesor_api()

        self.assertEqual(
            datos["profesor"]["documento"],
            self.doc_profesor
        )

        curso = self.sistema.buscar_curso(
            self.codigo_curso
        )

        assert curso is not None

        profesor = curso.profesor

        assert profesor is not None

        self.assertEqual(
            profesor.documento,
            self.doc_profesor
        )

    def test_registrar_inscripcion_mysql(self):

        self.preparar_inscripcion_api()

        inscripcion = self.sistema.buscar_inscripcion(
            self.codigo_inscripcion
        )

        assert inscripcion is not None

        self.assertEqual(
            inscripcion.estado,
            "Activa"
        )

        self.assertEqual(
            inscripcion.fecha_inscripcion,
            self.fecha
        )

    def test_buscar_inscripcion_mysql(self):

        self.preparar_inscripcion_api()

        respuesta = self.solicitar_http(
            "GET",
            f"/inscripciones/{self.codigo_inscripcion}"
        )

        datos = self.verificar_http(respuesta, 200)

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

    def test_inscripcion_duplicada_mysql(self):

        self.preparar_inscripcion_api()

        respuesta = self.solicitar_http(
            "POST",
            "/inscripciones",
            self.datos_inscripcion
        )

        self.verificar_http(respuesta, 409, False)

    def test_cancelar_inscripcion_mysql(self):

        self.preparar_inscripcion_api()

        respuesta = self.solicitar_http(
            "PATCH",
            f"/inscripciones/{self.codigo_inscripcion}/estado",
            {"estado": "Cancelada"}
        )

        datos = self.verificar_http(respuesta, 200)

        self.assertEqual(
            datos["estado"],
            "Cancelada"
        )

        inscripcion = self.sistema.buscar_inscripcion(
            self.codigo_inscripcion
        )

        assert inscripcion is not None

        self.assertEqual(
            inscripcion.estado,
            "Cancelada"
        )

    def test_finalizar_inscripcion_mysql(self):

        self.preparar_calificaciones_api()

        respuesta = self.solicitar_http(
            "PATCH",
            f"/inscripciones/{self.codigo_inscripcion}/estado",
            {"estado": "Finalizada"}
        )

        datos = self.verificar_http(respuesta, 200)

        self.assertEqual(
            datos["estado"],
            "Finalizada"
        )

    def test_registrar_calificacion_mysql(self):

        self.preparar_inscripcion_api()

        codigo = self.registrar_calificacion_api(
            1,
            4.5
        )

        calificacion = self.sistema.buscar_calificacion(
            codigo
        )

        assert calificacion is not None

        self.assertEqual(
            calificacion.nota,
            4.5
        )

        self.assertEqual(
            calificacion.fecha,
            self.fecha
        )

    def test_modificar_calificacion_mysql(self):

        self.preparar_inscripcion_api()

        codigo = self.registrar_calificacion_api(
            1,
            3.0
        )

        respuesta = self.solicitar_http(
            "PATCH",
            f"/calificaciones/{codigo}",
            {"nota": 4.5}
        )

        datos = self.verificar_http(respuesta, 200)

        self.assertEqual(
            datos["nota"],
            4.5
        )

        calificacion = self.sistema.buscar_calificacion(
            codigo
        )

        assert calificacion is not None

        self.assertEqual(
            calificacion.nota,
            4.5
        )

    def test_calificacion_duplicada_mysql(self):

        self.preparar_inscripcion_api()

        codigo = self.registrar_calificacion_api(
            1,
            4.0
        )

        respuesta = self.solicitar_http(
            "POST",
            "/calificaciones",
            {
                "codigo": codigo,
                "codigo_inscripcion": (
                    self.codigo_inscripcion
                ),
                "nota": 5.0
            }
        )

        self.verificar_http(respuesta, 409, False)

    def test_calificacion_fuera_rango_mysql(self):

        self.preparar_inscripcion_api()

        codigo = f"INVALIDA-{self.uid}"

        respuesta = self.solicitar_http(
            "POST",
            "/calificaciones",
            {
                "codigo": codigo,
                "codigo_inscripcion": (
                    self.codigo_inscripcion
                ),
                "nota": 6.0
            }
        )

        if respuesta[0] == 201:
            self.notas_creadas.append(codigo)

        self.verificar_http(respuesta, 422, False)

        self.assertIsNone(
            self.sistema.buscar_calificacion(codigo)
        )

    def test_consultar_calificaciones_mysql(self):

        self.preparar_calificaciones_api()

        respuesta = self.solicitar_http(
            "GET",
            f"/inscripciones/{self.codigo_inscripcion}/calificaciones"
        )

        datos = self.verificar_http(respuesta, 200)

        self.assertEqual(len(datos), 3)

        self.assertEqual(
            sorted(nota["nota"] for nota in datos),
            [3.0, 4.0, 5.0]
        )

    def test_calcular_promedio_mysql(self):

        self.preparar_calificaciones_api()

        respuesta = self.solicitar_http(
            "GET",
            f"/inscripciones/{self.codigo_inscripcion}/promedio"
        )

        datos = self.verificar_http(respuesta, 200)

        self.assertEqual(
            datos["promedio"],
            4.0
        )

        self.assertEqual(
            datos["estado"],
            "Aprobado"
        )

    def test_recalcular_promedio_mysql(self):

        self.preparar_calificaciones_api()

        codigo = self.notas_creadas[0]

        respuesta = self.solicitar_http(
            "PATCH",
            f"/calificaciones/{codigo}",
            {"nota": 4.0}
        )

        self.verificar_http(respuesta, 200)

        respuesta = self.solicitar_http(
            "GET",
            f"/inscripciones/{self.codigo_inscripcion}/promedio"
        )

        datos = self.verificar_http(respuesta, 200)

        self.assertEqual(
            datos["promedio"],
            4.33
        )

    def test_consultar_cursos_aprendiz_mysql(self):

        self.preparar_inscripcion_api()

        respuesta = self.solicitar_http(
            "GET",
            f"/aprendices/{self.doc_aprendiz}/cursos"
        )

        datos = self.verificar_http(respuesta, 200)

        self.assertEqual(len(datos), 1)

        self.assertEqual(
            datos[0]["codigo"],
            self.codigo_curso
        )

    def test_consultar_aprendices_curso_mysql(self):

        self.preparar_inscripcion_api()

        respuesta = self.solicitar_http(
            "GET",
            f"/cursos/{self.codigo_curso}/aprendices"
        )

        datos = self.verificar_http(respuesta, 200)

        self.assertEqual(len(datos), 1)

        self.assertEqual(
            datos[0]["documento"],
            self.doc_aprendiz
        )

    def test_reporte_calificaciones_mysql(self):

        self.preparar_calificaciones_api()

        respuesta = self.solicitar_http(
            "GET",
            "/reportes/calificaciones"
        )

        datos = self.verificar_http(respuesta, 200)

        for codigo in self.notas_creadas:

            self.assertIn(
                codigo,
                datos["reporte"]
            )

    def test_resumen_academico_mysql(self):

        respuesta = self.solicitar_http(
            "GET",
            "/reportes/resumen"
        )

        anterior = self.verificar_http(
            respuesta,
            200
        )

        self.registrar_profesor_api()

        self.preparar_calificaciones_api()

        respuesta = self.solicitar_http(
            "GET",
            "/reportes/resumen"
        )

        actual = self.verificar_http(
            respuesta,
            200
        )

        incrementos = {
            "profesores": 1,
            "aprendices": 1,
            "cursos": 1,
            "inscripciones": 1,
            "calificaciones": 3
        }

        for campo, incremento in incrementos.items():

            self.assertEqual(
                actual[campo],
                anterior[campo] + incremento
            )
