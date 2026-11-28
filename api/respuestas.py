import json

from dataclasses import dataclass, field
from http import HTTPStatus
from typing import Any


@dataclass(slots=True)
class Respuesta:

    estado: HTTPStatus
    contenido: dict[str, Any]

    encabezados: dict[str, str] = field(
        default_factory=dict
    )

    def convertir_json(self) -> bytes:

        return json.dumps(
            self.contenido,
            ensure_ascii=False,
            allow_nan=False
        ).encode("utf-8")


def respuesta_exitosa(
    datos: Any = None,
    mensaje: str = "Operación exitosa",
    estado: HTTPStatus = HTTPStatus.OK,
    encabezados: dict[str, str] | None = None
) -> Respuesta:

    return Respuesta(
        estado=estado,
        contenido={
            "exito": True,
            "mensaje": mensaje,
            "datos": datos
        },
        encabezados=encabezados or {}
    )


def respuesta_creada(
    datos: Any,
    mensaje: str = "Recurso creado correctamente",
    ubicacion: str | None = None
) -> Respuesta:

    encabezados = {}

    if ubicacion is not None:
        encabezados["Location"] = ubicacion

    return respuesta_exitosa(
        datos=datos,
        mensaje=mensaje,
        estado=HTTPStatus.CREATED,
        encabezados=encabezados
    )


def respuesta_error(
    mensaje: str,
    estado: HTTPStatus,
    encabezados: dict[str, str] | None = None
) -> Respuesta:

    return Respuesta(
        estado=estado,
        contenido={
            "exito": False,
            "mensaje": mensaje,
            "datos": None
        },
        encabezados=encabezados or {}
    )