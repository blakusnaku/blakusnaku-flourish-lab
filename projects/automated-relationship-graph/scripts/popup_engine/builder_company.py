from .html_blocks import small, section
from .utils import compress_html


# ------------------------------------------------------------
# PREMIUM COMPANY HEADER BLOCK
# ------------------------------------------------------------
def company_header_block(name, logo_url, sector_name, accent, website_url):
    return f"""
    <div style="margin-bottom:18px;">

        <!-- ROW: Logo + Identity -->
        <div style="
            display:flex;
            align-items:center;
            gap:16px;
        ">

            <!-- Large Clean Logo -->
            <div style="
                width:56px;
                height:56px;
                display:flex;
                justify-content:center;
                align-items:center;
                flex-shrink:0;
            ">
                <img src="{logo_url}" 
                     style="width:100%;height:100%;object-fit:contain;">
            </div>

            <!-- Company Text + Website Button -->
            <div style="line-height:1.20; display:flex; flex-direction:column;">

                <!-- Name Row w/ External Link Button -->
                <div style="display:flex; align-items:center; gap:6px;">

                    <div style="
                        font-size:20px;
                        font-weight:700;
                        color:{accent};
                    ">{name}</div>

                    <!-- Website Button -->
                    <a href="{website_url}" target="_blank" style="
                        display:flex;
                        padding:4px;
                        border-radius:6px;
                        background:rgba(255,255,255,0.10);
                        transition:0.15s;
                    " onmouseover="this.style.background='rgba(255,255,255,0.16)'" 
                      onmouseout="this.style.background='rgba(255,255,255,0.10)'">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="{accent}">
                            <path d="M14 3h7v7h-2V6.41l-9.29 9.3-1.42-1.42 9.3-9.29H14V3z"/>
                            <path d="M5 5h5V3H5c-1.1 0-2 .9-2 2v10c0 1.1.9 2 2 2h10c1.1 0 
                                     2-.9 2-2v-5h-2v5H5V5z"/>
                        </svg>
                    </a>

                </div>

                <!-- Subtitle -->
                <div style="
                    font-size:13px;
                    color:#CCCCCC;
                    margin-top:2px;
                ">{sector_name} • Company</div>

            </div>

        </div>

        <!-- Divider -->
        <div style="
            margin-top:14px;
            height:2px;
            width:100%;
            background:linear-gradient(90deg, {accent}, rgba(255,255,255,0));
            opacity:0.9;
        "></div>

    </div>
    """




# ------------------------------------------------------------
# MAIN COMPANY POPUP BUILDER
# ------------------------------------------------------------
def build_company_popup(node, data, cfg, theme, links_by_source, links_by_target):
    """
    Builds popup HTML for company nodes.
    """

    FONT  = theme["font_family"]
    ACCENT = theme["accent_color"]
    TEXT   = theme["text_color"]
    MUTED  = theme["muted_text_color"]
    WIDTH  = theme["width_px"]

    name = node["name"]
    popup_parts = []

    # ------------------------------------------------
    # 0. Find matching company
    # ------------------------------------------------
    company = next((c for c in data["companies"] if c["name"] == name), None)
    if not company:
        return ""  # fail gracefully

    # Resolve sector name
    sec_uid = company.get("sector_uid")
    sector = next((s for s in data["sectors"] if s["sector_uid"] == sec_uid), None)
    sector_name = sector["name"] if sector else "Sector"

    # ------------------------------------------------
    # 1. Premium Header
    # ------------------------------------------------
    popup_parts.append(
        company_header_block(
            name=name,
            logo_url=company.get("logo", ""),
            sector_name=sector_name,
            accent=ACCENT,
            website_url=company.get("website", "#")
        )
    )

    # ------------------------------------------------
    # 2. Company Meta Info
    # ------------------------------------------------
    meta_lines = []

    if cfg.get("show_sector", True) and sector:
        meta_lines.append(f"<strong>Sector:</strong> {sector['name']}")

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
    # 3. People Linked to the Company
    # ------------------------------------------------
    if cfg.get("show_people_summary", True):
        curr = []
        past = []

        node_id = node["id"]

        # Check both direction link maps
        for l in links_by_source[node_id] + links_by_target[node_id]:
            other_id = l["target"] if l["source"] == node_id else l["source"]

            if not other_id.startswith("P"):
                continue

            person_node = next((p for p in data["nodes"] if p["id"] == other_id), None)
            if not person_node:
                continue

            if l["type"] == "works_at":
                curr.append(person_node["name"])
            elif l["type"] == "worked_at":
                past.append(person_node["name"])

        # dedupe
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
    # 4. Capital Links
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

            if src == node_id and tgt.startswith("C"):
                other = next((c for c in data["nodes"] if c["id"] == tgt), None)
                if other:
                    portfolio.add(other["name"])

            if tgt == node_id and src.startswith("C"):
                other = next((c for c in data["nodes"] if c["id"] == src), None)
                if other:
                    investors.add(other["name"])

        lines = []
        if investors:
            max_inv = cfg.get("max_investors", 5)
            lines.append(f"<strong>Investors:</strong> {', '.join(list(investors)[:max_inv])}")

        if portfolio:
            max_port = cfg.get("max_portfolio", 5)
            lines.append(f"<strong>Portfolio:</strong> {', '.join(list(portfolio)[:max_port])}")

        if lines:
            popup_parts.append(
                section("Connections", "<br>".join(lines), ACCENT)
            )

    # ------------------------------------------------
    # Final HTML wrapper
    # ------------------------------------------------
    html = f"""
    <div style="width:{WIDTH}px; font-family:{FONT}; color:{TEXT};">
        {''.join(popup_parts)}
    </div>
    """

    return compress_html(html)
