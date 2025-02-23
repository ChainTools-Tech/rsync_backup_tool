import yaml
from pathlib import Path
from typing import Dict, Any


def load_config(config_file: str) -> Dict[str, Any]:
    config_path = Path(config_file)
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    with open(config_path, "r") as file:
        config = yaml.safe_load(file)

    # Validate required keys
    required_keys = ["destination", "common_folders", "hosts"]
    for key in required_keys:
        if key not in config:
            raise ValueError(f"Missing required key in configuration: {key}")

    return config