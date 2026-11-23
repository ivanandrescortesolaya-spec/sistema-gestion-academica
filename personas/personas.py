class Persona:
    def __init__(
        self,
        nombre: str,
        documento: int,
        edad: int ,
    ):
        self.__id = id
        self.__nombre = nombre
        self.__documento = documento
        self.__edad = edad
    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, nuevo_nombre):
        self.__nombre = nuevo_nombre

    @property
    def documento(self):
        return self.__documento
    
    @documento.setter
    def documento(self, documento):
        self.__documento = documento

    @property
    def edad(self):
        return self.__edad

    @edad.setter
    def edad(self, edad):
        self.__edad = edad

