
from collections.abc import MutableSequence
from typing import Protocol, Optional

from personas.aprendices import Aprendiz


class IGestionAprendices(Protocol):

    def registrar(self, aprendiz: Aprendiz) -> bool:
        ...

    def buscar_documento(
        self, documento: int
    ) -> Optional[Aprendiz]:
        ...

    def listar(self) -> list[Aprendiz]:
        ...


class Gestion_aprendices:

    def __init__(
    self,
    almacenamiento: Optional[MutableSequence[Aprendiz]] = None
):
        self.__aprendices: MutableSequence[Aprendiz] = (
        almacenamiento if almacenamiento is not None else []
    )

    def buscar_documento(
        self, documento: int
    ) -> Optional[Aprendiz]:

        for aprendiz in self.__aprendices:
            if aprendiz.documento == documento:
                return aprendiz

        return None

    def registrar(self, aprendiz: Aprendiz) -> bool:

        if not isinstance(aprendiz, Aprendiz):
            raise ValueError(
                "Debes registrar un aprendiz válido"
            )

        if self.buscar_documento(
            aprendiz.documento
        ) is not None:
            raise ValueError(
                "Ya existe un aprendiz con ese documento"
            )

        self.__aprendices.append(aprendiz)
        return True

    def mostrar(self, aprendiz: Aprendiz):
        print("Información del aprendiz:")
        print(aprendiz.mostrar_informacion())

    def listar(self) -> list[Aprendiz]:
        return list(self.__aprendices)
