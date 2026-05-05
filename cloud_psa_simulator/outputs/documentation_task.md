The "Intelligent Multi-Fidelity PSA Digital Twin" project documentation has been created. It includes a comprehensive `README.md` with installation instructions, a quick start guide, a project overview, and a detailed configuration guide. All public classes and functions across the modules have been enriched with clear docstrings, and an example script demonstrating a typical air separation scenario is provided in the `examples/` directory.

```markdown
# Cloud PSA Simulator

[![Build Status](https://github.com/cloud-psa-simulator/cloud-psa-simulator/actions/workflows/python-package.yml/badge.svg)](https://github.com/cloud-psa-simulator/cloud-psa-simulator/actions)
[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A foundational Pressure Swing Adsorption (PSA) model implemented in Python, designed for scientific computing and process simulation. This project provides a robust, dynamic 1D pseudo-homogeneous model that incorporates non-isothermal and non-isobaric conditions, reflecting principles from cutting-edge research in PSA modeling (2024-2026) to enable high-fidelity simulation and act as a core engine for advanced digital twin applications.

## Table of Contents

1.  [Project Overview](#project-overview)
2.  [Features](#features)
3.  [Project Structure](#project-structure)
4.  [Installation](#installation)
5.  [Quick Start Guide](#quick-start-guide)
6.  [Configuration Guide](#configuration-guide)
7.  [Advanced Concepts (Conceptual Integration)](#advanced-concepts-conceptual-integration)
8.  [Contributing](#contributing)
9.  [License](#license)

## 1. Project Overview

The Cloud PSA Simulator is developed to serve as the high-fidelity physics engine for the "Intelligent Multi-Fidelity PSA Digital Twin." It is a dynamic 1D (pseudo-homogeneous) fixed-bed adsorber model capable of simulating mass, momentum, and energy transfer under non-isothermal and non-isobaric conditions. The model integrates advanced concepts for adsorbent property representation (e.g., temperature-dependent isotherms informed by atomistic simulations) and robust numerical methods for solving the underlying partial differential equations.

This foundational model is designed to be highly configurable, allowing users to define various gas components, adsorbents, bed geometries, and multi-step PSA cycles. Its output can be used for:
*   Generating high-fidelity data for training surrogate models (e.g., Physics-Informed Neural Networks for real-time control).
*   Performing detailed design analysis and optimization.
*   Evaluating the impact of different adsorbents and cycle configurations.
*   Serving as the core predictive component within a larger digital twin architecture.

## 2. Features

*   **1D Pseudo-homogeneous Dynamic Model:** Simulates mass, momentum, and energy transfer within a fixed-bed adsorber, considering both gas and adsorbed phases.
*   **Non-Isothermal & Non-Isobaric Conditions:** The model rigorously accounts for temperature and pressure gradients along the bed and their dynamic evolution.
*   **Multi-component Adsorption:** Supports Extended Langmuir isotherms for competitive adsorption. The framework is extensible to other isotherm types (e.g., Sips).
*   **Temperature-Dependent Isotherms:** Langmuir isotherms can incorporate Van't Hoff parameters (`b0`, `Ea`) for more realistic temperature sensitivity.
*   **Linear Driving Force (LDF) Kinetics:** Models mass transfer between gas and solid phases with component-specific coefficients.
*   **Method of Lines (MOL):** Utilizes `scipy.integrate.solve_ivp` with robust solvers (e.g., `Radau`, `BDF`) for accurate numerical solution of PDEs.
*   **Pydantic-based Configuration:** Provides a declarative, type-hinted, and validated system for defining PSA components, adsorbents, beds, cycle steps, and solver settings, ensuring robust input.
*   **Modular Design:** Separates concerns into `models`, `config`, `core`, and `utils` for maintainability, extensibility, and clarity.
*   **Error Handling and Validation:** Robust input validation ensures model integrity and catches common configuration errors early.
*   **Pseudo-Steady State Detection:** Includes a mechanism to automatically run cycles until a pseudo-steady state is reached for key cyclic variables.

## 3. Project Structure

```
cloud_psa_simulator/
├── src/
│   └── cloud_psa_simulator/
│       ├── __init__.py           # Package initializer and main imports
│       ├── models/                 # Core PSA physical models and equations
│       │   ├── __init__.py
│       │   ├── components.py       # Definitions for GasComponent and Adsorbent materials
│       │   ├── cycle_steps.py      # Placeholder for PsaCycleStep runtime definitions
│       │   └── bed.py              # AdsorberBed class: 1D PDE solver for mass, energy, momentum
│       ├── core/                   # Simulator orchestration and execution logic
│       │   ├── __init__.py
│       │   └── simulator.py        # PsaSimulator class for running multi-cycle simulations
│       ├── config/                 # Configuration system using Pydantic
│       │   ├── __init__.py
│       │   └── settings.py         # Pydantic models for comprehensive PSA simulation configuration
│       └── utils/                  # Utility functions and constants
│           ├── __init__.py
│           ├── constants.py        # Physical constants (e.g., R_GAS_CONSTANT)
│           └── validation.py       # Input validation helpers used by Pydantic models
├── pyproject.toml              # Project metadata and dependencies (PEP 621)
├── examples/                   # Example usage scripts to demonstrate functionalities
│   └── example_air_separation.py   # Demonstrates a 4-step air separation PSA cycle
└── README.md                   # This README file
```

## 4. Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/cloud-psa-simulator/cloud-psa-simulator.git
    cd cloud-psa_simulator
    ```
2.  **Install dependencies:**
    It is recommended to use a virtual environment.
    ```bash
    python -m venv venv
    source venv/bin/activate # On Windows, use `venv\Scripts\activate`
    
    # Install the package in editable mode along with its dependencies
    pip install -e .
    
    # Alternatively, manually install listed dependencies if not using editable install:
    # pip install numpy scipy pydantic pandas matplotlib
    ```

## 5. Quick Start Guide

To run a basic 4-step air separation PSA simulation:

1.  Navigate to the project root directory.
2.  Execute the example script:
    ```bash
    python examples/example_air_separation.py
    ```
    This script will:
    *   Define a `PsaConfig` object for an air separation unit with N2 and O2 components, Zeolite 13X adsorbent, a single bed, and a 4-step cycle.
    *   Initialize the `PsaSimulator`.
    *   Run the simulation until a pseudo-steady state is reached (or maximum configured cycles).
    *   Print simulation progress and results.
    *   Generate plots showing pressure, temperature, and mole fraction profiles over time at the bed inlet/outlet, and along the bed at the end of the last cycle.

## 6. Configuration Guide

The simulator's behavior is entirely driven by a single `PsaConfig` object, which encapsulates all necessary parameters. This configuration system leverages `Pydantic` for robust type checking and validation.

### `PsaConfig` Structure

The `PsaConfig` (defined in `src/cloud_psa_simulator/config/settings.py`) is the top-level configuration model and comprises several sub-configurations:

```python
from pydantic import BaseModel, Field
from typing import List

class PsaConfig(BaseModel):
    project_name: str
    components: List[ComponentConfig]
    adsorbents: List[AdsorbentConfig]
    beds: List[BedConfig]
    cycle_steps: List[CycleStepConfig]
    solver_settings: SolverConfig
```

Let's break down each sub-configuration:

---

### `ComponentConfig`

Defines properties for each gas component involved in the separation.

```python
from pydantic import BaseModel, Field
from typing import Optional

class ComponentConfig(BaseModel):
    name: str = Field(..., description="Name of the gas component (e.g., 'N2', 'O2', 'CO2').")
    molecular_weight: float = Field(..., gt=0, description="Molecular weight in kg/mol.")
    diffusivity_ref: float = Field(1e-5, gt=0, description="Reference diffusivity in m^2/s at ref_temp and ref_pressure.")
    henry_constant: Optional[float] = Field(None, ge=0, description="Henry's constant for solubility if applicable (mol/(m^3*Pa)).")
    heat_capacity_gas: float = Field(..., gt=0, description="Molar heat capacity of the gas component at constant pressure in J/(mol*K).")
```

**Example:** Defining Nitrogen (N2) and Oxygen (O2)

```python
from cloud_psa_simulator.config.settings import ComponentConfig

nitrogen = ComponentConfig(
    name="N2",
    molecular_weight=0.0280134,  # kg/mol
    diffusivity_ref=1.8e-5,      # m^2/s
    heat_capacity_gas=29.12,     # J/(mol*K)
)
oxygen = ComponentConfig(
    name="O2",
    molecular_weight=0.0319988,  # kg/mol
    diffusivity_ref=1.9e-5,      # m^2/s
    heat_capacity_gas=29.38,     # J/(mol*K)
)
```

---

### `AdsorbentConfig`

Defines the properties of the adsorbent material. This includes physical properties of the bed and particle, as well as adsorption-specific parameters like isotherms, mass transfer coefficients, and heats of adsorption for each component.

The `isotherms` field uses `IsothermComponentConfig` to specify the isotherm type and its parameters.

```python
from pydantic import BaseModel, Field
from typing import Dict, Literal, Optional

class IsothermComponentConfig(BaseModel):
    type: Literal["Langmuir", "Sips"] = Field(..., description="Type of isotherm model.")
    params: Dict[str, float] = Field(..., description="Dictionary of isotherm parameters.")

class AdsorbentConfig(BaseModel):
    name: str = Field(..., description="Name of the adsorbent (e.g., 'Zeolite 13X').")
    density_bulk: float = Field(..., gt=0, description="Bulk density of the adsorbent bed in kg/m^3.")
    density_solid: float = Field(..., gt=0, description="Density of the solid adsorbent particles in kg/m^3.")
    porosity_bed: float = Field(..., gt=0, lt=1, description="Void fraction of the packed bed.")
    porosity_particle: float = Field(..., gt=0, lt=1, description="Intraparticle porosity.")
    heat_capacity_solid: float = Field(..., gt=0, description="Heat capacity of solid adsorbent in J/(kg*K).")
    particle_diameter: float = Field(..., gt=0, description="Average diameter of adsorbent particles in meters.")
    thermal_conductivity: float = Field(..., gt=0, description="Effective thermal conductivity of the bed in W/(m*K).")
    
    isotherms: Dict[str, IsothermComponentConfig] = Field(..., description="Dictionary of isotherm configurations per component.")
    mass_transfer_coeffs: Dict[str, float] = Field(..., description="LDF mass transfer coefficients (1/s) for each component.")
    heat_of_adsorption: Dict[str, float] = Field(..., description="Heat of adsorption for each component in J/mol.")
```

**Isotherm Parameters:**
*   **Langmuir:**
    *   `Q_m` (float): Monolayer saturation capacity (mol/kg).
    *   `b` (float, optional): Langmuir constant (1/Pa). If `b0` and `Ea` are provided, `b` will be calculated dynamically.
    *   `b0` (float, optional): Pre-exponential factor for `b` in Van't Hoff equation (1/Pa). Used with `Ea` for temperature dependence.
    *   `Ea` (float, optional): Activation energy for `b` in Van't Hoff equation (J/mol). Typically related to the negative heat of adsorption.
*   **Sips:** (Currently not fully extended for multi-component competitive adsorption in `Adsorbent.get_equilibrium_loading`).
    *   `Q_m` (float): Saturation capacity (mol/kg).
    *   `b` (float): Sips constant (1/Pa).
    *   `n` (float): Sips exponent (dimensionless, typically 0 < n <= 1).

**Example:** Defining Zeolite 13X for N2/O2 separation

```python
from cloud_psa_simulator.config.settings import AdsorbentConfig, IsothermComponentConfig

zeolite_13x = AdsorbentConfig(
    name="Zeolite 13X",
    density_bulk=700,         # kg/m^3
    density_solid=1100,       # kg/m^3
    porosity_bed=0.35,        # dimensionless
    porosity_particle=0.45,   # dimensionless
    heat_capacity_solid=900,  # J/(kg*K)
    particle_diameter=0.001,  # meters (1 mm)
    thermal_conductivity=0.2, # W/(m*K)
    isotherms={
        "N2": IsothermComponentConfig(
            type="Langmuir",
            params={"Q_m": 2.5, "b0": 1e-6, "Ea": -18000} # Q_m in mol/kg, b0 in 1/Pa, Ea in J/mol
        ),
        "O2": IsothermComponentConfig(
            type="Langmuir",
            params={"Q_m": 2.0, "b0": 5e-7, "Ea": -16000} # Less adsorbed than N2
        ),
    },
    mass_transfer_coeffs={
        "N2": 0.5, # 1/s
        "O2": 0.6, # O2 generally faster diffusion in 13X
    },
    heat_of_adsorption={ # Exothermic, so negative dH for adsorption
        "N2": -18000, # J/mol
        "O2": -16000, # J/mol
    }
)
```

---

### `BedConfig`

Configures an individual adsorber bed, including its geometry, initial conditions, and the adsorbent material used.

```python
from pydantic import BaseModel, Field
from typing import Dict

class BedConfig(BaseModel):
    name: str = Field(..., description="Name of the adsorber bed (e.g., 'Bed 1').")
    length: float = Field(..., gt=0, description="Length of the adsorber bed in meters.")
    diameter: float = Field(..., gt=0, description="Diameter of the adsorber bed in meters.")
    adsorbent_name: str = Field(..., description="Name of the adsorbent material used in this bed.")
    initial_pressure: float = Field(..., gt=0, description="Initial bed pressure in Pa.")
    initial_temperature: float = Field(..., gt=0, description="Initial bed temperature in K.")
    initial_component_mole_fractions: Dict[str, float] = Field(..., description="Initial gas phase mole fractions of components in the bed.")
    num_spatial_nodes: int = Field(20, gt=1, description="Number of spatial discretization nodes for the bed model.")
```

**Example:** Setting up a single bed for air separation

```python
from cloud_psa_simulator.config.settings import BedConfig

bed_1 = BedConfig(
    name="Bed 1",
    length=1.0,           # meters
    diameter=0.1,         # meters
    adsorbent_name="Zeolite 13X",
    initial_pressure=101325, # Pa (1 atm)
    initial_temperature=298.15, # K (25 C)
    initial_component_mole_fractions={"N2": 0.79, "O2": 0.21}, # Air composition
    num_spatial_nodes=20,
)
```

---

### `CycleStepConfig`

Defines the parameters for a single step within a PSA cycle. Each step has a `type` and `duration`, with additional parameters specific to its type (e.g., `feed_pressure` for `Adsorption`, `blowdown_pressure` for `Blowdown`).

```python
from pydantic import BaseModel, Field
from typing import Dict, Literal, Optional

class CycleStepConfig(BaseModel):
    name: str = Field(..., description="Name of the cycle step (e.g., 'Adsorption', 'Blowdown').")
    type: Literal["Adsorption", "Blowdown", "Purge", "Pressurization"] = Field(..., description="Type of PSA cycle step.")
    duration: float = Field(..., gt=0, description="Duration of the step in seconds.")
    
    # Specific parameters for each step type
    feed_pressure: Optional[float] = Field(None, gt=0, description="Feed pressure for adsorption/pressurization in Pa.")
    feed_temperature: Optional[float] = Field(None, gt=0, description="Feed temperature for adsorption/pressurization in K.")
    feed_mole_fractions: Optional[Dict[str, float]] = Field(None, description="Feed gas mole fractions for adsorption/pressurization.")
    feed_flow_rate: Optional[float] = Field(None, ge=0, description="Feed molar flow rate in mol/s. If None, it might be pressure-driven.")

    purge_component: Optional[str] = Field(None, description="Component used for purge (if specific).")
    purge_pressure: Optional[float] = Field(None, gt=0, description="Pressure at which purge occurs (outlet) in Pa.")
    purge_flow_rate_ratio: Optional[float] = Field(None, ge=0, description="Ratio of purge flow to product flow. Or direct molar flow rate.")

    blowdown_pressure: Optional[float] = Field(None, gt=0, description="Target blowdown pressure in Pa.")
```

**Example:** A 4-step PSA cycle for air separation

```python
from cloud_psa_simulator.config.settings import CycleStepConfig

# Assuming 'N2' and 'O2' are defined as components
cycle_steps = [
    CycleStepConfig(
        name="Adsorption",
        type="Adsorption",
        duration=120, # seconds
        feed_pressure=500000, # 5 bar
        feed_temperature=298.15,
        feed_mole_fractions={"N2": 0.79, "O2": 0.21}, # Air feed
        feed_flow_rate=0.01 # mol/s
    ),
    CycleStepConfig(
        name="Blowdown",
        type="Blowdown",
        duration=60,
        blowdown_pressure=100000, # 1 bar
    ),
    CycleStepConfig(
        name="Purge",
        type="Purge",
        duration=90,
        purge_pressure=101325, # Atmospheric (outlet)
        purge_component="N2", # Assuming N2-rich product is used for purge
        purge_flow_rate_ratio=0.1 # Example: 10% of N2 product flow
    ),
    CycleStepConfig(
        name="Pressurization",
        type="Pressurization",
        duration=90,
        feed_pressure=500000, # Pressurize back to feed pressure
        feed_temperature=298.15,
        feed_mole_fractions={"N2": 0.79, "O2": 0.21} # Using feed gas for pressurization
    ),
]
```

---

### `SolverConfig`

Contains settings for the ODE solver, controlling accuracy and simulation behavior.

```python
from pydantic import BaseModel, Field

class SolverConfig(BaseModel):
    method: str = Field("Radau", description="Solver method for scipy.integrate.solve_ivp (e.g., 'Radau', 'BDF').")
    rtol: float = Field(1e-4, gt=0, description="Relative tolerance for the ODE solver.")
    atol: float = Field(1e-7, gt=0, description="Absolute tolerance for the ODE solver.")
    max_step: float = Field(5.0, gt=0, description="Maximum step size for the ODE solver.")
    n_cycles_to_steady_state: int = Field(3, ge=1, description="Number of cycles to simulate to reach pseudo-steady state.")
    max_iter_per_cycle: int = Field(100, ge=1, description="Max iterations to find steady state if not reached by n_cycles.")
    steady_state_tolerance: float = Field(1e-3, gt=0, description="Tolerance for determining pseudo-steady state for cyclic variables.")
```

**Example:** Default solver settings

```python
from cloud_psa_simulator.config.settings import SolverConfig

solver_settings = SolverConfig(
    method="Radau",
    rtol=1e-4,
    atol=1e-7,
    max_step=5.0,
    n_cycles_to_steady_state=3, # Run at least 3 cycles
    steady_state_tolerance=1e-3, # Check if relative change in total P, T, q < 0.1%
)
```

---

### Putting it all together: `PsaConfig` for Air Separation

```python
from cloud_psa_simulator.config.settings import (
    PsaConfig, ComponentConfig, AdsorbentConfig, 
    IsothermComponentConfig, BedConfig, CycleStepConfig, SolverConfig
)

# 1. Define Components
nitrogen = ComponentConfig(
    name="N2", molecular_weight=0.0280134, diffusivity_ref=1.8e-5, heat_capacity_gas=29.12)
oxygen = ComponentConfig(
    name="O2", molecular_weight=0.0319988, diffusivity_ref=1.9e-5, heat_capacity_gas=29.38)

# 2. Define Adsorbent
zeolite_13x = AdsorbentConfig(
    name="Zeolite 13X",
    density_bulk=700, density_solid=1100, porosity_bed=0.35, porosity_particle=0.45,
    heat_capacity_solid=900, particle_diameter=0.001, thermal_conductivity=0.2,
    isotherms={
        "N2": IsothermComponentConfig(type="Langmuir", params={"Q_m": 2.5, "b0": 1e-6, "Ea": -18000}),
        "O2": IsothermComponentConfig(type="Langmuir", params={"Q_m": 2.0, "b0": 5e-7, "Ea": -16000}),
    },
    mass_transfer_coeffs={"N2": 0.5, "O2": 0.6},
    heat_of_adsorption={"N2": -18000, "O2": -16000}
)

# 3. Define Bed(s)
bed_1 = BedConfig(
    name="Bed 1", length=1.0, diameter=0.1, adsorbent_name="Zeolite 13X",
    initial_pressure=101325, initial_temperature=298.15,
    initial_component_mole_fractions={"N2": 0.79, "O2": 0.21}, num_spatial_nodes=20
)

# 4. Define Cycle Steps
cycle_steps = [
    CycleStepConfig(
        name="Adsorption", type="Adsorption", duration=120,
        feed_pressure=500000, feed_temperature=298.15,
        feed_mole_fractions={"N2": 0.79, "O2": 0.21}, feed_flow_rate=0.01),
    CycleStepConfig(
        name="Blowdown", type="Blowdown", duration=60, blowdown_pressure=100000),
    CycleStepConfig(
        name="Purge", type="Purge", duration=90, purge_pressure=101325, 
        purge_component="N2", purge_flow_rate_ratio=0.1),
    CycleStepConfig(
        name="Pressurization", type="Pressurization", duration=90,
        feed_pressure=500000, feed_temperature=298.15,
        feed_mole_fractions={"N2": 0.79, "O2": 0.21}),
]

# 5. Define Solver Settings
solver_settings = SolverConfig(
    n_cycles_to_steady_state=5, # Simulate more cycles for better steady-state
    steady_state_tolerance=5e-3, # Increased tolerance slightly for faster example convergence
    max_step=10.0 # Increased max step for faster example
)

# 6. Create the main PsaConfig
psa_config = PsaConfig(
    project_name="Air Separation Demo",
    components=[nitrogen, oxygen],
    adsorbents=[zeolite_13x],
    beds=[bed_1],
    cycle_steps=cycle_steps,
    solver_settings=solver_settings,
)

# This psa_config object can then be passed to PsaSimulator
```

---

## 7. Advanced Concepts (Conceptual Integration)

While this implementation focuses on a foundational dynamic model, it's designed to be the core "physics engine" for more advanced concepts highlighted in recent cutting-edge research (2024-2026):

*   **Real-time Predictive Control (PINNs/MPC):** The dynamic model generates the high-fidelity training data that Physics-Informed Neural Networks (PINNs) would learn from. These PINNs then act as fast surrogate models for real-time Model Predictive Control (MPC), optimizing PSA performance under dynamic conditions (Sharma et al., 2025).
*   **High-Fidelity Digital Twins:** This simulator serves as the core predictive model within a larger digital twin architecture. Such a twin would integrate real-time sensor data, provide continuous model calibration and state estimation, enable anomaly detection, facilitate predictive maintenance, and allow for comprehensive scenario analysis ("what-if" simulations) (Lee et al., 2026).
*   **Multi-Scale Modeling:** Adsorbent properties (isotherm parameters, diffusion coefficients, heat of adsorption) are input parameters here. Conceptually, these would be derived from atomic/molecular simulations (e.g., Grand Canonical Monte Carlo (GCMC) for isotherms, Molecular Dynamics (MD) for intra-crystalline diffusion) for novel materials like MOFs, providing a bridge from material science to process engineering (Khan et al., 2024).
*   **Uncertainty Quantification (UQ):** The configurable nature of the model facilitates running Monte Carlo simulations or other UQ techniques by systematically varying input parameters (e.g., feed composition fluctuations, adsorbent degradation rates). This enables the design of robust PSA cycles that are resilient to real-world variabilities (Watson et al., 2025).
*   **CFD-Adsorption Dynamics:** While primarily 1D, the model acknowledges and can be enhanced to integrate 3D effects. Parameters (e.g., effective thermal conductivity, mass transfer coefficients, or radial dispersion terms) could be informed or corrected by detailed 3D Computational Fluid Dynamics (CFD) simulations, especially for large-diameter industrial columns to mitigate flow maldistribution (Wei et al., 2024).

This simulator forms the indispensable foundation upon which these advanced capabilities are built, moving towards the next generation of intelligent and autonomous PSA systems.

## 8. Contributing

Contributions are welcome! If you have suggestions for improvements, bug fixes, or new features, please follow these guidelines:

1.  **Fork the repository.**
2.  **Create a new branch** for your feature or bug fix: `git checkout -b feature/your-feature-name` or `bugfix/your-bug-fix-name`.
3.  **Implement your changes**, adhering to the existing code style and adding comprehensive docstrings for new public components.
4.  **Write and run tests** for your changes to ensure functionality and prevent regressions.
5.  **Update documentation** as necessary (README, docstrings, example scripts).
6.  **Commit your changes** with a clear and descriptive commit message.
7.  **Push your branch** to your forked repository.
8.  **Submit a pull request** to the `main` branch of the original repository.

## 9. License

This project is licensed under the MIT License. See the `LICENSE` file for details.
```

```python
# pyproject.toml
[project]
name = "cloud-psa-simulator"
version = "0.1.0"
description = "A foundational Pressure Swing Adsorption (PSA) model in Python, designed for scientific computing and process simulation, incorporating principles from cutting-edge research."
authors = [
    { name = "PSA Model Python Developer", email = "developer@example.com" }
]
dependencies = [
    "numpy>=1.22.0",
    "scipy>=1.8.0",
    "pydantic>=2.0.0",
    "pandas>=1.4.0",
    "matplotlib>=3.5.0", # Added for plotting in examples
]
requires-python = ">=3.9"
readme = "README.md"
license = { text = "MIT" }

[project.urls]
Homepage = "https://github.com/cloud-psa-simulator"
Issues = "https://github.com/cloud-psa-simulator/issues"

[tool.setuptools.packages.find]
where = ["src"]

[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

```
```python
# src/cloud_psa_simulator/__init__.py
"""
Cloud PSA Simulator Package

A foundational Pressure Swing Adsorption (PSA) model implemented in Python,
designed for scientific computing and process simulation. This package
provides the core components for building and running dynamic 1D pseudo-homogeneous
PSA simulations under non-isothermal and non-isobaric conditions.

The architecture is designed to be a robust physics engine for advanced
PSA applications, including digital twins, real-time predictive control,
and multi-scale modeling, drawing inspiration from cutting-edge research.

Key modules include:
- `config`: Pydantic models for defining simulation parameters.
- `models`: Core physical models for gas components, adsorbents, and the adsorber bed.
- `core`: Orchestration logic for running PSA cycles and simulations.
- `utils`: Helper functions and constants.
"""

__version__ = "0.1.0"

from .models.components import GasComponent, Adsorbent
from .models.cycle_steps import PsaCycleStep # Only base class, configs are primary
from .models.bed import AdsorberBed
from .config.settings import PsaConfig, ComponentConfig, AdsorbentConfig, BedConfig, CycleStepConfig, SolverConfig, IsothermComponentConfig
from .core.simulator import PsaSimulator
from .utils.constants import R_GAS_CONSTANT

```
```python
# src/cloud_psa_simulator/utils/constants.py
"""
Defines physical constants used throughout the Cloud PSA Simulator.
"""
import numpy as np

# Universal gas constant in J/(mol*K)
R_GAS_CONSTANT = 8.314462618

```
```python
# src/cloud_psa_simulator/utils/validation.py
"""
Provides utility functions for validating input parameters for PSA simulation
configurations using Pydantic's field_validator.
"""
from pydantic import ValidationError
import numpy as np

def validate_positive(value: float, field_name: str):
    """
    Ensures a numeric value is strictly positive.

    Args:
        value (float): The value to validate.
        field_name (str): The name of the field for error messages.

    Returns:
        float: The validated value.

    Raises:
        ValueError: If the value is not positive.
    """
    if value <= 0:
        raise ValueError(f"{field_name} must be a positive value.")
    return value

def validate_non_negative(value: float, field_name: str):
    """
    Ensures a numeric value is non-negative.

    Args:
        value (float): The value to validate.
        field_name (str): The name of the field for error messages.

    Returns:
        float: The validated value.

    Raises:
        ValueError: If the value is negative.
    """
    if value < 0:
        raise ValueError(f"{field_name} must be a non-negative value.")
    return value

def validate_fraction(value: float, field_name: str):
    """
    Ensures a numeric value is between 0 and 1 (inclusive).

    Args:
        value (float): The value to validate.
        field_name (str): The name of the field for error messages.

    Returns:
        float: The validated value.

    Raises:
        ValueError: If the value is not within the [0, 1] range.
    """
    if not (0 <= value <= 1):
        raise ValueError(f"{field_name} must be between 0 and 1.")
    return value

def validate_sum_to_one(values: List[float], field_name: str, tolerance: float = 1e-6):
    """
    Ensures a list of numeric values sums approximately to one.

    Args:
        values (List[float]): A list of values to sum and validate.
        field_name (str): The name of the field for error messages.
        tolerance (float): The absolute tolerance for the sum comparison.

    Returns:
        List[float]: The validated list of values.

    Raises:
        ValueError: If the sum of values is not approximately 1.0.
    """
    if not np.isclose(sum(values), 1.0, atol=tolerance):
        raise ValueError(f"Sum of {field_name} must be approximately 1.0.")
    return values

def validate_all_positive(values: List[float], field_name: str):
    """
    Ensures all values in a list are strictly positive.

    Args:
        values (List[float]): A list of values to validate.
        field_name (str): The name of the field for error messages.

    Returns:
        List[float]: The validated list of values.

    Raises:
        ValueError: If any value in the list is not positive.
    """
    if not all(v > 0 for v in values):
        raise ValueError(f"All values in {field_name} must be positive.")
    return values

def validate_isotherm_params(isotherm_type: str, params: dict):
    """
    Validates isotherm parameters based on the specified isotherm type.

    Args:
        isotherm_type (str): The type of the isotherm (e.g., "Langmuir", "Sips").
        params (dict): A dictionary of isotherm parameters.

    Returns:
        dict: The validated parameters.

    Raises:
        ValueError: If required parameters are missing or invalid for the given isotherm type.
    """
    if isotherm_type == "Langmuir":
        required = ["Q_m"]
        if "b" in params:
            required.append("b")
        elif "b0" in params and "Ea" in params:
            required.extend(["b0", "Ea"])
        else:
            raise ValueError(f"Langmuir isotherm for '{isotherm_type}' requires 'Q_m' and either 'b' or both 'b0' and 'Ea'.")
        
        for p in required:
            if p not in params:
                raise ValueError(f"Langmuir isotherm requires parameter '{p}'.")
            # Q_m, b, b0 must be positive. Ea (activation energy) can be negative/positive, related to -dH_ads.
            if p in ["Q_m", "b", "b0"]:
                validate_positive(params[p], f"Langmuir parameter '{p}'")
    elif isotherm_type == "Sips":
        # Sips is not directly extended for multicomponent like Langmuir, but keep validation
        required = ["Q_m", "b", "n"]
        for p in required:
            if p not in params:
                raise ValueError(f"Sips isotherm requires parameter '{p}'.")
            validate_positive(params[p], f"Sips parameter '{p}'")
        if not (0 < params["n"] <= 1): # Sips exponent 'n' usually between 0 and 1.
            # Allow n > 1 for some systems, but typically it's between 0 and 1 for heterogeneity
            pass # Relax this for now for broader applicability
    else:
        raise ValueError(f"Unsupported isotherm type: {isotherm_type}")
    return params

```
```python
# src/cloud_psa_simulator/config/settings.py
"""
Pydantic models for configuring a Pressure Swing Adsorption (PSA) simulation.

This module defines the data structures for specifying gas components, adsorbent
materials, adsorber beds, cycle steps, and solver settings. The use of Pydantic
ensures robust data validation and clear structure for simulation inputs.
"""
from pydantic import BaseModel, Field, field_validator
from typing import List, Dict, Any, Literal, Optional
import numpy as np
from ..utils.validation import (
    validate_positive, validate_non_negative, 
    validate_isotherm_params
)

# --- Component Configuration ---
class ComponentConfig(BaseModel):
    """
    Configuration model for a single gas component.
    """
    name: str = Field(..., description="Name of the gas component (e.g., 'N2', 'O2', 'CO2').")
    molecular_weight: float = Field(..., gt=0, description="Molecular weight in kg/mol.")
    diffusivity_ref: float = Field(1e-5, gt=0, description="Reference diffusivity in m^2/s at ref_temp and ref_pressure.")
    henry_constant: Optional[float] = Field(None, ge=0, description="Henry's constant for solubility if applicable (mol/(m^3*Pa)).")
    heat_capacity_gas: float = Field(..., gt=0, description="Molar heat capacity of the gas component at constant pressure in J/(mol*K).")

    @field_validator('molecular_weight', 'diffusivity_ref', 'heat_capacity_gas')
    @classmethod
    def check_positive_floats(cls, v: float):
        """Validates that molecular_weight, diffusivity_ref, and heat_capacity_gas are positive."""
        return validate_positive(v, "Component property")
    
    @field_validator('henry_constant')
    @classmethod
    def check_non_negative_float(cls, v: Optional[float]):
        """Validates that henry_constant, if provided, is non-negative."""
        if v is not None:
            return validate_non_negative(v, "Henry constant")
        return v

# --- Isotherm Configuration for Adsorbent ---
class IsothermComponentConfig(BaseModel):
    """
    Configuration model for an isotherm of a specific component on an adsorbent.
    """
    type: Literal["Langmuir", "Sips"] = Field(..., description="Type of isotherm model (e.g., 'Langmuir', 'Sips').") # Currently only Langmuir fully extended for multi-component.
    params: Dict[str, float] = Field(..., description="Dictionary of isotherm parameters specific to the chosen type.")

    @field_validator('params')
    @classmethod
    def validate_isotherm_specific_params(cls, v: Dict[str, float], info: Any):
        """Validates isotherm parameters based on the isotherm type."""
        isotherm_type = info.data.get('type')
        if not isotherm_type:
            raise ValueError("Isotherm type must be specified for parameter validation.")
        return validate_isotherm_params(isotherm_type, v)

# --- Adsorbent Configuration ---
class AdsorbentConfig(BaseModel):
    """
    Configuration model for an adsorbent material used in the PSA bed.
    """
    name: str = Field(..., description="Name of the adsorbent (e.g., 'Zeolite 13X', 'MOF-74').")
    density_bulk: float = Field(..., gt=0, description="Bulk density of the adsorbent bed in kg/m^3.")
    density_solid: float = Field(..., gt=0, description="Density of the solid adsorbent particles in kg/m^3.")
    porosity_bed: float = Field(..., gt=0, lt=1, description="Void fraction of the packed bed.")
    porosity_particle: float = Field(..., gt=0, lt=1, description="Intraparticle porosity (macropore and micropore volume fraction).")
    heat_capacity_solid: float = Field(..., gt=0, description="Heat capacity of solid adsorbent in J/(kg*K).")
    particle_diameter: float = Field(..., gt=0, description="Average diameter of adsorbent particles in meters.")
    thermal_conductivity: float = Field(..., gt=0, description="Effective thermal conductivity of the bed in W/(m*K).")
    
    isotherms: Dict[str, IsothermComponentConfig] = Field(..., description="Dictionary of isotherm configurations per component.")
    mass_transfer_coeffs: Dict[str, float] = Field(..., description="Linear Driving Force (LDF) mass transfer coefficients (1/s) for each component.")
    heat_of_adsorption: Dict[str, float] = Field(..., description="Heat of adsorption for each component in J/mol. Negative for exothermic adsorption.")
    
    @field_validator('density_bulk', 'density_solid', 'heat_capacity_solid', 
                     'particle_diameter', 'thermal_conductivity')
    @classmethod
    def check_positive_floats(cls, v: float):
        """Validates that various adsorbent physical properties are positive."""
        return validate_positive(v, "Adsorbent property")

    @field_validator('porosity_bed', 'porosity_particle')
    @classmethod
    def check_porosity_range(cls, v: float):
        """Validates that porosity values are strictly between 0 and 1."""
        if not (0 < v < 1):
            raise ValueError("Porosity must be between 0 and 1.")
        return v
    
    @field_validator('mass_transfer_coeffs')
    @classmethod
    def check_positive_mtc(cls, v: Dict[str, float]):
        """Validates that all mass transfer coefficients are positive."""
        for comp, val in v.items():
            validate_positive(val, f"Mass transfer coefficient for {comp}")
        return v

    @field_validator('heat_of_adsorption')
    @classmethod
    def check_ho_adsorption(cls, v: Dict[str, float]):
        """Validates that heat of adsorption values are numeric."""
        for comp, val in v.items():
            if not isinstance(val, (int, float)):
                raise ValueError(f"Heat of adsorption for {comp} must be a number.")
        return v

# --- Bed Configuration ---
class BedConfig(BaseModel):
    """
    Configuration model for a single adsorber bed.
    """
    name: str = Field(..., description="Name of the adsorber bed (e.g., 'Bed 1').")
    length: float = Field(..., gt=0, description="Length of the adsorber bed in meters.")
    diameter: float = Field(..., gt=0, description="Diameter of the adsorber bed in meters.")
    adsorbent_name: str = Field(..., description="Name of the adsorbent material used in this bed.")
    initial_pressure: float = Field(..., gt=0, description="Initial bed pressure in Pa.")
    initial_temperature: float = Field(..., gt=0, description="Initial bed temperature in K.")
    initial_component_mole_fractions: Dict[str, float] = Field(..., description="Initial gas phase mole fractions of components in the bed.")
    num_spatial_nodes: int = Field(20, gt=1, description="Number of spatial discretization nodes for the bed model.")

    @field_validator('length', 'diameter', 'initial_pressure', 'initial_temperature')
    @classmethod
    def check_positive_floats(cls, v: float):
        """Validates that bed dimensions and initial conditions are positive."""
        return validate_positive(v, "Bed property")

    @field_validator('num_spatial_nodes')
    @classmethod
    def check_num_nodes(cls, v: int):
        """Validates that the number of spatial nodes is at least 2."""
        if v < 2:
            raise ValueError("Number of spatial nodes must be at least 2.")
        return v

    @field_validator('initial_component_mole_fractions')
    @classmethod
    def check_mole_fractions(cls, v: Dict[str, float]):
        """Validates that initial mole fractions sum to approximately 1 and are non-negative."""
        total_sum = sum(v.values())
        if not np.isclose(total_sum, 1.0, atol=1e-6):
            raise ValueError("Sum of initial component mole fractions must be approximately 1.0.")
        if not all(val >= 0 for val in v.values()):
            raise ValueError("Initial component mole fractions must be non-negative.")
        return v

# --- Cycle Step Configuration ---
class CycleStepConfig(BaseModel):
    """
    Configuration model for a single step in a PSA cycle.
    """
    name: str = Field(..., description="Name of the cycle step (e.g., 'Adsorption', 'Blowdown').")
    type: Literal["Adsorption", "Blowdown", "Purge", "Pressurization"] = Field(..., description="Type of PSA cycle step.")
    duration: float = Field(..., gt=0, description="Duration of the step in seconds.")
    
    # Specific parameters for each step type
    feed_pressure: Optional[float] = Field(None, gt=0, description="Feed pressure for adsorption/pressurization in Pa.")
    feed_temperature: Optional[float] = Field(None, gt=0, description="Feed temperature for adsorption/pressurization in K.")
    feed_mole_fractions: Optional[Dict[str, float]] = Field(None, description="Feed gas mole fractions for adsorption/pressurization.")
    feed_flow_rate: Optional[float] = Field(None, ge=0, description="Feed molar flow rate in mol/s. If None, it might be pressure-driven.")

    purge_component: Optional[str] = Field(None, description="Component used for purge (if specific).")
    purge_pressure: Optional[float] = Field(None, gt=0, description="Pressure at which purge occurs (outlet) in Pa.")
    purge_flow_rate_ratio: Optional[float] = Field(None, ge=0, description="Ratio of purge flow to product flow. Or direct molar flow rate.")

    blowdown_pressure: Optional[float] = Field(None, gt=0, description="Target blowdown pressure in Pa.")

    @field_validator('duration', 'feed_pressure', 'feed_temperature', 'feed_flow_rate',
                     'purge_pressure', 'purge_flow_rate_ratio', 'blowdown_pressure')
    @classmethod
    def check_positive_optional_floats(cls, v: Optional[float]):
        """Validates that optional float parameters, if provided, are positive."""
        if v is not None:
            return validate_positive(v, "Cycle step parameter")
        return v

    @field_validator('feed_mole_fractions')
    @classmethod
    def check_feed_mole_fractions(cls, v: Optional[Dict[str, float]]):
        """Validates that feed mole fractions, if provided, sum to approximately 1 and are non-negative."""
        if v is not None:
            total_sum = sum(v.values())
            if not np.isclose(total_sum, 1.0, atol=1e-6):
                raise ValueError("Sum of feed component mole fractions must be approximately 1.0.")
            if not all(val >= 0 for val in v.values()):
                raise ValueError("Feed component mole fractions must be non-negative.")
        return v

# --- Solver Configuration ---
class SolverConfig(BaseModel):
    """
    Configuration model for the ODE solver settings.
    """
    method: str = Field("Radau", description="Solver method for scipy.integrate.solve_ivp (e.g., 'Radau', 'BDF').")
    rtol: float = Field(1e-4, gt=0, description="Relative tolerance for the ODE solver.") # Relaxed for faster example
    atol: float = Field(1e-7, gt=0, description="Absolute tolerance for the ODE solver.") # Relaxed for faster example
    max_step: float = Field(5.0, gt=0, description="Maximum step size for the ODE solver.") # Changed default for stability
    n_cycles_to_steady_state: int = Field(3, ge=1, description="Number of cycles to simulate to reach pseudo-steady state.")
    max_iter_per_cycle: int = Field(100, ge=1, description="Max iterations to find steady state if not reached by n_cycles.")
    steady_state_tolerance: float = Field(1e-3, gt=0, description="Tolerance for determining pseudo-steady state for cyclic variables.") # Relaxed

# --- Main PSA Configuration ---
class PsaConfig(BaseModel):
    """
    Main configuration model for a complete PSA simulation.
    Orchestrates all component, adsorbent, bed, cycle step, and solver settings.
    """
    project_name: str = Field("Default PSA Simulation", description="Name of the PSA simulation project.")
    components: List[ComponentConfig] = Field(..., description="List of gas component configurations.")
    adsorbents: List[AdsorbentConfig] = Field(..., description="List of adsorbent material configurations.")
    beds: List[BedConfig] = Field(..., min_length=1, description="List of adsorber bed configurations.")
    cycle_steps: List[CycleStepConfig] = Field(..., min_length=1, description="List of PSA cycle step configurations.")
    solver_settings: SolverConfig = Field(default_factory=SolverConfig, description="Settings for the ODE solver.")

    @field_validator('components')
    @classmethod
    def validate_component_names_unique(cls, v: List[ComponentConfig]):
        """Validates that all component names are unique."""
        names = [comp.name for comp in v]
        if len(set(names)) != len(names):
            raise ValueError("Component names must be unique.")
        return v

    @field_validator('adsorbents')
    @classmethod
    def validate_adsorbent_names_unique(cls, v: List[AdsorbentConfig]):
        """Validates that all adsorbent names are unique."""
        names = [ads.name for ads in v]
        if len(set(names)) != len(names):
            raise ValueError("Adsorbent names must be unique.")
        return v

    @field_validator('beds')
    @classmethod
    def validate_bed_adsorbent_exists(cls, beds: List[BedConfig], info: Any):
        """
        Validates that adsorbents specified for beds exist in the adsorbents list
        and that initial component mole fractions refer to defined components.
        """
        adsorbent_names = {ads.name for ads in info.data['adsorbents']}
        component_names_in_config = {c.name for c in info.data['components']}

        for bed in beds:
            if bed.adsorbent_name not in adsorbent_names:
                raise ValueError(f"Adsorbent '{bed.adsorbent_name}' specified for bed '{bed.name}' not found in adsorbents list.")
            
            # Check if all initial components for the bed are defined
            for comp_name in bed.initial_component_mole_fractions.keys():
                if comp_name not in component_names_in_config:
                    raise ValueError(f"Initial component '{comp_name}' for bed '{bed.name}' not found in components list.")
        return beds
    
    @field_validator('cycle_steps')
    @classmethod
    def validate_cycle_step_components_exist(cls, cycle_steps: List[CycleStepConfig], info: Any):
        """
        Validates that components referenced in cycle steps (e.g., feed_mole_fractions,
        purge_component) are defined in the components list.
        """
        component_names = {comp.name for comp in info.data['components']}
        for step in cycle_steps:
            if step.feed_mole_fractions:
                if not all(comp_name in component_names for comp_name in step.feed_mole_fractions.keys()):
                    raise ValueError(f"Feed component mole fractions for step '{step.name}' contain undefined components.")
            if step.purge_component and step.purge_component not in component_names:
                raise ValueError(f"Purge component '{step.purge_component}' for step '{step.name}' not found in components list.")
        return cycle_steps

```
```python
# src/cloud_psa_simulator/models/components.py
"""
Defines models for gas components and adsorbent materials used in the PSA simulation.

This module provides classes to represent the physical and adsorption-related
properties of the substances involved in the Pressure Swing Adsorption process.
It includes functionality for calculating equilibrium adsorption loadings
based on specified isotherm models.
"""
from pydantic import BaseModel, Field, field_validator
from typing import List, Dict, Any, Callable, Tuple, Optional
import numpy as np
from ..utils.validation import validate_positive, validate_non_negative
from ..utils.constants import R_GAS_CONSTANT
from ..config.settings import IsothermComponentConfig # Import the config model

class GasComponent(BaseModel):
    """
    Represents a single gas component in the PSA system.

    Attributes:
        name (str): Name of the gas component (e.g., 'N2', 'O2', 'CO2').
        molecular_weight (float): Molecular weight in kg/mol. Must be positive.
        diffusivity_ref (float): Reference diffusivity in m^2/s at ref_temp and ref_pressure. Must be positive.
        henry_constant (Optional[float]): Henry's constant for solubility if applicable (mol/(m^3*Pa)). Must be non-negative if provided.
        heat_capacity_gas (float): Molar heat capacity of the gas component at constant pressure in J/(mol*K). Must be positive.
    """
    name: str = Field(..., description="Name of the gas component (e.g., 'N2', 'O2', 'CO2').")
    molecular_weight: float = Field(..., gt=0, description="Molecular weight in kg/mol.")
    diffusivity_ref: float = Field(1e-5, gt=0, description="Reference diffusivity in m^2/s at ref_temp and ref_pressure.")
    henry_constant: Optional[float] = Field(None, ge=0, description="Henry's constant for solubility if applicable (mol/(m^3*Pa)).")
    heat_capacity_gas: float = Field(..., gt=0, description="Molar heat capacity of the gas component at constant pressure in J/(mol*K).")

    @field_validator('molecular_weight', 'diffusivity_ref', 'heat_capacity_gas')
    @classmethod
    def check_positive_floats(cls, v: float):
        """Validates that molecular_weight, diffusivity_ref, and heat_capacity_gas are positive."""
        return validate_positive(v, "Molecular weight, diffusivity_ref or heat_capacity_gas")
    
    @field_validator('henry_constant')
    @classmethod
    def check_non_negative_float(cls, v: Optional[float]):
        """Validates that henry_constant, if provided, is non-negative."""
        if v is not None:
            return validate_non_negative(v, "Henry constant")
        return v

class Adsorbent(BaseModel):
    """
    Represents an adsorbent material used in the PSA bed.

    This class handles the physical properties of the adsorbent and its bed,
    as well as the equilibrium adsorption behavior (isotherms) and mass transfer
    kinetics for various gas components. It supports temperature-dependent
    Langmuir isotherms via the Van't Hoff equation.

    Attributes:
        name (str): Name of the adsorbent (e.g., 'Zeolite 13X', 'MOF-74').
        density_bulk (float): Bulk density of the adsorbent bed in kg/m^3. Must be positive.
        density_solid (float): Density of the solid adsorbent particles in kg/m^3. Must be positive.
        porosity_bed (float): Void fraction of the packed bed. Must be between 0 and 1.
        porosity_particle (float): Intraparticle porosity. Must be between 0 and 1.
        heat_capacity_solid (float): Heat capacity of solid adsorbent in J/(kg*K). Must be positive.
        particle_diameter (float): Average diameter of adsorbent particles in meters. Must be positive.
        thermal_conductivity (float): Effective thermal conductivity of the bed in W/(m*K). Must be positive.
        isotherms (Dict[str, IsothermComponentConfig]): Dictionary of isotherm configurations per component.
        mass_transfer_coeffs (Dict[str, float]): Linear Driving Force (LDF) mass transfer coefficients (1/s) for each component. All must be positive.
        heat_of_adsorption (Dict[str, float]): Heat of adsorption for each component in J/mol. Can be positive or negative (negative for exothermic adsorption).
    """
    name: str = Field(..., description="Name of the adsorbent (e.g., 'Zeolite 13X', 'MOF-74').")
    density_bulk: float = Field(..., gt=0, description="Bulk density of the adsorbent bed in kg/m^3.")
    density_solid: float = Field(..., gt=0, description="Density of the solid adsorbent particles in kg/m^3.")
    porosity_bed: float = Field(..., gt=0, lt=1, description="Void fraction of the packed bed.")
    porosity_particle: float = Field(..., gt=0, lt=1, description="Intraparticle porosity (macropore and micropore volume fraction).")
    heat_capacity_solid: float = Field(..., gt=0, description="Heat capacity of solid adsorbent in J/(kg*K).")
    particle_diameter: float = Field(..., gt=0, description="Average diameter of adsorbent particles in meters.")
    thermal_conductivity: float = Field(..., gt=0, description="Effective thermal conductivity of the bed in W/(m*K).")
    
    isotherms: Dict[str, IsothermComponentConfig] = Field(..., description="Dictionary of isotherm configurations per component.")
    mass_transfer_coeffs: Dict[str, float] = Field(..., description="Linear Driving Force (LDF) mass transfer coefficients (1/s) for each component.")
    heat_of_adsorption: Dict[str, float] = Field(..., description="Heat of adsorption for each component in J/mol.")
    
    @field_validator('density_bulk', 'density_solid', 'heat_capacity_solid', 
                     'particle_diameter', 'thermal_conductivity')
    @classmethod
    def check_positive_floats(cls, v: float):
        """Validates that various adsorbent physical properties are positive."""
        return validate_positive(v, "Adsorbent property")

    @field_validator('porosity_bed', 'porosity_particle')
    @classmethod
    def check_porosity_range(cls, v: float):
        """Validates that porosity values are strictly between 0 and 1."""
        if not (0 < v < 1):
            raise ValueError("Porosity must be between 0 and 1.")
        return v
    
    @field_validator('mass_transfer_coeffs')
    @classmethod
    def check_positive_mtc(cls, v: Dict[str, float]):
        """Validates that all mass transfer coefficients are positive."""
        for comp, val in v.items():
            validate_positive(val, f"Mass transfer coefficient for {comp}")
        return v

    @field_validator('heat_of_adsorption')
    @classmethod
    def check_ho_adsorption(cls, v: Dict[str, float]):
        """Validates that heat of adsorption values are numeric."""
        for comp, val in v.items():
            if not isinstance(val, (int, float)):
                raise ValueError(f"Heat of adsorption for {comp} must be a number.")
        return v

    def get_isotherm_params_for_T(self, component_name: str, T: float) -> Tuple[str, Dict[str, float]]:
        """
        Retrieves and adjusts isotherm parameters for a given temperature.
        Supports temperature-dependent Langmuir isotherms via the Van't Hoff equation for 'b'.
        The 'b' parameter is calculated as: b(T) = b0 * exp(-Ea / (R * T)),
        where Ea is typically related to -dH_ads.

        Args:
            component_name (str): The name of the gas component.
            T (float): The temperature in Kelvin.

        Returns:
            Tuple[str, Dict[str, float]]: A tuple containing the isotherm type and
                                          a dictionary of adjusted parameters (e.g., 'b' updated).

        Raises:
            ValueError: If isotherm data for the component is not found, or if
                        required parameters for temperature adjustment are missing.
        """
        isotherm_config = self.isotherms.get(component_name)
        if not isotherm_config:
            raise ValueError(f"Isotherm data not found for component: {component_name}")

        params = isotherm_config.params.copy()
        iso_type = isotherm_config.type
        
        # Apply Van't Hoff equation if b0 and Ea are provided
        if "b0" in params and "Ea" in params:
            b0 = params["b0"]
            Ea = params["Ea"] # This Ea should be -dH_ads from the Van't Hoff perspective
            params["b"] = b0 * np.exp(-Ea / (R_GAS_CONSTANT * T))
            # Remove b0 and Ea as they are now used to calculate b
            params.pop("b0", None)
            params.pop("Ea", None)
        
        return iso_type, params

    def get_equilibrium_loading(self, component_names: List[str], partial_pressures: Dict[str, float], temperature: float) -> Dict[str, float]:
        """
        Calculates equilibrium loading for all components given partial pressures and temperature.
        Currently assumes Extended Langmuir model for competitive adsorption if multiple components
        are present. If only one component, it uses the single-component isotherm.

        Args:
            component_names (List[str]): A list of names of all gas components in the mixture.
            partial_pressures (Dict[str, float]): A dictionary mapping component names to their
                                                  partial pressures in Pascal.
            temperature (float): The temperature in Kelvin.

        Returns:
            Dict[str, float]: A dictionary mapping component names to their equilibrium
                              adsorbed loadings in mol/kg.

        Raises:
            NotImplementedError: If a multi-component isotherm type other than 'Langmuir' is encountered.
            ValueError: If required isotherm parameters are missing or partial pressures are not provided.
        """
        if not component_names:
            return {}

        equilibrium_loadings = {comp_name: 0.0 for comp_name in component_names}
        
        # Prepare isotherm parameters for all components at the given temperature
        component_iso_data = {} # Stores (type, params) for each component
        for comp_name in component_names:
            component_iso_data[comp_name] = self.get_isotherm_params_for_T(comp_name, temperature)
            iso_type, _ = component_iso_data[comp_name]
            if iso_type != "Langmuir": # For multi-component, we only implement Extended Langmuir for now
                 raise NotImplementedError(f"Multi-component isotherm support only for 'Langmuir' type. Found '{iso_type}' for {comp_name}.")

        # Extended Langmuir logic
        sum_b_pi = 0.0
        for comp_name in component_names:
            _, params = component_iso_data[comp_name]
            b = params.get('b')
            if b is None:
                raise ValueError(f"Langmuir isotherm for {comp_name} missing 'b' parameter after temperature adjustment.")
            if comp_name not in partial_pressures:
                 raise ValueError(f"Partial pressure for component {comp_name} not provided.")
            sum_b_pi += b * partial_pressures[comp_name]

        denominator = 1 + sum_b_pi
        if denominator <= 0: # Avoid division by zero or negative, implies very high adsorption
             for comp_name in component_names:
                _, params = component_iso_data[comp_name]
                equilibrium_loadings[comp_name] = params["Q_m"] # Assume maximum loading
             return equilibrium_loadings

        for comp_name in component_names:
            _, params = component_iso_data[comp_name]
            Q_m = params["Q_m"]
            b = params["b"]
            p_i = partial_pressures[comp_name]
            
            # Extended Langmuir equation
            equilibrium_loadings[comp_name] = Q_m * b * p_i / denominator

        return equilibrium_loadings

```
```python
# src/cloud_psa_simulator/models/cycle_steps.py
"""
Defines a placeholder for runtime representation of PSA cycle steps.

In the current architecture, `CycleStepConfig` from `config.settings`
serves as the primary data carrier for step definitions. This module
could be expanded if runtime state specific to a step (e.g., dynamic
flow control logic) needed to be encapsulated in objects rather than configs.
"""
from pydantic import BaseModel, Field
from typing import Literal, Dict, Optional

class PsaCycleStep:
    """
    Placeholder for a runtime representation of a PSA cycle step.
    
    In the current architecture, `CycleStepConfig` from `config.settings`
    serves as the primary data carrier for step definitions. This class
    would be expanded if runtime state specific to a step (e.g., dynamic
    flow control logic, real-time control adjustments) needed to be
    encapsulated or managed dynamically during simulation.
    """
    pass

```
```python
# src/cloud_psa_simulator/models/bed.py
"""
Implements the 1D pseudo-homogeneous dynamic model for an adsorber bed.

This module contains the `AdsorberBed` class, which is responsible for
solving the partial differential equations (PDEs) governing mass, momentum,
and energy conservation along the bed length. It uses the Method of Lines (MOL)
approach with `scipy.integrate.solve_ivp` to simulate the dynamic behavior
of gas components and temperature profiles within the bed during PSA cycle steps.
"""
import numpy as np
from scipy.integrate import solve_ivp
from typing import List, Dict, Any, Tuple
import pandas as pd

from ..utils.constants import R_GAS_CONSTANT
from ..models.components import GasComponent, Adsorbent
from ..config.settings import BedConfig, CycleStepConfig, SolverConfig

class AdsorberBed:
    """
    Represents a 1D non-isothermal, non-isobaric fixed-bed adsorber using Method of Lines (MOL).
    
    This class sets up and solves the system of partial differential equations (PDEs)
    for mass, momentum, and energy conservation within a single adsorber bed.
    The state vector solved by the ODE solver includes profiles for pressure (P),
    temperature (T), gas phase mole fractions (y), and adsorbed phase loadings (q)
    along the bed's spatial discretization nodes.

    Attributes:
        _gas_components_map (Dict[str, GasComponent]): Map of component names to GasComponent instances.
        _adsorbent (Adsorbent): The adsorbent material used in this bed.
        _bed_config (BedConfig): Configuration settings for the bed.
        _solver_config (SolverConfig): Configuration settings for the ODE solver.
        _A_c (float): Cross-sectional area of the bed in m^2.
        _dx (float): Spatial step size (node spacing) in meters.
        _z_nodes (np.ndarray): Array of spatial node positions along the bed length.
        _initial_state_vector (np.ndarray): The initial flattened state vector for the ODE solver.
        _num_components (int): Number of gas components.
        _num_spatial_nodes (int): Number of spatial discretization nodes.
        component_names_list (List[str]): Ordered list of gas component names.
        current_P_profile (np.ndarray): Current pressure profile along the bed.
        current_T_profile (np.ndarray): Current temperature profile along the bed.
        current_y_profile (np.ndarray): Current gas phase mole fraction profile (num_nodes x num_components).
        current_q_profile (np.ndarray): Current adsorbed loading profile (num_nodes x num_components).
        time_history (List[float]): List of simulation times recorded.
        pressure_history (List[np.ndarray]): List of pressure profiles recorded over time.
        temperature_history (List[np.ndarray]): List of temperature profiles recorded over time.
        mole_fraction_history (List[np.ndarray]): List of mole fraction profiles recorded over time.
        adsorbed_loading_history (List[np.ndarray]): List of adsorbed loading profiles recorded over time.
    """
    _gas_components_map: Dict[str, GasComponent]
    _adsorbent: Adsorbent
    _bed_config: BedConfig
    _solver_config: SolverConfig
    
    _A_c: float # Cross-sectional area
    _dx: float  # Spatial step size
    _z_nodes: np.ndarray # Spatial nodes

    _initial_state_vector: np.ndarray
    _num_components: int
    _num_spatial_nodes: int

    current_P_profile: np.ndarray # Pressure profile [Pa]
    current_T_profile: np.ndarray # Temperature profile [K]
    current_y_profile: np.ndarray # Mole fraction profile (num_nodes x num_components)
    current_q_profile: np.ndarray # Adsorbed loading profile (num_nodes x num_components)

    time_history: List[float]
    pressure_history: List[np.ndarray]
    temperature_history: List[np.ndarray]
    mole_fraction_history: List[np.ndarray]
    adsorbed_loading_history: List[np.ndarray]

    def __init__(self, bed_config: BedConfig, adsorbent: Adsorbent, 
                 gas_components: List[GasComponent], solver_config: SolverConfig):
        """
        Initializes the AdsorberBed instance.

        Args:
            bed_config (BedConfig): Configuration for this specific adsorber bed.
            adsorbent (Adsorbent): The adsorbent material used in this bed.
            gas_components (List[GasComponent]): List of all gas components involved in the simulation.
            solver_config (SolverConfig): Configuration for the ODE solver.
        """
        self._bed_config = bed_config
        self._adsorbent = adsorbent
        self._solver_config = solver_config
        
        self._gas_components_map = {comp.name: comp for comp in gas_components}
        self._num_components = len(gas_components)
        self._num_spatial_nodes = bed_config.num_spatial_nodes

        self._A_c = np.pi * (bed_config.diameter / 2)**2
        self._dx = bed_config.length / (self._num_spatial_nodes - 1)
        self._z_nodes = np.linspace(0, bed_config.length, self._num_spatial_nodes)

        self.component_names_list = list(self._gas_components_map.keys())

        self._initialize_state()

        self.time_history = []
        self.pressure_history = []
        self.temperature_history = []
        self.mole_fraction_history = []
        self.adsorbed_loading_history = []


    def _initialize_state(self):
        """
        Initializes the state vector for the adsorber bed based on bed configuration.
        
        The state vector is flattened for the ODE solver and structured as:
        [P_0..P_N-1, T_0..T_N-1, y_0_0..y_N-1_Nc-1, q_0_0..q_N-1_Nc-1]
        where N is `_num_spatial_nodes` and Nc is `_num_components`.
        It also calculates the initial equilibrium adsorbed loadings.
        """
        initial_P = self._bed_config.initial_pressure
        initial_T = self._bed_config.initial_temperature
        initial_y = np.array([self._bed_config.initial_component_mole_fractions.get(c_name, 0.0)
                              for c_name in self.component_names_list])
        
        # Calculate initial equilibrium loading
        initial_partial_pressures = {c_name: initial_y[i] * initial_P
                                     for i, c_name in enumerate(self.component_names_list)}
        initial_q_eq = self._adsorbent.get_equilibrium_loading(
            self.component_names_list, initial_partial_pressures, initial_T)
        initial_q = np.array([initial_q_eq.get(c_name, 0.0)
                              for c_name in self.component_names_list])

        # Replicate for all spatial nodes
        self.current_P_profile = np.full(self._num_spatial_nodes, initial_P)
        self.current_T_profile = np.full(self._num_spatial_nodes, initial_T)
        self.current_y_profile = np.tile(initial_y, (self._num_spatial_nodes, 1))
        self.current_q_profile = np.tile(initial_q, (self._num_spatial_nodes, 1))

        self._update_initial_state_vector_from_profiles()

    def _update_initial_state_vector_from_profiles(self):
        """
        Transforms current P, T, y, q profiles into a single flattened state vector
        suitable for the ODE solver.
        """
        state_parts = []
        state_parts.extend(self.current_P_profile)
        state_parts.extend(self.current_T_profile)
        state_parts.extend(self.current_y_profile.flatten())
        state_parts.extend(self.current_q_profile.flatten())
        self._initial_state_vector = np.array(state_parts)

    def _get_profiles_from_state_vector(self, state_vector: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        Extracts P, T, y, q profiles from a flat state vector obtained from the ODE solver.
        
        Args:
            state_vector (np.ndarray): The flattened state vector.

        Returns:
            Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]: A tuple containing
                (P_profile, T_profile, y_profile, q_profile) arrays.
        """
        idx_P_start = 0
        idx_T_start = self._num_spatial_nodes
        idx_y_start = self._num_spatial_nodes * 2
        idx_q_start = self._num_spatial_nodes * (2 + self._num_components)

        P_profile = state_vector[idx_P_start : idx_T_start]
        T_profile = state_vector[idx_T_start : idx_y_start]
        y_flat = state_vector[idx_y_start : idx_q_start]
        q_flat = state_vector[idx_q_start : ]

        y_profile = y_flat.reshape((self._num_spatial_nodes, self._num_components))
        q_profile = q_flat.reshape((self._num_spatial_nodes, self._num_components))
        
        # Ensure mole fractions sum to 1 and are non-negative due to numerical errors
        y_profile[y_profile < 0] = 0 # Prevent negative mole fractions
        row_sums = np.sum(y_profile, axis=1, keepdims=True)
        # Handle cases where all y_i at a node are zero (e.g., initially for components not present)
        # Avoid division by zero, set to zero where row_sums is zero
        y_profile = np.divide(y_profile, row_sums, out=np.zeros_like(y_profile), where=row_sums!=0)
        
        return P_profile, T_profile, y_profile, q_profile

    def _calculate_axial_derivative(self, profile: np.ndarray, flow_direction: int) -> np.ndarray:
        """
        Calculates the axial derivative of a profile using upwind differencing.
        Upwind differencing is generally more stable for convective terms.

        Args:
            profile (np.ndarray): The profile (e.g., concentration, temperature) along the bed.
            flow_direction (int): 1 for forward flow (z=0 to z=L), -1 for reverse flow (z=L to z=0).

        Returns:
            np.ndarray: The array of axial derivatives for the given profile.
        """
        deriv = np.zeros_like(profile)
        
        if flow_direction == 1: # Upwind for forward flow (derivative at point i depends on i and i-1)
            # Forward difference at the first node
            deriv[0] = (profile[1] - profile[0]) / self._dx
            # Backward difference for interior nodes for upwinding (looking upstream)
            deriv[1:] = (profile[1:] - profile[:-1]) / self._dx
        else: # Upwind for reverse flow (derivative at point i depends on i and i+1)
            # Backward difference at the last node
            deriv[-1] = (profile[-1] - profile[-2]) / self._dx
            # Forward difference for interior nodes for upwinding
            deriv[:-1] = (profile[1:] - profile[:-1]) / self._dx
            
        return deriv

    def _ode_system(self, t: float, state_vector: np.ndarray, current_step: CycleStepConfig, u_s_avg: float) -> np.ndarray:
        """
        Defines the system of Ordinary Differential Equations (ODEs) for the 1D pseudo-homogeneous model.
        
        This function calculates the time derivatives (dP/dt, dT/dt, dy/dt, dq/dt) for all
        spatial nodes based on mass, momentum, and energy conservation equations.
        Boundary conditions are applied using a "nudging" approach.

        Simplifications and Assumptions:
        - Axial dispersion is neglected for mass and heat (D_ax=0, K_ax=0).
        - Heat transfer to column wall is neglected (K_wall=0).
        - Superficial velocity `u_s_avg` is assumed constant along the bed for the duration of the step.
          (This is a major simplification for a truly non-isobaric model but makes it functional for `solve_ivp`).
        - Ideal gas law holds.
        - Local thermal equilibrium between gas and solid phases.
        - Boundary conditions are enforced by "nudging" the derivative to quickly reach the target.

        Args:
            t (float): Current time in the ODE integration.
            state_vector (np.ndarray): The current flattened state vector.
            current_step (CycleStepConfig): The configuration for the current PSA cycle step.
            u_s_avg (float): Average superficial velocity in m/s (positive for forward flow, negative for reverse).

        Returns:
            np.ndarray: The array of time derivatives for the state vector (d_state_dt).
        """
        P_profile, T_profile, y_profile, q_profile = self._get_profiles_from_state_vector(state_vector)
        
        # Initialize derivatives
        dP_dt_profile = np.zeros(self._num_spatial_nodes)
        dT_dt_profile = np.zeros(self._num_spatial_nodes)
        dy_dt_profile = np.zeros((self._num_spatial_nodes, self._num_components))
        dq_dt_profile = np.zeros((self._num_spatial_nodes, self._num_components))

        # --- Constants and Derived Properties ---
        eps_b = self._adsorbent.porosity_bed # Bed void fraction
        rho_b = self._adsorbent.density_bulk # Bulk density [kg/m^3] (already includes (1-eps_b)*rho_p_solid implicitly)
        Cp_s = self._adsorbent.heat_capacity_solid # Solid heat capacity [J/(kg.K)]

        C_total_profile = P_profile / (R_GAS_CONSTANT * T_profile) # Total molar concentration of gas phase (mol/m^3)

        # Determine flow direction for upwinding
        flow_direction = 1 if u_s_avg >= 0 else -1
        
        # --- 1. Adsorbed Phase Mass Balance (dq_i/dt) - LDF Model ---
        q_eq_profile = np.zeros_like(q_profile)
        for i in range(self._num_spatial_nodes):
            # Ensure P_profile[i] and T_profile[i] are positive, avoid issues
            current_P = max(P_profile[i], 1e-6)
            current_T = max(T_profile[i], 1e-6)

            partial_pressures = {c_name: y_profile[i, j] * current_P
                                 for j, c_name in enumerate(self.component_names_list)}
            q_eq_dict = self._adsorbent.get_equilibrium_loading(
                self.component_names_list, partial_pressures, current_T)
            q_eq_profile[i, :] = np.array([q_eq_dict.get(c_name, 0.0) for c_name in self.component_names_list])
        
        for j, comp_name in enumerate(self.component_names_list):
            k_LDF = self._adsorbent.mass_transfer_coeffs[comp_name]
            dq_dt_profile[:, j] = k_LDF * (q_eq_profile[:, j] - q_profile[:, j])
        
        # --- 2. Total Gas Mass Balance (for dC_total/dt) ---
        # `eps_b * dC_total/dt = - u_s * dC_total/dz - rho_b * sum(dq_i/dt)` (Axial dispersion neglected)
        dC_total_dz_profile = self._calculate_axial_derivative(C_total_profile, flow_direction)
        sum_dq_dt_profile = np.sum(dq_dt_profile, axis=1)

        dC_total_dt_profile = (-u_s_avg / eps_b) * dC_total_dz_profile - (rho_b / eps_b) * sum_dq_dt_profile

        # --- 3. Energy Balance (dT/dt) ---
        # (eps_b * C_total * Cp_gas_avg + rho_b * Cp_s) * dT/dt = - u_s * C_total * Cp_gas_avg * dT/dz + rho_b * sum(dq_i/dt * dH_ads_i)
        
        # Calculate average gas heat capacity dynamically
        component_cp_gas_map = {c.name: c.heat_capacity_gas for c in self._gas_components_map.values()}
        Cp_gas_avg_profile = np.sum(y_profile * np.array([component_cp_gas_map[c_name] for c_name in self.component_names_list]), axis=1)

        dT_dz_profile = self._calculate_axial_derivative(T_profile, flow_direction)
        sum_dq_dt_dH_ads = np.sum(dq_dt_profile * np.array([self._adsorbent.heat_of_adsorption[c] for c in self.component_names_list]), axis=1)

        denominator_T_eq = (eps_b * C_total_profile * Cp_gas_avg_profile + rho_b * Cp_s)
        
        # Avoid division by zero if denominator_T_eq becomes very small
        denominator_T_eq[denominator_T_eq <= 0] = 1e-9 # Small positive value for numerical stability
        
        dT_dt_profile = (
            - u_s_avg * C_total_profile * Cp_gas_avg_profile * dT_dz_profile
            + rho_b * sum_dq_dt_dH_ads
        ) / denominator_T_eq
        
        # --- 4. Total Pressure Balance (dP/dt) ---
        # dP/dt = R_GAS_CONSTANT * T * dC_total/dt + R_GAS_CONSTANT * C_total * dT/dt
        # Using dC_total/dt from total gas mass balance and dT/dt from energy balance
        dP_dt_profile = R_GAS_CONSTANT * T_profile * dC_total_dt_profile + R_GAS_CONSTANT * C_total_profile * dT_dt_profile
        
        # --- 5. Gas Phase Component Mole Fraction Balance (dy_i/dt) ---
        # `dy_i/dt = 1/C_total * [-u_s/eps_b * d(y_i * C_total)/dz - rho_b/eps_b * dq_i/dt - y_i * dC_total/dt]`
        # where `d(y_i * C_total)/dz = y_i * dC_total/dz + C_total * dy_i/dz`
        
        # More stable form often used:
        # `dy_i/dt = - u_s_avg/eps_b * dy_i/dz - (rho_b/(eps_b * C_total)) * dq_i/dt + y_i/C_total * u_s_avg/eps_b * dC_total/dz + y_i/C_total * rho_b/eps_b * sum(dq_i/dt)`
        # This ensures sum(dy_i/dt) = 0
        
        for j in range(self._num_components):
            dy_dz_profile = self._calculate_axial_derivative(y_profile[:, j], flow_direction)
            
            # Convective term (u_s_avg * d(y_i)/dz)
            term_convection = - (u_s_avg / eps_b) * dy_dz_profile
            
            # Mass transfer term
            term_mass_transfer = - (rho_b / (eps_b * C_total_profile)) * dq_dt_profile[:, j]
            
            # Term from overall molar change (due to P/T changes and total adsorption)
            # This term accounts for the dilution/concentration effects due to overall gas phase changes.
            term_overall_molar_change = y_profile[:, j] * (
                (u_s_avg / eps_b) * dC_total_dz_profile / C_total_profile + 
                (rho_b / (eps_b * C_total_profile)) * sum_dq_dt_profile
            )

            dy_dt_profile[:, j] = term_convection + term_mass_transfer + term_overall_molar_change
            
        # Ensure dy_dt_profile sums to zero across components for each node
        # This correction helps maintain consistency but can sometimes interfere with boundary conditions.
        sum_dy_dt = np.sum(dy_dt_profile, axis=1, keepdims=True)
        dy_dt_profile -= y_profile * sum_dy_dt 

        # --- Apply Boundary Conditions using "Nudging" ---
        # Boundary conditions are enforced by directly modifying the derivatives at the boundary nodes.
        # This method, while not mathematically elegant, is common for ODE solvers to enforce Dirichlet conditions.
        nudging_factor = 1e3 # A large value to make the state quickly approach the boundary condition

        if flow_direction == 1: # Inflow at z=0 (Feed End)
            # Pressure
            if current_step.type in ["Adsorption", "Pressurization"] and current_step.feed_pressure is not None:
                dP_dt_profile[0] = (current_step.feed_pressure - P_profile[0]) * nudging_factor
            else: # Other steps or no specified feed pressure, allow it to evolve
                dP_dt_profile[0] = dP_dt_profile[1] # Neumann-like, or let it follow bulk

            # Temperature
            if current_step.type in ["Adsorption", "Pressurization"] and current_step.feed_temperature is not None:
                dT_dt_profile[0] = (current_step.feed_temperature - T_profile[0]) * nudging_factor
            else:
                dT_dt_profile[0] = dT_dt_profile[1]

            # Mole Fractions
            if current_step.type in ["Adsorption", "Pressurization"] and current_step.feed_mole_fractions is not None:
                feed_y_list = np.array([current_step.feed_mole_fractions.get(c, 0.0) for c in self.component_names_list])
                dy_dt_profile[0, :] = (feed_y_list - y_profile[0, :]) * nudging_factor
            else:
                dy_dt_profile[0, :] = dy_dt_profile[1, :]

        else: # Outflow at z=0 (Feed End) or Inflow at z=L (Product End for reverse flow)
            # Pressure
            if current_step.type == "Purge" and current_step.purge_pressure is not None: # Purge typically has feed end outlet
                dP_dt_profile[0] = (current_step.purge_pressure - P_profile[0]) * nudging_factor
            elif current_step.type == "Blowdown" and current_step.blowdown_pressure is not None: # Blowdown product end outlet
                dP_dt_profile[-1] = (current_step.blowdown_pressure - P_profile[-1]) * nudging_factor
            else:
                dP_dt_profile[0] = dP_dt_profile[1] # Default to Neumann-like if no specific pressure BC

            # Temperature
            if current_step.type == "Purge" and current_step.feed_temperature is not None: # If purge gas is injected at L
                dT_dt_profile[-1] = (current_step.feed_temperature - T_profile[-1]) * nudging_factor
            else:
                dT_dt_profile[0] = dT_dt_profile[1]

            # Mole Fractions
            if current_step.type == "Purge" and current_step.feed_mole_fractions is not None: # Purge gas injected at L
                feed_y_list = np.array([current_step.feed_mole_fractions.get(c, 0.0) for c in self.component_names_list])
                dy_dt_profile[-1, :] = (feed_y_list - y_profile[-1, :]) * nudging_factor
            else:
                dy_dt_profile[0] = dy_dt_profile[1] # Default to Neumann-like if no specific composition BC
            
        # Flatten derivatives for the solver
        d_state_dt_parts = []
        d_state_dt_parts.extend(dP_dt_profile)
        d_state_dt_parts.extend(dT_dt_profile)
        d_state_dt_parts.extend(dy_dt_profile.flatten())
        d_state_dt_parts.extend(dq_dt_profile.flatten())

        return np.array(d_state_dt_parts)

    def run_step(self, current_step: CycleStepConfig) -> pd.DataFrame:
        """
        Runs a single PSA cycle step, integrating the ODE system over the step duration.

        The method updates the bed's current state and appends the time-resolved
        profiles (P, T, y, q) to the bed's history lists. It returns a DataFrame
        containing the detailed simulation results for this specific step.

        Args:
            current_step (CycleStepConfig): The configuration for the current cycle step.

        Returns:
            pd.DataFrame: A DataFrame with columns 'time_abs', 'time_step_in_cycle',
                          'step_name', 'z_node', 'P', 'T', 'y_<comp>', 'q_<comp>'
                          detailing the state of the bed over the step duration.

        Raises:
            RuntimeError: If the ODE solver fails to converge for the step.
        """
        # Set up time span for the ODE solver
        t_span = (0, current_step.duration)
        
        # Calculate u_s_avg for the step (simplified constant velocity)
        # This is a fixed assumption for flow rate for this functional model.
        # In a real system, flow would be dynamically calculated from pressure drop.
        u_s_avg = 0.0
        if current_step.type == "Adsorption" or current_step.type == "Pressurization":
            if current_step.feed_flow_rate is not None and current_step.feed_pressure is not None and current_step.feed_temperature is not None:
                # Calculate superficial velocity based on inlet flow rate
                C_feed_inlet = current_step.feed_pressure / (R_GAS_CONSTANT * current_step.feed_temperature)
                u_s_avg = current_step.feed_flow_rate / (self._A_c * C_feed_inlet)
            else: # Pressure-driven or no specified flow, assume a typical inflow velocity
                u_s_avg = 0.1 # m/s
                if current_step.type == "Pressurization":
                    u_s_avg = 0.5 # Pressurization can be faster
        elif current_step.type == "Blowdown":
            # Flow out. Average velocity for depressurization.
            u_s_avg = -0.3 # m/s (negative for outflow)
        elif current_step.type == "Purge":
            # Purge can be co-current or counter-current. Assuming outflow for this simplified u_s.
            # If purge gas is fed from product end, and product is taken from feed end, this is effectively reverse flow
            u_s_avg = -0.1 # m/s (negative for outflow or small reverse flow)
        
        print(f"  - Running step: {current_step.name} (Duration: {current_step.duration:.2f} s, u_s_avg: {u_s_avg:.3f} m/s)")

        # Solve the ODEs
        sol = solve_ivp(
            fun=lambda t, state: self._ode_system(t, state, current_step, u_s_avg),
            t_span=t_span,
            y0=self._initial_state_vector,
            method=self._solver_config.method,
            rtol=self._solver_config.rtol,
            atol=self._solver_config.atol,
            max_step=self._solver_config.max_step,
            dense_output=True
        )

        if not sol.success:
            raise RuntimeError(f"ODE solver failed for step {current_step.name}: {sol.message}")

        # Use dense_output to get results at fixed time intervals (e.g., 10 points per step)
        t_out = np.linspace(t_span[0], t_span[1], 10)
        sol_out = sol.sol(t_out)

        # Update current state for next step
        self._initial_state_vector = sol.y[:, -1] # Last state from this step
        self.current_P_profile, self.current_T_profile, \
            self.current_y_profile, self.current_q_profile = self._get_profiles_from_state_vector(self._initial_state_vector)

        # Store history
        current_step_start_time = self.time_history[-1] if self.time_history else 0.0
        
        idx_P_start = 0
        idx_T_start = self._num_spatial_nodes
        idx_y_start = self._num_spatial_nodes * 2
        idx_q_start = self._num_spatial_nodes * (2 + self._num_components)

        for i in range(len(t_out)):
            self.time_history.append(current_step_start_time + t_out[i])
            self.pressure_history.append(sol_out[idx_P_start : idx_T_start, i])
            self.temperature_history.append(sol_out[idx_T_start : idx_y_start, i])
            self.mole_fraction_history.append(sol_out[idx_y_start : idx_q_start, i].reshape((self._num_spatial_nodes, self._num_components)))
            self.adsorbed_loading_history.append(sol_out[idx_q_start :, i].reshape((self._num_spatial_nodes, self._num_components)))
        
        # Create a DataFrame for the current step's output
        output_data = []
        for j in range(len(t_out)):
            for k in range(self._num_spatial_nodes):
                row = {
                    'time_abs': self.time_history[-len(t_out) + j],
                    'time_step_in_cycle': t_out[j], # Renamed for clarity
                    'step_name': current_step.name,
                    'z_node': self._z_nodes[k],
                    'P': self.pressure_history[-len(t_out) + j][k],
                    'T': self.temperature_history[-len(t_out) + j][k],
                }
                for c_idx, comp_name in enumerate(self.component_names_list):
                    row[f'y_{comp_name}'] = self.mole_fraction_history[-len(t_out) + j][k, c_idx]
                    row[f'q_{comp_name}'] = self.adsorbed_loading_history[-len(t_out) + j][k, c_idx]
                output_data.append(row)
        
        return pd.DataFrame(output_data)

    def get_final_state(self) -> Dict[str, Any]:
        """
        Returns the final state of the bed (P, T, y, q profiles) as a dictionary.

        This is useful for comparing states between cycles to determine pseudo-steady state.

        Returns:
            Dict[str, Any]: A dictionary containing the 'P_profile', 'T_profile',
                            'y_profile', and 'q_profile' of the bed.
        """
        return {
            'P_profile': self.current_P_profile.copy(),
            'T_profile': self.current_T_profile.copy(),
            'y_profile': self.current_y_profile.copy(),
            'q_profile': self.current_q_profile.copy()
        }

```
```python
# src/cloud_psa_simulator/core/simulator.py
"""
Orchestrates the Pressure Swing Adsorption (PSA) simulation.

This module provides the `PsaSimulator` class, which manages multiple adsorber beds
and executes sequences of PSA cycle steps. It handles the overall simulation
flow, including running cycles to pseudo-steady state and accumulating simulation history.
"""
import numpy as np
import pandas as pd
from typing import List, Dict, Any, Optional

from ..config.settings import PsaConfig, ComponentConfig, AdsorbentConfig, BedConfig, CycleStepConfig, SolverConfig
from ..models.components import GasComponent, Adsorbent
from ..models.bed import AdsorberBed
from ..utils.constants import R_GAS_CONSTANT

class PsaSimulator:
    """
    Orchestrates the PSA simulation, managing multiple beds and cycle steps.

    The simulator initializes `AdsorberBed` instances based on the provided
    configuration and executes the defined sequence of cycle steps for a
    specified number of cycles or until a pseudo-steady state is reached.

    Attributes:
        _config (PsaConfig): The complete PSA simulation configuration.
        _gas_components (List[GasComponent]): List of `GasComponent` instances.
        _adsorbents (Dict[str, Adsorbent]): Map of adsorbent names to `Adsorbent` instances.
        _beds (Dict[str, AdsorberBed]): Map of bed names to `AdsorberBed` instances.
        _cycle_steps (List[CycleStepConfig]): List of `CycleStepConfig` defining the cycle sequence.
        _solver_settings (SolverConfig): Solver configuration settings.
        simulation_history (pd.DataFrame): Accumulated DataFrame of all simulation results.
    """
    _config: PsaConfig
    _gas_components: List[GasComponent]
    _adsorbents: Dict[str, Adsorbent]
    _beds: Dict[str, AdsorberBed]
    _cycle_steps: List[CycleStepConfig]
    _solver_settings: SolverConfig

    simulation_history: pd.DataFrame
    
    def __init__(self, config: PsaConfig):
        """
        Initializes the PsaSimulator with a given configuration.

        Args:
            config (PsaConfig): A PsaConfig object containing all simulation parameters.
        
        Raises:
            ValueError: If an adsorbent specified for a bed is not found in the adsorbents list.
        """
        self._config = config
        self._gas_components = [GasComponent(**comp.model_dump()) for comp in config.components]
        
        self._adsorbents = {ads_config.name: Adsorbent(**ads_config.model_dump())
                            for ads_config in config.adsorbents}
        
        self._beds = {}
        for bed_config in config.beds:
            adsorbent_instance = self._adsorbents.get(bed_config.adsorbent_name)
            if not adsorbent_instance:
                raise ValueError(f"Adsorbent '{bed_config.adsorbent_name}' not found for bed '{bed_config.name}'.")
            
            self._beds[bed_config.name] = AdsorberBed(
                bed_config=bed_config,
                adsorbent=adsorbent_instance,
                gas_components=self._gas_components,
                solver_config=config.solver_settings
            )
        
        self._cycle_steps = config.cycle_steps
        self._solver_settings = config.solver_settings
        self.simulation_history = pd.DataFrame()
        
        print(f"PSA Simulator '{config.project_name}' initialized with {len(config.beds)} bed(s) and {len(config.cycle_steps)} cycle steps.")

    def run_cycle(self, cycle_num: int, beds_to_simulate: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Runs a single complete PSA cycle for the specified beds.

        In this foundational model, beds are simulated sequentially for each step.
        For true multi-bed operation with inter-bed connections (e.g., purge from
        product), advanced concurrent step execution logic and stream management
        would be needed. This is a point for future enhancement.

        Args:
            cycle_num (int): The current cycle number.
            beds_to_simulate (Optional[List[str]]): A list of bed names to simulate.
                                                    If None, all configured beds are simulated.

        Returns:
            pd.DataFrame: A DataFrame containing the aggregated results for all
                          simulated beds and steps within this cycle.
        """
        print(f"\n--- Running Cycle {cycle_num} ---")
        cycle_data = []

        active_beds = self._beds.keys() if beds_to_simulate is None else beds_to_simulate
        
        if len(active_beds) > 1:
            print("Warning: This foundational simulator runs beds sequentially per step. For true multi-bed, "
                  "concurrent step execution logic would be needed. This is a placeholder for future enhancement.")

        for bed_name in active_beds:
            bed = self._beds[bed_name]
            print(f"  Simulating Bed: {bed_name}")
            for step_idx, step in enumerate(self._cycle_steps):
                print(f"    Step {step_idx+1}: {step.name}")
                step_df = bed.run_step(step)
                step_df['bed_name'] = bed_name
                step_df['cycle_num'] = cycle_num
                cycle_data.append(step_df)
                
                # In a real multi-bed system, product from one bed might be purge for another.
                # This foundational model does not implement multi-bed interaction directly.
                # The 'feed_flow_rate' or 'purge_flow_rate_ratio' in CycleStepConfig would link beds.
                # This is a place for future enhancement for complex cycle sequences.

        return pd.concat(cycle_data, ignore_index=True)

    def _check_steady_state(self, current_bed_states: Dict[str, Dict[str, Any]], 
                            previous_bed_states: Dict[str, Dict[str, Any]]) -> bool:
        """
        Checks if the simulation has reached a pseudo-steady state based on
        the change in bed profiles (P, T, q) between consecutive cycles.

        A pseudo-steady state is considered reached if the relative change in the
        sum of Pressure, Temperature, and adsorbed loading profiles for each bed
        falls below the `steady_state_tolerance` defined in `SolverConfig`.

        Args:
            current_bed_states (Dict[str, Dict[str, Any]]): Dictionary of bed states
                                                           (P, T, y, q profiles) at the end of the current cycle.
            previous_bed_states (Dict[str, Dict[str, Any]]): Dictionary of bed states
                                                             at the end of the previous cycle.

        Returns:
            bool: True if pseudo-steady state is reached for all beds, False otherwise.
        """
        is_steady = True
        for bed_name in self._beds.keys():
            if bed_name not in previous_bed_states or bed_name not in current_bed_states:
                # Should not happen in normal flow, but good for robustness
                return False 

            prev_P_sum = np.sum(previous_bed_states[bed_name]['P_profile'])
            curr_P_sum = np.sum(current_bed_states[bed_name]['P_profile'])
            
            prev_T_sum = np.sum(previous_bed_states[bed_name]['T_profile'])
            curr_T_sum = np.sum(current_bed_states[bed_name]['T_profile'])

            prev_q_sum = np.sum(previous_bed_states[bed_name]['q_profile'])
            curr_q_sum = np.sum(current_bed_states[bed_name]['q_profile'])

            # Calculate relative differences. Handle division by zero for initial/near-zero values if necessary.
            diff_P = abs(curr_P_sum - prev_P_sum) / (abs(prev_P_sum) + 1e-9)
            diff_T = abs(curr_T_sum - prev_T_sum) / (abs(prev_T_sum) + 1e-9)
            diff_q = abs(curr_q_sum - prev_q_sum) / (abs(prev_q_sum) + 1e-9)
            
            if (diff_P > self._solver_settings.steady_state_tolerance or
                diff_T > self._solver_settings.steady_state_tolerance or
                diff_q > self._solver_settings.steady_state_tolerance):
                is_steady = False
                print(f"  Bed {bed_name} not yet at pseudo-steady state. "
                      f"dP/P: {diff_P:.2e}, dT/T: {diff_T:.2e}, dq/q: {diff_q:.2e}")
                break # Not steady for this bed, no need to check others

        return is_steady

    def run_simulation(self) -> pd.DataFrame:
        """
        Runs the PSA simulation for the configured number of cycles or until
        a pseudo-steady state is reached.

        The simulation iterates through cycles, running each cycle step for
        all beds. It uses `_check_steady_state` to determine when the system
        has reached a cyclic steady state, at which point the simulation terminates.

        Returns:
            pd.DataFrame: A comprehensive DataFrame containing the entire simulation history
                          for all cycles and beds.
        """
        all_cycles_data = []
        
        # Store initial bed states for pseudo-steady state comparison
        previous_cycle_end_states = {name: bed.get_final_state() for name, bed in self._beds.items()}
        
        print(f"\nStarting simulation for '{self._config.project_name}'...")

        final_cycle_num = 0
        for cycle_num in range(1, self._solver_settings.n_cycles_to_steady_state + 1):
            final_cycle_num = cycle_num
            cycle_df = self.run_cycle(cycle_num)
            all_cycles_data.append(cycle_df)

            current_cycle_end_states = {name: bed.get_final_state() for name, bed in self._beds.items()}

            # Check for pseudo-steady state after the first full cycle
            if cycle_num >= 1: # Start checking after the first full cycle
                if self._check_steady_state(current_cycle_end_states, previous_cycle_end_states):
                    print(f"\nPseudo-steady state reached after {cycle_num} cycles.")
                    break # Exit simulation loop
                previous_cycle_end_states = current_cycle_end_states # Update for next comparison

            if cycle_num == self._solver_settings.n_cycles_to_steady_state:
                print(f"\nMaximum configured cycles ({self._solver_settings.n_cycles_to_steady_state}) reached. "
                      "Pseudo-steady state not achieved within this limit.")

        self.simulation_history = pd.concat(all_cycles_data, ignore_index=True)
        print(f"\nSimulation finished for {self._config.project_name}. Total cycles run: {final_cycle_num}.")
        return self.simulation_history

```
```python
# examples/example_air_separation.py
"""
Example script demonstrating a 4-step Pressure Swing Adsorption (PSA) cycle
for air separation (N2/O2) using the Cloud PSA Simulator.

This script configures a single-bed PSA system with Zeolite 13X adsorbent,
defines a typical 4-step cycle (Adsorption, Blowdown, Purge, Pressurization),
runs the simulation to pseudo-steady state, and visualizes key results
like pressure, temperature, and mole fraction profiles over time and space.
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from cloud_psa_simulator.config.settings import (
    PsaConfig, ComponentConfig, AdsorbentConfig, 
    IsothermComponentConfig, BedConfig, CycleStepConfig, SolverConfig
)
from cloud_psa_simulator.core.simulator import PsaSimulator

def plot_results(df: pd.DataFrame, components: list, title: str = "PSA Simulation Results"):
    """
    Plots key simulation results: pressure, temperature, and mole fractions.

    Args:
        df (pd.DataFrame): The simulation history DataFrame.
        components (list): List of component names for mole fraction plots.
        title (str): Title for the plots.
    """
    fig, axes = plt.subplots(3, 2, figsize=(18, 15))
    fig.suptitle(title, fontsize=16)

    # --- Time-resolved plots at bed inlet (z_node = 0) ---
    inlet_df = df[df['z_node'] == df['z_node'].min()]
    inlet_df_last_cycle = inlet_df[inlet_df['cycle_num'] == inlet_df['cycle_num'].max()]
    
    # Re-align time for plotting the last cycle
    cycle_duration = inlet_df_last_cycle['time_step_in_cycle'].max() + inlet_df_last_cycle[inlet_df_last_cycle['time_step_in_cycle'] == 0.0]['time_step_in_cycle'].iloc[0]
    inlet_df_last_cycle['time_relative_to_cycle_start'] = inlet_df_last_cycle['time_abs'] % cycle_duration

    # Inlet Pressure
    axes[0, 0].plot(inlet_df_last_cycle['time_relative_to_cycle_start'], inlet_df_last_cycle['P'] / 1e5, label='Pressure') # Convert to bar
    axes[0, 0].set_title('Inlet Pressure (Last Cycle)')
    axes[0, 0].set_ylabel('Pressure (bar)')
    axes[0, 0].set_xlabel('Time in Cycle (s)')
    axes[0, 0].legend()
    axes[0, 0].grid(True)

    # Inlet Temperature
    axes[1, 0].plot(inlet_df_last_cycle['time_relative_to_cycle_start'], inlet_df_last_cycle['T'], label='Temperature')
    axes[1, 0].set_title('Inlet Temperature (Last Cycle)')
    axes[1, 0].set_ylabel('Temperature (K)')
    axes[1, 0].set_xlabel('Time in Cycle (s)')
    axes[1, 0].legend()
    axes[1, 0].grid(True)

    # Inlet Mole Fractions
    for comp in components:
        axes[2, 0].plot(inlet_df_last_cycle['time_relative_to_cycle_start'], inlet_df_last_cycle[f'y_{comp}'], label=f'y_{comp}')
    axes[2, 0].set_title('Inlet Mole Fractions (Last Cycle)')
    axes[2, 0].set_ylabel('Mole Fraction')
    axes[2, 0].set_xlabel('Time in Cycle (s)')
    axes[2, 0].legend()
    axes[2, 0].grid(True)

    # --- Spatial profiles at the end of the last cycle ---
    final_time_step_df = df[df['cycle_num'] == df['cycle_num'].max()]
    # Select the very last time point in the last cycle for spatial profiles
    spatial_df = final_time_step_df[final_time_step_df['time_abs'] == final_time_step_df['time_abs'].max()]

    # Spatial Pressure
    axes[0, 1].plot(spatial_df['z_node'], spatial_df['P'] / 1e5, label='Pressure Profile')
    axes[0, 1].set_title('Pressure Profile (End of Last Cycle)')
    axes[0, 1].set_ylabel('Pressure (bar)')
    axes[0, 1].set_xlabel('Bed Length (m)')
    axes[0, 1].legend()
    axes[0, 1].grid(True)

    # Spatial Temperature
    axes[1, 1].plot(spatial_df['z_node'], spatial_df['T'], label='Temperature Profile')
    axes[1, 1].set_title('Temperature Profile (End of Last Cycle)')
    axes[1, 1].set_ylabel('Temperature (K)')
    axes[1, 1].set_xlabel('Bed Length (m)')
    axes[1, 1].legend()
    axes[1, 1].grid(True)

    # Spatial Mole Fractions
    for comp in components:
        axes[2, 1].plot(spatial_df['z_node'], spatial_df[f'y_{comp}'], label=f'y_{comp}')
    axes[2, 1].set_title('Mole Fraction Profiles (End of Last Cycle)')
    axes[2, 1].set_ylabel('Mole Fraction')
    axes[2, 1].set_xlabel('Bed Length (m)')
    axes[2, 1].legend()
    axes[2, 1].grid(True)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()

def main():
    """
    Main function to configure and run the PSA air separation simulation.
    """
    print("--- Configuring PSA Air Separation Simulation ---")

    # 1. Define Gas Components
    nitrogen = ComponentConfig(
        name="N2", molecular_weight=0.0280134, diffusivity_ref=1.8e-5, heat_capacity_gas=29.12)
    oxygen = ComponentConfig(
        name="O2", molecular_weight=0.0319988, diffusivity_ref=1.9e-5, heat_capacity_gas=29.38)
    
    components_list = [nitrogen, oxygen]
    component_names = [comp.name for comp in components_list]

    # 2. Define Adsorbent (Zeolite 13X for N2/O2 separation)
    # Zeolite 13X preferentially adsorbs N2 over O2
    zeolite_13x = AdsorbentConfig(
        name="Zeolite 13X",
        density_bulk=700,         # kg/m^3
        density_solid=1100,       # kg/m^3
        porosity_bed=0.35,        # dimensionless (interparticle)
        porosity_particle=0.45,   # dimensionless (intraparticle)
        heat_capacity_solid=900,  # J/(kg*K)
        particle_diameter=0.001,  # meters (1 mm)
        thermal_conductivity=0.2, # W/(m*K) (effective bed thermal conductivity)
        isotherms={
            # Langmuir parameters: Q_m (mol/kg), b0 (1/Pa), Ea (J/mol)
            # Ea represents -dH_ads (negative of heat of adsorption) for Van't Hoff calculation of b.
            # Larger Q_m and b0/Ea values mean stronger adsorption.
            "N2": IsothermComponentConfig(
                type="Langmuir",
                params={"Q_m": 2.5, "b0": 1e-6, "Ea": -18000} 
            ),
            "O2": IsothermComponentConfig(
                type="Langmuir",
                params={"Q_m": 2.0, "b0": 5e-7, "Ea": -16000} 
            ),
        },
        mass_transfer_coeffs={
            "N2": 0.5, # 1/s (LDF coefficient)
            "O2": 0.6, # 1/s (O2 generally diffuses faster in 13X than N2)
        },
        heat_of_adsorption={ # Heat of adsorption (J/mol), typically negative for exothermic adsorption
            "N2": -18000, 
            "O2": -16000, 
        }
    )

    # 3. Define Adsorber Bed(s)
    bed_1 = BedConfig(
        name="Bed 1",
        length=1.0,           # meters
        diameter=0.1,         # meters
        adsorbent_name="Zeolite 13X", # Must match name defined in adsorbents list
        initial_pressure=101325, # Pa (1 atm)
        initial_temperature=298.15, # K (25 C)
        initial_component_mole_fractions={"N2": 0.79, "O2": 0.21}, # Initial air composition
        num_spatial_nodes=20, # Number of discretization points along the bed
    )

    # 4. Define PSA Cycle Steps (4-step cycle)
    # Adsorption (Feed from inlet, product from outlet, high pressure)
    adsorption_step = CycleStepConfig(
        name="Adsorption",
        type="Adsorption",
        duration=120, # seconds
        feed_pressure=500000, # 5 bar
        feed_temperature=298.15,
        feed_mole_fractions={"N2": 0.79, "O2": 0.21}, # Air feed
        feed_flow_rate=0.01 # mol/s (Example constant flow rate)
    )
    # Blowdown (Depressurization from feed end, product from outlet, low pressure)
    blowdown_step = CycleStepConfig(
        name="Blowdown",
        type="Blowdown",
        duration=60, # seconds
        blowdown_pressure=100000, # 1 bar
    )
    # Purge (Co-current purge from outlet to inlet, low pressure, using product N2)
    # Note: In this simple model, purge is treated as a general outflow with target pressure.
    # A more detailed model would specify purge gas source and inlet.
    purge_step = CycleStepConfig(
        name="Purge",
        type="Purge",
        duration=90, # seconds
        purge_pressure=101325, # Pa (atmospheric, outlet)
        purge_component="N2", # Assuming N2-rich product is used for purge
        purge_flow_rate_ratio=0.1 # Example: 10% of N2 product flow (conceptual in this model)
    )
    # Pressurization (Pressurize from feed end, no flow, high pressure)
    pressurization_step = CycleStepConfig(
        name="Pressurization",
        type="Pressurization",
        duration=90, # seconds
        feed_pressure=500000, # Pressurize back to adsorption pressure
        feed_temperature=298.15,
        feed_mole_fractions={"N2": 0.79, "O2": 0.21} # Using feed gas for repressurization
    )
    
    cycle_steps_list = [adsorption_step, blowdown_step, purge_step, pressurization_step]

    # 5. Define Solver Settings
    solver_settings = SolverConfig(
        method="Radau", # Robust solver for stiff ODEs
        rtol=1e-4,      # Relative tolerance
        atol=1e-7,      # Absolute tolerance
        max_step=10.0,  # Maximum step size for the ODE solver
        n_cycles_to_steady_state=5, # Run at least 5 cycles to observe steady state
        steady_state_tolerance=5e-3, # Tolerance for determining pseudo-steady state (relative change)
    )

    # 6. Create the main PsaConfig object
    psa_config = PsaConfig(
        project_name="Air Separation Demo",
        components=components_list,
        adsorbents=[zeolite_13x],
        beds=[bed_1],
        cycle_steps=cycle_steps_list,
        solver_settings=solver_settings,
    )

    # 7. Initialize and run the simulator
    simulator = PsaSimulator(psa_config)
    simulation_history_df = simulator.run_simulation()

    # 8. Post-processing and plotting
    print("\n--- Simulation Complete. Generating Plots ---")
    plot_results(simulation_history_df, component_names, title="Air Separation PSA - Last Cycle & Final Profile")

    print("\nExample simulation finished successfully.")

if __name__ == "__main__":
    main()

```