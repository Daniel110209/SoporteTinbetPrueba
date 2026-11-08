from utilidades import formatear_dni, buscar_posicion
from entradas import leer_entero
from pantalla import mostrar_titulo
from log import registrar_bitacora

def mostrar_usuario(datos, pos):
    print("DNI:               ", datos["dnis"][pos])
    print("Nombre completo:   ", datos["nombres"][pos])
    print("Lugar de vivienda: ", datos["lugares"][pos])
    print("Edad:              ", datos["edades"][pos])
    print("Codigo (12 num):   ", datos["codigos"][pos])
    print("Registrado el:     ", datos["fechas"][pos])


def listar_usuarios(datos, sesion):
    mostrar_titulo("Usuarios registrados")
    total = len(datos["dnis"])
    if total == 0:
        print("Aun no hay usuarios registrados.")
        return
    print(f"{'N':<4}{'DNI':<10}{'NOMBRE':<26}{'EDAD':<6}{'CODIGO'}")
    print("-" * 60)
    for i in range(total):
        nombre = datos["nombres"][i][:24]
        print(f"{i + 1:<4}{datos['dnis'][i]:<10}{nombre:<26}{datos['edades'][i]:<6}{datos['codigos'][i]}")
    print("-" * 60)
    print(f"Total: {total} usuarios")
    registrar_bitacora(sesion["usuario"], "Listo los usuarios registrados")


def buscar_usuario(datos, sesion):
    mostrar_titulo("Buscar usuario por DNI")
    dni = formatear_dni(leer_entero("Ingrese el DNI a buscar: "))
    pos = buscar_posicion(datos["dnis"], dni)
    if pos == -1:
        print("No existe un usuario con ese DNI.")
        registrar_bitacora(sesion["usuario"], f"Busqueda sin resultado (DNI {dni})")
        return
    print("\nUsuario encontrado:")
    mostrar_usuario(datos, pos)
    registrar_bitacora(sesion["usuario"], f"Busqueda de usuario (DNI {dni})")
