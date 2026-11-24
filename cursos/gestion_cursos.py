
from cursos.curso import Curso
from personas.profesores import Profesor


class GestionCursos:

    def __init__(self):
        self.__cursos = []

    def buscar_por_codigo(self, codigo: str):
        for curso in self.__cursos:
            if curso.codigo == codigo:
                return curso
        return None

    def registrar(self, curso: Curso):
        if not isinstance(curso, Curso):
            raise ValueError("Debes registrar un curso válido")

        if self.buscar_por_codigo(curso.codigo) is not None:
            raise ValueError("Ya existe un curso con ese código")

        self.__cursos.append(curso)
        return True

    def listar(self):
        return self.__cursos.copy()

    def mostrar(self):
        if not self.__cursos:
            return "No hay cursos registrados"

        return "\n\n".join(
            curso.mostrar_informacion()
            for curso in self.__cursos
        )

    def asignar_profesor(self, codigo: str, profesor: Profesor):
        curso = self.buscar_por_codigo(codigo)

        if curso is None:
            raise ValueError("El curso no existe")

        curso.asignar_profesor(profesor)
        return True

    def buscar_por_profesor(self, documento: int):
        return [
            curso for curso in self.__cursos
            if curso.profesor is not None
            and curso.profesor.documento == documento
        ]
