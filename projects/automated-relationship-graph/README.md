# Automated Relationship Intelligence Graph  
A fully automated, Python-generated relationship intelligence graph powered by a custom Clay-style CRM system.

This project demonstrates how structured relationship data (people, companies, sectors, work history, and custom edges) can be automatically generated, transformed, and visualized using a modular export pipeline.

---
## 📊 Preview

![Flourish Screenshot](https://github.com/blakusnaku/blakusnaku-flourish-lab/blob/main/projects/automated-relationship-graph/assets/screenshot.PNG)
[Flourish Live link](https://public.flourish.studio/visualisation/26247845/)

---

## 🚀 Overview

This project recreates the foundations of relationship-intelligence platforms (e.g., Clay, Affinity) by:

1. **Generating a synthetic CRM** with realistic entities and relationships  
2. **Exporting graph-ready files** (`nodes.csv`, `links.csv`)  
3. **Preparing for custom HTML popups** inside Flourish  
4. **Visualizing the graph** using Flourish’s Network Graph template

Every node and link in the graph is produced *entirely by Python scripts*, with no manual editing.

---

## 🧠 Project Architecture

```
/crm → auto-generated CRM tables
  
/scripts
generate_crm_csvs.py → builds dummy CRM (Clay-style)
build_flourish_export.py → generates nodes.csv + links.csv
build_popups.py → (coming soon) auto-generates popup_html
  
/export
nodes.csv → Flourish-ready nodes
links.csv → Flourish-ready edges
  
/flourish
screenshot.png → exported graph visualization
```

Each stage is fully modular, allowing easy upgrades, variations, and future tooling.

---

## 🧩 1. Clay-Style CRM Generation

`generate_crm_csvs.py` creates a complete internal CRM dataset, including:

### **Entities**
- **People** (name, title, current company, primary sector)
- **Companies** (sector, size bucket, location, tags)
- **Sectors** (FinTech, HealthTech, Climate, SaaS, etc.)

### **Work History**
- Multi-year role timelines  
- Start/end dates  
- Current vs past roles  
- Sector inference based on employment

### **Relationship Edges**
- cofounder_with  
- invested_in  
- advisor_to  
- board_member_of  
- plus any custom edges added during generation

The output mirrors the structure of professional relationship platforms.

---

## 🔗 2. Automated Export (nodes.csv + links.csv)

`build_flourish_export.py` transforms the CRM tables into clean graph files:

### **nodes.csv**
Contains:
- id (short ID: P001, C001, S001)
- name
- type (person, company, sector)
- group
- popup_html (currently empty — filled later)

### **links.csv**
Generates all relationship edges:
- `works_at`  
- `worked_at`  
- `in_sector`  
- `works_in_sector`  
- `worked_in_sector`  
- custom relationship links  

All IDs are consistently mapped using an internal UID → short ID conversion layer.

---

## 🎨 3. Visualization in Flourish

The graph is rendered using the **Flourish Network Graph** template.

Features:
- Color-coded node types  
- Auto-generated relationship clusters  
- Past + current sector paths  
- Clean header and footer styling  
- Supports rich HTML popups (coming soon)

---

## 🛠️ 4. Next Steps (Upcoming Additions)

### **🔧 Popup HTML Generator**
A new script (`build_popups.py`) will:

- Read CRM tables + `links.csv`  
- Build Clay-style profile cards  
- Insert them into `popup_html` field in `nodes.csv`  
- Support multiple designs through `popup_specs.json`

### **🎨 Custom Popup Themes**
Popup variations will be configurable through a JSON spec:
- Title/subtitle formatting  
- Career timeline block  
- Connections block  
- Sector expertise  
- Investments / companies / roles  

This will allow multiple UI versions with zero code changes.

---

## 🧡 Created By
JP Malit [@blakusnaku](https://github.com/blakusnaku)

This project is part of a larger initiative to explore data automation, visualization, and CRM intelligence systems through Python.
