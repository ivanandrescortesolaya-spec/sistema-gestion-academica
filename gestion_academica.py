
from personas.profesores import Profesor
from personas.aprendices import Aprendiz
from personas.gestion_profesores import Gestion_profesores
from personas.gestion_aprendices import Gestion_aprendices
from cursos.curso import Curso
from cursos.gestion_cursos import GestionCursos


class GestionAcademica:

    def __init__(self):
        self.__profesores = Gestion_profesores()
        self.__aprendices = Gestion_aprendices()
        self.__cursos = GestionCursos()

    # Gestión de profesores

    def registrar_profesor(self, profesor: Profesor):
        return self.__profesores.registrar(profesor)

    def buscar_profesor(self, documento: int):
        return self.__profesores.buscar_por_documento(documento)

    def listar_profesores(self):
        return self.__profesores.listar()

    # Gestión de aprendices

    def registrar_aprendiz(self, aprendiz: Aprendiz):
        return self.__aprendices.registrar(aprendiz)

    def buscar_aprendiz(self, documento: int):
        return self.__aprendices.buscar_documento(documento)

    def listar_aprendices(self):
        return self.__aprendices.listar()

    # Gestión de cursos

    def registrar_curso(self, curso: Curso):
        return self.__cursos.registrar(curso)

    def buscar_curso(self, codigo: str):
        return self.__cursos.buscar_por_codigo(codigo)

    def listar_cursos(self):
        return self.__cursos.listar()

    def asignar_profesor(self, codigo: str, documento: int):
        profesor = self.buscar_profesor(documento)

        if profesor is None:
            raise ValueError("El profesor no está registrado")

        return self.__cursos.asignar_profesor(codigo, profesor)

    def consultar_cursos_profesor(self, documento: int):
        return self.__cursos.buscar_por_profesor(documento)

    # Resumen académico

    def obtener_resumen(self):
        return {
            "profesores": len(self.listar_profesores()),
            "aprendices": len(self.listar_aprendices()),
            "cursos": len(self.listar_cursos())
        }
