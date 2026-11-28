import json
import unittest

from datetime import date

from personas.profesores import Profesor
from personas.aprendices import Aprendiz
from cursos.curso import Curso
from inscripciones.inscripcion import Inscripcion
from calificaciones.calificacion import Calificacion

from api.serializadores import (
    serializar_profesor,
    serializar_aprendiz,
    serializar_curso,
    serializar_inscripcion,
    serializar_calificacion
)


class TestSerializadoresAPI(unittest.TestCase):

    def setUp(self):

        self.profesor = Profesor(
            "Profesor Prueba",
            1000000001,
            35,
            "Ingeniero",
            1001,
            "Python"
        )

        self.aprendiz = Aprendiz(
            "Aprendiz Prueba",
            1000000002,
            22,
            "3001234567",
            "aprendiz@example.com",
            "Dirección de prueba"
        )

        self.curso = Curso(
            "CUR-001",
            "Python",
            "Curso de programación",
            48,
            "complementaria"
        )

        self.inscripcion = Inscripcion(
            "INS-001",
            self.aprendiz,
            self.curso,
            fecha_inscripcion=date(2026, 11, 28)
        )

        self.calificacion = Calificacion(
            "NOT-001",
            self.inscripcion,
            4.5,
            fecha=date(2026, 11, 28)
        )

    # Serialización de profesores

    def test_serializar_profesor(self):

        resultado = serializar_profesor(
            self.profesor
        )

        esperado = {
            "nombre": "Profesor Prueba",
            "documento": 1000000001,
            "edad": 35,
            "profesion": "Ingeniero",
            "codigo": 1001,
            "especialidad": "Python"
        }

        self.assertEqual(resultado, esperado)

    def test_profesor_tipo_diccionario(self):

        resultado = serializar_profesor(
            self.profesor
        )

        self.assertIsInstance(resultado, dict)

    def test_profesor_campos_exactos(self):

        resultado = serializar_profesor(
            self.profesor
        )

        self.assertEqual(
            set(resultado),
            {
                "nombre",
                "documento",
                "edad",
                "profesion",
                "codigo",
                "especialidad"
            }
        )

    # Serialización de aprendices

    def test_serializar_aprendiz(self):

        resultado = serializar_aprendiz(
            self.aprendiz
        )

        esperado = {
            "nombre": "Aprendiz Prueba",
            "documento": 1000000002,
            "edad": 22,
            "telefono": "3001234567",
            "correo": "aprendiz@example.com",
            "direccion": "Dirección de prueba"
        }

        self.assertEqual(resultado, esperado)

    def test_aprendiz_tipo_diccionario(self):

        resultado = serializar_aprendiz(
            self.aprendiz
        )

        self.assertIsInstance(resultado, dict)

    def test_aprendiz_telefono_texto(self):

        resultado = serializar_aprendiz(
            self.aprendiz
        )

        self.assertIsInstance(
            resultado["telefono"],
            str
        )

    # Serialización de cursos

    def test_serializar_curso_sin_profesor(self):

        resultado = serializar_curso(
            self.curso
        )

        esperado = {
            "codigo": "CUR-001",
            "nombre": "Python",
            "descripcion": "Curso de programación",
            "duracion_horas": 48,
            "modalidad": "complementaria",
            "profesor": None
        }

        self.assertEqual(resultado, esperado)

    def test_serializar_curso_con_profesor(self):

        self.curso.asignar_profesor(
            self.profesor
        )

        resultado = serializar_curso(
            self.curso
        )

        self.assertEqual(
            resultado["profesor"],
            serializar_profesor(self.profesor)
        )

    def test_curso_duracion_entera(self):

        resultado = serializar_curso(
            self.curso
        )

        self.assertIsInstance(
            resultado["duracion_horas"],
            int
        )

    def test_curso_campos_exactos(self):

        resultado = serializar_curso(
            self.curso
        )

        self.assertEqual(
            set(resultado),
            {
                "codigo",
                "nombre",
                "descripcion",
                "duracion_horas",
                "modalidad",
                "profesor"
            }
        )

    # Serialización de inscripciones

    def test_serializar_inscripcion(self):

        resultado = serializar_inscripcion(
            self.inscripcion
        )

        esperado = {
            "codigo": "INS-001",
            "aprendiz": serializar_aprendiz(
                self.aprendiz
            ),
            "curso": serializar_curso(
                self.curso
            ),
            "fecha_inscripcion": "2026-11-28",
            "estado": "Activa"
        }

        self.assertEqual(resultado, esperado)

    def test_inscripcion_aprendiz_anidado(self):

        resultado = serializar_inscripcion(
            self.inscripcion
        )

        self.assertEqual(
            resultado["aprendiz"],
            serializar_aprendiz(self.aprendiz)
        )

    def test_inscripcion_curso_anidado(self):

        resultado = serializar_inscripcion(
            self.inscripcion
        )

        self.assertEqual(
            resultado["curso"],
            serializar_curso(self.curso)
        )

    def test_inscripcion_fecha_iso(self):

        resultado = serializar_inscripcion(
            self.inscripcion
        )

        self.assertEqual(
            resultado["fecha_inscripcion"],
            "2026-11-28"
        )

    def test_inscripcion_estado_activa(self):

        resultado = serializar_inscripcion(
            self.inscripcion
        )

        self.assertEqual(
            resultado["estado"],
            "Activa"
        )

    def test_inscripcion_estado_cancelada(self):

        self.inscripcion.cancelar()

        resultado = serializar_inscripcion(
            self.inscripcion
        )

        self.assertEqual(
            resultado["estado"],
            "Cancelada"
        )

    def test_inscripcion_estado_finalizada(self):

        self.inscripcion.finalizar()

        resultado = serializar_inscripcion(
            self.inscripcion
        )

        self.assertEqual(
            resultado["estado"],
            "Finalizada"
        )

    # Serialización de calificaciones

    def test_serializar_calificacion(self):

        resultado = serializar_calificacion(
            self.calificacion
        )

        esperado = {
            "codigo": "NOT-001",
            "inscripcion": serializar_inscripcion(
                self.inscripcion
            ),
            "nota": 4.5,
            "fecha": "2026-11-28"
        }

        self.assertEqual(resultado, esperado)

    def test_calificacion_inscripcion_anidada(self):

        resultado = serializar_calificacion(
            self.calificacion
        )

        self.assertEqual(
            resultado["inscripcion"],
            serializar_inscripcion(self.inscripcion)
        )

    def test_calificacion_nota_numerica(self):

        resultado = serializar_calificacion(
            self.calificacion
        )

        self.assertIsInstance(
            resultado["nota"],
            float
        )

    def test_calificacion_fecha_iso(self):

        resultado = serializar_calificacion(
            self.calificacion
        )

        self.assertEqual(
            resultado["fecha"],
            "2026-11-28"
        )

    # Compatibilidad JSON

    def test_entidades_compatibles_json(self):

        entidades = (
            serializar_profesor(self.profesor),
            serializar_aprendiz(self.aprendiz),
            serializar_curso(self.curso),
            serializar_inscripcion(self.inscripcion),
            serializar_calificacion(self.calificacion)
        )

        for entidad in entidades:

            with self.subTest(entidad=entidad):

                contenido = json.dumps(
                    entidad,
                    ensure_ascii=False,
                    allow_nan=False
                )

                resultado = json.loads(contenido)

                self.assertEqual(
                    resultado,
                    entidad
                )

    def test_serializacion_anidada_completa(self):

        self.curso.asignar_profesor(
            self.profesor
        )

        resultado = serializar_calificacion(
            self.calificacion
        )

        profesor = resultado[
            "inscripcion"
        ][
            "curso"
        ][
            "profesor"
        ]

        self.assertEqual(
            profesor,
            serializar_profesor(self.profesor)
        )

    def test_serializaciones_independientes(self):

        primera = serializar_profesor(
            self.profesor
        )

        segunda = serializar_profesor(
            self.profesor
        )

        primera["nombre"] = "Nombre modificado"

        self.assertEqual(
            segunda["nombre"],
            "Profesor Prueba"
        )

        self.assertEqual(
            self.profesor.nombre,
            "Profesor Prueba"
        )

    def test_serializacion_refleja_cambios(self):

        primera = serializar_profesor(
            self.profesor
        )

        self.profesor.nombre = "Nuevo nombre"

        segunda = serializar_profesor(
            self.profesor
        )

        self.assertEqual(
            primera["nombre"],
            "Profesor Prueba"
        )

        self.assertEqual(
            segunda["nombre"],
            "Nuevo nombre"
        )


if __name__ == "__main__":

    unittest.main()