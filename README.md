# Integrated BESS Stochastic Model (Combined)

This repository presents an **integrated stochastic modeling framework** for simulating and optimizing the performance of **Battery Energy Storage Systems (BESS)** under uncertainty.

It merges multiple previously separate scripts into a **single, self-contained notebook**, resolving dependency issues and ensuring reproducibility.

---

## Project Overview

Energy storage systems (ESS) — particularly batteries — are increasingly important for **grid stability**, **renewable integration**, and **energy market participation**.

This project builds a **stochastic optimization model** that captures the uncertainty in:

* Energy prices
* Load variations
* Renewable generation patterns

and determines optimal BESS operation strategies to **maximize profit** or **minimize cost**.

---

## Motivation for Integration

Previously, the model was divided across multiple scripts:

* `Integrated_BESS_Stochastic_Model.py` – the main driver script
* `mystochastic.py` – supporting functions and utilities
* `Integrated_BESS_Stochastic_Model_(Combined).py` – combined experimental version

When running these separately, users often encountered:

```
ModuleNotFoundError: No module named 'mystochastic'
```

### Cause:

Python couldn’t locate the helper functions as they were not installed as a proper package or in the same module path.

### Solution:

To eliminate this error and simplify execution, all related modules have now been **combined into one unified notebook:**

> `Integrated BESS Stochastic Model (Combined).ipynb`

This integrated version ensures:

* No external module imports are needed from local scripts.
* Full compatibility in Jupyter or standalone environments.
* A clean and reproducible workflow for energy market modeling.

---

## Key Features

| Feature                               | Description                                                                        |
| ------------------------------------- | ---------------------------------------------------------------------------------- |
| **Stochastic Price Modeling**         | Simulates random energy price fluctuations using probabilistic methods.            |
| **Optimization Strategy**             | Determines optimal charge/discharge schedule for revenue maximization.             |
| **Integrated Notebook**               | Combines all helper and core functions into one file.                              |
| **Monte Carlo Simulation (Optional)** | Supports multi-scenario evaluation of stochastic behavior.                         |
| **Visualization**                     | Graphical output of price paths, battery state of charge (SOC), and profit trends. |

---

## Model Components

1. **Price Uncertainty Modeling**
   Randomized generation of price paths to simulate market variability (e.g., using normal or lognormal distributions).

2. **BESS Operational Constraints**

   * Power and energy capacity limits
   * Charge/discharge efficiency
   * State of Charge (SOC) boundaries

3. **Optimization Algorithm**

   * Evaluates multiple stochastic realizations
   * Calculates expected profit over horizon
   * Identifies optimal dispatch strategy

4. **Visualization Layer**

   * Price vs. SOC vs. Profit plots
   * Scenario comparison charts

---

## How to Run

### Option 1: Run the Combined Notebook

1. Clone the repository:

   ```bash
   git clone https://github.com/DataWithSyed/BESS-Stochastic-Model.git
   cd BESS-Stochastic-Model
   ```

2. Launch Jupyter Notebook:

   ```bash
   jupyter notebook "Integrated BESS Stochastic Model (Combined).ipynb"
   ```

### Option 2: (Advanced) Run the Modular Version

If you prefer using separate scripts:

* Ensure all `.py` files (`Integrated_BESS_Stochastic_Model.py`, `mystochastic.py`) are in the **same directory**.
* Do **not rename or move** them to avoid `ModuleNotFoundError`.
* You may add the following line to the main script to ensure Python finds the module:

  ```python
  import sys
  sys.path.append('.')
  ```

---

## Dependencies

* Python ≥ 3.10
* NumPy
* Pandas
* Matplotlib
* Random / SciPy (for stochastic generation, if applicable)

Install via:

```bash
pip install numpy pandas matplotlib scipy
```

---

## Analytical Insights

The stochastic BESS model provides insights into:

* Expected revenue under uncertain price trajectories.
* Optimal charge/discharge decisions for each scenario.
* Risk-adjusted profitability and operational robustness.

It is especially useful for **energy traders**, **system operators**, and **researchers** evaluating **energy arbitrage strategies** or **market participation policies**.

---

## Data Access and Usage Notes

> **Important:**
> No external market data is included for confidentiality reasons.
> Users may import their own datasets (from CSV files or databases).

When importing data from a **database**:

* Use SQL queries or APIs to pull time-series data.
* **Do not use** the CSV loading/preprocessing cells already included in the notebook.
* Ensure timestamps and price columns are correctly formatted before running the stochastic functions.

---

## Reliability and Analysis Context

### Why Reliability Analysis Matters

Reliability analysis ensures the **stochastic model produces consistent, unbiased, and robust results**.
It validates that variations in random seed, data noise, or distribution assumptions do not distort the underlying optimization outcomes.

### For Quantitative Studies:

* Use multiple random seeds for robustness testing.
* Evaluate sensitivity to key parameters (efficiency, capacity, price volatility).
* Aggregate multiple Monte Carlo runs to produce **expected value distributions** rather than single deterministic results.

---

## Outputs

* Energy price trajectories (stochastic simulations)
* Battery charge/discharge profiles
* Profit distributions and scenario summaries
* Visual comparison of deterministic vs. stochastic performance

---
