# Software FJ – Sistema Integral de Gestión de Clientes, Servicios y Reservas
Curso Programación (213023) – UNAD – Fase 4. Python 3.8+, sin bases de datos ni librerías externas.

## Ejecución
    python main.py
Genera `logs/software_fj.log` con todos los eventos (INFO/DEBUG) y errores (ERROR/CRITICAL).

## Estructura
| Archivo | Contenido |
|---|---|
| `excepciones.py` | Excepciones personalizadas (jerarquía desde `ErrorSoftwareFJ`) |
| `logger_config.py` | Configuración del log en archivo |
| `entidades.py` | `EntidadBase` (abstracta) y `Cliente` (encapsulación y validaciones) |
| `servicios.py` | `Servicio` (abstracta) + `ReservaSala`, `AlquilerEquipo`, `Asesoria` |
| `reserva.py` | `Reserva`: confirmar, cancelar, procesar (try/except/else/finally y `raise ... from`) |
| `gestor.py` | `GestorFJ`: listas internas y ejecución protegida de operaciones |
| `main.py` | 20 simulaciones (válidas e inválidas) |

## Conceptos aplicados
- **Abstracción / herencia / polimorfismo**: `calcular_costo`, `describir`, `validar_parametros` sobrescritos.
- **Encapsulación**: atributos privados con propiedades validadas.
- **Sobrecarga**: `calcular_costo_total(horas, impuesto=0, descuento=0, **params)` (variantes por parámetros opcionales).
- **Excepciones**: try/except, try/except/else, try/except/finally y encadenamiento (`raise X from e`).
- **Estabilidad**: `GestorFJ._ejecutar` captura incluso errores inesperados; el programa nunca se detiene.

## Equipo (5 integrantes) – ramas sugeridas
`feature/excepciones-logs`, `feature/cliente`, `feature/servicios`, `feature/reserva`, `feature/gestor-simulacion`.
