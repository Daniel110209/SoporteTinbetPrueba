from utilidades import formatear_dni, generar_codigo, buscar_posicion
from entradas import leer_entero, leer_rango, confirmar
from fechas import ahora
from pantalla import mostrar_titulo
from archivos import guardar_saldos, guardar_apuestas, guardar_resultados
from log import registrar_bitacora
from seguridad import exigir_admin

EVENTOS = [
    ("Alianza Lima vs Universitario", 2.40, 3.10, 2.90),
    ("Sporting Cristal vs Melgar", 1.95, 3.30, 3.80),
    ("Peru vs Chile", 2.20, 3.00, 3.30),
    ("Real Madrid vs Barcelona", 2.30, 3.50, 2.80),
    ("Boca Juniors vs River Plate", 2.60, 3.00, 2.70),
]
PRONOSTICOS = ["1", "X", "2"]
TEXTOS = ["Gana local", "Empate", "Gana visita"]
METODOS = ["Yape", "Plin", "Visa", "BCP"]
APUESTA_MAXIMA = 500
DEPOSITO_MAXIMO = 1000


def saldo_de(datos, dni):
    return datos["saldos"].get(dni, 0.0)


def contar_pendientes(datos):
    total = 0
    for ap in datos["apuestas"]:
        if ap["estado"] == "PENDIENTE":
            total = total + 1
    return total


def tiene_apuestas_pendientes(datos, dni):
    for ap in datos["apuestas"]:
        if ap["dni"] == dni and ap["estado"] == "PENDIENTE":
            return True
    return False


def pedir_usuario(datos, sesion):
    dni = formatear_dni(leer_entero("DNI del usuario: "))
    pos = buscar_posicion(datos["dnis"], dni)
    if pos == -1:
        print("El usuario no esta registrado. Registrelo primero.")
        registrar_bitacora(sesion["usuario"], f"Apuestas denegadas: DNI {dni} no registrado")
        return None
    print(f"Usuario: {datos['nombres'][pos]}")
    return dni


def mostrar_eventos(datos):
    print(f" {'N':<3}{'EVENTO':<32}{'LOCAL':<7}{'EMPATE':<8}{'VISITA':<8}")
    for i in range(len(EVENTOS)):
        nombre, local, empate, visita = EVENTOS[i]
        if i in datos["resultados"]:
            estado = "CERRADO"
        else:
            estado = ""
        print(f" {i + 1:<3}{nombre:<32}{local:<7.2f}{empate:<8.2f}{visita:<8.2f}{estado}")


def depositar(datos, sesion):
    mostrar_titulo("Depositar saldo")
    dni = pedir_usuario(datos, sesion)
    if dni is None:
        return
    print("\nMetodos de pago:")
    for i in range(len(METODOS)):
        print(f" {i + 1}. {METODOS[i]}")
    metodo = leer_rango("Elija el metodo (0 = cancelar): ", 0, len(METODOS))
    if metodo == 0:
        return
    monto = leer_rango(f"Monto en soles (0 = cancelar, maximo {DEPOSITO_MAXIMO}): ", 0, DEPOSITO_MAXIMO)
    if monto == 0:
        return
    datos["saldos"][dni] = round(saldo_de(datos, dni) + monto, 2)
    guardar_saldos(datos)
    registrar_bitacora(sesion["usuario"], f"Deposito de S/ {monto} por {METODOS[metodo - 1]} (DNI {dni})")
    print(f"\nDeposito registrado. Saldo actual: S/ {datos['saldos'][dni]:.2f}")


def ver_saldo(datos, sesion):
    mostrar_titulo("Saldo del usuario")
    dni = pedir_usuario(datos, sesion)
    if dni is None:
        return
    print(f"Saldo disponible: S/ {saldo_de(datos, dni):.2f}")


def apostar(datos, sesion):
    mostrar_titulo("Apostar")
    dni = pedir_usuario(datos, sesion)
    if dni is None:
        return
    saldo = saldo_de(datos, dni)
    print(f"Saldo disponible: S/ {saldo:.2f}")
    if saldo < 1:
        print("Saldo insuficiente. Deposite primero.")
        return
    print()
    mostrar_eventos(datos)
    evento = leer_rango("\nElija el evento (0 = cancelar): ", 0, len(EVENTOS))
    if evento == 0:
        return
    if (evento - 1) in datos["resultados"]:
        print("Ese evento ya termino. Elija otro.")
        return
    print("\n 1. Gana local\n 2. Empate\n 3. Gana visita")
    opcion = leer_rango("Su pronostico (0 = cancelar): ", 0, 3)
    if opcion == 0:
        return
    cuota = EVENTOS[evento - 1][opcion]
    tope = min(APUESTA_MAXIMA, int(saldo))
    monto = leer_rango(f"Monto en soles (0 = cancelar, maximo {tope}): ", 0, tope)
    if monto == 0:
        return
    print(f"\nEvento: {EVENTOS[evento - 1][0]}")
    print(f"Pronostico: {TEXTOS[opcion - 1]} (cuota {cuota:.2f})")
    print(f"Ganancia posible: S/ {monto * cuota:.2f}")
    if not confirmar("Confirmar apuesta"):
        return
    ticket = generar_codigo(8)
    datos["apuestas"].append({
        "ticket": ticket,
        "dni": dni,
        "evento": evento - 1,
        "pronostico": PRONOSTICOS[opcion - 1],
        "monto": monto,
        "cuota": cuota,
        "estado": "PENDIENTE",
        "fecha": ahora(),
    })
    datos["saldos"][dni] = round(saldo - monto, 2)
    guardar_apuestas(datos)
    guardar_saldos(datos)
    registrar_bitacora(sesion["usuario"], f"Apuesta {ticket} de S/ {monto} (DNI {dni}, evento {evento})")
    print(f"\nApuesta registrada. Ticket: {ticket}. Saldo actual: S/ {datos['saldos'][dni]:.2f}")


def ver_apuestas(datos, sesion):
    mostrar_titulo("Apuestas del usuario")
    dni = pedir_usuario(datos, sesion)
    if dni is None:
        return
    encontradas = 0
    for ap in datos["apuestas"]:
        if ap["dni"] == dni:
            encontradas = encontradas + 1
            nombre = EVENTOS[ap["evento"]][0]
            print(f" {ap['ticket']} | {nombre} | {ap['pronostico']} | S/ {ap['monto']} | cuota {ap['cuota']:.2f} | {ap['estado']}")
    if encontradas == 0:
        print("Este usuario no tiene apuestas.")


def liquidar_evento(datos, indice, ganador):
    ganadas = 0
    perdidas = 0
    pagado = 0.0
    for ap in datos["apuestas"]:
        if ap["evento"] == indice and ap["estado"] == "PENDIENTE":
            if ap["pronostico"] == ganador:
                premio = round(ap["monto"] * ap["cuota"], 2)
                datos["saldos"][ap["dni"]] = round(saldo_de(datos, ap["dni"]) + premio, 2)
                ap["estado"] = "GANADA"
                ganadas = ganadas + 1
                pagado = pagado + premio
            else:
                ap["estado"] = "PERDIDA"
                perdidas = perdidas + 1
    datos["resultados"][indice] = ganador
    return ganadas, perdidas, pagado


def resolver_evento(datos, sesion):
    if not exigir_admin(sesion, "Resolver un evento"):
        return
    mostrar_titulo("Resolver evento (administrador)")
    mostrar_eventos(datos)
    evento = leer_rango("\nEvento a cerrar (0 = cancelar): ", 0, len(EVENTOS))
    if evento == 0:
        return
    if (evento - 1) in datos["resultados"]:
        print("Ese evento ya fue cerrado.")
        return
    print("\n 1. Gano el local\n 2. Empate\n 3. Gano la visita")
    resultado = leer_rango("Resultado (0 = cancelar): ", 0, 3)
    if resultado == 0:
        return
    ganadas, perdidas, pagado = liquidar_evento(datos, evento - 1, PRONOSTICOS[resultado - 1])
    guardar_apuestas(datos)
    guardar_saldos(datos)
    guardar_resultados(datos)
    registrar_bitacora(
        sesion["usuario"],
        f"Evento {evento} cerrado: {ganadas} ganadas, {perdidas} perdidas, S/ {pagado:.2f} pagados",
    )
    print(f"\nEvento cerrado. Ganadas: {ganadas} | Perdidas: {perdidas} | Pagado: S/ {pagado:.2f}")


def mostrar_menu_apuestas():
    mostrar_titulo("Apuestas")
    print(" 1. Depositar saldo")
    print(" 2. Ver saldo")
    print(" 3. Ver eventos y cuotas")
    print(" 4. Apostar")
    print(" 5. Ver apuestas de un usuario")
    print(" 6. Resolver evento        [solo administrador]")
    print(" 0. Volver")


def gestionar_apuestas(datos, sesion):
    opcion = -1
    while opcion != 0:
        mostrar_menu_apuestas()
        opcion = leer_entero("Elija una opcion: ")
        if opcion == 1:
            depositar(datos, sesion)
        elif opcion == 2:
            ver_saldo(datos, sesion)
        elif opcion == 3:
            mostrar_titulo("Eventos y cuotas")
            mostrar_eventos(datos)
        elif opcion == 4:
            apostar(datos, sesion)
        elif opcion == 5:
            ver_apuestas(datos, sesion)
        elif opcion == 6:
            resolver_evento(datos, sesion)
        elif opcion != 0:
            print("Opcion no valida.")
