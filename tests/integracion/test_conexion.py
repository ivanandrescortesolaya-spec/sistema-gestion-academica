from integracion import BaseIntegracion


class TestConexion(BaseIntegracion):

    def test_conexion_mysql(self):
        self.assertTrue(self.conexion.verificar_conexion())

    def test_base_datos_pruebas(self):
        self.assertEqual(
            self.config.base_datos,
            "sistema_gestion_academica_test"
        )

    def test_usuario_pruebas(self):
        self.assertEqual(
            self.config.usuario,
            "academic_test_user"
        )

    def test_transaccion_rollback(self):
        documento = str(self.doc_profesor)

        with self.assertRaises(RuntimeError):
            with self.conexion.transaccion() as cn:
                cursor = cn.cursor()

                try:
                    cursor.execute("""
                        INSERT INTO persona
                            (documento, nombre, edad)
                        VALUES (%s, %s, %s)
                    """, (documento, "Rollback", 30))

                    raise RuntimeError("Forzar rollback")

                finally:
                    cursor.close()

        with self.conexion.transaccion() as cn:
            cursor = cn.cursor()

            try:
                cursor.execute(
                    "SELECT COUNT(*) FROM persona WHERE documento = %s",
                    (documento,)
                )

                fila = cursor.fetchone()

                assert isinstance(fila, (tuple, list)), (
                    "MySQL no devolvió una fila válida"
                )

                self.assertEqual(len(fila), 1)
                self.assertEqual(fila[0], 0)

            finally:
                cursor.close()
