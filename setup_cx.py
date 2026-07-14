import sys
import toml
from cx_Freeze import setup, Executable

sys.setrecursionlimit(sys.getrecursionlimit() * 5)

with open('pyproject.toml', 'r') as f:
    config = toml.load(f)

project_name = config['tool']['poetry']['name']
version = config['tool']['poetry']['version']
description = config['tool']['poetry']['description']

executables = [
    Executable(
        script="progress/__main__.py",
        target_name=project_name
    )
]

setup(
    name=project_name,
    version=version,
    description=description,
    executables=executables,
    options={
        'build_exe': {
            'packages': [
                'numpy', 'pyomo', 'pandas', 'matplotlib', 'openpyxl',
                'seaborn', 'sklearn', 'kneed', 'requests', 'pvlib', 'rex', 'PySide6',
                'shiboken6', 'plotly', 'kaleido', 'markdown', 'timezonefinder', 'cdsapi'
            ],
            'excludes': [
                'tkinter', 'test', 'unittest', 'email', 'http',
                'xml', 'pydoc', 'doctest', 'distutils',
            ],
            'bin_excludes': [
                'libqsqlodbc.dylib',
                'libiodbc.2.dylib',
            ],
            'include_files': [
                'README.md', 'LICENSE'
            ]
        }
    }
)
