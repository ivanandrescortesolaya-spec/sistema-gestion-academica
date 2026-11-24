
from personas.aprendices import Aprendiz


class Gestion_aprendices:

    def __init__(self):
        self.__aprendices = []

    def buscar_documento(self, documento: int):
        for aprendiz in self.__aprendices:
            if aprendiz.documento == documento:
                return aprendiz

        return None

    def registrar(self, aprendiz: Aprendiz):
        if not isinstance(aprendiz, Aprendiz):
            raise ValueError("Debes registrar un aprendiz válido")

        if self.buscar_documento(aprendiz.documento) is not None:
            raise ValueError("Ya existe un aprendiz con ese documento")

        self.__aprendices.append(aprendiz)
        return True

    def mostrar(self, aprendiz: Aprendiz):
        print("Información del aprendiz:")
        print(aprendiz.mostrar_informacion())

    def listar(self):
        return self.__aprendices.copy()
