"""Clase Reserva: integra cliente, servicio, duración y estado."""
from entidades import Cliente, EntidadBase
from excepciones import (CalculoInconsistenteError, ErrorSoftwareFJ,
                         OperacionNoPermitidaError, ReservaInvalidaError,
                         ServicioNoDisponibleError)
from logger_config import obtener_logger
from servicios import Servicio

log = obtener_logger()


class Reserva(EntidadBase):
    PENDIENTE, CONFIRMADA, CANCELADA, PROCESADA, FALLIDA = (
        "PENDIENTE", "CONFIRMADA", "CANCELADA", "PROCESADA", "FALLIDA")

    def __init__(self, cliente, servicio, horas, **params):
        super().__init__()
        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError("La reserva requiere un Cliente válido")
        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("La reserva requiere un Servicio válido")
        if not servicio.disponible:
            raise ServicioNoDisponibleError(f"'{servicio.nombre}' no está disponible")
        try:
            servicio.validar_parametros(horas=horas, **params)
        except ErrorSoftwareFJ as e:
            raise ReservaInvalidaError("Parámetros de reserva inválidos") from e
        self._cliente, self._servicio = cliente, servicio
        self._horas, self._params = horas, params
        self._estado, self._costo = self.PENDIENTE, None

    @property
    def estado(self):
        return self._estado

    @property
    def costo(self):
        return self._costo

    def confirmar(self):
        try:
            if self._estado != self.PENDIENTE:
                raise OperacionNoPermitidaError(
                    f"No se puede confirmar una reserva {self._estado}")
            if not self._servicio.disponible:
                raise ServicioNoDisponibleError(f"'{self._servicio.nombre}' ya no está disponible")
        except ErrorSoftwareFJ as e:
            log.error("Reserva #%s: fallo al confirmar -> %s", self.id, e)
            raise
        else:
            self._estado = self.CONFIRMADA
            log.info("Reserva #%s confirmada", self.id)
        finally:
            log.debug("Reserva #%s: intento de confirmación finalizado", self.id)

    def cancelar(self):
        if self._estado in (self.PROCESADA, self.CANCELADA):
            raise OperacionNoPermitidaError(f"No se puede cancelar una reserva {self._estado}")
        self._estado = self.CANCELADA
        log.info("Reserva #%s cancelada", self.id)

    def procesar(self, impuesto=0.19, descuento=0.0):
        """Calcula el costo final. Encadena la causa original con 'raise ... from'."""
        try:
            if self._estado != self.CONFIRMADA:
                raise OperacionNoPermitidaError(
                    f"Solo se procesan reservas CONFIRMADAS (actual: {self._estado})")
            costo = self._servicio.calcular_costo_total(
                self._horas, impuesto, descuento, **self._params)
        except CalculoInconsistenteError as e:
            self._estado = self.FALLIDA
            raise ReservaInvalidaError(f"Reserva #{self.id} no pudo procesarse") from e
        except OperacionNoPermitidaError:
            raise
        else:
            self._costo, self._estado = costo, self.PROCESADA
            log.info("Reserva #%s procesada. Total: $%s", self.id, f"{costo:,.2f}")
            return costo
        finally:
            log.debug("Reserva #%s: procesamiento finalizado (estado=%s)", self.id, self._estado)

    def describir(self):
        return (f"Reserva #{self.id} | {self._cliente.nombre} | {self._servicio.nombre} | "
                f"{self._horas}h | {self._estado}")
