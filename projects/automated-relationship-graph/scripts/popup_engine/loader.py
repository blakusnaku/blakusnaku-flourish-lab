import csv
import os

# popup_engine/loader.py → scripts/popup_engine → scripts → project root
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

CRM_DIR = os.path.join(PROJECT_ROOT, "crm")
EXPORT_DIR = os.path.join(PROJECT_ROOT, "export")

def load_csv(path):
    if not os.path.exists(path):
        print("ERROR: Missing file:", path)
        raise FileNotFoundError(path)

    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def load_all():
    people   = load_csv(os.path.join(CRM_DIR, "people.csv"))
    companies = load_csv(os.path.join(CRM_DIR, "companies.csv"))
    sectors   = load_csv(os.path.join(CRM_DIR, "sectors.csv"))
    work_hist = load_csv(os.path.join(CRM_DIR, "people_work_history.csv"))
    rels      = load_csv(os.path.join(CRM_DIR, "relationships.csv"))

    nodes = load_csv(os.path.join(EXPORT_DIR, "nodes.csv"))
    links = load_csv(os.path.join(EXPORT_DIR, "links.csv"))

    return {
        "people": people,
        "companies": companies,
        "sectors": sectors,
        "work_hist": work_hist,
        "relationships": rels,
        "nodes": nodes,
        "links": links
    }
