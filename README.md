# 🟠 blakusnaku-flourish-lab
>*A growing collection of interactive data visualizations, prototypes, and Flourish experiments.*

This repository serves as my sandbox and learning hub for mastering **Flourish**, an interactive data visualization tool used widely in journalism, analytics, and business intelligence.

The goal of this lab is to:

- Explore Flourish templates
- Build interactive prototypes
- Practice data storytelling
- Experiment with HTML-based popups
- Learn nodes-and-links relationship visualization
- Document real learning progress
- Connect Flourish with Python and CRM pipelines

This repo grows as I grow — every experiment, technique, or breakthrough will be logged here.

---

## 📊 Featured Project — VC Relationship Network Map
[![View in Flourish](https://img.shields.io/badge/Flourish-View%20Interactive-blue)](https://public.flourish.studio/visualisation/26229368/)
[![dashboard](https://github.com/blakusnaku/blakusnaku-flourish-lab/blob/main/projects/vc-network/screenshot.PNG)](https://public.flourish.studio/visualisation/26229368/)


Located in:  
**`/projects/vc-network/`**

This project is an interactive Flourish network visualization built using:

- `nodes.tsv`
- `links.tsv`
- Custom HTML popup cards
- Node-type–synchronized color themes
- A VC-style relationship intelligence data model

It visualizes connections between:

- People → Companies (current and prior staff)
- Companies → Portcos (current and prior portfolio relationships)
- People/Companies → Sectors (sector experience)

### Demonstrates:

- How to design clean, readable network charts  
- How to model CRM-style relationships  
- How to style Flourish popups using HTML  
- How to enrich network data via Python autogeneration  
- How nodes-and-links can tell a business or VC story  
 
---

## 🛠️ Automation — Python → Flourish

Inside **`/scripts/`**, reusable tools convert CRM or tabular datasets into Flourish-ready files.

### Tools include:

- Automatic `popup_content` HTML generation  
- Relationship grouping (staff, portcos, sectors)  
- Dynamic popup color assignment  
- Safe TSV export  
- CRM → Flourish transformation templates  

This enables workflows like:
```
CRM → Python processing → nodes.tsv + links.tsv → Upload to Flourish
```

Ideal for:

- VC/PE relationship maps  
- Organizational network charts  
- Partner ecosystem maps  
- Segment mapping  
- Internal BI storytelling  

---

## 📁 Repository Structure
```
blakusnaku-flourish-lab/
│
├── README.md
│
├── scripts/ 
│
├── data/
│   ├── raw/
│   ├── interim/
│   └── processed/
│
├── assets/
│   ├── banners/
│   └── screenshots/
│
├── projects/
│   └── vc-network/
│       ├── nodes.tsv
│       ├── links.tsv
│       ├── screenshot.png
│       └── notes.md
│
└── notes/
    └── vc-network-processing.md

```

Future Flourish experiments will be added inside `/projects/<name>/`.

---

## 🎯 Purpose of This Lab

Flourish excels at:

- Interactive storytelling  
- Rapid data visualization prototyping  
- Client-facing explainers  
- Network and relationship visualization  
- Clean, non-technical dashboards  
- Business intelligence narratives  

This repository documents my ongoing exploration of those capabilities.

---

## Author

**JP Malit (@blakusnaku)**  
Data Analytics · Python · SQL · Power BI · Visualization

---

## 🏷️ Tags

`#100DaysOfData` `#Flourish` `#InteractiveViz` `#DataStorytelling`  
`#NetworkGraphs` `#VisualizationLab` `#blakusnakuanalytics`


