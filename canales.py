from utilidades import formatear_dni, buscar_posicion
from entradas import leer_entero, leer_rango, confirmar
from fechas import ahora, minutos_transcurridos
from pantalla import mostrar_titulo
from archivos import guardar_cables
from log import registrar_bitacora

CANALES = [
    "HBO Max",
    "Disney+",
    "DirecTV GO",
    "ESPN",
    "Fox Sports",
    "Movistar Deportes",
    "Liga 1 MAX",
    "GOLPERU",
    "Win Sports",
    "Prime Video",
]


def cable_libre():
    return {"estado": 0, "dni": "", "canal": "", "inicio": ""}


def contar_cables_libres(cables):
    libres = 0
    for cable in cables:
        if cable["estado"] == 0:
            libres = libres + 1
    return libres


def cable_de_usuario(cables, dni):
    for i in range(len(cables)):
        if cables[i]["estado"] == 1 and cables[i]["dni"] == dni:
            return i
    return -1


def mostrar_canales():
    for i in range(len(CANALES)):
        print(f" {i + 1:>2}. {CANALES[i]}")


def mostrar_cables(cables):
    for i in range(len(cables)):
        cable = cables[i]
        if cable["estado"] == 0:
            print(f" Cable {i + 1}: DISPONIBLE")
        else:
            print(f" Cable {i + 1}: NO DISPONIBLE | {cable['canal']} | desde {cable['inicio']}")
    print(f"\n Disponibles: {contar_cables_libres(cables)} de {len(cables)}")


def elegir_canal():
    print("\nCanales para ver partido:")
    mostrar_canales()
    numero = leer_rango("\nElija el canal (0 = cancelar): ", 0, len(CANALES))
    if numero == 0:
        return None
    return CANALES[numero - 1]


def elegir_cable_libre(cables):
    print("\nEstado de los cables:")
    mostrar_cables(cables)
    while True:
        numero = leer_rango("\nElija un cable DISPONIBLE (0 = cancelar): ", 0, len(cables))
        if numero == 0:
            return -1
        if cables[numero - 1]["estado"] == 0:
            return numero - 1
        print("Ese cable no esta disponible. Elija otro.")


def asignar_cable(datos, cables, sesion):
    mostrar_titulo("Ver partido: asignar cable y canal")
    if contar_cables_libres(cables) == 0:
        print("No hay cables disponibles en este momento.")
        mostrar_cables(cables)
        registrar_bitacora(sesion["usuario"], "Solicitud de cable sin disponibilidad")
        return
    dni = formatear_dni(leer_entero("DNI del usuario: "))
    pos = buscar_posicion(datos["dnis"], dni)
    if pos == -1:
        print("El usuario no esta registrado. Registrelo primero.")
        registrar_bitacora(sesion["usuario"], f"Cable denegado: DNI {dni} no registrado")
        return
    if cable_de_usuario(cables, dni) != -1:
        print("Este usuario ya tiene un cable asignado.")
        registrar_bitacora(sesion["usuario"], f"Cable denegado: DNI {dni} ya tiene uno")
        return
    print(f"\nUsuario: {datos['nombres'][pos]}")
    canal = elegir_canal()
    if canal is None:
        return
    indice = elegir_cable_libre(cables)
    if indice == -1:
        return
    cables[indice] = {"estado": 1, "dni": dni, "canal": canal, "inicio": ahora()}
    guardar_cables(cables)
    registrar_bitacora(sesion["usuario"], f"Cable {indice + 1} asignado a DNI {dni} en {canal}")
    print(f"\nListo: {datos['nombres'][pos]} ve {canal} por el cable {indice + 1}.")


def liberar_cable(cables, sesion):
    mostrar_titulo("Liberar cable")
    mostrar_cables(cables)
    if contar_cables_libres(cables) == len(cables):
        print("\nNo hay cables en uso.")
        return
    numero = leer_rango("\nNumero de cable a liberar (0 = cancelar): ", 0, len(cables))
    if numero == 0:
        return
    cable = cables[numero - 1]
    if cable["estado"] == 0:
        print("Ese cable ya esta disponible.")
        return
    if not confirmar(f"Liberar el cable {numero}"):
        return
    minutos = minutos_transcurridos(cable["inicio"])
    cables[numero - 1] = cable_libre()
    guardar_cables(cables)
    registrar_bitacora(
        sesion["usuario"],
        f"Cable {numero} liberado (DNI {cable['dni']}, {cable['canal']}, {minutos} min)",
    )
    print(f"Cable {numero} liberado. Duracion: {minutos} minutos.")


def mostrar_menu_cables():
    mostrar_titulo("Cables y canales para ver partido")
    print(" 1. Ver cables disponibles y no disponibles")
    print(" 2. Asignar cable y canal a un usuario")
    print(" 3. Liberar un cable")
    print(" 4. Ver canales disponibles")
    print(" 0. Volver")


def gestionar_cables(datos, cables, sesion):
    opcion = -1
    while opcion != 0:
        mostrar_menu_cables()
        opcion = leer_entero("Elija una opcion: ")
        if opcion == 1:
            mostrar_titulo("Estado de los cables")
            mostrar_cables(cables)
        elif opcion == 2:
            asignar_cable(datos, cables, sesion)
        elif opcion == 3:
            liberar_cable(cables, sesion)
        elif opcion == 4:
            mostrar_titulo("Canales para ver partido")
            mostrar_canales()
        elif opcion != 0:
            print("Opcion no valida.")
