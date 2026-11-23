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

        self.profesion = profesion
        self.codigo = codigo
        self.especialidad = especialidad

    @property
    def profesion(self):
        return self.__profesion

    @profesion.setter
    def profesion(self, profesion):
        if not isinstance(profesion, str) or not profesion.strip():
            raise ValueError("La profesión no puede estar vacía")

        self.__profesion = profesion.strip()

    @property
    def codigo(self):
        return self.__codigo

    @codigo.setter
    def codigo(self, codigo):
        if type(codigo) is not int or codigo <= 0:
            raise ValueError("El código debe ser un número positivo")

        self.__codigo = codigo

    @property
    def especialidad(self):
        return self.__especialidad

    @especialidad.setter
    def especialidad(self, especialidad):
        if not isinstance(especialidad, str) or not especialidad.strip():
            raise ValueError("La especialidad no puede estar vacía")

        self.__especialidad = especialidad.strip()

    def mostrar_informacion(self)-> str:
        return (
            f"Nombre: {self.nombre}\n"
            f"Documento: {self.documento}\n"
            f"Edad: {self.edad}\n"
            f"Profesión: {self.profesion}\n"
            f"Código: {self.codigo}\n"
            f"Especialidad: {self.especialidad}"
        )

    def obtener_rol(self)-> str:
        return "Profesor"

    