"""
Data validation utilities for ProGRESS.

Provides schema definitions for all expected CSV files and functions to
validate directory structure, file existence, and column names.
"""

from pathlib import Path
import pandas as pd
import logging

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Schema definitions
#
# Each file's schema is a dict with:
#   "columns": list of {"name": str, ...} — expected column definitions
#   "allow_extra": bool — if True, extra columns beyond the schema are tolerated
#
# Columns use the exact names from the CSV files / codebase (which may differ
# from the README — e.g. "Tran OutRate" with a space).
# ---------------------------------------------------------------------------

SYSTEM_SCHEMAS = {
    "branch.csv": {
        "columns": [
            {"name": "Branch ID"},
            {"name": "From Bus"},
            {"name": "To Bus"},
            {"name": "R"},
            {"name": "X"},
            {"name": "B"},
            {"name": "Rating"},
            {"name": "MTTF"},
            {"name": "MTTR"},
            {"name": "Tran OutRate"},
            {"name": "Interzonal"},
        ],
        "allow_extra": False,
    },
    "bus.csv": {
        "columns": [
            {"name": "Bus Name"},
            {"name": "Bus No."},
            {"name": "Zone"},
        ],
        "allow_extra": False,
    },
    "gen.csv": {
        "columns": [
            {"name": "Gen No."},
            {"name": "Gen Name"},
            {"name": "Bus No."},
            {"name": "Zone"},
            {"name": "Tech"},
            {"name": "Max Cap"},
            {"name": "Min Cap"},
            {"name": "FOR"},
            {"name": "MTTF"},
            {"name": "MTTR"},
            {"name": "Cost"},
        ],
        "allow_extra": False,
    },
    "load.csv": {
        "columns": [
            {"name": "datetime"},
        ],
        "allow_extra": True,
    },
    "storage.csv": {
        "columns": [
            {"name": "Name"},
            {"name": "Bus No."},
            {"name": "Zone"},
            {"name": "Pmax"},
            {"name": "Pmin"},
            {"name": "Duration"},
            {"name": "max_SOC"},
            {"name": "min_SOC"},
            {"name": "Efficiency"},
            {"name": "Discharge Cost"},
            {"name": "Charge Cost"},
            {"name": "Units"},
            {"name": "MTTF"},
            {"name": "MTTR"},
            {"name": "Chemistry"},
        ],
        "allow_extra": False,
    },
}

SOLAR_SCHEMAS = {
    "solar_sites.csv": {
        "columns": [
            {"name": "Site Name"},
            {"name": "Latitude"},
            {"name": "Longitude"},
            {"name": "MW_Capacity"},
            {"name": "Tracking"},
            {"name": "Bus No."},
            {"name": "Zone"},
        ],
        "allow_extra": False,
    },
    "gen_all_sites.csv": {
        "columns": [
            {"name": "time"},
        ],
        "allow_extra": True,
    },
}

WIND_SCHEMAS = {
    "wind_sites.csv": {
        "columns": [
            {"name": "Site Name"},
            {"name": "Bus No."},
            {"name": "Zone"},
            {"name": "MW_Capacity"},
            {"name": "Power Class"},
            {"name": "Latitude"},
            {"name": "Longitude"},
            {"name": "Hub Height"},
            {"name": "Turbine Rating"},
        ],
        "allow_extra": True,
    },
    "w_power_curves.csv": {
        "columns": [
            {"name": "Start (m/s)"},
            {"name": "End (m/s)"},
        ],
        "allow_extra": True,
    },
    "windspeed_data.csv": {
        "columns": [
            {"name": "datetime"},
        ],
        "allow_extra": True,
    },
}

DOMAINS = {
    "system": {
        "dir": "System",
        "schemas": SYSTEM_SCHEMAS,
        "required": ["branch.csv", "bus.csv", "gen.csv", "load.csv", "storage.csv"],
        "optional": [],
    },
    "solar": {
        "dir": "Solar",
        "schemas": SOLAR_SCHEMAS,
        "required": ["solar_sites.csv"],
        "optional": ["gen_all_sites.csv"],
    },
    "wind": {
        "dir": "Wind",
        "schemas": WIND_SCHEMAS,
        "required": ["wind_sites.csv", "w_power_curves.csv"],
        "optional": ["windspeed_data.csv"],
    },
}


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def validate_file_columns(
    file_path: Path,
    schema: list[dict],
    allow_extra: bool = False,
) -> list[str]:
    """
    Validate that a CSV file contains the expected columns.

    Parameters
    ----------
    file_path : Path
        Path to the CSV file.
    schema : list[dict]
        Column specifications. Each dict must have a ``"name"`` key.
    allow_extra : bool
        If True, columns beyond the schema are tolerated (e.g. dynamically
        named bus / site columns). If False, every column must be listed
        in the schema.

    Returns
    -------
    list[str]
        Error messages. Empty when the file passes validation.
    """
    errors: list[str] = []
    file_path = Path(file_path)

    if not file_path.is_file():
        return errors

    expected = {col["name"] for col in schema if col.get("name")}

    try:
        df = pd.read_csv(file_path, nrows=1)
    except Exception as exc:
        errors.append(f"{file_path.name}: could not read CSV — {exc}")
        return errors

    actual = set(df.columns)

    missing = expected - actual
    for col in sorted(missing):
        errors.append(f"{file_path.name}: missing required column '{col}'")

    if not allow_extra:
        unexpected = actual - expected
        for col in sorted(unexpected):
            errors.append(f"{file_path.name}: unexpected column '{col}'")

    return errors


def validate_domain(data_dir: Path, domain: str) -> tuple[list[str], list[str]]:
    """
    Validate all files in a single domain.

    Checks directory existence, file existence, non-empty, and column names
    for every file defined in the domain (both required and optional).

    Parameters
    ----------
    data_dir : Path
        Root data directory (e.g. ``path/to/Data``).
    domain : str
        One of ``"system"``, ``"solar"``, or ``"wind"``.

    Returns
    -------
    tuple of (errors, warnings)
        Each is a list of human-readable messages. Empty list = no issues.
    """
    errors: list[str] = []
    warnings: list[str] = []
    data_dir = Path(data_dir)

    cfg = DOMAINS.get(domain)
    if cfg is None:
        errors.append(f"Unknown domain: {domain}")
        return errors, warnings

    subdir = data_dir / cfg["dir"]
    if not subdir.is_dir():
        errors.append(f"Missing directory: {cfg['dir']}/")
        return errors, warnings

    all_files = cfg["required"] + cfg["optional"]
    schemas = cfg["schemas"]

    for fname in all_files:
        fpath = subdir / fname
        is_required = fname in cfg["required"]

        if not fpath.is_file():
            msg = f"{fname}: file not found in {cfg['dir']}/"
            errors.append(msg) if is_required else warnings.append(msg)
            continue

        if fpath.stat().st_size == 0:
            msg = f"{fname}: file is empty (0 bytes)"
            errors.append(msg) if is_required else warnings.append(msg)
            continue

        try:
            df = pd.read_csv(fpath, nrows=1)
            if len(df) == 0:
                warnings.append(f"{fname}: has no data rows (header only)")
        except Exception as exc:
            errors.append(f"{fname}: could not be read — {exc}")
            continue

        if fname in schemas:
            sc = schemas[fname]
            col_errors = validate_file_columns(fpath, sc["columns"], sc["allow_extra"])
            errors.extend(col_errors)

    return errors, warnings


def check_file_structure(data_dir: Path) -> tuple[list[str], list[str]]:
    """
    Verify that the data directory has the expected subdirectories and files.

    Runs ``validate_domain`` for all three domains (system, solar, wind)
    and combines the results.

    Parameters
    ----------
    data_dir : Path
        Root data directory.

    Returns
    -------
    tuple of (errors, warnings)
    """
    all_errors: list[str] = []
    all_warnings: list[str] = []
    data_dir = Path(data_dir)

    if not data_dir.is_dir():
        all_errors.append(f"Data directory not found: {data_dir}")
        return all_errors, all_warnings

    for domain in DOMAINS:
        errs, warns = validate_domain(data_dir, domain)
        all_errors.extend(errs)
        all_warnings.extend(warns)

    return all_errors, all_warnings
