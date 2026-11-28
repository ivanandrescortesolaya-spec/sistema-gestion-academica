from personas.profesores import Profesor
from persistencia.conexion import (
    ConexionMySQL,
    reintentar_interbloqueo
)
from persistencia.excepciones import ErrorIntegridad


class RepositorioProfesores:

    CONSULTA = """
        SELECT p.nombre, p.documento, p.edad,
               pr.profesion, pr.codigo, pr.especialidad
        FROM profesor pr
        INNER JOIN persona p
            ON p.id_persona = pr.id_persona
    """

    def __init__(self, conexion: ConexionMySQL):
        self.__conexion = conexion

    @staticmethod
    def reconstruir(fila):
        return Profesor(
            nombre=fila["nombre"],
            documento=int(fila["documento"]),
            edad=fila["edad"],
            profesion=fila["profesion"],
            codigo=fila["codigo"],
            especialidad=fila["especialidad"]
        )

    @reintentar_interbloqueo
    def registrar(self, profesor: Profesor) -> bool:

        if not isinstance(profesor, Profesor):
            raise ValueError("Debe ingresar un profesor válido")

        try:
            with self.__conexion.transaccion() as conexion:
                cursor = conexion.cursor(dictionary=True)

                try:
                    cursor.execute("""
                        SELECT id_persona, nombre, edad
                        FROM persona
                        WHERE documento = %s
                        FOR UPDATE
                    """, (str(profesor.documento),))

                    persona = cursor.fetchone()

                    if persona is None:
                        cursor.execute("""
                            INSERT INTO persona
                                (documento, nombre, edad)
                            VALUES (%s, %s, %s)
                        """, (
                            str(profesor.documento),
                            profesor.nombre,
                            profesor.edad
                        ))

                        id_persona = cursor.lastrowid

                    else:
                        if (
                            persona["nombre"] != profesor.nombre
                            or persona["edad"] != profesor.edad
                        ):
                            raise ValueError(
                                "Los datos de la persona no coinciden"
                            )

                        id_persona = persona["id_persona"]

                    cursor.execute("""
                        INSERT INTO profesor
                            (id_persona, codigo,
                             profesion, especialidad)
                        VALUES (%s, %s, %s, %s)
                    """, (
                        id_persona,
                        profesor.codigo,
                        profesor.profesion,
                        profesor.especialidad
                    ))

                finally:
                    cursor.close()

        except ErrorIntegridad as error:
            raise ValueError(
                "Profesor duplicado o restricción incumplida"
            ) from error

        return True

    def buscar_por_documento(self, documento: int):

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

    def listar(self) -> list[Profesor]:

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
