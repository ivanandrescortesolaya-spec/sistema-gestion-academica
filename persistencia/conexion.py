
from contextlib import contextmanager
from functools import wraps
from random import uniform
from time import sleep
from typing import Callable, ParamSpec, TypeVar

import mysql.connector

from mysql.connector import Error, IntegrityError

from persistencia.configuracion import ConfiguracionBD
from persistencia.excepciones import (
    ErrorConexion,
    ErrorOperacion,
    ErrorIntegridad,
    ErrorInterbloqueo
)


P = ParamSpec("P")
R = TypeVar("R")


def reintentar_interbloqueo(
    operacion: Callable[P, R]
) -> Callable[P, R]:

    @wraps(operacion)
    def ejecutar(
        *args: P.args,
        **kwargs: P.kwargs
    ) -> R:

        maximo_intentos = 5

        for intento in range(maximo_intentos):

            try:
                return operacion(*args, **kwargs)

            except ErrorInterbloqueo:

                if intento == maximo_intentos - 1:
                    raise

                espera = (
                    0.025 * (2 ** intento)
                    + uniform(0.0, 0.025)
                )

                sleep(espera)

        raise RuntimeError(
            "Se agotaron los intentos de la operación"
        )

    return ejecutar


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

            if isinstance(error, Error):

                if error.errno == 1213:

                    raise ErrorInterbloqueo(
                        "Interbloqueo de transacciones "
                        "en MySQL (código 1213)."
                    ) from error

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
