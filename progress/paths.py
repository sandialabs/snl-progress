from pathlib import Path
from ruamel.yaml import YAML
from typing import Any
import yaml
import logging 

logger = logging.getLogger(__name__)

def get_path() -> Path:
    return Path(__file__).resolve().parent
# returns: /Users/...../projects/QuESt/quest-apps/forks/snl-progress/progress

def get_home_dir() -> Path:
    return Path.home()

# returns: /Users/xxxx...

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

BASE_DIR = get_path()
HOME_DIR = get_home_dir()
DATA_DIR = get_data_path()
SOLAR_DIR = get_solar_data_path()
SYSTEM_DIR = get_system_data_path()
WIND_DIR = get_wind_data_path()
RESULTS_DIR = get_results_path()
# /Users/eecabre/projects/QuESt/quest-apps/forks/snl-progress/progress/Data
# /Users/eecabre/projects/QuESt/quest-apps/forks/snl-progress/progress/Data/Solar
# /Users/eecabre/projects/QuESt/quest-apps/forks/snl-progress/progress/Data/System
# /Users/eecabre/projects/QuESt/quest-apps/forks/snl-progress/progress/Data/Wind
# /Users/eecabre/projects/QuESt/quest-apps/forks/snl-progress/progress/Results

def update_data_path() -> None:
    data_path = get_data_path()
    yaml_file_path = str(Path(__file__).resolve().parent / "input.yaml")

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
