import visualization;
import os
import json5
import pyramid_model
from muon_detector import MuonDetector
from muon_simulation import MuonSimulator

n_detectors = [1,2]
base_dir = os.path.dirname(os.path.abspath(__file__))

settings_path = os.path.join(base_dir, '..', 'config', 'settings.json')


with open(settings_path, 'r') as settings_file:
    settings = json5.load(settings_file)  


# visualization.visualize_pyramid(settings)

pyramid, cavity = pyramid_model.initialize_pyramid_and_cavity(settings)
muon_detector_1 = MuonDetector(settings, n_detectors[0])
muon_detector_2 = MuonDetector(settings, n_detectors[1])
muon_simulator = MuonSimulator(settings, pyramid, cavity, [muon_detector_1, muon_detector_2])
muons = muon_simulator.generate_muons(100000)
for m in muons:
  muon_simulator.simulate_muons_trajectory(m)
muon_detector_1.detected_muons

