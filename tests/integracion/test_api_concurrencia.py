
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier

from tests.integracion.test_api_mysql import (
    BaseIntegracionAPI
)


class TestAPIConcurrencia(BaseIntegracionAPI):

    def ejecutar_simultaneas(
        self,
        metodo: str,
        ruta: str,
        solicitudes: list[dict]
    ) -> list[tuple[int, dict, dict[str, str]]]:

        cantidad = len(solicitudes)

        barrera = Barrier(cantidad)

        def ejecutar(datos: dict):

            barrera.wait(timeout=10)

            return self.solicitar_http(
                metodo,
                ruta,
                datos
            )

        with ThreadPoolExecutor(
            max_workers=cantidad
        ) as ejecutor:

            return list(
                ejecutor.map(
                    ejecutar,
                    solicitudes
                )
            )

    def verificar_conflictos(
        self,
        respuestas: list[tuple[int, dict, dict[str, str]]]
    ):

        estados = sorted(
            respuesta[0]
            for respuesta in respuestas
        )

        esperados = [201] + [
            409
        ] * (len(respuestas) - 1)

        self.assertEqual(estados, esperados)

        for respuesta in respuestas:

            self.verificar_http(
                respuesta,
                respuesta[0],
                respuesta[0] == 201
            )

    def test_profesor_duplicado_concurrente(self):

        respuestas = self.ejecutar_simultaneas(
            "POST",
            "/profesores",
            [self.datos_profesor.copy() for _ in range(4)]
        )

        self.profesor_creado = any(
            respuesta[0] == 201
            for respuesta in respuestas
        )

        self.verificar_conflictos(respuestas)

        profesores = [
            profesor
            for profesor in self.sistema.listar_profesores()
            if profesor.documento == self.doc_profesor
        ]

        self.assertEqual(len(profesores), 1)

    def test_aprendiz_duplicado_concurrente(self):

        respuestas = self.ejecutar_simultaneas(
            "POST",
            "/aprendices",
            [self.datos_aprendiz.copy() for _ in range(4)]
        )

        self.aprendiz_creado = any(
            respuesta[0] == 201
            for respuesta in respuestas
        )

        self.verificar_conflictos(respuestas)

        aprendices = [
            aprendiz
            for aprendiz in self.sistema.listar_aprendices()
            if aprendiz.documento == self.doc_aprendiz
        ]

        self.assertEqual(len(aprendices), 1)

    def test_curso_duplicado_concurrente(self):

        respuestas = self.ejecutar_simultaneas(
            "POST",
            "/cursos",
            [self.datos_curso.copy() for _ in range(4)]
        )

        self.curso_creado = any(
            respuesta[0] == 201
            for respuesta in respuestas
        )

        self.verificar_conflictos(respuestas)

        cursos = [
            curso
            for curso in self.sistema.listar_cursos()
            if curso.codigo == self.codigo_curso
        ]

        self.assertEqual(len(cursos), 1)

    def test_inscripcion_duplicada_concurrente(self):

        self.registrar_aprendiz_api()

        self.registrar_curso_api()

        respuestas = self.ejecutar_simultaneas(
            "POST",
            "/inscripciones",
            [
                self.datos_inscripcion.copy()
                for _ in range(4)
            ]
        )

        self.inscripcion_creada = any(
            respuesta[0] == 201
            for respuesta in respuestas
        )

        self.verificar_conflictos(respuestas)

        inscripciones = (
            self.sistema.consultar_inscripciones_aprendiz(
                self.doc_aprendiz
            )
        )

        self.assertEqual(len(inscripciones), 1)

    def test_calificacion_duplicada_concurrente(self):

        self.preparar_inscripcion_api()

        codigo = f"N1-{self.uid}"

        datos = {
            "codigo": codigo,
            "codigo_inscripcion": self.codigo_inscripcion,
            "nota": 4.0
        }

        respuestas = self.ejecutar_simultaneas(
            "POST",
            "/calificaciones",
            [datos.copy() for _ in range(4)]
        )

        if any(
            respuesta[0] == 201
            for respuesta in respuestas
        ):

            self.notas_creadas.append(codigo)

        self.verificar_conflictos(respuestas)

        notas = (
            self.sistema.consultar_calificaciones_inscripcion(
                self.codigo_inscripcion
            )
        )

        self.assertEqual(len(notas), 1)

        self.assertEqual(notas[0].nota, 4.0)

    def test_calificaciones_distintas_concurrentes(self):

        self.preparar_inscripcion_api()

        solicitudes = [
            {
                "codigo": f"N{numero}-{self.uid}",
                "codigo_inscripcion": self.codigo_inscripcion,
                "nota": nota
            }
            for numero, nota in enumerate(
                [3.0, 4.0, 5.0],
                1
            )
        ]

        respuestas = self.ejecutar_simultaneas(
            "POST",
            "/calificaciones",
            solicitudes
        )

        for solicitud, respuesta in zip(
            solicitudes,
            respuestas
        ):

            if respuesta[0] == 201:

                self.notas_creadas.append(
                    str(solicitud["codigo"])
                )

        for respuesta in respuestas:

            self.verificar_http(respuesta, 201)

        notas = (
            self.sistema.consultar_calificaciones_inscripcion(
                self.codigo_inscripcion
            )
        )

        self.assertEqual(len(notas), 3)

        self.assertEqual(
            sorted(nota.nota for nota in notas),
            [3.0, 4.0, 5.0]
        )

        self.assertEqual(
            self.sistema.calcular_promedio(
                self.codigo_inscripcion
            ),
            4.0
        )

    def test_finalizacion_concurrente(self):

        self.preparar_calificaciones_api()

        respuestas = self.ejecutar_simultaneas(
            "PATCH",
            f"/inscripciones/{self.codigo_inscripcion}/estado",
            [
                {"estado": "Finalizada"}
                for _ in range(4)
            ]
        )

        estados = sorted(
            respuesta[0]
            for respuesta in respuestas
        )

        self.assertEqual(
            estados,
            [200, 409, 409, 409]
        )

        inscripcion = self.sistema.buscar_inscripcion(
            self.codigo_inscripcion
        )

        assert inscripcion is not None

        self.assertEqual(
            inscripcion.estado,
            "Finalizada"
        )

    def test_transiciones_estado_concurrentes(self):

        self.preparar_calificaciones_api()

        respuestas = self.ejecutar_simultaneas(
            "PATCH",
            f"/inscripciones/{self.codigo_inscripcion}/estado",
            [
                {"estado": "Cancelada"},
                {"estado": "Finalizada"}
            ]
        )

        self.assertEqual(
            sorted(r[0] for r in respuestas),
            [200, 409]
        )

        ganadora = next(
            respuesta
            for respuesta in respuestas
            if respuesta[0] == 200
        )

        datos = self.verificar_http(
            ganadora,
            200
        )

        inscripcion = self.sistema.buscar_inscripcion(
            self.codigo_inscripcion
        )

        assert inscripcion is not None

        self.assertEqual(
            inscripcion.estado,
            datos["estado"]
        )

        self.assertIn(
            inscripcion.estado,
            ["Cancelada", "Finalizada"]
        )

    def test_modificaciones_nota_concurrentes(self):

        self.preparar_inscripcion_api()

        codigo = self.registrar_calificacion_api(
            1,
            3.0
        )

        respuestas = self.ejecutar_simultaneas(
            "PATCH",
            f"/calificaciones/{codigo}",
            [
                {"nota": 3.5},
                {"nota": 4.0},
                {"nota": 4.5},
                {"nota": 5.0}
            ]
        )

        for respuesta in respuestas:

            self.verificar_http(respuesta, 200)

        calificacion = self.sistema.buscar_calificacion(
            codigo
        )

        assert calificacion is not None

        self.assertIn(
            calificacion.nota,
            [3.5, 4.0, 4.5, 5.0]
        )

        notas = (
            self.sistema.consultar_calificaciones_inscripcion(
                self.codigo_inscripcion
            )
        )

        self.assertEqual(len(notas), 1)

    def test_servidor_operativo_despues_concurrencia(self):

        respuestas = self.ejecutar_simultaneas(
            "POST",
            "/profesores",
            [self.datos_profesor.copy() for _ in range(4)]
        )

        self.profesor_creado = any(
            respuesta[0] == 201
            for respuesta in respuestas
        )

        self.verificar_conflictos(respuestas)

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
