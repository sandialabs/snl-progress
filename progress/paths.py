from pathlib import Path
from ruamel.yaml import YAML
from typing import Any
import yaml
import logging
import sys
import shutil

logger = logging.getLogger(__name__)

def _is_frozen() -> bool:
    return getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')

def get_bundle_path() -> Path:
    """Read-only path to bundled resources inside the PyInstaller bundle."""
    if _is_frozen():
        return Path(sys._MEIPASS) / "progress"
    return Path(__file__).resolve().parent

def get_path() -> Path:
    if _is_frozen():
        return Path.home() / ".progress"
    return Path(__file__).resolve().parent

def get_home_dir() -> Path:
    return Path.home()

def get_data_path() -> Path:
    return get_path() / "Data"

def get_solar_data_path() -> Path:
    return get_data_path() / "Solar"

def get_system_data_path() -> Path:
    return get_data_path() / "System"

def get_wind_data_path() -> Path:
    return get_data_path() / "Wind"

def get_results_path() -> Path:
    results_dir = get_path() / "Results"
    results_dir.mkdir(exist_ok=True, parents=True)
    return results_dir

def get_theme_path() -> Path:
    return get_path() / "resources"

def _setup_user_dir() -> None:
    """Copy bundled resources to the writable user directory on first run."""
    if not _is_frozen():
        return
    bundle = get_bundle_path()
    user = get_path()
    user.mkdir(parents=True, exist_ok=True)
    for name in ["Data", "resources", "Images"]:
        src = bundle / name
        dst = user / name
        if src.exists() and not dst.exists():
            shutil.copytree(src, dst)
    src_yaml = bundle / "input.yaml"
    dst_yaml = user / "input.yaml"
    if src_yaml.exists() and not dst_yaml.exists():
        shutil.copy2(src_yaml, dst_yaml)

BASE_DIR = get_path()
if _is_frozen():
    _setup_user_dir()
HOME_DIR = get_home_dir()
DATA_DIR = get_data_path()
SOLAR_DIR = get_solar_data_path()
SYSTEM_DIR = get_system_data_path()
WIND_DIR = get_wind_data_path()
RESULTS_DIR = get_results_path()

def update_data_path() -> None:
    data_path = get_data_path()
    yaml_file_path = str(get_path() / "input.yaml")

    # initialize the round-trip YAML parser
    yaml = YAML()
    yaml.preserve_quotes = True  # Keeps quotes around strings if they were there

    # read the existing file (including comments)
    with open(yaml_file_path, "r") as file:
        config_data = yaml.load(file)

    # update only the targeted data path key
    config_data["data"] = str(data_path)

    # write the changes back to the file (comments are preserved)
    with open(yaml_file_path, "w") as file:
        yaml.dump(config_data, file)
    # safely print the confirmation using mixed quotes
    logger.info(f"Successfully updated the data path, data path is now: {config_data['data']}")

def check_era_api_key_existence() -> bool:
    api_key_file = get_home_dir() / ".cdsapirc"
    if api_key_file.is_file():
        logger.info(f"API KEY LOCATION: {api_key_file}")
        return True
    else:
        logger.error("NO API KEY EXISTS")
        return False

def load_config() -> dict[str, Any]:
    config_path = get_path() / "input.yaml"

    with open(config_path, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}
