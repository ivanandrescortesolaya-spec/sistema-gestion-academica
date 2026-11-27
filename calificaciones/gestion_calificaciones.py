from calificaciones.calificacion import Calificacion


class GestionCalificaciones:

    def __init__(self):
        self.__calificaciones = []

    def registrar(self, calificacion):
        if not isinstance(calificacion, Calificacion):
            raise ValueError("Debe ingresar una calificacion valida")

        if self.buscar_por_codigo(calificacion.codigo):
            raise ValueError("La calificacion ya existe")

        self.__calificaciones.append(calificacion)
        return True

    def buscar_por_codigo(self, codigo):
        for calificacion in self.__calificaciones:
            if calificacion.codigo == codigo:
                return calificacion

        return None

    def listar(self):
        return self.__calificaciones.copy()

    def buscar_por_aprendiz(self, documento):
        resultado = []

        for calificacion in self.__calificaciones:
            if calificacion.inscripcion.aprendiz.documento == documento:
                resultado.append(calificacion)

        return resultado

    def buscar_por_curso(self, codigo_curso):
        resultado = []

        for calificacion in self.__calificaciones:
            if calificacion.inscripcion.curso.codigo == codigo_curso:
                resultado.append(calificacion)

        return resultado

    def mostrar(self):
        if not self.__calificaciones:
            return "No hay calificaciones registradas"

        informacion = []

        for calificacion in self.__calificaciones:
            informacion.append(calificacion.mostrar_informacion())

        return "\n\n".join(informacion)
