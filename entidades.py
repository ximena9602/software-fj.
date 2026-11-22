"""Clase abstracta base y clase Cliente (encapsulación + validaciones)."""
import re
from abc import ABC, abstractmethod
from itertools import count

from excepciones import ClienteInvalidoError


class EntidadBase(ABC):
    """Entidad general del sistema: todo objeto tiene id y descripción."""
    _contador = count(1)

    def __init__(self):
        self._id = next(EntidadBase._contador)

    @property
    def id(self) -> int:
        return self._id

    @abstractmethod
    def describir(self) -> str:
        """Devuelve una descripción legible de la entidad."""


class Cliente(EntidadBase):
    _EMAIL = re.compile(r"^[\w.+-]+@[\w-]+\.[\w.-]+$")

    def __init__(self, nombre, documento, email, telefono):
        super().__init__()
        self.nombre = nombre
        self.documento = documento
        self.email = email
        self.telefono = telefono

    # ---- propiedades con validación (datos personales encapsulados) ----
    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, v):
        if not isinstance(v, str) or len(v.strip()) < 3 or any(c.isdigit() for c in v):
            raise ClienteInvalidoError(f"Nombre inválido: {v!r}")
        self.__nombre = v.strip().title()

    @property
    def documento(self):
        return self.__documento

    @documento.setter
    def documento(self, v):
        if not (isinstance(v, str) and v.isdigit() and 6 <= len(v) <= 12):
            raise ClienteInvalidoError(f"Documento inválido (6-12 dígitos): {v!r}")
        self.__documento = v

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, v):
        if not isinstance(v, str) or not self._EMAIL.match(v):
            raise ClienteInvalidoError(f"Email inválido: {v!r}")
        self.__email = v.lower()

    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, v):
        if not (isinstance(v, str) and v.isdigit() and 7 <= len(v) <= 10):
            raise ClienteInvalidoError(f"Teléfono inválido (7-10 dígitos): {v!r}")
        self.__telefono = v

    def describir(self) -> str:
        return f"Cliente #{self.id}: {self.nombre} | Doc {self.documento} | {self.email}"
