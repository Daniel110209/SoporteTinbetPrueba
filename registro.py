from utilidades import formatear_dni, generar_codigo, existe_texto
from entradas import leer_entero, leer_texto
from pantalla import mostrar_titulo
from fechas import ahora
from archivos import guardar_usuarios, guardar_rechazado
from log import registrar_bitacora
from consultas import mostrar_usuario

EDAD_MINIMA = 18
EDAD_MAXIMA = 120
LARGO_CODIGO = 12


def pedir_dni(datos):
    dni_num = leer_entero("Ingrese el DNI (8 digitos): ")
    if dni_num < 1 or dni_num > 99999999:
        print("DNI no valido. Debe tener 8 digitos.")
        return None
    dni = formatear_dni(dni_num)
    if existe_texto(datos["dnis"], dni):
        print("Ese DNI ya esta registrado.")
        return None
    return dni


def codigo_unico(datos):
    codigo = generar_codigo(LARGO_CODIGO)
    while existe_texto(datos["codigos"], codigo):
        codigo = generar_codigo(LARGO_CODIGO)
    return codigo


def rechazar_menor(datos, dni, edad, sesion):
    datos["rechazados"] = datos["rechazados"] + 1
    guardar_rechazado(dni, edad)
    print("\nREGISTRO RECHAZADO: el usuario es menor de edad.")
    print(f"No cumple con el requisito de edad minima ({EDAD_MINIMA} anios).")
    registrar_bitacora(sesion["usuario"], f"Usuario RECHAZADO por ser menor de edad (DNI {dni}, edad {edad})")


def guardar_usuario(datos, dni, nombre, lugar, edad, codigo):
    datos["dnis"].append(dni)
    datos["nombres"].append(nombre)
    datos["lugares"].append(lugar)
    datos["edades"].append(edad)
    datos["codigos"].append(codigo)
    datos["fechas"].append(ahora())
    guardar_usuarios(datos)


def registrar_usuario(datos, sesion):
    mostrar_titulo("Registro de usuario")
    dni = pedir_dni(datos)
    if dni is None:
        registrar_bitacora(sesion["usuario"], "Registro cancelado: DNI invalido o repetido")
        return
    edad = leer_entero("Ingrese la edad: ")
    if edad < 0 or edad > EDAD_MAXIMA:
        print("Edad no valida.")
        registrar_bitacora(sesion["usuario"], f"Registro cancelado: edad no valida (DNI {dni})")
        return
    if edad < EDAD_MINIMA:
        rechazar_menor(datos, dni, edad, sesion)
        return
    nombre = leer_texto("Ingrese el nombre completo: ")
    lugar = leer_texto("Ingrese el lugar donde vive: ")
    codigo = codigo_unico(datos)
    guardar_usuario(datos, dni, nombre, lugar, edad, codigo)
    registrar_bitacora(sesion["usuario"], f"Usuario REGISTRADO: {nombre} (DNI {dni}, codigo {codigo})")
    print("\nUSUARIO ACEPTADO Y REGISTRADO")
    mostrar_usuario(datos, len(datos["dnis"]) - 1)
