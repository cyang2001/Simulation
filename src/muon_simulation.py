import numpy as np

class MuonSimulator:
  def __init__(self, altitude, energy_range, pyramid, cavity, mean_free_path):
    """
    Initialize the MuonSimulator class.

    Parameters:
    altitude (float): The altitude at which the muon simulation is performed.
    energy_range (tuple): The range of energy for the generated muons.
    pyramid (Pyramid): The pyramid model.
    cavity (Cavity): The cavity model.
    mean_free_path (float): The mean free path of muons.
    Returns:
    None
    """
    self.altitude = altitude
    self.energy_range = energy_range
    self.pyramid = pyramid
    self.cavity = cavity
    self.mean_free_path = mean_free_path

  def generate_muons(self, n_muons):
    """
    Generate muons based on the given number.

    Parameters:
    n_muons (int): The number of muons to generate.

    Returns:
    list: A list of tuples containing the position, direction, and energy of each generated muon.
    """
    muons = []
    for _ in range(n_muons):
      position = np.array([0, 0, self.altitude])
      phi = np.random.uniform(0, 2 * np.pi)
      theta = np.arccos(np.random.uniform(-1, 1))
      direction = np.array([np.sin(theta) * np.cos(phi), np.sin(theta) * np.sin(phi), -np.cos(theta)])
      energy = np.random.uniform(self.energy_range[0], self.energy_range[1])
      muons.append((position, direction, energy))
    return muons

  def simulate_muons_trajectory(self, muons):
    """
    Simulates the trajectory of muons.

    Parameters:
    - muons: A tuple containing the position, direction, and energy of the muons.

    Returns:
    - If the muon is outside the pyramid, returns None.
    - If the muon intersects with the cavity, returns a tuple with True, the new position, and the energy.
    - If the muon is absorbed, returns a tuple with False, the new position, and 0 energy.
    - Otherwise, returns a tuple with True, the new position, and the energy.
    """
    position, direction, energy = muons
    if not self.pyramid.is_inside(position):
      return None
    length = self.pyramid.path_length(position, direction)
    if self.cavity.is_inside(position, direction):
      return True, position + direction * length, energy
    if np.random.random() < self.absorption_probability(length):
      return False, position + direction * length, 0 
    return True, position + direction * length, energy
  
  def absorption_probability(self, length):
    
    return 1 - np.exp(-length / self.mean_free_path)