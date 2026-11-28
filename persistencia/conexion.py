from contextlib import contextmanager

import mysql.connector

from mysql.connector import Error, IntegrityError

from persistencia.configuracion import ConfiguracionBD
from persistencia.excepciones import (
    ErrorConexion,
    ErrorOperacion,
    ErrorIntegridad
)


class ConexionMySQL:

    def __init__(self, configuracion: ConfiguracionBD):
        self.__configuracion = configuracion

    def conectar(self):
        try:
            return mysql.connector.connect(
                host=self.__configuracion.host,
                port=self.__configuracion.puerto,
                database=self.__configuracion.base_datos,
                user=self.__configuracion.usuario,
                password=self.__configuracion.contrasena,
                charset="utf8mb4",
                autocommit=False,
                connection_timeout=10
            )

        except Error as error:
            raise ErrorConexion(
                f"No fue posible conectar con MySQL "
                f"(código {error.errno})."
            ) from error

    @contextmanager
    def transaccion(self):
        conexion = self.conectar()

        try:
            yield conexion
            conexion.commit()

        except BaseException as error:
            try:
                conexion.rollback()
            except Error:
                pass

            if isinstance(error, IntegrityError):
                raise ErrorIntegridad(
                    f"Error de integridad "
                    f"(código {error.errno})."
                ) from error

            if isinstance(error, Error):
                raise ErrorOperacion(
                    f"Error SQL (código {error.errno})."
                ) from error

            raise

        finally:
            conexion.close()

    def verificar_conexion(self) -> bool:
        with self.transaccion() as conexion:
            cursor = conexion.cursor()

            try:
                cursor.execute("SELECT 1")
                return cursor.fetchone() == (1,)

            finally:
                cursor.close()
