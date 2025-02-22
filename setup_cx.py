import toml
from cx_Freeze import setup, Executable

# Load the .toml file
with open('pyproject.toml', 'r') as f:
    config = toml.load(f)

# Extract relevant information from the .toml file
project_name = config['tool']['poetry']['name']
version = config['tool']['poetry']['version']
description = config['tool']['poetry']['description']

# Define the executables
executables = [
    Executable(
        script="progress/__main__.py",  # Entry point for the module
        target_name=project_name
    )
]

# Define the setup configuration
setup(
    name=project_name,
    version=version,
    description=description,
    executables=executables,
    options={
        'build_exe': {
            'packages': [
                'numpy', 'pyomo', 'pandas', 'mpi4py', 'matplotlib', 'openpyxl',
                'seaborn', 'sklearn', 'kneed', 'requests', 'pvlib', 'rex', 'PySide6',
                'plotly', 'kaleido'
            ],
            'include_files': [
                'README.md', 'LICENSE'
            ]
        }
    }
)
