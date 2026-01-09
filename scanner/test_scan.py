from scanner.port_scan import scan_target

target = "localhost"
results = scan_target(target)

if not results:
    print("Nenhuma porta aberta encontrada.")
else:
    for r in results:
        print(r)
