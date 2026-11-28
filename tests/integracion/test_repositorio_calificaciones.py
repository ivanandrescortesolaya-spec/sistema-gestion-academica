from tests.integracion import BaseIntegracion
from calificaciones.calificacion import Calificacion


class TestRepositorioCalificaciones(BaseIntegracion):

    def test_registrar_calificacion(self):
        self.preparar_inscripcion()

        codigo = self.registrar_nota(1, 4.5)

        nota = self.sistema.buscar_calificacion(codigo)

        assert nota is not None, "Calificación no encontrada"

        self.assertEqual(nota.nota, 4.5)
        self.assertEqual(nota.fecha, self.fecha)

    def test_calificacion_duplicada(self):
        self.preparar_inscripcion()

        codigo = self.registrar_nota(1, 4.0)

        calificacion = Calificacion(
            codigo,
            self.inscripcion,
            4.0
        )

        with self.assertRaises(ValueError):
            self.sistema.registrar_calificacion(calificacion)

    def test_modificar_calificacion(self):
        self.preparar_inscripcion()

        codigo = self.registrar_nota(1, 3.0)

        self.assertTrue(
            self.sistema.modificar_calificacion(codigo, 4.5)
        )

        nota = self.sistema.buscar_calificacion(codigo)

        assert nota is not None, "Calificación no encontrada"

        self.assertEqual(nota.nota, 4.5)

    def test_calcular_promedio(self):
        self.preparar_calificaciones()

        self.assertEqual(
            self.sistema.calcular_promedio(
                self.codigo_inscripcion
            ),
            4.0
        )

    def test_recalcular_promedio(self):
        self.preparar_calificaciones()

        self.sistema.modificar_calificacion(
            self.notas_creadas[0],
            4.0
        )

        self.assertEqual(
            self.sistema.calcular_promedio(
                self.codigo_inscripcion
            ),
            4.33
        )

    def test_estado_aprobado(self):
        self.preparar_calificaciones()

        self.assertEqual(
            self.sistema.obtener_estado_academico(
                self.codigo_inscripcion
            ),
            "Aprobado"
        )

    def test_estado_reprobado(self):
        self.preparar_inscripcion()

        for numero in range(1, 4):
            self.registrar_nota(numero, 2.0)

        self.assertEqual(
            self.sistema.obtener_estado_academico(
                self.codigo_inscripcion
            ),
            "Reprobado"
        )

    def test_rendimiento_pendiente(self):
        self.preparar_inscripcion()
        self.registrar_nota(1, 4.0)

        resultado = self.sistema.consultar_rendimiento_inscripcion(
            self.codigo_inscripcion
        )

        self.assertIsNone(resultado["promedio"])
        self.assertEqual(resultado["estado"], "Pendiente")

    def test_promedio_insuficiente(self):
        self.preparar_inscripcion()
        self.registrar_nota(1, 4.0)

        with self.assertRaises(ValueError):
            self.sistema.calcular_promedio(
                self.codigo_inscripcion
            )

    def test_buscar_notas_por_inscripcion(self):
        self.preparar_calificaciones()

        resultado = self.sistema.consultar_calificaciones_inscripcion(
            self.codigo_inscripcion
        )

        self.assertEqual(len(resultado), 3)

    def test_buscar_notas_por_aprendiz(self):
        self.preparar_calificaciones()

        resultado = self.sistema.consultar_calificaciones_aprendiz(
            self.doc_aprendiz
        )

        self.assertEqual(len(resultado), 3)

    def test_buscar_notas_por_curso(self):
        self.preparar_calificaciones()

        resultado = self.sistema.consultar_calificaciones_curso(
            self.codigo_curso
        )

        self.assertEqual(len(resultado), 3)

    def test_impedir_modificacion_finalizada(self):
        self.preparar_calificaciones()

        self.sistema.finalizar_inscripcion(
            self.codigo_inscripcion
        )

        with self.assertRaises(ValueError):
            self.sistema.modificar_calificacion(
                self.notas_creadas[0],
                5.0
            )

    def test_impedir_nota_en_inscripcion_cancelada(self):
        self.preparar_inscripcion()

        self.sistema.cancelar_inscripcion(
            self.codigo_inscripcion
        )

        with self.assertRaises(ValueError):
            self.registrar_nota(1, 4.0)
