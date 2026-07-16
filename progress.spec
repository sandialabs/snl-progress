# -*- mode: python ; coding: utf-8 -*-

import os
import sys
import shutil
import subprocess

from PyInstaller.utils.hooks import collect_submodules, collect_data_files, collect_all

_pyomo_top = [
    'pyomo.common', 'pyomo.core', 'pyomo.dae', 'pyomo.dataportal',
    'pyomo.duality', 'pyomo.environ', 'pyomo.gdp', 'pyomo.mpec',
    'pyomo.neos', 'pyomo.network', 'pyomo.repn',
    'pyomo.scripting', 'pyomo.util', 'pyomo.version',
]
pyomo_imports = []
for pkg in _pyomo_top:
    pyomo_imports.extend(collect_submodules(pkg))

_opt_pkgs = ['pyomo.opt.base', 'pyomo.opt.parallel', 'pyomo.opt.plugins',
             'pyomo.opt.problem', 'pyomo.opt.results', 'pyomo.opt.solver']
for pkg in _opt_pkgs:
    pyomo_imports.extend(collect_submodules(pkg))
pyomo_imports.append('pyomo.opt')

pyomo_imports.extend(collect_submodules('pyomo.solvers.plugins'))
pyomo_imports.extend(['pyomo.solvers', 'pyomo.solvers.amplfunc_merge', 'pyomo.solvers.mockmip'])

_pyomo_contrib = [
    'pyomo.contrib.appsi', 'pyomo.contrib.ampl_function_demo',
    'pyomo.contrib.community_detection', 'pyomo.contrib.cp',
    'pyomo.contrib.example', 'pyomo.contrib.fbbt', 'pyomo.contrib.fme',
    'pyomo.contrib.gdp_bounds', 'pyomo.contrib.gdpopt', 'pyomo.contrib.gjh',
    'pyomo.contrib.mcpp', 'pyomo.contrib.mindtpy', 'pyomo.contrib.multistart',
    'pyomo.contrib.preprocessing', 'pyomo.contrib.pynumero', 'pyomo.contrib.satsolver',
    'pyomo.contrib.simplification', 'pyomo.contrib.solver', 'pyomo.contrib.trustregion',
]
for pkg in _pyomo_contrib:
    pyomo_imports.extend(collect_submodules(pkg))
pyomo_imports.append('pyomo.contrib')
pvlib_data = collect_data_files('pvlib')
timezonefinder_data = collect_data_files('timezonefinder')
matplotlib_backends = collect_submodules('matplotlib.backends')

casadi_datas, casadi_binaries, casadi_hiddenimports = collect_all('casadi')
pybamm_datas, pybamm_binaries, pybamm_hiddenimports = collect_all('pybamm')
pybammsolvers_datas, pybammsolvers_binaries, pybammsolvers_hiddenimports = collect_all('pybammsolvers')

glpk_binaries = []
glpsol_path = shutil.which("glpsol")
if glpsol_path:
    glpk_binaries.append((glpsol_path, "glpk"))
    if sys.platform == "darwin":
        output = subprocess.check_output(["otool", "-L", glpsol_path], text=True)
        for line in output.splitlines()[1:]:
            lib = line.split()[0]
            if os.path.isfile(lib) and "/opt/homebrew" in lib:
                glpk_binaries.append((lib, "glpk"))
    elif sys.platform == "win32":
        glpk_dir = os.path.dirname(glpsol_path)
        for f in os.listdir(glpk_dir):
            if f.lower().endswith(".dll"):
                glpk_binaries.append((os.path.join(glpk_dir, f), "glpk"))

a = Analysis(
    ['progress/__main__.py'],
    pathex=[],
    binaries=casadi_binaries + pybamm_binaries + pybammsolvers_binaries + glpk_binaries,
    datas=[
        ('progress/resources', 'progress/resources'),
        ('progress/Images', 'progress/Images'),
        ('progress/Data', 'progress/Data'),
        ('progress/input.yaml', 'progress'),
        ('README.md', '.'),
    ] + pvlib_data + timezonefinder_data + casadi_datas + pybamm_datas + pybammsolvers_datas,
    hiddenimports=[
        'progress.resources_rc',
        'progress.ui.forms.main_window.ui_main_window',
        'progress.ui.forms.landing.ui_landing',
        'progress.ui.forms.solar.ui_solar',
        'progress.ui.forms.solar.ui_solar_results',
        'progress.ui.forms.wind.ui_wind',
        'progress.ui.forms.simulation.ui_simulation',
        'progress.ui.forms.simulation.ui_pcm_config',
        'progress.ui.forms.results.ui_results',
        'progress.ui.forms.about.ui_about',
        'progress.ui.forms.settings.ui_settings',
        'progress.ui.forms.log_window.ui_log_window',
        'progress.dpi',
        'progress.paths',
        'progress.mod_solar',
        'progress.mod_wind',
        'progress.mod_kmeans',
        'progress.mod_sysdata',
        'progress.mod_utilities',
        'progress.mod_matrices',
        'progress.mod_mcs_utils',
        'progress.mod_plot',
        'progress.mod_degradation',
        'progress.mod_pcm',
        'progress.mod_bus_statistics',
        'progress.utils.data_validator',
        'progress.ui.utils.data_handler',
        'progress.ui.utils.worker',
        'progress.ui.msgbox',
        'progress.services.logger',
        'ruamel.yaml',
        'cdsapi',
        'timezonefinder',
        'pvlib',
        'rex',
        'kneed',
        '_casadi',
        'casadi._casadi',
    ] + pyomo_imports + matplotlib_backends + casadi_hiddenimports + pybamm_hiddenimports + pybammsolvers_hiddenimports,
    hookspath=['hooks'],
    hooksconfig={},
    runtime_hooks=['hooks/runtime_hook_casadi.py'],
    excludes=[
        'tkinter',
    ],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='snl-progress',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[m for m in casadi_binaries + pybamm_binaries + pybammsolvers_binaries if m[1].endswith(('.dll', '.so', '.pyd'))],
    name='snl-progress',
)

app = BUNDLE(
    coll,
    name='snl-progress.app',
    icon=None,
    bundle_identifier='gov.snl.progress',
    info_plist={
        'CFBundleShortVersionString': '2.0.0',
        'NSHighResolutionCapable': True,
        'NSRequiresAquaSystemAppearance': False,
    },
)
