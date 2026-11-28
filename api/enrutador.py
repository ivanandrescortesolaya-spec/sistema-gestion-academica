import re

from dataclasses import dataclass
from typing import Any, Callable
from urllib.parse import unquote, urlsplit

from api.excepciones import (
    RecursoNoEncontrado,
    MetodoNoPermitido,
    SolicitudInvalida
)

from api.respuestas import Respuesta


Controlador = Callable[
    [dict[str, str], dict[str, Any]],
    Respuesta
]


@dataclass(frozen=True, slots=True)
class Ruta:

    metodo: str
    patron: re.Pattern[str]
    controlador: Controlador


class Enrutador:

    def __init__(self):

        self.__rutas: list[Ruta] = []

    @staticmethod
    def __compilar_ruta(
        ruta: str
    ) -> re.Pattern[str]:

        if not ruta.startswith("/"):
            raise ValueError(
                "La ruta debe comenzar con /"
            )

        segmentos = ruta.strip("/").split("/")

        patrones: list[str] = []

        for segmento in segmentos:

            parametro = re.fullmatch(
                r"\{([A-Za-z_][A-Za-z0-9_]*)\}",
                segmento
            )

            if parametro:

                nombre = parametro.group(1)

                patrones.append(
                    f"(?P<{nombre}>[^/]+)"
                )

            else:

                patrones.append(
                    re.escape(segmento)
                )

        expresion = (
            "/" + "/".join(patrones)
        )

        return re.compile(
            "^" + expresion + "$"
        )

    def registrar(
        self,
        metodo: str,
        ruta: str,
        controlador: Controlador
    ) -> None:

        metodo = metodo.upper()

        patron = self.__compilar_ruta(ruta)

        for registrada in self.__rutas:

            if (
                registrada.metodo == metodo
                and registrada.patron.pattern
                == patron.pattern
            ):
                raise ValueError(
                    f"Ruta duplicada: {metodo} {ruta}"
                )

        self.__rutas.append(
            Ruta(
                metodo=metodo,
                patron=patron,
                controlador=controlador
            )
        )

    def resolver(
        self,
        metodo: str,
        url: str,
        datos: dict[str, Any] | None = None
    ) -> Respuesta:

        metodo = metodo.upper()

        try:

            componentes = urlsplit(url)

            if componentes.scheme or componentes.netloc:
                raise ValueError(
                    "URL absoluta no permitida"
                )

            ruta = unquote(
                componentes.path,
                errors="strict"
            )

        except (ValueError, UnicodeError) as error:

            raise SolicitudInvalida(
                "La URL no es válida"
            ) from error

        if not ruta.startswith("/"):
            raise SolicitudInvalida(
                "La ruta no es válida"
            )

        ruta = ruta.rstrip("/") or "/"

        permitidos: set[str] = set()

        for registrada in self.__rutas:

            coincidencia = registrada.patron.fullmatch(
                ruta
            )

            if coincidencia is None:
                continue

            permitidos.add(
                registrada.metodo
            )

            if registrada.metodo == metodo:

                return registrada.controlador(
                    coincidencia.groupdict(),
                    datos or {}
                )

        if permitidos:

            raise MetodoNoPermitido(
                tuple(sorted(permitidos))
            )

        raise RecursoNoEncontrado(
            "La ruta solicitada no existe"
        )

    @property
    def cantidad_rutas(self) -> int:

        return len(self.__rutas)