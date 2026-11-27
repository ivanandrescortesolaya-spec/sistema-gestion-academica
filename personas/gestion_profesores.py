
from typing import Protocol, Optional

from personas.profesores import Profesor


class IGestionProfesores(Protocol):

    def registrar(self, profesor: Profesor) -> bool:
        ...

    def buscar_por_documento(
        self, documento: int
    ) -> Optional[Profesor]:
        ...

    def listar(self) -> list[Profesor]:
        ...


class Gestion_profesores:

    def __init__(self):
        self.__profesores: list[Profesor] = []

    def buscar_por_documento(
        self, documento: int
    ) -> Optional[Profesor]:

        for profesor in self.__profesores:
            if profesor.documento == documento:
                return profesor

        return None

    def registrar(self, profesor: Profesor) -> bool:

        if not isinstance(profesor, Profesor):
            raise ValueError(
                "Debes registrar un profesor válido"
            )

        if self.buscar_por_documento(
            profesor.documento
        ) is not None:
            raise ValueError(
                "Ya existe un profesor con ese documento"
            )

        self.__profesores.append(profesor)
        return True

    def mostrar(self, profesor: Profesor):
        print("Información del profesor:")
        print(profesor.mostrar_informacion())

    def listar(self) -> list[Profesor]:
        return self.__profesores.copy()
