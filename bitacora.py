from entradas import leer_entero, leer_texto
from pantalla import mostrar_titulo
from fechas import ahora
from archivos import contar_rechazados_hoy, guardar_reporte
from log import leer_bitacora, registrar_bitacora
from seguridad import exigir_admin
from equipos import contar_libres
from canales import CANALES

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


def lineas_de_hoy(lineas, fecha):
    hoy = []
    for linea in lineas:
        if linea.startswith(fecha):
            hoy.append(linea)
    return hoy


def contar_con_texto(lineas, texto):
    total = 0
    for linea in lineas:
        if texto in linea:
            total = total + 1
    return total


def canal_mas_pedido(lineas):
    asignaciones = buscar_en_bitacora(lineas, "asignado a DNI")
    mejor = "Ninguno"
    mejor_total = 0
    for canal in CANALES:
        total = contar_con_texto(asignaciones, " en " + canal)
        if total > mejor_total:
            mejor = canal
            mejor_total = total
    return mejor, mejor_total


def apuestas_de_hoy(datos, fecha):
    cantidad = 0
    monto = 0
    for ap in datos["apuestas"]:
        if ap["fecha"].startswith(fecha):
            cantidad = cantidad + 1
            monto = monto + ap["monto"]
    return cantidad, monto


def registrados_hoy(datos, fecha):
    total = 0
    for registro in datos["fechas"]:
        if registro.startswith(fecha):
            total = total + 1
    return total


def construir_reporte(datos, televisores, lineas, fecha, sesion):
    canal, veces = canal_mas_pedido(lineas)
    cantidad, monto = apuestas_de_hoy(datos, fecha)
    ocupados = len(televisores) - contar_libres(televisores)
    return [
        "REPORTE DIARIO - TINBET (KING TECH CORPORATION S.A.C.)",
        "=" * 54,
        f"Fecha: {fecha}",
        f"Generado por: {sesion['usuario']} a las {ahora()[11:]}",
        "",
        "USUARIOS",
        f"  Registrados hoy:           {registrados_hoy(datos, fecha)}",
        f"  Menores rechazados hoy:    {contar_rechazados_hoy(fecha)}",
        f"  Total de usuarios:         {len(datos['dnis'])}",
        "",
        "TELEVISORES",
        f"  Ocupados ahora:            {ocupados} de {len(televisores)}",
        f"  Canal mas pedido hoy:      {canal} ({veces} pedidos)",
        "",
        "APUESTAS",
        f"  Apuestas hoy:              {cantidad}",
        f"  Monto apostado hoy:        S/ {monto:.2f}",
        "",
        "SEGURIDAD",
        f"  Intentos de sesion fallidos: {contar_con_texto(lineas, 'Intento de sesion fallido')}",
        f"  Accesos denegados:           {contar_con_texto(lineas, 'Acceso denegado')}",
        f"  Movimientos totales hoy:     {len(lineas)}",
    ]


def generar_reporte(datos, televisores, sesion):
    fecha = ahora()[:10]
    lineas = lineas_de_hoy(leer_bitacora(), fecha)
    contenido = construir_reporte(datos, televisores, lineas, fecha, sesion)
    ruta = guardar_reporte(fecha, contenido)
    registrar_bitacora(sesion["usuario"], "Genero el reporte diario " + ruta)
    print()
    mostrar_lineas(contenido)
    print(f"\nReporte guardado en: {ruta}")


def mostrar_menu_bitacora():
    mostrar_titulo("Bitacora y reportes (solo administradores)")
    print(" 1. Ver los ultimos movimientos")
    print(" 2. Buscar movimientos por palabra")
    print(" 3. Ver el total de movimientos")
    print(" 4. Generar reporte diario (.txt)")
    print(" 0. Volver")


def ver_bitacora(datos, televisores, sesion):
    if not exigir_admin(sesion, "Ver la bitacora y los reportes"):
        return
    registrar_bitacora(sesion["usuario"], "Ingreso a bitacora y reportes")
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
        elif opcion == 4:
            generar_reporte(datos, televisores, sesion)
        elif opcion != 0:
            print("Opcion no valida.")
