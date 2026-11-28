import unittest

from tests.api_rest import BasePruebasAPI

from api.excepciones import Conflicto


class TestReportesAPI(BasePruebasAPI):

    def preparar_sistema(self):

        registros = (
            (
                "/profesores",
                {
                    "nombre": "Profesor Prueba",
                    "documento": 123456789,
                    "edad": 35,
                    "profesion": "Ingeniero",
                    "codigo": 1001,
                    "especialidad": "Python"
                }
            ),
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
                    "descripcion": "Curso de programación",
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

        respuesta = self.solicitar(
            "PUT",
            "/cursos/CUR-001/profesor",
            {"documento": 123456789}
        )

        self.verificar_respuesta(respuesta, 200)

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

    def test_resumen_sistema_vacio(self):

        respuesta = self.solicitar(
            "GET", "/reportes/resumen"
        )

        self.verificar_respuesta(respuesta, 200)

        self.assertEqual(
            respuesta.contenido["datos"],
            {
                "profesores": 0,
                "aprendices": 0,
                "cursos": 0,
                "inscripciones": 0,
                "calificaciones": 0
            }
        )

    def test_resumen_sistema_con_registros(self):

        self.preparar_sistema()

        respuesta = self.solicitar(
            "GET", "/reportes/resumen"
        )

        self.verificar_respuesta(respuesta, 200)

        self.assertEqual(
            respuesta.contenido["datos"],
            {
                "profesores": 1,
                "aprendices": 1,
                "cursos": 1,
                "inscripciones": 1,
                "calificaciones": 0
            }
        )

    def test_resumen_sistema_completo(self):

        self.preparar_sistema()

        self.registrar_calificaciones()

        respuesta = self.solicitar(
            "GET", "/reportes/resumen"
        )

        self.verificar_respuesta(respuesta, 200)

        self.assertEqual(
            respuesta.contenido["datos"],
            {
                "profesores": 1,
                "aprendices": 1,
                "cursos": 1,
                "inscripciones": 1,
                "calificaciones": 3
            }
        )

    def test_resumen_campos_exactos(self):

        respuesta = self.solicitar(
            "GET", "/reportes/resumen"
        )

        self.verificar_respuesta(respuesta, 200)

        self.assertEqual(
            set(respuesta.contenido["datos"]),
            {
                "profesores",
                "aprendices",
                "cursos",
                "inscripciones",
                "calificaciones"
            }
        )

    def test_resumen_valores_enteros(self):

        respuesta = self.solicitar(
            "GET", "/reportes/resumen"
        )

        self.verificar_respuesta(respuesta, 200)

        for valor in respuesta.contenido["datos"].values():

            with self.subTest(valor=valor):

                self.assertIs(type(valor), int)

                self.assertGreaterEqual(valor, 0)

    def test_reporte_calificaciones_vacio(self):

        respuesta = self.solicitar(
            "GET", "/reportes/calificaciones"
        )

        self.verificar_respuesta(respuesta, 200)

        self.assertIn(
            "reporte",
            respuesta.contenido["datos"]
        )

        self.assertIsInstance(
            respuesta.contenido["datos"]["reporte"],
            str
        )

    def test_reporte_calificaciones_con_datos(self):

        self.preparar_sistema()

        self.registrar_calificaciones()

        respuesta = self.solicitar(
            "GET", "/reportes/calificaciones"
        )

        self.verificar_respuesta(respuesta, 200)

        reporte = respuesta.contenido["datos"]["reporte"]

        self.assertIsInstance(reporte, str)

        self.assertTrue(reporte.strip())

    def test_resumen_no_contabiliza_duplicados(self):

        self.preparar_sistema()

        with self.assertRaises(Conflicto):

            self.solicitar(
                "POST",
                "/inscripciones",
                {
                    "codigo": "INS-002",
                    "documento_aprendiz": 987654321,
                    "codigo_curso": "CUR-001"
                }
            )

        respuesta = self.solicitar(
            "GET", "/reportes/resumen"
        )

        self.verificar_respuesta(respuesta, 200)

        self.assertEqual(
            respuesta.contenido["datos"]["inscripciones"],
            1
        )

    def test_resumen_despues_modificar_calificacion(self):

        self.preparar_sistema()

        self.registrar_calificaciones()

        respuesta = self.solicitar(
            "PATCH",
            "/calificaciones/NOT-001",
            {"nota": 4.0}
        )

        self.verificar_respuesta(respuesta, 200)

        respuesta = self.solicitar(
            "GET", "/reportes/resumen"
        )

        self.verificar_respuesta(respuesta, 200)

        self.assertEqual(
            respuesta.contenido["datos"]["calificaciones"],
            3
        )

    def test_rendimiento_por_aprendiz(self):

        self.preparar_sistema()

        self.registrar_calificaciones()

        respuesta = self.solicitar(
            "GET",
            "/aprendices/987654321/rendimiento"
        )

        self.verificar_respuesta(respuesta, 200)

        datos = respuesta.contenido["datos"]

        self.assertEqual(len(datos), 1)
        self.assertEqual(datos[0]["promedio"], 4.0)
        self.assertEqual(datos[0]["estado"], "Aprobado")

    def test_rendimiento_por_curso(self):

        self.preparar_sistema()

        self.registrar_calificaciones()

        respuesta = self.solicitar(
            "GET",
            "/cursos/CUR-001/rendimiento"
        )

        self.verificar_respuesta(respuesta, 200)

        datos = respuesta.contenido["datos"]

        self.assertEqual(len(datos), 1)
        self.assertEqual(datos[0]["promedio"], 4.0)
        self.assertEqual(datos[0]["estado"], "Aprobado")

    def test_consultar_aprendices_por_profesor(self):

        self.preparar_sistema()

        respuesta = self.solicitar(
            "GET",
            "/profesores/123456789/aprendices"
        )

        self.verificar_respuesta(respuesta, 200)

        datos = respuesta.contenido["datos"]

        self.assertEqual(len(datos), 1)

        self.assertEqual(
            datos[0]["curso"]["codigo"],
            "CUR-001"
        )

        self.assertEqual(
            len(datos[0]["aprendices"]),
            1
        )

        self.assertEqual(
            datos[0]["aprendices"][0]["documento"],
            987654321
        )

    def test_consultar_aprendices_por_curso(self):

        self.preparar_sistema()

        respuesta = self.solicitar(
            "GET",
            "/cursos/CUR-001/aprendices"
        )

        self.verificar_respuesta(respuesta, 200)

        datos = respuesta.contenido["datos"]

        self.assertEqual(len(datos), 1)

        self.assertEqual(
            datos[0]["documento"],
            987654321
        )

    def test_consultar_inscripciones_por_aprendiz(self):

        self.preparar_sistema()

        respuesta = self.solicitar(
            "GET",
            "/aprendices/987654321/inscripciones"
        )

        self.verificar_respuesta(respuesta, 200)

        datos = respuesta.contenido["datos"]

        self.assertEqual(len(datos), 1)

        self.assertEqual(
            datos[0]["codigo"], "INS-001"
        )

    def test_consultar_inscripciones_por_curso(self):

        self.preparar_sistema()

        respuesta = self.solicitar(
            "GET",
            "/cursos/CUR-001/inscripciones"
        )

        self.verificar_respuesta(respuesta, 200)

        datos = respuesta.contenido["datos"]

        self.assertEqual(len(datos), 1)

        self.assertEqual(
            datos[0]["codigo"], "INS-001"
        )


if __name__ == "__main__":

    unittest.main()