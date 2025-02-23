import os
from datetime import datetime


def ensure_directory(path: str) -> str:
    """Ensure the directory exists. If not, create it."""
    os.makedirs(path, exist_ok=True)
    return path


def generate_timestamp() -> str:
    """Generate a timestamp in the format YYYYMMDDHHMM."""
    return datetime.now().strftime("%Y%m%d%H%M")