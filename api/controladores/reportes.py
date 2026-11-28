from typing import Any

from api.respuestas import (
    Respuesta,
    respuesta_exitosa
)

from gestion_academica import GestionAcademica


class ControladorReportes:

    def __init__(self, sistema: GestionAcademica):

        self.__sistema = sistema

    def resumen(
        self,
        parametros: dict[str, str],
        datos: dict[str, Any]
    ) -> Respuesta:

        resumen = self.__sistema.obtener_resumen()

        return respuesta_exitosa(
            datos=resumen,
            mensaje="Resumen académico generado correctamente"
        )

    def calificaciones(
        self,
        parametros: dict[str, str],
        datos: dict[str, Any]
    ) -> Respuesta:

        reporte = (
            self.__sistema.generar_reporte_calificaciones()
        )

        return respuesta_exitosa(
            datos={
                "reporte": reporte
            },
            mensaje="Reporte generado correctamente"
        )