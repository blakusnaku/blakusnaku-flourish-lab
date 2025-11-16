from .html_blocks import title_block, small, section 
from .utils import compress_html

def build_person_popup(node, data, cfg, theme, links_by_source, links_by_target):
    """
    Builds popup HTML for PERSON nodes.
    """

    # -------------------------------
    # THEME SETTINGS
    # -------------------------------
    FONT  = theme["font_family"]
    ACCENT = theme["accent_color"]
    TEXT   = theme["text_color"]
    MUTED  = theme["muted_text_color"]
    WIDTH  = theme["width_px"]

    # -------------------------------
    # BASIC INFO
    # -------------------------------
    name = node["name"]
    popup_parts = []

    # Title
    popup_parts.append(title_block(name, ACCENT))

    # Person CRM entry
    person = next((p for p in data["people"] if p["name"] == name), None)
    if not person:
        return ""

    # -------------------------------
    # CURRENT ROLE & SECTOR
    # -------------------------------
    if cfg.get("show_current_role", True):
        role = person.get("current_title", "")
        if role:
            popup_parts.append(small(role, MUTED))

    # Primary Sector (resolve name)
    if cfg.get("show_primary_sector", True):
        sec_uid = person.get("primary_sector_uid", "")
        sec = next((s for s in data["sectors"] if s["sector_uid"] == sec_uid), None)
        if sec:
            popup_parts.append(small(f"Sector: {sec['name']}", MUTED))

    # -------------------------------
    # CAREER HISTORY
    # -------------------------------
    if cfg.get("show_career_history", True):
        wh = data["work_hist"]

        # UID → company_name map
        companies_by_uid = {c["company_uid"]: c for c in data["companies"]}

        entries = []
        for r in wh:
            if r["person_uid"] != person["person_uid"]:
                continue

            comp_uid = r["company_uid"]
            comp = companies_by_uid.get(comp_uid, {})
            comp_name = comp.get("name", comp_uid)

            start = r["start_date"][:4]
            end   = r["end_date"][:4]

            entries.append(f"{r['title']} @ {comp_name} ({start}–{end})")

        if entries:
            popup_parts.append(
                section(
                    "Career history",
                    "<br>".join(entries[: cfg.get("max_history_items", 4)]),
                    ACCENT
                )
            )

    # -------------------------------
    # CONNECTION SUMMARY
    # -------------------------------
    if cfg.get("show_connection_summary", True):
        node_id = node["id"]
        neighbors = set()

        for l in links_by_source[node_id] + links_by_target[node_id]:
            other = l["target"] if l["source"] == node_id else l["source"]
            neighbors.add(other)

        popup_parts.append(
            small(f"Connections: {len(neighbors)} nodes", MUTED)
        )

    # -------------------------------
    # FINAL HTML BLOCK
    # -------------------------------
    html = f"""
    <div style="
        width:{WIDTH}px;
        font-family:{FONT};
        color:{TEXT};
    ">
        {''.join(popup_parts)}
    </div>
    """

    return compress_html(html)
