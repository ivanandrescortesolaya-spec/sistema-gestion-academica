import json
import unittest

from http import HTTPStatus

from api.respuestas import (
    Respuesta,
    respuesta_exitosa,
    respuesta_creada,
    respuesta_error
)


class TestRespuestasAPI(unittest.TestCase):

    def test_respuesta_exitosa(self):

        respuesta = respuesta_exitosa(
            {"nombre": "Python"}
        )

        self.assertEqual(
            respuesta.estado,
            HTTPStatus.OK
        )

        self.assertTrue(
            respuesta.contenido["exito"]
        )

        self.assertEqual(
            respuesta.contenido["datos"],
            {"nombre": "Python"}
        )

    def test_respuesta_exitosa_sin_datos(self):

        respuesta = respuesta_exitosa()

        self.assertEqual(respuesta.estado, 200)

        self.assertTrue(
            respuesta.contenido["exito"]
        )

        self.assertIsNone(
            respuesta.contenido["datos"]
        )

    def test_respuesta_mensaje_personalizado(self):

        respuesta = respuesta_exitosa(
            datos=[],
            mensaje="Consulta completada"
        )

        self.assertEqual(
            respuesta.contenido["mensaje"],
            "Consulta completada"
        )

    def test_respuesta_estado_personalizado(self):

        respuesta = respuesta_exitosa(
            estado=HTTPStatus.ACCEPTED
        )

        self.assertEqual(
            respuesta.estado,
            202
        )

    def test_respuesta_creada(self):

        respuesta = respuesta_creada(
            {"codigo": "CUR-001"}
        )

        self.assertEqual(respuesta.estado, 201)

        self.assertTrue(
            respuesta.contenido["exito"]
        )

        self.assertEqual(
            respuesta.contenido["datos"],
            {"codigo": "CUR-001"}
        )

    def test_respuesta_creada_con_location(self):

        respuesta = respuesta_creada(
            datos={"codigo": "CUR-001"},
            ubicacion="/api/v1/cursos/CUR-001"
        )

        self.assertEqual(
            respuesta.encabezados["Location"],
            "/api/v1/cursos/CUR-001"
        )

    def test_respuesta_creada_sin_location(self):

        respuesta = respuesta_creada(
            {"codigo": "CUR-001"}
        )

        self.assertNotIn(
            "Location",
            respuesta.encabezados
        )

    def test_respuesta_error(self):

        respuesta = respuesta_error(
            mensaje="Recurso inexistente",
            estado=HTTPStatus.NOT_FOUND
        )

        self.assertEqual(respuesta.estado, 404)

        self.assertFalse(
            respuesta.contenido["exito"]
        )

        self.assertEqual(
            respuesta.contenido["mensaje"],
            "Recurso inexistente"
        )

        self.assertIsNone(
            respuesta.contenido["datos"]
        )

    def test_respuesta_error_con_encabezados(self):

        respuesta = respuesta_error(
            mensaje="Método no permitido",
            estado=HTTPStatus.METHOD_NOT_ALLOWED,
            encabezados={"Allow": "GET, POST"}
        )

        self.assertEqual(respuesta.estado, 405)

        self.assertEqual(
            respuesta.encabezados["Allow"],
            "GET, POST"
        )

    def test_estructura_respuesta(self):

        respuesta = respuesta_exitosa()

        self.assertEqual(
            set(respuesta.contenido.keys()),
            {"exito", "mensaje", "datos"}
        )

    def test_convertir_json(self):

        respuesta = respuesta_exitosa(
            {"codigo": "CUR-001"}
        )

        contenido = respuesta.convertir_json()

        self.assertIsInstance(contenido, bytes)

        resultado = json.loads(
            contenido.decode("utf-8")
        )

        self.assertEqual(
            resultado,
            respuesta.contenido
        )

    def test_serializar_caracteres_especiales(self):

        respuesta = respuesta_exitosa(
            {"nombre": "Programación académica"}
        )

        contenido = respuesta.convertir_json()

        self.assertIn(
            "Programación académica",
            contenido.decode("utf-8")
        )

    def test_serializar_lista(self):

        respuesta = respuesta_exitosa(
            [
                {"codigo": "CUR-001"},
                {"codigo": "CUR-002"}
            ]
        )

        resultado = json.loads(
            respuesta.convertir_json()
        )

        self.assertEqual(
            len(resultado["datos"]),
            2
        )

    def test_rechazar_nan(self):

        respuesta = respuesta_exitosa(
            {"nota": float("nan")}
        )

        with self.assertRaises(ValueError):

            respuesta.convertir_json()

    def test_rechazar_infinito(self):

        respuesta = respuesta_exitosa(
            {"nota": float("inf")}
        )

        with self.assertRaises(ValueError):

            respuesta.convertir_json()

    def test_encabezados_independientes(self):

        primera = Respuesta(
            estado=HTTPStatus.OK,
            contenido={}
        )

        segunda = Respuesta(
            estado=HTTPStatus.OK,
            contenido={}
        )

        primera.encabezados["Prueba"] = "Valor"

        self.assertNotIn(
            "Prueba",
            segunda.encabezados
        )

    def test_objeto_no_serializable(self):

        respuesta = respuesta_exitosa(
            {"objeto": object()}
        )

        with self.assertRaises(TypeError):

            respuesta.convertir_json()


if __name__ == "__main__":

    unittest.main()