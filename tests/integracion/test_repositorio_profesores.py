from tests.integracion import BaseIntegracion


class TestRepositorioProfesores(BaseIntegracion):

    def test_registrar_profesor(self):
        self.preparar_profesor()

        profesor = self.sistema.buscar_profesor(
            self.doc_profesor
        )

        self.assertIsNotNone(profesor)

    def test_recuperar_datos_profesor(self):
        self.preparar_profesor()

        profesor = self.sistema.buscar_profesor(
            self.doc_profesor
        )

        assert profesor is not None, "Profesor no encontrado"

        self.assertEqual(profesor.nombre, self.profesor.nombre)
        self.assertEqual(profesor.documento, self.doc_profesor)
        self.assertEqual(profesor.codigo, self.codigo_profesor)
        self.assertEqual(profesor.especialidad, "Python")

    def test_listar_profesores(self):
        self.preparar_profesor()

        documentos = [
            p.documento
            for p in self.sistema.listar_profesores()
        ]

        self.assertIn(self.doc_profesor, documentos)

    def test_profesor_duplicado(self):
        self.preparar_profesor()

        with self.assertRaises(ValueError):
            self.sistema.registrar_profesor(self.profesor)

    def test_profesor_inexistente(self):
        self.assertIsNone(
            self.sistema.buscar_profesor(self.doc_profesor)
        )
