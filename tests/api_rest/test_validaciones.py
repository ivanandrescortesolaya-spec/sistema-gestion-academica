import unittest

from datetime import date

from api.excepciones import DatosInvalidos

from api.validaciones import (
    validar_campos,
    validar_texto,
    validar_entero,
    validar_documento,
    validar_codigo,
    validar_nota,
    validar_modalidad,
    validar_estado,
    validar_fecha
)


class TestValidacionesAPI(unittest.TestCase):

    # Validación de campos

    def test_campos_obligatorios_validos(self):

        validar_campos(
            {"nombre": "Python"},
            {"nombre"}
        )

    def test_campos_obligatorios_faltantes(self):

        with self.assertRaises(DatosInvalidos):

            validar_campos(
                {},
                {"nombre"}
            )

    def test_campos_desconocidos(self):

        with self.assertRaises(DatosInvalidos):

            validar_campos(
                {
                    "nombre": "Python",
                    "desconocido": True
                },
                {"nombre"}
            )

    def test_campos_opcionales(self):

        validar_campos(
            {
                "codigo": "INS-001",
                "fecha": "2026-11-28"
            },
            {"codigo"},
            {"fecha"}
        )

    def test_campos_opcionales_ausentes(self):

        validar_campos(
            {"codigo": "INS-001"},
            {"codigo"},
            {"fecha"}
        )

    # Validación de texto

    def test_texto_valido(self):

        self.assertEqual(
            validar_texto("Python", "nombre"),
            "Python"
        )

    def test_texto_eliminar_espacios(self):

        self.assertEqual(
            validar_texto("  Python  ", "nombre"),
            "Python"
        )

    def test_texto_vacio(self):

        for valor in ("", " ", "   "):

            with self.subTest(valor=valor):

                with self.assertRaises(DatosInvalidos):

                    validar_texto(valor, "nombre")

    def test_texto_tipo_invalido(self):

        for valor in (123, True, None, [], {}):

            with self.subTest(valor=valor):

                with self.assertRaises(DatosInvalidos):

                    validar_texto(valor, "nombre")

    def test_texto_longitud_maxima(self):

        self.assertEqual(
            validar_texto(
                "Python",
                "nombre",
                maximo=6
            ),
            "Python"
        )

    def test_texto_supera_longitud(self):

        with self.assertRaises(DatosInvalidos):

            validar_texto(
                "Python",
                "nombre",
                maximo=5
            )

    # Validación de enteros

    def test_entero_valido(self):

        self.assertEqual(
            validar_entero(25, "edad"),
            25
        )

    def test_entero_limites_validos(self):

        for valor in (1, 100):

            with self.subTest(valor=valor):

                self.assertEqual(
                    validar_entero(
                        valor,
                        "cantidad",
                        minimo=1,
                        maximo=100
                    ),
                    valor
                )

    def test_entero_inferior_minimo(self):

        with self.assertRaises(DatosInvalidos):

            validar_entero(
                0,
                "cantidad",
                minimo=1
            )

    def test_entero_superior_maximo(self):

        with self.assertRaises(DatosInvalidos):

            validar_entero(
                101,
                "cantidad",
                maximo=100
            )

    def test_entero_tipo_invalido(self):

        for valor in (
            True, False, 1.5, "25", None, []
        ):

            with self.subTest(valor=valor):

                with self.assertRaises(DatosInvalidos):

                    validar_entero(valor, "edad")

    # Validación de documentos

    def test_documento_entero(self):

        self.assertEqual(
            validar_documento(123456789),
            123456789
        )

    def test_documento_texto_numerico(self):

        self.assertEqual(
            validar_documento("123456789"),
            123456789
        )

    def test_documento_maximo(self):

        documento = 10**20 - 1

        self.assertEqual(
            validar_documento(documento),
            documento
        )

    def test_documento_supera_maximo(self):

        with self.assertRaises(DatosInvalidos):

            validar_documento(10**20)

    def test_documentos_invalidos(self):

        valores = (
            0,
            -1,
            True,
            12.5,
            "",
            "ABC123",
            "00123",
            None
        )

        for valor in valores:

            with self.subTest(valor=valor):

                with self.assertRaises(DatosInvalidos):

                    validar_documento(valor)

    # Validación de códigos

    def test_codigo_valido(self):

        for codigo in (
            "CUR-001",
            "INS_001",
            "Python123"
        ):

            with self.subTest(codigo=codigo):

                self.assertEqual(
                    validar_codigo(codigo),
                    codigo
                )

    def test_codigo_longitud_maxima(self):

        codigo = "A" * 30

        self.assertEqual(
            validar_codigo(codigo),
            codigo
        )

    def test_codigo_supera_longitud(self):

        with self.assertRaises(DatosInvalidos):

            validar_codigo("A" * 31)

    def test_codigos_invalidos(self):

        valores = (
            "",
            "CUR 001",
            "CUR/001",
            "CUR@001",
            "CUR.001",
            "CÓDIGO",
            123,
            None
        )

        for valor in valores:

            with self.subTest(valor=valor):

                with self.assertRaises(DatosInvalidos):

                    validar_codigo(valor)

    # Validación de notas

    def test_nota_entera(self):

        self.assertEqual(
            validar_nota(4),
            4.0
        )

    def test_nota_decimal(self):

        self.assertEqual(
            validar_nota(4.25),
            4.25
        )

    def test_nota_limites_validos(self):

        for nota in (0.0, 5.0):

            with self.subTest(nota=nota):

                self.assertEqual(
                    validar_nota(nota),
                    nota
                )

    def test_nota_fuera_rango(self):

        for nota in (-0.01, 5.01, 10):

            with self.subTest(nota=nota):

                with self.assertRaises(DatosInvalidos):

                    validar_nota(nota)

    def test_nota_exceso_decimales(self):

        with self.assertRaises(DatosInvalidos):

            validar_nota(4.123)

    def test_nota_tipo_invalido(self):

        for nota in ("4.5", True, None, []):

            with self.subTest(nota=nota):

                with self.assertRaises(DatosInvalidos):

                    validar_nota(nota)

    def test_nota_no_finita(self):

        valores = (
            float("nan"),
            float("inf"),
            float("-inf")
        )

        for nota in valores:

            with self.subTest(nota=nota):

                with self.assertRaises(DatosInvalidos):

                    validar_nota(nota)

    # Validación de modalidades

    def test_modalidades_validas(self):

        for modalidad in (
            "titulada",
            "complementaria"
        ):

            with self.subTest(modalidad=modalidad):

                self.assertEqual(
                    validar_modalidad(modalidad),
                    modalidad
                )

    def test_normalizar_modalidad(self):

        self.assertEqual(
            validar_modalidad("  TITULADA  "),
            "titulada"
        )

    def test_modalidades_invalidas(self):

        for modalidad in (
            "virtual",
            "presencial",
            "",
            None
        ):

            with self.subTest(modalidad=modalidad):

                with self.assertRaises(DatosInvalidos):

                    validar_modalidad(modalidad)

    # Validación de estados

    def test_estados_validos(self):

        for estado in (
            "Cancelada",
            "Finalizada"
        ):

            with self.subTest(estado=estado):

                self.assertEqual(
                    validar_estado(estado),
                    estado
                )

    def test_estado_activa_no_permitido(self):

        with self.assertRaises(DatosInvalidos):

            validar_estado("Activa")

    def test_estados_invalidos(self):

        for estado in (
            "Pendiente",
            "finalizada",
            "",
            None
        ):

            with self.subTest(estado=estado):

                with self.assertRaises(DatosInvalidos):

                    validar_estado(estado)

    # Validación de fechas

    def test_fecha_valida(self):

        self.assertEqual(
            validar_fecha(
                "2026-11-28",
                "fecha"
            ),
            date(2026, 11, 28)
        )

    def test_fecha_anio_bisiesto(self):

        self.assertEqual(
            validar_fecha(
                "2024-02-29",
                "fecha"
            ),
            date(2024, 2, 29)
        )

    def test_fecha_formato_invalido(self):

        valores = (
            "28/11/2026",
            "28-11-2026",
            "2026-1-1",
            "20261128",
            ""
        )

        for valor in valores:

            with self.subTest(valor=valor):

                with self.assertRaises(DatosInvalidos):

                    validar_fecha(valor, "fecha")

    def test_fecha_calendario_invalido(self):

        valores = (
            "2026-02-29",
            "2026-02-30",
            "2026-13-01",
            "2026-01-32"
        )

        for valor in valores:

            with self.subTest(valor=valor):

                with self.assertRaises(DatosInvalidos):

                    validar_fecha(valor, "fecha")

    def test_fecha_tipo_invalido(self):

        for valor in (123, None, True, []):

            with self.subTest(valor=valor):

                with self.assertRaises(DatosInvalidos):

                    validar_fecha(valor, "fecha")


if __name__ == "__main__":

    unittest.main()