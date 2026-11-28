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
    serializar_profesor,
    serializar_curso,
    serializar_aprendiz
)

from gestion_academica import GestionAcademica
from personas.profesores import Profesor


class ControladorProfesores:

    def __init__(self, sistema: GestionAcademica):

        self.__sistema = sistema

    def listar(
        self,
        parametros: dict[str, str],
        datos: dict[str, Any]
    ) -> Respuesta:

        profesores = self.__sistema.listar_profesores()

        return respuesta_exitosa(
            datos=[
                serializar_profesor(profesor)
                for profesor in profesores
            ]
        )

    def buscar(
        self,
        parametros: dict[str, str],
        datos: dict[str, Any]
    ) -> Respuesta:

        documento = validar_documento(
            parametros["documento"]
        )

        profesor = self.__sistema.buscar_profesor(
            documento
        )

        if profesor is None:
            raise RecursoNoEncontrado(
                "Profesor no encontrado"
            )

        return respuesta_exitosa(
            serializar_profesor(profesor)
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
                "profesion",
                "codigo",
                "especialidad"
            }
        )

        profesor = Profesor(
            nombre=validar_texto(
                datos["nombre"], "nombre", 150
            ),
            documento=validar_documento(
                datos["documento"]
            ),
            edad=validar_entero(
                datos["edad"], "edad"
            ),
            profesion=validar_texto(
                datos["profesion"], "profesion", 100
            ),
            codigo=validar_entero(
                datos["codigo"], "codigo", minimo=1
            ),
            especialidad=validar_texto(
                datos["especialidad"], "especialidad", 100
            )
        )

        if self.__sistema.buscar_profesor(
            profesor.documento
        ) is not None:
            raise Conflicto(
                "El profesor ya está registrado"
            )

        try:

            registrado = self.__sistema.registrar_profesor(
                profesor
            )

        except ValueError as error:

            raise Conflicto(str(error)) from error

        if not registrado:
            raise DatosInvalidos(
                "No fue posible registrar el profesor"
            )

        return respuesta_creada(
            datos=serializar_profesor(profesor),
            mensaje="Profesor registrado correctamente",
            ubicacion=(
                f"{PREFIJO_API}/profesores/"
                f"{profesor.documento}"
            )
        )

    def consultar_cursos(
        self,
        parametros: dict[str, str],
        datos: dict[str, Any]
    ) -> Respuesta:

        documento = validar_documento(
            parametros["documento"]
        )

        if self.__sistema.buscar_profesor(documento) is None:
            raise RecursoNoEncontrado(
                "Profesor no encontrado"
            )

        cursos = self.__sistema.consultar_cursos_profesor(
            documento
        )

        return respuesta_exitosa(
            [
                serializar_curso(curso)
                for curso in cursos
            ]
        )

    def consultar_aprendices(
        self,
        parametros: dict[str, str],
        datos: dict[str, Any]
    ) -> Respuesta:

        documento = validar_documento(
            parametros["documento"]
        )

        if self.__sistema.buscar_profesor(documento) is None:
            raise RecursoNoEncontrado(
                "Profesor no encontrado"
            )

        registros = (
            self.__sistema.consultar_aprendices_profesor(
                documento
            )
        )

        resultado = []

        for registro in registros:

            resultado.append({
                "curso": serializar_curso(
                    registro["curso"]
                ),
                "aprendices": [
                    serializar_aprendiz(aprendiz)
                    for aprendiz in registro["aprendices"]
                ]
            })

        return respuesta_exitosa(resultado)