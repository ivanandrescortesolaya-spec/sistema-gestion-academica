
from collections.abc import MutableSequence
from typing import Protocol, Optional

from inscripciones.inscripcion import Inscripcion


class IGestionInscripciones(Protocol):

    def registrar(self, inscripcion: Inscripcion) -> bool:
        ...

    def buscar_por_codigo(
        self, codigo: str
    ) -> Optional[Inscripcion]:
        ...

    def listar(self) -> list[Inscripcion]:
        ...

    def buscar_por_aprendiz(
        self, documento: int
    ) -> list[Inscripcion]:
        ...

    def buscar_por_curso(
        self, codigo_curso: str
    ) -> list[Inscripcion]:
        ...


class GestionInscripciones:

    def __init__(
        self,
        almacenamiento: Optional[MutableSequence[Inscripcion]] = None
    ):
        self.__inscripciones: MutableSequence[Inscripcion] = (
        almacenamiento if almacenamiento is not None else []
    )

    def registrar(self, inscripcion: Inscripcion) -> bool:

        if not isinstance(inscripcion, Inscripcion):
            raise ValueError(
                "Debe ingresar una inscripción válida"
            )

        if self.buscar_por_codigo(
            inscripcion.codigo
        ) is not None:
            raise ValueError("La inscripción ya existe")

        if self.buscar_por_aprendiz_y_curso(
            inscripcion.aprendiz.documento,
            inscripcion.curso.codigo
        ) is not None:
            raise ValueError(
                "El aprendiz ya está inscrito en este curso"
            )

        self.__inscripciones.append(inscripcion)
        return True

    def buscar_por_codigo(
        self, codigo: str
    ) -> Optional[Inscripcion]:

        for inscripcion in self.__inscripciones:
            if inscripcion.codigo == codigo:
                return inscripcion

        return None

    def listar(self) -> list[Inscripcion]:
        return list(self.__inscripciones)

    def buscar_por_aprendiz(
        self, documento: int
    ) -> list[Inscripcion]:

        resultado = []

        for inscripcion in self.__inscripciones:
            if inscripcion.aprendiz.documento == documento:
                resultado.append(inscripcion)

        return resultado

    def buscar_por_curso(
        self, codigo_curso: str
    ) -> list[Inscripcion]:

        resultado = []

        for inscripcion in self.__inscripciones:
            if inscripcion.curso.codigo == codigo_curso:
                resultado.append(inscripcion)

        return resultado

    def buscar_por_aprendiz_y_curso(
        self, documento: int, codigo_curso: str
    ) -> Optional[Inscripcion]:

        for inscripcion in self.__inscripciones:
            if (
                inscripcion.aprendiz.documento == documento
                and inscripcion.curso.codigo == codigo_curso
            ):
                return inscripcion

        return None

    def mostrar(self) -> str:

        if not self.__inscripciones:
            return "No hay inscripciones registradas"

        informacion = []

        for inscripcion in self.__inscripciones:
            informacion.append(
                inscripcion.mostrar_informacion()
            )

        return "\n\n".join(informacion)
