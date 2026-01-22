# BESS-Performance-Task

# BESS Performance Analysis

## Overview

This repository contains a Python package for analyzing performance data from a utility-scale Battery Energy Storage System (BESS). The station consists of 72 inverters (~3.6 MW each), with two DC inputs per inverter. Each DC input may be connected to two or three BESS enclosures (battery containers) depending on the system configuration.

The objective of this project is to provide reproducible, modular, and well-documented tooling to:

* Calculate daily energy charged and discharged by each BESS enclosure

* Identify underperforming (outlier) enclosures

* Visualize discharge performance over time using a daily heatmap

Note: Raw data and configuration files are intentionally excluded from this repository in accordance with the assignment requirements.

---

## Repository Structure

```
bess-performance-task/
├── bess_performance/
│   ├── __init__.py
│   ├── calc_energy.py
│   ├── peek_data.py
│   ├── run_calc_energy.py
│   └── BESS_Performance_Analysis.ipynb
├── setup.py
├── README.md
├── LICENSE
└── .gitignore

```

---

## Functionality

The package implements the following functionality:

### 1. Daily Energy Calculations

* **Total daily energy charged** per BESS enclosure
* **Total daily energy discharged** per BESS enclosure

Energy is calculated by integrating power over time using the configured sampling interval.

### 2. Visualization

* A **heatmap** showing daily discharged energy (kWh) for all BESS enclosures over time
* Generated using `matplotlib` and `seaborn`

### 3. Outlier Detection

* Identification of the **top 5 BESS enclosures** with the lowest:

  * Energy charged
  * Energy discharged

Results are returned as tabular outputs suitable for further analysis or reporting.

---

## Configuration (Not Tracked)

All environment-specific settings (such as data paths and time resolution) are stored in a separate `config.py` file, which is **not included in this repository**.

Example `config.py`:

```python
from pathlib import Path

DATA_FOLDER = Path("/path/to/parquet/files")
INTERVAL_HOURS = 0.25  # 15-minute intervals
```

This file should be provided separately when running the analysis.

---

## Installation

Build the package locally:

```bash
python setup.py sdist bdist_wheel
```

Install the wheel:

```bash
pip install dist/bess_performance-0.1-py3-none-any.whl
```

---

## Running the Analysis

Once installed and configured:

```bash
python -m bess_performance.run_calc_energy
```

The script will:

1. Load parquet files from the configured data directory
2. Compute daily charge/discharge metrics
3. Generate summary tables and plots

---

## Development Notes

* Code follows PEP 8 conventions
* Modular design enables reuse in notebooks and pipelines
* Tested locally using parquet data (not committed)

---

## Jupyter Notebook

A companion Jupyter notebook is provided separately to walk through the full methodology step by step, including:

* Data loading
* Assumptions
* Calculations
* Visualizations
* Interpretation of results

---

## License

MIT License
