#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .anisotropic import anisotropic
from .boussinesq import boussinesq
from .coefficients import coefficients
from .constant import constant
from .nasa_9_piecewise_polynomial import nasa_9_piecewise_polynomial
from .number_of_coefficients import number_of_coefficients
from .option import option
from .orthotropic import orthotropic
from .piecewise_linear import piecewise_linear
from .piecewise_polynomial import piecewise_polynomial
from .var_class import var_class


class latent_heat(Group):
    """'latent_heat' child."""

    fluent_name = "latent-heat"

    child_names = [
        "option",
        "constant",
        "boussinesq",
        "coefficients",
        "number_of_coefficients",
        "piecewise_polynomial",
        "nasa_9_piecewise_polynomial",
        "piecewise_linear",
        "anisotropic",
        "orthotropic",
        "var_class",
    ]

    option: option = option
    """
    option child of latent_heat
    """
    constant: constant = constant
    """
    constant child of latent_heat
    """
    boussinesq: boussinesq = boussinesq
    """
    boussinesq child of latent_heat
    """
    coefficients: coefficients = coefficients
    """
    coefficients child of latent_heat
    """
    number_of_coefficients: number_of_coefficients = number_of_coefficients
    """
    number_of_coefficients child of latent_heat
    """
    piecewise_polynomial: piecewise_polynomial = piecewise_polynomial
    """
    piecewise_polynomial child of latent_heat
    """
    nasa_9_piecewise_polynomial: nasa_9_piecewise_polynomial = (
        nasa_9_piecewise_polynomial
    )
    """
    nasa_9_piecewise_polynomial child of latent_heat
    """
    piecewise_linear: piecewise_linear = piecewise_linear
    """
    piecewise_linear child of latent_heat
    """
    anisotropic: anisotropic = anisotropic
    """
    anisotropic child of latent_heat
    """
    orthotropic: orthotropic = orthotropic
    """
    orthotropic child of latent_heat
    """
    var_class: var_class = var_class
    """
    var_class child of latent_heat
    """