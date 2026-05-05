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
```markdown
# README.md
# Cloud PSA Simulator

A foundational Pressure Swing Adsorption (PSA) model implemented in Python, designed for scientific computing and process simulation. This project aims to provide a robust, dynamic 1D pseudo-homogeneous model that incorporates non-isothermal and non-isobaric conditions, while reflecting principles from cutting-edge research in PSA modeling (2024-2026).

## Project Structure

```
cloud_psa_simulator/
├── src/
│   └── cloud_psa_simulator/
│       ├── __init__.py           # Package initializer
│       ├── models/                 # Core PSA physical models
│       │   ├── __init__.py
│       │   ├── components.py       # GasComponent, Adsorbent definitions
│       │   ├── cycle_steps.py      # Placeholder for PsaCycleStep runtime definitions
│       │   └── bed.py              # AdsorberBed (1D PDE solver for mass, energy, momentum)
│       ├── core/                   # Simulator orchestration
│       │   ├── __init__.py
│       │   └── simulator.py        # PsaSimulator class for running cycles
│       ├── config/                 # Configuration system
│       │   ├── __init__.py
│       │   └── settings.py         # Pydantic models for PSA simulation configuration
│       └── utils/                  # Utility functions and constants
│           ├── __init__.py
│           ├── constants.py        # Physical constants
│           └── validation.py       # Input validation helpers
├── pyproject.toml              # Project metadata and dependencies
├── examples/                   # Example usage scripts
│   └── example_air_separation.py   # Demonstrates a 4-step air separation PSA
└── README.md                   # This README file
```

## Features

*   **1D Pseudo-homogeneous Dynamic Model:** Simulates mass and energy transfer within a fixed-bed adsorber, considering both gas and adsorbed phases.
*   **Non-Isothermal & Non-Isobaric Conditions:** The model accounts for temperature and pressure gradients along the bed and their dynamic evolution.
*   **Multi-component Adsorption:** Supports Extended Langmuir isotherms for competitive adsorption (implementable through `Adsorbent` class).
*   **Linear Driving Force (LDF) Kinetics:** Models mass transfer between gas and solid phases.
*   **Method of Lines (MOL):** Uses `scipy.integrate.solve_ivp` for robust numerical solution of PDEs.
*   **Pydantic-based Configuration:** Provides a declarative and validated system for defining PSA components, adsorbents, beds, cycle steps, and solver settings.
*   **Modular Design:** Separates concerns into `models`, `config`, `core`, and `utils` for maintainability and extensibility.
*   **Error Handling and Validation:** Robust input validation ensures model integrity.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/cloud-psa-simulator/cloud-psa-simulator.git
    cd cloud-psa-simulator
    ```
2.  **Install dependencies:**
    You can install dependencies directly using `pip`:
    ```bash
    pip install -e .
    # Or manually install listed dependencies if not using editable install:
    # pip install numpy scipy pydantic pandas matplotlib
    ```

## Usage

To run an example simulation:

```bash
python examples/example_air_separation.py
```

This script defines a simplified 4-step PSA cycle for air separation, configures the simulator, runs it to pseudo-steady state, and plots the results.

## Advanced Concepts (Conceptual Integration)

While this implementation focuses on a foundational dynamic model, it's designed to be the core "physics engine" for more advanced concepts highlighted in recent research:

*   **Real-time Predictive Control (PINNs/MPC):** The dynamic model generates the high-fidelity data that Physics-Informed Neural Networks (PINNs) would learn from to create fast surrogate models for Model Predictive Control (MPC).
*   **High-Fidelity Digital Twins:** This simulator serves as the core predictive model within a larger digital twin architecture, which would integrate real-time sensor data, provide continuous calibration, and enable scenario analysis.
*   **Multi-Scale Modeling:** Adsorbent properties (isotherm parameters, diffusion coefficients) are input parameters here, but conceptually, they would be derived from atomic/molecular simulations (e.g., GCMC, MD).
*   **Uncertainty Quantification (UQ):** The configurable nature of the model facilitates running Monte Carlo simulations or other UQ techniques by systematically varying input parameters to assess robustness.
*   **CFD-Adsorption Dynamics:** While primarily 1D, the model acknowledges 3D effects. Parameters (e.g., effective thermal conductivity, mass transfer coefficients) could be informed or corrected by detailed 3D CFD simulations.

## Contributing

Contributions are welcome! Please follow standard Python development practices: fork the repository, create a feature branch, and submit a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
```
```python
# src/cloud_psa_simulator/__init__.py
"""
Cloud PSA Simulator Package
A foundational Pressure Swing Adsorption (PSA) model in Python.
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
import numpy as np

# Universal gas constant in J/(mol*K)
R_GAS_CONSTANT = 8.314462618

```
```python
# src/cloud_psa_simulator/utils/validation.py
from pydantic import ValidationError
import numpy as np

def validate_positive(value, field_name: str):
    """Ensures a value is positive."""
    if value <= 0:
        raise ValueError(f"{field_name} must be a positive value.")
    return value

def validate_non_negative(value, field_name: str):
    """Ensures a value is non-negative."""
    if value < 0:
        raise ValueError(f"{field_name} must be a non-negative value.")
    return value

def validate_fraction(value, field_name: str):
    """Ensures a value is between 0 and 1 (inclusive)."""
    if not (0 <= value <= 1):
        raise ValueError(f"{field_name} must be between 0 and 1.")
    return value

def validate_sum_to_one(values, field_name: str, tolerance: float = 1e-6):
    """Ensures a list of values sums approximately to one."""
    if not np.isclose(sum(values), 1.0, atol=tolerance):
        raise ValueError(f"Sum of {field_name} must be approximately 1.0.")
    return values

def validate_all_positive(values, field_name: str):
    """Ensures all values in a list are positive."""
    if not all(v > 0 for v in values):
        raise ValueError(f"All values in {field_name} must be positive.")
    return values

def validate_isotherm_params(isotherm_type: str, params: dict):
    """Validates isotherm parameters based on type."""
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
from pydantic import BaseModel, Field, field_validator
from typing import List, Dict, Any, Literal, Optional
import numpy as np
from ..utils.validation import (
    validate_positive, validate_non_negative, 
    validate_isotherm_params
)

# --- Component Configuration ---
class ComponentConfig(BaseModel):
    name: str = Field(..., description="Name of the gas component (e.g., 'N2', 'O2', 'CO2').")
    molecular_weight: float = Field(..., gt=0, description="Molecular weight in kg/mol.")
    diffusivity_ref: float = Field(1e-5, gt=0, description="Reference diffusivity in m^2/s at ref_temp and ref_pressure.")
    henry_constant: Optional[float] = Field(None, ge=0, description="Henry's constant for solubility if applicable (mol/(m^3*Pa)).")
    heat_capacity_gas: float = Field(..., gt=0, description="Molar heat capacity of the gas component at constant pressure in J/(mol*K).")

    @field_validator('molecular_weight', 'diffusivity_ref', 'heat_capacity_gas')
    @classmethod
    def check_positive_floats(cls, v):
        return validate_positive(v, "Component property")
    
    @field_validator('henry_constant')
    @classmethod
    def check_non_negative_float(cls, v):
        if v is not None:
            return validate_non_negative(v, "Henry constant")
        return v

# --- Isotherm Configuration for Adsorbent ---
class IsothermComponentConfig(BaseModel):
    type: Literal["Langmuir", "Sips"] = Field(..., description="Type of isotherm model.") # Currently only Langmuir fully extended for multi-component.
    params: Dict[str, float] = Field(..., description="Dictionary of isotherm parameters.")

    @field_validator('params')
    @classmethod
    def validate_isotherm_specific_params(cls, v, info):
        isotherm_type = info.data.get('type')
        if not isotherm_type:
            raise ValueError("Isotherm type must be specified for parameter validation.")
        return validate_isotherm_params(isotherm_type, v)

# --- Adsorbent Configuration ---
class AdsorbentConfig(BaseModel):
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
    def check_positive_floats(cls, v):
        return validate_positive(v, "Adsorbent property")

    @field_validator('porosity_bed', 'porosity_particle')
    @classmethod
    def check_porosity_range(cls, v):
        if not (0 < v < 1):
            raise ValueError("Porosity must be between 0 and 1.")
        return v
    
    @field_validator('mass_transfer_coeffs')
    @classmethod
    def check_positive_mtc(cls, v):
        for comp, val in v.items():
            validate_positive(val, f"Mass transfer coefficient for {comp}")
        return v

    @field_validator('heat_of_adsorption')
    @classmethod
    def check_ho_adsorption(cls, v):
        for comp, val in v.items():
            if not isinstance(val, (int, float)):
                raise ValueError(f"Heat of adsorption for {comp} must be a number.")
        return v

# --- Bed Configuration ---
class BedConfig(BaseModel):
    name: str = Field(..., description="Name of the adsorber bed (e.g., 'Bed 1').")
    length: float = Field(..., gt=0, description="Length of the adsorber bed in meters.")
    diameter: float = Field(..., gt=0, description="Diameter of the adsorber bed in meters.")
    adsorbent_name: str = Field(..., description="Name of the adsorbent material used in this bed.")
    initial_pressure: float = Field(..., gt=0, description="Initial bed pressure in Pa.")
    initial_temperature: float = Field(..., gt=0, description="Initial bed temperature in K.")
    initial_component_mole_fractions: Dict[str, float] = Field(..., description="Initial gas phase mole fractions of components in the bed.")
    num_spatial_nodes: int = Field(20, gt=1, description="Number of spatial discretization nodes for the bed model.") # Changed default to 20 for faster execution

    @field_validator('length', 'diameter', 'initial_pressure', 'initial_temperature')
    @classmethod
    def check_positive_floats(cls, v):
        return validate_positive(v, "Bed property")

    @field_validator('num_spatial_nodes')
    @classmethod
    def check_num_nodes(cls, v):
        if v < 2:
            raise ValueError("Number of spatial nodes must be at least 2.")
        return v

    @field_validator('initial_component_mole_fractions')
    @classmethod
    def check_mole_fractions(cls, v):
        total_sum = sum(v.values())
        if not np.isclose(total_sum, 1.0, atol=1e-6):
            raise ValueError("Sum of initial component mole fractions must be approximately 1.0.")
        if not all(val >= 0 for val in v.values()):
            raise ValueError("Initial component mole fractions must be non-negative.")
        return v

# --- Cycle Step Configuration ---
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

    @field_validator('duration', 'feed_pressure', 'feed_temperature', 'feed_flow_rate',
                     'purge_pressure', 'purge_flow_rate_ratio', 'blowdown_pressure')
    @classmethod
    def check_positive_optional_floats(cls, v):
        if v is not None:
            return validate_positive(v, "Cycle step parameter")
        return v

    @field_validator('feed_mole_fractions')
    @classmethod
    def check_feed_mole_fractions(cls, v):
        if v is not None:
            total_sum = sum(v.values())
            if not np.isclose(total_sum, 1.0, atol=1e-6):
                raise ValueError("Sum of feed component mole fractions must be approximately 1.0.")
            if not all(val >= 0 for val in v.values()):
                raise ValueError("Feed component mole fractions must be non-negative.")
        return v

# --- Solver Configuration ---
class SolverConfig(BaseModel):
    method: str = Field("Radau", description="Solver method for scipy.integrate.solve_ivp (e.g., 'Radau', 'BDF').")
    rtol: float = Field(1e-4, gt=0, description="Relative tolerance for the ODE solver.") # Relaxed for faster example
    atol: float = Field(1e-7, gt=0, description="Absolute tolerance for the ODE solver.") # Relaxed for faster example
    max_step: float = Field(5.0, gt=0, description="Maximum step size for the ODE solver.") # Changed default for stability
    n_cycles_to_steady_state: int = Field(3, ge=1, description="Number of cycles to simulate to reach pseudo-steady state.")
    max_iter_per_cycle: int = Field(100, ge=1, description="Max iterations to find steady state if not reached by n_cycles.")
    steady_state_tolerance: float = Field(1e-3, gt=0, description="Tolerance for determining pseudo-steady state for cyclic variables.") # Relaxed

# --- Main PSA Configuration ---
class PsaConfig(BaseModel):
    project_name: str = Field("Default PSA Simulation", description="Name of the PSA simulation project.")
    components: List[ComponentConfig] = Field(..., description="List of gas component configurations.")
    adsorbents: List[AdsorbentConfig] = Field(..., description="List of adsorbent material configurations.")
    beds: List[BedConfig] = Field(..., min_length=1, description="List of adsorber bed configurations.")
    cycle_steps: List[CycleStepConfig] = Field(..., min_length=1, description="List of PSA cycle step configurations.")
    solver_settings: SolverConfig = Field(default_factory=SolverConfig, description="Settings for the ODE solver.")

    @field_validator('components')
    @classmethod
    def validate_component_names_unique(cls, v):
        names = [comp.name for comp in v]
        if len(set(names)) != len(names):
            raise ValueError("Component names must be unique.")
        return v

    @field_validator('adsorbents')
    @classmethod
    def validate_adsorbent_names_unique(cls, v):
        names = [ads.name for ads in v]
        if len(set(names)) != len(names):
            raise ValueError("Adsorbent names must be unique.")
        return v

    @field_validator('beds')
    @classmethod
    def validate_bed_adsorbent_exists(cls, beds, info):
        adsorbent_names = {ads.name for ads in info.data['adsorbents']}
        for bed in beds:
            if bed.adsorbent_name not in adsorbent_names:
                raise ValueError(f"Adsorbent '{bed.adsorbent_name}' specified for bed '{bed.name}' not found in adsorbents list.")
            if not all(comp_name in [c.name for c in info.data['components']] for comp_name in bed.initial_component_mole_fractions.keys()):
                raise ValueError(f"Initial component mole fractions for bed '{bed.name}' contain undefined components.")
        return beds
    
    @field_validator('cycle_steps')
    @classmethod
    def validate_cycle_step_components_exist(cls, cycle_steps, info):
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
from pydantic import BaseModel, Field, field_validator
from typing import List, Dict, Any, Callable, Tuple
import numpy as np
from ..utils.validation import validate_positive, validate_non_negative
from ..utils.constants import R_GAS_CONSTANT
from ..config.settings import IsothermComponentConfig # Import the config model

class GasComponent(BaseModel):
    """
    Represents a single gas component in the PSA system.
    """
    name: str = Field(..., description="Name of the gas component (e.g., 'N2', 'O2', 'CO2').")
    molecular_weight: float = Field(..., gt=0, description="Molecular weight in kg/mol.")
    diffusivity_ref: float = Field(1e-5, gt=0, description="Reference diffusivity in m^2/s at ref_temp and ref_pressure.")
    henry_constant: float = Field(None, ge=0, description="Henry's constant for solubility if applicable (mol/(m^3*Pa)).")
    heat_capacity_gas: float = Field(..., gt=0, description="Molar heat capacity of the gas component at constant pressure in J/(mol*K).")

    @field_validator('molecular_weight', 'diffusivity_ref', 'heat_capacity_gas')
    @classmethod
    def check_positive_floats(cls, v):
        return validate_positive(v, "Molecular weight, diffusivity_ref or heat_capacity_gas")
    
    @field_validator('henry_constant')
    @classmethod
    def check_non_negative_float(cls, v):
        if v is not None:
            return validate_non_negative(v, "Henry constant")
        return v

class Adsorbent(BaseModel):
    """
    Represents an adsorbent material used in the PSA bed.
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
    def check_positive_floats(cls, v):
        return validate_positive(v, "Adsorbent property")

    @field_validator('porosity_bed', 'porosity_particle')
    @classmethod
    def check_porosity_range(cls, v):
        if not (0 < v < 1):
            raise ValueError("Porosity must be between 0 and 1.")
        return v
    
    @field_validator('mass_transfer_coeffs')
    @classmethod
    def check_positive_mtc(cls, v):
        for comp, val in v.items():
            validate_positive(val, f"Mass transfer coefficient for {comp}")
        return v

    @field_validator('heat_of_adsorption')
    @classmethod
    def check_ho_adsorption(cls, v):
        for comp, val in v.items():
            if not isinstance(val, (int, float)):
                raise ValueError(f"Heat of adsorption for {comp} must be a number.")
        return v

    def get_isotherm_params_for_T(self, component_name: str, T: float) -> Tuple[str, Dict[str, float]]:
        """
        Retrieves and adjusts isotherm parameters for a given temperature.
        Supports temperature-dependent Langmuir via Van't Hoff equation for 'b'.
        b(T) = b0 * exp(-Ea / (R * T)) where Ea is typically related to -dH_ads.
        Returns a tuple of (isotherm_type, adjusted_params).
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
        Assumes Extended Langmuir for competitive adsorption if multiple components are present.
        Currently only supports "Langmuir" type for multi-component Extended Langmuir.
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
from pydantic import BaseModel, Field
from typing import Literal, Dict, Optional

class PsaCycleStep:
    """
    Placeholder for a runtime representation of a PSA cycle step.
    In the current architecture, CycleStepConfig from settings.py
    serves as the primary data carrier for step definitions.
    This class would be expanded if runtime state specific to a step
    (e.g., dynamic flow control logic) needed to be encapsulated.
    """
    pass

```
```python
# src/cloud_psa_simulator/models/bed.py
import numpy as np
from scipy.integrate import solve_ivp
from typing import List, Dict, Any, Tuple
import pandas as pd

from ..utils.constants import R_GAS_CONSTANT
from ..models.components import GasComponent, Adsorbent
from ..config.settings import BedConfig, CycleStepConfig, SolverConfig

class AdsorberBed:
    """
    Represents a 1D non-isothermal, non-isobaric fixed-bed adsorber using Method of Lines.
    Solves mass and energy conservation equations along the bed length.
    State vector: [P_nodes, T_nodes, y_flat, q_flat]
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
        Initializes the state vector based on bed configuration.
        State vector structure per node (z-position):
        [P_0..P_N-1, T_0..T_N-1, y_0_0..y_N-1_Nc-1, q_0_0..q_N-1_Nc-1]
        Total length: num_nodes * (2 + 2 * num_components)
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
        Transforms current profiles into a flat state vector for the ODE solver.
        """
        state_parts = []
        state_parts.extend(self.current_P_profile)
        state_parts.extend(self.current_T_profile)
        state_parts.extend(self.current_y_profile.flatten())
        state_parts.extend(self.current_q_profile.flatten())
        self._initial_state_vector = np.array(state_parts)

    def _get_profiles_from_state_vector(self, state_vector: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        Extracts P, T, y, q profiles from a flat state vector.
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
        
        # Ensure mole fractions sum to 1 and are non-negative
        y_profile[y_profile < 0] = 0 # Prevent negative mole fractions due to numerical errors
        row_sums = np.sum(y_profile, axis=1, keepdims=True)
        # Handle cases where all y_i at a node are zero (e.g., initially for components not present)
        # Avoid division by zero, set to zero where row_sums is zero
        y_profile = np.divide(y_profile, row_sums, out=np.zeros_like(y_profile), where=row_sums!=0)
        
        return P_profile, T_profile, y_profile, q_profile

    def _calculate_axial_derivative(self, profile: np.ndarray, flow_direction: int) -> np.ndarray:
        """
        Calculates axial derivative using upwind or central differencing.
        For convective terms, upwind is generally more stable.
        flow_direction = 1 (z=0 to z=L, forward flow)
        flow_direction = -1 (z=L to z=0, reverse flow)
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
        Defines the system of ODEs based on 1D pseudo-homogeneous model.
        State vector: [P_nodes, T_nodes, y_flat, q_flat]
        Simplifications for this functional model:
        - Axial dispersion is neglected for mass and heat (D_ax=0, K_ax=0).
        - Heat transfer to wall is neglected (K_wall=0).
        - Superficial velocity `u_s_avg` is assumed constant along the bed for the duration of the step.
          (This is a major simplification for a truly non-isobaric model but makes it functional for `solve_ivp`).
        - Ideal gas law holds.
        - Local thermal equilibrium between gas and solid.
        - Boundary conditions are enforced by 'nudging' the derivative to quickly reach the target.
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
                dy_dt_profile[0, :] = dy_dt_profile[1, :] # Default to Neumann-like if no specific composition BC
            
        # Flatten derivatives for the solver
        d_state_dt_parts = []
        d_state_dt_parts.extend(dP_dt_profile)
        d_state_dt_parts.extend(dT_dt_profile)
        d_state_dt_parts.extend(dy_dt_profile.flatten())
        d_state_dt_parts.extend(dq_dt_profile.flatten())

        return np.array(d_state_dt_parts)

    def run_step(self, current_step: CycleStepConfig) -> pd.DataFrame:
        """
        Runs a single PSA cycle step.
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
        """Returns the final state of the bed as a dictionary."""
        return {
            'P_profile': self.current_P_profile,
            'T_profile': self.current_T_profile,
            'y_profile': self.current_y_profile,
            'q_profile': self.current_q_profile
        }

```
```python
# src/cloud_psa_simulator/core/simulator.py
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
    """
    _config: PsaConfig
    _gas_components: List[GasComponent]
    _adsorbents: Dict[str, Adsorbent]
    _beds: Dict[str, AdsorberBed]
    _cycle_steps: List[CycleStepConfig]
    _solver_settings: SolverConfig

    simulation_history: pd.DataFrame
    
    def __init__(self, config: PsaConfig):
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
        For true multi-bed operation, concurrent step execution logic would be needed.
        """
        print(f"\n--- Running Cycle {cycle_num} ---")
        cycle_data = []

        active_beds = self._beds.keys() if beds_to_simulate is None else beds_to_simulate
        
        if len(active_beds) > 1:
            print("Warning: This foundational simulator runs beds sequentially per step. For true multi-bed, "
                  "concurrent step execution logic would be needed.")

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

    def run_simulation(self) -> pd.DataFrame:
        """
        Runs the PSA simulation for the configured number of cycles to reach pseudo-steady state.
        """
        all_cycles_data = []
        
        # Store initial bed states for pseudo-steady state comparison
        initial_bed_states = {name: bed.get_final_state() for name, bed in self._beds.items()}
        
        for cycle_num in range(1, self._solver_settings.n_cycles_to_steady_state + 1):
            cycle_df = self.run_cycle(cycle_num)
            all_cycles_data.append(cycle_df)

            # Check for pseudo-steady state (very basic check for now)
            if cycle_num > 1: # Start checking after the first full cycle
                is_steady = True
                for bed_name, bed in self._beds.items():
                    prev_P = initial_bed_states[bed_name