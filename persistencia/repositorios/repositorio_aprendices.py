from personas.aprendices import Aprendiz
from persistencia.conexion import (
    ConexionMySQL,
    reintentar_interbloqueo
)
from persistencia.excepciones import ErrorIntegridad


class RepositorioAprendices:

    CONSULTA = """
        SELECT p.nombre, p.documento, p.edad,
               a.telefono, a.correo, a.direccion
        FROM aprendiz a
        INNER JOIN persona p
            ON p.id_persona = a.id_persona
    """

    def __init__(self, conexion: ConexionMySQL):
        self.__conexion = conexion

    @staticmethod
    def reconstruir(fila):
        return Aprendiz(
            nombre=fila["nombre"],
            documento=int(fila["documento"]),
            edad=fila["edad"],
            telefono=fila["telefono"],
            correo=fila["correo"],
            direccion=fila["direccion"]
        )

    @reintentar_interbloqueo
    def registrar(self, aprendiz: Aprendiz) -> bool:

        if not isinstance(aprendiz, Aprendiz):
            raise ValueError("Debe ingresar un aprendiz válido")

        try:
            with self.__conexion.transaccion() as conexion:
                cursor = conexion.cursor(dictionary=True)

                try:
                    cursor.execute("""
                        SELECT id_persona, nombre, edad
                        FROM persona
                        WHERE documento = %s
                        FOR UPDATE
                    """, (str(aprendiz.documento),))

                    persona = cursor.fetchone()

                    if persona is None:
                        cursor.execute("""
                            INSERT INTO persona
                                (documento, nombre, edad)
                            VALUES (%s, %s, %s)
                        """, (
                            str(aprendiz.documento),
                            aprendiz.nombre,
                            aprendiz.edad
                        ))

                        id_persona = cursor.lastrowid

                    else:
                        if (
                            persona["nombre"] != aprendiz.nombre
                            or persona["edad"] != aprendiz.edad
                        ):
                            raise ValueError(
                                "Los datos de la persona no coinciden"
                            )

                        id_persona = persona["id_persona"]

                    cursor.execute("""
                        INSERT INTO aprendiz
                            (id_persona, telefono,
                             correo, direccion)
                        VALUES (%s, %s, %s, %s)
                    """, (
                        id_persona,
                        aprendiz.telefono,
                        aprendiz.correo,
                        aprendiz.direccion
                    ))

                finally:
                    cursor.close()

        except ErrorIntegridad as error:
            raise ValueError(
                "Aprendiz duplicado o restricción incumplida"
            ) from error

        return True

    def buscar_documento(self, documento: int):

        with self.__conexion.transaccion() as conexion:
            cursor = conexion.cursor(dictionary=True)

            try:
                cursor.execute(
                    self.CONSULTA + " WHERE p.documento = %s",
                    (str(documento),)
                )

                fila = cursor.fetchone()

                return self.reconstruir(fila) if fila else None

            finally:
                cursor.close()

    def listar(self) -> list[Aprendiz]:

        with self.__conexion.transaccion() as conexion:
            cursor = conexion.cursor(dictionary=True)

            try:
                cursor.execute(
                    self.CONSULTA + " ORDER BY p.id_persona"
                )

                return [
                    self.reconstruir(fila)
                    for fila in cursor.fetchall()
                ]

            finally:
                cursor.close()
