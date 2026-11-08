from entradas import leer_entero, leer_texto
from pantalla import mostrar_titulo
from log import leer_bitacora, registrar_bitacora
from seguridad import exigir_admin

ULTIMOS = 15


def mostrar_lineas(lineas):
    if len(lineas) == 0:
        print("No hay movimientos para mostrar.")
        return
    for linea in lineas:
        print(" " + linea)


def buscar_en_bitacora(lineas, palabra):
    encontradas = []
    for linea in lineas:
        if palabra.lower() in linea.lower():
            encontradas.append(linea)
    return encontradas


def mostrar_menu_bitacora():
    mostrar_titulo("Bitacora del sistema (solo administradores)")
    print(" 1. Ver los ultimos movimientos")
    print(" 2. Buscar movimientos por palabra")
    print(" 3. Ver el total de movimientos")
    print(" 0. Volver")


def ver_bitacora(sesion):
    if not exigir_admin(sesion, "Ver la bitacora"):
        return
    registrar_bitacora(sesion["usuario"], "Consulto la bitacora")
    opcion = -1
    while opcion != 0:
        mostrar_menu_bitacora()
        opcion = leer_entero("Elija una opcion: ")
        lineas = leer_bitacora()
        if opcion == 1:
            print()
            mostrar_lineas(lineas[-ULTIMOS:])
        elif opcion == 2:
            palabra = leer_texto("Palabra a buscar: ")
            print()
            mostrar_lineas(buscar_en_bitacora(lineas, palabra))
        elif opcion == 3:
            print(f"\nTotal de movimientos registrados: {len(lineas)}")
        elif opcion != 0:
            print("Opcion no valida.")
