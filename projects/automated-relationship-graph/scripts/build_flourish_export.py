#===================================================
# 📦 PROJECT METADATA
#---------------------------------------------------
# Genrates Flourish-ready nodes.csv and links.csv
# from the exitings CRM tables.
#
# Input:
#   - crm/people.csv
#   - crm/companies.csv
#   - crm/sectors.csv
#   - crm/people_work_history.csv
#   - crm/relationships.csv
#
# Output:
#   - export/nodes.csv
#   - export/links.csv
#===================================================

import csv
import os
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CRM_DIR = os.path.join(ROOT, "crm")
EXPORT_DIR = os.path.join(ROOT, "export")

os.makedirs(EXPORT_DIR, exist_ok=True)

# Helper: Write CSV
def write_csv(path, fieldnames, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

# Helper: Short ID Mapper
uid_map = {}
id_counter = defaultdict(int)

def get_export_id(uid, prefix):
    #consistently maps long UID -> short ID (e.g., P001)
    if uid in uid_map:
        return uid_map[uid]
    
    id_counter[prefix] += 1
    export_id = f"{prefix}{id_counter[prefix]:03d}"
    uid_map[uid] = export_id
    return export_id

# load crm tables
def load_csv(name):
    path = os.path.join(CRM_DIR,name)
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))

people = load_csv("people.csv")
companies = load_csv("companies.csv")
sectors = load_csv("sectors.csv")
work_history = load_csv("people_work_history.csv")
relationships = load_csv("relationships.csv")

#indexes for fast lookup
companies_by_uid = {c["company_uid"]: c for c in companies}
sectors_by_uid = {s["sector_uid"]: s for s in sectors}

work_by_person = defaultdict(list)
for w in work_history:
    work_by_person[w['person_uid']].append(w)


nodes = []

#build nodes
def build_nodes():

    #sectors
    for s in sectors:
        export_id = get_export_id(s['sector_uid'], "S")
        nodes.append({
            "id": export_id,
            "name": s["name"],
            "type": "sector",
            "group": "Sectors",
            "size_by": 18,
            "popup_html": ""
        })

    #companies
    for c in companies:
        export_id = get_export_id(c['company_uid'], "C")
        nodes.append({
        "id": export_id,
        "name": c["name"],
        "type": "company",
        "group": "Companies",
        "size_by": 12,
        "popup_html": ""
    })
        
    #people
    for p in people:
        export_id = get_export_id(p['person_uid'], "P")
        nodes.append({
            "id": export_id,
            "name": p['name'],
            "type": "person",
            "group": "People",
            "size_by": 3,
            "popup_html": ""
        })


links = []
def build_links():

    #work history links (worked_at, works_at)
    for w in work_history:
        p_id = get_export_id(w['person_uid'], "P")
        c_id = get_export_id(w['company_uid'], "C")

        rel_type = "works_at" if w['is_current'] == "TRUE" else "worked_at"

        links.append({
            "source": p_id,
            "target": c_id,
            "type": rel_type
        })
    
    #company -> sector links
    for c in companies:
        c_id = get_export_id(c['company_uid'], "C")
        s_id = get_export_id(c['sector_uid'], "S")

        links.append({
            "source": c_id,
            "target": s_id,
            "type": "in_sector"
        }) 

    #person -> sector links (based on all companies)
    for w in work_history:
        person_uid = w['person_uid']
        company_uid = w['company_uid']

        #get export ids
        person_export = get_export_id(person_uid,"P")

        #look up company
        comp = companies_by_uid.get(company_uid)
        if not comp:
            continue

        #its sector
        sector_uid = comp["sector_uid"]
        sector_export = get_export_id(sector_uid, "S")

        #determine link type
        #current jobs -> works_in_sector
        #past jobs -> worked_in_sector
        if w['is_current'] == "TRUE":
            link_type = "works_in_sector"
        else:
            link_type = "worked_in_sector"
        
        #add the link
        links.append({
            "source": person_export,
            "target": sector_export,
            "type": link_type
        })

    #special relationships
    for r in relationships:
        src = get_export_id(r["source_uid"], "X")
        tgt = get_export_id(r["target_uid"], "X")

        links.append({
            "source": src,
            "target": tgt,
            "type": r["relationship_type"]
        })

def write_csvs():
    write_csv(
        os.path.join(EXPORT_DIR, "nodes.csv"),
        ["id","name","type","group","size_by","popup_html"],
        nodes
    )

    write_csv(
        os.path.join(EXPORT_DIR, "links.csv"),
        ["source", "target", "type"],
        links
    )

def run_build_flourish_export():
    build_nodes()
    build_links()
    write_csvs()
    print("\n====================================")
    print("✅ Flourish export generated (NO POPUPS)")
    print("📄 export/nodes.csv")
    print("📄 export/links.csv")
    print("====================================\n")

if __name__ == "__main__":
    run_build_flourish_export()