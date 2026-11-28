
from personas.profesores import Profesor


class Curso:

    MODALIDADES_VALIDAS = frozenset({
        "titulada",
        "complementaria"
    })

    def __init__(
        self,
        codigo: str,
        nombre: str,
        descripcion: str,
        duracion_horas: int,
        modalidad: str
    ):
        self.codigo = codigo
        self.nombre = nombre
        self.descripcion = descripcion
        self.duracion_horas = duracion_horas
        self.modalidad = modalidad
        self.__profesor = None

    @property
    def codigo(self):
        return self.__codigo

    @property
    def nombre(self):
        return self.__nombre

    @property
    def descripcion(self):
        return self.__descripcion

    @property
    def duracion_horas(self):
        return self.__duracion_horas

    @property
    def modalidad(self):
        return self.__modalidad

    @property
    def profesor(self):
        return self.__profesor

    @codigo.setter
    def codigo(self, codigo):
        if not isinstance(codigo, str) or not codigo.strip():
            raise ValueError("El codigo no puede estar vacio")

        self.__codigo = codigo.strip()

    @nombre.setter
    def nombre(self, nombre):
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("El nombre no puede estar vacio")

        self.__nombre = nombre.strip()

    @descripcion.setter
    def descripcion(self, descripcion):
        if not isinstance(descripcion, str) or not descripcion.strip():
            raise ValueError("La descripcion no puede estar vacio")

        self.__descripcion = descripcion.strip()

    @duracion_horas.setter
    def duracion_horas(self, horas):
        if type(horas) is not int or horas <= 0:
            raise ValueError("La duracion debe ser entero positivo")

        self.__duracion_horas = horas

    @modalidad.setter
    def modalidad(self, modalidad):
        if not isinstance(modalidad, str) or not modalidad.strip():
            raise ValueError("La modalidad no puede estar vacia")

        modalidad = modalidad.strip().lower()

        if modalidad not in self.MODALIDADES_VALIDAS:
            modalidades = " o ".join(
                sorted(self.MODALIDADES_VALIDAS, reverse=True)
            )

            raise ValueError(
                f"La modalidad debe ser {modalidades}"
            )

        self.__modalidad = modalidad

    def asignar_profesor(self, profesor: Profesor):
        if not isinstance(profesor, Profesor):
            raise ValueError("Debes asignar un profesor valido")

        self.__profesor = profesor

    def mostrar_informacion(self) -> str:
        profesor_nombre = (
            self.__profesor.nombre
            if self.__profesor is not None
            else "sin asignar"
        )

        return (
            f"Código: {self.codigo}\n"
            f"Nombre: {self.nombre}\n"
            f"Descripción: {self.descripcion}\n"
            f"Duración: {self.duracion_horas} horas\n"
            f"Modalidad: {self.modalidad}\n"
            f"Profesor: {profesor_nombre}"
        )
