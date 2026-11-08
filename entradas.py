def leer_entero(mensaje):
    while True:
        texto = input(mensaje).strip()
        if texto.lstrip("-").isdigit():
            return int(texto)
        print("Entrada no valida. Escriba solo numeros.")


def leer_texto(mensaje):
    while True:
        texto = input(mensaje).strip()
        if len(texto) > 0 and "|" not in texto:
            return texto
        print("Dato no valido. No puede estar vacio ni contener el simbolo |")


def leer_rango(mensaje, minimo, maximo):
    while True:
        numero = leer_entero(mensaje)
        if minimo <= numero <= maximo:
            return numero
        print(f"Elija un numero entre {minimo} y {maximo}.")


def confirmar(mensaje):
    respuesta = input(mensaje + " (s/n): ").strip().lower()
    return respuesta == "s"
