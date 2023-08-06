from dataclasses import dataclass

import numpy as np
from pyroll.core import RollPass, Roll
from scipy.optimize import fsolve
from shapely.geometry import Point


@dataclass
class MatrixMethod:

    @staticmethod
    def transition_matrix(disk_width: float, youngs_modulus: float, load: float, area_moment_of_inertia: float):
        return np.array([[1, disk_width, disk_width ** 2 / (2 * youngs_modulus * area_moment_of_inertia),
                          disk_width ** 3 / (6 * youngs_modulus * area_moment_of_inertia),
                          load * disk_width ** 4 / (24 * youngs_modulus * area_moment_of_inertia)],
                         [0, 1, disk_width / (youngs_modulus * area_moment_of_inertia),
                          disk_width ** 2 / (2 * youngs_modulus * area_moment_of_inertia),
                          load * disk_width ** 3 / (6 * youngs_modulus * area_moment_of_inertia)],
                         [0, 0, 1, disk_width, load * disk_width ** 2 / 2],
                         [0, 0, 0, 1, load * disk_width],
                         [0, 0, 0, 0, 1]])

    @staticmethod
    def initial_solution(roll_pass: RollPass, roll: Roll):

        force_application_point = Point(roll.body.distance_to_groove, roll.body.mean_diameter / 2)
        bearing_force_point_a = Point(roll.body.left_joint_center.x, roll.body.mean_diameter / 2)
        mean_area_moment_of_inertia = np.pi / 4 * (roll.body.mean_diameter / 2) ** 4
        distance_a_to_force = force_application_point.distance(bearing_force_point_a)
        distance_b_to_force = roll.body.distance_between_joint_centers - distance_a_to_force

        initial_shear_force = distance_b_to_force / roll.body.distance_between_joint_centers * roll_pass.roll_force
        initial_bending_angle = (roll_pass.roll_force * distance_a_to_force * distance_b_to_force * (
                roll.body.distance_between_joint_centers + distance_b_to_force)) / (
                                        6 * roll.youngs_modulus * mean_area_moment_of_inertia * roll.body.distance_between_joint_centers)
        return np.array([initial_bending_angle, -initial_shear_force])

    def state_variables(self, left_bearing_vector: np.ndarray, roll: Roll):
        vectors = [left_bearing_vector]
        for disk_element in roll.disk_elements:
            current_vector = np.dot(self.transition_matrix(roll.body.disk_width,
                                                           roll.youngs_modulus,
                                                           disk_element.surface_load,
                                                           disk_element.area_moment_of_inertia), vectors[-1])
            vectors.append(current_vector)
        return vectors

    def solve_fun(self, initial_solution, roll: Roll):
        initial_left_bearing_vector = np.array([0, initial_solution[0], 0, initial_solution[1], 1])
        vectors = self.state_variables(initial_left_bearing_vector, roll)
        return [vectors[-1][0], vectors[-1][2]]

    def solve(self, roll_pass: RollPass, roll: Roll):
        initial_solution = self.initial_solution(roll_pass, roll)
        final_solution = fsolve(self.solve_fun, initial_solution, args=roll)
        final_left_bearing_vector = np.array([0, final_solution[0], 0, final_solution[1], 1])

        return self.state_variables(final_left_bearing_vector, roll)
