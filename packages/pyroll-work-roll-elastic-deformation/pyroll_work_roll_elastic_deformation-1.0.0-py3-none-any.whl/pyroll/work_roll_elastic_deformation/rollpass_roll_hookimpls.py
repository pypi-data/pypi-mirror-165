from pyroll.core import RollPass, Roll

from pyroll.work_roll_elastic_deformation.matix_method import MatrixMethod


@RollPass.Roll.hookimpl
def disk_elements(roll_pass: RollPass, roll: Roll):
    return roll.body.create_disk_elements(roll_pass)


@RollPass.Roll.hookimpl
def matrix_method_results(roll_pass: RollPass, roll: Roll):
    matrix_method = MatrixMethod()
    return matrix_method.solve(roll_pass, roll)


@RollPass.Roll.hookimpl
def deflection(roll_pass, roll):
    return [vector[0] for vector in roll_pass.roll.matrix_method_results]


@RollPass.Roll.hookimpl
def inclination(roll_pass, roll):
    return [vector[1] for vector in roll_pass.roll.matrix_method_results]


@RollPass.Roll.hookimpl
def bending_moment(roll_pass, roll):
    return [vector[2] for vector in roll_pass.roll.matrix_method_results]


@RollPass.Roll.hookimpl
def shear_force(roll_pass, roll):
    return [vector[3] for vector in roll_pass.roll.matrix_method_results]
