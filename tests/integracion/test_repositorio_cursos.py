from integracion import BaseIntegracion


class TestRepositorioCursos(BaseIntegracion):

    def test_registrar_curso(self):
        self.preparar_curso()

        curso = self.sistema.buscar_curso(self.codigo_curso)

        assert curso is not None, "Curso no encontrado"
        self.assertEqual(curso.nombre, "Python")
        self.assertEqual(curso.duracion_horas, 48)
        self.assertEqual(curso.modalidad, "complementaria")

    def test_curso_sin_profesor(self):
        self.preparar_curso()

        curso = self.sistema.buscar_curso(self.codigo_curso)

        assert curso is not None, "Curso no encontrado"

        self.assertIsNone(curso.profesor)

    def test_asignar_profesor(self):
        self.preparar_profesor()
        self.preparar_curso()

        self.assertTrue(
            self.sistema.asignar_profesor(
                self.codigo_curso,
                self.doc_profesor
            )
        )

        curso = self.sistema.buscar_curso(self.codigo_curso)

        assert curso is not None, "Curso no encontrado"

        profesor = curso.profesor
        assert profesor is not None, "Profesor no asignado"

        self.assertEqual(
            profesor.documento,
            self.doc_profesor
        )

    def test_buscar_cursos_por_profesor(self):
        self.preparar_profesor()
        self.preparar_curso()

        self.sistema.asignar_profesor(
            self.codigo_curso,
            self.doc_profesor
        )

        cursos = self.sistema.consultar_cursos_profesor(
            self.doc_profesor
        )

        self.assertIn(
            self.codigo_curso,
            [c.codigo for c in cursos]
        )

    def test_curso_duplicado(self):
        self.preparar_curso()

        with self.assertRaises(ValueError):
            self.sistema.registrar_curso(self.curso)

    def test_listar_cursos(self):
        self.preparar_curso()

        self.assertIn(
            self.codigo_curso,
            [c.codigo for c in self.sistema.listar_cursos()]
        )

    def test_curso_inexistente(self):
        self.assertIsNone(
            self.sistema.buscar_curso(self.codigo_curso)
        )
