from integracion import BaseIntegracion
from inscripciones.inscripcion import Inscripcion


class TestRepositorioInscripciones(BaseIntegracion):

    def test_registrar_inscripcion(self):
        self.preparar_inscripcion()

        inscripcion = self.sistema.buscar_inscripcion(
            self.codigo_inscripcion
        )

        assert inscripcion is not None, (
            "Inscripción no encontrada"
        )
        self.assertEqual(inscripcion.estado, "Activa")
        self.assertEqual(inscripcion.fecha_inscripcion, self.fecha)

    def test_inscripcion_duplicada(self):
        self.preparar_inscripcion()

        with self.assertRaises(ValueError):
            self.sistema.registrar_inscripcion(self.inscripcion)

    def test_duplicar_aprendiz_curso(self):
        self.preparar_inscripcion()

        duplicada = Inscripcion(
            "D-" + self.uid,
            self.aprendiz,
            self.curso
        )

        with self.assertRaises(ValueError):
            resultado = self.sistema.registrar_inscripcion(
                duplicada
            )

            if resultado:
                self.addCleanup(
                    self.eliminar_duplicada,
                    duplicada.codigo
                )

    def eliminar_duplicada(self, codigo):
        with self.conexion.transaccion() as cn:
            cursor = cn.cursor()

            try:
                cursor.execute(
                    "DELETE FROM inscripcion WHERE codigo = %s",
                    (codigo,)
                )
            finally:
                cursor.close()

    def test_buscar_por_aprendiz(self):
        self.preparar_inscripcion()

        resultado = self.sistema.consultar_inscripciones_aprendiz(
            self.doc_aprendiz
        )

        self.assertIn(
            self.codigo_inscripcion,
            [i.codigo for i in resultado]
        )

    def test_buscar_por_curso(self):
        self.preparar_inscripcion()

        resultado = self.sistema.consultar_inscripciones_curso(
            self.codigo_curso
        )

        self.assertIn(
            self.codigo_inscripcion,
            [i.codigo for i in resultado]
        )

    def test_cancelar_inscripcion(self):
        self.preparar_inscripcion()

        self.assertTrue(
            self.sistema.cancelar_inscripcion(
                self.codigo_inscripcion
            )
        )

        inscripcion = self.sistema.buscar_inscripcion(
            self.codigo_inscripcion
        )

        assert inscripcion is not None, (
            "Inscripción no encontrada"
        )

        self.assertEqual(inscripcion.estado, "Cancelada")

    def test_finalizar_inscripcion(self):
        self.preparar_inscripcion()

        self.assertTrue(
            self.sistema.finalizar_inscripcion(
                self.codigo_inscripcion
            )
        )

        inscripcion = self.sistema.buscar_inscripcion(
            self.codigo_inscripcion
        )

        assert inscripcion is not None, (
            "Inscripción no encontrada"
        )

        self.assertEqual(inscripcion.estado, "Finalizada")

    def test_transicion_invalida(self):
        self.preparar_inscripcion()

        self.sistema.finalizar_inscripcion(
            self.codigo_inscripcion
        )

        with self.assertRaises(ValueError):
            self.sistema.cancelar_inscripcion(
                self.codigo_inscripcion
            )

    def test_listar_inscripciones(self):
        self.preparar_inscripcion()

        self.assertIn(
            self.codigo_inscripcion,
            [
                i.codigo
                for i in self.sistema.listar_inscripciones()
            ]
        )
