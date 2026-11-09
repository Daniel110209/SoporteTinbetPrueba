from entradas import leer_entero
from pantalla import mostrar_titulo
from archivos import cargar_usuarios, cargar_estados, cargar_televisores, contar_rechazados
from log import registrar_bitacora
from seguridad import (
    crear_admin_inicial,
    iniciar_sesion,
    crear_sesion_operador,
    crear_admin,
    es_admin,
)
from registro import registrar_usuario
from consultas import listar_usuarios, buscar_usuario
from equipos import gestionar_televisores, contar_libres, televisor_libre
from camaras import gestionar_camaras, contar_activas
from canales import CANALES
from bitacora import ver_bitacora

TOTAL_TELEVISORES = 9
TOTAL_CAMARAS = 3


def crear_datos():
    return {
        "dnis": [],
        "nombres": [],
        "lugares": [],
        "edades": [],
        "codigos": [],
        "fechas": [],
        "rechazados": 0,
    }


def crear_estados():
    return {"cam": [1] * TOTAL_CAMARAS}


def crear_televisores():
    televisores = []
    for _ in range(TOTAL_TELEVISORES):
        televisores.append(televisor_libre())
    return televisores


def mostrar_menu_inicio():
    mostrar_titulo("Sistema Tinbet - King Tech Corporation")
    print(" 1. Ingresar como administrador")
    print(" 2. Ingresar como operador")
    print(" 0. Salir del programa")


def describir_sesion(sesion):
    if es_admin(sesion):
        return "Administrador (" + sesion["usuario"] + ")"
    return "Operador"


def mostrar_menu(sesion):
    mostrar_titulo("Menu principal - " + describir_sesion(sesion))
    print(" 1. Registrar usuario")
    print(" 2. Listar usuarios registrados")
    print(" 3. Buscar usuario por DNI")
    print(f" 4. Televisores y canales para ver partido ({TOTAL_TELEVISORES})")
    print(" 5. Camaras de seguridad            [solo administrador]")
    print(" 6. Bitacora del sistema            [solo administrador]")
    print(" 7. Resumen general")
    print(" 8. Crear nuevo administrador       [solo administrador]")
    print(" 0. Cerrar sesion")


def mostrar_resumen(datos, estados, televisores, sesion):
    mostrar_titulo("Resumen general")
    print(f" Usuarios registrados (aceptados):     {len(datos['dnis'])}")
    print(f" Usuarios rechazados por ser menores:  {datos['rechazados']}")
    print(f" Televisores disponibles:              {contar_libres(televisores)} de {len(televisores)}")
    print(f" Canales para ver partido:             {len(CANALES)}")
    if es_admin(sesion):
        print(f" Camaras activas:                      {contar_activas(estados)} de {len(estados['cam'])}")
    registrar_bitacora(sesion["usuario"], "Consulto el resumen general")


def ejecutar_sesion(datos, estados, televisores, sesion):
    opcion = -1
    while opcion != 0:
        mostrar_menu(sesion)
        opcion = leer_entero("Elija una opcion: ")
        if opcion == 1:
            registrar_usuario(datos, sesion)
        elif opcion == 2:
            listar_usuarios(datos, sesion)
        elif opcion == 3:
            buscar_usuario(datos, sesion)
        elif opcion == 4:
            gestionar_televisores(datos, televisores, sesion)
        elif opcion == 5:
            gestionar_camaras(estados, sesion)
        elif opcion == 6:
            ver_bitacora(sesion)
        elif opcion == 7:
            mostrar_resumen(datos, estados, televisores, sesion)
        elif opcion == 8:
            crear_admin(sesion)
        elif opcion == 0:
            registrar_bitacora(sesion["usuario"], "Cierre de sesion")
            print("\nSesion cerrada.")
        else:
            print("\nOpcion no valida. Intente de nuevo.")


def main():
    crear_admin_inicial()
    datos = crear_datos()
    estados = crear_estados()
    televisores = crear_televisores()
    cargar_usuarios(datos)
    datos["rechazados"] = contar_rechazados()
    cargar_estados(estados)
    cargar_televisores(televisores)
    registrar_bitacora("SISTEMA", "Programa iniciado")
    opcion = -1
    while opcion != 0:
        mostrar_menu_inicio()
        opcion = leer_entero("Elija una opcion: ")
        if opcion == 1:
            sesion = iniciar_sesion()
            if sesion is not None:
                ejecutar_sesion(datos, estados, televisores, sesion)
        elif opcion == 2:
            ejecutar_sesion(datos, estados, televisores, crear_sesion_operador())
        elif opcion == 0:
            print("\nCerrando el sistema. Hasta pronto.")
        else:
            print("\nOpcion no valida. Intente de nuevo.")
    registrar_bitacora("SISTEMA", "Programa cerrado")


if __name__ == "__main__":
    main()
