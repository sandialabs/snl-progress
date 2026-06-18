from dataclasses import dataclass
from pathlib import Path
import numpy as np

@dataclass
class DataHandler:
    genbus: np.ndarray | None = None
    ng: int | None = None
    pmax: np.ndarray | None = None
    pmin: np.ndarray | None = None
    FOR_gen: np.ndarray | None = None
    MTTF_gen: np.ndarray | None = None
    MTTR_gen: np.ndarray | None = None
    gencost: np.ndarray | None = None
    genname: object | None = None
    nl: int | None = None
    fb: np.ndarray | None = None
    tb: np.ndarray | None = None
    cap_trans: np.ndarray | None = None
    MTTF_trans: np.ndarray | None = None
    MTTR_trans: np.ndarray | None = None
    branchname: object | None = None
    bus_name: object | None = None
    bus_no: np.ndarray | None = None
    nz: int | None = None
    load_all_regions: object | None = None
    essname: object | None = None
    essbus: np.ndarray | None = None
    ness: int | None = None
    ess_pmax: np.ndarray | None = None
    ess_pmin: np.ndarray | None = None
    ess_duration: np.ndarray | None = None
    ess_socmax: np.ndarray | None = None
    ess_socmin: np.ndarray | None = None
    ess_eff: np.ndarray | None = None
    disch_cost: np.ndarray | None = None
    ch_cost: np.ndarray | None = None
    MTTF_ess: np.ndarray | None = None
    MTTR_ess: np.ndarray | None = None
    ess_units: np.ndarray | None = None
    ess_chemistry: object | None = None
    mu_tot: np.ndarray | None = None
    lambda_tot: np.ndarray | None = None
    cap_max: dict | None = None
    cap_min: dict | None = None
    raut: object | None = None
    # solar fields
    solar_directory: Path | None = None
    s_sites: object | None = None
    s_zone_no: object | None = None
    s_max: np.ndarray | None = None
    s_profiles: object | None = None
    solar_prob: np.ndarray | None = None
    # wind fields
    wind_directory: Path | None = None
    w_sites: int | None = None
    farm_name: object | None = None
    zone_no: object | None = None
    w_classes: int | None = None
    w_turbines: int | None = None
    r_cap: object | None = None
    p_class: object | None = None
    out_curve2: np.ndarray | None = None
    out_curve3: np.ndarray | None = None
    start_speed: np.ndarray | None = None
    tr_mats: np.ndarray | None = None
