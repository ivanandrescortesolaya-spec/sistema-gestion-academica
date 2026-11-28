from typing import Any

from api import PREFIJO_API

from api.excepciones import (
    RecursoNoEncontrado,
    Conflicto
)

from api.respuestas import (
    Respuesta,
    respuesta_exitosa,
    respuesta_creada
)

from api.validaciones import (
    validar_campos,
    validar_codigo,
    validar_nota,
    validar_fecha
)

from api.serializadores import (
    serializar_calificacion
)

from gestion_academica import GestionAcademica
from calificaciones.calificacion import Calificacion


class ControladorCalificaciones:

    def __init__(self, sistema: GestionAcademica):

        self.__sistema = sistema

    def __obtener_calificacion(
        self,
        parametros: dict[str, str]
    ) -> Calificacion:

        codigo = validar_codigo(
            parametros["codigo"]
        )

        calificacion = (
            self.__sistema.buscar_calificacion(
                codigo
            )
        )

        if calificacion is None:
            raise RecursoNoEncontrado(
                "Calificación no encontrada"
            )

        return calificacion

    def listar(
        self,
        parametros: dict[str, str],
        datos: dict[str, Any]
    ) -> Respuesta:

        calificaciones = (
            self.__sistema.listar_calificaciones()
        )

        return respuesta_exitosa(
            [
                serializar_calificacion(calificacion)
                for calificacion in calificaciones
            ]
        )

    def buscar(
        self,
        parametros: dict[str, str],
        datos: dict[str, Any]
    ) -> Respuesta:

        calificacion = self.__obtener_calificacion(
            parametros
        )

        return respuesta_exitosa(
            serializar_calificacion(calificacion)
        )

    def registrar(
        self,
        parametros: dict[str, str],
        datos: dict[str, Any]
    ) -> Respuesta:

        validar_campos(
            datos,
            {
                "codigo",
                "codigo_inscripcion",
                "nota"
            },
            {"fecha"}
        )

        codigo = validar_codigo(
            datos["codigo"]
        )

        codigo_inscripcion = validar_codigo(
            datos["codigo_inscripcion"]
        )

        nota = validar_nota(
            datos["nota"]
        )

        fecha = (
            validar_fecha(datos["fecha"], "fecha")
            if "fecha" in datos
            else None
        )

        inscripcion = (
            self.__sistema.buscar_inscripcion(
                codigo_inscripcion
            )
        )

        if inscripcion is None:
            raise RecursoNoEncontrado(
                "Inscripción no encontrada"
            )

        if inscripcion.estado != "Activa":
            raise Conflicto(
                "La inscripción debe estar activa"
            )

        if self.__sistema.buscar_calificacion(
            codigo
        ) is not None:
            raise Conflicto(
                "La calificación ya está registrada"
            )

        calificacion = Calificacion(
            codigo=codigo,
            inscripcion=inscripcion,
            nota=nota,
            fecha=fecha
        )

        try:

            registrado = (
                self.__sistema.registrar_calificacion(
                    calificacion
                )
            )

        except ValueError as error:

            raise Conflicto(str(error)) from error

        if not registrado:
            raise Conflicto(
                "No fue posible registrar la calificación"
            )

        return respuesta_creada(
            datos=serializar_calificacion(calificacion),
            mensaje="Calificación registrada correctamente",
            ubicacion=(
                f"{PREFIJO_API}/calificaciones/{codigo}"
            )
        )

    def modificar(
        self,
        parametros: dict[str, str],
        datos: dict[str, Any]
    ) -> Respuesta:

        validar_campos(datos, {"nota"})

        calificacion = self.__obtener_calificacion(
            parametros
        )

        nota = validar_nota(
            datos["nota"]
        )

        inscripcion = (
            self.__sistema.buscar_inscripcion(
                calificacion.inscripcion.codigo
            )
        )

        if inscripcion is None:
            raise RecursoNoEncontrado(
                "Inscripción no encontrada"
            )

        if inscripcion.estado != "Activa":
            raise Conflicto(
                "No se pueden modificar calificaciones "
                "de una inscripción inactiva"
            )

        try:

            actualizado = (
                self.__sistema.modificar_calificacion(
                    calificacion.codigo,
                    nota
                )
            )

        except ValueError as error:

            raise Conflicto(str(error)) from error

        if not actualizado:
            raise Conflicto(
                "No fue posible modificar la calificación"
            )

        calificacion_actualizada = (
            self.__obtener_calificacion(parametros)
        )

        return respuesta_exitosa(
            datos=serializar_calificacion(
                calificacion_actualizada
            ),
            mensaje="Calificación modificada correctamente"
        )