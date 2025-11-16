# 🧠 Automated Relationship Intelligence Graph (Python → Flourish)

A fully automated relationship-mapping system that generates CRM-style entity tables, builds multi-layered graph data, and renders dynamic pop-up cards for interactive network visualization in Flourish.

This project simulates how tools like **Clay**, **Affinity**, and **Apollo** model people, companies, sectors, and connections — but everything is generated and automated end-to-end with Python.

---
## Flourish Preview

[![Flourish Preview](https://github.com/blakusnaku/blakusnaku-flourish-lab/blob/main/projects/automated-relationship-graph/assets/generated_popup_screenshot.PNG)](https://public.flourish.studio/visualisation/26247845/)

---

## 🚀 Features

### **1. Automated Clay-Style CRM Data Generator**
Python script creates realistic CRM tables:
- `people.csv`
- `companies.csv`
- `sectors.csv`
- `people_work_history.csv`
- `relationships.csv`

Each record includes:
- current/previous roles  
- sector classification  
- company-level metadata  
- cross-entity relationships (e.g., works_at, worked_at, invested_in, cofounder_with)

---

### **2. Export Pipeline → `nodes.csv` & `links.csv`**
A second script produces Flourish-ready graph files:
- Node attributes (type, group, size_by, label)
- Relationship edges with typed links:
  - `works_at`
  - `worked_at`
  - `in_sector`
  - `cofounder_with`
  - `invested_in`

This allows Flourish to generate a fully interactive graph.

---

### **3. 🔥 Automated Pop-Up HTML Engine (Modular)**
A fully modular Python “popup engine” generates beautiful interactive HTML cards for every node.

It:
- loads the CRM tables  
- merges node + graph context  
- resolves UIDs to clean names  
- builds Clay-style HTML popups  
- fully styles each card using configurable theme values  
- compresses HTML into a clean one-line string for Flourish  

Popups include:
- **For People:**  
  - role, sector, work history, connection summary  
- **For Companies:**  
  - sector, HQ, size, tags, team list, alumni, investors, portfolio  
- **For Sectors:**  
  - key companies, approximate people linked  

Powered by a modular structure:
```
scripts/
popup_engine/
builder_person.py
builder_company.py
builder_sector.py
html_blocks.py
loader.py
writer.py
engine.py

```
Everything is configurable via:
```
popup_config.json
```

---

## 📁 Project Structure

```
automated-relationship-graph/
│
├── crm/
│   ├── people.csv
│   ├── companies.csv
│   ├── sectors.csv
│   ├── people_work_history.csv
│   └── relationships.csv
│
├── export/
│   ├── nodes.csv
│   └── links.csv
│
├── scripts/
│   ├── generate_crm_csvs.py
│   ├── build_flourish_export.py
│   ├── build_popups.py
│   └── popup_engine/
│       ├── engine.py
│       ├── loader.py
│       ├── writer.py
│       ├── utils.py
│       ├── html_blocks.py
│       ├── builder_person.py
│       ├── builder_company.py
│       └── builder_sector.py
│
├── popup_config.json
└── run_whole_pipeline.py
```

---

## 🛠 Tech Stack

Python 3.10+  
Pandas (optional)  
Flourish Studio  
HTML/CSS (inline styling)  

---

## 📊 Output Preview

The final visualization includes:  
• Sector, company, and person nodes  
• Automatically sized nodes  
• Fully dynamic pop-ups  
• Connection paths and typed edges  
• Hover-based exploration similar to professional intelligence tools  

---

## 🟠 Author

**JP Malit (@blakusnaku)**  
Data modeling, pipeline automation, and visualization logic built in Python.  
Nodes, relationship links, and pop-up HTML cards generated fully automatically.  

---

## 🧩 Next Steps (Planned)

• Add color themes for different datasets  
• Extend relationship types (advisor_of, reports_to, partner_with)  
• Optional: integrate real CRM/API data (HubSpot, Clay, Notion)  
