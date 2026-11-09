from datetime import datetime, timedelta, timezone

FORMATO_FECHA = "%Y-%m-%d %H:%M:%S"
DIFERENCIA_PERU = timedelta(hours=-5)


def hora_peru():
    return datetime.now(timezone(DIFERENCIA_PERU)).replace(tzinfo=None)


def ahora():
    return hora_peru().strftime(FORMATO_FECHA)


def minutos_transcurridos(inicio):
    desde = datetime.strptime(inicio, FORMATO_FECHA)
    segundos = (hora_peru() - desde).total_seconds()
    return int(segundos // 60)
