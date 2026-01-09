import socket
import email.utils
from datetime import datetime
from zoneinfo import ZoneInfo

def get_brasilia_timestamp():
   
    return datetime.now(ZoneInfo("America/Sao_Paulo"))

def convert_gmt_to_brt_auto(date_line: str):
    try:
        text = date_line.replace("Date:", "", 1).strip()

        dt_gmt = email.utils.parsedate_to_datetime(text)

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

        try:
            sock.sendall(b"HEAD / HTTP/1.0\r\n\r\n")
        except Exception:
            pass  

        data = sock.recv(1024)
        banner = data.decode(errors="ignore").strip()

        return banner if banner else None

    except Exception:
        return None
    finally:
        sock.close()
