from pyroll.core import RollPass, Roll


@RollPass.Roll.hookspec
def matrix_method_results(roll_pass: RollPass, roll: Roll):
    """Result of the matrix method."""


@RollPass.Roll.hookspec
def disk_elements(roll_pass: RollPass, roll: Roll):
    """Disk elements of the work roll"""


@RollPass.Roll.hookspec
def deflection(roll_pass, roll):
    """Mechanical deflection of the work roll for a roll pass"""


@RollPass.Roll.hookspec
def inclination(roll_pass, roll):
    """Mechanical inclination of the work roll for a roll pass"""


@RollPass.Roll.hookspec
def bending_moment(roll_pass, roll):
    """Bending moment resulting from roll force of the roll pass"""


@RollPass.Roll.hookspec
def shear_force(roll_pass, roll):
    """Shear stress resulting from roll force of the roll pass"""
