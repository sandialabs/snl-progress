from pathlib import Path

def get_path() -> Path:
    return Path(__file__).resolve().parent
# returns: /Users/...../projects/QuESt/quest-apps/forks/snl-progress/progress

def get_home_dir() -> Path:
    return Path.home()

# returns: /Users/xxxx...
