from cursos.curso import Curso
from personas.profesores import Profesor
from persistencia.conexion import ConexionMySQL
from persistencia.excepciones import ErrorIntegridad


class RepositorioCursos:

    CONSULTA = """
        SELECT
            c.codigo,
            c.nombre,
            c.descripcion,
            c.duracion_horas,
            m.nombre AS modalidad,
            p.documento AS profesor_documento,
            p.nombre AS profesor_nombre,
            p.edad AS profesor_edad,
            pr.codigo AS profesor_codigo,
            pr.profesion AS profesor_profesion,
            pr.especialidad AS profesor_especialidad
        FROM curso c
        INNER JOIN modalidad m
            ON m.id_modalidad = c.id_modalidad
        LEFT JOIN profesor pr
            ON pr.id_persona = c.id_profesor
        LEFT JOIN persona p
            ON p.id_persona = pr.id_persona
    """

    def __init__(self, conexion: ConexionMySQL):
        self.__conexion = conexion

    @staticmethod
    def reconstruir(fila):

        curso = Curso(
            codigo=fila["codigo"],
            nombre=fila["nombre"],
            descripcion=fila["descripcion"],
            duracion_horas=fila["duracion_horas"],
            modalidad=fila["modalidad"]
        )

        if fila["profesor_documento"] is not None:

            profesor = Profesor(
                nombre=fila["profesor_nombre"],
                documento=int(fila["profesor_documento"]),
                edad=fila["profesor_edad"],
                profesion=fila["profesor_profesion"],
                codigo=fila["profesor_codigo"],
                especialidad=fila["profesor_especialidad"]
            )

            curso.asignar_profesor(profesor)

        return curso

    @staticmethod
    def obtener_id_profesor(cursor, documento):

        cursor.execute("""
            SELECT pr.id_persona
            FROM profesor pr
            INNER JOIN persona p
                ON p.id_persona = pr.id_persona
            WHERE p.documento = %s
        """, (str(documento),))

        fila = cursor.fetchone()

        if fila is None:
            raise ValueError("El profesor no está registrado")

        return fila["id_persona"]

    def registrar(self, curso: Curso) -> bool:

        if not isinstance(curso, Curso):
            raise ValueError("Debe ingresar un curso válido")

        try:
            with self.__conexion.transaccion() as conexion:
                cursor = conexion.cursor(dictionary=True)

                try:
                    cursor.execute("""
                        SELECT id_modalidad
                        FROM modalidad
                        WHERE nombre = %s
                    """, (curso.modalidad,))

                    modalidad = cursor.fetchone()

                    if modalidad is None:
                        raise ValueError("La modalidad no existe")

                    id_profesor = None

                    if curso.profesor is not None:
                        id_profesor = self.obtener_id_profesor(
                            cursor,
                            curso.profesor.documento
                        )

                    cursor.execute("""
                        INSERT INTO curso (
                            codigo, nombre, descripcion,
                            duracion_horas, id_modalidad,
                            id_profesor
                        )
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (
                        curso.codigo,
                        curso.nombre,
                        curso.descripcion,
                        curso.duracion_horas,
                        modalidad["id_modalidad"],
                        id_profesor
                    ))

                finally:
                    cursor.close()

        except ErrorIntegridad as error:
            raise ValueError(
                "Curso duplicado o restricción incumplida"
            ) from error

        return True

    def buscar_por_codigo(self, codigo: str):

        with self.__conexion.transaccion() as conexion:
            cursor = conexion.cursor(dictionary=True)

            try:
                cursor.execute(
                    self.CONSULTA + " WHERE c.codigo = %s",
                    (codigo,)
                )

                fila = cursor.fetchone()

                return self.reconstruir(fila) if fila else None

            finally:
                cursor.close()

    def listar(self) -> list[Curso]:

        with self.__conexion.transaccion() as conexion:
            cursor = conexion.cursor(dictionary=True)

            try:
                cursor.execute(
                    self.CONSULTA + " ORDER BY c.id_curso"
                )

                return [
                    self.reconstruir(fila)
                    for fila in cursor.fetchall()
                ]

            finally:
                cursor.close()

    def asignar_profesor(
        self, codigo: str, profesor: Profesor
    ) -> bool:

        if not isinstance(profesor, Profesor):
            raise ValueError("Debe asignar un profesor válido")

        with self.__conexion.transaccion() as conexion:
            cursor = conexion.cursor(dictionary=True)

            try:
                cursor.execute("""
                    SELECT id_curso
                    FROM curso
                    WHERE codigo = %s
                    FOR UPDATE
                """, (codigo,))

                curso = cursor.fetchone()

                if curso is None:
                    raise ValueError("El curso no existe")

                id_profesor = self.obtener_id_profesor(
                    cursor,
                    profesor.documento
                )

                cursor.execute("""
                    UPDATE curso
                    SET id_profesor = %s
                    WHERE id_curso = %s
                """, (
                    id_profesor,
                    curso["id_curso"]
                ))

            finally:
                cursor.close()

        return True

    def buscar_por_profesor(
        self, documento: int
    ) -> list[Curso]:

        with self.__conexion.transaccion() as conexion:
            cursor = conexion.cursor(dictionary=True)

            try:
                cursor.execute(
                    self.CONSULTA
                    + " WHERE p.documento = %s"
                    + " ORDER BY c.id_curso",
                    (str(documento),)
                )

                return [
                    self.reconstruir(fila)
                    for fila in cursor.fetchall()
                ]

            finally:
                cursor.close()
