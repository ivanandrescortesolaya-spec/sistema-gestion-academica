
class ErrorPersistencia(Exception):
    """Excepción base de la capa de persistencia."""


class ErrorConfiguracion(ErrorPersistencia):
    """Error de configuración."""


class ErrorConexion(ErrorPersistencia):
    """Error de conexión con MySQL."""


class ErrorOperacion(ErrorPersistencia):
    """Error durante una operación SQL."""


class ErrorIntegridad(ErrorOperacion):
    """Incumplimiento de una restricción de integridad."""


class ErrorInterbloqueo(ErrorOperacion):
    """Interbloqueo de transacciones en MySQL."""
