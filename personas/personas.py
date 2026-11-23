
from abc import ABC, abstractmethod


class Persona(ABC):

    def __init__(self, nombre: str, documento: int, edad: int):
        self.nombre = nombre
        self.documento = documento
        self.edad = edad

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, nuevo_nombre):
        if not isinstance(nuevo_nombre, str) or not nuevo_nombre.strip():
            raise ValueError("El nombre no puede estar vacío")

        self.__nombre = nuevo_nombre.strip()

    @property
    def documento(self):
        return self.__documento

    @documento.setter
    def documento(self, documento):
        if type(documento) is not int or documento <= 0:
            raise ValueError("El documento debe ser un número positivo")

        self.__documento = documento

    @property
    def edad(self):
        return self.__edad

    @edad.setter
    def edad(self, edad):
        if type(edad) is not int or edad < 0:
            raise ValueError("La edad debe ser un número válido")

        self.__edad = edad

    @abstractmethod
    def mostrar_informacion(self)->str:
        pass

    @abstractmethod
    def obtener_rol(self)-> str:
        pass
