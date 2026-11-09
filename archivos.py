import os
from rutas import (
    ARCHIVO_USUARIOS,
    ARCHIVO_RECHAZADOS,
    ARCHIVO_EQUIPOS,
    ARCHIVO_TELEVISORES,
    preparar_carpeta,
)
from fechas import ahora


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
