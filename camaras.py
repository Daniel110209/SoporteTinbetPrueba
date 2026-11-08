from entradas import leer_entero
from pantalla import mostrar_titulo
from archivos import guardar_estados
from log import registrar_bitacora
from seguridad import exigir_admin

NOMBRES = ["Entrada principal", "Sala de apuestas", "Caja y atencion"]


def texto_estado(valor):
    if valor == 1:
        return "ACTIVA (grabando)"
    return "APAGADA"


def contar_activas(estados):
    activas = 0
    for valor in estados["cam"]:
        if valor == 1:
            activas = activas + 1
    return activas


def mostrar_camaras(estados):
    for i in range(len(estados["cam"])):
        print(f" {i + 1}. Camara {NOMBRES[i]:<20} {texto_estado(estados['cam'][i])}")
    print(f"\n Activas: {contar_activas(estados)} de {len(estados['cam'])}")


def cambiar_camara(estados, num, sesion):
    estados["cam"][num - 1] = 1 - estados["cam"][num - 1]
    guardar_estados(estados)
    nuevo = texto_estado(estados["cam"][num - 1])
    registrar_bitacora(sesion["usuario"], f"Camara {NOMBRES[num - 1]} cambio a {nuevo}")
    print("Estado actualizado.")


def gestionar_camaras(estados, sesion):
    if not exigir_admin(sesion, "Ver camaras de seguridad"):
        return
    registrar_bitacora(sesion["usuario"], "Ingreso al panel de camaras")
    while True:
        mostrar_titulo("Camaras de seguridad (solo administradores)")
        mostrar_camaras(estados)
        num = leer_entero("\nNumero de camara para encender o apagar (0 = volver): ")
        if num == 0:
            return
        if 1 <= num <= len(estados["cam"]):
            cambiar_camara(estados, num, sesion)
        else:
            print("Numero fuera de rango.")
