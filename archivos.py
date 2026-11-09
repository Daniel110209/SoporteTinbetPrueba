import os
from fechas import ahora

CARPETA = "datos"
ARCHIVO_USUARIOS = os.path.join(CARPETA, "usuarios.txt")
ARCHIVO_RECHAZADOS = os.path.join(CARPETA, "rechazados.txt")
ARCHIVO_ADMINS = os.path.join(CARPETA, "administradores.txt")
ARCHIVO_BITACORA = os.path.join(CARPETA, "bitacora.txt")
ARCHIVO_EQUIPOS = os.path.join(CARPETA, "equipos.txt")
ARCHIVO_TELEVISORES = os.path.join(CARPETA, "televisores.txt")
ARCHIVO_SALDOS = os.path.join(CARPETA, "saldos.txt")
ARCHIVO_APUESTAS = os.path.join(CARPETA, "apuestas.txt")
ARCHIVO_RESULTADOS = os.path.join(CARPETA, "resultados.txt")


def preparar_carpeta():
    if not os.path.exists(CARPETA):
        os.makedirs(CARPETA)


def guardar_usuarios(datos):
    preparar_carpeta()
    with open(ARCHIVO_USUARIOS, "w", encoding="utf-8") as archivo:
        for i in range(len(datos["dnis"])):
            linea = "|".join([
                datos["dnis"][i],
                datos["nombres"][i],
                datos["lugares"][i],
                str(datos["edades"][i]),
                datos["codigos"][i],
                datos["fechas"][i],
            ])
            archivo.write(linea + "\n")


def cargar_usuarios(datos):
    if not os.path.exists(ARCHIVO_USUARIOS):
        return
    with open(ARCHIVO_USUARIOS, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            partes = linea.strip().split("|")
            if len(partes) == 6:
                datos["dnis"].append(partes[0])
                datos["nombres"].append(partes[1])
                datos["lugares"].append(partes[2])
                datos["edades"].append(int(partes[3]))
                datos["codigos"].append(partes[4])
                datos["fechas"].append(partes[5])


def guardar_rechazado(dni, edad):
    preparar_carpeta()
    with open(ARCHIVO_RECHAZADOS, "a", encoding="utf-8") as archivo:
        archivo.write(f"{dni}|{edad}|{ahora()}\n")


def contar_rechazados():
    if not os.path.exists(ARCHIVO_RECHAZADOS):
        return 0
    total = 0
    with open(ARCHIVO_RECHAZADOS, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            if linea.strip() != "":
                total = total + 1
    return total


def guardar_estados(estados):
    preparar_carpeta()
    with open(ARCHIVO_EQUIPOS, "w", encoding="utf-8") as archivo:
        for clave in estados:
            valores = ",".join([str(v) for v in estados[clave]])
            archivo.write(clave + "|" + valores + "\n")


def cargar_estados(estados):
    if not os.path.exists(ARCHIVO_EQUIPOS):
        return
    with open(ARCHIVO_EQUIPOS, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            partes = linea.strip().split("|")
            if len(partes) == 2 and partes[0] in estados:
                valores = [int(v) for v in partes[1].split(",")]
                if len(valores) == len(estados[partes[0]]):
                    estados[partes[0]] = valores


def guardar_televisores(televisores):
    preparar_carpeta()
    with open(ARCHIVO_TELEVISORES, "w", encoding="utf-8") as archivo:
        for tv in televisores:
            linea = "|".join([
                str(tv["estado"]),
                tv["dni"],
                tv["canal"],
                tv["inicio"],
            ])
            archivo.write(linea + "\n")


def cargar_televisores(televisores):
    if not os.path.exists(ARCHIVO_TELEVISORES):
        return
    with open(ARCHIVO_TELEVISORES, "r", encoding="utf-8") as archivo:
        lineas = archivo.read().splitlines()
    for i in range(min(len(lineas), len(televisores))):
        partes = lineas[i].split("|")
        if len(partes) == 4:
            televisores[i] = {
                "estado": int(partes[0]),
                "dni": partes[1],
                "canal": partes[2],
                "inicio": partes[3],
            }


def contar_rechazados_hoy(fecha):
    if not os.path.exists(ARCHIVO_RECHAZADOS):
        return 0
    total = 0
    with open(ARCHIVO_RECHAZADOS, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            partes = linea.strip().split("|")
            if len(partes) == 3 and partes[2].startswith(fecha):
                total = total + 1
    return total


def guardar_saldos(datos):
    preparar_carpeta()
    with open(ARCHIVO_SALDOS, "w", encoding="utf-8") as archivo:
        for dni in datos["saldos"]:
            archivo.write(f"{dni}|{datos['saldos'][dni]:.2f}\n")


def cargar_saldos(datos):
    if not os.path.exists(ARCHIVO_SALDOS):
        return
    with open(ARCHIVO_SALDOS, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            partes = linea.strip().split("|")
            if len(partes) == 2:
                datos["saldos"][partes[0]] = float(partes[1])


def guardar_apuestas(datos):
    preparar_carpeta()
    with open(ARCHIVO_APUESTAS, "w", encoding="utf-8") as archivo:
        for ap in datos["apuestas"]:
            linea = "|".join([
                ap["ticket"],
                ap["dni"],
                str(ap["evento"]),
                ap["pronostico"],
                str(ap["monto"]),
                str(ap["cuota"]),
                ap["estado"],
                ap["fecha"],
            ])
            archivo.write(linea + "\n")


def cargar_apuestas(datos):
    if not os.path.exists(ARCHIVO_APUESTAS):
        return
    with open(ARCHIVO_APUESTAS, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            partes = linea.strip().split("|")
            if len(partes) == 8:
                datos["apuestas"].append({
                    "ticket": partes[0],
                    "dni": partes[1],
                    "evento": int(partes[2]),
                    "pronostico": partes[3],
                    "monto": int(partes[4]),
                    "cuota": float(partes[5]),
                    "estado": partes[6],
                    "fecha": partes[7],
                })


def guardar_resultados(datos):
    preparar_carpeta()
    with open(ARCHIVO_RESULTADOS, "w", encoding="utf-8") as archivo:
        for evento in datos["resultados"]:
            archivo.write(f"{evento}|{datos['resultados'][evento]}\n")


def cargar_resultados(datos):
    if not os.path.exists(ARCHIVO_RESULTADOS):
        return
    with open(ARCHIVO_RESULTADOS, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            partes = linea.strip().split("|")
            if len(partes) == 2:
                datos["resultados"][int(partes[0])] = partes[1]


def guardar_reporte(fecha, lineas):
    preparar_carpeta()
    ruta = os.path.join(CARPETA, f"reporte_{fecha}.txt")
    with open(ruta, "w", encoding="utf-8") as archivo:
        archivo.write("\n".join(lineas) + "\n")
    return ruta
