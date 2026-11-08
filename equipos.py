from entradas import leer_entero
from pantalla import mostrar_titulo
from archivos import guardar_estados
from log import registrar_bitacora

def contar_disponibles(estado):
    disponibles = 0
    for valor in estado:
        if valor == 0:
            disponibles = disponibles + 1
    return disponibles


def mostrar_equipos(nombre, estado, texto_ocupado):
    for i in range(len(estado)):
        if estado[i] == 0:
            situacion = "DISPONIBLE"
        else:
            situacion = texto_ocupado
        print(f" {i + 1:>2}. {nombre} {i + 1:<3} {situacion}")
    print(f"\n Disponibles: {contar_disponibles(estado)} de {len(estado)}")


def gestionar_equipo(nombre, plural, clave, estados, sesion, texto_ocupado="EN USO"):
    estado = estados[clave]
    while True:
        mostrar_titulo("Control de " + plural)
        mostrar_equipos(nombre, estado, texto_ocupado)
        num = leer_entero("\nNumero para cambiar su estado (0 = volver): ")
        if num == 0:
            return
        if 1 <= num <= len(estado):
            estado[num - 1] = 1 - estado[num - 1]
            guardar_estados(estados)
            if estado[num - 1] == 0:
                nuevo = "DISPONIBLE"
            else:
                nuevo = texto_ocupado
            registrar_bitacora(sesion["usuario"], f"{nombre} {num} ahora {nuevo}")
            print("Estado actualizado.")
        else:
            print("Numero fuera de rango.")
