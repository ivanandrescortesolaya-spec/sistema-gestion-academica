from http import HTTPStatus


class ErrorAPI(Exception):
    """Excepción base de la API REST."""

    def __init__(
        self,
        mensaje: str,
        estado: HTTPStatus = HTTPStatus.BAD_REQUEST
    ):
        super().__init__(mensaje)

        self.mensaje = mensaje
        self.estado = estado


class SolicitudInvalida(ErrorAPI):

    def __init__(self, mensaje: str):
        super().__init__(
            mensaje,
            HTTPStatus.BAD_REQUEST
        )


class RecursoNoEncontrado(ErrorAPI):

    def __init__(self, mensaje: str):
        super().__init__(
            mensaje,
            HTTPStatus.NOT_FOUND
        )


class MetodoNoPermitido(ErrorAPI):

    def __init__(self, permitidos: tuple[str, ...]):
        super().__init__(
            "Método HTTP no permitido",
            HTTPStatus.METHOD_NOT_ALLOWED
        )

        self.permitidos = permitidos


class Conflicto(ErrorAPI):

    def __init__(self, mensaje: str):
        super().__init__(
            mensaje,
            HTTPStatus.CONFLICT
        )


class ContenidoDemasiadoGrande(ErrorAPI):

    def __init__(self):
        super().__init__(
            "El contenido supera el tamaño permitido",
            HTTPStatus.REQUEST_ENTITY_TOO_LARGE
        )


class FormatoNoSoportado(ErrorAPI):

    def __init__(self):
        super().__init__(
            "El contenido debe tener formato application/json",
            HTTPStatus.UNSUPPORTED_MEDIA_TYPE
        )


class DatosInvalidos(ErrorAPI):

    def __init__(self, mensaje: str):
        super().__init__(
            mensaje,
            HTTPStatus.UNPROCESSABLE_ENTITY
        )


class ErrorInterno(ErrorAPI):

    def __init__(self):
        super().__init__(
            "Error interno del servidor",
            HTTPStatus.INTERNAL_SERVER_ERROR
        )


class ServicioNoDisponible(ErrorAPI):

    def __init__(self):
        super().__init__(
            "Servicio temporalmente no disponible",
            HTTPStatus.SERVICE_UNAVAILABLE
        )