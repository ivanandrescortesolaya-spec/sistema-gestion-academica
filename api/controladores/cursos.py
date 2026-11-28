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
    validar_texto,
    validar_entero,
    validar_modalidad,
    validar_documento
)

from api.serializadores import (
    serializar_curso,
    serializar_aprendiz,
    serializar_inscripcion,
    serializar_calificacion
)

from gestion_academica import GestionAcademica
from cursos.curso import Curso


class ControladorCursos:

    def __init__(self, sistema: GestionAcademica):

        self.__sistema = sistema

    def __obtener_curso(
        self,
        parametros: dict[str, str]
    ) -> Curso:

        codigo = validar_codigo(
            parametros["codigo"]
        )

        curso = self.__sistema.buscar_curso(codigo)

        if curso is None:
            raise RecursoNoEncontrado(
                "Curso no encontrado"
            )

        return curso

    def listar(
        self,
        parametros: dict[str, str],
        datos: dict[str, Any]
    ) -> Respuesta:

        cursos = self.__sistema.listar_cursos()

        return respuesta_exitosa(
            [
                serializar_curso(curso)
                for curso in cursos
            ]
        )

    def buscar(
        self,
        parametros: dict[str, str],
        datos: dict[str, Any]
    ) -> Respuesta:

        curso = self.__obtener_curso(parametros)

        return respuesta_exitosa(
            serializar_curso(curso)
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
                "nombre",
                "descripcion",
                "duracion_horas",
                "modalidad"
            }
        )

        curso = Curso(
            codigo=validar_codigo(
                datos["codigo"]
            ),
            nombre=validar_texto(
                datos["nombre"], "nombre", 150
            ),
            descripcion=validar_texto(
                datos["descripcion"], "descripcion", 16000
            ),
            duracion_horas=validar_entero(
                datos["duracion_horas"],
                "duracion_horas",
                minimo=1
            ),
            modalidad=validar_modalidad(
                datos["modalidad"]
            )
        )

        if self.__sistema.buscar_curso(
            curso.codigo
        ) is not None:
            raise Conflicto(
                "El curso ya está registrado"
            )

        try:

            registrado = self.__sistema.registrar_curso(
                curso
            )

        except ValueError as error:

            raise Conflicto(str(error)) from error

        if not registrado:
            raise DatosInvalidos(
                "No fue posible registrar el curso"
            )

        return respuesta_creada(
            datos=serializar_curso(curso),
            mensaje="Curso registrado correctamente",
            ubicacion=(
                f"{PREFIJO_API}/cursos/{curso.codigo}"
            )
        )

    def asignar_profesor(
        self,
        parametros: dict[str, str],
        datos: dict[str, Any]
    ) -> Respuesta:

        validar_campos(datos, {"documento"})

        curso = self.__obtener_curso(parametros)

        documento = validar_documento(
            datos["documento"]
        )

        if self.__sistema.buscar_profesor(documento) is None:
            raise RecursoNoEncontrado(
                "Profesor no encontrado"
            )

        try:

            asignado = self.__sistema.asignar_profesor(
                curso.codigo,
                documento
            )

        except ValueError as error:

            raise Conflicto(str(error)) from error

        if not asignado:
            raise Conflicto(
                "No fue posible asignar el profesor"
            )

        curso_actualizado = self.__obtener_curso(
            parametros
        )

        return respuesta_exitosa(
            datos=serializar_curso(curso_actualizado),
            mensaje="Profesor asignado correctamente"
        )

    def consultar_aprendices(
        self,
        parametros: dict[str, str],
        datos: dict[str, Any]
    ) -> Respuesta:

        curso = self.__obtener_curso(parametros)

        aprendices = (
            self.__sistema.consultar_aprendices_curso(
                curso.codigo
            )
        )

        return respuesta_exitosa(
            [
                serializar_aprendiz(aprendiz)
                for aprendiz in aprendices
            ]
        )

    def consultar_inscripciones(
        self,
        parametros: dict[str, str],
        datos: dict[str, Any]
    ) -> Respuesta:

        curso = self.__obtener_curso(parametros)

        inscripciones = (
            self.__sistema.consultar_inscripciones_curso(
                curso.codigo
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

        curso = self.__obtener_curso(parametros)

        calificaciones = (
            self.__sistema.consultar_calificaciones_curso(
                curso.codigo
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

        curso = self.__obtener_curso(parametros)

        rendimiento = (
            self.__sistema.consultar_rendimiento_curso(
                curso.codigo
            )
        )

        return respuesta_exitosa(rendimiento)