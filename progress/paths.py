from pathlib import Path

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

BASE_DIR = get_path()
DATA_DIR = get_data_path()
SOLAR_DIR = get_solar_data_path()
SYSTEM_DIR = get_system_data_path()
WIND_DIR = get_wind_data_path()
# /Users/eecabre/projects/QuESt/quest-apps/forks/snl-progress/progress/Data
# /Users/eecabre/projects/QuESt/quest-apps/forks/snl-progress/progress/Data/Solar
# /Users/eecabre/projects/QuESt/quest-apps/forks/snl-progress/progress/Data/System
# /Users/eecabre/projects/QuESt/quest-apps/forks/snl-progress/progress/Data/Wind
