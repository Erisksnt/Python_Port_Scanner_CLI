import socket

from datetime import datetime
from zoneinfo import ZoneInfo
import email.utils

def convert_gmt_to_brt_auto(date_line: str):
    try:
        text = date_line.replace("Date:", "", 1).strip()

        # parser mais resiliente para headers HTTP
        dt_gmt = email.utils.parsedate_to_datetime(text)

        # força timezone UTC caso não venha explícito
        if dt_gmt.tzinfo is None:
            dt_gmt = dt_gmt.replace(tzinfo=ZoneInfo("UTC"))

        dt_brt = dt_gmt.astimezone(ZoneInfo("America/Sao_Paulo"))

        return f"Date (America/Sao_Paulo): {dt_brt.strftime('%Y-%m-%d %H:%M:%S')}"
    except Exception:
        return date_line


def grab_banner(target: str, port: int, timeout: float = 2.0):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)

    try:
        sock.connect((target, port))

        # Envia requisição leve para serviços que só respondem após input
        try:
            sock.sendall(b"HEAD / HTTP/1.0\r\n\r\n")
        except Exception:
            pass  # se o serviço não esperar dados, ignoramos

        data = sock.recv(1024)
        banner = data.decode(errors="ignore").strip()

        return banner if banner else None

    except Exception:
        return None
    finally:
        sock.close()
