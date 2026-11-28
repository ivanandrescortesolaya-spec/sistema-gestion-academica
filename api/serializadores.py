from typing import Any

from personas.profesores import Profesor
from personas.aprendices import Aprendiz
from cursos.curso import Curso
from inscripciones.inscripcion import Inscripcion
from calificaciones.calificacion import Calificacion


def serializar_profesor(
    profesor: Profesor
) -> dict[str, Any]:

    return {
        "nombre": profesor.nombre,
        "documento": profesor.documento,
        "edad": profesor.edad,
        "profesion": profesor.profesion,
        "codigo": profesor.codigo,
        "especialidad": profesor.especialidad
    }


def serializar_aprendiz(
    aprendiz: Aprendiz
) -> dict[str, Any]:

    return {
        "nombre": aprendiz.nombre,
        "documento": aprendiz.documento,
        "edad": aprendiz.edad,
        "telefono": aprendiz.telefono,
        "correo": aprendiz.correo,
        "direccion": aprendiz.direccion
    }


def serializar_curso(
    curso: Curso
) -> dict[str, Any]:

    profesor = curso.profesor

    return {
        "codigo": curso.codigo,
        "nombre": curso.nombre,
        "descripcion": curso.descripcion,
        "duracion_horas": curso.duracion_horas,
        "modalidad": curso.modalidad,
        "profesor": (
            serializar_profesor(profesor)
            if profesor is not None
            else None
        )
    }


def serializar_inscripcion(
    inscripcion: Inscripcion
) -> dict[str, Any]:

    return {
        "codigo": inscripcion.codigo,
        "aprendiz": serializar_aprendiz(
            inscripcion.aprendiz
        ),
        "curso": serializar_curso(
            inscripcion.curso
        ),
        "fecha_inscripcion": (
            inscripcion.fecha_inscripcion.isoformat()
        ),
        "estado": inscripcion.estado
    }


def serializar_calificacion(
    calificacion: Calificacion
) -> dict[str, Any]:

    return {
        "codigo": calificacion.codigo,
        "inscripcion": serializar_inscripcion(
            calificacion.inscripcion
        ),
        "nota": calificacion.nota,
        "fecha": calificacion.fecha.isoformat()
    }