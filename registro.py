from utilidades import formatear_dni, generar_codigo, existe_texto, buscar_posicion
from entradas import leer_entero, leer_texto, leer_rango, confirmar
from pantalla import mostrar_titulo
from fechas import ahora
from archivos import guardar_usuarios, guardar_rechazado, guardar_saldos
from log import registrar_bitacora
from consultas import mostrar_usuario
from seguridad import exigir_admin
from equipos import televisor_de_usuario
from apuestas import saldo_de, tiene_apuestas_pendientes

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


def pedir_usuario_existente(datos, mensaje):
    dni = formatear_dni(leer_entero(mensaje))
    pos = buscar_posicion(datos["dnis"], dni)
    if pos == -1:
        print("No existe un usuario con ese DNI.")
        return None, -1
    print()
    mostrar_usuario(datos, pos)
    return dni, pos


def aplicar_cambio(datos, pos, opcion):
    if opcion == 1:
        antes = datos["nombres"][pos]
        datos["nombres"][pos] = leer_texto("Nuevo nombre completo: ")
        return f"nombre de {antes} a {datos['nombres'][pos]}"
    if opcion == 2:
        antes = datos["lugares"][pos]
        datos["lugares"][pos] = leer_texto("Nuevo lugar donde vive: ")
        return f"lugar de {antes} a {datos['lugares'][pos]}"
    nueva = leer_entero("Nueva edad: ")
    if nueva < EDAD_MINIMA or nueva > EDAD_MAXIMA:
        print(f"Edad no valida. Debe estar entre {EDAD_MINIMA} y {EDAD_MAXIMA}.")
        return None
    antes = datos["edades"][pos]
    datos["edades"][pos] = nueva
    return f"edad de {antes} a {nueva}"


def editar_usuario(datos, sesion):
    if not exigir_admin(sesion, "Editar usuario"):
        return
    mostrar_titulo("Editar usuario")
    dni, pos = pedir_usuario_existente(datos, "DNI del usuario a editar: ")
    if dni is None:
        return
    print("\n 1. Cambiar nombre\n 2. Cambiar lugar donde vive\n 3. Cambiar edad")
    opcion = leer_rango("Que desea cambiar (0 = cancelar): ", 0, 3)
    if opcion == 0:
        return
    detalle = aplicar_cambio(datos, pos, opcion)
    if detalle is None:
        registrar_bitacora(sesion["usuario"], f"Edicion cancelada por dato no valido (DNI {dni})")
        return
    guardar_usuarios(datos)
    registrar_bitacora(sesion["usuario"], f"Edito al usuario DNI {dni}: {detalle}")
    print("\nUsuario actualizado:")
    mostrar_usuario(datos, pos)


def motivo_bloqueo(datos, televisores, dni):
    if televisor_de_usuario(televisores, dni) != -1:
        return "tiene un televisor asignado"
    if saldo_de(datos, dni) > 0:
        return "tiene saldo disponible"
    if tiene_apuestas_pendientes(datos, dni):
        return "tiene apuestas pendientes"
    return None


def eliminar_usuario(datos, televisores, sesion):
    if not exigir_admin(sesion, "Eliminar usuario"):
        return
    mostrar_titulo("Eliminar usuario")
    dni, pos = pedir_usuario_existente(datos, "DNI del usuario a eliminar: ")
    if dni is None:
        return
    motivo = motivo_bloqueo(datos, televisores, dni)
    if motivo is not None:
        print(f"\nNo se puede eliminar: el usuario {motivo}.")
        registrar_bitacora(sesion["usuario"], f"Eliminacion bloqueada (DNI {dni}): {motivo}")
        return
    if not confirmar("\nEsta seguro de eliminar a este usuario"):
        return
    nombre = datos["nombres"][pos]
    for clave in ("dnis", "nombres", "lugares", "edades", "codigos", "fechas"):
        datos[clave].pop(pos)
    datos["saldos"].pop(dni, None)
    guardar_usuarios(datos)
    guardar_saldos(datos)
    registrar_bitacora(sesion["usuario"], f"Elimino al usuario {nombre} (DNI {dni})")
    print("Usuario eliminado.")
