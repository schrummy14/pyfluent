from ansys.fluent.core import LOG
from ansys.fluent.launcher.launcher import launch_fluent
from ansys.fluent.session import Session

try:
    from ansys.fluent.meshing import tui as meshing_tui
    from ansys.fluent.solver import tui as solver_tui

    Session.MeshingTui.register_module(meshing_tui)
    Session.SolverTui.register_module(solver_tui)
except ImportError:
    pass


def set_log_level(level):
    """Set logging level

    Parameters
    ----------
    level : Any
        Any of the logging level (CRITICAL, ERROR, WARNING, INFO, DEBUG)
        in string or enum format
    """
    LOG.set_level(level)


def enable_logging_to_stdout():
    """Enable logging to stdout"""
    LOG.enable_logging_to_stdout()


def disable_logging_to_stdout():
    """Disable logging to stdout"""
    LOG.disable_logging_to_stdout()


def enable_logging_to_file(filepath: str = None):
    """Enable logging to file

    Parameters
    ----------
    filepath : str, optional
        filapath, a default filepath will be chosen if filepath is not
        passed
    """
    LOG.enable_logging_to_file(filepath)


def disable_logging_to_file():
    """Disable logging to file"""
    LOG.disable_logging_to_file()