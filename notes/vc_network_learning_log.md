# VC Network Learning Log

*Flourish Side Quest – Relationship Network Visualization*

## 🧠 Overview

Today’s session focused on understanding how to model and visualize VC-style relationship data using **Flourish Network Charts**. I explored how people, companies, and sectors interact, and how to translate those relationships into a nodes-and-links structure that Flourish understands.

This learning log documents the full processing workflow, decisions made, reasoning, and the construction of enriched `nodes.tsv` and `links.tsv` files used in the visualization.

---

## 📊 Data Sources & Structure

### **Nodes**

All entities in the system:

* 10 People
* 10 Companies
* 3 Sectors

Each node includes:

* `id` – Unique identifier
* `label` – Human-readable name
* `color_by` – Person / Company / Sector
* `size_by` – Visual weight
* `popup_color` – Color synced to node type
* `popup_content` – Custom HTML popup card

### **Links**

Defines explicit relationships:

* Current Staff (person → company)
* Prior Staff
* Current Portco (company → company)
* Prior Portco
* Sector Experience (person/company → sector)

Flourish requires *explicit* links — no assumptions.

---

## 🔗 Relationship Logic

### **Staff Relationships**

People are linked to companies through:

* Current Staff
* Prior Staff

### **Portco Relationships**

Company-to-company connections through:

* Current Portcos
* Prior Portcos

### **Sector Experience**

This was the important part of the modeling.

Originally, not all people had explicit sector relationships. Since people are always connected to companies (and every company has a sector), this was improved by:

👉 Automatically linking every person to the sector of their company.

This strengthens cluster visibility and ensures no isolated nodes.

---

## 🎨 Popup Content Generation

Each popup uses custom HTML for a polished, VC-style feel:

* Cream background (`#FFF2E9`)
* Dynamic border-left color
* Title text color synced to node type
* Lowercase muted type subtitle
* Spacing between groups
* Bullet lists for relationship groups

### **Dynamic Color Mapping**

* Person: `#41C7C7`
* Company: `#FE7E70`
* Sector: `#AFF4D7`

### **Section Rules**

Sections appear *only if they have content*:

**For people:**

* works at
* worked at
* sector

**For companies:**

* staff
* portcos
* sector

**For sectors:**

* companies
* people

This makes each card clean, purposeful, and easy to scan.

---

## 🛠️ Automation (Python)

A Python script can fully automate all popup generation:

* Load base nodes + links
* Group relationships
* Build `<ul>` lists
* Assign popup colors
* Insert dynamic HTML templates
* Export Flourish-ready TSV

Pipeline structure:

```
CRM → Python → nodes.tsv + links.tsv → Flourish
```

This means Flourish becomes the **visual layer**, not the data processing layer.

---

## 🚀 Improvements for Later

* Add search functionality inside Flourish
* Add filters (staff only, sectors only, portcos only)
* Resize nodes based on centrality
* Use GitHub Pages to embed Flourish iframe
* Build a reusable template engine for popup HTML
* Add Notion/HubSpot CRM → Python → Flourish integration

---

## ⭐ Key Learnings

1. **Flourish never assumes relationships** — all links must be explicitly defined.
2. **Nodes and links require clean modeling**; unclear relationship logic breaks the visualization.
3. **Popup HTML dramatically improves storytelling**; raw labels alone are insufficient.
4. **Color synchronization matters** — matching popup color to node type makes the chart intuitive.
5. **Sectors must be fully linked** to avoid isolated groups and improve network cohesion.
6. **Python automation is essential** for scaling this beyond the dummy dataset.
7. **CRM schemas fit naturally** into the nodes-and-links model (people, companies, sectors, roles).
8. **Flourish is a visualization layer**, not an ETL or logic layer — data must be preprocessed.

---

## 📝 Reflection

This exercise helped me understand *why* Flourish is popular in VC and PE environments. It's not just a visualization tool — it's a way to **navigate relational data visually**, especially when the relationships tell a story about people, companies, and industries.

I realized that the value isn’t in the chart alone, but in how **clean the underlying model is**. Good visualization comes from good data design.

The process also reminded me how important automation is. Manually writing popup HTML or linking sectors doesn't scale, but once the Python pipeline is set up, it becomes a powerful engine that can transform CRM exports directly into Flourish dashboards.

Overall, this side quest made me appreciate the connection between:

* Data modeling
* Automation
* Storytelling
* Visualization

And how these pieces fit together in real-world analytics roles.

---

## 🔜 Next Steps

* Build the standalone repo (`blakusnaku-flourish-lab`)
* Add VC Network as first project in `/projects/vc-network/`
* Add automation scripts
* Add screenshot thumbnails + README links
* Continue exploring Flourish templates (sunburst, sankey, hierarchy, cards)

---
