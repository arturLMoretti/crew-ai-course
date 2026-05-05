To ensure the robustness, correctness, and performance of the "Intelligent Multi-Fidelity PSA Digital Twin" core model, a comprehensive test suite has been developed. This suite includes unit tests for foundational components, integration tests for complete PSA cycles, validation tests against physically consistent expected outputs, and benchmark tests for performance assessment.

The test suite structure aligns with best practices for scientific software development, focusing on modularity, clarity, and maintainability.

---

### `pyproject.toml` (Updated)

Added `pytest` and `pytest-cov` as development dependencies.

```toml
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

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "pytest-benchmark>=4.0.0", # For performance benchmarks
]

[tool.pytest.ini_options]
minversion = "7.0"
addopts = "--cov=src/cloud_psa_simulator --cov-report=term-missing"
testpaths = "tests"
python_files = "test_*.py"
```

---

### `pytest.ini`

Configuration for `pytest` to discover tests, apply coverage reporting, and set minimum version.

```ini
[pytest]
minversion = "7.0"
addopts = "--cov=src/cloud_psa_simulator --cov-report=term-missing --strict-markers"
testpaths = "tests"
python_files = "test_*.py"
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    benchmark: marks tests as benchmarks (run with '-m benchmark')
```

---

### `tests/` Directory Structure

```
cloud_psa_simulator/
├── src/
│   └── cloud_psa_simulator/
│       ├── ... (existing model, config, core, utils files)
├── tests/
│   ├── __init__.py
│   ├── conftest.py                 # Shared fixtures for tests
│   ├── unit/                       # Unit tests for individual components/functions
│   │   ├── test_components.py
│   │   ├── test_settings.py
│   │   └── test_bed_primitives.py  # Primitives of AdsorberBed
│   ├── integration/                # Tests for interactions between modules
│   │   └── test_simulator_integration.py
│   ├── validation/                 # Tests against expected physical behavior/trends
│   │   └── test_basic_cycle_validation.py
│   ├── benchmarks/                 # Performance benchmark tests
│   │   └── test_performance_benchmarks.py
├── pyproject.toml
├── pytest.ini
└── README.md
```

---

### `tests/__init__.py`

```python
# Empty file to mark tests as a Python package
```

---

### `tests/conftest.py`

Provides reusable fixtures to set up common `PsaConfig` objects for various test scenarios, ensuring consistency and reducing boilerplate.

```python
import pytest
import numpy as np
from pydantic import ValidationError

from src.cloud_psa_simulator.config.settings import (
    PsaConfig, ComponentConfig, AdsorbentConfig, 
    IsothermComponentConfig, BedConfig, CycleStepConfig, SolverConfig
)
from src.cloud_psa_simulator.models.components import GasComponent, Adsorbent
from src.cloud_psa_simulator.models.bed import AdsorberBed
from src.cloud_psa_simulator.core.simulator import PsaSimulator

@pytest.fixture
def nitrogen_component_config():
    """Fixture for a Nitrogen component config."""
    return ComponentConfig(
        name="N2", molecular_weight=0.028, diffusivity_ref=1.8e-5, heat_capacity_gas=29.12
    )

@pytest.fixture
def oxygen_component_config():
    """Fixture for an Oxygen component config."""
    return ComponentConfig(
        name="O2", molecular_weight=0.032, diffusivity_ref=1.9e-5, heat_capacity_gas=29.38
    )

@pytest.fixture
def co2_component_config():
    """Fixture for a CO2 component config."""
    return ComponentConfig(
        name="CO2", molecular_weight=0.044, diffusivity_ref=1.5e-5, heat_capacity_gas=37.1
    )

@pytest.fixture
def basic_components(nitrogen_component_config, oxygen_component_config):
    """Fixture for a list of basic gas components (N2, O2)."""
    return [nitrogen_component_config, oxygen_component_config]

@pytest.fixture
def extended_components(basic_components, co2_component_config):
    """Fixture for a list of extended gas components (N2, O2, CO2)."""
    return basic_components + [co2_component_config]

@pytest.fixture
def zeolite_13x_adsorbent_config():
    """Fixture for a Zeolite 13X adsorbent config."""
    return AdsorbentConfig(
        name="Zeolite 13X",
        density_bulk=700, density_solid=1100, porosity_bed=0.35, porosity_particle=0.45,
        heat_capacity_solid=900, particle_diameter=0.001, thermal_conductivity=0.2,
        isotherms={
            "N2": IsothermComponentConfig(type="Langmuir", params={"Q_m": 2.5, "b0": 1e-6, "Ea": -18000}),
            "O2": IsothermComponentConfig(type="Langmuir", params={"Q_m": 2.0, "b0": 5e-7, "Ea": -16000}),
            "CO2": IsothermComponentConfig(type="Langmuir", params={"Q_m": 3.0, "b0": 2e-5, "Ea": -25000}) # Stronger CO2 adsorption
        },
        mass_transfer_coeffs={"N2": 0.5, "O2": 0.6, "CO2": 0.4},
        heat_of_adsorption={"N2": -18000, "O2": -16000, "CO2": -25000}
    )

@pytest.fixture
def carbon_molecular_sieve_adsorbent_config():
    """Fixture for a Carbon Molecular Sieve (CMS) adsorbent config (O2/N2 separation)."""
    return AdsorbentConfig(
        name="CMS",
        density_bulk=500, density_solid=900, porosity_bed=0.4, porosity_particle=0.4,
        heat_capacity_solid=850, particle_diameter=0.0008, thermal_conductivity=0.15,
        isotherms={
            "N2": IsothermComponentConfig(type="Langmuir", params={"Q_m": 1.5, "b0": 8e-7, "Ea": -15000}),
            "O2": IsothermComponentConfig(type="Langmuir", params={"Q_m": 1.8, "b0": 1.2e-6, "Ea": -17000}), # O2 preferentially adsorbed by kinetics
        },
        mass_transfer_coeffs={"N2": 0.1, "O2": 0.8}, # N2 slower, O2 faster in CMS
        heat_of_adsorption={"N2": -15000, "O2": -17000}
    )

@pytest.fixture
def basic_adsorbents(zeolite_13x_adsorbent_config):
    """Fixture for a list of basic adsorbents."""
    return [zeolite_13x_adsorbent_config]

@pytest.fixture
def two_adsorbents(zeolite_13x_adsorbent_config, carbon_molecular_sieve_adsorbent_config):
    """Fixture for a list of two different adsorbents."""
    return [zeolite_13x_adsorbent_config, carbon_molecular_sieve_adsorbent_config]

@pytest.fixture
def initial_air_bed_config(zeolite_13x_adsorbent_config):
    """Fixture for an adsorber bed configured with air initially."""
    return BedConfig(
        name="Bed 1", length=1.0, diameter=0.1, adsorbent_name=zeolite_13x_adsorbent_config.name,
        initial_pressure=101325, initial_temperature=298.15,
        initial_component_mole_fractions={"N2": 0.79, "O2": 0.21}, num_spatial_nodes=10
    )

@pytest.fixture
def initial_co2_air_bed_config(zeolite_13x_adsorbent_config):
    """Fixture for an adsorber bed configured with air + CO2 initially."""
    return BedConfig(
        name="Bed A", length=0.5, diameter=0.05, adsorbent_name=zeolite_13x_adsorbent_config.name,
        initial_pressure=101325, initial_temperature=298.15,
        initial_component_mole_fractions={"N2": 0.78, "O2": 0.20, "CO2": 0.02}, num_spatial_nodes=10
    )

@pytest.fixture
def basic_adsorption_step():
    """Fixture for a basic adsorption cycle step."""
    return CycleStepConfig(
        name="Adsorption", type="Adsorption", duration=120,
        feed_pressure=500000, feed_temperature=298.15,
        feed_mole_fractions={"N2": 0.79, "O2": 0.21}, feed_flow_rate=0.01
    )

@pytest.fixture
def basic_blowdown_step():
    """Fixture for a basic blowdown cycle step."""
    return CycleStepConfig(
        name="Blowdown", type="Blowdown", duration=60, blowdown_pressure=100000
    )

@pytest.fixture
def basic_purge_step():
    """Fixture for a basic purge cycle step."""
    return CycleStepConfig(
        name="Purge", type="Purge", duration=90, purge_pressure=101325,
        purge_component="N2", purge_flow_rate_ratio=0.1
    )

@pytest.fixture
def basic_pressurization_step():
    """Fixture for a basic pressurization cycle step."""
    return CycleStepConfig(
        name="Pressurization", type="Pressurization", duration=90,
        feed_pressure=500000, feed_temperature=298.15,
        feed_mole_fractions={"N2": 0.79, "O2": 0.21}
    )

@pytest.fixture
def basic_solver_config():
    """Fixture for basic solver settings."""
    return SolverConfig(
        method="Radau", rtol=1e-4, atol=1e-7, max_step=10.0,
        n_cycles_to_steady_state=3, steady_state_tolerance=1e-2
    )

@pytest.fixture
def long_solver_config():
    """Fixture for solver settings configured for more cycles."""
    return SolverConfig(
        method="Radau", rtol=1e-4, atol=1e-7, max_step=5.0,
        n_cycles_to_steady_state=10, steady_state_tolerance=1e-3
    )

@pytest.fixture
def psa_air_separation_config(basic_components, basic_adsorbents, initial_air_bed_config,
                              basic_adsorption_step, basic_blowdown_step, basic_purge_step,
                              basic_pressurization_step, basic_solver_config):
    """
    Fixture for a complete PSA configuration for a 4-step air separation.
    """
    return PsaConfig(
        project_name="Air Separation Test",
        components=basic_components,
        adsorbents=basic_adsorbents,
        beds=[initial_air_bed_config],
        cycle_steps=[
            basic_adsorption_step,
            basic_blowdown_step,
            basic_purge_step,
            basic_pressurization_step
        ],
        solver_settings=basic_solver_config
    )

@pytest.fixture
def psa_co2_capture_config(extended_components, basic_adsorbents, initial_co2_air_bed_config,
                           basic_adsorption_step, basic_blowdown_step, basic_purge_step,
                           basic_pressurization_step, basic_solver_config):
    """
    Fixture for a complete PSA configuration for a CO2 capture scenario.
    Adjust adsorption/purge steps to reflect CO2 capture.
    """
    co2_adsorption = basic_adsorption_step.model_copy(update={
        "feed_mole_fractions": {"N2": 0.78, "O2": 0.20, "CO2": 0.02},
        "duration": 200, "feed_pressure": 800000 # Higher pressure for CO2 capture
    })
    co2_blowdown = basic_blowdown_step.model_copy(update={"blowdown_pressure": 50000}) # Lower blowdown for desorption
    co2_purge = basic_purge_step.model_copy(update={
        "purge_component": "CO2", "duration": 150, "purge_pressure": 200000 # Purge with CO2-rich gas at moderate pressure
    })
    co2_pressurization = basic_pressurization_step.model_copy(update={
        "feed_mole_fractions": {"N2": 0.78, "O2": 0.20, "CO2": 0.02},
        "duration": 100, "feed_pressure": 800000
    })

    return PsaConfig(
        project_name="CO2 Capture Test",
        components=extended_components,
        adsorbents=basic_adsorbents,
        beds=[initial_co2_air_bed_config],
        cycle_steps=[
            co2_adsorption,
            co2_blowdown,
            co2_purge,
            co2_pressurization
        ],
        solver_settings=basic_solver_config
    )

# Fixtures for direct model instantiation
@pytest.fixture
def gas_component_n2(nitrogen_component_config):
    return GasComponent(**nitrogen_component_config.model_dump())

@pytest.fixture
def adsorbent_zeolite_13x(zeolite_13x_adsorbent_config):
    return Adsorbent(**zeolite_13x_adsorbent_config.model_dump())

@pytest.fixture
def adsorber_bed_instance(initial_air_bed_config, adsorbent_zeolite_13x, basic_components, basic_solver_config):
    components = [GasComponent(**comp.model_dump()) for comp in basic_components]
    return AdsorberBed(
        bed_config=initial_air_bed_config,
        adsorbent=adsorbent_zeolite_13x,
        gas_components=components,
        solver_config=basic_solver_config
    )

@pytest.fixture
def psa_simulator_air_sep(psa_air_separation_config):
    return PsaSimulator(psa_air_separation_config)

@pytest.fixture
def psa_simulator_co2_capture(psa_co2_capture_config):
    return PsaSimulator(psa_co2_capture_config)
```

---

### `tests/unit/test_settings.py`

Unit tests for `src/cloud_psa_simulator/config/settings.py` and `src/cloud_psa_simulator/utils/validation.py`. These tests ensure that the configuration models correctly validate inputs, raising `ValidationError` for invalid data and accepting valid data.

```python
import pytest
import numpy as np
from pydantic import ValidationError

from src.cloud_psa_simulator.config.settings import (
    PsaConfig, ComponentConfig, AdsorbentConfig, BedConfig,
    CycleStepConfig, SolverConfig, IsothermComponentConfig
)
from src.cloud_psa_simulator.utils.validation import (
    validate_positive, validate_non_negative, validate_fraction,
    validate_sum_to_one, validate_all_positive, validate_isotherm_params
)

# --- Test Utility Validation Functions ---
def test_validate_positive():
    assert validate_positive(1.0, "test") == 1.0
    with pytest.raises(ValueError, match="must be a positive value"):
        validate_positive(0.0, "test")
    with pytest.raises(ValueError, match="must be a positive value"):
        validate_positive(-1.0, "test")

def test_validate_non_negative():
    assert validate_non_negative(0.0, "test") == 0.0
    assert validate_non_negative(1.0, "test") == 1.0
    with pytest.raises(ValueError, match="must be a non-negative value"):
        validate_non_negative(-1.0, "test")

def test_validate_fraction():
    assert validate_fraction(0.0, "test") == 0.0
    assert validate_fraction(0.5, "test") == 0.5
    assert validate_fraction(1.0, "test") == 1.0
    with pytest.raises(ValueError, match="must be between 0 and 1"):
        validate_fraction(-0.1, "test")
    with pytest.raises(ValueError, match="must be between 0 and 1"):
        validate_fraction(1.1, "test")

def test_validate_sum_to_one():
    assert validate_sum_to_one([0.5, 0.5], "test") == [0.5, 0.5]
    assert validate_sum_to_one([0.3, 0.7], "test") == [0.3, 0.7]
    with pytest.raises(ValueError, match="must be approximately 1.0"):
        validate_sum_to_one([0.4, 0.5], "test")
    with pytest.raises(ValueError, match="must be approximately 1.0"):
        validate_sum_to_one([0.6, 0.5], "test")

def test_validate_all_positive():
    assert validate_all_positive([1.0, 2.0], "test") == [1.0, 2.0]
    with pytest.raises(ValueError, match="All values in test must be positive"):
        validate_all_positive([1.0, 0.0], "test")
    with pytest.raises(ValueError, match="All values in test must be positive"):
        validate_all_positive([1.0, -1.0], "test")

def test_validate_isotherm_params_langmuir():
    # Valid Langmuir with 'b'
    params_b = {"Q_m": 1.0, "b": 0.1}
    assert validate_isotherm_params("Langmuir", params_b) == params_b
    
    # Valid Langmuir with 'b0' and 'Ea'
    params_b0_ea = {"Q_m": 1.0, "b0": 0.01, "Ea": -10000}
    assert validate_isotherm_params("Langmuir", params_b0_ea) == params_b0_ea

    # Missing Q_m
    with pytest.raises(ValueError, match="requires parameter 'Q_m'"):
        validate_isotherm_params("Langmuir", {"b": 0.1})
    
    # Missing b or b0/Ea
    with pytest.raises(ValueError, match="requires 'Q_m' and either 'b' or both 'b0' and 'Ea'"):
        validate_isotherm_params("Langmuir", {"Q_m": 1.0})
    
    # Invalid Q_m
    with pytest.raises(ValueError, match="must be a positive value"):
        validate_isotherm_params("Langmuir", {"Q_m": 0.0, "b": 0.1})

def test_validate_isotherm_params_sips():
    params = {"Q_m": 1.0, "b": 0.1, "n": 0.5}
    assert validate_isotherm_params("Sips", params) == params
    
    # Missing parameters
    with pytest.raises(ValueError, match="requires parameter 'n'"):
        validate_isotherm_params("Sips", {"Q_m": 1.0, "b": 0.1})
    
    # Invalid Q_m
    with pytest.raises(ValueError, match="must be a positive value"):
        validate_isotherm_params("Sips", {"Q_m": 0.0, "b": 0.1, "n": 0.5})

# --- Test Config Models ---

def test_component_config_valid(nitrogen_component_config):
    # Fixture already provides a valid config
    assert nitrogen_component_config.name == "N2"
    assert nitrogen_component_config.molecular_weight == 0.028

def test_component_config_invalid_molecular_weight():
    with pytest.raises(ValidationError):
        ComponentConfig(name="N2", molecular_weight=0, diffusivity_ref=1e-5, heat_capacity_gas=29.12)

def test_adsorbent_config_valid(zeolite_13x_adsorbent_config):
    # Fixture already provides a valid config
    assert zeolite_13x_adsorbent_config.name == "Zeolite 13X"
    assert zeolite_13x_adsorbent_config.porosity_bed == 0.35

def test_adsorbent_config_invalid_porosity():
    with pytest.raises(ValidationError):
        AdsorbentConfig(
            name="Bad Ads", density_bulk=700, density_solid=1100, porosity_bed=1.1,
            porosity_particle=0.45, heat_capacity_solid=900, particle_diameter=0.001,
            thermal_conductivity=0.2, isotherms={"N2": IsothermComponentConfig(type="Langmuir", params={"Q_m": 1, "b": 1})},
            mass_transfer_coeffs={"N2": 0.5}, heat_of_adsorption={"N2": -18000}
        )
    with pytest.raises(ValidationError):
        AdsorbentConfig(
            name="Bad Ads", density_bulk=700, density_solid=1100, porosity_bed=0.35,
            porosity_particle=0.0, heat_capacity_solid=900, particle_diameter=0.001,
            thermal_conductivity=0.2, isotherms={"N2": IsothermComponentConfig(type="Langmuir", params={"Q_m": 1, "b": 1})},
            mass_transfer_coeffs={"N2": 0.5}, heat_of_adsorption={"N2": -18000}
        )

def test_bed_config_valid(initial_air_bed_config):
    # Fixture already provides a valid config
    assert initial_air_bed_config.name == "Bed 1"
    assert initial_air_bed_config.length == 1.0

def test_bed_config_invalid_mole_fractions():
    with pytest.raises(ValidationError):
        BedConfig(
            name="Bed 2", length=1.0, diameter=0.1, adsorbent_name="Zeolite 13X",
            initial_pressure=101325, initial_temperature=298.15,
            initial_component_mole_fractions={"N2": 0.7, "O2": 0.2}, # Sums to 0.9
            num_spatial_nodes=10
        )
    with pytest.raises(ValidationError):
        BedConfig(
            name="Bed 2", length=1.0, diameter=0.1, adsorbent_name="Zeolite 13X",
            initial_pressure=101325, initial_temperature=298.15,
            initial_component_mole_fractions={"N2": 0.8, "O2": 0.3}, # Sums to 1.1
            num_spatial_nodes=10
        )
    with pytest.raises(ValidationError):
        BedConfig(
            name="Bed 2", length=1.0, diameter=0.1, adsorbent_name="Zeolite 13X",
            initial_pressure=101325, initial_temperature=298.15,
            initial_component_mole_fractions={"N2": 1.1, "O2": -0.1}, # Negative
            num_spatial_nodes=10
        )

def test_cycle_step_config_valid(basic_adsorption_step):
    # Fixture already provides a valid config
    assert basic_adsorption_step.name == "Adsorption"
    assert basic_adsorption_step.duration == 120

def test_cycle_step_config_invalid_duration():
    with pytest.raises(ValidationError):
        CycleStepConfig(name="Adsorption", type="Adsorption", duration=0)

def test_solver_config_valid(basic_solver_config):
    # Fixture already provides a valid config
    assert basic_solver_config.method == "Radau"
    assert basic_solver_config.rtol == 1e-4

def test_solver_config_invalid_rtol():
    with pytest.raises(ValidationError):
        SolverConfig(method="Radau", rtol=0)

def test_psa_config_valid(psa_air_separation_config):
    # Fixture already provides a valid config
    assert psa_air_separation_config.project_name == "Air Separation Test"
    assert len(psa_air_separation_config.components) == 2

def test_psa_config_duplicate_component_names(nitrogen_component_config):
    with pytest.raises(ValidationError, match="Component names must be unique"):
        PsaConfig(
            project_name="Dup Comp",
            components=[nitrogen_component_config, nitrogen_component_config],
            adsorbents=[], beds=[], cycle_steps=[], solver_settings=SolverConfig()
        )

def test_psa_config_adsorbent_not_found(basic_components, initial_air_bed_config):
    initial_air_bed_config.adsorbent_name = "NonExistentAdsorbent"
    with pytest.raises(ValidationError, match="Adsorbent 'NonExistentAdsorbent' specified for bed 'Bed 1' not found"):
        PsaConfig(
            project_name="Missing Ads",
            components=basic_components,
            adsorbents=[],
            beds=[initial_air_bed_config],
            cycle_steps=[],
            solver_settings=SolverConfig()
        )

def test_psa_config_undefined_bed_component(basic_components, zeolite_13x_adsorbent_config):
    bed_config_invalid = BedConfig(
        name="Bed 2", length=1.0, diameter=0.1, adsorbent_name=zeolite_13x_adsorbent_config.name,
        initial_pressure=101325, initial_temperature=298.15,
        initial_component_mole_fractions={"N2": 0.79, "UNKNOWN": 0.21}, # UNKNOWN component
        num_spatial_nodes=10
    )
    with pytest.raises(ValidationError, match="Initial component 'UNKNOWN' for bed 'Bed 2' not found in components list"):
        PsaConfig(
            project_name="Undefined Bed Comp",
            components=basic_components,
            adsorbents=[zeolite_13x_adsorbent_config],
            beds=[bed_config_invalid],
            cycle_steps=[],
            solver_settings=SolverConfig()
        )

def test_psa_config_undefined_cycle_step_component(basic_components, basic_adsorbents, initial_air_bed_config):
    invalid_step = CycleStepConfig(
        name="Adsorption", type="Adsorption", duration=120,
        feed_pressure=500000, feed_temperature=298.15,
        feed_mole_fractions={"N2": 0.79, "UNKNOWN": 0.21}, # UNKNOWN component in feed
        feed_flow_rate=0.01
    )
    with pytest.raises(ValidationError, match="Feed component mole fractions for step 'Adsorption' contain undefined components"):
        PsaConfig(
            project_name="Undefined Cycle Comp",
            components=basic_components,
            adsorbents=basic_adsorbents,
            beds=[initial_air_bed_config],
            cycle_steps=[invalid_step],
            solver_settings=SolverConfig()
        )

def test_adsorbent_config_isotherm_validation_in_config(zeolite_13x_adsorbent_config):
    # Test valid isotherm config directly
    assert zeolite_13x_adsorbent_config.isotherms["N2"].type == "Langmuir"
    assert "Q_m" in zeolite_13x_adsorbent_config.isotherms["N2"].params

    # Test invalid isotherm params
    bad_isotherm_config = zeolite_13x_adsorbent_config.model_copy(deep=True)
    bad_isotherm_config.isotherms["N2"].params = {"b": 0.1} # Missing Q_m
    with pytest.raises(ValidationError, match="requires parameter 'Q_m'"):
        AdsorbentConfig(**bad_isotherm_config.model_dump())

    bad_isotherm_config_2 = zeolite_13x_adsorbent_config.model_copy(deep=True)
    bad_isotherm_config_2.isotherms["N2"].params = {"Q_m": 0.0, "b": 0.1} # Q_m not positive
    with pytest.raises(ValidationError, match="must be a positive value"):
        AdsorbentConfig(**bad_isotherm_config_2.model_dump())
```

---

### `tests/unit/test_components.py`

Unit tests for `src/cloud_psa_simulator/models/components.py`, covering `GasComponent` and `Adsorbent` classes, including isotherm calculations.

```python
import pytest
import numpy as np

from src.cloud_psa_simulator.models.components import GasComponent, Adsorbent
from src.cloud_psa_simulator.config.settings import IsothermComponentConfig
from src.cloud_psa_simulator.utils.constants import R_GAS_CONSTANT

# --- Test GasComponent ---
def test_gas_component_initialization(nitrogen_component_config):
    n2 = GasComponent(**nitrogen_component_config.model_dump())
    assert n2.name == "N2"
    assert n2.molecular_weight == 0.028
    assert n2.diffusivity_ref == 1.8e-5
    assert n2.heat_capacity_gas == 29.12

def test_gas_component_default_diffusivity():
    comp = GasComponent(name="Test", molecular_weight=0.01, heat_capacity_gas=20)
    assert comp.diffusivity_ref == 1e-5 # Default value

def test_gas_component_henry_constant():
    comp = GasComponent(name="Test", molecular_weight=0.01, heat_capacity_gas=20, henry_constant=1e-5)
    assert comp.henry_constant == 1e-5
    comp_no_henry = GasComponent(name="Test", molecular_weight=0.01, heat_capacity_gas=20)
    assert comp_no_henry.henry_constant is None

# --- Test Adsorbent ---
def test_adsorbent_initialization(adsorbent_zeolite_13x):
    ads = adsorbent_zeolite_13x
    assert ads.name == "Zeolite 13X"
    assert ads.density_bulk == 700
    assert "N2" in ads.isotherms
    assert ads.isotherms["N2"].type == "Langmuir"
    assert ads.mass_transfer_coeffs["O2"] == 0.6
    assert ads.heat_of_adsorption["N2"] == -18000

# --- Test Adsorbent.get_isotherm_params_for_T ---
def test_get_isotherm_params_for_t_with_b(adsorbent_zeolite_13x):
    # Manually add a Langmuir isotherm with direct 'b'
    adsorbent_zeolite_13x.isotherms["H2"] = IsothermComponentConfig(type="Langmuir", params={"Q_m": 0.5, "b": 1e-8})
    iso_type, params = adsorbent_zeolite_13x.get_isotherm_params_for_T("H2", 300)
    assert iso_type == "Langmuir"
    assert params["Q_m"] == 0.5
    assert params["b"] == 1e-8 # 'b' should remain unchanged

def test_get_isotherm_params_for_t_with_b0_ea(adsorbent_zeolite_13x):
    # N2 and O2 in fixture use b0 and Ea
    T_test = 300.0
    
    # N2
    iso_type_n2, params_n2 = adsorbent_zeolite_13x.get_isotherm_params_for_T("N2", T_test)
    assert iso_type_n2 == "Langmuir"
    assert "b" in params_n2
    assert "b0" not in params_n2
    assert "Ea" not in params_n2
    
    expected_b_n2 = 1e-6 * np.exp(-(-18000) / (R_GAS_CONSTANT * T_test))
    assert np.isclose(params_n2["b"], expected_b_n2)

    # O2
    iso_type_o2, params_o2 = adsorbent_zeolite_13x.get_isotherm_params_for_T("O2", T_test)
    assert iso_type_o2 == "Langmuir"
    assert "b" in params_o2
    assert "b0" not in params_o2
    assert "Ea" not in params_o2
    
    expected_b_o2 = 5e-7 * np.exp(-(-16000) / (R_GAS_CONSTANT * T_test))
    assert np.isclose(params_o2["b"], expected_b_o2)

def test_get_isotherm_params_for_t_missing_component(adsorbent_zeolite_13x):
    with pytest.raises(ValueError, match="Isotherm data not found for component: Unknown"):
        adsorbent_zeolite_13x.get_isotherm_params_for_T("Unknown", 300)

# --- Test Adsorbent.get_equilibrium_loading ---
def test_get_equilibrium_loading_single_component_langmuir(adsorbent_zeolite_13x):
    T_test = 298.15
    P_test = 100000 # 1 bar
    
    # Single component N2
    partial_pressures_n2 = {"N2": P_test}
    loadings_n2 = adsorbent_zeolite_13x.get_equilibrium_loading(["N2"], partial_pressures_n2, T_test)
    
    iso_type_n2, params_n2 = adsorbent_zeolite_13x.get_isotherm_params_for_T("N2", T_test)
    b_n2 = params_n2["b"]
    Q_m_n2 = params_n2["Q_m"]
    expected_q_n2 = Q_m_n2 * b_n2 * P_test / (1 + b_n2 * P_test)
    
    assert "N2" in loadings_n2
    assert np.isclose(loadings_n2["N2"], expected_q_n2)
    assert "O2" not in loadings_n2 # Only requested component returned

def test_get_equilibrium_loading_extended_langmuir(adsorbent_zeolite_13x):
    T_test = 298.15
    P_total = 100000
    p_n2 = 0.79 * P_total
    p_o2 = 0.21 * P_total
    
    partial_pressures = {"N2": p_n2, "O2": p_o2}
    loadings = adsorbent_zeolite_13x.get_equilibrium_loading(["N2", "O2"], partial_pressures, T_test)
    
    iso_type_n2, params_n2 = adsorbent_zeolite_13x.get_isotherm_params_for_T("N2", T_test)
    b_n2 = params_n2["b"]
    Q_m_n2 = params_n2["Q_m"]

    iso_type_o2, params_o2 = adsorbent_zeolite_13x.get_isotherm_params_for_T("O2", T_test)
    b_o2 = params_o2["b"]
    Q_m_o2 = params_o2["Q_m"]

    denominator = 1 + b_n2 * p_n2 + b_o2 * p_o2
    expected_q_n2 = Q_m_n2 * b_n2 * p_n2 / denominator
    expected_q_o2 = Q_m_o2 * b_o2 * p_o2 / denominator

    assert "N2" in loadings and "O2" in loadings
    assert np.isclose(loadings["N2"], expected_q_n2)
    assert np.isclose(loadings["O2"], expected_q_o2)
    assert loadings["N2"] > loadings["O2"] # N2 is more strongly adsorbed on 13X

def test_get_equilibrium_loading_zero_partial_pressure(adsorbent_zeolite_13x):
    T_test = 298.15
    partial_pressures = {"N2": 0.0, "O2": 100000}
    loadings = adsorbent_zeolite_13x.get_equilibrium_loading(["N2", "O2"], partial_pressures, T_test)
    
    assert np.isclose(loadings["N2"], 0.0) # No N2, so no N2 adsorbed
    assert loadings["O2"] > 0 # O2 should still adsorb

def test_get_equilibrium_loading_very_high_pressure(adsorbent_zeolite_13x):
    T_test = 298.15
    P_high = 1e10 # Very high pressure
    partial_pressures = {"N2": P_high, "O2": 0.0}
    loadings = adsorbent_ze zeolite_13x.get_equilibrium_loading(["N2", "O2"], partial_pressures, T_test)
    
    iso_type_n2, params_n2 = adsorbent_zeolite_13x.get_isotherm_params_for_T("N2", T_test)
    Q_m_n2 = params_n2["Q_m"]
    
    # At very high pressure, loading should approach Q_m
    assert np.isclose(loadings["N2"], Q_m_n2, rtol=1e-3) # Relaxed rtol for numerical stability
    assert np.isclose(loadings["O2"], 0.0)

def test_get_equilibrium_loading_unsupported_isotherm_type(adsorbent_zeolite_13x):
    # Temporarily add a Sips isotherm for a component
    adsorbent_zeolite_13x.isotherms["H2"] = IsothermComponentConfig(type="Sips", params={"Q_m": 1.0, "b": 0.1, "n": 0.5})
    with pytest.raises(NotImplementedError, match="Multi-component isotherm support only for 'Langmuir' type"):
        adsorbent_zeolite_13x.get_equilibrium_loading(["N2", "H2"], {"N2": 1000, "H2": 1000}, 300)

def test_get_equilibrium_loading_missing_b_param(adsorbent_zeolite_13x):
    # Test case where 'b' is directly missing in isotherm params and no b0/Ea provided
    adsorbent_zeolite_13x.isotherms["Ar"] = IsothermComponentConfig(type="Langmuir", params={"Q_m": 1.0})
    with pytest.raises(ValueError, match="Langmuir isotherm for Ar missing 'b' parameter after temperature adjustment."):
        adsorbent_zeolite_13x.get_equilibrium_loading(["Ar"], {"Ar": 1000}, 300)

def test_get_equilibrium_loading_missing_partial_pressure(adsorbent_zeolite_13x):
    with pytest.raises(ValueError, match="Partial pressure for component N2 not provided."):
        adsorbent_zeolite_13x.get_equilibrium_loading(["N2", "O2"], {"O2": 1000}, 300)
```

---

### `tests/unit/test_bed_primitives.py`

Unit tests for primitive (non-ODE integration) methods of `src/cloud_psa_simulator/models/bed.py`.

```python
import pytest
import numpy as np

from src.cloud_psa_simulator.models.bed import AdsorberBed
from src.cloud_psa_simulator.models.components import GasComponent, Adsorbent
from src.cloud_psa_simulator.config.settings import (
    BedConfig, IsothermComponentConfig, CycleStepConfig
)

# --- Test AdsorberBed._initialize_state and state vector management ---
def test_bed_initialization(adsorber_bed_instance):
    bed = adsorber_bed_instance
    assert bed._num_spatial_nodes == 10
    assert bed._num_components == 2
    assert bed.component_names_list == ["N2", "O2"]
    
    # Check initial profiles (flat)
    assert np.all(bed.current_P_profile == 101325)
    assert np.all(bed.current_T_profile == 298.15)
    assert np.all(bed.current_y_profile[:, 0] == 0.79) # N2 mole fraction
    assert np.all(bed.current_y_profile[:, 1] == 0.21) # O2 mole fraction

    # Check initial adsorbed loadings (should be non-zero due to equilibrium)
    assert np.all(bed.current_q_profile > 0)
    # N2 is more strongly adsorbed, so q_N2 should be higher
    assert np.all(bed.current_q_profile[:, 0] > bed.current_q_profile[:, 1])

def test_get_profiles_from_state_vector(adsorber_bed_instance):
    bed = adsorber_bed_instance
    # Modify the initial state vector slightly to test extraction
    test_state_vector = bed._initial_state_vector.copy()
    test_state_vector[0] += 1000 # Change first pressure node
    test_state_vector[bed._num_spatial_nodes] += 5 # Change first temperature node
    
    # Change first N2 mole fraction
    test_state_vector[bed._num_spatial_nodes * 2] = 0.8
    test_state_vector[bed._num_spatial_nodes * 2 + 1] = 0.2 # Adjust O2 to sum to 1

    # Change first N2 adsorbed loading
    test_state_vector[bed._num_spatial_nodes * (2 + bed._num_components)] += 0.1

    P, T, y, q = bed._get_profiles_from_state_vector(test_state_vector)

    assert P[0] == 101325 + 1000
    assert T[0] == 298.15 + 5
    assert np.isclose(y[0, 0], 0.8)
    assert np.isclose(y[0, 1], 0.2)
    assert np.isclose(q[0, 0], bed.current_q_profile[0, 0] + 0.1)

    # Test mole fraction normalization
    bad_y_state_vector = bed._initial_state_vector.copy()
    bad_y_state_vector[bed._num_spatial_nodes * 2] = 0.5
    bad_y_state_vector[bed._num_spatial_nodes * 2 + 1] = 0.5 # Sums to 1
    bad_y_state_vector[bed._num_spatial_nodes * 2 + 2] = -0.1 # Should be clamped to 0
    bad_y_state_vector[bed._num_spatial_nodes * 2 + 3] = 0.1 # Should be adjusted
    
    _, _, y_normalized, _ = bed._get_profiles_from_state_vector(bad_y_state_vector)
    assert np.isclose(np.sum(y_normalized[0, :]), 1.0)
    assert np.all(y_normalized >= 0)


# --- Test AdsorberBed._calculate_axial_derivative ---
def test_calculate_axial_derivative_forward_flow(adsorber_bed_instance):
    bed = adsorber_bed_instance
    # Profile: 0, 1, 2, ..., 9
    profile = np.arange(bed._num_spatial_nodes, dtype=float)
    
    # Forward flow (z=0 to z=L)
    # Upwind differencing: deriv[i] = (profile[i] - profile[i-1]) / dx for i > 0
    # For deriv[0], using forward diff: (profile[1]-profile[0])/dx
    deriv = bed._calculate_axial_derivative(profile, flow_direction=1)
    
    # Expected: (profile[1]-profile[0])/dx, (profile[1]-profile[0])/dx, ..., (profile[N-1]-profile[N-2])/dx
    # For linear profile x = z, dx = L/(N-1)
    # Derivative should be approx 1 / dx
    expected_deriv_first = (profile[1] - profile[0]) / bed._dx
    expected_deriv_rest = (profile[1:] - profile[:-1]) / bed._dx
    
    assert np.isclose(deriv[0], expected_deriv_first)
    assert np.allclose(deriv[1:], expected_deriv_rest[1:]) # Compare from second element of expected_deriv_rest

    # A simple linear profile (e.g., [0, 1, 2, 3]) for dx=1 should give [1, 1, 1, 1] for forward diff at 0 and backward diff for rest
    # deriv[0] = (1-0)/dx = 1/dx
    # deriv[1] = (1-0)/dx = 1/dx
    # deriv[2] = (2-1)/dx = 1/dx
    # deriv[3] = (3-2)/dx = 1/dx
    # All derivatives should be 1/dx for this profile

    assert np.allclose(deriv, 1 / bed._dx)

def test_calculate_axial_derivative_reverse_flow(adsorber_bed_instance):
    bed = adsorber_bed_instance
    # Profile: 0, 1, 2, ..., 9
    profile = np.arange(bed._num_spatial_nodes, dtype=float)
    
    # Reverse flow (z=L to z=0)
    # Upwind differencing: deriv[i] = (profile[i+1] - profile[i]) / dx for i < N-1
    # For deriv[N-1], using backward diff: (profile[N-1]-profile[N-2])/dx
    deriv = bed._calculate_axial_derivative(profile, flow_direction=-1)

    # Expected: (profile[1]-profile[0])/dx, (profile[2]-profile[1])/dx, ..., (profile[N-1]-profile[N-2])/dx
    # For linear profile x = z, dx = L/(N-1)
    # deriv[0] = (1-0)/dx = 1/dx
    # deriv[1] = (2-1)/dx = 1/dx
    # ...
    # deriv[N-1] = ( (N-1) - (N-2) ) / dx = 1/dx

    assert np.allclose(deriv, 1 / bed._dx)

def test_calculate_axial_derivative_constant_profile(adsorber_bed_instance):
    bed = adsorber_bed_instance
    profile = np.full(bed._num_spatial_nodes, 5.0)
    
    deriv_forward = bed._calculate_axial_derivative(profile, flow_direction=1)
    deriv_reverse = bed._calculate_axial_derivative(profile, flow_direction=-1)
    
    assert np.all(deriv_forward == 0)
    assert np.all(deriv_reverse == 0)

# --- Test AdsorberBed.get_final_state ---
def test_get_final_state(adsorber_bed_instance):
    bed = adsorber_bed_instance
    final_state = bed.get_final_state()

    assert "P_profile" in final_state
    assert "T_profile" in final_state
    assert "y_profile" in final_state
    assert "q_profile" in final_state

    # Check that they are copies, not references
    final_state["P_profile"][0] += 1
    assert bed.current_P_profile[0] != final_state["P_profile"][0]
```

---

### `tests/integration/test_simulator_integration.py`

Integration tests for `src/cloud_psa_simulator/core/simulator.py` and its interaction with `AdsorberBed`.

```python
import pytest
import numpy as np
import pandas as pd

from src.cloud_psa_simulator.core.simulator import PsaSimulator
from src.cloud_psa_simulator.models.bed import AdsorberBed
from src.cloud_psa_simulator.config.settings import CycleStepConfig

def test_psa_simulator_initialization(psa_air_separation_config):
    simulator = PsaSimulator(psa_air_separation_config)
    assert simulator._config.project_name == "Air Separation Test"
    assert len(simulator._beds) == 1
    assert isinstance(simulator._beds["Bed 1"], AdsorberBed)
    assert len(simulator._cycle_steps) == 4

def test_psa_simulator_run_single_cycle(psa_simulator_air_sep):
    simulator = psa_simulator_air_sep
    cycle_df = simulator.run_cycle(cycle_num=1)
    
    assert isinstance(cycle_df, pd.DataFrame)
    assert not cycle_df.empty
    
    # Check expected columns
    expected_cols = ['time_abs', 'time_step_in_cycle', 'step_name', 'z_node', 'P', 'T']
    for comp in simulator._beds["Bed 1"].component_names_list:
        expected_cols.append(f'y_{comp}')
        expected_cols.append(f'q_{comp}')
    expected_cols.extend(['bed_name', 'cycle_num'])
    
    assert all(col in cycle_df.columns for col in expected_cols)
    
    # Check number of rows: 4 steps * 10 time_out per step * 10 nodes = 400 rows
    assert len(cycle_df) == len(simulator._cycle_steps) * 10 * simulator._beds["Bed 1"]._num_spatial_nodes
    assert cycle_df['cycle_num'].unique() == [1]
    
    # Verify bed state updated
    final_p = simulator._beds["Bed 1"].current_P_profile
    assert final_p[0] != simulator._beds["Bed 1"]._bed_config.initial_pressure # Should have changed from initial

def test_psa_simulator_run_simulation_to_steady_state(psa_simulator_air_sep):
    simulator = psa_simulator_air_sep
    # Basic solver config is n_cycles_to_steady_state=3, steady_state_tolerance=1e-2
    history_df = simulator.run_simulation()

    assert isinstance(history_df, pd.DataFrame)
    assert not history_df.empty

    # Check if cycles were run. Max cycles to steady state is 3. It could be less if steady state is hit early.
    assert history_df['cycle_num'].max() >= 1
    assert history_df['cycle_num'].max() <= 3

    # Check if the overall simulation history accumulated correctly
    total_expected_rows_if_3_cycles = 3 * len(simulator._cycle_steps) * 10 * simulator._beds["Bed 1"]._num_spatial_nodes
    assert len(history_df) <= total_expected_rows_if_3_cycles

    # A weak check: final bed state should ideally be "pseudo-steady"
    # This is hard to assert quantitatively without a reference.
    # We will check the internal _check_steady_state method logic instead.
    
def test_psa_simulator_check_steady_state_logic(psa_simulator_air_sep):
    simulator = psa_simulator_air_sep
    bed = simulator._beds["Bed 1"]

    # Initial state
    state1 = bed.get_final_state()
    # Simulate one step (to change state)
    bed.run_step(simulator._cycle_steps[0])
    state2 = bed.get_final_state()

    # If states are identical, should be steady
    assert simulator._check_steady_state({bed.name: state1}, {bed.name: state1}) is True

    # If states are different by more than tolerance, should not be steady
    # Ensure a significant change for this test
    state2_changed_P = state2['P_profile'].copy()
    state2_changed_P[0] *= 1.5 # 50% change
    state2_changed = state2.copy()
    state2_changed['P_profile'] = state2_changed_P
    
    # Original states are very different. Default tolerance is 1e-2. This should not be steady.
    assert simulator._check_steady_state({bed.name: state2_changed}, {bed.name: state1}) is False

    # Make states very close (within tolerance)
    state3_close = state1.copy()
    state3_close['P_profile'] = state1['P_profile'] * (1 + simulator._solver_settings.steady_state_tolerance / 2) # Within tolerance
    state3_close['T_profile'] = state1['T_profile'] * (1 + simulator._solver_settings.steady_state_tolerance / 2)
    state3_close['q_profile'] = state1['q_profile'] * (1 + simulator._solver_settings.steady_state_tolerance / 2)

    assert simulator._check_steady_state({bed.name: state3_close}, {bed.name: state1}) is True

def test_psa_simulator_with_multiple_beds(
    psa_air_separation_config, initial_co2_air_bed_config, two_adsorbents, extended_components
):
    # Create a config with two beds, different adsorbents, etc.
    multi_bed_config = psa_air_separation_config.model_copy(deep=True)
    multi_bed_config.beds.append(initial_co2_air_bed_config)
    multi_bed_config.adsorbents = two_adsorbents
    multi_bed_config.components = extended_components
    
    simulator = PsaSimulator(multi_bed_config)
    assert len(simulator._beds) == 2
    assert "Bed 1" in simulator._beds
    assert "Bed A" in simulator._beds

    history_df = simulator.run_simulation()
    assert len(history_df['bed_name'].unique()) == 2
    assert "Bed 1" in history_df['bed_name'].unique()
    assert "Bed A" in history_df['bed_name'].unique()

def test_psa_simulator_raises_error_on_ode_failure(psa_air_separation_config):
    # Intentionally create a configuration that might cause solver issues (e.g., extremely short step)
    faulty_config = psa_air_separation_config.model_copy(deep=True)
    faulty_config.cycle_steps[0].duration = 1e-6 # Very short duration
    faulty_config.solver_settings.max_step = 1e-7 # Max step larger than duration is sometimes fine, but tiny values can cause issues

    simulator = PsaSimulator(faulty_config)
    # Mock AdsorberBed.run_step to simulate a failure
    original_run_step = simulator._beds["Bed 1"].run_step
    
    def mock_run_step(step_config):
        if step_config.name == "Adsorption":
            raise RuntimeError("ODE solver failed for step Adsorption: Mock failure")
        return original_run_step(step_config)
    
    simulator._beds["Bed 1"].run_step = mock_run_step

    with pytest.raises(RuntimeError, match="ODE solver failed for step Adsorption"):
        simulator.run_simulation()

```

---

### `tests/validation/test_basic_cycle_validation.py`

Validation tests for `src/cloud_psa_simulator/models/bed.py` and `src/cloud_psa_simulator/core/simulator.py` by checking expected physical trends and approximate values.

```python
import pytest
import numpy as np
import pandas as pd

from src.cloud_psa_simulator.core.simulator import PsaSimulator
from src.cloud_psa_simulator.config.settings import CycleStepConfig

# Use a slightly relaxed steady state tolerance and more cycles for validation
@pytest.fixture
def validation_solver_config():
    return PsaSimulator.SolverConfig(
        method="Radau", rtol=1e-4, atol=1e-7, max_step=10.0,
        n_cycles_to_steady_state=5, steady_state_tolerance=5e-3
    )

@pytest.fixture
def psa_air_separation_validation_config(psa_air_separation_config, validation_solver_config):
    config = psa_air_separation_config.model_copy(deep=True)
    config.solver_settings = validation_solver_config
    # Set a more pronounced N2 adsorption for clearer validation
    config.adsorbents[0].isotherms["N2"].params = {"Q_m": 3.0, "b0": 2e-6, "Ea": -20000}
    config.adsorbents[0].isotherms["O2"].params = {"Q_m": 1.5, "b0": 8e-7, "Ea": -15000}
    config.adsorbents[0].mass_transfer_coeffs = {"N2": 0.3, "O2": 0.5} # N2 slower MT
    config.adsorbents[0].heat_of_adsorption = {"N2": -20000, "O2": -15000}
    
    return config

@pytest.fixture
def psa_co2_capture_validation_config(psa_co2_capture_config, validation_solver_config):
    config = psa_co2_capture_config.model_copy(deep=True)
    config.solver_settings = validation_solver_config
    # Set a more pronounced CO2 adsorption
    config.adsorbents[0].isotherms["CO2"].params = {"Q_m": 4.0, "b0": 5e-5, "Ea": -30000}
    config.adsorbents[0].mass_transfer_coeffs["CO2"] = 0.2 # Slower MT for CO2
    config.adsorbents[0].heat_of_adsorption["CO2"] = -30000
    return config

# --- Validation for Air Separation ---
def test_air_separation_adsorption_step_trends(psa_air_separation_validation_config):
    simulator = PsaSimulator(psa_air_separation_validation_config)
    history_df = simulator.run_simulation()
    
    # Get data for the last adsorption step
    last_cycle_df = history_df[history_df['cycle_num'] == history_df['cycle_num'].max()]
    adsorption_df = last_cycle_df[last_cycle_df['step_name'] == 'Adsorption']

    # At the start of adsorption, pressure is high, N2 is adsorbed, O2 is less adsorbed
    start_adsorption_bed_0 = adsorption_df[adsorption_df['time_step_in_cycle'] == adsorption_df['time_step_in_cycle'].min()]
    end_adsorption_bed_0 = adsorption_df[adsorption_df['time_step_in_cycle'] == adsorption_df['time_step_in_cycle'].max()]

    # Check pressure trend: Should increase from initial (pressurization leads to adsorption)
    # The pressure should be maintained high at the inlet (feed_pressure)
    assert start_adsorption_bed_0['P'].iloc[0] > psa_air_separation_validation_config.beds[0].initial_pressure
    assert np.isclose(end_adsorption_bed_0['P'].iloc[0], psa_air_separation_validation_config.cycle_steps[0].feed_pressure, rtol=0.05) # Inlet pressure should be feed pressure

    # Check temperature trend: Exothermic adsorption should increase temperature
    initial_T = start_adsorption_bed_0['T'].iloc[0]
    peak_T = adsorption_df['T'].max()
    assert peak_T > initial_T # Temperature should rise due to N2 adsorption

    # Check mole fraction trend: N2 preferentially adsorbed, so outlet O2 should be enriched
    # Inlet is 0.79 N2 / 0.21 O2. Product (outlet at z_node = bed length, for adsorption) should have lower N2, higher O2
    initial_y_n2 = psa_air_separation_validation_config.cycle_steps[0].feed_mole_fractions["N2"]
    initial_y_o2 = psa_air_separation_validation_config.cycle_steps[0].feed_mole_fractions["O2"]

    # At the end of the bed (product end for adsorption step)
    product_end_df = adsorption_df[adsorption_df['z_node'] == adsorption_df['z_node'].max()]
    final_y_n2_product = product_end_df['y_N2'].iloc[-1]
    final_y_o2_product = product_end_df['y_O2'].iloc[-1]
    
    # N2 is more adsorbed, so its fraction should be lower at the product end than feed
    assert final_y_n2_product < initial_y_n2
    assert final_y_o2_product > initial_y_o2 # O2 is enriched

    # Check adsorbed loading trend: N2 loading should be higher than O2
    q_n2_profile_end = end_adsorption_bed_0[end_adsorption_bed_0['z_node'] == end_adsorption_bed_0['z_node'].min()]['q_N2'].iloc[0]
    q_o2_profile_end = end_adsorption_bed_0[end_adsorption_bed_0['z_node'] == end_adsorption_bed_0['z_node'].min()]['q_O2'].iloc[0]
    assert q_n2_profile_end > q_o2_profile_end

def test_air_separation_blowdown_step_trends(psa_air_separation_validation_config):
    simulator = PsaSimulator(psa_air_separation_validation_config)
    history_df = simulator.run_simulation()

    last_cycle_df = history_df[history_df['cycle_num'] == history_df['cycle_num'].max()]
    blowdown_df = last_cycle_df[last_cycle_df['step_name'] == 'Blowdown']

    # Blowdown starts from high pressure, ends at low pressure
    start_P = blowdown_df['P'].iloc[0] # Inlet (z=0) at start of blowdown
    end_P_outlet = blowdown_df[blowdown_df['z_node'] == blowdown_df['z_node'].max()]['P'].iloc[-1] # Outlet (z=L) at end of blowdown

    assert start_P > psa_air_separation_validation_config.cycle_steps[1].blowdown_pressure
    assert np.isclose(end_P_outlet, psa_air_separation_validation_config.cycle_steps[1].blowdown_pressure, rtol=0.05) # Outlet pressure should reach target

    # Desorption is endothermic, so temperature should decrease
    start_T = blowdown_df['T'].iloc[0]
    min_T = blowdown_df['T'].min()
    assert min_T < start_T

    # Desorption should release adsorbed N2 (heavy component), leading to N2 enrichment in blowdown gas
    # This is often the waste product, enriched in the more adsorbed component
    initial_y_n2_blowdown_start = blowdown_df['y_N2'].iloc[0] # Inlet N2 at start of blowdown
    
    # Gas leaving the bed during blowdown (from outlet, z=L for feed-end blowdown)
    outlet_y_n2_blowdown = blowdown_df[blowdown_df['z_node'] == blowdown_df['z_node'].max()]['y_N2'].mean()
    
    # N2 content in blowdown should be higher than the O2 content
    outlet_y_o2_blowdown = blowdown_df[blowdown_df['z_node'] == blowdown_df['z_node'].max()]['y_O2'].mean()
    assert outlet_y_n2_blowdown > outlet_y_o2_blowdown
    
    # This blowdown should be N2-rich, meaning N2 mole fraction should be higher than initial feed
    # Initial air feed N2 = 0.79. Blowdown is expected to be enriched in adsorbed N2
    assert outlet_y_n2_blowdown > psa_air_separation_validation_config.cycle_steps[0].feed_mole_fractions["N2"]

def test_air_separation_purge_step_trends(psa_air_separation_validation_config):
    simulator = PsaSimulator(psa_air_separation_validation_config)
    history_df = simulator.run_simulation()
    
    last_cycle_df = history_df[history_df['cycle_num'] == history_df['cycle_num'].max()]
    purge_df = last_cycle_df[last_cycle_df['step_name'] == 'Purge']

    # Purge is typically at low pressure
    start_P = purge_df['P'].iloc[0] # Inlet (z=0) at start of purge
    end_P_outlet = purge_df[purge_df['z_node'] == purge_df['z_node'].min()]['P'].iloc[-1] # Outlet (z=0 for this simplified model)
    assert np.isclose(end_P_outlet, psa_air_separation_validation_config.cycle_steps[2].purge_pressure, rtol=0.05)

    # During purge, residual N2 (heavy component) should be removed, leaving O2 in the bed
    # After purge, the bed should be largely stripped of N2, ready for next adsorption
    # For a counter-current purge (which is implied by the `u_s_avg = -0.1` for purge)
    # the gas is fed from z=L and exits at z=0. The last component exiting z=0 at the end of purge should be the purged component
    # For this simplified model, u_s_avg is negative implying general outflow/reverse flow,
    # so purge_pressure is applied to the feed end (z=0) as outlet.
    
    # Check end of purge bed composition (should be O2-rich, as N2 was purged)
    end_purge_bed_state = purge_df[purge_df['time_step_in_cycle'] == purge_df['time_step_in_cycle'].max()]
    
    avg_y_n2_bed = end_purge_bed_state['y_N2'].mean()
    avg_y_o2_bed = end_purge_bed_state['y_O2'].mean()
    
    # Bed should be significantly depleted of N2 and enriched in O2 compared to initial air
    assert avg_y_n2_bed < psa_air_separation_validation_config.beds[0].initial_component_mole_fractions["N2"]
    assert avg_y_o2_bed > psa_air_separation_validation_config.beds[0].initial_component_mole_fractions["O2"]

def test_air_separation_pressurization_step_trends(psa_air_separation_validation_config):
    simulator = PsaSimulator(psa_air_separation_validation_config)
    history_df = simulator.run_simulation()
    
    last_cycle_df = history_df[history_df['cycle_num'] == history_df['cycle_num'].max()]
    pressurization_df = last_cycle_df[last_cycle_df['step_name'] == 'Pressurization']

    # Pressure should increase from purge pressure to adsorption pressure
    start_P = pressurization_df['P'].iloc[0]
    end_P = pressurization_df['P'].iloc[-1]
    
    assert end_P > start_P
    assert np.isclose(end_P, psa_air_separation_validation_config.cycle_steps[3].feed_pressure, rtol=0.05)

    # Temperature should increase due to exothermic adsorption during pressurization
    start_T = pressurization_df['T'].iloc[0]
    end_T = pressurization_df['T'].iloc[-1]
    assert end_T > start_T # Temperature should rise

    # Mole fractions should move towards feed composition, but N2 will adsorb, so gas will be slightly O2 enriched
    initial_y_n2 = psa_air_separation_validation_config.cycle_steps[3].feed_mole_fractions["N2"]
    initial_y_o2 = psa_air_separation_validation_config.cycle_steps[3].feed_mole_fractions["O2"]

    end_press_bed_0 = pressurization_df[pressurization_df['z_node'] == pressurization_df['z_node'].min()]
    final_y_n2_inlet = end_press_bed_0['y_N2'].iloc[-1]
    final_y_o2_inlet = end_press_bed_0['y_O2'].iloc[-1]
    
    assert final_y_n2_inlet < initial_y_n2 # N2 adsorbs, so gas phase N2 concentration drops
    assert final_y_o2_inlet > initial_y_o2 # O2 is enriched in the gas phase
```

---

### `tests/benchmarks/test_performance_benchmarks.py`

Benchmark tests using `pytest-benchmark` to assess the performance of the simulator under varying computational loads.

```python
import pytest
import numpy as np
import pandas as pd

from src.cloud_psa_simulator.core.simulator import PsaSimulator
from src.cloud_psa_simulator.config.settings import SolverConfig

# Mark these tests as benchmarks
pytestmark = pytest.mark.benchmark

def create_config_with_nodes_and_cycles(base_config, num_spatial_nodes, n_cycles):
    """Helper to create a PsaConfig with specified spatial nodes and cycles."""
    config = base_config.model_copy(deep=True)
    config.beds[0].num_spatial_nodes = num_spatial_nodes
    config.solver_settings = SolverConfig(
        method="Radau", rtol=1e-4, atol=1e-7, max_step=10.0,
        n_cycles_to_steady_state=n_cycles, steady_state_tolerance=1e-1 # Relax tolerance for faster benchmark convergence
    )
    return config

# --- Benchmarks for Spatial Discretization ---
@pytest.mark.parametrize("num_spatial_nodes", [10, 20, 50])
def test_benchmark_spatial_nodes(benchmark, psa_air_separation_config, num_spatial_nodes):
    config = create_config_with_nodes_and_cycles(psa_air_separation_config, num_spatial_nodes, n_cycles=3)
    simulator = PsaSimulator(config)
    benchmark.name = f"spatial_nodes_{num_spatial_nodes}"
    benchmark(simulator.run_simulation)

# --- Benchmarks for Number of Cycles ---
@pytest.mark.parametrize("n_cycles", [1, 3, 5])
def test_benchmark_num_cycles(benchmark, psa_air_separation_config, n_cycles):
    config = create_config_with_nodes_and_cycles(psa_air_separation_config, num_spatial_nodes=20, n_cycles=n_cycles)
    simulator = PsaSimulator(config)
    benchmark.name = f"cycles_{n_cycles}"
    benchmark(simulator.run_simulation)

# --- Benchmarks for Different Solver Methods ---
@pytest.mark.parametrize("solver_method", ["Radau", "BDF"])
def test_benchmark_solver_method(benchmark, psa_air_separation_config, solver_method):
    config = psa_air_separation_config.model_copy(deep=True)
    config.solver_settings.method = solver_method
    config.solver_settings.n_cycles_to_steady_state = 2 # Shorten for quicker benchmark
    config.solver_settings.steady_state_tolerance = 1e-1 # Relax for quicker benchmark
    simulator = PsaSimulator(config)
    benchmark.name = f"solver_method_{solver_method}"
    benchmark(simulator.run_simulation)

# --- Benchmarks for Different Applications (Air Sep vs CO2 Capture) ---
def test_benchmark_air_separation(benchmark, psa_air_separation_config):
    config = create_config_with_nodes_and_cycles(psa_air_separation_config, num_spatial_nodes=20, n_cycles=3)
    simulator = PsaSimulator(config)
    benchmark.name = "app_air_separation"
    benchmark(simulator.run_simulation)

def test_benchmark_co2_capture(benchmark, psa_co2_capture_config):
    # CO2 capture config might have different component counts/isotherms
    config = create_config_with_nodes_and_cycles(psa_co2_capture_config, num_spatial_nodes=20, n_cycles=3)
    simulator = PsaSimulator(config)
    benchmark.name = "app_co2_capture"
    benchmark(simulator.run_simulation)
```

---

### Instructions to Run Tests

1.  **Ensure all dependencies are installed:**
    ```bash
    pip install -e .[dev]
    ```
2.  **Navigate to the project's root directory** (where `pytest.ini` and `pyproject.toml` are located).
3.  **Run all tests (unit, integration, validation, and coverage):**
    ```bash
    pytest
    ```
4.  **Run only unit tests:**
    ```bash
    pytest tests/unit/
    ```
5.  **Run only integration tests:**
    ```bash
    pytest tests/integration/
    ```
6.  **Run only validation tests:**
    ```bash
    pytest tests/validation/
    ```
7.  **Run benchmark tests:**
    ```bash
    pytest -m benchmark --benchmark-sort=mean --benchmark-histogram=.
    ```
    This will execute tests marked with `@pytest.mark.benchmark`, sort results by mean execution time, and generate histograms for each benchmark.

This comprehensive test suite ensures that the "Intelligent Multi-Fidelity PSA Digital Twin" model's core functionalities are correct, robust, and performant, providing a solid foundation for advanced PSA simulation and control.