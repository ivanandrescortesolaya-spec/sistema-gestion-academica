
from collections.abc import MutableSequence
from typing import Protocol, Optional

from calificaciones.calificacion import Calificacion


class IGestionCalificaciones(Protocol):

    def registrar(self, calificacion: Calificacion) -> bool:
        ...

    def buscar_por_codigo(
        self, codigo: str
    ) -> Optional[Calificacion]:
        ...

    def listar(self) -> list[Calificacion]:
        ...

    def buscar_por_aprendiz(
        self, documento: int
    ) -> list[Calificacion]:
        ...

    def buscar_por_curso(
        self, codigo_curso: str
    ) -> list[Calificacion]:
        ...

    def buscar_por_inscripcion(
        self, codigo_inscripcion: str
    ) -> list[Calificacion]:
        ...

    def modificar_calificacion(
        self, codigo: str, nueva_nota: float
    ) -> bool:
        ...

    def calcular_promedio(
        self, codigo_inscripcion: str
    ) -> float:
        ...

    def obtener_estado_academico(
        self, codigo_inscripcion: str
    ) -> str:
        ...

    def consultar_rendimiento(
        self, codigo_inscripcion: str
    ) -> dict:
        ...


class GestionCalificaciones:

    def __init__(
        self,
        almacenamiento: Optional[MutableSequence[Calificacion]] = None
    ):
        self.__calificaciones: MutableSequence[Calificacion] = (
            almacenamiento if almacenamiento is not None else []
        )

    def registrar(self, calificacion: Calificacion) -> bool:

        if not isinstance(calificacion, Calificacion):
            raise ValueError(
                "Debe ingresar una calificación válida"
            )

        if self.buscar_por_codigo(
            calificacion.codigo
        ) is not None:
            raise ValueError("La calificación ya existe")

        self.__calificaciones.append(calificacion)
        return True

    def buscar_por_codigo(
        self, codigo: str
    ) -> Optional[Calificacion]:

        for calificacion in self.__calificaciones:
            if calificacion.codigo == codigo:
                return calificacion

        return None

    def listar(self) -> list[Calificacion]:
        return list(self.__calificaciones)

    def buscar_por_aprendiz(
        self, documento: int
    ) -> list[Calificacion]:

        resultado = []

        for calificacion in self.__calificaciones:
            if calificacion.inscripcion.aprendiz.documento == documento:
                resultado.append(calificacion)

        return resultado

    def buscar_por_curso(
        self, codigo_curso: str
    ) -> list[Calificacion]:

        resultado = []

        for calificacion in self.__calificaciones:
            if calificacion.inscripcion.curso.codigo == codigo_curso:
                resultado.append(calificacion)

        return resultado

    def buscar_por_inscripcion(
        self, codigo_inscripcion: str
    ) -> list[Calificacion]:

        resultado = []

        for calificacion in self.__calificaciones:
            if calificacion.inscripcion.codigo == codigo_inscripcion:
                resultado.append(calificacion)

        return resultado

    def modificar_calificacion(
        self, codigo: str, nueva_nota: float
    ) -> bool:

        calificacion = self.buscar_por_codigo(codigo)

        if calificacion is None:
            raise ValueError("La calificación no existe")

        calificacion.nota = nueva_nota
        return True

    def calcular_promedio(
        self, codigo_inscripcion: str
    ) -> float:

        calificaciones = self.buscar_por_inscripcion(
            codigo_inscripcion
        )

        if len(calificaciones) < 3:
            raise ValueError(
                "Se requieren mínimo tres calificaciones"
            )

        notas = [
            calificacion.nota
            for calificacion in calificaciones
        ]

        return sum(notas) / len(notas)

    def obtener_estado_academico(
        self, codigo_inscripcion: str
    ) -> str:

        promedio = self.calcular_promedio(
            codigo_inscripcion
        )

        if promedio >= 3.0:
            return "Aprobado"

        return "Reprobado"

    def consultar_rendimiento(
        self, codigo_inscripcion: str
    ) -> dict:

        calificaciones = self.buscar_por_inscripcion(
            codigo_inscripcion
        )

        if not calificaciones:
            raise ValueError(
                "No hay calificaciones registradas"
            )

        inscripcion = calificaciones[0].inscripcion

        notas = [
            calificacion.nota
            for calificacion in calificaciones
        ]

        if len(notas) < 3:
            promedio = None
            estado = "Pendiente"

        else:
            promedio = round(
                self.calcular_promedio(
                    codigo_inscripcion
                ),
                2
            )

            estado = self.obtener_estado_academico(
                codigo_inscripcion
            )

        return {
            "inscripcion": codigo_inscripcion,
            "aprendiz": inscripcion.aprendiz.nombre,
            "curso": inscripcion.curso.nombre,
            "notas": notas,
            "promedio": promedio,
            "estado": estado
        }

    def mostrar(self) -> str:

        if not self.__calificaciones:
            return "No hay calificaciones registradas"

        informacion = []

        for calificacion in self.__calificaciones:
            informacion.append(
                calificacion.mostrar_informacion()
            )

        return "\n\n".join(informacion)
