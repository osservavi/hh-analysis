import os
from pathlib import Path

BASE_DIR = Path(__file__).parent

DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

NOTEBOOKS_DIR = BASE_DIR / "notebooks"
REPORTS_DIR = BASE_DIR / "reports"
SRC_DIR = BASE_DIR / "src"

for directory in [RAW_DATA_DIR, PROCESSED_DATA_DIR, NOTEBOOKS_DIR, REPORTS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)