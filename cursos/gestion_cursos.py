
from typing import Protocol, Optional

from cursos.curso import Curso
from personas.profesores import Profesor


class IGestionCursos(Protocol):

    def registrar(self, curso: Curso) -> bool:
        ...

    def buscar_por_codigo(
        self, codigo: str
    ) -> Optional[Curso]:
        ...

    def listar(self) -> list[Curso]:
        ...

    def asignar_profesor(
        self, codigo: str, profesor: Profesor
    ) -> bool:
        ...

    def buscar_por_profesor(
        self, documento: int
    ) -> list[Curso]:
        ...


class GestionCursos:

    def __init__(self):
        self.__cursos: list[Curso] = []

    def buscar_por_codigo(
        self, codigo: str
    ) -> Optional[Curso]:

        for curso in self.__cursos:
            if curso.codigo == codigo:
                return curso

        return None

    def registrar(self, curso: Curso) -> bool:

        if not isinstance(curso, Curso):
            raise ValueError(
                "Debes registrar un curso válido"
            )

        if self.buscar_por_codigo(curso.codigo) is not None:
            raise ValueError(
                "Ya existe un curso con ese código"
            )

        self.__cursos.append(curso)
        return True

    def listar(self) -> list[Curso]:
        return self.__cursos.copy()

    def mostrar(self) -> str:
        if not self.__cursos:
            return "No hay cursos registrados"

        return "\n\n".join(
            curso.mostrar_informacion()
            for curso in self.__cursos
        )

    def asignar_profesor(
        self, codigo: str, profesor: Profesor
    ) -> bool:

        curso = self.buscar_por_codigo(codigo)

        if curso is None:
            raise ValueError("El curso no existe")

        curso.asignar_profesor(profesor)
        return True

    def buscar_por_profesor(
        self, documento: int
    ) -> list[Curso]:

        return [
            curso for curso in self.__cursos
            if curso.profesor is not None
            and curso.profesor.documento == documento
        ]
