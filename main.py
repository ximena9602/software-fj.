"""Software FJ - Simulación de 16 operaciones (válidas e inválidas)."""
from gestor import GestorFJ
from logger_config import RUTA_LOG, obtener_logger
from servicios import Asesoria, AlquilerEquipo, ReservaSala

log = obtener_logger()


def main():
    g = GestorFJ()
    log.info("=== INICIO DE SIMULACIÓN SOFTWARE FJ ===")

    # --- Clientes ---
    ana = g._ejecutar("1. Cliente válido (Ana)", g.registrar_cliente,
                                               "ana gómez", "1012345678", "ana@correo.com", "3001234567")
    luis = g._ejecutar("2. Cliente válido (Luis)", g.registrar_cliente,
                       "Luis Pérez", "80123456", "luis@correo.com", "3109876543")
    g._ejecutar("3. Cliente inválido (email)", g.registrar_cliente,
                "Pedro Ruiz", "123456789", "pedro-correo", "3001112233")
    g._ejecutar("4. Cliente inválido (documento corto)", g.registrar_cliente,
                "Marta Díaz", "123", "marta@correo.com", "3001112233")
    g._ejecutar("5. Cliente duplicado", g.registrar_cliente,
                "Ana Copia", "1012345678", "copia@correo.com", "3001234567")

    # --- Servicios ---
    sala = g._ejecutar("6. Servicio válido: sala", g.agregar_servicio, ReservaSala, "Sala Innovación", 80000, 10)
    equipo = g._ejecutar("7. Servicio válido: equipo", g.agregar_servicio, AlquilerEquipo, "Portátil Pro", 15000, 5)
    asesoria = g._ejecutar("8. Servicio válido: asesoría", g.agregar_servicio, Asesoria, "Arquitectura Cloud", 120000, "Cloud")
    g._ejecutar("9. Servicio inválido (tarifa negativa)", g.agregar_servicio, ReservaSala, "Sala X", -5, 10)

    # --- Reservas ---
    r1 = g._ejecutar("10. Reserva exitosa de sala", g.crear_reserva, ana, sala, 3, personas=8, proyector=True)
    if r1:
        g._ejecutar("11. Confirmar + procesar (19% IVA, 10% desc.)",
                    lambda: (r1.confirmar(), f"Total ${r1.procesar(0.19, 0.10):,.2f}")[1])
    g._ejecutar("12. Reserva inválida (horas fuera de rango)", g.crear_reserva, luis, asesoria, 30, nivel="senior")
    g._ejecutar("13. Reserva con parámetro faltante (sin cantidad)", g.crear_reserva, luis, equipo, 2)
    if equipo:
        equipo.disponible = False
    g._ejecutar("14. Servicio no disponible", g.crear_reserva, luis, equipo, 2, cantidad=2)
    r2 = g._ejecutar("15. Reserva de asesoría senior", g.crear_reserva, luis, asesoria, 2, nivel="senior")
    if r2:
        g._ejecutar("16. Procesar sin confirmar (no permitido)", r2.procesar)
        g._ejecutar("17. Cancelar reserva", lambda: (r2.cancelar(), "Cancelada")[1])
        g._ejecutar("18. Confirmar reserva cancelada (no permitido)", r2.confirmar)
    g._ejecutar("19. Reserva con cliente inexistente (None)", g.crear_reserva, None, sala, 1, personas=2)
    g._ejecutar("20. Cálculo inconsistente (descuento 250%)",
                lambda: sala.calcular_costo_total(2, 0.19, 2.5, personas=3))

    # --- Polimorfismo ---
    print("\n▶ Descripción polimórfica de servicios")
    for s in g.servicios:
        print("   •", s.describir())
    print("\n▶ Reservas registradas")
    for r in g.reservas:
        print("   •", r.describir())

    log.info("=== FIN: %s exitosas, %s fallidas ===", g.exitos, g.fallos)
    print(f"\nResumen: {g.exitos} operaciones exitosas, {g.fallos} fallos controlados.")
    print(f"Log generado en: {RUTA_LOG}")


if __name__ == "__main__":
    main()
