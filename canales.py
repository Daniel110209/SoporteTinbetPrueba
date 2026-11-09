from entradas import leer_rango

CANALES = [
    "HBO Max",
    "Disney+",
    "DirecTV GO",
    "ESPN",
    "Fox Sports",
    "Movistar Deportes",
    "Liga 1 MAX",
    "GOLPERU",
    "Win Sports",
    "Prime Video",
]


def mostrar_canales():
    for i in range(len(CANALES)):
        print(f" {i + 1:>2}. {CANALES[i]}")


def elegir_canal():
    print("\nCanales para ver partido:")
    mostrar_canales()
    numero = leer_rango("\nElija el canal (0 = cancelar): ", 0, len(CANALES))
    if numero == 0:
        return None
    return CANALES[numero - 1]
