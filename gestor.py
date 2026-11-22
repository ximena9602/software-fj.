"""Gestor central: listas internas y ejecución protegida de operaciones."""
from entidades import Cliente
from excepciones import ErrorSoftwareFJ
from logger_config import obtener_logger
from reserva import Reserva

log = obtener_logger()


class GestorFJ:
    def __init__(self):
        self.clientes, self.servicios, self.reservas = [], [], []
        self.exitos = self.fallos = 0

    def _ejecutar(self, titulo, funcion, *args, **kwargs):
        """Ejecuta una operación sin permitir que el programa se detenga."""
        print(f"\n▶ {titulo}")
        try:
            resultado = funcion(*args, **kwargs)
        except ErrorSoftwareFJ as e:
            self.fallos += 1
            causa = f" (causa: {e.__cause__!r})" if e.__cause__ else ""
            log.error("%s -> %s: %s%s", titulo, type(e).__name__, e, causa)
            print(f"   ✘ {type(e).__name__}: {e}{causa}")
            return None
        except Exception as e:  # error inesperado: se registra y el sistema continúa
            self.fallos += 1
            log.critical("%s -> error inesperado %s: %s", titulo, type(e).__name__, e, exc_info=True)
            print(f"   ✘ Error inesperado controlado: {e}")
            return None
        else:
            self.exitos += 1
            log.info("%s -> OK", titulo)
            print(f"   ✔ {resultado if isinstance(resultado, (str, float)) else 'OK'}")
            return resultado
        finally:
            log.debug("Fin de operación: %s", titulo)

    def registrar_cliente(self, *args, **kw):
        c = Cliente(*args, **kw)
        if any(x.documento == c.documento for x in self.clientes):
            from excepciones import ClienteInvalidoError
            raise ClienteInvalidoError(f"Documento duplicado: {c.documento}")
        self.clientes.append(c)
        return c

    def agregar_servicio(self, clase, *args, **kw):
        s = clase(*args, **kw)
        self.servicios.append(s)
        return s

    def crear_reserva(self, cliente, servicio, horas, **params):
        r = Reserva(cliente, servicio, horas, **params)
        self.reservas.append(r)
        return r
