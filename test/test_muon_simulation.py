import unittest
import os
from unittest.mock import Mock
import sys
from BeautifulReport import BeautifulReport
sys.path.append('/Users/gregyoungforever/Documents/ISEP2023-2024/Simulation/src')
from muon_simulation import MuonSimulator
import numpy as np
from unittest.mock import Mock
from pyramid_model import Pyramid, Cavity
class TestMuonSimulator(unittest.TestCase):
  """
  Unit tests for the MuonSimulator class.
  """
  @classmethod
  def setUp(self):
    self.altitude = 10000  
    self.energy_range = (10, 1000)  
    self.mean_free_path = 1000  

    self.pyramid = Pyramid(200, 140)
    self.cavity = Cavity([100,100,65], 20)
    self.simulator = MuonSimulator(
      altitude=self.altitude,
      energy_range=self.energy_range,
      pyramid=self.pyramid,
      cavity=self.cavity,
      mean_free_path=self.mean_free_path
    )

  def test_generate_muons(self):
    n_muons = 100
    muons = self.simulator.generate_muons(n_muons)
    self.assertEqual(len(muons), n_muons)
    for position, direction, energy in muons:
      self.assertEqual(position[2], self.altitude)
      self.assertTrue(self.energy_range[0] <= energy <= self.energy_range[1])

  def test_simulate_muons_trajectory(self):
    self.pyramid.is_inside = Mock(return_value = True)
    self.pyramid.path_length = Mock(return_value = 100)
    self.cavity.is_inside = Mock(return_value = True)

    muon = (np.array([self.pyramid.base_length/2, self.pyramid.base_length/2, self.altitude]), np.array([0, 0, -1]), 500)
    result = self.simulator.simulate_muons_trajectory(muon)
    self.assertIsNotNone(result)

    intersects, position, energy = result
    
    self.assertTrue(intersects) 
    self.assertGreater(energy, 0)  
    
    self.pyramid.is_inside.assert_called()
    self.pyramid.path_length.assert_called_with(muon[0], muon[1])

  def test_simulate_muons_trajectory_outside(self):
    self.pyramid.is_inside = Mock(return_value = False)
    muon = (np.array([self.pyramid.base_length/2, self.pyramid.base_length/2, self.altitude]), np.array([0, 0, -1]), 500)
    result = self.simulator.simulate_muons_trajectory(muon)
    self.assertIsNone(result)

    self.pyramid.is_inside.assert_called()
  
  def test_simulate_muons_trajectory_absorbed(self):
    self.pyramid.is_inside = Mock(return_value = True)
    self.pyramid.path_length = Mock(return_value = 1000000)
    self.cavity.is_inside = Mock(return_value = False)
    muon = (np.array([self.pyramid.base_length/2, self.pyramid.base_length/2, self.altitude]), np.array([0, 0, -1]), 500)
    result = self.simulator.simulate_muons_trajectory(muon)
    intersects, _, energy = result
    self.assertIsNotNone(result)
    self.assertFalse(intersects)
    self.assertEqual(energy, 0)
    self.pyramid.is_inside.assert_called()
    self.pyramid.path_length.assert_called_with(muon[0], muon[1])

if __name__ == '__main__':
    suit = unittest.TestSuite()
    suit.addTest(unittest.makeSuite(TestMuonSimulator))
    report_path = os.getcwd() + '/testReport'
    run = BeautifulReport(suit)
    run.report(filename = "test of muon simulation", description = "test of muon simulation", report_dir = report_path)