# src/utils.py
from __future__ import annotations
import logging
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

def get_project_root() -> Path:
    return PROJECT_ROOT

def get_data_path() -> Path:
    p = PROJECT_ROOT / "data"
    p.mkdir(parents=True, exist_ok=True)
    return p

def configure_logging(level=logging.INFO):
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
