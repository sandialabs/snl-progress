from pathlib import Path
from ruamel.yaml import YAML
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
    return get_path() / "Results"

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

    # # Read the existing YAML file
    # yaml_file_path = str(Path(__file__).resolve().parent / "input.yaml")
    # with open(yaml_file_path, "r") as file:
    #     # Use safe_load to safely parse existing data into a dictionary
    #     config_data = yaml.safe_load(file) or {}
    #
    # # Update ONLY the target key with the string version of the path
    # config_data["data"] = str(data_path)
    #
    # # Write the updated data back to the file
    # with open(yaml_file_path, "w") as file:
    #     yaml.dump(config_data, file, default_flow_style=False)
    #
    # print(f"Successfully updated the data path, data path is now: {config_data['data']}")



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
