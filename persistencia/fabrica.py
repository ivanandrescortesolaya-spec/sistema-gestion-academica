from gestion_academica import GestionAcademica

from persistencia.configuracion import ConfiguracionBD
from persistencia.conexion import ConexionMySQL
from persistencia.excepciones import ErrorConexion

from persistencia.repositorios import (
    RepositorioProfesores,
    RepositorioAprendices,
    RepositorioCursos,
    RepositorioInscripciones,
    RepositorioCalificaciones
)


def crear_sistema_mysql(
    pruebas: bool = False
) -> GestionAcademica:

    configuracion = ConfiguracionBD.desde_entorno(
        pruebas=pruebas
    )

    conexion = ConexionMySQL(configuracion)

    if not conexion.verificar_conexion():
        raise ErrorConexion(
            "No fue posible verificar la conexión"
        )

    return GestionAcademica(
        profesores=RepositorioProfesores(conexion),
        aprendices=RepositorioAprendices(conexion),
        cursos=RepositorioCursos(conexion),
        inscripciones=RepositorioInscripciones(conexion),
        calificaciones=RepositorioCalificaciones(conexion),
        entidades_persistidas=True
    )
