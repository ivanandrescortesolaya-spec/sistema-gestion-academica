"""Repositorios de persistencia MySQL."""

from .repositorio_profesores import RepositorioProfesores
from .repositorio_aprendices import RepositorioAprendices
from .repositorio_cursos import RepositorioCursos
from .repositorio_inscripciones import RepositorioInscripciones
from .repositorio_calificaciones import RepositorioCalificaciones

__all__ = [
    "RepositorioProfesores",
    "RepositorioAprendices",
    "RepositorioCursos",
    "RepositorioInscripciones",
    "RepositorioCalificaciones"
]
