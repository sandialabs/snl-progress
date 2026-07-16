# ProGRESS v2.0.0 Release Notes

**Release date:** July 17, 2026

## Summary

ProGRESS v2.0.0 is a major update to the open-source probabilistic grid reliability analysis platform. This release expands the resource-adequacy engine with nodal modeling, multi-period optimization, chemistry-specific battery degradation, data-center load scenarios, and optional QuESt Production Cost Model (PCM) co-simulation.

The release also introduces a redesigned desktop application, richer result visualization, improved data validation, and more consistent execution across the GUI, command line, and high-performance computing environments.

## Highlights

- Redesigned graphical interface with guided workflows.
- Copper-sheet, zonal, and nodal power-system models.
- Single-period reliability operation and configurable multi-period economic dispatch.
- Chemistry-specific battery degradation for LMO, LFP, NMC, and NCA systems.
- ERA5 meteorological data downloads through the Copernicus Climate Data Store.
- Stochastic data-center load profiles for nodal, copper-sheet, and zonal studies.
- Optional QuESt PCM integration for detailed nodal production-cost simulation.
- Expanded reliability reports, sample-level CSV exports, outage heat maps, and bus-level outage summaries.

## Added

### Power-system and reliability modeling

- Added a full nodal network model alongside the existing copper-sheet and zonal models.
- Added single-period and multi-period optimization within the Monte Carlo simulation.
- Added configurable optimization horizons, including 24-hour day-ahead dispatch.
- Added detailed sample-level records for conventional generator output, transmission flow, variable generation, load curtailment, ESS dispatch, and ESS state of charge.
- Added bus-level outage analysis that ranks buses by outage hours, total unserved energy, and average outage magnitude.
- Added command-line options for selecting a configuration file and output directory:

  ```bash
  python -m progress.example_simulation \
      --config /path/to/input.yaml \
      --out /path/to/results
  ```

### Energy-storage modeling

- Added stress-factor-based battery degradation models for LMO, LFP, NMC, and NCA chemistries.
- Added rainflow cycle counting and degradation effects associated with depth of discharge, state of charge, C-rate, temperature, and elapsed operation.
- Added an optional PyBaMM thermal model for estimating battery temperature during degradation calculations.
- Added ESS capacity tracking so failure-related and degradation-related capacity losses can be reviewed together.
- Improved ESS failure handling in multi-period simulations.

### Data-center load modeling

- Added optional data-center demand to Monte Carlo samples.
- Added random selection from user-provided `profile_*.csv` load profiles.
- Added automatic aggregation of bus-level data-center profiles for zonal simulations.
- Added example data-center load profiles to the bundled dataset.

### Production Cost Model integration

- Added optional co-simulation with the QuESt PCM platform.
- Added a PCM configuration dialog for selecting the PCM Python environment, start date, solver, MIP gap, pricing calculations, and storage ancillary-service participation.
- Added export of stochastic generator, branch, load, and storage conditions to PCM inputs.
- Added support for day-ahead unit commitment, detailed nodal dispatch, reserves, storage operation, and optional pricing outputs through QuESt PCM.
- Added reserve time-series data used by the integrated PCM workflow.

### Desktop application

- Rebuilt the GUI with a simplified sidebar and guided page navigation.
- Added a simulation configuration page backed by round-trip YAML editing.
- Added a separate application log window for processing messages and simulation output.
- Added light and dark themes with operating-system theme detection.
- Added contextual help dialogs and styled cross-platform message boxes.
- Added improved Windows DPI scaling, sizing, fonts, icons, and logo rendering.

### Results and reproducibility

- Added a file-based results browser with previews for CSV, XLSX, PDF, PNG, TXT, JSON, and HTML/Plotly outputs.
- Added multi-sheet Excel preview support.
- Added timestamped result directories for GUI and command-line simulations.
- Added a sanitized configuration snapshot to each completed run.
- Added CSV exports for ESS state of charge.
- Moved aggregate plotting into the simulation workflow so GUI and command-line runs produce consistent reports.

### Validation, packaging, and maintenance

- Added reusable schema validation for input files.
- Added GUI validation messages for missing, empty, and incorrectly structured data files.
- Added Python 3.9-compatible type annotations.
- Added PyPI and GitHub release workflows.
- Standardized the distribution name as `snl-progress`.
- Added third-party license notices for newly introduced dependencies.

## Changed

- Replaced NSRDB and WIND Toolkit downloads with ERA5 data from the Copernicus Climate Data Store.
- Replaced the previous `progress/App` GUI layout with the new `progress/ui` package structure.
- Updated the bundled RTS-GMLC-derived datasets for the expanded workflows.
- Updated the input configuration with network-model, optimization, degradation, data-center load, and PCM settings.
- Updated result organization to use one timestamped directory per run and one subdirectory per Monte Carlo sample.
- Updated the application branding, landing page, logos, and icons.

## Fixed

- Fixed zonal load aggregation and all-region load handling.
- Fixed nodal plotting and outage heat-map generation.
- Fixed post-simulation plotting so reports are produced by both GUI and command-line runs.
- Fixed results-page navigation, styling, and preview behavior.
- Fixed application log handling across background workers.
- Fixed configuration persistence while preserving YAML comments and formatting.
- Fixed multiple Windows layout, scaling, dialog, and theme issues.
- Updated the `requests` dependency in response to a reported security issue.

## Upgrade Notes

- ProGRESS v2.0.0 supports Python 3.11 and greater. 
- Reinstall the dependencies for this release because some workflows introduce new packages.
- ERA5 downloads require a valid Copernicus Climate Data Store credential file at `~/.cdsapirc`. Existing NREL API credentials are no longer used by the data download workflow.
- Review the updated `progress/input.yaml` before reusing a configuration from v1.2.0.
- Review the current `progress/Data` templates before reusing older input files. Several schemas and generated data paths have changed.
- QuESt PCM is a separate installation and requires its own compatible Python environment and optimization solver.

## Known Limitations

- PCM co-simulation currently requires the nodal network model and a 24-hour optimization period. (Dilip check this)
- PCM and battery degradation cannot currently be enabled in the same simulation. (Dilip check this)
- PCM co-simulation is not supported by the MPI workflow. (Dilip check this)
- Convergence plots require multiple Monte Carlo samples and nonzero loss-of-load results.

## Assets

- Windows release archives include the packaged ProGRESS application and supporting data files.
- Source installations can launch the GUI with:

  ```bash
  python -m progress
  ```

- Command-line and MPI workflows remain available for local, remote-server, and HPC execution.
