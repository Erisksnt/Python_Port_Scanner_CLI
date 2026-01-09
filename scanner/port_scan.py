import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
from .banner_grabber import grab_banner

COMMON_PORTS = {
    21: "FTP",
    22: "SSH",
    23: "TELNET",
    25: "SMTP",
    80: "HTTP",
    443: "HTTPS",
    8000: "HTTP-ALT",
    3306: "MySQL",
}


def scan_port(target: str, port: int, timeout: float = 0.5):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)

    try:
        if sock.connect_ex((target, port)) == 0:
            banner = grab_banner(target, port)
            return {
                "port": port,
                "service": COMMON_PORTS.get(port, "UNKNOWN"),
                "status": "open",
                "banner": banner
            }
    except Exception:
        pass
    finally:
        sock.close()

    return None


def scan_ports(
    target: str,
    ports: list[int],
    timeout: float = 0.5,
    threads: int = 100
):
    results = []

    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {
            executor.submit(scan_port, target, port, timeout): port
            for port in ports
        }

        for future in as_completed(futures):
            result = future.result()
            if result:
                results.append(result)

    return sorted(results, key=lambda x: x["port"]) # Get order the doors