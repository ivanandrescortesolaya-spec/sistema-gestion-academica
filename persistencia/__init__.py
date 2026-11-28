"""Capa de persistencia del Sistema de Gestión Académica."""

from persistencia.configuracion import ConfiguracionBD
from persistencia.conexion import ConexionMySQL

__all__ = [
    "ConfiguracionBD",
    "ConexionMySQL"
]
