
from personas.aprendices import Aprendiz
from cursos.curso import Curso
from datetime import date


class Inscripcion:

    def __init__(self, codigo: str, aprendiz: Aprendiz, curso: Curso):
        self.codigo = codigo
        self.aprendiz = aprendiz
        self.curso = curso
        self.__fecha_inscripcion = date.today()
        self.__estado = "Activa"

    @property
    def codigo(self):
        return self.__codigo

    @codigo.setter
    def codigo(self, codigo):
        if not isinstance(codigo, str) or not codigo.strip():
            raise ValueError("El código debe ser un texto válido")

        self.__codigo = codigo.strip()

    @property
    def aprendiz(self):
        return self.__aprendiz

    @aprendiz.setter
    def aprendiz(self, aprendiz):
        if not isinstance(aprendiz, Aprendiz):
            raise ValueError("Debe ingresar un aprendiz válido")

        self.__aprendiz = aprendiz

    @property
    def curso(self):
        return self.__curso

    @curso.setter
    def curso(self, curso):
        if not isinstance(curso, Curso):
            raise ValueError("Debe ingresar un curso válido")

        self.__curso = curso

    @property
    def fecha_inscripcion(self):
        return self.__fecha_inscripcion

    @property
    def estado(self):
        return self.__estado

    def cancelar(self):
        self.__estado = "Cancelada"

    def finalizar(self):
        self.__estado = "Finalizada"

    def mostrar_informacion(self) -> str:
        return (
            f"Inscripción: {self.codigo}\n"
            f"Aprendiz: {self.aprendiz.nombre}\n"
            f"Curso: {self.curso.nombre}\n"
            f"Fecha: {self.fecha_inscripcion}\n"
            f"Estado: {self.estado}"
        )
