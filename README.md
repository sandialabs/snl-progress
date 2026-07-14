<p align="center">
  <img src = "progress/Images/logos/progress_bold_s.svg" width="1400" height="250" alt="API" />
</p>

# <ins>Pro</ins>babilistic <ins>G</ins>rid <ins>R</ins>eliability Analysis with <ins>E</ins>nergy <ins>S</ins>torage <ins>S</ins>ystems (ProGRESS)

Current release version: v2.0.0

Release date: 07/15/2026

## Table of Contents

- [Introduction](#intro)
- [Key Features of ProGRESS](#key-features)
- [Getting Started](#getting-started)
- [Sample Case Study](#sample-case-study)
- [Learn More](#learn-more)
- [Citing ProGRESS](#cite)
- [Contact](#contact)

## Introduction

<a id="intro"></a>

**Probabilistic Grid Reliability Analysis with Energy Storage Systems (ProGRESS)** is an open-source, Python-based software tool for assessing the resource adequacy of modern electric power systems with high penetrations of energy storage systems (ESS), variable energy resources (VER), and emerging large loads such as AI data centers. ProGRESS employs a Markov Chain Monte Carlo (MCMC) stochastic simulation engine to generate thousands of diverse operating scenarios that capture the uncertainty and variability of future power systems.

The tool includes detailed, state-of-the-art ESS models that represent charge-discharge behavior, state-of-charge (SOC) evolution, failures, repairs, and technology-specific degradation mechanisms, enabling realistic assessment of storage availability and performance over time. Multiple ESS operating modes are supported, including **reliability mode**, **economic dispatch mode**, and **market participation mode** through integration with the **QuESt PCM** tool, allowing users to evaluate storage performance under a variety of operational strategies.

ProGRESS also models the uncertainty associated with VERs by incorporating historical weather-driven generation data, enabling users to simulate thousands of diverse generation scenarios that reflect realistic operating conditions. Users can build custom power system models, download and integrate historical VER datasets through supported APIs, and perform comprehensive probabilistic reliability analyses. The software quantifies expected outage frequency, duration, and magnitude using industry-standard reliability metrics while also providing detailed reliability assessments at the **individual bus level**, enabling users to identify localized reliability risks and evaluate the impact of storage and generation resources across the network.

By combining advanced stochastic simulation, detailed component modeling, and flexible ESS operating strategies, ProGRESS enables planners, researchers, and system operators to evaluate reliability tradeoffs, assess the value of energy storage, and make informed decisions for the planning and operation of future electric grids.


[Back to Top](#top)


## Key Features of ProGRESS
<a id="key-features"></a>

- **Probabilistic resource-adequacy assessment**: Uses sequential Monte Carlo simulation to model stochastic failures and repairs of generators, transmission lines, and energy-storage systems. It calculates reliability metrics including LOLP, LOLH, LOLE, LOLF, EUE, EPNS, and mean outage duration.

- **Comprehensive energy-storage modeling**: Represents ESS charge/discharge behavior, state of charge, efficiency, operating limits, duration,
    component availability, failures, and repairs. It supports single-period reliability operation and multi-period economic dispatch, as well
    as chemistry-specific degradation models for LMO, LFP, NMC, and NCA batteries. Degradation can account for depth of discharge, state of
    charge, C-rate, cycling, and temperature using an optional [PyBaMM](https://pybamm.org/) thermal model.

- **Flexible power-system and optimization models**: Supports copper-sheet, zonal, and nodal network representations, enabling users to balance
    computational speed and transmission detail. Configurable optimization horizons support both reliability-focused operation and multi-
    period dispatch considering generation costs, renewable curtailment, storage scheduling, and load shedding.

- **Variable generation and uncertainty modeling**: Accepts user-provided variable generation data or downloads ERA5 meteorological data through the
    [Copernicus Climate Data Store](https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels?tab=overview). Solar generation is calculated using [pvlib](https://pvlib-python.readthedocs.io/en/stable/) and modeled stochastically with k-means clustering and month-specific probabilities. Wind generation uses configurable turbine power curves and transition-rate matrices.

- **Data-center load modeling**: Incorporates data-center demand into resource-adequacy studies using user-provided collections of load
    profiles. ProGRESS randomly selects a profile for each Monte Carlo sample, adds it to matching system load buses, and can aggregate bus-
    level data-center demand into zone-level profiles for zonal studies.

- **Production-cost-model integration**: Integrates with [QuESt PCM](https://github.com/sandialabs/quest_PCM) for detailed nodal day-ahead unit commitment and economic dispatch, including
    generator and transmission outages, renewable availability, storage constraints, ancillary services, and optional pricing calculations.

- **Detailed results and visualization**: Generates per-sample records for load curtailment, generator dispatch, transmission
    flows, ESS state of charge, and ESS capacity. Aggregate outputs include reliability indices, convergence plots, outage heat maps, and bus-
    level outage frequency and magnitude rankings. A built-in results browser can be used to preview CSV, Excel, PDF, PNG, text, JSON, and HTML results.

- **Accessible and scalable workflows**: Provides a desktop GUI for data preparation, validation, simulation configuration, execution, logging, and results review. Simulations can also run from the command line or across multiple MPI processes on high-performance computing systems.

- **Customizable and reproducible open-source platform**: Uses documented CSV schemas for custom grid, load, storage, solar, and wind datasets, with an [RTS-GMLC](https://github.com/GridMod/RTS-GMLC) example included. Its modular Python architecture supports research extensions, while timestamped result directories and saved configuration snapshots make runs easier to reproduce.

[Back to Top](#top)

## Getting started

<a id="getting-started"></a>

### Manual Installation Instructions

### Prerequisites

- Python (>= 3.11) installed on your system
- Git installed on your system

### Installing Python

1. Installers can be found at: https://www.python.org/downloads/release/python-3119/
2. Make sure to check the box "Add Python to PATH" at the bottom of the installer prompt.

### Installing Git

- Visit [git-scm.com](https://git-scm.com/) to download Git for your operating system.
- Follow the installation instructions provided on the website.

### Setting Up a Virtual Environment

1. Open Command Prompt on Windows or Terminal on macOS and Linux.
2. Install `virtualenv` (if not already installed):
   ```
   python -m pip install virtualenv
   ```
3. Create a virtual environment:
   ```
   cd <your_path>
   python -m virtualenv <env_name>
   ```
   Replace `<your_path>` with the path to the folder where you want to create the virtual environment.
4. Activate the virtual environment:
   - On Windows:
     ```
     cd <your_path>
     .\<env_name>\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source <env_name>/bin/activate
     ```

### Installing ProGRESS

1. Clone the Repository:

   ```bash
   git clone https://github.com/sandialabs/snl-progress.git
   ```

2. Navigate to the `snl_progress` Directory:

   ```bash
   cd <path_to_snl-progress>
   ```

3. Install Dependencies:
   ```bash
   python -m pip install -r requirements.txt
   ```

<a id="solver"></a>

### Solver Installation

Ensure an optimization solver is installed on your machine. Solvers to consider include:

**Open-source Solvers**

- [GLPK](https://www.gnu.org/software/glpk/)
- [Clp](https://github.com/coin-or/Clp)
- [HiGHs](https://highs.dev/#top)

**Commercial Solvers**

- [Gurobi](https://www.gurobi.com/)
- [Cplex](https://www.ibm.com/products/ilog-cplex-optimization-studio)

[Back to Top](#top)

## Sample Case Study

A test case is included with this tool. The test system is the [IEEE RTS-GMLC](https://ieeexplore.ieee.org/abstract/document/8753693), which is a modernized version of the [IEEE RTS-96](https://ieeexplore.ieee.org/abstract/document/780914). A zonal model of the test system is illustrated as follows:

<p align="center">
  <img src = "progress/Images/workflow/RTS_GMLC.png" width="600" height="500" alt="RTS" />
</p>

All test system data provided with the tool has been taken from the [RTS-GMLC GitHub repository](https://github.com/GridMod/RTS-GMLC).

## Learn More

For detailed documentation on data preparation, simulation workflows, and advanced features, visit the **[ProGRESS Wiki](https://github.com/sandialabs/snl-progress/wiki)**:

- **[Data Requirements](https://github.com/sandialabs/snl-progress/wiki/Data-Requirements)** — Directory structure, CSV schemas, and file formats for system, solar, and wind data.
- **[Workflow](https://github.com/sandialabs/snl-progress/wiki/Workflow)** — Step-by-step guides for the GUI, command-line, and HPC workflows.
- **[Additional Features](https://github.com/sandialabs/snl-progress/wiki/Additional-Features)** — Battery degradation, PCM integration, and multi-period optimization.

## Citing ProGRESS

<a id="cite"></a>

If you use ProGRESS in your research, please cite the following paper:

A. Bera, C. J. Newlun, A. Lopez, Y. -J. Pomeroy, T. Nguyen and R. Byrne, "Probabilistic Grid Reliability Analysis with Energy Storage System (ProGRESS): An Open-Source Tool for Assessing the Reliability of Power Systems," 2025 IEEE Electrical Energy Storage Applications and Technologies Conference (EESAT), Charlotte, NC, USA, 2025, pp. 1-5, doi: 10.1109/EESAT62935.2025.10891214.

Bibtex Entry:

@inproceedings{bera2025probabilistic, <br>
title={Probabilistic Grid Reliability Analysis with Energy Storage System (ProGRESS): An Open-Source Tool for Assessing the Reliability of Power Systems}, <br>
author={Bera, Atri and Newlun, Cody J and Lopez, Andres and Pomeroy, Yung-Jai and Nguyen, Tu and Byrne, Ray}, <br>
booktitle={2025 IEEE Electrical Energy Storage Applications and Technologies Conference (EESAT)}, <br>
pages={1--5}, <br>
year={2025}, <br>
organization={IEEE} <br>
}

## Acknowledgment

<a id="acknowledgement"></a>
The ProGRESS tool is developed and maintained by the [Energy Storage Analytics Group](https://energy.sandia.gov/programs/energy-storage/analytics/) at [Sandia National Laboratories](https://www.sandia.gov/). This material is based upon work supported by the **U.S. Department of Energy, Office of Electricity (OE), Energy Storage Division**.

**Project team:**

- Atri Bera
- Dilip Pandit
- Eriel Cabrera
- Andres Lopez
- Yung-Jai Pomeroy
- Cody Newlun
- Tu Nguyen


| <img src = "progress/Images/logos/SNL_logo.png" width="260" height="120" alt="SNL" /> | <img src = "progress/Images/logos/New_DOE_Logo_Color.png" width="300" height="100" alt="DOE" /> |
| ------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |

[Back to Top](#top)

## Contact

<a id="contact"></a>

For reporting bugs and other issues, please use the "Issues" feature of this repository. For more information regarding the tool and collaboration opportunities, please contact project developer: Atri Bera (`abera@sandia.gov`)
