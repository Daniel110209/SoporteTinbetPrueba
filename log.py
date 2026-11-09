import os
from archivos import ARCHIVO_BITACORA, preparar_carpeta
from fechas import ahora


def registrar_bitacora(usuario, accion):
    preparar_carpeta()
    with open(ARCHIVO_BITACORA, "a", encoding="utf-8") as archivo:
        archivo.write(f"{ahora()} | {usuario} | {accion}\n")


def leer_bitacora():
    if not os.path.exists(ARCHIVO_BITACORA):
        return []
    with open(ARCHIVO_BITACORA, "r", encoding="utf-8") as archivo:
        return archivo.read().splitlines()
