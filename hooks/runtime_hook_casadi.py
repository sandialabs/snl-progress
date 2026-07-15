import os
import sys

if sys.platform == "win32" and getattr(sys, "frozen", False):
    bundle_dir = sys._MEIPASS
    casadi_dir = os.path.join(bundle_dir, "casadi")

    if hasattr(os, "add_dll_directory"):
        os.add_dll_directory(bundle_dir)
        if os.path.isdir(casadi_dir):
            os.add_dll_directory(casadi_dir)

    path = os.environ.get("PATH", "")
    for d in [casadi_dir, bundle_dir]:
        if d not in path:
            path = d + os.pathsep + path
    os.environ["PATH"] = path

    if os.path.isdir(casadi_dir):
        os.environ["CASADIPATH"] = casadi_dir
