#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .constant import constant
from .field_name import field_name
from .option import option
from .profile_name import profile_name
from .udf import udf


class mrf_omega(Group):
    """'mrf_omega' child."""

    fluent_name = "mrf-omega"

    child_names = ["option", "constant", "profile_name", "field_name", "udf"]

    option: option = option
    """
    option child of mrf_omega
    """
    constant: constant = constant
    """
    constant child of mrf_omega
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of mrf_omega
    """
    field_name: field_name = field_name
    """
    field_name child of mrf_omega
    """
    udf: udf = udf
    """
    udf child of mrf_omega
    """