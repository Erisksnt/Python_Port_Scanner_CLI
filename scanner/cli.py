import argparse
from scanner.port_scanner import scan_target, scan_port

def main():
    parser = argparse.ArgumentParser(description="Port Scanner CLI")
    parser.add_argument("--host", required=True, help="Host/IP de destino")
    parser.add_argument("--port", type=int, help="Escanear apenas uma porta")

    args = parser.parse_args()

    if args.port:
        result = scan_port(args.host, args.port)
        print(result if result else f"Porta {args.port} fechada.")
    else:
        results = scan_target(args.host)
        if not results:
            print("Nenhuma porta aberta encontrada.")
        else:
            for r in results:
                print(r)

if __name__ == "__main__":
    main()
