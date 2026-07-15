import os
import sys

if sys.platform == "win32" and getattr(sys, "frozen", False):
    bundle_dir = os.path.dirname(sys.executable)
    if hasattr(os, "add_dll_directory"):
        os.add_dll_directory(bundle_dir)
    path = os.environ.get("PATH", "")
    if bundle_dir not in path:
        os.environ["PATH"] = bundle_dir + os.pathsep + path
