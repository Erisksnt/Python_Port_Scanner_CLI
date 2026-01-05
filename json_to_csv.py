import json
import csv
from pathlib import Path

json_file = Path("scan_result.json")
csv_file = Path("scan_result.csv")

data = json.loads(json_file.read_text(encoding="utf-8"))

# pega a lista correta
results = data.get("results", [])

if not results:
    print("Nenhum resultado para converter (results está vazio).")
    raise SystemExit()

with open(csv_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)

print("CSV gerado em:", csv_file)
