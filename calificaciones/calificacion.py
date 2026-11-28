
from datetime import date
from inscripciones.inscripcion import Inscripcion


class Calificacion:

    def __init__(
        self,
        codigo: str,
        inscripcion: Inscripcion,
        nota: float,
        *,
        fecha: date | None = None
    ):
        self.codigo = codigo
        self.inscripcion = inscripcion
        self.nota = nota
        if fecha is not None and type(fecha) is not date:
            raise ValueError("Fecha de calificación inválida")

        self.__fecha = fecha or date.today()

    @property
    def codigo(self):
        return self.__codigo

    @codigo.setter
    def codigo(self, codigo):
        if not isinstance(codigo, str) or not codigo.strip():
            raise ValueError("El código es obligatorio")

        self.__codigo = codigo.strip()

    @property
    def inscripcion(self):
        return self.__inscripcion

    @inscripcion.setter
    def inscripcion(self, inscripcion):
        if not isinstance(inscripcion, Inscripcion):
            raise ValueError("Debe ingresar una inscripción válida")

        self.__inscripcion = inscripcion

    @property
    def nota(self):
        return self.__nota

    @nota.setter
    def nota(self, nota):
        if type(nota) not in (int, float) or not 0.0 <= nota <= 5.0:
            raise ValueError("La nota debe estar entre 0.0 y 5.0")

        self.__nota = float(nota)

    @property
    def fecha(self):
        return self.__fecha

    def mostrar_informacion(self) -> str:
        return (
            f"Código: {self.codigo}\n"
            f"Aprendiz: {self.inscripcion.aprendiz.nombre}\n"
            f"Curso: {self.inscripcion.curso.nombre}\n"
            f"Nota: {self.nota:.2f}\n"
            f"Fecha: {self.fecha}"
        )
