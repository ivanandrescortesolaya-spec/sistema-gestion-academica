
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
            raise ValueError("El profesor no está registrado")

        return self.__cursos.asignar_profesor(codigo, profesor)

    def consultar_cursos_profesor(self, documento: int):
        return self.__cursos.buscar_por_profesor(documento)

    def consultar_aprendices_profesor(self, documento: int):
        if self.buscar_profesor(documento) is None:
            raise ValueError("El profesor no está registrado")

        cursos = self.consultar_cursos_profesor(documento)

        resultado = []

        for curso in cursos:
            resultado.append({
                "curso": curso,
                "aprendices": self.consultar_aprendices_curso(
                    curso.codigo
                )
            })

        return resultado

    # Gestion de inscripciones

    def registrar_inscripcion(self, inscripcion: Inscripcion):
        if not isinstance(inscripcion, Inscripcion):
            raise ValueError("Debe ingresar una inscripción válida")

        aprendiz = self.buscar_aprendiz(
            inscripcion.aprendiz.documento
        )

        if aprendiz is None:
            raise ValueError("El aprendiz no está registrado")

        curso = self.buscar_curso(inscripcion.curso.codigo)

        if curso is None:
            raise ValueError("El curso no está registrado")

        if aprendiz is not inscripcion.aprendiz:
            raise ValueError(
                "Debe utilizar el aprendiz registrado"
            )

        if curso is not inscripcion.curso:
            raise ValueError(
                "Debe utilizar el curso registrado"
            )

        return self.__inscripciones.registrar(inscripcion)

    def buscar_inscripcion(self, codigo: str):
        return self.__inscripciones.buscar_por_codigo(codigo)

    def listar_inscripciones(self):
        return self.__inscripciones.listar()

    def consultar_inscripciones_aprendiz(self, documento: int):
        return self.__inscripciones.buscar_por_aprendiz(documento)

    def consultar_inscripciones_curso(self, codigo_curso: str):
        return self.__inscripciones.buscar_por_curso(codigo_curso)

    def consultar_cursos_aprendiz(self, documento: int):
        if self.buscar_aprendiz(documento) is None:
            raise ValueError("El aprendiz no está registrado")

        inscripciones = self.consultar_inscripciones_aprendiz(
            documento
        )

        return [
            inscripcion.curso
            for inscripcion in inscripciones
        ]

    def consultar_aprendices_curso(self, codigo_curso: str):
        if self.buscar_curso(codigo_curso) is None:
            raise ValueError("El curso no está registrado")

        inscripciones = self.consultar_inscripciones_curso(
            codigo_curso
        )

        return [
            inscripcion.aprendiz
            for inscripcion in inscripciones
        ]

    # Gestion de calificaciones

    def registrar_calificacion(self, calificacion: Calificacion):
        if not isinstance(calificacion, Calificacion):
            raise ValueError("Debe ingresar una calificación válida")

        inscripcion = self.buscar_inscripcion(
            calificacion.inscripcion.codigo
        )

        if inscripcion is None:
            raise ValueError("La inscripción no está registrada")

        if inscripcion is not calificacion.inscripcion:
            raise ValueError(
                "Debe utilizar la inscripción registrada"
            )

        return self.__calificaciones.registrar(calificacion)

    def buscar_calificacion(self, codigo: str):
        return self.__calificaciones.buscar_por_codigo(codigo)

    def listar_calificaciones(self):
        return self.__calificaciones.listar()

    def modificar_calificacion(self, codigo: str, nueva_nota: float):
        return self.__calificaciones.modificar_calificacion(
            codigo,
            nueva_nota
        )

    # Consultas academicas

    def consultar_calificaciones_aprendiz(self, documento: int):
        return self.__calificaciones.buscar_por_aprendiz(documento)

    def consultar_calificaciones_curso(self, codigo_curso: str):
        return self.__calificaciones.buscar_por_curso(codigo_curso)

    def consultar_calificaciones_inscripcion(
        self,
        codigo_inscripcion: str
    ):
        return self.__calificaciones.buscar_por_inscripcion(
            codigo_inscripcion
        )

    def calcular_promedio(self, codigo_inscripcion: str):
        if self.buscar_inscripcion(codigo_inscripcion) is None:
            raise ValueError("La inscripción no está registrada")

        return self.__calificaciones.calcular_promedio(
            codigo_inscripcion
        )

    def obtener_estado_academico(self, codigo_inscripcion: str):
        if self.buscar_inscripcion(codigo_inscripcion) is None:
            raise ValueError("La inscripción no está registrada")

        return self.__calificaciones.obtener_estado_academico(
            codigo_inscripcion
        )

    def consultar_rendimiento_inscripcion(
        self,
        codigo_inscripcion: str
    ):
        inscripcion = self.buscar_inscripcion(
            codigo_inscripcion
        )

        if inscripcion is None:
            raise ValueError("La inscripción no está registrada")

        calificaciones = self.consultar_calificaciones_inscripcion(
            codigo_inscripcion
        )

        if not calificaciones:
            return {
                "inscripcion": codigo_inscripcion,
                "aprendiz": inscripcion.aprendiz.nombre,
                "curso": inscripcion.curso.nombre,
                "notas": [],
                "promedio": None,
                "estado": "Pendiente"
            }

        return self.__calificaciones.consultar_rendimiento(
            codigo_inscripcion
        )

    def consultar_rendimiento_aprendiz(self, documento: int):
        if self.buscar_aprendiz(documento) is None:
            raise ValueError("El aprendiz no está registrado")

        inscripciones = self.consultar_inscripciones_aprendiz(
            documento
        )

        return [
            self.consultar_rendimiento_inscripcion(
                inscripcion.codigo
            )
            for inscripcion in inscripciones
        ]

    def consultar_rendimiento_curso(self, codigo_curso: str):
        if self.buscar_curso(codigo_curso) is None:
            raise ValueError("El curso no está registrado")

        inscripciones = self.consultar_inscripciones_curso(
            codigo_curso
        )

        return [
            self.consultar_rendimiento_inscripcion(
                inscripcion.codigo
            )
            for inscripcion in inscripciones
        ]

    # Reporte de calificaciones

    def generar_reporte_calificaciones(self):
        calificaciones = self.listar_calificaciones()

        if not calificaciones:
            return "No hay calificaciones registradas"

        notas = [
            calificacion.nota
            for calificacion in calificaciones
        ]

        promedio = sum(notas) / len(notas)

        reporte = [
            "========== REPORTE DE CALIFICACIONES ==========",
            f"Total de calificaciones: {len(notas)}",
            f"Promedio general: {promedio:.2f}",
            f"Nota más alta: {max(notas):.2f}",
            f"Nota más baja: {min(notas):.2f}",
            "",
            "DETALLE DE CALIFICACIONES"
        ]

        for calificacion in calificaciones:
            reporte.append(
                calificacion.mostrar_informacion()
            )

            reporte.append(
                "----------------------------------------"
            )

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
