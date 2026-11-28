import re

from datetime import date
from decimal import Decimal
from typing import Any

from api.excepciones import DatosInvalidos


def validar_campos(
    datos: dict[str, Any],
    obligatorios: set[str],
    opcionales: set[str] | None = None
) -> None:

    permitidos = obligatorios | (opcionales or set())

    faltantes = obligatorios - datos.keys()

    if faltantes:
        raise DatosInvalidos(
            "Campos obligatorios faltantes: "
            + ", ".join(sorted(faltantes))
        )

    desconocidos = datos.keys() - permitidos

    if desconocidos:
        raise DatosInvalidos(
            "Campos no permitidos: "
            + ", ".join(sorted(desconocidos))
        )


def validar_texto(
    valor: Any,
    campo: str,
    maximo: int | None = None
) -> str:

    if not isinstance(valor, str):
        raise DatosInvalidos(
            f"El campo {campo} debe ser texto"
        )

    valor = valor.strip()

    if not valor:
        raise DatosInvalidos(
            f"El campo {campo} no puede estar vacío"
        )

    if maximo is not None and len(valor) > maximo:
        raise DatosInvalidos(
            f"El campo {campo} admite máximo "
            f"{maximo} caracteres"
        )

    return valor


def validar_entero(
    valor: Any,
    campo: str,
    minimo: int = 0,
    maximo: int = 4294967295
) -> int:

    if type(valor) is not int:
        raise DatosInvalidos(
            f"El campo {campo} debe ser un entero"
        )

    if not minimo <= valor <= maximo:
        raise DatosInvalidos(
            f"El campo {campo} está fuera del rango permitido"
        )

    return valor


def validar_documento(valor: Any) -> int:

    if isinstance(valor, str):

        if not re.fullmatch(r"[0-9]{1,20}", valor):
            raise DatosInvalidos(
                "El documento debe contener entre "
                "1 y 20 dígitos"
            )

        if valor.startswith("0"):
            raise DatosInvalidos(
                "El documento no admite ceros iniciales"
            )

        valor = int(valor)

    return validar_entero(
        valor,
        "documento",
        minimo=1,
        maximo=10**20 - 1
    )


def validar_codigo(valor: Any) -> str:

    codigo = validar_texto(
        valor,
        "codigo",
        maximo=30
    )

    if not re.fullmatch(
        r"[A-Za-z0-9_-]+",
        codigo
    ):
        raise DatosInvalidos(
            "El código solo admite letras, números, "
            "guiones y guiones bajos"
        )

    return codigo


def validar_nota(valor: Any) -> float:

    if type(valor) not in (int, float):
        raise DatosInvalidos(
            "La nota debe ser numérica"
        )

    nota = Decimal(str(valor))

    if not nota.is_finite():
        raise DatosInvalidos(
            "La nota debe ser un número finito"
        )

    if not Decimal("0") <= nota <= Decimal("5"):
        raise DatosInvalidos(
            "La nota debe estar entre 0.0 y 5.0"
        )

    if nota != nota.quantize(Decimal("0.01")):
        raise DatosInvalidos(
            "La nota admite máximo dos decimales"
        )

    return float(nota)


def validar_modalidad(valor: Any) -> str:

    modalidad = validar_texto(
        valor,
        "modalidad",
        maximo=50
    ).lower()

    if modalidad not in (
        "titulada",
        "complementaria"
    ):
        raise DatosInvalidos(
            "La modalidad debe ser titulada "
            "o complementaria"
        )

    return modalidad


def validar_estado(valor: Any) -> str:

    estado = validar_texto(
        valor,
        "estado",
        maximo=15
    )

    if estado not in (
        "Cancelada",
        "Finalizada"
    ):
        raise DatosInvalidos(
            "El estado debe ser Cancelada o Finalizada"
        )

    return estado


def validar_fecha(
    valor: Any,
    campo: str
) -> date:

    texto = validar_texto(
        valor,
        campo,
        maximo=10
    )

    if not re.fullmatch(
        r"[0-9]{4}-[0-9]{2}-[0-9]{2}",
        texto
    ):
        raise DatosInvalidos(
            f"El campo {campo} debe tener "
            "formato AAAA-MM-DD"
        )

    try:
        return date.fromisoformat(texto)

    except ValueError as error:
        raise DatosInvalidos(
            f"El campo {campo} contiene una fecha inválida"
        ) from error