from pathlib import Path

def get_path() -> Path:
    return Path(__file__).resolve().parent

