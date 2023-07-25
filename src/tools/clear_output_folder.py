import sys
import os

from pathlib import Path

base_path = Path(__file__).parent.parent.parent
sys.path.append(base_path.as_posix())
from src.config import TARGET_PATH

def clear_output_folder():
    if not os.path.isdir(TARGET_PATH):
        return
    for root, dirs, files in os.walk(TARGET_PATH, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    print(f"Output folder cleared.")
