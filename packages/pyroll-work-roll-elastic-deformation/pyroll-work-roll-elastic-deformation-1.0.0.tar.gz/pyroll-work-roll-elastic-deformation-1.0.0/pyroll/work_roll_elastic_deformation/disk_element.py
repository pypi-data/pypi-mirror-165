from dataclasses import dataclass

import numpy as np
from shapely.geometry import Polygon, Point


@dataclass
class DiskElement:
    body: Polygon
    surface_load: float = None

    def __post_init__(self):
        self.width = Point(self.body.bounds[0], 0).distance(Point(self.body.bounds[2], 0))
        self.center = (self.body.bounds[0] + self.body.bounds[2]) / 2
        self.diameter = self.body.area / self.width
        self.area_moment_of_inertia = np.pi / 4 * (self.diameter / 2) ** 4
