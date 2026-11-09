from utilidades import formatear_dni, buscar_posicion
from entradas import leer_entero, leer_rango, confirmar
from fechas import ahora, minutos_transcurridos
from pantalla import mostrar_titulo
from archivos import guardar_televisores
from log import registrar_bitacora
from canales import elegir_canal, mostrar_canales


def televisor_libre():
    return {"estado": 0, "dni": "", "canal": "", "inicio": ""}


def contar_libres(televisores):
    libres = 0
    for tv in televisores:
        if tv["estado"] == 0:
            libres = libres + 1
    return libres


def televisor_de_usuario(televisores, dni):
    for i in range(len(televisores)):
        if televisores[i]["estado"] == 1 and televisores[i]["dni"] == dni:
            return i
    return -1


def mostrar_televisores(televisores):
    for i in range(len(televisores)):
        tv = televisores[i]
        if tv["estado"] == 0:
            print(f" Televisor {i + 1}: DISPONIBLE")
        else:
            print(f" Televisor {i + 1}: OCUPADO | {tv['canal']} | desde {tv['inicio']}")
    print(f"\n Disponibles: {contar_libres(televisores)} de {len(televisores)}")


def elegir_televisor_libre(televisores):
    print("\nEstado de los televisores:")
    mostrar_televisores(televisores)
    while True:
        numero = leer_rango("\nElija un televisor DISPONIBLE (0 = cancelar): ", 0, len(televisores))
        if numero == 0:
            return -1
        if televisores[numero - 1]["estado"] == 0:
            return numero - 1
        print("Ese televisor esta ocupado. Elija otro.")


def asignar_televisor(datos, televisores, sesion):
    mostrar_titulo("Ver partido: elegir televisor y canal")
    if contar_libres(televisores) == 0:
        print("No hay televisores disponibles en este momento.")
        mostrar_televisores(televisores)
        registrar_bitacora(sesion["usuario"], "Solicitud de televisor sin disponibilidad")
        return
    indice = elegir_televisor_libre(televisores)
    if indice == -1:
        return
    canal = elegir_canal()
    if canal is None:
        return
    dni = formatear_dni(leer_entero("DNI del usuario que va a ver el partido: "))
    pos = buscar_posicion(datos["dnis"], dni)
    if pos == -1:
        print("El usuario no esta registrado. Registrelo primero.")
        registrar_bitacora(sesion["usuario"], f"Televisor denegado: DNI {dni} no registrado")
        return
    if televisor_de_usuario(televisores, dni) != -1:
        print("Este usuario ya tiene un televisor asignado.")
        registrar_bitacora(sesion["usuario"], f"Televisor denegado: DNI {dni} ya tiene uno")
        return
    televisores[indice] = {"estado": 1, "dni": dni, "canal": canal, "inicio": ahora()}
    guardar_televisores(televisores)
    registrar_bitacora(sesion["usuario"], f"Televisor {indice + 1} asignado a DNI {dni} en {canal}")
    print(f"\nListo: {datos['nombres'][pos]} ve {canal} en el televisor {indice + 1}.")


def liberar_televisor(televisores, sesion):
    mostrar_titulo("Liberar televisor")
    mostrar_televisores(televisores)
    if contar_libres(televisores) == len(televisores):
        print("\nNo hay televisores ocupados.")
        return
    numero = leer_rango("\nNumero de televisor a liberar (0 = cancelar): ", 0, len(televisores))
    if numero == 0:
        return
    tv = televisores[numero - 1]
    if tv["estado"] == 0:
        print("Ese televisor ya esta disponible.")
        return
    if not confirmar(f"Liberar el televisor {numero}"):
        return
    minutos = minutos_transcurridos(tv["inicio"])
    televisores[numero - 1] = televisor_libre()
    guardar_televisores(televisores)
    registrar_bitacora(
        sesion["usuario"],
        f"Televisor {numero} liberado (DNI {tv['dni']}, {tv['canal']}, {minutos} min)",
    )
    print(f"Televisor {numero} liberado. Duracion: {minutos} minutos.")


def mostrar_menu_televisores():
    mostrar_titulo("Televisores y canales para ver partido")
    print(" 1. Ver televisores disponibles y ocupados")
    print(" 2. Elegir televisor y canal para un usuario")
    print(" 3. Liberar un televisor")
    print(" 4. Ver canales disponibles")
    print(" 0. Volver")


def gestionar_televisores(datos, televisores, sesion):
    opcion = -1
    while opcion != 0:
        mostrar_menu_televisores()
        opcion = leer_entero("Elija una opcion: ")
        if opcion == 1:
            mostrar_titulo("Estado de los televisores")
            mostrar_televisores(televisores)
        elif opcion == 2:
            asignar_televisor(datos, televisores, sesion)
        elif opcion == 3:
            liberar_televisor(televisores, sesion)
        elif opcion == 4:
            mostrar_titulo("Canales para ver partido")
            mostrar_canales()
        elif opcion != 0:
            print("Opcion no valida.")
