import socket

COMMON_PORTS = {
    21: "FTP",
    22: "SSH",
    23: "TELNET",
    25: "SMTP",
    80: "HTTP",
    443: "HTTPS",
    3306: "MySQL"
}


def scan_port(target: str, port: int, timeout: float = 1.0):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)

    try:
        result = sock.connect_ex((target, port))
        if result == 0:
            return {
                "port": port,
                "service": COMMON_PORTS.get(port, "UNKNOWN"),
                "status": "open"
            }
    except socket.error:
        pass
    finally:
        sock.close()

    return None


def scan_target(target: str):
    open_ports = []

    for port in COMMON_PORTS:
        result = scan_port(target, port)
        if result:
            open_ports.append(result)

    return open_ports
