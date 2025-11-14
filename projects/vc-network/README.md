# VC Relationship Network (Flourish Visualization)

This project is an interactive **network visualization** built in Flourish, modeling relationships between **people**, **companies**, and **sectors** using a nodes-and-links data structure.

It is the first project inside the `blakusnaku-flourish-lab` and demonstrates how VC-style relationship intelligence dashboards can be constructed using structured TSV files + custom HTML popups.

---

## 🔗 Live Visualization
[View Live Dashboard Here](https://public.flourish.studio/visualisation/26229368/)

---

## 📸 Preview
![VC Network Screenshot](https://github.com/blakusnaku/blakusnaku-flourish-lab/blob/main/projects/vc-network/screenshot.PNG)

---

## 📁 Project Contents
```
vc-network/
├── nodes.tsv
├── links.tsv
└── screenshot.png 
```

The main processing notes and learning documentation are stored at the repo root:

➡️ [`/vc_network_learning_log.md`](https://github.com/blakusnaku/blakusnaku-flourish-lab/blob/main/notes/vc_network_learning_log.md)

---

## 🧩 Dataset Model

### **Nodes (`nodes.tsv`)**
Contains the list of all entities:
- 10 People  
- 10 Companies  
- 3 Sectors  

Key columns:
- `id`
- `label`
- `color_by` (person/company/sector)
- `size_by`
- `popup_color`
- `popup_content` (custom HTML card)

### **Links (`links.tsv`)**
Defines explicit relationships:
- Current Staff
- Prior Staff
- Current Portcos
- Prior Portcos
- Sector Experience (person/company → sector)

Flourish reads these two TSV files and builds the network.

---

## 🎨 Popup Card Design

Each popup uses HTML to create a clean, readable, VC-style card:

- Dynamic color synced to node type  
- Lowercase muted subtitle  
- Logical grouping:
  - staff  
  - portcos  
  - sector  
  - works at / worked at  

The full HTML logic is auto-generated through a Python script (optional).

---

## 🛠 Automation

A Python script (`generate_popups.py`) can reconstruct the `popup_content` field automatically from CRM-like relationship tables.

Pipeline:

```
CRM export → Python processing → nodes.tsv + links.tsv → Flourish upload
```

This makes the workflow scalable for larger datasets.

---

## 📝 Notes

For the full processing workflow, reasoning, and learning breakdown:

➡️ See: [`/vc_network_learning_log.md`](https://github.com/blakusnaku/blakusnaku-flourish-lab/blob/main/notes/vc_network_learning_log.md)

---

## ✔ Status
Project completed (v1).  
Future updates planned:
- Node size scaling
- Alternative layout tuning
- Auto-generated TSVs from CRM exports

