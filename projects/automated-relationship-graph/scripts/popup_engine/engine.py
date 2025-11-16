from .config import load_config
from .loader import load_all
from .writer import write_nodes
from .utils import infer_node_type, group_by
from .builder_person import build_person_popup
from .builder_company import build_company_popup
from .builder_sector import build_sector_popup

def run_popup_engine():
    cfg = load_config()
    theme = cfg["theme"]

    data = load_all()
    nodes = data["nodes"]
    links = data["links"]

    # adjacency
    from collections import defaultdict
    links_by_src = defaultdict(list)
    links_by_tgt = defaultdict(list)
    for l in links:
        links_by_src[l["source"]].append(l)
        links_by_tgt[l["target"]].append(l)

    for n in nodes:
        t = n["type"]
        if t == "person":
            n["popup_html"] = build_person_popup(n, data, cfg["person"], theme, links_by_src, links_by_tgt)
        elif t == "company":
            n["popup_html"] = build_company_popup(n, data, cfg["company"], theme, links_by_src, links_by_tgt)
        elif t == "sector":
            n["popup_html"] = build_sector_popup(n, data, cfg["sector"], theme, links_by_src, links_by_tgt)
        else:
            n["popup_html"] = ""

    write_nodes(nodes)

    print("Popups generated successfully.")
