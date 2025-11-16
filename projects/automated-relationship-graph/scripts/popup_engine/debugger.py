import os
from popup_engine.config import load_config

print("ROOT:", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
print("CONFIG:", load_config())