import sys
import importlib

m = importlib.import_module("progress.resources_rc")
sys.modules["resources_rc"] = m
