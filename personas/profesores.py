from .personas import Persona

class Profesor(Persona):
    def __init__(
        self,
        nombre: str,
        documento: int,
        edad: int,
        profesion: str,
        codigo: int,
        especialidad: str
    ):
        super().__init__(nombre, documento, edad)

        self.__profesion = profesion
        self.__codigo = codigo
        self.__especialidad = especialidad

    @property
    def profesion(self):
        return self.__profesion

    @property
    def codigo(self):
        return self.__codigo

    @property
    def especialidad(self):
        return self.__especialidad

    @profesion.setter
    def profesion(self, profesion):
        self.__profesion = profesion

    @codigo.setter
    def codigo(self, codigo):
        self.__codigo = codigo

    @especialidad.setter
    def especialidad(self, especialidad):
        self.__especialidad = especialidad