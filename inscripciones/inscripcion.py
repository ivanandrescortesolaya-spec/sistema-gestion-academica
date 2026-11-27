from personas.aprendices import Aprendiz
from cursos.curso import Curso
from datetime import date


class Inscripcion:

    def __init__(self, codigo, aprendiz, curso):
        self.codigo = codigo
        self.aprendiz = aprendiz
        self.curso = curso
        self.fecha_inscripcion = date.today()
        self.estado = "Activa"

    @property
    def codigo(self):
        return self.__codigo

    @codigo.setter
    def codigo(self, codigo):
        if not codigo:
            raise ValueError("El código es obligatorio")
        self.__codigo = codigo

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

    def cancelar(self):
        self.estado = "Cancelada"

    def finalizar(self):
        self.estado = "Finalizada"

    def mostrar_informacion(self):
        return (
            f"Inscripción: {self.codigo}\n"
            f"Aprendiz: {self.aprendiz.nombre}\n"
            f"Curso: {self.curso.nombre}\n"
            f"Fecha: {self.fecha_inscripcion}\n"
            f"Estado: {self.estado}"
        )
