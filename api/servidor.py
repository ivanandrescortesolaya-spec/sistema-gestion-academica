import json
import logging
import re

from http import HTTPStatus
from http.server import (
    BaseHTTPRequestHandler,
    ThreadingHTTPServer
)

from typing import Any

from api.enrutador import Enrutador

from api.excepciones import (
    ErrorAPI,
    SolicitudInvalida,
    MetodoNoPermitido,
    ContenidoDemasiadoGrande,
    FormatoNoSoportado
)

from api.respuestas import (
    Respuesta,
    respuesta_error
)

from persistencia.excepciones import (
    ErrorConexion,
    ErrorIntegridad,
    ErrorPersistencia
)


logger = logging.getLogger(__name__)

MAXIMO_CONTENIDO = 1024 * 1024

TIEMPO_ESPERA = 15


def rechazar_constante(valor: str):

    raise ValueError(
        "Constante JSON no permitida"
    )


def validar_objeto_json(
    pares: list[tuple[str, Any]]
) -> dict[str, Any]:

    resultado: dict[str, Any] = {}

    for clave, valor in pares:

        if clave in resultado:

            raise ValueError(
                "El JSON contiene campos duplicados"
            )

        resultado[clave] = valor

    return resultado


class ManejadorHTTP(BaseHTTPRequestHandler):

    enrutador: Enrutador

    protocol_version = "HTTP/1.0"

    server_version = "AcademicAPI/1.0"

    sys_version = ""

    def setup(self):

        self.request.settimeout(TIEMPO_ESPERA)

        super().setup()

    def __leer_json(self) -> dict[str, Any]:

        if self.headers.get("Transfer-Encoding"):

            raise SolicitudInvalida(
                "Transfer-Encoding no soportado"
            )

        longitudes = self.headers.get_all(
            "Content-Length"
        ) or []

        if len(longitudes) > 1:

            raise SolicitudInvalida(
                "Content-Length duplicado"
            )

        longitud_texto = (
            longitudes[0]
            if longitudes
            else "0"
        )

        if not re.fullmatch(
            r"[0-9]{1,10}",
            longitud_texto
        ):

            raise SolicitudInvalida(
                "Content-Length inválido"
            )

        longitud = int(longitud_texto)

        if longitud > MAXIMO_CONTENIDO:

            raise ContenidoDemasiadoGrande()

        if self.command not in (
            "POST", "PUT", "PATCH"
        ):

            if longitud != 0:

                raise SolicitudInvalida(
                    "El método no admite contenido"
                )

            return {}

        if longitud == 0:

            raise SolicitudInvalida(
                "El cuerpo de la solicitud es obligatorio"
            )

        tipo = self.headers.get(
            "Content-Type", ""
        )

        tipo = tipo.split(";")[0].strip().lower()

        if tipo != "application/json":

            raise FormatoNoSoportado()

        contenido = self.rfile.read(longitud)

        if len(contenido) != longitud:

            raise SolicitudInvalida(
                "Contenido incompleto"
            )

        try:

            datos = json.loads(
                contenido.decode("utf-8"),
                parse_constant=rechazar_constante,
                object_pairs_hook=validar_objeto_json
            )

        except (
            ValueError,
            UnicodeError,
            RecursionError
        ) as error:

            raise SolicitudInvalida(
                "El contenido JSON no es válido"
            ) from error

        if not isinstance(datos, dict):

            raise SolicitudInvalida(
                "El contenido JSON debe ser un objeto"
            )

        return datos

    def __enviar_respuesta(
        self,
        respuesta: Respuesta
    ) -> None:

        contenido = respuesta.convertir_json()

        self.send_response(
            int(respuesta.estado)
        )

        self.send_header(
            "Content-Type",
            "application/json; charset=utf-8"
        )

        self.send_header(
            "Content-Length",
            str(len(contenido))
        )

        self.send_header(
            "Cache-Control",
            "no-store"
        )

        self.send_header(
            "X-Content-Type-Options",
            "nosniff"
        )

        self.send_header(
            "Connection",
            "close"
        )

        for nombre, valor in respuesta.encabezados.items():

            self.send_header(nombre, valor)

        self.end_headers()

        if self.command != "HEAD":

            self.wfile.write(contenido)

        self.close_connection = True

    def __procesar_solicitud(self) -> None:

        try:

            datos = self.__leer_json()

            respuesta = self.enrutador.resolver(
                metodo=self.command,
                url=self.path,
                datos=datos
            )

        except MetodoNoPermitido as error:

            respuesta = respuesta_error(
                mensaje=error.mensaje,
                estado=error.estado,
                encabezados={
                    "Allow": ", ".join(
                        error.permitidos
                    )
                }
            )

        except ErrorAPI as error:

            respuesta = respuesta_error(
                mensaje=error.mensaje,
                estado=error.estado
            )

        except ErrorConexion:

            logger.exception(
                "Error de conexión con MySQL"
            )

            respuesta = respuesta_error(
                "Base de datos temporalmente no disponible",
                HTTPStatus.SERVICE_UNAVAILABLE
            )

        except ErrorIntegridad:

            respuesta = respuesta_error(
                "Conflicto de integridad de datos",
                HTTPStatus.CONFLICT
            )

        except ErrorPersistencia:

            logger.exception(
                "Error de persistencia"
            )

            respuesta = respuesta_error(
                "Error interno de persistencia",
                HTTPStatus.INTERNAL_SERVER_ERROR
            )

        except TimeoutError:

            respuesta = respuesta_error(
                "Tiempo de espera agotado",
                HTTPStatus.REQUEST_TIMEOUT
            )

        except Exception:

            logger.exception(
                "Error inesperado de la API"
            )

            respuesta = respuesta_error(
                "Error interno del servidor",
                HTTPStatus.INTERNAL_SERVER_ERROR
            )

        try:

            respuesta.convertir_json()

        except (TypeError, ValueError, RecursionError):

            logger.exception(
                "Error al serializar la respuesta"
            )

            respuesta = respuesta_error(
                "Error interno del servidor",
                HTTPStatus.INTERNAL_SERVER_ERROR
            )

        try:

            self.__enviar_respuesta(respuesta)

        except (OSError, TimeoutError):

            self.close_connection = True

    def do_GET(self):

        self.__procesar_solicitud()

    def do_POST(self):

        self.__procesar_solicitud()

    def do_PUT(self):

        self.__procesar_solicitud()

    def do_PATCH(self):

        self.__procesar_solicitud()

    def do_DELETE(self):

        self.__procesar_solicitud()

    def do_HEAD(self):

        self.__procesar_solicitud()

    def do_OPTIONS(self):

        self.__procesar_solicitud()

    def send_error(
        self,
        code: int,
        message: str | None = None,
        explain: str | None = None
    ) -> None:

        try:

            estado = HTTPStatus(code)

        except ValueError:

            estado = HTTPStatus.INTERNAL_SERVER_ERROR

        respuesta = respuesta_error(
            estado.phrase,
            estado
        )

        self.__enviar_respuesta(respuesta)

    def log_message(
        self,
        format: str,
        *args: Any
    ) -> None:

        # No registrar documentos ni datos personales
        # contenidos en las rutas.

        logger.info(
            "Solicitud HTTP desde %s",
            self.client_address[0]
        )


def crear_servidor(
    enrutador: Enrutador,
    host: str = "127.0.0.1",
    puerto: int = 8000
) -> ThreadingHTTPServer:

    class ManejadorConfigurado(ManejadorHTTP):

        pass

    ManejadorConfigurado.enrutador = enrutador

    return ThreadingHTTPServer(
        (host, puerto),
        ManejadorConfigurado
    )