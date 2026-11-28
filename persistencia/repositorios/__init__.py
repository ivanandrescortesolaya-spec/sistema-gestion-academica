"""Repositorios de persistencia MySQL."""

from .repositorio_profesores import RepositorioProfesores
from .repositorio_aprendices import RepositorioAprendices
from .repositorio_cursos import RepositorioCursos

__all__ = [
    "RepositorioProfesores",
    "RepositorioAprendices",
    "RepositorioCursos"
]
