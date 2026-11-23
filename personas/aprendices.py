
from .personas import Persona


class Aprendiz(Persona):

    def __init__(
        self,
        nombre: str,
        documento: int,
        edad: int,
        telefono: str,
        correo: str,
        direccion: str
    ):
        super().__init__(nombre, documento, edad)

        self.telefono = telefono
        self.correo = correo
        self.direccion = direccion

    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, telefono):
        if not isinstance(telefono, str) or not telefono.strip():
            raise ValueError("El teléfono no puede estar vacío")

        telefono = telefono.strip()

        if not telefono.lstrip("+").isdigit():
            raise ValueError("El teléfono debe contener números")

        self.__telefono = telefono

    @property
    def correo(self):
        return self.__correo

    @correo.setter
    def correo(self, correo):
        if not isinstance(correo, str) or not correo.strip():
            raise ValueError("El correo no puede estar vacío")

        correo = correo.strip()

        if correo.count("@") != 1 or "." not in correo.split("@")[-1]:
         raise ValueError("El correo no tiene un formato válido")

        self.__correo = correo
    @property
    def direccion(self):
        return self.__direccion

    @direccion.setter
    def direccion(self, direccion):
        if not isinstance(direccion, str) or not direccion.strip():
            raise ValueError("La dirección no puede estar vacía")

        self.__direccion = direccion.strip()

    def mostrar_informacion(self) -> str:
        return (
            f"Nombre: {self.nombre}\n"
            f"Documento: {self.documento}\n"
            f"Edad: {self.edad}\n"
            f"Teléfono: {self.telefono}\n"
            f"Correo: {self.correo}\n"
            f"Dirección: {self.direccion}"
        )

    def obtener_rol(self) -> str:
        return "Aprendiz"