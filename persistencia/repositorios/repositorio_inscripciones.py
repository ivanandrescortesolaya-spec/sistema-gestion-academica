from inscripciones.inscripcion import Inscripcion
from persistencia.conexion import ConexionMySQL
from persistencia.excepciones import ErrorIntegridad
from .repositorio_aprendices import RepositorioAprendices
from .repositorio_cursos import RepositorioCursos


class RepositorioInscripciones:

    CONSULTA = """
        SELECT
            i.codigo AS inscripcion_codigo,
            i.fecha_inscripcion,
            i.estado,
            a.telefono,
            a.correo,
            a.direccion,
            pa.nombre AS aprendiz_nombre,
            pa.documento AS aprendiz_documento,
            pa.edad AS aprendiz_edad,
            c.codigo,
            c.nombre,
            c.descripcion,
            c.duracion_horas,
            m.nombre AS modalidad,
            pp.documento AS profesor_documento,
            pp.nombre AS profesor_nombre,
            pp.edad AS profesor_edad,
            pr.codigo AS profesor_codigo,
            pr.profesion AS profesor_profesion,
            pr.especialidad AS profesor_especialidad
        FROM inscripcion i
        INNER JOIN aprendiz a
            ON a.id_persona = i.id_aprendiz
        INNER JOIN persona pa
            ON pa.id_persona = a.id_persona
        INNER JOIN curso c
            ON c.id_curso = i.id_curso
        INNER JOIN modalidad m
            ON m.id_modalidad = c.id_modalidad
        LEFT JOIN profesor pr
            ON pr.id_persona = c.id_profesor
        LEFT JOIN persona pp
            ON pp.id_persona = pr.id_persona
    """

    def __init__(self, conexion: ConexionMySQL):
        self.__conexion = conexion

    @staticmethod
    def reconstruir(fila):
        aprendiz = RepositorioAprendices.reconstruir({
            "nombre": fila["aprendiz_nombre"],
            "documento": fila["aprendiz_documento"],
            "edad": fila["aprendiz_edad"],
            "telefono": fila["telefono"],
            "correo": fila["correo"],
            "direccion": fila["direccion"]
        })

        curso = RepositorioCursos.reconstruir(fila)

        return Inscripcion(
            codigo=fila["inscripcion_codigo"],
            aprendiz=aprendiz,
            curso=curso,
            fecha_inscripcion=fila["fecha_inscripcion"],
            estado=fila["estado"]
        )

    def registrar(self, inscripcion: Inscripcion) -> bool:

        if not isinstance(inscripcion, Inscripcion):
            raise ValueError("Debe ingresar una inscripción válida")

        if inscripcion.estado != "Activa":
            raise ValueError("La inscripción debe iniciar activa")

        try:
            with self.__conexion.transaccion() as conexion:
                cursor = conexion.cursor(dictionary=True)

                try:
                    cursor.execute("""
                        SELECT a.id_persona
                        FROM aprendiz a
                        INNER JOIN persona p
                            ON p.id_persona = a.id_persona
                        WHERE p.documento = %s
                    """, (str(inscripcion.aprendiz.documento),))

                    aprendiz = cursor.fetchone()

                    if aprendiz is None:
                        raise ValueError("El aprendiz no está registrado")

                    cursor.execute("""
                        SELECT id_curso
                        FROM curso
                        WHERE codigo = %s
                    """, (inscripcion.curso.codigo,))

                    curso = cursor.fetchone()

                    if curso is None:
                        raise ValueError("El curso no está registrado")

                    cursor.execute("""
                        INSERT INTO inscripcion (
                            codigo,
                            id_aprendiz,
                            id_curso,
                            fecha_inscripcion,
                            estado
                        )
                        VALUES (%s, %s, %s, %s, %s)
                    """, (
                        inscripcion.codigo,
                        aprendiz["id_persona"],
                        curso["id_curso"],
                        inscripcion.fecha_inscripcion,
                        inscripcion.estado
                    ))

                finally:
                    cursor.close()

        except ErrorIntegridad as error:
            raise ValueError(
                "Inscripción duplicada o restricción incumplida"
            ) from error

        return True

    def __consultar(self, filtro="", parametros=()):

        with self.__conexion.transaccion() as conexion:
            cursor = conexion.cursor(dictionary=True)

            try:
                cursor.execute(
                    self.CONSULTA + filtro
                    + " ORDER BY i.id_inscripcion",
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
            " WHERE i.codigo = %s", (codigo,)
        )

        return resultado[0] if resultado else None

    def listar(self) -> list[Inscripcion]:
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

    def buscar_por_aprendiz_y_curso(
        self, documento: int, codigo_curso: str
    ):
        resultado = self.__consultar(
            " WHERE pa.documento = %s AND c.codigo = %s",
            (str(documento), codigo_curso)
        )

        return resultado[0] if resultado else None

    def cambiar_estado(self, codigo: str, estado: str) -> bool:

        if estado not in ("Cancelada", "Finalizada"):
            raise ValueError("Estado de destino inválido")

        with self.__conexion.transaccion() as conexion:
            cursor = conexion.cursor()

            try:
                cursor.execute("""
                    UPDATE inscripcion
                    SET estado = %s
                    WHERE codigo = %s
                    AND estado = 'Activa'
                """, (estado, codigo))

                if cursor.rowcount != 1:
                    raise ValueError(
                        "La inscripción no existe o no está activa"
                    )

            finally:
                cursor.close()

        return True

    def cancelar(self, codigo: str) -> bool:
        return self.cambiar_estado(codigo, "Cancelada")

    def finalizar(self, codigo: str) -> bool:
        return self.cambiar_estado(codigo, "Finalizada")
