from integracion import BaseIntegracion


class TestRepositorioAprendices(BaseIntegracion):

    def test_registrar_aprendiz(self):
        self.preparar_aprendiz()

        self.assertIsNotNone(
            self.sistema.buscar_aprendiz(self.doc_aprendiz)
        )

    def test_recuperar_datos_aprendiz(self):
        self.preparar_aprendiz()

        aprendiz = self.sistema.buscar_aprendiz(
            self.doc_aprendiz
        )

        assert aprendiz is not None, "Aprendiz no encontrado"

        self.assertEqual(aprendiz.nombre, self.aprendiz.nombre)
        self.assertEqual(aprendiz.documento, self.doc_aprendiz)
        self.assertEqual(aprendiz.correo, self.aprendiz.correo)
        self.assertEqual(aprendiz.telefono, self.aprendiz.telefono)
        self.assertEqual(aprendiz.direccion, self.aprendiz.direccion)

    def test_listar_aprendices(self):
        self.preparar_aprendiz()

        documentos = [
            a.documento
            for a in self.sistema.listar_aprendices()
        ]

        self.assertIn(self.doc_aprendiz, documentos)

    def test_aprendiz_duplicado(self):
        self.preparar_aprendiz()

        with self.assertRaises(ValueError):
            self.sistema.registrar_aprendiz(self.aprendiz)

    def test_aprendiz_inexistente(self):
        self.assertIsNone(
            self.sistema.buscar_aprendiz(self.doc_aprendiz)
        )
