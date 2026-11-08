import random


def formatear_dni(numero):
    texto = str(numero)
    while len(texto) < 8:
        texto = "0" + texto
    return texto


def generar_codigo(largo):
    codigo = ""
    for _ in range(largo):
        codigo = codigo + str(random.randint(0, 9))
    return codigo


def existe_texto(lista, valor):
    for elemento in lista:
        if elemento == valor:
            return True
    return False


def buscar_posicion(lista, valor):
    for i in range(len(lista)):
        if lista[i] == valor:
            return i
    return -1
