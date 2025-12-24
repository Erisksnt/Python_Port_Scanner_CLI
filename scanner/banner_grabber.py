import socket


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
