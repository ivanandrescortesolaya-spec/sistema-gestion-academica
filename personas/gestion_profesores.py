from personas.profesores import Profesor

class Gestion_profesores(Profesor):
    def __init__(self):
        self.__profesores = []

    def buscar_por_documento(self,documento: int):
        for profesor in self.__profesores:
            if profesor.documento == documento:
                return profesor

        return None

    def registrar(self, profesor: Profesor):
        if self.buscar_por_documento(profesor.documento):
            print("ya existe un profesor con ese documento")
            return
        self.__profesores.append(profesor)
        print("profesor registrado.")

    def mostrar(self, profesor: Profesor):
        print("informacion del profesor:")
        print(f"Nombre{profesor.nombre}")
        print(f"Documento{profesor.documento}")
        print(f"Edad{profesor.edad}")
        print(f"Profesion{profesor.profesion}")
        print(f"Codigo{profesor.codigo}")
        print(f"Especialidad{profesor.especialidad}")

    def listar(self):
        if not self.__profesores:
            print("no hay profesores registrados.")
            return
        for profesor in self.__profesores:
            self.mostrar(profesor)
        