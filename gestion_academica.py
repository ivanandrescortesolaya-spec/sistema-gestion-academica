
from personas.profesores import Profesor
from personas.aprendices import Aprendiz
from personas.gestion_profesores import Gestion_profesores
from personas.gestion_aprendices import Gestion_aprendices

from cursos.curso import Curso
from cursos.gestion_cursos import GestionCursos

from inscripciones.inscripcion import Inscripcion
from inscripciones.gestion_inscripciones import GestionInscripciones

from calificaciones.calificacion import Calificacion
from calificaciones.gestion_calificaciones import GestionCalificaciones


class GestionAcademica:

    def __init__(self):
        self.__profesores = Gestion_profesores()
        self.__aprendices = Gestion_aprendices()
        self.__cursos = GestionCursos()
        self.__inscripciones = GestionInscripciones()
        self.__calificaciones = GestionCalificaciones()

    # Gestion de profesores
    def registrar_profesor(self, profesor: Profesor):
        return self.__profesores.registrar(profesor)

    def buscar_profesor(self, documento: int):
        return self.__profesores.buscar_por_documento(documento)

    def listar_profesores(self):
        return self.__profesores.listar()

    # Gestion de aprendices
    def registrar_aprendiz(self, aprendiz: Aprendiz):
        return self.__aprendices.registrar(aprendiz)

    def buscar_aprendiz(self, documento: int):
        return self.__aprendices.buscar_documento(documento)

    def listar_aprendices(self):
        return self.__aprendices.listar()

    # Gestion de cursos
    def registrar_curso(self, curso: Curso):
        return self.__cursos.registrar(curso)

    def buscar_curso(self, codigo: str):
        return self.__cursos.buscar_por_codigo(codigo)

    def listar_cursos(self):
        return self.__cursos.listar()

    def asignar_profesor(self, codigo: str, documento: int):
        profesor = self.buscar_profesor(documento)

        if profesor is None:
            raise ValueError("El profesor no esta registrado")

        return self.__cursos.asignar_profesor(codigo, profesor)

    def consultar_cursos_profesor(self, documento: int):
        return self.__cursos.buscar_por_profesor(documento)

    # Gestion de inscripciones
    def registrar_inscripcion(self, inscripcion: Inscripcion):
        return self.__inscripciones.registrar(inscripcion)

    def buscar_inscripcion(self, codigo: str):
        return self.__inscripciones.buscar_por_codigo(codigo)

    def listar_inscripciones(self):
        return self.__inscripciones.listar()

    def consultar_inscripciones_aprendiz(self, documento: int):
        return self.__inscripciones.buscar_por_aprendiz(documento)

    def consultar_inscripciones_curso(self, codigo_curso: str):
        return self.__inscripciones.buscar_por_curso(codigo_curso)

    # Gestion de calificaciones
    def registrar_calificacion(self, calificacion: Calificacion):
        return self.__calificaciones.registrar(calificacion)

    def buscar_calificacion(self, codigo: str):
        return self.__calificaciones.buscar_por_codigo(codigo)

    def listar_calificaciones(self):
        return self.__calificaciones.listar()

    # Consultas academicas
    def consultar_calificaciones_aprendiz(self, documento: int):
        return self.__calificaciones.buscar_por_aprendiz(documento)

    def consultar_calificaciones_curso(self, codigo_curso: str):
        return self.__calificaciones.buscar_por_curso(codigo_curso)

    # Reporte de calificaciones
    def generar_reporte_calificaciones(self):
        calificaciones = self.listar_calificaciones()

        if not calificaciones:
            return "No hay calificaciones registradas"

        notas = [calificacion.nota for calificacion in calificaciones]

        promedio = sum(notas) / len(notas)

        reporte = [
            "========== REPORTE DE CALIFICACIONES ==========",
            f"Total de calificaciones: {len(notas)}",
            f"Promedio general: {promedio:.2f}",
            f"Nota mas alta: {max(notas)}",
            f"Nota mas baja: {min(notas)}",
            "",
            "DETALLE DE CALIFICACIONES"
        ]

        for calificacion in calificaciones:
            reporte.append(calificacion.mostrar_informacion())
            reporte.append("----------------------------------------")

        return "\n".join(reporte)

    # Resumen academico
    def obtener_resumen(self):
        return {
            "profesores": len(self.listar_profesores()),
            "aprendices": len(self.listar_aprendices()),
            "cursos": len(self.listar_cursos()),
            "inscripciones": len(self.listar_inscripciones()),
            "calificaciones": len(self.listar_calificaciones())
        }
