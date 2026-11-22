"""Servicio abstracto y tres servicios especializados (polimorfismo)."""
from abc import abstractmethod

from entidades import EntidadBase
from excepciones import (CalculoInconsistenteError, ParametroFaltanteError,
                         ServicioInvalidoError)


class Servicio(EntidadBase):
    def __init__(self, nombre, tarifa_hora):
        super().__init__()
        if not isinstance(nombre, str) or not nombre.strip():
            raise ServicioInvalidoError("El nombre del servicio es obligatorio")
        if not isinstance(tarifa_hora, (int, float)) or isinstance(tarifa_hora, bool) or tarifa_hora <= 0:
            raise ServicioInvalidoError(f"Tarifa inválida: {tarifa_hora!r}")
        self._nombre = nombre.strip()
        self._tarifa_hora = float(tarifa_hora)
        self._disponible = True

    @property
    def nombre(self):
        return self._nombre

    @property
    def disponible(self):
        return self._disponible

    @disponible.setter
    def disponible(self, valor: bool):
        self._disponible = bool(valor)

    @abstractmethod
    def calcular_costo(self, horas, **params) -> float:
        """Costo base (sin impuestos ni descuentos)."""

    @abstractmethod
    def validar_parametros(self, **params) -> None:
        """Valida los parámetros propios del servicio."""

    def calcular_costo_total(self, horas, impuesto=0.0, descuento=0.0, **params) -> float:
        """Método 'sobrecargado' mediante parámetros opcionales:
        costo_total(h) | costo_total(h, impuesto) | costo_total(h, impuesto, descuento)."""
        try:
            self.validar_parametros(horas=horas, **params)
            base = self.calcular_costo(horas, **params)
            if not (0 <= impuesto <= 1 and 0 <= descuento <= 1):
                raise ValueError("Impuesto y descuento deben estar entre 0 y 1")
            total = base * (1 - descuento) * (1 + impuesto)
            if total <= 0:
                raise ArithmeticError("El costo total debe ser positivo")
            return round(total, 2)
        except (ValueError, ArithmeticError, TypeError) as e:
            raise CalculoInconsistenteError(f"Cálculo inconsistente en '{self.nombre}'") from e

    def _exigir(self, params, *claves):
        faltan = [c for c in claves if params.get(c) is None]
        if faltan:
            raise ParametroFaltanteError(f"'{self.nombre}' requiere: {', '.join(faltan)}")


class ReservaSala(Servicio):
    def __init__(self, nombre, tarifa_hora, capacidad):
        super().__init__(nombre, tarifa_hora)
        if not isinstance(capacidad, int) or capacidad <= 0:
            raise ServicioInvalidoError(f"Capacidad inválida: {capacidad!r}")
        self._capacidad = capacidad

    def validar_parametros(self, **p):
        self._exigir(p, "horas", "personas")
        if not 1 <= p["horas"] <= 12:
            raise ParametroFaltanteError("Horas fuera de rango (1-12)")
        if not 1 <= p["personas"] <= self._capacidad:
            raise ParametroFaltanteError(f"Personas excede capacidad ({self._capacidad})")

    def calcular_costo(self, horas, **p):
        return self._tarifa_hora * horas + (50000 if p.get("proyector") else 0)

    def describir(self):
        return f"Sala '{self.nombre}' (cap. {self._capacidad}) ${self._tarifa_hora:,.0f}/h"


class AlquilerEquipo(Servicio):
    def __init__(self, nombre, tarifa_hora, stock):
        super().__init__(nombre, tarifa_hora)
        if not isinstance(stock, int) or stock <= 0:
            raise ServicioInvalidoError(f"Stock inválido: {stock!r}")
        self._stock = stock

    def validar_parametros(self, **p):
        self._exigir(p, "horas", "cantidad")
        if not 1 <= p["horas"] <= 12:
            raise ParametroFaltanteError("Horas fuera de rango (1-12)")
        if not 1 <= p["cantidad"] <= self._stock:
            raise ParametroFaltanteError(f"Cantidad supera el stock ({self._stock})")

    def calcular_costo(self, horas, **p):
        return self._tarifa_hora * horas * p["cantidad"]

    def describir(self):
        return f"Equipo '{self.nombre}' (stock {self._stock}) ${self._tarifa_hora:,.0f}/h c/u"


class Asesoria(Servicio):
    _FACTOR = {"junior": 1.0, "senior": 1.8}

    def __init__(self, nombre, tarifa_hora, especialidad):
        super().__init__(nombre, tarifa_hora)
        if not isinstance(especialidad, str) or not especialidad.strip():
            raise ServicioInvalidoError("Especialidad obligatoria")
        self._especialidad = especialidad.strip()

    def validar_parametros(self, **p):
        self._exigir(p, "horas", "nivel")
        if p["nivel"] not in self._FACTOR:
            raise ParametroFaltanteError(f"Nivel inválido: {p['nivel']!r}")
        if not 1 <= p["horas"] <= 12:
            raise ParametroFaltanteError("Horas fuera de rango (1-12)")

    def calcular_costo(self, horas, **p):
        return self._tarifa_hora * horas * self._FACTOR[p["nivel"]]

    def describir(self):
        return f"Asesoría '{self.nombre}' en {self._especialidad} ${self._tarifa_hora:,.0f}/h"
