"""Controladores de la API REST académica."""

from api.controladores.profesores import (
    ControladorProfesores
)

from api.controladores.aprendices import (
    ControladorAprendices
)

from api.controladores.cursos import (
    ControladorCursos
)

from api.controladores.inscripciones import (
    ControladorInscripciones
)

from api.controladores.calificaciones import (
    ControladorCalificaciones
)

from api.controladores.reportes import (
    ControladorReportes
)


__all__ = [
    "ControladorProfesores",
    "ControladorAprendices",
    "ControladorCursos",
    "ControladorInscripciones",
    "ControladorCalificaciones",
    "ControladorReportes"
]