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
        if self.buscar_documento(aprendiz.documento):
            print("Ya existe un aprendiz con ese documento")
            return

        self.__aprendices.append(aprendiz)
        print("Aprendiz registrado correctamente")

    def mostrar(self, aprendiz: Aprendiz):
        print("Información del aprendiz:")
        print(aprendiz.mostrar_informacion())

    def listar(self):
        if not self.__aprendices:
            print("No hay aprendices registrados")
            return

        for aprendiz in self.__aprendices:
            self.mostrar(aprendiz)
