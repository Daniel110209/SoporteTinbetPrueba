import hashlib
import os
from archivos import ARCHIVO_ADMINS, preparar_carpeta
from log import registrar_bitacora
from entradas import leer_texto
from pantalla import mostrar_titulo

MAX_INTENTOS = 3
USUARIO_INICIAL = "admin"
CLAVE_INICIAL = "tinbet2026"
LARGO_MINIMO_CLAVE = 6


def cifrar(clave):
    return hashlib.sha256(clave.encode("utf-8")).hexdigest()


def cargar_admins():
    admins = {}
    if os.path.exists(ARCHIVO_ADMINS):
        with open(ARCHIVO_ADMINS, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                partes = linea.strip().split("|")
                if len(partes) == 2:
                    admins[partes[0]] = partes[1]
    return admins


def guardar_admins(admins):
    preparar_carpeta()
    with open(ARCHIVO_ADMINS, "w", encoding="utf-8") as archivo:
        for usuario in admins:
            archivo.write(usuario + "|" + admins[usuario] + "\n")


def crear_admin_inicial():
    admins = cargar_admins()
    if len(admins) == 0:
        admins[USUARIO_INICIAL] = cifrar(CLAVE_INICIAL)
        guardar_admins(admins)
        registrar_bitacora("SISTEMA", "Se creo el administrador inicial")


def iniciar_sesion():
    admins = cargar_admins()
    mostrar_titulo("Inicio de sesion - administrador")
    for intento in range(1, MAX_INTENTOS + 1):
        usuario = input("Usuario: ").strip()
        clave = input("Clave: ").strip()
        if usuario in admins and admins[usuario] == cifrar(clave):
            registrar_bitacora(usuario, "Inicio de sesion como administrador")
            print(f"\nBienvenido, {usuario}.")
            return {"usuario": usuario, "rol": "ADMIN"}
        nombre = usuario if usuario != "" else "desconocido"
        registrar_bitacora(nombre, "Intento de sesion fallido")
        print(f"Credenciales incorrectas. Intento {intento} de {MAX_INTENTOS}.")
    registrar_bitacora("SISTEMA", "Acceso de administrador bloqueado por intentos fallidos")
    print("Demasiados intentos fallidos. Volviendo al inicio.")
    return None


def crear_sesion_operador():
    registrar_bitacora("operador", "Ingreso como operador")
    return {"usuario": "operador", "rol": "OPERADOR"}


def es_admin(sesion):
    return sesion["rol"] == "ADMIN"


def exigir_admin(sesion, accion):
    if es_admin(sesion):
        return True
    registrar_bitacora(sesion["usuario"], "Acceso denegado: " + accion)
    print("\nACCESO DENEGADO: esta opcion es solo para administradores.")
    return False


def crear_admin(sesion):
    if not exigir_admin(sesion, "Crear administrador"):
        return
    mostrar_titulo("Nuevo administrador")
    admins = cargar_admins()
    usuario = leer_texto("Nuevo usuario: ")
    if usuario in admins:
        print("Ese usuario ya existe.")
        return
    clave = input(f"Clave (minimo {LARGO_MINIMO_CLAVE} caracteres): ").strip()
    if len(clave) < LARGO_MINIMO_CLAVE:
        print("La clave es demasiado corta. No se creo el administrador.")
        return
    admins[usuario] = cifrar(clave)
    guardar_admins(admins)
    registrar_bitacora(sesion["usuario"], "Creo al administrador " + usuario)
    print("Administrador creado correctamente.")
