import argparse
import csv
import json
import socket
from datetime import datetime
from scanner.banner_grabber import grab_banner

def scan_port(host, port, timeout=0.5):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)

    try:
        result = sock.connect_ex((host, port))

        try:
            service = socket.getservbyport(port, "tcp")
        except OSError:
            service = "unknown"

        if result == 0:
            if result == 0:
                banner = grab_banner(host, port)
                status = "open"
            else:
                banner = ""
                status = "closed"

            return {
                "port": port,
                "service": service,
                "status": status,
                "banner": banner
            }

        else:
            return {
                "port": port,
                "service": service,
                "status": "closed",
                "banner": ""
            }

    finally:
        sock.close()

def export_results(results):
    print("\nDeseja salvar os resultados?")
    print("[1] JSON")
    print("[2] CSV")
    print("[3] CSV e JSON")
    print("[0] Não salvar")
    choice = input("Escolha uma opção: ").strip()

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    if choice == "1":
        filename = f"scan_{ts}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"✔ Resultado salvo em {filename}")

    elif choice == "2":
        filename = f"scan_{ts}.csv"
        with open(filename, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=["port","service","status","banner"])
            w.writeheader()
            for r in results:
                w.writerow(r)
        print(f"✔ Resultado salvo em {filename}")

    elif choice == "3":
        filename = f"scan_{ts}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
            
        print(f"✔ Resultado salvo em {filename}")

        filename = f"scan_{ts}.csv"
        with open(filename, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=["port","service","status","banner"])
            w.writeheader()
            for r in results:
                w.writerow(r)
        print(f"✔ Resultado salvo em {filename}")

    else:
        print("⏭ Resultados não foram salvos.")

def main():
    parser = argparse.ArgumentParser(description="Simple Port Scanner CLI")
    parser.add_argument("host", help="Host alvo")
    parser.add_argument("-p", "--ports", default="80,443,8000",
                        help="Lista de portas (ex: 80,443,8000)")
    args = parser.parse_args()

    host = args.host
    ports = [int(p.strip()) for p in args.ports.split(",")]

    print(f"\n🔎 Scaneando {host}...🔎\n")
    results = []

    for port in ports:
        r = scan_port(host, port)
        results.append(r)
        print(f"{r['port']},{r['service']},{r['status']}")

    export_results(results)

if __name__ == "__main__":
    main()
