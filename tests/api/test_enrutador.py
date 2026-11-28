import unittest

from api.enrutador import Enrutador
from api.excepciones import (
    RecursoNoEncontrado,
    MetodoNoPermitido
)
from api.respuestas import respuesta_exitosa


class TestEnrutador(unittest.TestCase):

    def setUp(self):

        self.enrutador = Enrutador()

    def test_enrutador_inicialmente_vacio(self):

        self.assertEqual(
            self.enrutador.cantidad_rutas,
            0
        )

    def test_registrar_ruta(self):

        self.enrutador.registrar(
            "GET",
            "/prueba",
            lambda parametros, datos: respuesta_exitosa()
        )

        self.assertEqual(
            self.enrutador.cantidad_rutas,
            1
        )

    def test_resolver_ruta_estatica(self):

        self.enrutador.registrar(
            "GET",
            "/prueba",
            lambda parametros, datos: respuesta_exitosa(
                {"estado": "correcto"}
            )
        )

        respuesta = self.enrutador.resolver(
            "GET",
            "/prueba"
        )

        self.assertEqual(respuesta.estado, 200)

        self.assertEqual(
            respuesta.contenido["datos"],
            {"estado": "correcto"}
        )

    def test_resolver_ruta_dinamica(self):

        self.enrutador.registrar(
            "GET",
            "/profesores/{documento}",
            lambda parametros, datos: respuesta_exitosa(
                parametros
            )
        )

        respuesta = self.enrutador.resolver(
            "GET",
            "/profesores/123456"
        )

        self.assertEqual(
            respuesta.contenido["datos"],
            {"documento": "123456"}
        )

    def test_resolver_multiples_parametros(self):

        self.enrutador.registrar(
            "GET",
            "/cursos/{curso}/aprendices/{documento}",
            lambda parametros, datos: respuesta_exitosa(
                parametros
            )
        )

        respuesta = self.enrutador.resolver(
            "GET",
            "/cursos/CUR-001/aprendices/123456"
        )

        self.assertEqual(
            respuesta.contenido["datos"],
            {
                "curso": "CUR-001",
                "documento": "123456"
            }
        )

    def test_transferir_datos_al_controlador(self):

        self.enrutador.registrar(
            "POST",
            "/prueba",
            lambda parametros, datos: respuesta_exitosa(
                datos
            )
        )

        datos = {"nombre": "Prueba"}

        respuesta = self.enrutador.resolver(
            "POST",
            "/prueba",
            datos
        )

        self.assertEqual(
            respuesta.contenido["datos"],
            datos
        )

    def test_ruta_inexistente(self):

        with self.assertRaises(RecursoNoEncontrado):

            self.enrutador.resolver(
                "GET",
                "/inexistente"
            )

    def test_metodo_no_permitido(self):

        self.enrutador.registrar(
            "GET",
            "/prueba",
            lambda parametros, datos: respuesta_exitosa()
        )

        with self.assertRaises(MetodoNoPermitido):

            self.enrutador.resolver(
                "DELETE",
                "/prueba"
            )

    def test_metodos_permitidos(self):

        for metodo in ("GET", "POST"):

            self.enrutador.registrar(
                metodo,
                "/prueba",
                lambda parametros, datos: respuesta_exitosa()
            )

        with self.assertRaises(
            MetodoNoPermitido
        ) as contexto:

            self.enrutador.resolver(
                "DELETE",
                "/prueba"
            )

        self.assertEqual(
            set(contexto.exception.permitidos),
            {"GET", "POST"}
        )

    def test_ruta_duplicada(self):

        controlador = (
            lambda parametros, datos: respuesta_exitosa()
        )

        self.enrutador.registrar(
            "GET",
            "/prueba",
            controlador
        )

        with self.assertRaises(ValueError):

            self.enrutador.registrar(
                "GET",
                "/prueba",
                controlador
            )

    def test_misma_ruta_distinto_metodo(self):

        for metodo in ("GET", "POST"):

            self.enrutador.registrar(
                metodo,
                "/prueba",
                lambda parametros, datos: respuesta_exitosa()
            )

        self.assertEqual(
            self.enrutador.cantidad_rutas,
            2
        )

    def test_metodo_en_minusculas(self):

        self.enrutador.registrar(
            "get",
            "/prueba",
            lambda parametros, datos: respuesta_exitosa()
        )

        respuesta = self.enrutador.resolver(
            "get",
            "/prueba"
        )

        self.assertEqual(respuesta.estado, 200)

    def test_ruta_con_barra_final(self):

        self.enrutador.registrar(
            "GET",
            "/prueba",
            lambda parametros, datos: respuesta_exitosa()
        )

        respuesta = self.enrutador.resolver(
            "GET",
            "/prueba/"
        )

        self.assertEqual(respuesta.estado, 200)

    def test_ruta_con_parametros_consulta(self):

        self.enrutador.registrar(
            "GET",
            "/prueba",
            lambda parametros, datos: respuesta_exitosa()
        )

        respuesta = self.enrutador.resolver(
            "GET",
            "/prueba?pagina=1"
        )

        self.assertEqual(respuesta.estado, 200)

    def test_decodificar_parametro_url(self):

        self.enrutador.registrar(
            "GET",
            "/prueba/{codigo}",
            lambda parametros, datos: respuesta_exitosa(
                parametros
            )
        )

        respuesta = self.enrutador.resolver(
            "GET",
            "/prueba/CUR%2D001"
        )

        self.assertEqual(
            respuesta.contenido["datos"],
            {"codigo": "CUR-001"}
        )


if __name__ == "__main__":

    unittest.main()