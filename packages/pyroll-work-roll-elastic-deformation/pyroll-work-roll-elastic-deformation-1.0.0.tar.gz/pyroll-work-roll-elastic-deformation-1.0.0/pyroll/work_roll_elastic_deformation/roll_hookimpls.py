from pyroll.core import Roll


@Roll.hookimpl
def youngs_modulus(roll: Roll):
    raise ValueError("You must provide a Young's modulus to use the pyroll-work-roll-elastic-deformation plugin.")


@Roll.hookimpl
def body(roll: Roll):
    raise ValueError("You must provide a roll body to use the pyroll-work-roll-elastic-deformation plugin.")
