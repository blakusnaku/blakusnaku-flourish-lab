from collections import defaultdict

def index_by_key(rows, key):
    return {r[key]: r for r in rows}

def group_by(rows, key):
    out = defaultdict(list)
    for r in rows:
        out[r[key]].append(r)
    return out

def infer_node_type(node_id):
    if node_id.startswith("P"): return "person"
    if node_id.startswith("C"): return "company"
    if node_id.startswith("S"): return "sector"
    return "unknown"

def compress_html(html: str) -> str:
    return " ".join(html.split())