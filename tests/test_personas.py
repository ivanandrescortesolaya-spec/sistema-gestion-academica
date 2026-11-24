
import inspect
import unittest

from personas.personas import Persona
from personas.profesores import Profesor
from personas.aprendices import Aprendiz


class TestPersonas(unittest.TestCase):

    def setUp(self):
        self.profesor = Profesor(
            "Carlos Pérez", 123456, 35,
            "Ingeniero", 101, "Programación"
        )

    def test_persona_abstracta(self):
        self.assertTrue(inspect.isabstract(Persona))

    def test_herencia_profesor(self):
        self.assertTrue(issubclass(Profesor, Persona))

    def test_herencia_aprendiz(self):
        self.assertTrue(issubclass(Aprendiz, Persona))

    def test_instancia_persona(self):
        self.assertIsInstance(self.profesor, Persona)

    def test_mostrar_informacion(self):
        informacion = self.profesor.mostrar_informacion()
        self.assertIn("Carlos Pérez", informacion)

    def test_obtener_rol(self):
        self.assertEqual(
            self.profesor.obtener_rol().lower(),
            "profesor"
        )


if __name__ == "__main__":
    unittest.main()
