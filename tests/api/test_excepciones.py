import unittest

from http import HTTPStatus

from api.excepciones import (
    ErrorAPI,
    SolicitudInvalida,
    RecursoNoEncontrado,
    MetodoNoPermitido,
    Conflicto,
    ContenidoDemasiadoGrande,
    FormatoNoSoportado,
    DatosInvalidos,
    ErrorInterno,
    ServicioNoDisponible
)


class TestExcepcionesAPI(unittest.TestCase):

    def test_error_api_base(self):

        error = ErrorAPI("Error de prueba")

        self.assertEqual(
            error.mensaje,
            "Error de prueba"
        )

        self.assertEqual(
            error.estado,
            HTTPStatus.BAD_REQUEST
        )

    def test_error_api_estado_personalizado(self):

        error = ErrorAPI(
            "Error personalizado",
            HTTPStatus.FORBIDDEN
        )

        self.assertEqual(
            error.estado,
            HTTPStatus.FORBIDDEN
        )

    def test_solicitud_invalida(self):

        error = SolicitudInvalida(
            "Solicitud incorrecta"
        )

        self.assertEqual(error.estado, 400)

        self.assertEqual(
            error.mensaje,
            "Solicitud incorrecta"
        )

    def test_recurso_no_encontrado(self):

        error = RecursoNoEncontrado(
            "Profesor inexistente"
        )

        self.assertEqual(error.estado, 404)

        self.assertEqual(
            error.mensaje,
            "Profesor inexistente"
        )

    def test_conflicto(self):

        error = Conflicto(
            "Registro duplicado"
        )

        self.assertEqual(error.estado, 409)

        self.assertEqual(
            error.mensaje,
            "Registro duplicado"
        )

    def test_contenido_demasiado_grande(self):

        error = ContenidoDemasiadoGrande()

        self.assertEqual(error.estado, 413)

        self.assertTrue(error.mensaje)

    def test_formato_no_soportado(self):

        error = FormatoNoSoportado()

        self.assertEqual(error.estado, 415)

        self.assertTrue(error.mensaje)

    def test_datos_invalidos(self):

        error = DatosInvalidos(
            "La nota no es válida"
        )

        self.assertEqual(error.estado, 422)

        self.assertEqual(
            error.mensaje,
            "La nota no es válida"
        )

    def test_error_interno(self):

        error = ErrorInterno()

        self.assertEqual(error.estado, 500)

        self.assertTrue(error.mensaje)

    def test_servicio_no_disponible(self):

        error = ServicioNoDisponible()

        self.assertEqual(error.estado, 503)

        self.assertTrue(error.mensaje)

    def test_herencia_excepciones(self):

        clases = (
            SolicitudInvalida,
            RecursoNoEncontrado,
            MetodoNoPermitido,
            Conflicto,
            ContenidoDemasiadoGrande,
            FormatoNoSoportado,
            DatosInvalidos,
            ErrorInterno,
            ServicioNoDisponible
        )

        for clase in clases:

            with self.subTest(clase=clase.__name__):

                self.assertTrue(
                    issubclass(clase, ErrorAPI)
                )

    def test_capturar_excepcion_especifica(self):

        with self.assertRaises(ErrorAPI):

            raise DatosInvalidos(
                "Datos incorrectos"
            )


if __name__ == "__main__":

    unittest.main()