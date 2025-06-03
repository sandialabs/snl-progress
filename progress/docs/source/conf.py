import os
import sys
from unittest.mock import MagicMock

# conf.py

# List the names exactly as they are imported in your code.
autodoc_mock_imports = [
    # "mod_wind",
    "pyomo",
    "plotly",
    "pvlib",
    "rex",
    "mpi4py",
    "mpi4py.MPI",
    "pyomo.environ",
    "plotly.offline",
    "plotly.graph_objects",  # if needed
    "pvlib.location",
    "pvlib.system",
    "pvlib.modelchain",
    "PySide6.QtCore",
    "PySide6.QtGui",
    "PySide6",
    "sklearn",
    "kneed",
    "mod_sysdata",
    "mod_wind"
    
]


# Get the absolute path to the directory containing conf.py
current_dir = os.path.dirname(os.path.abspath(__file__))

# Get the project root directory
project_root = os.path.abspath(os.path.join(current_dir, '..', '..', '..'))

# Add the project root to sys.path
sys.path.insert(0, project_root)

print(f"Current directory: {current_dir}")
print(f"Project root: {project_root}")

# -- Project information -----------------------------------------------------
project = 'ProGRESS'
copyright = '2024, Atri Bera'
author = 'Atri Bera'
release = '1.0.0'

# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    "myst_parser",
]

templates_path = ['_templates']
exclude_patterns = []

# Optional: Configure autodoc options
autodoc_default_options = {
    'members': True,
    'undoc-members': True,
    'private-members': True,
    'show-inheritance': True,
}
html_theme_options = {
    'collapse_navigation': False,
    'navigation_depth': 4,
}
master_doc = 'index'

# -- Options for HTML output -------------------------------------------------
html_theme = 'alabaster'
# html_static_path = ['_static']
