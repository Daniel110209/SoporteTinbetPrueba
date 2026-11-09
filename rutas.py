import os

CARPETA = "datos"
ARCHIVO_USUARIOS = os.path.join(CARPETA, "usuarios.txt")
ARCHIVO_RECHAZADOS = os.path.join(CARPETA, "rechazados.txt")
ARCHIVO_ADMINS = os.path.join(CARPETA, "administradores.txt")
ARCHIVO_BITACORA = os.path.join(CARPETA, "bitacora.txt")
ARCHIVO_EQUIPOS = os.path.join(CARPETA, "equipos.txt")
ARCHIVO_TELEVISORES = os.path.join(CARPETA, "televisores.txt")


def preparar_carpeta():
    if not os.path.exists(CARPETA):
        os.makedirs(CARPETA)
