Progress Package
================

General Introduction
--------------------

Welcome to the **ProGRESS API** documentation. The modules here implement the
core functionality of the ProGRESS software tool, a Python-based resource adequacy
simulation environment focused on integrating and analyzing conventional generators,
energy storage systems (ESS), wind farms, and solar photovoltaic sites.

All modules are written in Python, with an object-oriented design. Together, they
provide functionality for:

- Parsing and managing system data (buses, branches, generators, storage).
- Downloading and processing solar and wind data.
- Clustering solar generation days.
- Creating and solving resource adequacy studies via a Monte Carlo Simulation framework.
- Plotting and visualizing results.

.. note::
   For a complete picture of how these modules interact, see the main project README 
   and the API reference within the documentation.


__main__.py
~~~~~~~~~~~

``__main__.py`` is the entry point for running the ProGRESS GUI. It sets up the PySide6
application, provides user interface elements (tabs for Solar, Wind, and System data),
and manages long-running tasks through worker threads.

**Overview**:

- Launches the GUI with PySide6.
- Defines a main window class and worker threads to handle background operations without blocking the UI.
- Coordinates data loading (system, wind, solar), parameter input, and simulation runs.


.. automodule:: progress
   :members:
   :undoc-members:
   :show-inheritance:
