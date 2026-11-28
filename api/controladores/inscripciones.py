from typing import Any

from api import PREFIJO_API

from api.excepciones import (
    RecursoNoEncontrado,
    Conflicto,
    DatosInvalidos
)

from api.respuestas import (
    Respuesta,
    respuesta_exitosa,
    respuesta_creada
)

from api.validaciones import (
    validar_campos,
    validar_codigo,
    validar_documento,
    validar_estado,
    validar_fecha
)

from api.serializadores import (
    serializar_inscripcion,
    serializar_calificacion
)

from gestion_academica import GestionAcademica
from inscripciones.inscripcion import Inscripcion


class ControladorInscripciones:

    def __init__(self, sistema: GestionAcademica):

        self.__sistema = sistema

    def __obtener_inscripcion(
        self,
        parametros: dict[str, str]
    ) -> Inscripcion:

        codigo = validar_codigo(
            parametros["codigo"]
        )

        inscripcion = self.__sistema.buscar_inscripcion(
            codigo
        )

        if inscripcion is None:
            raise RecursoNoEncontrado(
                "Inscripción no encontrada"
            )

        return inscripcion

    def listar(
        self,
        parametros: dict[str, str],
        datos: dict[str, Any]
    ) -> Respuesta:

        inscripciones = (
            self.__sistema.listar_inscripciones()
        )

        return respuesta_exitosa(
            [
                serializar_inscripcion(inscripcion)
                for inscripcion in inscripciones
            ]
        )

    def buscar(
        self,
        parametros: dict[str, str],
        datos: dict[str, Any]
    ) -> Respuesta:

        inscripcion = self.__obtener_inscripcion(
            parametros
        )

        return respuesta_exitosa(
            serializar_inscripcion(inscripcion)
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
                "documento_aprendiz",
                "codigo_curso"
            },
            {"fecha_inscripcion"}
        )

        codigo = validar_codigo(
            datos["codigo"]
        )

        documento = validar_documento(
            datos["documento_aprendiz"]
        )

        codigo_curso = validar_codigo(
            datos["codigo_curso"]
        )

        fecha = (
            validar_fecha(
                datos["fecha_inscripcion"],
                "fecha_inscripcion"
            )
            if "fecha_inscripcion" in datos
            else None
        )

        aprendiz = self.__sistema.buscar_aprendiz(
            documento
        )

        if aprendiz is None:
            raise RecursoNoEncontrado(
                "Aprendiz no encontrado"
            )

        curso = self.__sistema.buscar_curso(
            codigo_curso
        )

        if curso is None:
            raise RecursoNoEncontrado(
                "Curso no encontrado"
            )

        if self.__sistema.buscar_inscripcion(
            codigo
        ) is not None:
            raise Conflicto(
                "La inscripción ya está registrada"
            )

        inscripcion = Inscripcion(
            codigo=codigo,
            aprendiz=aprendiz,
            curso=curso,
            fecha_inscripcion=fecha
        )

        try:

            registrado = (
                self.__sistema.registrar_inscripcion(
                    inscripcion
                )
            )

        except ValueError as error:

            raise Conflicto(str(error)) from error

        if not registrado:
            raise Conflicto(
                "No fue posible registrar la inscripción"
            )

        return respuesta_creada(
            datos=serializar_inscripcion(inscripcion),
            mensaje="Inscripción registrada correctamente",
            ubicacion=(
                f"{PREFIJO_API}/inscripciones/{codigo}"
            )
        )

    def cambiar_estado(
        self,
        parametros: dict[str, str],
        datos: dict[str, Any]
    ) -> Respuesta:

        validar_campos(datos, {"estado"})

        inscripcion = self.__obtener_inscripcion(
            parametros
        )

        estado = validar_estado(
            datos["estado"]
        )

        if inscripcion.estado != "Activa":
            raise Conflicto(
                "Solo se pueden modificar inscripciones activas"
            )

        try:

            if estado == "Cancelada":

                actualizado = (
                    self.__sistema.cancelar_inscripcion(
                        inscripcion.codigo
                    )
                )

            else:

                actualizado = (
                    self.__sistema.finalizar_inscripcion(
                        inscripcion.codigo
                    )
                )

        except ValueError as error:

            raise Conflicto(str(error)) from error

        if not actualizado:
            raise Conflicto(
                "No fue posible actualizar la inscripción"
            )

        inscripcion_actualizada = (
            self.__obtener_inscripcion(parametros)
        )

        return respuesta_exitosa(
            datos=serializar_inscripcion(
                inscripcion_actualizada
            ),
            mensaje="Estado actualizado correctamente"
        )

    def consultar_calificaciones(
        self,
        parametros: dict[str, str],
        datos: dict[str, Any]
    ) -> Respuesta:

        inscripcion = self.__obtener_inscripcion(
            parametros
        )

        calificaciones = (
            self.__sistema.consultar_calificaciones_inscripcion(
                inscripcion.codigo
            )
        )

        return respuesta_exitosa(
            [
                serializar_calificacion(calificacion)
                for calificacion in calificaciones
            ]
        )

    def consultar_rendimiento(
        self,
        parametros: dict[str, str],
        datos: dict[str, Any]
    ) -> Respuesta:

        inscripcion = self.__obtener_inscripcion(
            parametros
        )

        rendimiento = (
            self.__sistema.consultar_rendimiento_inscripcion(
                inscripcion.codigo
            )
        )

        return respuesta_exitosa(rendimiento)

    def calcular_promedio(
        self,
        parametros: dict[str, str],
        datos: dict[str, Any]
    ) -> Respuesta:

        inscripcion = self.__obtener_inscripcion(
            parametros
        )

        try:

            promedio = self.__sistema.calcular_promedio(
                inscripcion.codigo
            )

            estado = (
                self.__sistema.obtener_estado_academico(
                    inscripcion.codigo
                )
            )

        except ValueError as error:

            raise DatosInvalidos(str(error)) from error

        return respuesta_exitosa({
            "inscripcion": inscripcion.codigo,
            "promedio": round(promedio, 2),
            "estado": estado
        })