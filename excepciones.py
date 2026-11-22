"""Excepciones personalizadas de Software FJ."""


class ErrorSoftwareFJ(Exception):
    """Excepción base del sistema."""


class ClienteInvalidoError(ErrorSoftwareFJ):
    """Datos de cliente inválidos."""


class ServicioInvalidoError(ErrorSoftwareFJ):
    """Datos de servicio inválidos."""


class ServicioNoDisponibleError(ErrorSoftwareFJ):
    """El servicio solicitado no está disponible."""


class ParametroFaltanteError(ErrorSoftwareFJ):
    """Falta un parámetro obligatorio."""


class ReservaInvalidaError(ErrorSoftwareFJ):
    """Reserva incorrecta o que no pudo procesarse."""


class OperacionNoPermitidaError(ErrorSoftwareFJ):
    """Operación no permitida para el estado actual."""


class CalculoInconsistenteError(ErrorSoftwareFJ):
    """Cálculo de costos inconsistente."""
