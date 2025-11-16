from .html_blocks import title_block, small, section
from .utils import compress_html

def build_sector_popup(node, data, cfg, theme, links_by_source, links_by_target):
    """
    Builds popup HTML for sector nodes.
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

    node_id = node["id"]

    # ------------------------------------------------
    # 2. Companies connected to this sector
    # ------------------------------------------------
    if cfg.get("show_companies", True):
        companies = []

        for l in links_by_source[node_id] + links_by_target[node_id]:
            other_id = l["target"] if l["source"] == node_id else l["source"]
            if other_id.startswith("C"):
                comp_node = next((c for c in data["nodes"] if c["id"] == other_id), None)
                if comp_node:
                    companies.append(comp_node["name"])

        companies = list(dict.fromkeys(companies))
        max_comp = cfg.get("max_companies", 8)

        if companies:
            popup_parts.append(
                section("Key companies", ", ".join(companies[:max_comp]), ACCENT)
            )

    # ------------------------------------------------
    # 3. People count (optional)
    # ------------------------------------------------
    if cfg.get("show_people_count", True):
        people = set()

        for l in links_by_source[node_id] + links_by_target[node_id]:
            other_id = l["target"] if l["source"] == node_id else l["source"]

            if other_id.startswith("C"):
                # collect people linked to these companies
                for l2 in links_by_source[other_id] + links_by_target[other_id]:
                    oid2 = l2["target"] if l2["source"] == other_id else l2["source"]
                    if oid2.startswith("P"):
                        people.add(oid2)

        if people:
            popup_parts.append(
                small(f"Approx. {len(people)} people linked to this sector.", MUTED)
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
