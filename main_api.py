import argparse
import logging

from api import PREFIJO_API

from api.rutas import crear_enrutador
from api.servidor import crear_servidor

from persistencia.fabrica import crear_sistema_mysql

from persistencia.excepciones import ErrorPersistencia


def main() -> int:

    parser = argparse.ArgumentParser(
        description="API REST del Sistema de Gestión Académica"
    )

    parser.add_argument(
        "--puerto",
        type=int,
        default=8000,
        help="Puerto HTTP de la API"
    )

    parser.add_argument(
        "--pruebas",
        action="store_true",
        help="Utilizar la base de datos de pruebas"
    )

    argumentos = parser.parse_args()

    if not 1 <= argumentos.puerto <= 65535:

        parser.error(
            "El puerto debe estar entre 1 y 65535"
        )

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s"
    )

    host = "127.0.0.1"

    try:

        sistema = crear_sistema_mysql(
            pruebas=argumentos.pruebas
        )

        enrutador = crear_enrutador(sistema)

        servidor = crear_servidor(
            enrutador=enrutador,
            host=host,
            puerto=argumentos.puerto
        )

    except ErrorPersistencia as error:

        print(
            f"No fue posible iniciar la API: {error}"
        )

        return 1

    except OSError as error:

        print(
            f"No fue posible iniciar el servidor: {error}"
        )

        return 1

    ambiente = (
        "PRUEBAS"
        if argumentos.pruebas
        else "PRINCIPAL"
    )

    url = (
        f"http://{host}:"
        f"{argumentos.puerto}"
        f"{PREFIJO_API}"
    )

    print("\n" + "=" * 60)

    print("API REST - SISTEMA DE GESTIÓN ACADÉMICA")

    print("=" * 60)

    print("Conexión con MySQL: establecida")

    print(f"Ambiente: {ambiente}")

    print(f"URL base: {url}")

    print(f"Endpoints: {enrutador.cantidad_rutas}")

    print(f"Estado del servidor: {url}/salud")

    print("Presiona Ctrl+C para detener el servidor")

    print("=" * 60 + "\n")

    try:

        servidor.serve_forever()

    except KeyboardInterrupt:

        print("\nDeteniendo servidor HTTP...")

    finally:

        servidor.server_close()

        print("Servidor detenido correctamente")

    return 0


if __name__ == "__main__":

    raise SystemExit(main())