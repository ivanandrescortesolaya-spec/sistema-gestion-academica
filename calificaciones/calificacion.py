from datetime import date
from inscripciones.inscripcion import Inscripcion


class Calificacion:

    def __init__(self, codigo, inscripcion, nota):
        self.codigo = codigo
        self.inscripcion = inscripcion
        self.nota = nota
        self.fecha = date.today()

    @property
    def codigo(self):
        return self.__codigo

    @codigo.setter
    def codigo(self, codigo):
        if not isinstance(codigo, str) or not codigo.strip():
            raise ValueError("El codigo es obligatorio")
        self.__codigo = codigo.strip()

    @property
    def inscripcion(self):
        return self.__inscripcion

    @inscripcion.setter
    def inscripcion(self, inscripcion):
        if not isinstance(inscripcion, Inscripcion):
            raise ValueError("Debe ingresar una inscripcion valida")
        self.__inscripcion = inscripcion

    @property
    def nota(self):
        return self.__nota

    @nota.setter
    def nota(self, nota):
        if type(nota) not in (int, float) or not 0 <= nota <= 100:
            raise ValueError("La nota debe estar entre 0 y 100")
        self.__nota = nota

    def mostrar_informacion(self):
        return (
            f"Codigo: {self.codigo}\n"
            f"Aprendiz: {self.inscripcion.aprendiz.nombre}\n"
            f"Curso: {self.inscripcion.curso.nombre}\n"
            f"Nota: {self.nota}\n"
            f"Fecha: {self.fecha}"
        )
