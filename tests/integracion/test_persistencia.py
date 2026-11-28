from integracion import BaseIntegracion
from persistencia.fabrica import crear_sistema_mysql


class TestPersistencia(BaseIntegracion):

    def test_persistencia_profesor(self):
        self.preparar_profesor()

        nuevo = crear_sistema_mysql(pruebas=True)

        self.assertIsNotNone(
            nuevo.buscar_profesor(self.doc_profesor)
        )

    def test_persistencia_aprendiz(self):
        self.preparar_aprendiz()

        nuevo = crear_sistema_mysql(pruebas=True)

        self.assertIsNotNone(
            nuevo.buscar_aprendiz(self.doc_aprendiz)
        )

    def test_persistencia_curso(self):
        self.preparar_curso()

        nuevo = crear_sistema_mysql(pruebas=True)

        self.assertIsNotNone(
            nuevo.buscar_curso(self.codigo_curso)
        )

    def test_persistencia_asignacion_profesor(self):
        self.preparar_profesor()
        self.preparar_curso()

        self.sistema.asignar_profesor(
            self.codigo_curso,
            self.doc_profesor
        )

        nuevo = crear_sistema_mysql(pruebas=True)

        curso = nuevo.buscar_curso(self.codigo_curso)

        assert curso is not None, "Curso no encontrado"

        profesor = curso.profesor
        assert profesor is not None, "Profesor no asignado"

        self.assertEqual(
            profesor.documento,
            self.doc_profesor
        )

    def test_persistencia_inscripcion(self):
        self.preparar_inscripcion()

        nuevo = crear_sistema_mysql(pruebas=True)

        inscripcion = nuevo.buscar_inscripcion(
            self.codigo_inscripcion
        )

        assert inscripcion is not None, (
            "Inscripción no encontrada"
        )
        self.assertEqual(inscripcion.fecha_inscripcion, self.fecha)

    def test_persistencia_estado(self):
        self.preparar_inscripcion()

        self.sistema.finalizar_inscripcion(
            self.codigo_inscripcion
        )

        nuevo = crear_sistema_mysql(pruebas=True)

        inscripcion = nuevo.buscar_inscripcion(
            self.codigo_inscripcion
        )

        assert inscripcion is not None, (
            "Inscripción no encontrada"
        )

        self.assertEqual(inscripcion.estado, "Finalizada")

    def test_persistencia_calificaciones(self):
        self.preparar_calificaciones()

        nuevo = crear_sistema_mysql(pruebas=True)

        notas = nuevo.consultar_calificaciones_inscripcion(
            self.codigo_inscripcion
        )

        self.assertEqual(len(notas), 3)
        self.assertTrue(
            all(n.fecha == self.fecha for n in notas)
        )

    def test_persistencia_rendimiento(self):
        self.preparar_calificaciones()

        nuevo = crear_sistema_mysql(pruebas=True)

        self.assertEqual(
            nuevo.calcular_promedio(self.codigo_inscripcion),
            4.0
        )

    def test_reporte_persistente(self):
        self.preparar_calificaciones()

        nuevo = crear_sistema_mysql(pruebas=True)

        reporte = nuevo.generar_reporte_calificaciones()

        self.assertIn(self.notas_creadas[0], reporte)
