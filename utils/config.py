# utils/config.py

import yaml
from pathlib import Path

def load_config(path="config.yaml") -> dict:
    config_path = Path.cwd() / path
    if not config_path.exists():
        raise FileNotFoundError(f"Missing config file at: {config_path}")

    with open(config_path, "r") as f:
        return yaml.safe_load(f)
