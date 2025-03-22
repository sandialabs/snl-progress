import sys
from PySide6.QtCore import Signal, QThread
class DataHandler:
    """Contains all data necessary for GUI/optimization"""
    def __init__(self) -> None:
        ##api vars
        self.input_api = None
        self.input_name = None
        self.input_email = None
        self.input_aff = None
        ##sys vars
        self.genbus = None
        self.ng = None
        self.pmax = None
        self.pmin = None
        self.FOR_gen = None
        self.MTTF_gen = None
        self.MTTR_gen = None
        self.gencost = None
        self.nl = None
        self.fb = None
        self.tb = None
        self.cap_trans = None
        self.MTTF_trans = None
        self.MTTR_trans = None
        self.bus_name = None
        self.bus_no = None
        self.nz = None
        self.load_all_regions = None
        self.essname = None
        self.essbus = None
        self.ness = None
        self.ess_pmax = None
        self.ess_pmin = None
        self.ess_duration = None
        self.ess_socmax = None
        self.ess_socmin = None
        self.ess_eff = None
        self.disch_cost = None
        self.ch_cost = None
        self.MTTF_ess = None
        self.MTTR_ess = None
        self.ess_units = None
        self.mu_tot = None
        self.lambda_tot = None
        self.cap_max = None
        self.cap_min = None
        ##solar vars
        self.solar_directory = None
        self.s_sites = None
        self.s_zone_no = None
        self.s_max = None
        self.s_profiles = None
        self.solar_prob = None
        ##wind vars
        self.wind_directory = None
        self.w_sites = None
        self.farm_name = None
        self.zone_no = None
        self.w_classes = None
        self.w_turbines = None
        self.r_cap = None
        self.p_class = None
        self.out_curve2 = None
        self.out_curve3 = None
        self.start_speed = None
        self.tr_mats = None

    def set_input_api(self, input_api):
        self.input_api = input_api

    def set_input_name(self, input_name):
        self.input_name = input_name

    def set_input_email(self, input_email):
        self.input_email = input_email

    def set_input_aff(self, input_aff):
        self.input_aff = input_aff

    def set_genbus(self, genbus):
        self.genbus = genbus

    def set_ng(self, ng):
        self.ng = ng

    def set_pmax(self, pmax):
        self.pmax = pmax

    def set_pmin(self, pmin):
        self.pmin = pmin

    def set_FOR_gen(self, FOR_gen):
        self.FOR_gen = FOR_gen

    def set_MTTF_gen(self, MTTF_gen):
        self.MTTF_gen = MTTF_gen

    def set_MTTR_gen(self, MTTR_gen):
        self.MTTR_gen = MTTR_gen

    def set_gencost(self, gencost):
        self.gencost = gencost

    def set_nl(self, nl):
        self.nl = nl

    def set_fb(self, fb):
        self.fb = fb

    def set_tb(self, tb):
        self.tb = tb

    def set_cap_trans(self, cap_trans):
        self.cap_trans = cap_trans

    def set_MTTF_trans(self, MTTF_trans):
        self.MTTF_trans = MTTF_trans

    def set_MTTR_trans(self, MTTR_trans):
        self.MTTR_trans = MTTR_trans

    def set_bus_name(self, bus_name):
        self.bus_name = bus_name

    def set_bus_no(self, bus_no):
        self.bus_no = bus_no

    def set_nz(self, nz):
        self.nz = nz

    def set_load_all_regions(self, load_all_regions):
        self.load_all_regions = load_all_regions

    def set_essname(self, essname):
        self.essname = essname

    def set_essbus(self, essbus):
        self.essbus = essbus

    def set_ness(self, ness):
        self.ness = ness

    def set_ess_pmax(self, ess_pmax):
        self.ess_pmax = ess_pmax

    def set_ess_pmin(self, ess_pmin):
        self.ess_pmin = ess_pmin

    def set_ess_duration(self, ess_duration):
        self.ess_duration = ess_duration

    def set_ess_socmax(self, ess_socmax):
        self.ess_socmax = ess_socmax

    def set_ess_socmin(self, ess_socmin):
        self.ess_socmin = ess_socmin

    def set_ess_eff(self, ess_eff):
        self.ess_eff = ess_eff

    def set_disch_cost(self, disch_cost):
        self.disch_cost = disch_cost

    def set_ch_cost(self, ch_cost):
        self.ch_cost = ch_cost

    def set_MTTF_ess(self, MTTF_ess):
        self.MTTF_ess = MTTF_ess

    def set_MTTR_ess(self, MTTR_ess):
        self.MTTR_ess = MTTR_ess

    def set_ess_units(self, ess_units):
        self.ess_units = ess_units

    def set_mu_tot(self, mu_tot):
        self.mu_tot = mu_tot

    def set_lambda_tot(self, lambda_tot):
        self.lambda_tot = lambda_tot

    def set_cap_max(self, cap_max):
        self.cap_max = cap_max

    def set_cap_min(self, cap_min):
        self.cap_min = cap_min

    def set_raut(self, raut):
        self.raut = raut

    def set_solar_directory(self, solar_directory):
        self.solar_directory = solar_directory

    def set_s_sites(self, s_sites):
        self.s_sites = s_sites

    def set_s_zone_no(self, s_zone_no):
        self.s_zone_no = s_zone_no

    def set_s_max(self, s_max):
        self.s_max = s_max

    def set_s_profiles(self, s_profiles):
        self.s_profiles = s_profiles

    def set_solar_prob(self, solar_prob):
        self.solar_prob = solar_prob

    def set_wind_directory(self, wind_directory):
        self.wind_directory = wind_directory

    def set_w_sites(self, w_sites):
        self.w_sites = w_sites

    def set_farm_name(self, farm_name):
        self.farm_name = farm_name

    def set_zone_no(self, zone_no):
        self.zone_no = zone_no

    def set_w_classes(self, w_classes):
        self.w_classes = w_classes

    def set_w_turbines(self, w_turbines):
        self.w_turbines = w_turbines

    def set_r_cap(self, r_cap):
        self.r_cap = r_cap

    def set_p_class(self, p_class):
        self.p_class = p_class

    def set_out_curve2(self, out_curve2):
        self.out_curve2 = out_curve2

    def set_out_curve3(self, out_curve3):
        self.out_curve3 = out_curve3

    def set_start_speed(self, start_speed):
        self.start_speed = start_speed

    def set_tr_mats(self, tr_mats):
        self.tr_mats = tr_mats


class WorkerThread(QThread):
    """
    A worker thread for running long-running methods in the background.

    Signals:
    - finished: Emitted when the thread finishes execution.
    - output_updated: Emitted when the output is updated.

    Methods:
    - __init__(self, method, *args): Initializes the worker thread with a method and its arguments.
    - run(self): Redirects stdout, runs the method, restores stdout, and emits the finished signal.
    """
    finished = Signal()
    output_updated = Signal(str)

    def __init__(self, method, *args):
        super().__init__()
        self.method = method
        self.args = args

    def run(self):
        # Redirect stdout to a buffer
        stdout_buffer = StdoutBuffer(self)
        sys.stdout = stdout_buffer

        # Execute the long-running method
        self.method(*self.args)

        # Restore stdout
        sys.stdout = sys.__stdout__

        # Emit the finished signal when the process completes
        self.finished.emit()

class StdoutBuffer:
    """
    A buffer for capturing and emitting stdout text.

    Methods:
    - __init__(self, worker_thread): Initializes the buffer with a worker thread.
    - write(self, text): Captures and emits text.
    - flush(self): No-op for compatibility.
    """
    def __init__(self, worker_thread):
        self.worker_thread = worker_thread
        self.buffer = ""

    def write(self, text):
        self.buffer += text
        lines = self.buffer.split("\n")
        for line in lines[:-1]:
            self.worker_thread.output_updated.emit(line)
        self.buffer = lines[-1]

    def flush(self):
        pass
