from inscripciones.inscripcion import Inscripcion


class GestionInscripciones:

    def __init__(self):
        self.__inscripciones = []

    def registrar(self, inscripcion):
        if not isinstance(inscripcion, Inscripcion):
            raise ValueError("Debe ingresar una inscripción válida")

        if self.buscar_por_codigo(inscripcion.codigo):
            raise ValueError("La inscripción ya existe")

        self.__inscripciones.append(inscripcion)
        return True

    def buscar_por_codigo(self, codigo):
        for inscripcion in self.__inscripciones:
            if inscripcion.codigo == codigo:
                return inscripcion

        return None

    def listar(self):
        return self.__inscripciones.copy()

    def buscar_por_aprendiz(self, documento):
        resultado = []

        for inscripcion in self.__inscripciones:
            if inscripcion.aprendiz.documento == documento:
                resultado.append(inscripcion)

        return resultado

    def buscar_por_curso(self, codigo_curso):
        resultado = []

        for inscripcion in self.__inscripciones:
            if inscripcion.curso.codigo == codigo_curso:
                resultado.append(inscripcion)

        return resultado

    def mostrar(self):
        if not self.__inscripciones:
            return "No hay inscripciones registradas"

        informacion = []

        for inscripcion in self.__inscripciones:
            informacion.append(inscripcion.mostrar_informacion())

        return "\n\n".join(informacion)
