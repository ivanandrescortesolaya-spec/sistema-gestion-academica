from personas.profesores import Profesor

class Gestion_profesores:

    def __init__(self):
        self.__profesores = []

    def buscar_por_documento(self, documento: int):
        for profesor in self.__profesores:
            if profesor.documento == documento:
                return profesor

        return None

    def registrar(self, profesor: Profesor):
        if self.buscar_por_documento(profesor.documento):
            print("Ya existe un profesor con ese documento")
            return

        self.__profesores.append(profesor)
        print("Profesor registrado correctamente")

    def mostrar(self, profesor: Profesor):
        print("Información del profesor:")
        print(profesor.mostrar_informacion())

    def listar(self):
        if not self.__profesores:
            print("No hay profesores registrados")
            return

        for profesor in self.__profesores:
            self.mostrar(profesor)
