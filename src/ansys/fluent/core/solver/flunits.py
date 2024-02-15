"""Module for accessing Fluent units labels per quantity type.

Example
-------
>>> units = get_si_unit_for_fluent_quantity("pressure")

The following code is employed to translate the source data
into Python data structures:

from ansys.fluent.core.filereader import lispy
import re
from pprint import pprint

fl_unit_subs = {'deg': 'radian', 'rad':'radian',}
def replace_units(match):
    return fl_unit_subs[match.group(0)]

def substitute_fl_units_with_py_units(fl_units_dict):
    subs = {}
    for k, v in fl_units_dict.items():
    new_val = re.sub('|'.join(r'\b%s\b' % re.escape(s) for s in fl_unit_subs), replace_units, v)
    if new_val != v:
        subs[k] = new_val
    print("Substitutions:")
    for k, v in subs.items():
        print(f"'{fl_units_dict[k]}' -> '{v}' for '{k}'")
        print("\n")
        fl_units_dict.update(subs)
    return fl_units_dict

def make_python_fl_unit_table(scheme_unit_table):
    as_list = lispy.parse(scheme_unit_table)[1][1]
    as_dict = { x[0]:x[1][3].split('"')[1] for x in as_list }
    return substitute_fl_units_with_py_units(as_dict)
"""

_fl_unit_table = {
    "acceleration": "m s^-2",
    "angle": "radian",
    "angular-velocity": "radian s^-1",
    "area": "m^2",
    "area-inverse": "m^-2",
    "collision-rate": "m^-3 s^-1",
    "concentration": "kmol m^-3",
    "contact-resistance": "m^2 K W^-1",
    "contact-resistance-vol": "Ohm m^3",
    "crank-angle": "radian",
    "crank-angular-velocity": "rev min^-1",
    "current": "A",
    "current-density": "A m^-2",
    "current-vol-density": "A m^-3",
    "density": "kg m^-3",
    "density*specific-energy": "J m^-3",
    "density*specific-heat": "J m^-3 K^-1",
    "density*velocity": "kg m^-2 s^-1",
    "density-gradient": "kg m^-4",
    "density-inverse": "m^3 kg^-1",
    "depth": "m",
    "elec-charge": "A h",
    "elec-charge-density": "A s m^-3",
    "elec-conductivity": "S m^-1",
    "elec-contact-resistance": "Ohm m^2",
    "elec-field": "V m^-1",
    "elec-permittivity": "farad m^-1",
    "elec-resistance": "Ohm",
    "elec-resistivity": "Ohm m",
    "energy": "J",
    "energy-density": "J/m2",
    "force": "N",
    "force*time-per-volume": "N s m^-3",
    "force-per-area": "N m^-2",
    "force-per-volume": "N m^-3",
    "frequency": "Hz",
    "gas-constant": "J kg^-1 K^-1",
    "heat-flux": "W m^-2",
    "heat-flux-resolved": "m K s^-1",
    "heat-generation-rate": "W m^-3",
    "heat-transfer-coefficient": "W m^-2 K^-1",
    "ignition-energy": "J mol^-1",
    "kinematic-viscosity": "m^2 s^-1",
    "length": "m",
    "length-inverse": "m^-1",
    "length-time-inverse": "m^-1 s^-1",
    "mag-permeability": "H m^-1",
    "mass": "kg",
    "mass-diffusivity": "m^2 s^-1",
    "mass-flow": "kg s^-1",
    "mass-flow-per-depth": "kg m^-1 s^-1",
    "mass-flow-per-time": "kg s^-2",
    "mass-flux": "kg m^-2 s^-1",
    "mass-transfer-rate": "kg m^-3 s^-1",
    "mole-con-henry-const": "Pa m^3 kgmol^-1",
    "mole-specific-energy": "J kgmol^-1",
    "mole-specific-entropy": "J kgmol^-1 K^-1",
    "mole-transfer-rate": "kgmol m^-3 s^-1",
    "molec-wt": "kg kmol^-1",
    "moment": "N m",
    "moment-of-inertia": "kg m^2",
    "nucleation-rate": "m^-3 s^-1",
    "number-density": "m^-3",
    "particles-conc": "1.e15-particles/kg",
    "particles-rate": "1.e15 m^-3 s^-1",
    "percentage": "%",
    "power": "W",
    "power-per-time": "W s^-1",
    "pressure": "Pa",
    "pressure-2nd-time-derivative": "Pa s^-2",
    "pressure-gradient": "Pa m^-1",
    "pressure-time-deriv-sqr": "Pa^2 s^-2",
    "pressure-time-derivative": "Pa s^-1",
    "resistance": "m^-1",
    "site-density": "kgmol m^-2",
    "soot-formation-constant-unit": "kg N^-1 m^-1 s^-1",
    "soot-limiting-nuclei-rate": "1e+15-particles/m3-s",
    "soot-linear-termination": "m^3 s^-1",
    "soot-oxidation-constant": "kg m kgmol^-1 K^-0.5 s^-1",
    "soot-pre-exponential-constant": "1.e15 kg^-1 s^-1",
    "soot-sitespecies-concentration": "kmol m^-3",
    "soot-surface-growth-scale-factor": "kg m kgmol^-1 s^-1",
    "source-elliptic-relaxation-function": "kg m^-3 s^-2",
    "source-energy": "W m^-3",
    "source-kinetic-energy": "kg m^-1 s^-3",
    "source-mass": "kg m^-3 s^-1",
    "source-momentum": "N m^-3",
    "source-specific-dissipation-rate": "kg m^-3 s^-2",
    "source-temperature-variance": "K^2 m^-3 s^-1",
    "source-turbulent-dissipation-rate": "kg m^-1 s^-4",
    "source-turbulent-viscosity": "kg m^-1 s^-2",
    "specific-area": "m^2 kg^-1",
    "specific-energy": "J kg^-1",
    "specific-heat": "J kg^-1 K^-1",
    "spring-constant": "N m^-1",
    "spring-constant-angular": "N m radian^-1",
    "stefan-boltzmann-constant": "W m^-2 K^-4",
    "surface-density": "kg m^-2",
    "surface-mole-transfer-rate": "kgmol m^-2 s^-1",
    "surface-tension": "N m^-1",
    "surface-tension-gradient": "N m^-1 K^-1",
    "temperature": "K",
    "temperature-difference": "K",
    "temperature-gradient": "K m^-1",
    "temperature-inverse": "K^-1",
    "temperature-variance": "K^2",
    "thermal-conductivity": "W m^-1 K^-1",
    "thermal-resistance": "m^2 K W^-1",
    "thermal-resistivity": "m K W^-1",
    "thermophoretic-diffusivity": "kg m^2 s^-2",
    "time": "s",
    "time-inverse": "s^-1",
    "time-inverse-cubed": "s^-3",
    "time-inverse-squared": "s^-2",
    "turb-kinetic-energy-production": "kg m^-1 s^-3",
    "turbulent-energy-diss-rate": "m^2 s^-3",
    "turbulent-energy-diss-rate-gradient": "m s^-3",
    "turbulent-kinetic-energy": "m^2 s^-2",
    "turbulent-kinetic-energy-gradient": "m s^-2",
    "univ-gas-constant": "J K^-1 kgmol^-1",
    "velocity": "m s^-1",
    "viscosity": "kg m^-1 s^-1",
    "viscosity-consistency-index": "kg s^n-2 m^-1",
    "voltage": "V",
    "volume": "m^3",
    "volume-flow-rate": "m^3 s^-1",
    "volume-flow-rate-per-depth": "m^3 s^-1 m^-1",
    "volume-inverse": "m^-3",
    "wave-length": "Angstrom",
    "youngs-modulus": "N m^-2",
}


def get_si_unit_for_fluent_quantity(quantity: str, unit_table: dict = None):
    """Get the SI unit for the given Fluent quantity.

    Raises
    ------
    TypeError
        If ``quantity`` is not a string instance.
    """
    try:
        if quantity.startswith("'"):
            quantity = quantity[1:]
    except AttributeError:
        # not a string
        raise TypeError(
            "Invalid quantity argument type in get_si_unit_for_fluent_quantity."
        )
    return (unit_table or _fl_unit_table)[quantity]