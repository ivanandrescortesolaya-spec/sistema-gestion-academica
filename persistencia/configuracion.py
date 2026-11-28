import os

from dataclasses import dataclass, field
from pathlib import Path
from dotenv import load_dotenv

from persistencia.excepciones import ErrorConfiguracion


@dataclass(frozen=True, slots=True)
class ConfiguracionBD:
    host: str
    puerto: int
    base_datos: str
    usuario: str
    contrasena: str = field(repr=False)

    @classmethod
    def desde_entorno(
        cls,
        pruebas: bool = False
    ) -> "ConfiguracionBD":

        ruta_env = (
            Path(__file__).resolve().parent.parent
            / "infra"
            / ".env"
        )

        load_dotenv(ruta_env, override=False)

        host = os.getenv("DB_HOST", "127.0.0.1")

        try:
            puerto = int(os.getenv("DB_PORT", "3307"))
        except ValueError as error:
            raise ErrorConfiguracion(
                "El puerto debe ser un número entero."
            ) from error

        if not 1 <= puerto <= 65535:
            raise ErrorConfiguracion(
                "Puerto fuera del rango permitido."
            )

        if pruebas:
            base_datos = os.getenv("DB_TEST_NAME")
            usuario = os.getenv("DB_TEST_USER")
            contrasena = os.getenv("DB_TEST_PASSWORD")

            base_esperada = "sistema_gestion_academica_test"
            usuario_esperado = "academic_test_user"

        else:
            base_datos = os.getenv("DB_NAME")
            usuario = os.getenv("DB_USER")
            contrasena = os.getenv("MYSQL_PASSWORD")

            base_esperada = "sistema_gestion_academica"
            usuario_esperado = "academic_user"

        if not all((host, base_datos, usuario, contrasena)):
            raise ErrorConfiguracion(
                "Configuración de MySQL incompleta."
            )

        if usuario == "root":
            raise ErrorConfiguracion(
                "No se permite utilizar root."
            )

        if base_datos != base_esperada:
            raise ErrorConfiguracion(
                "Base de datos incorrecta."
            )

        if usuario != usuario_esperado:
            raise ErrorConfiguracion(
                "Usuario incorrecto para el ambiente."
            )

        return cls(
            host=host,
            puerto=puerto,
            base_datos=base_datos,
            usuario=usuario,
            contrasena=contrasena
        )
