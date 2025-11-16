from .html_blocks import title_block, small, section
from .utils import compress_html

def build_company_popup(node, data, cfg, theme, links_by_source, links_by_target):
    """
    Builds popup HTML for company nodes.

    node:  dict from nodes.csv
    data:  dict containing CRM tables (people, companies, sectors, work_hist, relationships)
    cfg:   company section of popup_config.json
    theme: theme section of popup_config.json
    """

    FONT  = theme["font_family"]
    ACCENT = theme["accent_color"]
    TEXT   = theme["text_color"]
    MUTED  = theme["muted_text_color"]
    WIDTH  = theme["width_px"]

    name = node["name"]
    popup_parts = []

    # ------------------------------------------------
    # 1. Title
    # ------------------------------------------------
    popup_parts.append(title_block(name, ACCENT))

    # Find matching company in CRM
    company = next((c for c in data["companies"] if c["name"] == name), None)
    if not company:
        return ""  # no match (shouldn't happen)

    # ------------------------------------------------
    # 2. Company Meta Info
    # ------------------------------------------------
    meta_lines = []

    if cfg.get("show_sector", True):
        sec_uid = company.get("sector_uid", "")
        sec = next((s for s in data["sectors"] if s["sector_uid"] == sec_uid), None)
        if sec:
            meta_lines.append(f"<strong>Sector:</strong> {sec['name']}")

    if cfg.get("show_location", True):
        loc = company.get("hq_location", "")
        if loc:
            meta_lines.append(f"<strong>HQ:</strong> {loc}")

    if cfg.get("show_size", True):
        size = company.get("size_bucket", "")
        if size:
            meta_lines.append(f"<strong>Size:</strong> {size}")

    if cfg.get("show_tags", True):
        tags = company.get("tags", "")
        if tags:
            meta_lines.append(f"<strong>Tags:</strong> {tags}")

    if meta_lines:
        popup_parts.append(
            small("<br>".join(meta_lines), MUTED)
        )

    # ------------------------------------------------
    # 3. People Linked to Company
    # ------------------------------------------------
    if cfg.get("show_people_summary", True):
        curr = []
        past = []

        node_id = node["id"]

        # Look at all links where this company is source or target
        for l in links_by_source[node_id] + links_by_target[node_id]:
            other_id = l["target"] if l["source"] == node_id else l["source"]

            if not other_id.startswith("P"):
                continue  # only want people

            person_node = next((p for p in data["nodes"] if p["id"] == other_id), None)
            if not person_node:
                continue

            if l["type"] == "works_at":
                curr.append(person_node["name"])
            elif l["type"] == "worked_at":
                past.append(person_node["name"])

        # Deduplicate
        curr = list(dict.fromkeys(curr))
        past = list(dict.fromkeys(past))

        lines = []
        if curr:
            max_curr = cfg.get("max_current_people", 5)
            lines.append(f"<strong>Current team:</strong> {', '.join(curr[:max_curr])}")

        if past:
            max_past = cfg.get("max_past_people", 3)
            lines.append(f"<strong>Alumni:</strong> {', '.join(past[:max_past])}")

        if lines:
            popup_parts.append(
                section("People", "<br>".join(lines), ACCENT)
            )

    # ------------------------------------------------
    # 4. Capital Links (investors & portfolio)
    # ------------------------------------------------
    if cfg.get("show_investor_summary", True):
        investors = set()
        portfolio = set()
        node_id = node["id"]

        for l in data["links"]:
            if l["type"] != "invested_in":
                continue

            src = l["source"]
            tgt = l["target"]

            # If this company invested in another company
            if src == node_id and tgt.startswith("C"):
                other = next((c for c in data["nodes"] if c["id"] == tgt), None)
                if other:
                    portfolio.add(other["name"])

            # If another company invested in this company
            if tgt == node_id and src.startswith("C"):
                other = next((c for c in data["nodes"] if c["id"] == src), None)
                if other:
                    investors.add(other["name"])

        lines = []
        if investors:
            lines.append(f"<strong>Investors:</strong> {', '.join(list(investors)[:cfg.get('max_investors',5)])}")
        if portfolio:
            lines.append(f"<strong>Portfolio:</strong> {', '.join(list(portfolio)[:cfg.get('max_portfolio',5)])}")

        if lines:
            popup_parts.append(
                section("Capital links", "<br>".join(lines), ACCENT)
            )

    # ------------------------------------------------
    # Final HTML
    # ------------------------------------------------
    html = f"""
    <div style="width:{WIDTH}px; font-family:{FONT}; color:{TEXT};">
        {''.join(popup_parts)}
    </div>
    """
    return compress_html(html)
