import csv
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
EXPORT_DIR = os.path.join(ROOT, "export")

def write_nodes(nodes):
    path = os.path.join(EXPORT_DIR, "nodes.csv")
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=nodes[0].keys())
        writer.writeheader()
        writer.writerows(nodes)
