from datetime import datetime

FORMATO_FECHA = "%Y-%m-%d %H:%M:%S"


def ahora():
    return datetime.now().strftime(FORMATO_FECHA)


def minutos_transcurridos(inicio):
    desde = datetime.strptime(inicio, FORMATO_FECHA)
    segundos = (datetime.now() - desde).total_seconds()
    return int(segundos // 60)
