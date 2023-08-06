from ashdisperse.ashdisperse import setup, solve
from ashdisperse.core import AshDisperseResult
from ashdisperse.interface import load_inputs, save_inputs, set_met, set_parameters
from ashdisperse.met import load_met, save_met, wind_plot
from ashdisperse.params import (
    copy_parameters,
    load_parameters,
    save_parameters,
    update_parameters,
)
from ashdisperse.version import __version__

__author__ = "Mark Woodhouse"
