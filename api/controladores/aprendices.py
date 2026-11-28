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
    validar_documento,
    validar_texto,
    validar_entero
)

from api.serializadores import (
    serializar_aprendiz,
    serializar_curso,
    serializar_inscripcion,
    serializar_calificacion
)

from gestion_academica import GestionAcademica
from personas.aprendices import Aprendiz


class ControladorAprendices:

    def __init__(self, sistema: GestionAcademica):

        self.__sistema = sistema

    def __obtener_aprendiz(
        self,
        parametros: dict[str, str]
    ) -> Aprendiz:

        documento = validar_documento(
            parametros["documento"]
        )

        aprendiz = self.__sistema.buscar_aprendiz(
            documento
        )

        if aprendiz is None:
            raise RecursoNoEncontrado(
                "Aprendiz no encontrado"
            )

        return aprendiz

    def listar(
        self,
        parametros: dict[str, str],
        datos: dict[str, Any]
    ) -> Respuesta:

        aprendices = self.__sistema.listar_aprendices()

        return respuesta_exitosa(
            [
                serializar_aprendiz(aprendiz)
                for aprendiz in aprendices
            ]
        )

    def buscar(
        self,
        parametros: dict[str, str],
        datos: dict[str, Any]
    ) -> Respuesta:

        aprendiz = self.__obtener_aprendiz(
            parametros
        )

        return respuesta_exitosa(
            serializar_aprendiz(aprendiz)
        )

    def registrar(
        self,
        parametros: dict[str, str],
        datos: dict[str, Any]
    ) -> Respuesta:

        validar_campos(
            datos,
            {
                "nombre",
                "documento",
                "edad",
                "telefono",
                "correo",
                "direccion"
            }
        )

        try:

            aprendiz = Aprendiz(
                nombre=validar_texto(
                    datos["nombre"], "nombre", 150
                ),
                documento=validar_documento(
                    datos["documento"]
                ),
                edad=validar_entero(
                    datos["edad"], "edad"
                ),
                telefono=validar_texto(
                    datos["telefono"], "telefono", 20
                ),
                correo=validar_texto(
                    datos["correo"], "correo", 254
                ),
                direccion=validar_texto(
                    datos["direccion"], "direccion", 200
                )
            )

        except ValueError as error:

            raise DatosInvalidos(str(error)) from error

        if self.__sistema.buscar_aprendiz(
            aprendiz.documento
        ) is not None:
            raise Conflicto(
                "El aprendiz ya está registrado"
            )

        try:

            registrado = self.__sistema.registrar_aprendiz(
                aprendiz
            )

        except ValueError as error:

            raise Conflicto(str(error)) from error

        if not registrado:
            raise DatosInvalidos(
                "No fue posible registrar el aprendiz"
            )

        return respuesta_creada(
            datos=serializar_aprendiz(aprendiz),
            mensaje="Aprendiz registrado correctamente",
            ubicacion=(
                f"{PREFIJO_API}/aprendices/"
                f"{aprendiz.documento}"
            )
        )

    def consultar_cursos(
        self,
        parametros: dict[str, str],
        datos: dict[str, Any]
    ) -> Respuesta:

        aprendiz = self.__obtener_aprendiz(parametros)

        cursos = self.__sistema.consultar_cursos_aprendiz(
            aprendiz.documento
        )

        return respuesta_exitosa(
            [
                serializar_curso(curso)
                for curso in cursos
            ]
        )

    def consultar_inscripciones(
        self,
        parametros: dict[str, str],
        datos: dict[str, Any]
    ) -> Respuesta:

        aprendiz = self.__obtener_aprendiz(parametros)

        inscripciones = (
            self.__sistema.consultar_inscripciones_aprendiz(
                aprendiz.documento
            )
        )

        return respuesta_exitosa(
            [
                serializar_inscripcion(inscripcion)
                for inscripcion in inscripciones
            ]
        )

    def consultar_calificaciones(
        self,
        parametros: dict[str, str],
        datos: dict[str, Any]
    ) -> Respuesta:

        aprendiz = self.__obtener_aprendiz(parametros)

        calificaciones = (
            self.__sistema.consultar_calificaciones_aprendiz(
                aprendiz.documento
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

        aprendiz = self.__obtener_aprendiz(parametros)

        rendimiento = (
            self.__sistema.consultar_rendimiento_aprendiz(
                aprendiz.documento
            )
        )

        return respuesta_exitosa(rendimiento)