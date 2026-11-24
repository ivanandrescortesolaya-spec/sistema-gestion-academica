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
        if not isinstance(profesor, Profesor):
            raise ValueError("Debes registrar un profesor válido")

        if self.buscar_por_documento(profesor.documento) is not None:
            raise ValueError("Ya existe un profesor con ese documento")

        self.__profesores.append(profesor)
        return True

    def mostrar(self, profesor: Profesor):
        print("Información del profesor:")
        print(profesor.mostrar_informacion())

    def listar(self):
        return self.__profesores.copy()

