import json
import os

# Always resolve config path relative to this file's position
# popup_engine/config.py  → project root = two levels up
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CONFIG_PATH = os.path.join(PROJECT_ROOT, "popup_config.json")

def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        print("WARNING: popup_config.json not found at:", CONFIG_PATH)
        return {}
