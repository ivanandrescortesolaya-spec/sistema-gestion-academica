from decimal import Decimal, ROUND_HALF_UP

from calificaciones.calificacion import Calificacion
from persistencia.conexion import ConexionMySQL
from persistencia.excepciones import ErrorIntegridad
from .repositorio_inscripciones import RepositorioInscripciones


class RepositorioCalificaciones:

    CONSULTA = RepositorioInscripciones.CONSULTA.replace(
        "SELECT",
        """SELECT
            ca.codigo AS calificacion_codigo,
            ca.nota,
            ca.fecha AS calificacion_fecha,""",
        1
    ) + """
        INNER JOIN calificacion ca
            ON ca.id_inscripcion = i.id_inscripcion
    """

    def __init__(self, conexion: ConexionMySQL):
        self.__conexion = conexion

    @staticmethod
    def validar_nota(nota):

        if type(nota) not in (int, float):
            raise ValueError("La nota debe ser numérica")

        valor = Decimal(str(nota))

        if not valor.is_finite() or not 0 <= valor <= 5:
            raise ValueError("La nota debe estar entre 0.0 y 5.0")

        redondeada = valor.quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP
        )

        if valor != redondeada:
            raise ValueError(
                "La nota admite máximo dos decimales"
            )

        return redondeada

    @staticmethod
    def reconstruir(fila):

        inscripcion = RepositorioInscripciones.reconstruir(fila)

        return Calificacion(
            codigo=fila["calificacion_codigo"],
            inscripcion=inscripcion,
            nota=float(fila["nota"]),
            fecha=fila["calificacion_fecha"]
        )

    def registrar(self, calificacion: Calificacion) -> bool:

        if not isinstance(calificacion, Calificacion):
            raise ValueError("Debe ingresar una calificación válida")

        nota = self.validar_nota(calificacion.nota)

        try:
            with self.__conexion.transaccion() as conexion:
                cursor = conexion.cursor(dictionary=True)

                try:
                    cursor.execute("""
                        SELECT id_inscripcion, estado
                        FROM inscripcion
                        WHERE codigo = %s
                        FOR UPDATE
                    """, (calificacion.inscripcion.codigo,))

                    inscripcion = cursor.fetchone()

                    if inscripcion is None:
                        raise ValueError(
                            "La inscripción no está registrada"
                        )

                    if inscripcion["estado"] != "Activa":
                        raise ValueError(
                            "La inscripción no está activa"
                        )

                    cursor.execute("""
                        INSERT INTO calificacion (
                            codigo,
                            id_inscripcion,
                            nota,
                            fecha
                        )
                        VALUES (%s, %s, %s, %s)
                    """, (
                        calificacion.codigo,
                        inscripcion["id_inscripcion"],
                        nota,
                        calificacion.fecha
                    ))

                finally:
                    cursor.close()

        except ErrorIntegridad as error:
            raise ValueError(
                "Calificación duplicada o restricción incumplida"
            ) from error

        return True

    def __consultar(self, filtro="", parametros=()):

        with self.__conexion.transaccion() as conexion:
            cursor = conexion.cursor(dictionary=True)

            try:
                cursor.execute(
                    self.CONSULTA + filtro
                    + " ORDER BY ca.id_calificacion",
                    parametros
                )

                return [
                    self.reconstruir(fila)
                    for fila in cursor.fetchall()
                ]

            finally:
                cursor.close()

    def buscar_por_codigo(self, codigo: str):

        resultado = self.__consultar(
            " WHERE ca.codigo = %s", (codigo,)
        )

        return resultado[0] if resultado else None

    def listar(self) -> list[Calificacion]:
        return self.__consultar()

    def buscar_por_aprendiz(self, documento: int):
        return self.__consultar(
            " WHERE pa.documento = %s",
            (str(documento),)
        )

    def buscar_por_curso(self, codigo_curso: str):
        return self.__consultar(
            " WHERE c.codigo = %s",
            (codigo_curso,)
        )

    def buscar_por_inscripcion(self, codigo_inscripcion: str):
        return self.__consultar(
            " WHERE i.codigo = %s",
            (codigo_inscripcion,)
        )

    def modificar_calificacion(
        self, codigo: str, nueva_nota: float
    ) -> bool:

        nota = self.validar_nota(nueva_nota)

        with self.__conexion.transaccion() as conexion:
            cursor = conexion.cursor(dictionary=True)

            try:
                cursor.execute("""
                    SELECT id_inscripcion
                    FROM calificacion
                    WHERE codigo = %s
                """, (codigo,))

                calificacion = cursor.fetchone()

                if calificacion is None:
                    raise ValueError("La calificación no existe")

                cursor.execute("""
                    SELECT estado
                    FROM inscripcion
                    WHERE id_inscripcion = %s
                    FOR UPDATE
                """, (calificacion["id_inscripcion"],))

                inscripcion = cursor.fetchone()

                if inscripcion is None or inscripcion["estado"] != "Activa":
                    raise ValueError("La inscripción no está activa")

                cursor.execute("""
                    SELECT id_calificacion
                    FROM calificacion
                    WHERE codigo = %s
                    AND id_inscripcion = %s
                    FOR UPDATE
                """, (
                    codigo,
                    calificacion["id_inscripcion"]
                ))

                if cursor.fetchone() is None:
                    raise ValueError("La calificación no existe")

                cursor.execute("""
                    UPDATE calificacion
                    SET nota = %s
                    WHERE codigo = %s
                    AND id_inscripcion = %s
                """, (
                    nota,
                    codigo,
                    calificacion["id_inscripcion"]
                ))

            finally:
                cursor.close()

        return True

    @staticmethod
    def __promedio(notas):

        if len(notas) < 3:
            raise ValueError(
                "Se requieren mínimo tres calificaciones"
            )

        valores = [Decimal(str(nota)) for nota in notas]

        promedio = (
            sum(valores) / Decimal(len(valores))
        ).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP
        )

        return float(promedio)

    def calcular_promedio(self, codigo_inscripcion: str):

        calificaciones = self.buscar_por_inscripcion(
            codigo_inscripcion
        )

        return self.__promedio([
            calificacion.nota
            for calificacion in calificaciones
        ])

    def obtener_estado_academico(
        self, codigo_inscripcion: str
    ):

        promedio = self.calcular_promedio(
            codigo_inscripcion
        )

        return "Aprobado" if promedio >= 3.0 else "Reprobado"

    def consultar_rendimiento(
        self, codigo_inscripcion: str
    ) -> dict:

        calificaciones = self.buscar_por_inscripcion(
            codigo_inscripcion
        )

        if not calificaciones:
            raise ValueError(
                "No hay calificaciones registradas"
            )

        inscripcion = calificaciones[0].inscripcion

        notas = [
            calificacion.nota
            for calificacion in calificaciones
        ]

        promedio = None
        estado = "Pendiente"

        if len(notas) >= 3:
            promedio = self.__promedio(notas)

            estado = (
                "Aprobado"
                if promedio >= 3.0
                else "Reprobado"
            )

        return {
            "inscripcion": codigo_inscripcion,
            "aprendiz": inscripcion.aprendiz.nombre,
            "curso": inscripcion.curso.nombre,
            "notas": notas,
            "promedio": promedio,
            "estado": estado
        }
