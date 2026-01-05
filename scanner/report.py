import json


def export_json(results, filename="scan_result.json"):
    data = {
        "results": results
    }

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    return filename
