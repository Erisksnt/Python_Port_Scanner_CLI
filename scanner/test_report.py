from scanner.port_scan import scan_target
from scanner.report import export_json

target = "localhost"
results = scan_target(target)

file = export_json(results)

print("Arquivo gerado:", file)
