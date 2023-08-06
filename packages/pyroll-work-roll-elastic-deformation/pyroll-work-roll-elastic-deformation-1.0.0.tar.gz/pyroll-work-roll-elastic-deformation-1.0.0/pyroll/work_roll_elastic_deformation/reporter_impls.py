import math

import numpy as np
from matplotlib import pyplot as plt
from pyroll.core import RollPass
from pyroll.ui import Reporter
from pyroll.utils import for_units
from shapely.affinity import translate
from shapely.geometry import Polygon
from shapely.ops import clip_by_rect


def cut_roll_in_half(roll_contour: Polygon):
    return clip_by_rect(roll_contour, -math.inf, roll_contour.bounds[1], math.inf, roll_contour.bounds[3] / 2)


def move_roll_contour_upper_bound_to_origin(roll_contour: Polygon):
    return translate(roll_contour, xoff=0, yoff=-roll_contour.bounds[3])


def plot_neutral_line_deflection(ax: plt.Axes, roll_pass: RollPass):
    x_values = [disk.center for disk in roll_pass.roll.disk_elements]
    ax.grid(lw=0.5)
    ax.plot(x_values, roll_pass.roll.deflection[0:-1])


def plot_roll_contour(ax: plt.Axes, roll_pass: RollPass):
    half_contour = cut_roll_in_half(roll_pass.roll.body.contour)
    contour = move_roll_contour_upper_bound_to_origin(half_contour)
    ax.spines['left'].set_position(('axes', 0))
    ax.grid(lw=0.5)
    ax.plot(*contour.exterior.xy, color='black', alpha=0.75)


@Reporter.hookimpl
@for_units(RollPass)
def unit_properties(unit: RollPass):
    return dict(
        work_roll_elastic_modulus=f"{unit.roll.youngs_modulus}",
        work_roll_max_deflection=f"{np.max(unit.roll.deflection)}"
    )


@Reporter.hookimpl
@for_units(RollPass)
def unit_plot(unit: RollPass):
    """Plot roll pass contour and its profiles"""
    fig: plt.Figure = plt.figure(constrained_layout=True, figsize=(9, 6))
    ax: plt.Axes = fig.subplots(2, 1, sharex=True)
    fig.subplots_adjust(hspace=0)

    plot_neutral_line_deflection(ax[0], unit)
    fig.suptitle('Work roll deflection', fontsize=16)
    plot_roll_contour(ax[1], unit)

    return fig
