import os
import unittest
import sys

from BeautifulReport import BeautifulReport
sys.path.append('/Users/gregyoungforever/Documents/ISEP2023-2024/Simulation/src')
from pyramid_model import Pyramid, Cavity

class TestPyramid(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base_length = 200
        cls.height = 140

    def setUp(self):
        self.pyramid = Pyramid(self.base_length, self.height)

    def test_is_inside_with_points_inside_pyramid(self):
        # Test points inside the pyramid
        self.assertTrue(self.pyramid.is_inside([50, 50, 50]), "Point should be inside the pyramid")

    def test_is_inside_with_points_on_pyramid_surface(self):
        # Test points on the surface of the pyramid
        self.assertTrue(self.pyramid.is_inside([100, 100, 100]), "Point on the surface should be considered inside")

    def test_is_inside_with_points_outside_pyramid(self):
        # Test points outside the pyramid
        self.assertFalse(self.pyramid.is_inside([300, 300, 300]), "Point should be outside the pyramid")

    def test_path_length_with_ray_entering_from_top(self):
        # Test path length for a ray entering from the top of the pyramid
        expected_length = self.height
        actual_length = self.pyramid.path_length([100, 100, self.height + 10], [0, 0, -1])
        self.assertAlmostEqual(actual_length, expected_length, msg="Path length should match pyramid height")


class TestCavity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cavity_center = [100, 100, 65]
        cls.cavity_radius = 20

    def setUp(self):
        self.cavity = Cavity(self.cavity_center, self.cavity_radius)

    def test_ray_intersects_cavity(self):
        # Test a ray intersecting the cavity
        position = [80, 80, 65]  # A point outside the cavity
        direction = [1, 1, 0]  # Direction vector towards the cavity center
        self.assertTrue(self.cavity.does_ray_intersect(position, direction), "Ray should intersect the cavity")

    def test_ray_on_cavity_surface(self):
        # Test a ray on the surface of the cavity
        position = [100, 120, 65]  # A point on the surface of the cavity
        direction = [0, -1, 0]  # Direction vector pointing away from the cavity center
        self.assertTrue(self.cavity.does_ray_intersect(position, direction), "Ray on cavity surface should intersect the cavity")

    def test_ray_outside_cavity(self):
        # Test a ray outside and not intersecting the cavity
        position = [150, 150, 65]  # A point outside the cavity
        direction = [1, 0, 0]  # Direction vector pointing away from the cavity
        self.assertFalse(self.cavity.does_ray_intersect(position, direction), "Ray should not intersect the cavity")
    

if __name__ == '__main__':
  testClass = [TestPyramid, TestCavity]
  for i in range(testClass.__len__()):
    suit = unittest.TestSuite()
    suit.addTest(unittest.makeSuite(testClass[i]))
    report_path = os.getcwd() + '/testReport'
    run = BeautifulReport(suit)
    if i == 0:
      run.report(filename = "test of pyramid model", description = "test of pramid model", report_dir = report_path)
    else:
      run.report(filename = "test of cavity model", description = "test of cavity model", report_dir = report_path)