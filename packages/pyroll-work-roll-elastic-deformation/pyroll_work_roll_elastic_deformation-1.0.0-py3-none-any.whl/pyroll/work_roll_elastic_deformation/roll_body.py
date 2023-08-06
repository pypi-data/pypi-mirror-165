import logging
import math

from typing import Optional, Union

import numpy as np
from cad_to_shapely import dxf
from dataclasses import dataclass

from pyroll.core import RollPass
from shapely.affinity import translate
from shapely.geometry import Polygon, Point
from shapely.ops import clip_by_rect, unary_union

from pyroll.work_roll_elastic_deformation.disk_element import DiskElement


@dataclass
class RollBody:
    """Class representing the body of the work roll."""
    joint_diameter: float
    joint_length: float
    distance_to_groove: float
    contour: Optional[Union[Polygon, None]] = None
    path_to_body: Optional[Union[str, None]] = None
    discretization_count: int = 5000
    log = logging.getLogger(__name__)

    def __post_init__(self):
        if self.contour and self.path_to_body is None:
            raise ValueError("You must provide either a roll body as a Polygon or a valid path to a .dxf file.")
        elif self.contour is None and self.path_to_body is not None:
            try:
                contour = dxf.DxfImporter(self.path_to_body)
                contour.process(spline_delta=0.01)
                contour.polygonize(force_zip=False)
                self.contour = unary_union(contour.polygons)
            except OSError:
                self.log.error("Path to drawing is not valid. Please check path.")
                raise OSError("Path to drawing is not valid. Please check path.")
        elif self.contour and self.path_to_body is not None:
            self.log.info("You provided a roll body as a polygon and the drawing. Continued with Polygon.")

        self.contour = self.correct_contour_position()
        self.left_joint_center = Point(self.contour.bounds[0] + self.joint_length / 2, self.joint_diameter / 2)
        self.right_joint_center = Point(self.contour.bounds[2] - self.joint_length / 2, self.joint_diameter / 2)
        self.distance_between_joint_centers = self.left_joint_center.distance(self.right_joint_center)
        self.body_with_half_joints = clip_by_rect(self.contour, self.left_joint_center.x, -math.inf, self.right_joint_center.x, math.inf)
        self.disk_width = self.distance_between_joint_centers / self.discretization_count
        self.mean_diameter = (self.contour.bounds[1] + self.contour.bounds[3]) / 2

    def horizontal_offset_from_origin(self):
        """Horizontal offset of the rolls reference point to the origin."""
        ideal_point = Point(-self.joint_length, 0)
        real_reference_point = Point(self.contour.bounds[0], 0)

        if real_reference_point.x < 0:
            horizontal_offset = ideal_point.distance(real_reference_point)
        elif real_reference_point.x > 0:
            horizontal_offset = - ideal_point.distance(real_reference_point)
        else:
            return 0
        return horizontal_offset

    def vertical_offset_from_origin(self):
        """Vertical offset of the rolls reference point to the origin."""
        origin = Point(0, 0)
        real_reference_point = Point(0, self.contour.bounds[1])

        if real_reference_point.y < 0:
            vertical_offset = origin.distance(real_reference_point)
        elif real_reference_point.y > 0:
            vertical_offset = - origin.distance(real_reference_point)
        else:
            return 0
        return vertical_offset

    def correct_contour_position(self):
        """Moving the reference point to the origin."""
        horizontal_offset = self.horizontal_offset_from_origin()
        vertical_offset = self.vertical_offset_from_origin()
        roll_with_correct_coordinates = translate(self.contour, xoff=horizontal_offset, yoff=vertical_offset)

        return roll_with_correct_coordinates

    def cut_disk_elements_from_body(self, i: int):
        """Cut disk elements from the roll body."""
        left_disk_boundary = self.body_with_half_joints.bounds[0] + i * self.disk_width
        right_disk_boundary = self.body_with_half_joints.bounds[0] + (i + 1) * self.disk_width
        return clip_by_rect(self.body_with_half_joints, left_disk_boundary, -math.inf, right_disk_boundary, math.inf)

    def calculate_disk_load(self, disk: DiskElement, roll_pass: RollPass):

        if "lendl_width" not in roll_pass.__dict__:
            load_distribution_width = roll_pass.out_profile.width

        else:
            load_distribution_width = roll_pass.lendl_width

        if (self.distance_to_groove - load_distribution_width / 2) <= disk.center <= (self.distance_to_groove + load_distribution_width / 2):

            large_half_axis = load_distribution_width / 2
            small_half_axis = 2 * roll_pass.roll_force / (large_half_axis * np.pi)
            horizontal_ellipse_center = self.distance_to_groove
            vertical_ellipse_center = 0

            load = (small_half_axis * np.sqrt(
                large_half_axis ** 2 - disk.center ** 2 + 2 * disk.center * horizontal_ellipse_center - horizontal_ellipse_center ** 2)) / large_half_axis + vertical_ellipse_center

        else:
            load = 0

        return load

    def create_disk_elements(self, roll_pass: RollPass):
        """Create disk elements."""
        disks = []
        for i in range(self.discretization_count):
            disk_body = self.cut_disk_elements_from_body(i)
            disk = DiskElement(body=disk_body)
            disk.surface_load = self.calculate_disk_load(disk=disk, roll_pass=roll_pass)
            disks.append(disk)
        return disks
