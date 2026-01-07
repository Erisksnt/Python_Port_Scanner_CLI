from .banner_grabber import grab_banner
import socket

COMMON_PORTS = {
    21: "FTP",
    22: "SSH",
    23: "TELNET",
    25: "SMTP",
    80: "HTTP",
    443: "HTTPS",
    8000: "HTTP-ALT",
    3306: "MySQL"
}

def scan_port(target: str, port: int, timeout: float = 0.5):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)

    try:
        result = sock.connect_ex((target, port))
        if result == 0:
            banner = grab_banner(target, port)
            return {
                "port": port,
                "service": COMMON_PORTS.get(port, "UNKNOWN"),
                "status": "open",
                "banner": banner
            }
    finally:
        sock.close()

    return None


def scan_ports(target: str, ports: list[int]):
    results = []
    for port in ports:
        r = scan_port(target, port)
        if r:
            results.append(r)
    return results


def scan_target(target: str):
    # agora é apenas um atalho para COMMON_PORTS
    return scan_ports(target, list(COMMON_PORTS.keys()))
