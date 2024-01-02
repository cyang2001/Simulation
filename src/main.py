import visualization;
import numpy as np
import os
import json5
import pyramid_model
from muon_detector import MuonDetector
from muon_simulation import MuonSimulator
from data_processing import MuonDataAnalysis

def run_simulation():
  base_dir = os.path.dirname(os.path.abspath(__file__))

  settings_path = os.path.join(base_dir, '..', 'config', 'settings.json')

  n_detectors = [1, 2]
  with open(settings_path, 'r') as settings_file:
      settings = json5.load(settings_file)  


  # visualization.visualize_pyramid(settings)

  pyramid, cavity = pyramid_model.initialize_pyramid_and_cavity(settings)


  muon_detector_1 = MuonDetector(settings, n_detectors[0])
  muon_detector_2 = MuonDetector(settings, n_detectors[1])
  muon_detectors = [muon_detector_1, muon_detector_2]
  muon_simulation = MuonSimulator(settings, pyramid, cavity, muon_detectors)
  res = muon_simulation.simulate_muons_parallel(1600)
  return res
if __name__ == '__main__':
  run_simulation()
  res = run_simulation()
  #print(res)



